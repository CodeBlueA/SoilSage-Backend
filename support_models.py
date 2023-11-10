import pyowm
import os
import pandas as pd
from meteostat import Hourly, Point
from datetime import datetime, timedelta



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
        weather_data["rainfall"] = rain if prcp_mean == 0 or pd.isna(prcp_mean) else prcp_mean
        weather_data["temperature"] = temp_mean if not pd.isna(temp_mean) else 26
        weather_data["humidity"] = rhum_mean if not pd.isna(rhum_mean) else 71
        
        return weather_data
    

class Soil :
    def __init__(self, *args, **kwargs) :
        pass
    
    def find_soil_data_panchayat(self, panchayat) :
        # Rea the dataset
        df = pd.read_csv("Ernakulam.csv")
        # Locate all data belonging to the same panchayt
        results = df.loc[df["Panchayaths"] == panchayat.capitalize().strip()]
        results = {i: list(results[i])[0] for i in results}
        del results["Panchayaths"]
        
        return results