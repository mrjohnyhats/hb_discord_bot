import discord, os, asyncio
from discord.ext import commands

class Sound_system:
	queue = []
	playing = False
	curplayer = None
	after_queue = None

	def __init__(self, voice_client, after_queue=None):
		self.voice_client = voice_client
		if after_queue != None:
			if callable(after_queue):
				self.after_queue = after_queue
			else:
				raise TypeError("'after_queue' argument must be callable")

	def queue_player(self, player):
		self.queue.append(player)
		if not self.playing:
			self.play_if_enqueued()

	def play_if_enqueued(self):
		if len(self.queue) > 0:
			print("playing next in queue")
			self.playing = True
			self.curplayer = self.queue.pop(0)
			self.curplayer.start()
		else:
			self.playing = False
			if self.after_queue != None:
				self.after_queue(self)

	def play(self, soundfile, custom_after=None):
		if os.path.exists(soundfile):
			if custom_after == None:
				after = self.play_if_enqueued
			else:
				def after():
					custom_after()
					self.play_if_enqueued()

			player = self.voice_client.create_ffmpeg_player(soundfile, after=after)
		else:
			raise FileNotFoundError("soundfile does not exist")

		self.queue_player(player)

	def stop(self):
		self.queue = []
		self.next_in_queue()

	@asyncio.coroutine
	def yt_play(self, query, custom_after=None):
		if custom_after == None:
			after = self.play_if_enqueued
		else:
			def after():
				custom_after()
				self.play_if_enqueued()
		opts = {
			"default_search": "auto"
		}
		player = yield from self.voice_client.create_ytdl_player(query, after=after, ytdl_options=opts)
		self.queue_player(player)

	def next_in_queue(self):
		if self.playing:
			self.curplayer.stop()

	# def queue_new_ytdl_player_syncronous(self, query, **kwargs):
	# 	loop = asyncio.get_event_loop()
	# 	def background_task():
	# 		self.voice_client.create_ytdl_player
	# 	loop.run_in_executor(self.voice_client.create_ytdl_player(query, **kwargs))
