import json
import time
import requests
import schedule
import datetime
from pymongo import MongoClient
import statistics

baseMongoURL = "mongodb+srv://AD-DB-User:%26h8Xt2Q%23V%26SG@cluster0.pglda.mongodb.net/SensorThingsDashboard"


def checkForNewAlerts():
    # Connect to MongoDB and get a list of all the collections (rules and alerts for every server)
    client = MongoClient(baseMongoURL)
    listOfCollections = client['SensorThingsDashboard'].list_collection_names()
    filteredListOfCollections = list(filter(filterRules, listOfCollections))

    for collectionName in filteredListOfCollections:
        # Connect to MongoDB and get the rules for this server
        client = MongoClient(baseMongoURL)
        db = client['SensorThingsDashboard'][collectionName]
        myCursor = None
        myCursor = db.find()
        rulesCollection = list(myCursor)

        # Get just the server address from the collection name
        serverAddress = collectionName[6:]

        # Calculate if each rule is currently true or false
        for rule in rulesCollection:
            rule = calculateState(rule, serverAddress)

        # Get all alerts without end dates
        db = client['SensorThingsDashboard']['Alerts-' + serverAddress]
        myCursor = None
        myquery = {"endTime": ""}
        myCursor = db.find(myquery)
        activeAlertsCollection = list(myCursor)

        for rule in rulesCollection:
            # If a rule is currently triggered and there is no active alert, make an alert
            if rule['currentState'] == True and not ruleHasActiveAlert(rule, activeAlertsCollection):
                alert_data = {
                    "startTime": str(datetime.datetime.now().timestamp()),
                    "endTime": "",
                    "ruleID": str(rule['_id']),
                    "datastreamID": str(rule['dataStreamID']),
                    "dataForm": str(rule['dataForm']),
                    "comparator": str(rule['comparator']),
                    "limit": str(rule['limit']),
                    "severity": str(rule['severity'])
                }
                db.insert_one(alert_data)
                print("Added new alert!")
            # If a rule is not triggered but there is an active alert, end the alert
            elif rule['currentState'] == False and ruleHasActiveAlert(rule, activeAlertsCollection):
                myquery = {"$and": [{"endTime": ""},
                                    {"ruleID": str(rule['_id'])}
                                    ]}
                newvalues = {"$set": {"endTime": str(
                    datetime.datetime.now().timestamp())}}

                db.update_one(myquery, newvalues)
                print("Ending Alert")


def ruleHasActiveAlert(rule, activeAlerts):
    for alert in activeAlerts:
        if alert['ruleID'] == str(rule['_id']):
            return True
    return False


def calculateState(rule, serverAddress):
    serverAddress = serverAddress + \
        "/Datastreams(" + rule['dataStreamID'] + ")/Observations"

    if (rule['dataForm'] == 'Most Recent Value'):

        serverAddress += "?$top=1&$orderby=phenomenonTime desc"
        result = getJSONData(serverAddress)['value'][0]
        rule['currentState'] = evaluateComparator(
            result['result'], rule['comparator'], rule['limit'])

    elif (rule['dataForm'] == '1 min Average'):

        resultsFromTime = (datetime.datetime.now(
        ) - datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

        serverAddress += "?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
        mean = statistics.mean(getMultiPartJSONDataAsList(serverAddress))

        rule['currentState'] = evaluateComparator(
            mean, rule['comparator'], rule['limit'])

    elif (rule['dataForm'] == '5 min Average'):

        resultsFromTime = (datetime.datetime.now(
        ) - datetime.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")

        serverAddress += "?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
        mean = statistics.mean(getMultiPartJSONDataAsList(serverAddress))

        rule['currentState'] = evaluateComparator(
            mean, rule['comparator'], rule['limit'])

    elif (rule['dataForm'] == '1 hour Average'):

        resultsFromTime = (datetime.datetime.now(
        ) - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

        serverAddress += "?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
        mean = statistics.mean(getMultiPartJSONDataAsList(serverAddress))

        rule['currentState'] = evaluateComparator(
            mean, rule['comparator'], rule['limit'])

    return rule


def evaluateComparator(operand1, comparator, operand2):
    if (comparator == "Less Than"):
        return float(operand1) < float(operand2)
    elif (comparator == "More Than"):
        return float(operand1) > float(operand2)
    else:
        return "Error in comparator name"


def getJSONData(url):
    response = requests.get(url)
    decoded_response = response.content.decode("UTF-8")
    data = json.loads(decoded_response)
    return data


def getMultiPartJSONDataAsList(url):
    response = requests.get(url)
    decoded_response = response.content.decode("UTF-8")
    data = json.loads(decoded_response)
    resultsList = []

    if ('@iot.nextLink' in data):
        resultsList = getMultiPartJSONDataAsList(data['@iot.nextLink'])

    for observation in data['value']:
        resultsList.append(observation['result'])

    return resultsList


def filterRules(url):
    if (url.startswith('Rules-')):
        return True
    else:
        return False


# Check for new alerts every 5 seconds
checkForNewAlerts()
schedule.every(5).seconds.do(checkForNewAlerts)
while True:
    schedule.run_pending()
    time.sleep(1)
