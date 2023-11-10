from flask import Flask, jsonify, request
from flask_cors import CORS
from support_models import Weather, Soil
from crop_recommendation_model import AI_models


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def home() :
    if request.method == "POST" :
        # Find and initialize request data
        response = request.json
        latitude = response["Latitude"]
        longitude = response["Longitude"]
        panchayat = response["Panchayat"]
        
        # Get the weather data and the soil data associated with the user
        weather_data = weather.find_weather_from_coords(latitude, longitude)
        soil_data = soil.find_soil_data_panchayat(panchayat)
        print(weather_data, soil_data)
        
        # Pass the data into a model to perform prediction
        crops = ai.predict_crops_in_order({**weather_data, **soil_data})
        
        return jsonify(
            {
                "Crops": crops
            }
        )
        


weather = Weather()    
soil = Soil()
ai = AI_models()