# Weather-Forecasting

* This is Historical forecast data available from 7 October 2017.
* A 16-day forecast is a set of values for weather parameters for each of the 16 days ahead.
* There are 4 model recalculation cycles available for each day. Each time when recalculation happens, the new forecast is generated (it updates values of weather parameters in the forecast). It means that for each day, starting from 7 October 2017, you will have four 16-day forecasts.
* Forecasts are updated at these times: 00:00 UTC, 06:00 UTC, 12:00 UTC, 18:00 UTC.
* A 16-day forecast is a set of values for weather parameters that are available in 1-hour steps for 16 days ahead.

Thus, each day will have the following structure:
* 00:00 UTC  {forecast weather data for 1st day - 16th day}
* 06:00 UTC  {forecast weather data for 1st day - 16th day}
* 12:00 UTC  {forecast weather data for 1st day - 16th day}
* 18:00 UTC  {forecast weather data for 1st day - 16th day}
## Dataset Fields

| Column Name               | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `forecast_dt_unixtime`    | Forecast calculation time in Unix timestamp.                               |
| `forecast_dt_iso`         | Forecast calculation time in ISO format.                                   |
| `slice_dt_unixtime`       | Time for which the corresponding forecast part was calculated (Unix timestamp). |
| `slice_dt_iso`            | Time for which the corresponding forecast part was calculated (ISO format). |
| `lat`                     | Latitude of the location, decimal (−90; 90).                               |
| `lon`                     | Longitude of the location, decimal (-180; 180).                            |
| `temperature`             | Temperature in Celsius.                                                    |
| `dew_point`               | Temperature of the dew point in Celsius.                                   |
| `pressure`                | Atmospheric pressure (on the sea level) in hPa.                           |
| `ground_pressure`         | Atmospheric pressure (on the surface) in hPa.                             |
| `humidity`                | Humidity as a percentage.                                                  |
| `clouds`                  | Cloudiness as a percentage.                                                |
| `wind_speed`              | Wind speed in meters per second.                                           |
| `wind_deg`                | Wind direction in meteorological degrees.                                  |
| `rain`                    | Rain volume in mm.                                                         |
| `snow`                    | Snow water equivalent in mm.                                               |
| `ice`                     | Ice pellets volume in mm.                                                  |
| `fr_rain`                 | Freezing rain volume in mm.                                                |
| `convective`              | Convective precipitation in mm.                                            |
| `snow_depth`              | Depth of snow in meters.                                                   |
| `accumulated`             | Accumulated volume of precipitation in mm.                                 |
| `hours`                   | Number of hours for which precipitation values are calculated.             |
| `rate`                    | Precipitation intensity in mm/s.                                           |
| `probability`             | Probability of precipitation as a percentage.                              |
                        
## Objective
Predict weather conditions using historical data and provide insights into temperature trends, seasonal variations, and precipitation probabilities. Build a deployable machine learning model 

## Data Preparation and Understanding
* Converting time columns (forecast dt unixtime, slice dt iso) into datetime objects for easier manipulation.
* Aggregating precipitation types (rain, snow, ice, convective) into a total precipitation column.
* Calculating wind chill index and heat index as new features

### Wind Chill Index
* Wind Chill Index (WCI) measures how cold the wind makes us feel at lower temperatures. It combines the air temperature and wind speed to estimate the perceived temperature on exposed skin
* The Wind Chill Index is primarily used in colder climates to assess the risk of frostbite and hypothermia. It indicates how quickly heat is lost from exposed skin, increasing the sensation of cold
* Wind chill applies when the temperature is below 10°C and wind speed is greater than 4.8 km/h.

Formula:
Wind Chill = 13.12 + 0.6215 𝑇 = 11.37 𝑣^ 0.16 + 0.3965 𝑇 𝑣^ 0.16

Where:

𝑇 = Temperature in °C. 𝑣 = Wind speed in km/h.

### Heat Index
* The Heat Index (HI), also known as the apparent temperature, measures how hot it feels by combining the air temperature and relative humidity. It provides an estimate of the perceived temperature considering moisture in the air.
* The Heat Index is used in warmer climates to assess the risk of heat-related illnesses. It indicates how quickly the body can cool itself through sweating. High humidity reduces the evaporation rate of sweat, making it feel hotter.
* Heat index applies when the temperature is above 27°C and humidity is greater than 40%.

Formula:

![image](https://github.com/user-attachments/assets/21f171e6-a621-4b8c-8bf8-b43291f25a25)

Where:

𝑇 = Temperature in °C. 𝐻 = Relative humidity (%). Constants: 𝑐1 to 𝑐9 are given in the heat index formula.

## Exploratory Data Analysis (EDA)

### Histograms for continuous variables

![image](https://github.com/user-attachments/assets/51353fe0-ef73-4940-bace-768697a8af37)

* The histogram appears to be approximately normally distributed, which means that the temperatures follow a bell-shaped curve.
* The highest frequency of occurrences is in the temperature range of 10-12.5. This suggests that these temperatures are the most common in your data set.
* The frequency of occurrences decreases symmetrically as the temperature moves away from the central range, indicating that extreme temperatures are less common.
* Most temperature observations are clustered around the mean, with fewer observations at the extremes

![image](https://github.com/user-attachments/assets/6203f538-b9c0-4b1f-8bdb-63e32dfe74d1)

* The distribution is skewed to the right, meaning that higher humidity levels are more common in your dataset.
* The highest frequency of occurrences is at the 100 humidity level, indicating that this is the most common humidity level.
* The humidity levels range from 40 to 100, with a noticeable increase in frequency as the levels approach 100.
* The frequencies vary from 0 to 160, showing a broad range of occurrences across different humidity levels.

### Correlation heatmap for numerical variables

![image](https://github.com/user-attachments/assets/c4aa8e2a-9be2-40ac-8562-441548036358)

* Dew Point: Strong positive correlation with probability (0.52) and a moderate positive correlation with heat index (0.38). This implies higher dew points are associated with higher probabilities of certain weather conditions and an increase in the heat index.
* Ground Pressure: Strong negative correlation with probability (-0.48). Lower ground pressure tends to be linked with higher probabilities of certain weather patterns.
* Clouds and Wind Degree: Moderate positive correlation (0.30), indicating that certain cloud formations are associated with specific wind directions.
* Heat Index and Wind Speed: Negative correlation (-0.22), suggesting that as wind speed increases, the perceived temperature (heat index) decreases.

### Scatter plots

![image](https://github.com/user-attachments/assets/1ad5fb14-09f7-4681-b067-18e22ca3a78d)

Negative Correlation: As the temperature increases, the humidity tends to decrease. This is evident from the downward trend of the data points

![image](https://github.com/user-attachments/assets/763b27f8-6df3-40ca-9898-1f0ef09beb29)

* The data points are spread out, indicating a lack of strong correlation between wind speed and total precipitation. This suggests that high wind speeds do not necessarily result in higher or lower amounts of precipitation.
* The plot shows considerable variability in the relationship, suggesting that other factors might influence precipitation levels aside from wind speed

![image](https://github.com/user-attachments/assets/72649328-98ec-4199-bd76-75dc578927bd)

* The data points are spread across the plot, with some clustering at specific values of total precipitation and probability.
* There doesn't appear to be a clear, consistent trend between total precipitation and probability, suggesting that other factors might influence the probability of an event occurring.

## Model Building

* Objective: Predicting whether rainfall will occur (classification) or predict the amount of rainfall (regression).
* Target Variable:
    * For classification: Binary target (Rain = 1 if rainfall occurs, 0 otherwise).
    * For regression: Continuous target (Rain = total precipitation in mm).

### Classification

#### Logistic Regression

* Got 0.9675 accuracy

##### Key Observations:

* High Class:
    * Precision, Recall, F1-Score: All are 0.00 because there are no correctly classified samples in this category.
    * Support: No samples are correctly predicted as 'High.'

* Low Class:
    * Precision, Recall, F1-Score: Very high scores (0.97 - 1.00), indicating that the model is almost perfect at identifying 'Low' samples.
    * Support: High number of samples (298).

* Medium Class:
    * Precision, Recall, F1-Score: All are 0.00 due to poor performance in predicting 'Medium' samples.
    * Support: Low number of samples (10).

##### Insights:
* The dataset is highly imbalanced, with a dominant 'Low' class and very few 'High' and 'Medium' samples. This causes the model to perform well on the 'Low' class but poorly on the other classes.
* The high accuracy is misleading because it's mainly driven by the dominant 'Low' class. The model is not effectively learning to distinguish between the 'High' and 'Medium' classes.
* Macro Avg vs. Weighted Avg:
    * Macro Avg: Low scores (0.32 - 0.33), indicating poor performance across all classes.
    * Weighted Avg: Higher scores (0.94 - 0.97), reflecting the dominance of the 'Low' class in the accuracy calculation.

To handle this, we use use RandomOverSampler

Got 0.8611 accuracy.

After using GridSearchCV got:
* Best Parameters: {'C': 0.1, 'penalty': 'l2', 'solver': 'lbfgs'}
* Accuracy: 0.8398

#### Decision Trees

* Accuracy: 0.9977
* Decision Tree Multi-class ROC AUC: 0.9983

#### Random Forest

* Accuracy: 0.99888

I decided to go with Random Forest

### Feature Importances

![image](https://github.com/user-attachments/assets/c19ff5a4-ed3e-472e-bb50-01a7938116af)

### Regression
#### Random Forest Regressor
* Mean Absolute Error: 0.00477
* Mean Squared Error: 0.00300

lower MAE & MSE values indicate better model performance.

After using GridSearchCV:
* Best Parameters: {'max_depth': 30, 'min_samples_split': 2, 'n_estimators': 50}
* Mean Absolute Error: 0.004972004479283315
* Mean Squared Error: 0.003017245240761478

![image](https://github.com/user-attachments/assets/3b4172e7-3f8d-4488-bfb8-342481f63085)

### XGBoost

* Using DMatrix which is a special data structure in XGBoost optimized for both memory efficiency and training speed
* Test MAE: 0.011

As an alternative to RandomizedSearchCV, i am using Optuna libraries that are compatible with xgboost without involving scikit-learn

* Best parameters: {'n_estimators': 192, 'max_depth': 9, 'learning_rate': 0.04087692599956305, 'subsample': 0.7722912252008296, 'colsample_bytree': 0.6139628901061935}
* Mean Squared Error: 0.00089

Dumping both random forest model (Classification) and xgboost model (Regression) to predict values

Deploying the models on Streamlit cloud

Below is the link to the app

https://weather-forecasting-cqtbgg4vr2arbejbchq3xh.streamlit.app/
