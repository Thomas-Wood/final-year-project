import requests
import json


def postToServer(file, entityName):
    selfLinks = []
    fileAddress = 'FROST-setup-json-data/' + file
    with open(fileAddress, 'r') as rawData:
        jsonData = json.load(rawData)
        for entity in jsonData['values']:
            response = requests.post(
                'http://localhost:8080/FROST-Server/v1.0/' + entityName, data=json.dumps(entity)
            )
            selfLinks.append(response.headers['location'])
    return selfLinks


# Set up OberservedProperties
observedPropertiesLinks = postToServer(
    'ObservedProperties.json', 'ObservedProperties')
print("ObservedProperties created at:")
for link in observedPropertiesLinks:
    print(link)

# Set up Locations
locationLinks = postToServer(
    'Locations.json', 'Locations')
print("Locations created at:")
for link in locationLinks:
    print(link)

# Set up Things (link to location)
thingLinks = postToServer(
    'Things.json', 'Things')
print("Things created at:")
for link in thingLinks:
    print(link)

# Set up Datastream (with sensor, link to ObserveredProperty and Thing)
datastreamLinks = postToServer(
    'DatastreamsAndSensors.json', 'Datastreams')
print("Datastreams created at:")
for link in datastreamLinks:
    print(link)

# Send test observations
# observationLinks = postToServer(
#     'SampleObservations.json', 'Datastreams(1)/Observations')
# print("Observations created at:")
# for link in observationLinks:
#     print(link)
