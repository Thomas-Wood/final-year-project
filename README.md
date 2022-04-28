# final-year-project

This contains the implementation of my final year project.

## Conventional Commits

This project follows the [conventional commits specification](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) which enables easy understanding of commits and allows for automatic versioning.

## Project Components

The project is made up of the following key components:

- Flask Application
- FROST Server
- Simulated Sensors

## Flask Application

The Falsk application will provide the user interface for the user to view graphs showing sensors data obtained from the FROST server. It also has a MongoDB connection for saving details other than sensor data such as groups of sensors, graph layouts, notifications storage and triggers etc.

## FROST Server

FROST is a server implementaiton of the SensorThings API standard. The Flask app will connect to this server for collect sensor data. The simulated sensor will send their data to FROST for organised storage. FROST is available in a docker container and will be used here to help with rapid development.

## Simulated Sensors

The sensors are simulated by a class for each snesor which is called by the sensor scheduler. The only requirement for these sensors is that they fill up FROST with reasonable data that can be viewed and 'monitored' in the user interface. FROST already provides the standard interface to other real sensor systems or future virtual factory developments, this is why these 'sensors' are not waiting for a request to send their data and instead send them at regular intervals.

## Running the project

All commands are run from the root of the project (same level as this readme)

There are three parts to this project:

1. The FROST server
2. The simulated sensors
3. The user interface

To start FROST in the docker container, run:

    docker-compose up

To set up the all the starting entities required for the sensors, run the simulatedSensorSetup.py script:

    python .\simulatedSensors\simulatedSensorSetup.py

This adds:

- Things. A thing can take many forms depending on the context. In the malt loaf factory context, a 'thing' is a machine or system with 1 to many sensors like 'storage system'.

- Datastreams. A datastream is defined as: "A Datastream groups a collection of Observations measuring the same ObservedProperty and produced by the same Sensor." It basically links the 'Thing' with the sensors it has, the properties it measures, and the observations that are stored in the server.

- Sensors. These are the details of a sensor including its description and a link to it's datasheet or specification.

- ObservedProperties. ObservedProperty is something like weight, temperature, velocity etc. The Datastream contains the unitOfMeasurement like m/s or Kg.

- Location. Location is the gps coords of the 'Thing'.

To run the sensors and start sending regular data (Observations) to FROST, run the simulatedSensorScheduler.py script:

    python .\simulatedSensors\simulatedSensorScheduler.py

Observation is the recording of a sensor's output. It has a result (the number it recorded), and the time it was made.

To clear the inputed data during testing, the volume created in docker must be deleted (Stopping the container doesn't clear it). This can be done through the UI or the CLI.

To start the alert creator (checks for when an alert needs to me made or ended), run this command:

    python alertCreator/alertCreator.py

To start the user interface, first start up the Flask server:

    python FlaskServer/main.py

Then view the interface at:

    http://127.0.0.1:8080/

## Accessing raw FROST data

You can access the data via a URL like this:

http://localhost:8080/FROST-Server/v1.0

http://localhost:8080/FROST-Server/v1.0/Datastreams(1)/Observations

http://localhost:8080/FROST-Server/v1.0/Datastreams
