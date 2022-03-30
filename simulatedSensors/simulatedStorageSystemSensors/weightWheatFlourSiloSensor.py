import simulatedSensorTemplate
import datetime


class weightWheatFlourSiloSensor(simulatedSensorTemplate.simulatedSensorTemplate):

    def firstTimeSetup(self):
        self.lastResultTime = datetime.datetime.now()
        self.lastResult = 7010  # 25 Tonnes of flour in the silo
        self.usePerSecond = 0.289  # 0.289 Kg used per second
        self.refillRatePerSecond = 10  # Tanker fills silo at 10 kg per second
        self.startRefillLimit = 7000  # Start refilling at 7 Tonnes
        self.refillInProgress = False
        self.currentRefillTotal = 0  # How much weight has been delivered so far
        self.limitPerRefill = 18000  # Number of Kg per lorry delivery

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
            print("Refilling " + str(self.refillRatePerSecond *
                  secondsPassed) + " over " + str(secondsPassed) + " seconds")
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
