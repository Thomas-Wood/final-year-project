import requests
import datetime


class simulatedSensorTemplate:
    def __init__(self, serverRoot, datastreamID, logging=True):
        self.serverRoot = serverRoot
        self.datastreamID = datastreamID
        self.logging = logging

    def sendObservation(self):
        response = requests.post(
            self.serverRoot + 'Datastreams(' + self.datastreamID + ')/Observations', data=self.generateObservation()
        )
        if self.logging:
            print("Observation available at: " + response.headers['location'])
        return response.headers['location']

    def generateObservation(self):
        timeFormat = "%Y-%m-%dT%H:%M:%SZ"
        currentTime = datetime.datetime.now().strftime(timeFormat)
        data = '{"phenomenonTime": "' + currentTime + \
            '", "result": ' + self.getNextResult() + '}'
        return data

    def getNextResult(self):
        return '1'
