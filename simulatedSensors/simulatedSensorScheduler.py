import schedule
import time
from simulatedStorageSystemSensors.weightMaltFlourSiloSensor import weightMaltFlourSiloSensor
from simulatedStorageSystemSensors.weightWheatFlourSiloSensor import weightWheatFlourSiloSensor

# Send regular observations to the FROST server
# Uses scheduler library: https://github.com/dbader/schedule

# Initalise 'Weight - Wheat Flour Silo sensor'
# Add to scheduler
# Repeat for all other sensors

sensorList = []

sensorList.append({
    'sensor': weightWheatFlourSiloSensor(
        'http://localhost:8080/FROST-Server/v1.0/', '1', False),
    'secondsBetweenReading': 3
})

sensorList.append({
    'sensor': weightMaltFlourSiloSensor('http://localhost:8080/FROST-Server/v1.0/', '2'),
    'secondsBetweenReading': 2
})

for sensorSchedule in sensorList:
    schedule.every(sensorSchedule['secondsBetweenReading']).seconds.do(
        sensorSchedule['sensor'].sendObservation)

while True:
    schedule.run_pending()
    time.sleep(1)
