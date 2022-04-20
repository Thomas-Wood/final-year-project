import simulatedSensorTemplate
import datetime
import random


class weightStarchHopperSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 1000  # 1 Tonne of flour in the silo
        self.usePerSecond = 0.2  # 0.2 Kg used per second
        self.refillRatePerSecond = 100  # bag emptied at 100 kg per second
        self.startRefillLimit = 20  # Start refilling at 20 kg
        self.refillInProgress = False
        self.currentRefillTotal = 0  # How much weight has been delivered so far
        self.limitPerRefill = 1000  # Number of Kg per bag emptying

    def getNextResult(self):
        secondsPassed = (datetime.datetime.now() -
                         self.lastResultTime).total_seconds()
        workingWeightInSilo = self.lastResult

        # Standard usage
        workingWeightInSilo -= self.usePerSecond * \
            secondsPassed * random.uniform(0.5, 1.5)

        # Add any refill amounts
        requiresRefill = self.lastResult <= self.startRefillLimit
        if requiresRefill or self.refillInProgress:
            workingWeightInSilo += self.refillRatePerSecond*secondsPassed
            self.currentRefillTotal += self.refillRatePerSecond*secondsPassed
            if self.currentRefillTotal >= self.limitPerRefill:
                self.refillInProgress = False
            else:
                self.refillInProgress = True
            pass

        # Round to 3 decimal places
        workingWeightInSilo = round(workingWeightInSilo, 3)

        if self.logging:
            print("Sending result: " + str(workingWeightInSilo))

        return workingWeightInSilo
