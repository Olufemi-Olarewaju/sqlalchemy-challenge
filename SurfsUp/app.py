# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# Create an engine for the `hawaii.sqlite` database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/"<start>"<br/>"
        f"/api/v1.0/"<start>"/<end>"
    )

# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    precipitation = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        precipitation.append(row)

    return jsonify(precipitation)

# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Return a JSON list of Temperature Observations (tobs) for the previous year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    tobs_list = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        tobs_list.append(row)

    return jsonify(tobs_list)

# Define what to do when a user hits the /api/v1.0/<start> route
@app.route("/api/v1.0/<start>")
def start(start):

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_temps = list(np.ravel(results))

    return jsonify(start_temps)

# Define what to do when a user hits the /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    start_end_temps = list(np.ravel(results))

    return jsonify(start_end_temps)

if __name__ == "__main__":
    app.run(debug=True)
