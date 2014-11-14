__author__ = 'carnifex'

import subprocess
import json
import requests
import time

class Weather(object):
    weather_url = ""
    tts_url = ""
    clouds = 0
    temp_min = 0
    temp_max = 0
    temp_avg = 0

    def __init__(self):
        self.weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Miskolc,hu&units=metric&cnt=1"
        self.tts_url = "http://translate.google.com/translate_tts?tl=en&q="

    def Get(self):
        weather_json = requests.get(self.weather_url)
        if weather_json.status_code == 200:
            weather_obj = json.loads(weather_json.text)

            self.clouds = weather_obj["list"][0]["clouds"]
            self.temp_min = weather_obj["list"][0]["temp"]["min"]
            self.temp_max = weather_obj["list"][0]["temp"]["max"]
            self.temp_avg = weather_obj["list"][0]["temp"]["day"]

        else:
            print("error: ", str(weather_json.status_code), weather_json.reason)

    def Read(self):
        #date = time.localtime(time.time())
        text = ["today is " + time.strftime("%A %d %B"),
                "the sky is " + str(self.clouds) + " percent covered in clouds",
                "today's lowest temperature will be " + str(self.temp_min) + " celsius",
                "highest " + str(self.temp_min) + " celsius",
                "and on average " + str(self.temp_avg) + " celsius",
                "have a nice effing day"]

        print(text)
        for lines in text:
            subprocess.call('mplayer "' + self.tts_url + lines.replace(" ", "+") + '"', shell=True)

