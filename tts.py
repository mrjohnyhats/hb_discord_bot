import os, pydub, re
from gtts import gTTS
from sound_system import Sound_system

LANGS = ["af","sq","ar","hy","bn","ca","zh","zh-cn","zh-tw","zh-yue","hr","cs","da","nl","en","en-au","en-uk","en-us","eo","fi","fr","de","el","hi","hu","is","id","it","ja","ko","la","lv","mk","no","pl","pt","pt-br","ro","ru","sr","sk","es","es-es","es-us","sw","sv","ta","th","tr","vi","cy"]

def make_tts_file(words, parsed_args, server_id):
	if not os.path.exists("./tts_audio/"+server_id):
		os.makedirs("./tts_audio/"+server_id)
		filenum = 0
	else:
		filenum = len([name for name in os.listdir("./tts_audio/"+server_id) if os.path.isfile("./tts_audio/{0}/{1}".format(server_id, name))])

	filename = "tts_audio/{0}/tts{1}.mp3".format(server_id, filenum)

	print("tts filename "+filename)

	lang = parsed_args["lang"]
	reverse = parsed_args["reverse"]
	speed = parsed_args["speed"]

	speech = gTTS(text=words, lang=lang)
	speech.save(filename)

	if reverse or speed != 1.0:
		segs = pydub.AudioSegment.from_mp3(filename)
		if reverse:
			segs = segs.reverse()

		if speed != 1.0:
			segs = segs.speedup(playback_speed=speed)
		segs.export(filename, format="mp3")

	return filename


def parse_args(args):
	reverse = False
	if args.find("reverse=True") != -1:
		reverse = True

	lang = "en"
	if re.search("lang=\w+", args) != None:
		lang_start_i = re.search("lang=", args).end()
		lang_end_i = args.find(" ", lang_start_i)
		if lang_end_i == -1:
			lang_end_i = len(args)
		lang = args[lang_start_i:lang_end_i]

		if not lang in LANGS:
			bot.say(lang + " is not a valid language :/")
			lang = "en"

	speed = 1.0
	if re.search("speed=\d+(\.\d+)?", args) != None:
		speed_start_i = re.search("speed=", args).end()
		speed_end_i = args.find(" ", speed_start_i)
		if speed_end_i == -1:
			speed_end_i = len(args)

		#set speed here so that we can send a good error message later
		speed = args[speed_start_i:speed_end_i]

		try:
			speed = float(speed)
		except ValueError:
			yield from bot.say(speed + " is not a valid speed (valid speeds can be parsed as floats)")
			speed = 1.0
		else:
			if speed < 1.0:
				yield from bot.say("speed has to be greater than 1 due to the pydub library being dumb :/")
				speed = 1.0

	return {
		"reverse": reverse,
		"lang": lang,
		"speed": speed
	}
