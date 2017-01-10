from league import League
from riotwatcher import LoLException
from discord.ext import commands
from gtts import gTTS
from sound_system import Sound_system
import riotwatcher, discord, asyncio, random, os, sys, pydub, re, tts

league = League()

bot = commands.Bot(command_prefix="$", description="a bot that executes commands sometimes")

MY_ID = "171332734130716673"
PRANAV_ID = "171332734130716673"
OOSHERS_ID = "175784723715588107"
TOKEN = "MjY2MzE2NTA1ODA3OTc4NDk3.C076GQ.58m6_4MyFg5LtIpUNVb3wMQrK5k"
LANGS = ["af","sq","ar","hy","bn","ca","zh","zh-cn","zh-tw","zh-yue","hr","cs","da","nl","en","en-au","en-uk","en-us","eo","fi","fr","de","el","hi","hu","is","id","it","ja","ko","la","lv","mk","no","pl","pt","pt-br","ro","ru","sr","sk","es","es-es","es-us","sw","sv","ta","th","tr","vi","cy"]

ADMINS = {
	MY_ID: ["*"],
	PRANAV_ID: [OOSHERS_ID]
}

class Server_sound:
	def __init__(self, voice_client):
		def after_queue(sound_sys):
			server_id = sound_sys.voice_client.server.id
			for name in os.listdir("./tts_audio/"+server_id):
				if os.path.isfile("./tts_audio/{0}/{1}".format(server_id, name)):
					os.remove("./tts_audio/{0}/{1}".format(server_id, name))

		self.sound_sys = Sound_system(voice_client, after_queue=after_queue)
		self.voice_client = voice_client

server_sounds = {}

if not discord.opus.is_loaded():
	discord.opus.load_opus("opus")

def is_admin(id : str, server_id : str):
	if ADMINS[id] == "*" or server_id in ADMINS[id]:
		return True
	return False

def member_from_ctx(ctx):
	member = ctx.message.author
	if type(ctx.message.author).__name__ is "User":
		member = ctx.message.server.get_member(ctx.message.author.id)
		if member == None:
			yield from bot.say("this server doesn't see you as a member :/")
			return None

	return member

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
	global server_sounds

	member = yield from member_from_ctx(ctx)
	if member == None:
		return False

	chan = member.voice_channel
	server_id = ctx.message.author.server.id

	if chan is None:
		yield from bot.say("please join a voice channel before asking me to join one with you")
	else:
		try:
			if not server_id in server_sounds:
				vclient = yield from bot.join_voice_channel(chan)
				server_sounds[server_id] = Server_sound(vclient)
			else:
				yield from server_sounds[server_id].voice_client.move_to(chan)
		except discord.InvalidArgument:
			yield from bot.say("not a valid voice channel :/")

@bot.command(pass_context=True)
@asyncio.coroutine
def next_sound(ctx):
	member = yield from member_from_ctx(ctx)
	if member == None:
		return False
	elif not member.server.id in server_sounds:
		yield from bot.say("the bot isn't in a voice channel on this server")
		return False

	server_sounds[member.server.id].sound_sys.next_in_queue()

@bot.command(pass_context=True)
@asyncio.coroutine
def sound(ctx, file : str):
	filename = "recording/{0}.mp3".format(file)
	if not os.path.exists(filename):
		yield from bot.say(file + ".mp3 is not a recording file")
	else:
		yield from join_vchan.callback(ctx)

		server_id = ctx.message.author.server.id

		server_sounds[server_id].sound_sys.play(filename)


@bot.command(pass_context=True)
@asyncio.coroutine
def stopbot(ctx):
	if ctx.message.author.id == MY_ID:
		sys.exit()
	else:
		yield from bot.say("you can't stop me!")

@bot.command(pass_context=True)
@asyncio.coroutine
def say(ctx, words, args=""):
	yield from join_vchan.callback(ctx)

	server_id = ctx.message.author.server.id
	parsed_args = yield from tts.parse_args(args)
	filename = tts.make_tts_file(words, parsed_args, server_id)

	server_sounds[server_id].sound_sys.play(filename)

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
