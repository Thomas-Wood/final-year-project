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
