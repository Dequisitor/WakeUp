__author__ = 'carnifex'

import subprocess
import json
import requests
import time
from datetime import datetime, timedelta


class Weather(object):
    weather_url = ""
    tts_url = ""
    clouds = 0
    temp_min = 0
    temp_max = 0
    temp_avg = 0
    weather_type = ""
    weather_desc = ""

    def __init__(self):
        self.tts_url = "http://translate.google.com/translate_tts?tl=en&q="

    def getTargetDay(self):
        #if its already afternoon, then get the forecast for tomorrow
        date = time.localtime(time.time())
        if date.tm_hour > 12:
            return 2
        else:
            return 1

    def get(self):
        self.weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Miskolc,hu&units=metric&cnt="
        self.weather_url += str(self.getTargetDay())

        weather_json = requests.get(self.weather_url)
        if weather_json.status_code == 200:
            weather_obj = json.loads(weather_json.text)
            self.clouds = weather_obj["list"][-1]["clouds"]
            self.temp_min = weather_obj["list"][-1]["temp"]["min"]
            self.temp_max = weather_obj["list"][-1]["temp"]["max"]
            self.temp_avg = weather_obj["list"][-1]["temp"]["day"]
            self.weather_type = weather_obj["list"][-1]["weather"][0]["main"]
            self.weather_desc = weather_obj["list"][-1]["weather"][0]["description"]
        else:
            print("error: ", str(weather_json.status_code), weather_json.reason)

    def read(self):

        description = ""
        if self.weather_type == "Clear":
            description = "sunglasses might prove to be useful."
        elif self.weather_type == "Clouds":
            description = "the weather will be rather cloudy."
        else:
            description = "there is a high chance for " + self.weather_desc + "."

        today = datetime.today()
        if self.getTargetDay() == 1:
            text = ["today is " + today.strftime("%A %d %B"),
                    "the sky is " + str(self.clouds) + " percent covered in clouds",
                    description,
                    "today's lowest temperature will be " + str(self.temp_min) + " celsius",
                    "highest " + str(self.temp_min) + " celsius",
                    "and on average " + str(self.temp_avg) + " celsius",
                    "have a nice effing day"]
        else:
            today += timedelta(days=1)
            text = ["tomorrow will be " + today.strftime("%A %d %B"),
                    "the sky will be " + str(self.clouds) + " percent covered in clouds",
                    description,
                    "tomorrow's lowest temperature will be " + str(self.temp_min) + " celsius",
                    "highest " + str(self.temp_min) + " celsius",
                    "and on average " + str(self.temp_avg) + " celsius",
                    "have a nice effing day"]

        for line in text:
            print(line)
            subprocess.call('mplayer "' + self.tts_url + line.replace(" ", "+") + '"', shell=True)

