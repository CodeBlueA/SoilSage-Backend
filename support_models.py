import pyowm
import os
from dotenv import load_dotenv
from meteostat import Hourly, Point
from datetime import datetime, timedelta


load_dotenv()


class Weather :
    def __init__(self, *args, **kwargs) :
        try :
            self.owm = pyowm.OWM(os.environ.get("OPENWEATHERMAP_API_KEY"))
            self.w_manager = self.owm.weather_manager()
        except Exception :
            self.owm = None
        
    def find_weather_from_coords(self, latitude, longitude) :
        weather_data = dict()
        rain = 103
        if self.owm :
            w_at_coor = self.w_manager.weather_at_coords(latitude, longitude).weather
            try :
                owm_rain = w_at_coor.rain["1h"] * 25.4 * 30
                rain = owm_rain if owm_rain > 0 else rain
            except KeyError :
                pass
        
        # get current date and date 30 days prior
        start = (datetime.now() - timedelta(30)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get the weather data from meteostat
        place = Point(latitude, longitude) # 9.9816, 76.2999
        data = Hourly(place, start, end)
        data = data.fetch()
        
        # Average temp and humidity of last 30 days:
        temp_mean = data["temp"].mean()
        rhum_mean = data["rhum"].mean()
        prcp_mean = data["prcp"].mean() * 25.4 * 30
        
        # compiling together the gather weather data
        weather_data["Rainfall"] = rain if prcp_mean == 0 else prcp_mean
        weather_data["Temperature"] = temp_mean
        weather_data["Humidity"] = rhum_mean
        
        return weather_data