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
        /api/v1.0/precipitation  - Click <a href="/api/v1.0/precipitation">here</a> to get the precipitation data on json format.<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/<start><br/>
        /api/v1.0/<start>/<end>
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

    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= last_minus_12m).order_by(Measurements.date).all()
    results = pd.DataFrame(results).dropna().sort_values('date').to_dict()
    # prc_dict = [{result[0]: result[1]} for result in results]
    session.close()
    return jsonify(results)

# 5. Define station route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    results = session.query().all()
    session.close()
    return jsonify()

# 5. Define station route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    results = session.query().all()
    session.close()
    return jsonify()

# 5. Define station route
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start_Date' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    results = session.query().all()
    session.close()
    return jsonify()

# 5. Define station route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'Start_End_Date' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query 
    results = session.query().all()
    session.close()
    return jsonify()


if __name__ == "__main__":
    app.run(debug=True)

    #  <p>Click <a href="/about">here</a> to go to the About page.</p>
    # <p>Click <a href="/contact">here</a> to go to the Contact page.</p>