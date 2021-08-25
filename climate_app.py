from os import name
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from sqlalchemy.orm.session import make_transient


####################################################
# Database Setup
####################################################
engine = create_engine("sqlite:///static/Resources/hawaii.sqlite")

# reflect an existin datavase into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

###############################################
# Flask Setup
###############################################

# Create an app
app = Flask(__name__)

###############################################
# Flask Routes
###############################################

@app.route("/")
def home():
    return render_template("index.html")

# This portion I am hoping to work on more later but 
# due to time constraints I am unable to finish it before 
# the homework submission deadline. 

# @app.route("/album")
# def album():
#     return render_template("album.html")

##################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data as jsonified dict."""
    # Query precipitation data for the year requested. 
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitations = session.query(Station.name, Measurement.date, Measurement.prcp).\
        filter(Station.station == Measurement.station).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).\
        filter(Measurement.prcp >= 0.0).all()

    session.close()

    # Create a dictionary from the row data and append to a list.
    precipitation =[]
    for name,date,prcp in precipitations:
        precipitation_dict = {}
        precipitation_dict['Station Name'] = name
        precipitation_dict['Date'] = date
        precipitation_dict['Precipitation (Inches)'] = prcp
        precipitation.append(precipitation_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precipitation)

######################################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the stations:
    stations = session.query(Station.station, Station.name).all()

    session.close()
    # Return a JSON list of stations from the dataset.
    return jsonify(stations)

#######################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the dates and temperature observations of the most 
    # active station for the last year of data.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active_station = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()
    temp_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.station == most_active_station[0]).\
    order_by(Measurement.date).all()

    session.close()

    temperature =[]
    for date,tobs in temp_data:
        temperature_dict = {}
        temperature_dict['Date'] = date
        temperature_dict['Temperature (F)'] = tobs
        temperature.append(temperature_dict)

    # Return a JSON list of temperature observations 
    # (TOBS) for the previous year.
    #return (f"The temperature data for Station: USC00519281.")
    return jsonify(temperature)

#########################################################################

@app.route("/api/v1.0/<start>")
def temp_start(start="YYYY-MM-DD"):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    max = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    avg = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    return jsonify(
        f"From your chosen start date, the lowest recorded temp was:{min}, the highest recorded temp was:{max}, and the average over-all temp was:{avg}. Enjoy your vacation!")

    # Return a JSON list of the minimum temperature, the average 
    # temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all 
    # dates greater than and equal to the start date.
    # When given the start and the end date, calculate the TMIN, TAVG, 
    # and TMAX for dates between the start and end date inclusive.

#############################################################################
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start="YYYY-MM-DD", end="YYYY-MM-DD"):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    max = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    return jsonify(f"From your chosen start dateto your chosen end date, the lowest recorded temp was:{min}, the highest recorded temp was:{max}, and the average over-all temp was:{avg}. Enjoy your vacation!")


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
