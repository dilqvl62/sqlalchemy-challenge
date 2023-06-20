# Import the dependencies.
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
from datetime import datetime
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
def welcome():
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
    session.close()
    
    #Convert a list of tuples into a normal list
    all_stations = list(np.ravel(results))
    
    
    #Return a JSON list
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    #Query the dates and temperature observations of the most-
    #active station for the previous year of data.
    dates_temp = one_year_Temp
    
    #Extract the temperature from the list of tuple 
    date_temp_list = [value for _, value in dates_temp]
   
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(date_temp_list)

@app.route("/api/v1.0/<start>")
def min_max_avg_startDate(start):
            
            #  Return the min, max , and average of the tempeature from the start date 
            #  supplied by the user to the end of the data set or 404 if the date is greater then the date 
            #  at the end of the data set
            
            # Create our session (link) from Python to the DB
            session = Session(engine)
            
            #Query the most recent date witch is the last date of the dataset
            most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
             
            # using try-except blocks for handling the exceptions
            try:
                # formatting the date using strptime() function
                dateObject = datetime.strptime(start, '%Y-%m-%d').date()
                print(dateObject)
            # If the date validation goes wrong
            except ValueError:
                return jsonify({"eroor":"Incorrect date format, should be YYYY-MM-DD"}), 404
                
            if(start <= most_recent_date):
                Min_max_avg = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),                        func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
                #closing the session
                session.close()              
                
                return jsonify(list(np.ravel(Min_max_avg)))
            return jsonify({"error": "Date not Found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def min_max_avg_startDate_endDate(start, end):
    #  Return the min, max , and average of the tempeature from the start date 
            #  supplied by the user to the end of the data set or 404 if the date is greater then the date 
            #  at the end of the data set
            
            # Create our session (link) from Python to the DB
            session = Session(engine)
            
            # using try-except blocks for handling the exceptions
            try:
                # formatting the date using strptime() function
                startDate = datetime.strptime(start, '%Y-%m-%d').date()
                endDate = datetime.strptime(end, '%Y-%m-%d').date()
                print(f"start date is:{startDate}. End date is {endDate}" )
            # If the date validation goes wrong
            except ValueError:
                return jsonify({"eroor":"Incorrect date format, should be YYYY-MM-DD"}), 404
                
            Min_max_avg = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),                        func.avg(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end)).all()
                #closing the session
            session.close()              
                
            return jsonify(list(np.ravel(Min_max_avg)))
            
    
    
            
if __name__ == '__main__':
    app.run(debug=True)
 



























