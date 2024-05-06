# sqlalchemy_challenge

The following project uses Python and SQLAlchemy to conduct a basic weather data analysis to help plan a fictional trip. The results are consolidated into json format and pushed via an API SQLite Connection onto a landing page using Flask.

**ANALYSIS TASKS**

Precipitation Analysis Tasks
* Create a query that finds the most recent date in the dataset
* Create a query that collects only the date and precipitation for the last year of data
* Save the query results to a Pandas DataFrame to create date and precipitation columns
* Sort the DataFrame by date
* Plot the results by using the DataFrame plot method with date as the x and precipitation as the y variables
* Use Pandas to print the summary statistics for the precipitation data 

Station and Temperature Analysis Tasks
* Design a query that correctly finds the number of stations in the dataset 
* Design a query that correctly lists the stations and observation counts in descending order and finds the most active station
* Design a query that correctly finds the min, max, and average temperatures for the most active station
* Design a query to get the previous 12 months of temperature observation (TOBS) data that filters by the station with the most observations
* Save the query results to a Pandas DataFrame
* Plot a histogram for the last year of data using tobs as the column to count.

**FLASK TASKS**

API SQLite Connection & Landing Page Tasks
* Generate the engine
* Reflect the database schema
* Save references to the tables in the sqlite file (measurement and station)
* Create and bind the session between the python app and database 
* Display the available routes on the landing page
* Create Static and Dynamic routes

  **API Static Routes**
  1. Precipitation route:
  * Returns json with the date as the key and the value as the precipitation
  * Only returns the jsonified precipitation data for the last year in the database
  
  2. Stations route:
  * Returns jsonified data of all of the stations in the database
  
  3. A tobs route:
  * Returns jsonified data for the most active station (USC00519281)
  * Only returns the jsonified data for the last year of data
  
  **API Dynamic Routes**
  1. A start route:
  * Accepts the start date as a parameter from the URL
  * Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset 
  
  2. A start/end route:
  * Accepts the start and end dates as parameters from the URL
  * Returns the min, max, and average temperatures calculated from the given start date to the given end date

**REFERENCES**
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xmlLinks to an external site.
