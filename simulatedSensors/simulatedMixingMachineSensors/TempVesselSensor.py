import simulatedSensorTemplate
import datetime


class TempVesselSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 18  # Measured in C
        self.upperLimit = 42  # Measured in C
        self.lowerLimit = 18  # Measured in C
        self.warmUpRate = 0.8  # C change per second
        self.coolDownRate = 0.15  # C change per second
        self.staticWait = 50  # Seconds of static state
        self.tempDirectionChange = 'up'  # One of 'up' or 'down'

        # The time stamp of when the motor stopped accelerating
        self.lastStateChangeTime = datetime.datetime.now()

    def getNextResult(self):
        secondsPassed = (datetime.datetime.now() -
                         self.lastResultTime).total_seconds()
        workingTemp = self.lastResult

        timeSinceLastStateChange = datetime.datetime.now() - self.lastStateChangeTime

        # swap cooling / warming state if time is over
        if timeSinceLastStateChange.total_seconds() >= self.staticWait:
            if self.tempDirectionChange == 'up':
                self.tempDirectionChange = 'down'
            else:
                self.tempDirectionChange = 'up'
            self.lastStateChangeTime = datetime.datetime.now()

        if self.tempDirectionChange == 'up':  # Temp is increasing
            workingTemp += self.warmUpRate*secondsPassed
            if workingTemp > self.upperLimit:
                workingTemp = self.upperLimit
        else:  # Temp is descreasing
            workingTemp -= self.coolDownRate*secondsPassed
            if workingTemp < self.lowerLimit:
                workingTemp = self.lowerLimit

        # Round to 3 decimal places
        workingTemp = round(workingTemp, 3)

        if self.logging:
            print("Sending result: " + str(workingTemp))

        return workingTemp
