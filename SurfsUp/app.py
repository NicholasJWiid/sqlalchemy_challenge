# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station


#################################################
# Flask Setup
#################################################
# 1. Import Flask
from flask import Flask

# 2. Creat the app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return """
        <h1>Welcome to the homepage!</h1>
        <b>Available Routes:</b><br/>
        Precipitation API /api/v1.0/precipitation<br/>Click <a href="/api/v1.0/precipitation">here</a> to get the precipitation data in json format.<br/><p>
        Stations API /api/v1.0/stations<br/>Click <a href="/api/v1.0/stations">here</a> to get the list of stations in json format.<br/><p>
        Temperature API /api/v1.0/tobs<br/>Click <a href="/api/v1.0/tobs">here</a> to get the temperature data in json format.<br/><p>
        Temperature min/max/avg API from specified start date /api/v1.0/<start><br/> Enter in your desired start_date in YYYY-MM-DD format: E.g. <a href="/api/v1.0/2016-08-21">/api/v1.0/2016-08-21</a><br/><p>
        Temperature min/max/avg API between specified start and end  dates /api/v1.0/<start>/<end><br/>Enter in your desired start_date/end_date combination in YYYY-MM-DD format: E.g. <a href="/api/v1.0/2016-08-21/2017-08-21">/api/v1.0/2016-08-21/2017-08-21</a>
    """

# 4. Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_yr = int(last_date[0][:4])
    last_m = int(last_date[0][5:7])
    last_d = int(last_date[0][8:])
    last_minus_12m = dt.date(last_yr, last_m, last_d) - dt.timedelta(days=365)

    prcp_results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= last_minus_12m).order_by(Measurements.date).all()
    prcp_dict = [{result[0]: result[1]} for result in prcp_results]
    session.close()
    return jsonify(prcp_dict)

# 5. Define station route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    station_results = session.query(Measurements.station, func.count(Measurements.id)).group_by(Measurements.station).order_by(func.count(Measurements.id).desc()).all()
    station_dict = [{station[0]: station[1]} for station in station_results]
    session.close()
    return jsonify(station_dict)

# 5. Define station route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_yr = int(last_date[0][:4])
    last_m = int(last_date[0][5:7])
    last_d = int(last_date[0][8:])
    last_minus_12m = dt.date(last_yr, last_m, last_d) - dt.timedelta(days=365)

    tobs_results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.station == 'USC00519281').filter(Measurements.date > last_minus_12m).all()
    tobs_dict = [{temp[0]: temp[1]} for temp in tobs_results]
    session.close()
    return jsonify(tobs_dict)

# 5. Define station route
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start_Date' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    start_date = start
    first_date = session.query(Measurements.date).order_by(Measurements.date).first()
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()

    if start_date > last_date[0]:
        return f"Start date entered is out of recorded range: Last record is {last_date[0]}"
    elif start_date < first_date[0]:
        return f"Start date entered is out of recorded range: First record is {first_date[0]}"
    else:
        start_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()
        tobs_calc_dict = {
            'chosen_start_date': start_date,
            'last_record_date': last_date[0],
            'temp_min': start_results[0][0],
            'temp_max': start_results[0][1],
            'temp_avg': round(start_results[0][2], 2)}
        session.close()
        return jsonify(tobs_calc_dict)

# 5. Define station route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'Start_End_Date' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    start_date = start
    end_date = end
    first_date = session.query(Measurements.date).order_by(Measurements.date).first()
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()

    if start_date > last_date[0]:
        return f"Start date entered is out of recorded range: Last record is {last_date[0]}"
    elif end_date > last_date[0]:
        return f"End date entered is out of recorded range: Last record is {last_date[0]}"
    elif start_date < first_date[0]:
        return f"Start date entered is out of recorded range: First record is {first_date[0]}"
    else:
        start_end_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
        tobs_calc_dict = {
            'chosen_start_date': start_date,
            'chosen_end_date': end_date,
            'temp_min': start_end_results[0][0],
            'temp_max': start_end_results[0][1],
            'temp_avg': round(start_end_results[0][2], 2)}
        session.close()
        return jsonify(tobs_calc_dict)


if __name__ == "__main__":
    app.run(debug=True)

    #  <p>Click <a href="/about">here</a> to go to the About page.</p>
    # <p>Click <a href="/contact">here</a> to go to the Contact page.</p>