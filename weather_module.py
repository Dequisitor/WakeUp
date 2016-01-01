__author__ = 'carnifex'

import subprocess
import json
import requests
import time
import urllib, urllib2
from datetime import datetime, timedelta

WIND_TYPES = [
	[1.1, 'calm'],
	[5.5, 'light air'],
	[11.9, 'a light breeze'],
	[19.7, 'a gentle breeze'],
	[28.8, 'a moderate breeze'],
	[38.8, 'a fresh breeze'],
	[49.9, 'a strong breeze'],
	[61.8, 'high wind'],
	[74.6, 'a gale'],
	[88.1, 'a strong gale'],
	[102.4, 'a storm'],
	[117.4, 'a violent storm'],
	[999, 'hurricane force']
]
WIND_DIRECTIONS = []

class Weather(object):
	tts_url = ""
	base_url = "";
	city = "";
	text = "";
	weather_api = "";
	tts_api = "";
	weather = {};

	def __init__(self):
		self.date = time.localtime(time.time())
		self.tts_url = "http://api.voicerss.org/?hl=en-us&f=22khz_16bit_stereo&key="
		self.base_url = "https://api.worldweatheronline.com/free/v2/weather.ashx?"
		self.city = "Miskolc,hu"
		f = open("weather.api", "r")
		print f
		self.weather_api = f.readline().strip()
		print "weather api: ", self.weather_api
		f.close()
		f = open("tts.api", "r")
		self.tts_api = f.readline().strip()
		print "tts api: ", self.tts_api
		f.close()

	def getTargetDay(self):
		#if its already afternoon, then get the forecast for tomorrow
		if self.date.tm_hour > 12:
			return 2
		else:
			return 1

	def getWindDescription(self):
		speed = int(self.weather['current_condition'][0]['windspeedKmph'])

		i = 1
		while (WIND_TYPES[i][0] < speed):
			print str(WIND_TYPES[i][0]) + ' < ' + str(speed)
			i = i + 1

		return WIND_TYPES[i-1][1]

	def loadWeatherDataRaw(self):
		query_url = "q=" + self.city + "&num_of_days=1&format=json&key=" + self.weather_api
		url = self.base_url + query_url
		print url
		result = urllib2.urlopen(url).read()
		data = json.loads(result)

		self.weather = data['data']
	
	def decideGreeting(self):
		if self.date.tm_hour < 12:
			return "Good morning!"
		elif self.date.tm_hour < 18:
			return "Good afternoon!"
		else:
			return "Good evening!"

        def isEarlierTime(self, time0, time1):
            t0 = time0.tm_hour * 3600 + time0.tm_min * 60 + time0.tm_sec
            t1 = time1.tm_hour * 3600 + time1.tm_min * 60 + time1.tm_sec

            return t0 < t1

	def getSunrise(self):
		sunrise = self.weather['weather'][0]['astronomy'][0]['sunrise']
		sunriseTime = time.strptime(sunrise, "%I:%M %p")

                if self.isEarlierTime(self.date, sunriseTime):
			return "The Sun will rise at " + sunrise + ","
		else:
			return "The Sun has risen at " + sunrise + ","

	def getSunset(self):
		sunset = self.weather['weather'][0]['astronomy'][0]['sunset']
		sunsetTime = time.strptime(sunset, "%I:%M %p")

                if self.isEarlierTime(self.date, sunsetTime):
			return "and it will set at " + sunset + "."
		else:
			return "and has set at " + sunset + "."
		

	def createSentences(self):
		today = datetime.today()

		self.text = [	self.decideGreeting(),
				"Today is " + today.strftime("%A %d %B") + ".",
				self.getSunrise(),
				self.getSunset(),
				"It's " + self.weather['current_condition'][0]['temp_C'] + " degrees celsius outside.",
				"The weather can be described as: " + self.weather['current_condition'][0]['weatherDesc'][0]['value'] + ".",
				"There is " + self.getWindDescription() + ".",
				"Have a nice effing day!"
			]

	def readOutLoud(self):
		self.tts_url = self.tts_url + self.tts_api + "&src="
		for line in self.text:
			print(line)
			subprocess.call('mplayer "' + self.tts_url + line.replace(" ", "+") + '"', shell=True)

