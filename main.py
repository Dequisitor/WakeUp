__author__ = 'carnifex'

import weather_module
import tts_service
import data_service

def main():
	dataService = data_service.DataService()
	weatherData = dataService.getWeatherData()
	exchangeData = dataService.getExchangeRates()

	weather = weather_module.Weather()
	sentences = weather.createSentences(weatherData, exchangeData)

	ttsService = tts_service.TtsService()
	ttsService.readOutLoud(sentences)

if __name__ == "__main__":
	main()
