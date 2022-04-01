import schedule
import time
from simulatedStorageSystemSensors.weightInvertedSugarTankSensor import weightInvertedSugarTankSensor
from simulatedStorageSystemSensors.weightMaltExtractTankSensor import weightMaltExtractTankSensor
from simulatedStorageSystemSensors.weightStarchHopperSensor import weightStarchHopperSensor
from simulatedStorageSystemSensors.weightMaltFlourHopperSensor import weightMaltFlourHopperSensor
from simulatedStorageSystemSensors.weightWheatFlourSiloSensor import weightWheatFlourSiloSensor

# Send regular observations to the FROST server
# Uses scheduler library: https://github.com/dbader/schedule

sensorList = []

# Wheat flour sensor
sensorList.append({
    'sensor': weightWheatFlourSiloSensor(
        'http://localhost:8080/FROST-Server/v1.0/', '1', False),
    'secondsBetweenReading': 3
})

# Malt flour sensor
sensorList.append({
    'sensor': weightMaltFlourHopperSensor('http://localhost:8080/FROST-Server/v1.0/', '2', False),
    'secondsBetweenReading': 2
})

# Starch sensor
sensorList.append({
    'sensor': weightStarchHopperSensor('http://localhost:8080/FROST-Server/v1.0/', '3', False),
    'secondsBetweenReading': 1
})

# Malt extract sensor
sensorList.append({
    'sensor': weightMaltExtractTankSensor('http://localhost:8080/FROST-Server/v1.0/', '4', False),
    'secondsBetweenReading': 5
})

# Inverted sugar sensor
sensorList.append({
    'sensor': weightInvertedSugarTankSensor('http://localhost:8080/FROST-Server/v1.0/', '5'),
    'secondsBetweenReading': 5
})

for sensorSchedule in sensorList:
    schedule.every(sensorSchedule['secondsBetweenReading']).seconds.do(
        sensorSchedule['sensor'].sendObservation)

while True:
    schedule.run_pending()
    time.sleep(1)
