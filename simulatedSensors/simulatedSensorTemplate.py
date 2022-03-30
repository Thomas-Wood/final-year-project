import requests
import datetime


class simulatedSensorTemplate:
    def __init__(self, serverRoot, datastreamID, logging=True):
        self.serverRoot = serverRoot
        self.datastreamID = datastreamID
        self.logging = logging
        self.lastResult = None
        self.lastResultTime = None
        self.firstTimeSetup()

    # Overriden by child classes
    def firstTimeSetup(self):
        pass

    def sendObservation(self):
        response = requests.post(
            self.serverRoot + 'Datastreams(' + self.datastreamID + ')/Observations', data=self.generateObservation()
        )
        if self.logging:
            print("Observation available at: " + response.headers['location'])
        return response.headers['location']

    def generateObservation(self):
        self.lastResultTime.datetime.datetime.now()
        timeFormat = "%Y-%m-%dT%H:%M:%SZ"
        formattedTime = self.lastResultTime.strftime(timeFormat)
        self.lastResult = self.getNextResult()
        data = '{"phenomenonTime": "' + formattedTime + \
            '", "result": ' + str(self.lastResult) + '}'
        return data

    # Overriden by child classes
    def getNextResult(self):
        return '1'
