import discord, os
from discord.ext import commands

class Sound_system:
	queue = []
	playing = False

	def __init__(self, voice_client):
		self.voice_client = voice_client

	def add_to_queue(self, player):
		self.queue.append(player)

	def play_if_enqueued(self):
		if len(self.queue) > 0:
			self.playing = True
			curplayer = self.queue.pop(0)
			curplayer.start()
		else:
			self.playing = False

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

		self.add_to_queue(player)
		if not self.playing:
			self.play_if_enqueued()