import simulatedSensorTemplate
import datetime


class weightMaltFlourSiloSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 20000  # 20 Tonnes of flour in the silo
        self.usePerSecond = 0.25  # 0.25 Kg used per second
        self.refillRatePerSecond = 11  # Tanker fills silo at 11 kg per second
        self.startRefillLimit = 7000  # Start refilling at 7 Tonnes
        self.refillInProgress = False
        self.currentRefillTotal = 0  # How much weight has been delivered so far
        self.limitPerRefill = 15000  # Number of Kg per lorry delivery

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
