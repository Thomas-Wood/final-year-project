# final-year-project WIP

This contains the implementation of my final year project.

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

The simulated sensors will have a interface that represents a sensor collecting data at regular intervals. It does not need to actually collect data but could take semi-random values from a standard deviation set. These will likey be set up as docker containers and programatically created so many instances of sensors can be made for testing purposes.

## Running the project

The aim is to have a script that will run the flask application and spin up the sensors and FROST server all in one go. Instructions to follow...

To spin up the docker contains, run:

    docker-compose up

To set up the all the starting entities required, run the simulatedSensorSetup.py script.

This adds:

- A 'Thing'. A thing can be many things depending on the context. In the malt loaf factory context, a 'thing' is a machine or system with 1 to many sensors like 'storage system'.

- Datastreams. A datastream is defined as: "A Datastream groups a collection of Observations measuring the same ObservedProperty and produced by the same Sensor." It basically links the 'Thing' with the sensors it has, the properties it measures, and the observations that are stored in the server.

- Sensors. These are the details of a sensor including its description and a link to it's datasheet or specification.

- ObservedProperties. ObservedProperty is something like weight, temperature, velocity etc. The Datastream contains the unitOfMeasurement like m/s or Kg.

- Location. Location is the gps coords of the 'Thing'.

Observation is the recording of a sensor's output. It has a result (the number it recorded), and the time it was made. These are not added in the set up script yet.

You can access the data via a URL like this:

http://localhost:8080/FROST-Server/v1.0

http://localhost:8080/FROST-Server/v1.0/Datastreams(1)/Observations

http://localhost:8080/FROST-Server/v1.0/Datastreams

To clear the inputed data during testing, the volume created in docker must be deleted (Stopping the container doesn't clear it). This can be done through the UI or the CLI.
