# 🏄‍♀️ SQLAlchemy-Challenge: Surfs Up🏄‍♂️

For this challenge we were asked to evaluate the climate data for Hawaii to determine the best time of year to take a vacation (where the weather is concerned). We first completed data exploration and analysis using SQLAlchemy and an Interactive Python Notebook (Jupyter Lab). We queried, cleaned, and ordered the data for analysis. 

## Analysis of Precipitation for the Final Year of Data:

![image](https://user-images.githubusercontent.com/83737584/130727158-18c501a5-5420-4383-bae9-8f097195fbf2.png)

* All rows containing a value of "none" in the precipitation column were discluded from the analysis. Additionally, an assumption of Farenheit was made on the temperature analysis. 

## Analysis of Temperature for the Final Year of Data:

![image](https://user-images.githubusercontent.com/83737584/130727535-b36a45c1-7153-439f-8c08-8e96ed117672.png)

In addition to these analyses, the summary statistics data for precipitation was taken, the station with the most data was calculated, and from the station with the most data I found the minimum, maximum, and average temperatures recorded. 

Once this was completed, an app was created using Flask to share the information that was analyzed. If you open my app you will find that there are links (please click on any one of them) for the precipitation, stations, and temperature data. Additionally, the app has the ability to query the minimum and maximum temperatures, where, and when they were recorded for any date range that you would like to query within the dataset AND the average temperature over all of the available data for any date range of your choosing. This information will potentially be different from the information on the Interactive Notebook as the calculations requested were read as the minimum, maximum, and average temperatures over-all data within the requested date set rather than only for the station with the most data as requested in the notebook section. 

A couple notes: the notebook may be viewed through the Analysis folder, the images in this README have been saved in the static folder, and the app is accessed as climate_app.py. 

