import discord
from discord.ext import commands

import youtube_dl
import os
from random import choice
from time import sleep

class VoiceCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.srcdir = 'C:/Users/qdtro/Desktop/Docs/Projects/Python/Jeffrey/src'
		self.audiodir = os.path.join(self.srcdir, 'audio')

	async def connect(self, ctx):
		channel = ctx.author.voice.channel
		voice = ctx.guild.voice_client

		if voice and voice.is_connected():
			voice.move_to(channel)
		else:
			voice = await channel.connect()

		await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
		return voice

	@commands.command(description='Jeffrey joins voice channel')
	async def join(self, ctx):
		await self.connect(ctx)

	@commands.command(description='Jeffrey leaves the voice channel')
	async def leave(self, ctx):
		voice = ctx.guild.voice_client
		if voice:
			await voice.disconnect()
		else:
			await ctx.send('Error or not connected.')

	@commands.command(description='')
	async def pause(self, ctx):
		voice = ctx.guild.voice_client
		if voice:
			if voice.is_playing():
				voice.pause()
			else:
				await ctx.send('Not playing anything.')
		else:
			await ctx.send('Not connected.')

	@commands.command(description='')
	async def stop(self, ctx):
		voice = ctx.guild.voice_client
		if voice:
			if voice.source:
				voice.stop()
			else:
				await ctx.send('Not playing anything or nothing paused.')
		else:
			await ctx.send('Not connected.')

	async def playYoutube(self, ctx, link, loop):
		voice = ctx.guild.voice_client
		YT_FFMPEG_OPTIONS = {
			'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ',
			'options': '-vn '
		}
		ydl_opts = {
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3'
			}],
		}

		YT_FFMPEG_OPTIONS['before_options'] += '-stream_loop -1 ' if loop else ''

		if(not voice or not voice.is_connected):
			channel = ctx.author.voice.channel
			voice = await channel.connect()

		if(link != None):
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				data = ydl.extract_info(link, download=False)

			input_url = data['formats'][0]['url']
			title = data['title']
			uploader = data['uploader']
			if(input_url):
				source = discord.FFmpegPCMAudio(input_url, **YT_FFMPEG_OPTIONS)
				source = discord.PCMVolumeTransformer(source, volume=0.2)
				await ctx.send(f'Now Playing **{title}** by *{uploader}*.')
				voice.play(source)
		else:
			await ctx.send("Not A Valid Link")

	async def lookForAndPlay(self, ctx, query, loop, volume):
		voice = ctx.guild.voice_client
		if(not voice or not voice.is_connected):
			channel = ctx.author.voice.channel
			voice = await channel.connect()

		b_opt = '-stream_loop -1' if loop else ''

		filelist = []
		for path, dir, files in os.walk(self.audiodir):
			filelist += files
		for file in filelist:
			if query in file:
				voice = ctx.guild.voice_client
				source = discord.FFmpegPCMAudio(os.path.join(self.audiodir, file), before_options=b_opt)
				source = discord.PCMVolumeTransformer(source, volume)
				voice.play(source)

	@commands.command(description='Jeffrey Will Play a Youtube Link')
	async def play(self, ctx, query=None, loop=False, volume=0.2):  # Query: URL or File name
		channel = ctx.author.voice.channel
		voice = ctx.guild.voice_client

		if voice: # If we're already connected to a channel
			if voice.source and voice.is_paused() and query is None: # If we already have a song but it's paused and no input was given
				voice.resume()
			else: # If user is trying to play an audio
				if query and voice.is_playing() or voice.source: # If we've got something playing or paused but want something new
					voice.stop() # Stop so we can get a new song
			
				if 'https://www.youtube.com' in query: # If it's a YouTube link
					await self.playYoutube(ctx, query, loop=loop)
				else: # Handle it as an audio file name
					await self.lookForAndPlay(ctx, query, loop=loop, volume=volume)

				# await ctx.guild.change_voice_state(channel=channel, self_deaf=True) # Deafen ourself
		else: # If we're not connected to any channel yet
			await self.connect(ctx)
			await self.play(ctx, query, loop)

	@commands.command()
	async def burn(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
			channel = user.voice.channel
		else:
			await ctx.send("I need a person to burn...")
			return

		voice = ctx.guild.voice_client
		if voice and voice.channel:
			if user and channel:
				await voice.move_to(channel)
				source = discord.FFmpegPCMAudio(os.path.join(self.audiodir, 'burn.mp3'), before_options='-stream_loop -1')
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

	# @commands.command(description=)

def setup(bot):
	bot.add_cog(VoiceCommands(bot))
