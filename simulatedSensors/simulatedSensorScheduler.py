import schedule
import time
import simulatedSensorTemplate

# Send regular observations to the FROST server
# Uses scheduler library: https://github.com/dbader/schedule

# Initalise 'Weight - Wheat Flour Silo sensor'
# Add to scheduler
# Repeat for all other sensors

testSensor = simulatedSensorTemplate.simulatedSensorTemplate(
    'http://localhost:8080/FROST-Server/v1.0/', '1')

schedule.every(3).seconds.do(testSensor.sendObservation)

while True:
    schedule.run_pending()
    time.sleep(1)
