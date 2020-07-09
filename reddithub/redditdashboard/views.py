from django.views.generic import View
from django.shortcuts import render

from redditdashboard import redditdatapull, reddit_config as RC, api_data_pull


class HomeView(View):

    template_name = 'redditdashboard/dashboard.html'

    rdp = redditdatapull.DataPull(RC.CLIENT_ID, RC.CLIENT_SECRET,
                                  RC.USER_AGENT, RC.USERNAME, RC.PASSWORD)

    weather_data = api_data_pull.Weather()
    airquality_data = api_data_pull.AirQuality()

    def get(self, request, *args, **kwargs):
        worldnews = self.rdp.get_articles('worldnews')
        ukpolitics = self.rdp.get_articles('ukpolitics')
        football = self.rdp.get_articles('soccer')
        science = self.rdp.get_articles('science')
        car = self.rdp.get_image('carporn')
        nature = self.rdp.get_image('EarthPorn')
        space = self.rdp.get_image('spaceporn')
        skyline = self.rdp.get_image('CityPorn')
        quote = self.rdp.get_quote('quotes')
        airquality = self.airquality_data.get_air_quality()
        weather = self.weather_data.get_weather()

        context = {
            "worldnews": worldnews,
            "ukpolitics": ukpolitics,
            "football": football,
            "science": science,
            "car": car,
            "nature": nature,
            "space": space,
            "skyline": skyline,
            "quote": quote,
            "airquality": airquality,
            "weather": weather
        }
        return render(request, self.template_name, context)
