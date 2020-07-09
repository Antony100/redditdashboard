import requests

from redditdashboard import api_keys

class Weather():

    def get_data(self, api):
        response = requests.get(api)
        result = response.json()
        return result

    def get_weather(self):
        weather_data = self.get_data(api_keys.WEATHER_API)
        filtered_weather_data = {
            'description': weather_data['weather'][0]['description'],
            'temp': round(weather_data['main']['temp']),
            'humidity': weather_data['main']['humidity'],
            'wind_speed': self.convert_to_mph(weather_data['wind']['speed']),
            'icon': weather_data['weather'][0]['icon']
        }
        return filtered_weather_data

    # converting from m/s
    def convert_to_mph(self, wind_speed):
        return round(wind_speed * 2.236936)

class AirQuality():

    def get_data(self, api):
        response = requests.get(api)
        result = response.json()
        return result

    def get_air_quality(self):
        air_quality = self.get_data(api_keys.AIRQUALITY_API)
        return air_quality['results'][0]['value']
