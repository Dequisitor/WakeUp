__author__ = 'carnifex'

import subprocess
import json
import requests
import time
import urllib, urllib2
from datetime import datetime, timedelta

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
		self.tts_url = "http://api.voicerss.org/?hl=en-gb&f=44khz_16bit_stereo&key="
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

	def getTemp(self):
		temp = int(self.weather['current_condition'][0]['temp_C'])
		feels = int(self.weather['current_condition'][0]['FeelsLikeC'])

		if feels != temp:
			return "It is " + str(temp) + " degrees celsius outside, but it feels like " + str(feels) + " degrees celsius."
		else:
			return "It is " + str(temp) + " degrees celsius outside."

	def getPressureAndHumidity(self):
		pressure = int(self.weather['current_condition'][0]['pressure'])
		humidity = int(self.weather['current_condition'][0]['humidity'])

		return "Pressure is " + str(pressure/10) + " KiloPascals, and humidity is " + str(humidity) + " percent."

	def getWind(self):
		windkmph = int(self.weather['current_condition'][0]['windspeedKmph'])
		winddir = self.weather['current_condition'][0]['winddir16Point']

		if len(winddir) == 3:
			direction = winddir[0] + '-' + winddir[1:]
		else:
			direction = winddir
		direction = direction.replace('N', 'north')
		direction = direction.replace('S', 'south')
		direction = direction.replace('E', 'east')
		direction = direction.replace('W', 'west')

		return "There is a " + str(windkmph) + " kilometer per hour " + direction + "ern wind."

	def getDay(self):
		today = datetime.today()

		print today
		DoM = datetime.now().day
		suffix = 'th'
		if DoM % 10 == 1:
			suffix = 'st'
		if DoM % 10 == 2:
			suffix = 'nd'

		return "Today is " + today.strftime('%A') + ", the " + str(DoM) + suffix + " of " + today.strftime('%B') + "."

	def createSentences(self):
		self.text = [	self.decideGreeting(),
				self.getDay(),
				self.getSunrise(),
				self.getSunset(),
				self.getTemp(),
				self.getPressureAndHumidity(),
				"The weather is described as: " + self.weather['current_condition'][0]['weatherDesc'][0]['value'] + ".",
				self.getWind(),
				"Have a nice effing day, you worthless faggot!"
			]

	def readOutLoud(self):
		self.tts_url = self.tts_url + self.tts_api + "&src="
		for index, line in enumerate(self.text):
			print(line)
			with open(str(index) + ".wav", "wb") as wave:
				wave.write(urllib2.urlopen(self.tts_url + line.replace(" ", "+")).read())
		for index, line in enumerate(self.text):
			subprocess.call('mplayer -really-quiet "' + str(index) + '.wav"', shell=True)
			subprocess.call('rm ' + str(index) + '.wav', shell=True)
