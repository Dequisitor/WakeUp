__author__ = 'carnifex'

import requests
import ConfigParser
import subprocess

class TtsService(object):
	tts_url = ""
	config = None

	def __init__(self):
		self.config = ConfigParser.ConfigParser()

	def readConfig(self):
		self.config.read("/usr/share/WakeUp/weather.ini") #error check
		tts_url = self.config.get("TTSApi", "url")
		tts_lang = self.config.get("TTSApi", "language")
		tts_quality = self.config.get("TTSApi", "quality")

		self.config.read("./tts.api")
		tts_api = self.config.get("ApiKey", "key")

		self.tts_url = tts_url + tts_lang + "&f=" + tts_quality + "&key=" + tts_api + "&src="

	def readOutLoud(self, sentences):
		errors = 0
		if self.tts_url == "":
			self.readConfig()
		for index, line in enumerate(sentences):
			print(line)
			with open(str(index) + ".wav", "wb") as wave:
				try:
					data = requests.get(self.tts_url + line.replace(" ", "+"))
					if data.status_code == 200 and data.content[0:5] != "ERROR":
						wave.write(data.content)
					else:
						errors += 1
				except requests.exceptions.RequestException as e:
					errors += 1

		if errors == 0:
			for index, line in enumerate(sentences):
				#subprocess.call('mplayer "' + str(index) + '.wav"', shell=True)
				subprocess.call('mplayer -really-quiet "' + str(index) + '.wav"', shell=True)
				subprocess.call('rm ' + str(index) + '.wav', shell=True)
		else:
			subprocess.call('mplayer "./wavs/tts_error.wav"', shell=True)
