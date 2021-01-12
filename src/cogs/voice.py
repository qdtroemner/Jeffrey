import discord
from discord import voice_client
from discord.ext import commands

import youtube_dl
import os
from random import choice
from time import sleep
import re

class VoiceCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.src_dir = 'C:/Users/qdtro/Desktop/Docs/Projects/Python/Jeffrey/src'
		self.audio_dir = os.path.join(self.src_dir, 'audio')

	def AudioError(self, error):
		print(error)

	@commands.command(aliases=['connect', 'jo', 'j'])
	async def join(self, ctx):
		if not ctx.author.voice:
			await ctx.send('You are not connected to a voice channel.')

		channel = ctx.author.voice.channel
		
		if ctx.voice_client:
			await ctx.voice_client.move_to(channel)
		else:
			await channel.connect()
		await ctx.guild.change_voice_state(channel=channel, self_deaf=True, self_mute=False)

	@commands.command(aliases=['disconnect', 'le', 'l'])
	async def leave(self, ctx):
		if ctx.voice_client and ctx.voice_client.channel is ctx.author.voice.channel:
			await ctx.guild.change_voice_state(channel=None)

	@commands.command(aliases=['resume', 'pa', 're'])
	async def pause(self, ctx):
		if ctx.voice_client and ctx.voice_client.channel is ctx.author.voice.channel:
			voice = ctx.voice_client
			if voice.source:
				if voice.is_paused():
					voice.resume()
				else:
					voice.pause()
	
	@commands.command(aliases=['st'])
	async def stop(self, ctx):
		if ctx.voice_client and ctx.voice_client.channel is ctx.author.voice.channel:
			voice = ctx.voice_client
			if voice.source:
				voice.stop()

	@commands.command(aliases=['p'])
	async def play(self, ctx, query:str=None):
		src = None
		if ctx.voice_client and ctx.voice_client.channel is ctx.author.voice.channel:
			voice = ctx.voice_client

			if re.match("^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$", query):
				print("Youtube URL")

			if src is not None and isinstance(src, discord.AudioSource):
				voice.play(src, after=self.AudioError)

	"""
	@commands.command()
	async def burn(self, ctx):
		if ctx.message.mentions:
			users = ctx.message.mentions[0]
			channel = user.voice.channel
		else:
			await ctx.send("I need a person to burn...")
			return

		if voice and voice.channel:
			if user and channel:
				await voice.move_to(channel)
				source = discord.FFmpegPCMAudio(os.path.join(self.audio_dir, 'burn.mp3'), before_options='-stream_loop -1')
				source = discord.PCMVolumeTransformer(source, volume=0.2)
				voice.play(source)
				await user.edit(mute=True)
				sleep(10)
				await user.edit(deafen=True)
				sleep(10)
				await user.edit(mute=False, deafen=False, voice_channel=None) # None channel kicks them from their channel.
		else:
			if channel:
				await channel.connect()
				await self.burn(ctx)
	"""

def setup(bot):
	bot.add_cog(VoiceCommands(bot))