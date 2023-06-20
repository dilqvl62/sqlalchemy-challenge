#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# # Reflect Tables into SQLAlchemy ORM

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,cast, Date


# In[4]:


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[5]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)


# In[6]:


# View all of the classes that automap found
Base.classes.keys()


# In[7]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[8]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Precipitation Analysis

# In[9]:


# Find the most recent date in the data set.
#Convert the date column from a string into a datetime
Date_time = session.query(Measurement.date).all()
Date_time
most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
most_recent_date


# In[10]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 

#converting the date as a string to datetime
most_recent_datetime = datetime.strptime(most_recent_date, '%Y-%m-%d' )


# Calculate the date one year from the last date in data set.
date_12_months_ago = (most_recent_datetime - timedelta(days = 365)).date()

# Perform a query to retrieve the data and precipitation scores
date_perception = session.query(Measurement.date, func.Max(Measurement.prcp)).\
                                filter(Measurement.date >= date_12_months_ago).\
                                group_by(Measurement.date).all()

# Save the query results as a Pandas DataFrame. Explicitly set the column names
date_perc_df = pd.DataFrame(date_perception, columns=['date', 'perception'])
date_perc_df.set_index('date',inplace=True)
date_perc_df
# Sort the dataframe by date
date_perc_df.sort_values('date')

# Use Pandas Plotting with Matplotlib to plot the data

date_perc_df.plot(rot=90)
plt.xlabel('Date')
plt.ylabel('Inches')
date_12_months_ago


# In[11]:


# Use Pandas to calculate the summary statistics for the precipitation data
date_perception_summary = session.query(Measurement.date, Measurement.prcp).\
                  filter(Measurement.date > date_12_months_ago).all()   
sumary_df = pd.DataFrame(date_perception_summary).dropna()
sumary_df.describe()


# # Exploratory Station Analysis

# In[15]:


# Design a query to calculate the total number of stations in the dataset
total_station = session.query(func.count(func.distinct(Measurement.station))).scalar()
total_station 


# In[16]:


# Design a query to find the most active stations (i.e. which stations have the most rows?)
# List the stations and their counts in descending order.
most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                       group_by(Measurement.station).\
                       order_by(func.count(Measurement.station).desc()).all()
most_active_stations


# In[17]:


# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
id = most_active_stations[0].station
max_min_avg = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == id).all()
max_min_avg


# In[18]:


# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
one_year_Temp= session.query (Measurement.date, Measurement.tobs).\
               filter((func.strftime(Measurement.date) >= date_12_months_ago) & (Measurement.station == id)).all()
               

One_yearTemp_df = pd.DataFrame(one_year_Temp)

One_yearTemp_df.set_index('date', inplace=True)
One_yearTemp_df.plot.hist()
plt.show()


# # Close Session

# In[19]:


# Close Session
session.close()


# In[ ]:




