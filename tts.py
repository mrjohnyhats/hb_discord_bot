import os, pydub, re
from gtts import gTTS

 
def __init__(server_id):
	server_id = server_id

queue = []
playing = False

def play(words, voice_client, tts_args):
	add_tts(words, voice_client, tts_args)
	if not playing:
		play_if_enqueued()

def add_tts(words, voice_client, tts_args):
	queue.append(make_tts_player(words, tts_args["lang"], tts_args["reverse"], tts_args["speed"], voice_client))

def play_if_enqueued():
	global playing
	if len(queue) > 0:
		playing = True
		cur_player = queue.pop(0)
		cur_player.start()
	else:
		playing = False
		for name in os.listdir("./tts_audio"):
			os.remove("tts_audio/"+name)

def make_tts_player(words, lang, reverse, speed, voice_client):
	filenum = len([name for name in os.listdir('./tts_audio') if os.path.isfile(name)])
	filename = "tts_audio/tts{0}.mp3".format(filenum)

	speech = gTTS(text=words, lang=lang)
	speech.save(filename)

	if reverse or speed != 1.0:
		segs = pydub.AudioSegment.from_mp3(filename)
		if reverse:
			segs = segs.reverse()

		if speed != 1.0:
			segs = segs.speedup(playback_speed=speed)
		segs.export(filename, format="mp3")

	return voice_client.create_ffmpeg_player(filename, after=play_if_enqueued)

def get_tts_args(args):
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