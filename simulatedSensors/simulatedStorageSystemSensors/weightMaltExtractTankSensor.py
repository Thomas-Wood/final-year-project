import simulatedSensorTemplate
import datetime


class weightMaltExtractTankSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 18000  # 18 Tonnes of extract in the tank
        self.usePerSecond = 0.15  # 0.15 Kg used per second
        self.refillRatePerSecond = 5  # Tanker fills silo at 5 kg per second
        self.startRefillLimit = 3000  # Start refilling at 3 Tonnes
        self.refillInProgress = False
        self.currentRefillTotal = 0  # How much weight has been delivered so far
        self.limitPerRefill = 15000  # Number of Kg per delivery

    def getNextResult(self):
        secondsPassed = (datetime.datetime.now() -
                         self.lastResultTime).total_seconds()
        workingWeightInSilo = self.lastResult

        # Standard usage
        workingWeightInSilo -= self.usePerSecond*secondsPassed

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
