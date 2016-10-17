__author__ = 'carnifex'

import requests
import ConfigParser
import pytz
from pytz import timezone
from datetime import datetime

class DataService(object):
	weatherApiUrl = ""
	exchangeApiUrl = ""
        currency = ""
	config = None

	def __init__(self):
		self.config = ConfigParser.ConfigParser()

	def readConfig(self):
		self.config.read("./weather.ini") #error check
		w_url = self.config.get("WeatherApi", "url")
		w_location = self.config.get("WeatherApi", "location")
		exchange_url = self.config.get("ExchangeApi", "url")
		exchange_base = self.config.get("ExchangeApi", "base")
		self.currency = self.config.get("ExchangeApi", "convertTo")
		timeZone = self.config.get("Config", "timeZone")

		self.config.read("./weather.api")
		weather_api = self.config.get("ApiKey", "key")

		self.weatherApiUrl = w_url + "q=" + w_location + "&num_of_days=1&format=json&key=" + weather_api
		self.exchangeApiUrl = exchange_url + "base=" + exchange_base + "&symbols=" + self.currency

	def getUrl(self, url):
		try:
			res = requests.get(url)
			return res.json()
		except requests.exceptions.RequestException as e:
			return None

	def getWeatherData(self):
		if self.weatherApiUrl == "":
			self.readConfig()
		data = self.getUrl(self.weatherApiUrl)
		if data is not None:
			return data['data']
		else:
			return data

	def getExchangeRates(self):
		if self.exchangeApiUrl == "":
			self.readConfig()
		data = self.getUrl(self.exchangeApiUrl)
		if data is not None:
			return data['rates'][self.currency]
		else:
			return data
