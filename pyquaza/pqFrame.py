import numpy as np
import pandas as pd
import requests
from datetime import date,datetime
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import get_body,get_sun,get_moon,EarthLocation,AltAz

class Transformations:
    """
    Pulls data for celestial body locations in the solar system and transforms those to a reference frame fixed in your backyard.
    
    Attributes
    ----------
    backyard_frame: Coordinate Frame
        Coordinate frame fixed at user-input defined location in teh Altitude-Azimuth system.
    timeframe: astropy Time
        Time object ranging from the time when run to a week ahead.
    delta_time: numpy Array
        Array of time points at which body is located over the next week.
    body_data pandas DataFrame
        DataFrame containing altitude (in degrees) and azimuth (in degrees) for celestial bodies in the solar system in the backyard frame over the following week.
    body_altaz astropy SkyCoord Object
        SkyCoord object containing location of a single user-defined celestial body in the backyard frame over the following week.
    sun_altaz SkyCoord Object
        SkyCoord object containing location of the Sun in the backyard frame over the following week.
    """
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.delta_time = np.linspace(0,168,2016)*u.hour
        today = datetime.combine(date.today(), datetime.min.time())
        time_now = Time(today)
        self.timeframe = Time(time_now)+self.delta_time
        self.backyard = EarthLocation(lat=self.lat*u.deg ,lon=self.long*u.deg)
        self.backyard_frame = AltAz(obstime=self.timeframe, location=self.backyard)
        
    
    def in_my_sky(self, body):
        """
        Finds the location of a user-defined celestial body and transforms it into the backyard frame over the next week.
        
        Parameters
        ----------
        body : str
            Celestial body in the solar system to locate.
        """
        
        if body.lower() == 'moon':
            body_location = get_moon(time=self.timeframe, location=self.backyard)
        else:
            body_location = get_body(body=body,time=self.timeframe, location=self.backyard)

        self.body_altaz = body_location.transform_to(self.backyard_frame)

        return self.body_altaz
    
    
    def sun_for_me(self):
        """Finds the location of the Sun and transforms it to the backyard frame over the next week. """
        
        self.sun_altaz  = get_sun(self.timeframe).transform_to(self.backyard_frame)
        
        return self.sun_altaz
    
    def check_weather(self):
        
        url = "https://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(self.lat) + "&lon=" + str(self.long) + "&cnt=7&appid=ece9f5354fef610b3f4ac8e96a6a4895&units=imperial"
        response = requests.request("GET", url)
        results = response.json()
        df_weather = pd.DataFrame(results["list"])
        clouds = df_weather['clouds'].to_numpy()
        
        return clouds