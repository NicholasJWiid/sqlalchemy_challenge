# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import re
# Save a date pattern to prevent injection
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

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

# Create initial session and save global variables
session = Session(engine)
# Query the first date on record
first_date = session.query(Measurements.date).order_by(Measurements.date).first()
# Query the last date on record
last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
# Parse for last date components
last_yr = int(last_date[0][:4])
last_m = int(last_date[0][5:7])
last_d = int(last_date[0][8:])
# Find 12 months before last date
last_minus_12m = dt.date(last_yr, last_m, last_d) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
# 1. Import Flask
from flask import Flask

# 2. Create the app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the home route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # Return available routes and links with basic html formatting
    return """
        <center><h1>Welcome to the homepage!</h1>

        <b>Available Routes:</b><br/>

        <p>Precipitation API /api/v1.0/precipitation<br/>Click <a href="/api/v1.0/precipitation">here</a> to get precipitation data for the last year on record in json format.<p/>

        <p>Stations API /api/v1.0/stations<br/>Click <a href="/api/v1.0/stations">here</a> to get the list of stations and the number of observations per station.</>
        
        <p>Temperature API /api/v1.0/tobs<br/>Click <a href="/api/v1.0/tobs">here</a> to get temperature data for the last year on record in json format.<p/>
        
        <p>Temperature min/max/avg API from specified start date /api/v1.0/<start><br/> Add your desired start_date in YYYY-MM-DD format to the url: E.g. <a href="/api/v1.0/2016-08-21">/api/v1.0/2016-08-21</a><p/>
        
       <p>Temperature min/max/avg API between specified start and end  dates /api/v1.0/<start>/<end><br/>Add your desired start_date/end_date combination in YYYY-MM-DD format to the url: E.g. <a href="/api/v1.0/2016-08-21/2017-08-21">/api/v1.0/2016-08-21/2017-08-21</a></p></center>
    """

# Define the precipitation route for last year of data on record
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    # Create session
    session = Session(engine)
    # Create main query and save results to a list of dictionaries
    prcp_results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= last_minus_12m).order_by(Measurements.date).all()
    prcp_dict = [{result[0]: result[1]} for result in prcp_results]
    session.close()
    # Return results for publishing
    return jsonify(prcp_dict)

# Define the station route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    # Create session
    session = Session(engine)
    # Create main query and save results to a list of dictionaries
    station_results = session.query(Measurements.station, func.count(Measurements.id)).group_by(Measurements.station).order_by(func.count(Measurements.id).desc()).all()
    station_dict = [{station[0]: station[1]} for station in station_results]
    session.close()
    # Return results for publishing
    return jsonify(station_dict)

# Define the temperature route for last year of data on record
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature' page...")
    # Create session
    session = Session(engine)
   # Create main query and save results to a list of dictionaries
    tobs_results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.station == 'USC00519281').filter(Measurements.date > last_minus_12m).all()
    tobs_dict = [{temp[0]: temp[1]} for temp in tobs_results]
    session.close()
    # Return results for publishing
    return jsonify(tobs_dict)

# Define the start_date route
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start_Date' page...")
    # Create session
    session = Session(engine)
    # Save user date input
    start_date = start
    # Check date inputs are in range, fit date pattern and run query to get data
    if date_pattern.match(start_date):
        if start_date > last_date[0]:
            return f"Start date entered is out of recorded range: Last record is {last_date[0]}"
        elif start_date < first_date[0]:
            return f"Start date entered is out of recorded range: First record is {first_date[0]}"
        else:
            start_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()
            # Save results to dictionary
            tobs_calc_dict = {
                'chosen_start_date': start_date,
                'last_record_date': last_date[0],
                'temp_min': start_results[0][0],
                'temp_max': start_results[0][1],
                'temp_avg': round(start_results[0][2], 2)}
            session.close()
            # Return results for publishing
            return jsonify(tobs_calc_dict)
    else:
        return "The date format is incorrect"

# Define the start_end_date route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'Start_End_Date' page...")
    # Create session
    session = Session(engine)
    # Save user date inputs
    start_date = start
    end_date = end
    # Check date inputs are in range, fit date pattern and run query to get data
    if date_pattern.match(start_date) and date_pattern.match(end_date):
        if start_date > last_date[0]:
            return f"Start date entered is out of recorded range: Last record is {last_date[0]}"
        elif end_date > last_date[0]:
            return f"End date entered is out of recorded range: Last record is {last_date[0]}"
        elif start_date < first_date[0]:
            return f"Start date entered is out of recorded range: First record is {first_date[0]}"
        else:
            start_end_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
            # Save results to dictionary
            tobs_calc_dict = {
                'chosen_start_date': start_date,
                'chosen_end_date': end_date,
                'temp_min': start_end_results[0][0],
                'temp_max': start_end_results[0][1],
                'temp_avg': round(start_end_results[0][2], 2)}
            session.close()
            # Return results for publishing
            return jsonify(tobs_calc_dict)
    else:
        return "The date format is incorrect"

# Run the app with debugger
if __name__ == "__main__":
    app.run(debug=True)

