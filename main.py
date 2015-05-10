__author__ = 'carnifex'

import weather_module

weather = weather_module.Weather()
weather.loadWeatherDataRaw()
weather.createSentences()
weather.readOutLoud()
