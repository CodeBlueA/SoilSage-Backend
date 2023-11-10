from flask import Flask, jsonify, request
from flask_cors import CORS
from support_models import Weather


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
        
        # Get the weather data associated with the user
        weather_data = weather.find_weather_from_coords(latitude, longitude)
        
        


weather = Weather()        