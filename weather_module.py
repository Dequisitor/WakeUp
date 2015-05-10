__author__ = 'carnifex'

import subprocess
import json
import requests
import time
import urllib, urllib2
from datetime import datetime, timedelta

WIND_TYPES = 	[
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
	apiKey = "8c1d920518fe5a6aa3875b3d59897";
	city = "";
	text = "";
	weather = {};

	def __init__(self):
		self.tts_url = "http://translate.google.com/translate_tts?tl=en&q="
		self.base_url = "https://api.worldweatheronline.com/free/v2/weather.ashx?"
		self.city = "Miskolc,hu"

	def getTargetDay(self):
		#if its already afternoon, then get the forecast for tomorrow
		date = time.localtime(time.time())
		if date.tm_hour > 12:
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
		query_url = "q=" + self.city + "&num_of_days=1&format=json&key=" + self.apiKey
		url = self.base_url + query_url
		print url
		result = urllib2.urlopen(url).read()
		data = json.loads(result)

		self.weather = data['data']

	def createSentences(self):
		today = datetime.today()
		self.text = [	"Good morning!",
						"Today is " + today.strftime("%A %d %B"),
						"Its " + self.weather['current_condition'][0]['temp_C'] + " degrees celsius outside.",
						"The weather can be described as: " + self.weather['current_condition'][0]['weatherDesc'][0]['value'] + ".",
						"There is " + self.getWindDescription(),
						"Have a nice effing day!"
					]

	def readOutLoud(self):
		for line in self.text:
			print(line)
			subprocess.call('mplayer "' + self.tts_url + line.replace(" ", "+") + '"', shell=True)

