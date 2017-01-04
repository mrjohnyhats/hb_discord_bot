from league import League
from riotwatcher import LoLException
from discord.ext import commands
from gtts import gTTS
import riotwatcher, discord, asyncio, random, os, sys, pydub, re

league = League()

bot = commands.Bot(command_prefix="$", description="a bot that executes commands sometimes")

MY_ID = "171332734130716673"
PRANAV_ID = "171332734130716673"
OOSHERS_ID = "175784723715588107"
TOKEN = "MjY2MzE2NTA1ODA3OTc4NDk3.C076GQ.58m6_4MyFg5LtIpUNVb3wMQrK5k"
LANGS = [
"af",
"sq",
"ar",
"hy",
"bn",
"ca",
"zh",
"zh-cn",
"zh-tw",
"zh-yue",
"hr",
"cs",
"da",
"nl",
"en",
"en-au",
"en-uk",
"en-us",
"eo",
"fi",
"fr",
"de",
"el",
"hi",
"hu",
"is",
"id",
"it",
"ja",
"ko",
"la",
"lv",
"mk",
"no",
"pl",
"pt",
"pt-br",
"ro",
"ru",
"sr",
"sk",
"es",
"es-es",
"es-us",
"sw",
"sv",
"ta",
"th",
"tr",
"vi",
"cy"
]

ADMINS = {
	MY_ID: ["*"],
	PRANAV_ID: [OOSHERS_ID]
}

voice_client = None

if not discord.opus.is_loaded():
	discord.opus.load_opus("opus")

def is_admin(id : str, server_id : str):
	if ADMINS[id] == "*" or server_id in ADMINS[id]:
		return True
	return False

def make_tts(words, lang, reverse, speed):
	if os.path.isfile("tts.mp3"):
		os.remove("tts.mp3")

	speech = gTTS(text=words, lang=lang)
	speech.save("tts.mp3")

	if reverse or speed != 1.0:
		segs = pydub.AudioSegment.from_mp3("tts.mp3")
		if reverse:
			segs = segs.reverse()

		if speed != 1.0:
			segs = segs.speedup(playback_speed=speed)
		segs.export("tts.mp3", format="mp3")

@asyncio.coroutine
def be_jianyang(msg):
	if msg.content[0] != "$" and bot.user.id != msg.author.id:
		yield from bot.send_message(msg.channel, "I eat the fish")

bot.is_jianyang = False

@bot.event
@asyncio.coroutine
def on_ready():
	print("ready!")
	yield from bot.change_presence(game=discord.Game(name="with his penis"))


@bot.command(pass_context=True)
@asyncio.coroutine
def toggle_jianyang(ctx):
	if is_admin(ctx.message.author.id, ctx.message.server.id):
		if bot.is_jianyang:
			bot.is_jianyang = False
			bot.remove_listener(be_jianyang, "on_message")
		else:
			bot.add_listener(be_jianyang, "on_message")
			bot.is_jianyang = True
	else:
		yield from bot.say("member {0} isn't allowed to toggle jian yang :(".format(member.name))

@bot.command(pass_context=True)
@asyncio.coroutine
def join_vchan(ctx):
	global voice_client
	if type(ctx.message.author).__name__ is "User":
		member = ctx.message.server.get_member(ctx.message.author.id)
		if member == None:
			yield from bot.say("the server doesn't see you as a member :\\")
			return False
		chan = member.voice_channel
	else:
		chan = ctx.message.author.voice_channel

	if chan is None:
		yield from bot.say("please join a voice channel before asking me to join one with you")
	else:
		if voice_client is None:
			voice_client = yield from bot.join_voice_channel(chan)
		else:
			yield from voice_client.move_to(chan)

@bot.command(pass_context=True)
@asyncio.coroutine
def stop(ctx):
	if ctx.message.author.id == MY_ID:
		sys.exit()
	else:
		yield from bot.say("you can't stop me!")

@bot.command(pass_context=True)
@asyncio.coroutine
def say(ctx, words, args=""):
	if len(words) == 0:
		yield from bot.say("please give me a string of words to say")
		return False

	try:
		yield from join_vchan.callback(ctx)
	except discord.InvalidArgument:
		yield from bot.say("not a valid voice channel :/")
		return False

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

	make_tts(words, lang, reverse, speed)

	try:
		player = voice_client.create_ffmpeg_player("tts.mp3")
	except Exception as e:
		yield from bot.say("an error occured creating the player {0}: {1}".format(type(e).__name__, e))
	else:
		player.start()


@bot.command()
@asyncio.coroutine
def givemerick():
	yield from bot.say("Rick is here for you https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@bot.command()
@asyncio.coroutine
def choose(*choices : str):
    yield from bot.say(random.choice(choices))

@bot.command()
@asyncio.coroutine
def getgame(summ_name : str):
	try:
		game = league.get_cur_game(summ_name)
		time = game["gameLength"]
		secs = int(time%60)
		mins = int((time-secs)/60)

		yield from bot.say("{0} has been in game for {1} minutes and {2} seconds".format(summ_name, secs, mins))

	except LoLException:
		yield from bot.say(summ_name + " is not in game")

bot.run(TOKEN)
