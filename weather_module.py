__author__ = 'carnifex'

import time
import ConfigParser
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class Weather(object):

	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		self.readConfig()

	def readConfig(self):
		self.config.read("./weather.ini") #error check
		timeZone = self.config.get("Config", "timeZone")
		tz = pytz.timezone(timeZone)
		self.date = datetime.now(tz)

	def getTargetDay(self):
		#if it's already afternoon, then get the forecast for tomorrow
		if self.date.tm_hour > 12:
			return 2
		else:
			return 1

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

	def getSunrise(self, weather):
		sunrise = weather['weather'][0]['astronomy'][0]['sunrise']
		sunriseTime = time.strptime(sunrise, "%I:%M %p")

		if self.isEarlierTime(self.date.time(), sunriseTime):
			return "The Sun will rise at " + sunrise + ","
		else:
			return "The Sun has risen at " + sunrise + ","

	def getSunset(self, weather):
		sunset = weather['weather'][0]['astronomy'][0]['sunset']
		sunsetTime = time.strptime(sunset, "%I:%M %p")

		if self.isEarlierTime(self.date, sunsetTime):
			return "and it will set at " + sunset + "."
		else:
			return "and has set at " + sunset + "."

	def getTemp(self, weather):
		temp = int(weather['current_condition'][0]['temp_C'])
		feels = int(weather['current_condition'][0]['FeelsLikeC'])

		if feels != temp:
			return "It is " + str(temp) + " degrees celsius outside, but it feels like " + str(feels) + " degrees celsius."
		else:
			return "It is " + str(temp) + " degrees celsius outside."

	def getPressureAndHumidity(self, weather):
		pressure = int(weather['current_condition'][0]['pressure'])
		humidity = int(weather['current_condition'][0]['humidity'])

		return "Pressure is " + str(pressure) + " millibars, and humidity is " + str(humidity) + " percent."

	def getWind(self, weather):
		windkmph = int(weather['current_condition'][0]['windspeedKmph'])
		winddir = weather['current_condition'][0]['winddir16Point']

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

	def getChanceOfRain(self, weather):
		result = 0
		data = weather['weather'][0]['hourly']
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

	def getChanceOfSnow(self, weather):
		result = 0
		data = weather['weather'][0]['hourly']
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

	def describeWeather(self, weather):
		return "The weather is described as: " + weather['current_condition'][0]['weatherDesc'][0]['value'] + "."

	def createSentences(self, weather, exchange):
		if weather is None:
			return ["Error occurred while querying weather data."]
		text = [self.decideGreeting(),
			self.getDay(),
			self.getSunrise(weather),
			self.getSunset(weather),
			self.getTemp(weather),
			self.getPressureAndHumidity(weather),
			self.describeWeather(weather),
			self.getWind(weather),
			self.getChanceOfRain(weather),
			"Have a nice effing day, faggot!"]

		return text
