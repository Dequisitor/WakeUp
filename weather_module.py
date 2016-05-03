__author__ = 'carnifex'

import subprocess
import json
import requests
import time
import urllib, urllib2
import ConfigParser
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class Weather(object):
	tts_url = ""
	weather_url = ""
	city = ""
	text = ""
	weather = {}

	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.read("./weather.ini") #error check
		tts_url = config.get("TTSApi", "url")
		tts_lang = config.get("TTSApi", "language")
		tts_quality = config.get("TTSApi", "quality")
		w_url = config.get("WeatherApi", "url")
		w_location = config.get("WeatherApi", "location")
		exchange_url = config.get("ExchangeApi", "url")
		exchange_base = config.get("ExchangeApi", "base")
		exchange_convertTo = config.get("ExchangeApi", "convertTo")
		timeZone = config.get("Config", "timeZone")

		config.read("./weather.api")
		weather_api = config.get("ApiKey", "key")
		config.read("./tts.api")
		tts_api = config.get("ApiKey", "key")

		tz = pytz.timezone(timeZone)
		self.date = datetime.now(tz)
		self.tts_url = tts_url + tts_lang + "&f=" + tts_quality + "&key=" + tts_api + "&src="
		self.weather_url = w_url + "q=" + w_location + "&num_of_days=1&format=json&key=" + weather_api

	def getTargetDay(self):
		#if its already afternoon, then get the forecast for tomorrow
		if self.date.tm_hour > 12:
			return 2
		else:
			return 1

	def loadWeatherDataRaw(self):
		result = urllib2.urlopen(self.weather_url).read()
		data = json.loads(result)

		self.weather = data['data']

	def decideGreeting(self):
		if self.date.time().hour < 12:
			return "Good morning!"
		elif self.date.time().hour < 18:
			return "Good afternoon!"
		else:
			return "Good evening!"

	def isEarlierTime(self, time0, time1):
		t0 = time0.hour * 3600 + time0.minute * 60 + time0.second
		t1 = time1.tm_hour * 3600 + time1.tm_min * 60 + time1.tm_sec

		return t0 < t1

	def getSunrise(self):
		sunrise = self.weather['weather'][0]['astronomy'][0]['sunrise']
		sunriseTime = time.strptime(sunrise, "%I:%M %p")

		if self.isEarlierTime(self.date.time(), sunriseTime):
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

		return "Pressure is " + str(pressure) + " millibars, and humidity is " + str(humidity) + " percent."

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

		return "There is a " + str(windkmph) + " kilometers per hour " + direction + "ern wind."

	def getDay(self):
		print self.date
		DoM = self.date.day
		suffix = 'th'
		if DoM % 10 == 1 and DoM != 11:
			suffix = 'st'
		if DoM % 10 == 2 and DoM != 12:
			suffix = 'nd'
		if DoM % 10 == 3 and DoM != 13:
			suffix = 'rd'

		return "Today is " + self.date.strftime('%A') + ", the " + str(DoM) + suffix + " of " + self.date.strftime('%B') + "."

	def getChanceOfRain(self):
		result = 0
		data = self.weather['weather'][0]['hourly']
		for i in range(0, len(data)):
			chance = int(data[i]['chanceofrain'])
			if chance > 25:
				result = 1 if (result < 1) else result
			if chance > 50:
				result = 2 if (result < 2) else result
			if chance >75:
				result = 3

		str = 'You will not need an umbrella today.'
		if result == 1:
			str = 'There is a small chance for rain.'
		elif result == 2:
			str = 'There is a high chance for rain.'
		elif result == 3:
			str = 'It will be raining today, bring an umbrella.'

		return str

	def getChanceOfSnow(self):
		result = 0
		data = self.weather['weather'][0]['hourly']
		for i in range(0, len(data)):
			chance = int(data[i]['chanceofsnow'])
			if chance > 25:
				result = 1 if (result < 1) else result
			if chance > 50:
				result = 2 if (result < 2) else result
			if chance >75:
				result = 3

		str = ''
		if result == 1:
			str = 'There is a small chance for snow.'
		elif result == 2:
			str = 'There is a high chance for snow.'
		elif result == 3:
			str = 'It will be snowing today.'

		return str

	def createSentences(self):
		self.text = [self.decideGreeting(),
				self.getDay(),
				self.getSunrise(),
				self.getSunset(),
				self.getTemp(),
				self.getPressureAndHumidity(),
				"The weather is described as: " + self.weather['current_condition'][0]['weatherDesc'][0]['value'] + ".",
				self.getWind(),
				self.getChanceOfRain(),
				"Have a nice effing day!"
			]

	def readOutLoud(self):
		for index, line in enumerate(self.text):
			print(line)
			with open(str(index) + ".wav", "wb") as wave:
				wave.write(urllib2.urlopen(self.tts_url + line.replace(" ", "+")).read())
		for index, line in enumerate(self.text):
			subprocess.call('mplayer -really-quiet "' + str(index) + '.wav"', shell=True)
			subprocess.call('rm ' + str(index) + '.wav', shell=True)
