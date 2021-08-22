import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy.orm.session import make_transient


##################################
# Database Setup
##################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existin datavase into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

##################################
# Flask Setup
##################################
# Create an app
app = Flask(__name__)

##################################
# Flask Routes
##################################

@app.route("/")
def welcome():
    """Home page, list all available api routes"""
    return (
        f"Welcome to the Climate App API home page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data as jsonified dict."""
    # Query precipitation data for the year requested. 
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).\
    order_by(Measurement.date).\
    filter(Measurement.prcp >= 0.0).all()

    session.close()

    # Create a dictionary from the row data and append to a list.
    precipitation =[]
    for date, prcp in precipitation:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = precipitation
        precipitation.append(precipitation_dict)

    return jsonify(precipitation_dict)
    # Convert the query results to a dictionary using date as the key and 
    # prcp as the value.
    # Return the JSON representation of your dictionary.

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the stations:
    stations = session.query(Station.station).all()

    session.close()
    # Return a JSON list of stations from the dataset.
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most 
    # active station for the last year of data.
    temp_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()

    session.close()
    
    temperatures =[]
    for date, tobs in temp_data:
        temperature_dict = {}
        temperature_dict['date'] = date
        temperature_dict['tobs'] = temperature
        temperature.append(temperature_dict)

    return jsonify(temperature_dict)

    # Return a JSON list of temperature observations 
    # (TOBS) for the previous year.

@app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of the minimum temperature, the average 
    # temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all 
    # dates greater than and equal to the start date.
    # When given the start and the end date, calculate the TMIN, TAVG, 
    # and TMAX for dates between the start and end date inclusive.

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
