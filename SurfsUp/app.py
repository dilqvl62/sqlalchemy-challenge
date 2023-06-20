# Import the dependencies.
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from climate_starter import date_perception, one_year_Temp
from climate_starter import one_year_Temp
#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(autoload_with = engine)
# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def wecome():
    return(
        f"Welcome to the climate app API! <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_dict = {date : value for (date, value) in date_perception}
    return(
        jsonify(precipitation_dict)
    )
    
  
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # list of stations from the dataset.
    results = session.query(Station.station).all()
    
    #Convert a list of tuples into a normal list
    all_stations = list(np.ravel(results))
    session.close()
    
    #Return a JSON list
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query the dates and temperature observations of the most-
    #active station for the previous year of data.
    dates_temp = one_year_Temp
    
    #Extract the temperature from the list of tuple 
    date_temp_list = [value for _, value in dates_temp]
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(date_temp_list)

if __name__ == '__main__':
    app.run(debug=True)
 



























