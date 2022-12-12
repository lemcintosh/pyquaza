<h1 align="center">
<img src="/pyquazaLogo.png" width="452">
</h1><br>

**What is PyQuaza?**

PyQuaza is a forecasting resource for amateur astronomers to optimize their stargazing experiences. 

**GUI Usage**

PyQuaza is intended to be utilized through a provided GUI, pqGUI.py. Users input their latitude & longitude and choose between two forecasting options. The first allows the user to select a specific body of interest from a drop-down menu and generate the optimal viewing time* for that body over a 7-day timeframe. The second option looks through all available bodies on the drop-down menu, selects the best choice to view within a 7-day time frame, and then outputs the best viewing time similarly to the first option. 

Both forecasting functionalities utilize a cost function to determine the optimal viewing time, based on the body distance from the earth and weather forecast for percent cloud coverage. 

*Note: When selecting a specific celestial body to view, it is possible that the body will not be visible within the 7-day timeframe. In that case, the GUI will output a message indicating that the body will not be visible.

**Module Overview**

PyQuaza consists of 4 main modules: pqFrame, pqBodyForecast, pqWeeklyForecast, pqGUI:
- pqFrame: Pulls data for celestial body locations in the solar system and transforms those to a earth-based reference frame
- pqBodyForecast: Evaluates weather conditions and celestial body locations over a 7-day time frame; this data is used in a cost function to output the optimal celestial body viewing time
- pqWeeklyForecast: Performs similar evaluation as pqBodyForecast, but for all available celestial bodies to provide a more general forecast; the optimal body to view is selected through a cost function, and its optimal viewing time is displayed in the same manner as the specific body forecast
- pqGUI: Provides a user interface to input viewing location and desired celestial body (if applicable); outputs the optimal celestial body viewing time and cloud coverage conditions

While the intent is that the user utilizes these modules through the GUI, an example notebook is included in the respository to demonstrate the functionality of each module in further detail. 
