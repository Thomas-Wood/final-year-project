import logging
import requests
import json
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/selectServer', methods=['GET'])
def home():
    """The main landing page of the site.
    This is where the user enters which server address they are using.
    """

    return render_template('selectServer.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Connect to the mongoDB server and retrieve any customisations
    # TODO

    addressParameters = get_current_parameters()

    # Connect to the FROST server and get all the Things and their Datastreams that should be visible
    serverAddress = request.args.get('address')
    thingsAndDatastreams = json.loads(bytes.decode(
        requests.get(serverAddress + '/Things?$expand=Datastreams').content))['value']

    # Sort Datastreams by ID
    for thing in thingsAndDatastreams:
        thing['Datastreams'].sort(key=lambda datastream: datastream['@iot.id'])

    # Sort Things by ID
    thingsAndDatastreams.sort(key=lambda thing: thing['@iot.id'])

    # If any FROST entities are missing from MongoDB, add them with default settings
    # TODO

    # Pass data to template to dynamically generate the checkboxes
    # TODO

    return render_template('dashboard.html',
                           thingsAndDatastreams=thingsAndDatastreams,
                           addressParameters=addressParameters)


@app.route('/alerts', methods=['GET'])
def alerts():

    addressParameters = get_current_parameters()

    alerts = []

    return render_template('alerts.html', alerts=alerts, addressParameters=addressParameters)


@app.route('/rules', methods=['GET'])
def rules():

    addressParameters = get_current_parameters()

    # Connect to MongoDB and get the rules for this server
    client = MongoClient(
        "mongodb+srv://AD-DB-User:%26h8Xt2Q%23V%26SG@cluster0.pglda.mongodb.net/SensorThingsDashboard")
    serverAddress = request.args.get('address')
    collectionName = 'Rules-' + serverAddress
    db = client['SensorThingsDashboard'][collectionName]
    myCursor = None
    myCursor = db.find()
    rules = list(myCursor)

    return render_template('rules.html', rules=rules, addressParameters=addressParameters, serverAddress=serverAddress)


@app.route('/add_rule', methods=['POST'])
def add_rule():

    serverAddress = request.args.get('address')

    # Connect to MongoDB and get the rules for this server
    client = MongoClient(
        "mongodb+srv://AD-DB-User:%26h8Xt2Q%23V%26SG@cluster0.pglda.mongodb.net/SensorThingsDashboard")
    collectionName = 'Rules-' + serverAddress
    db = client['SensorThingsDashboard'][collectionName]

    rule = {
        "dataForm": request.form['dataForm'],
        "dataStreamID": request.form['dataStream'][0],
        "comparator": request.form['comparator'],
        "limit": request.form['limit'],
        "severity": request.form['severity']
    }
    db.insert_one(rule)

    return redirect(url_for('rules', address=serverAddress), 301)


@app.route('/delete_rule', methods=['POST'])
def delete_rule():

    serverAddress = request.args.get('address')

    # Connect to MongoDB and get the rules for this server
    client = MongoClient(
        "mongodb+srv://AD-DB-User:%26h8Xt2Q%23V%26SG@cluster0.pglda.mongodb.net/SensorThingsDashboard")
    collectionName = 'Rules-' + serverAddress
    db = client['SensorThingsDashboard'][collectionName]

    # Search for rule and delete it
    myquery = {"_id": ObjectId(request.form['ruleID'])}
    db.delete_one(myquery)

    return redirect(url_for('rules', address=serverAddress), 301)


@app.errorhandler(500)
def server_error(error):
    logging.exception('An error occurred during a request.')
    return render_template('error.html', errorCode=500), 500


@app.errorhandler(404)
def page_not_found(error):
    logging.warning('Missing page requested')
    return render_template('error.html', errorCode=404), 404


def get_current_parameters():
    currentURL = request.url
    endOfMainAddressIndex = currentURL.find('?')
    addressParameters = currentURL[endOfMainAddressIndex:]

    return addressParameters


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
