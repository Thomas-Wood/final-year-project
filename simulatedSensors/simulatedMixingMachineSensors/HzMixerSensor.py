import simulatedSensorTemplate
import datetime


class HzMixerSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 0  # Measured in Hz
        self.upperLimit = 2  # Measured in Hz
        self.lowerLimit = 0  # Measured in Hz
        self.spinAcceleration = 0.5  # Hz increase per second
        self.spinState = 'up'  # one of 'static', 'up', or 'down'
        self.staticWait = 50  # Seconds of static state

        # The time stamp of when the motor stopped accelerating
        self.staticTime = datetime.datetime.now()

    def getNextResult(self):
        secondsPassed = (datetime.datetime.now() -
                         self.lastResultTime).total_seconds()
        workingHz = self.lastResult

        # Spinning up or down adjustment
        if self.spinState == 'static':
            timeAtStatic = datetime.datetime.now() - self.staticTime
            if timeAtStatic.total_seconds() >= self.staticWait:
                if workingHz == self.lowerLimit:  # Start spinning up
                    self.spinState = 'up'
                else:  # Start spinning down
                    self.spinState = 'down'
        elif self.spinState == 'up':
            workingHz += secondsPassed*self.spinAcceleration
            if workingHz > self.upperLimit:
                workingHz = self.upperLimit
                self.spinState = 'static'
                self.staticTime = datetime.datetime.now()
        else:
            workingHz -= secondsPassed*self.spinAcceleration
            if workingHz < self.lowerLimit:
                workingHz = self.lowerLimit
                self.spinState = 'static'
                self.staticTime = datetime.datetime.now()

        # Round to 3 decimal places
        workingHz = round(workingHz, 3)

        if self.logging:
            print("Sending result: " + str(workingHz))

        return workingHz
