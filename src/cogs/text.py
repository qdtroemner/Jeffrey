import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord import Spotify

from reqs import jeffreyActions, facts, translate
from reqs.random_lyrics import get_random_song, get_lyrics
from requests import get
from random import random, choice, randint
from datetime import datetime

class TextCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def send_random_metadata(self, ctx):
		try:	
			data = get_random_song()["response"]["song"]
			title = data["title"]
			album = data["album"]["name"]
			url = data["url"]
			author = data["primary_artist"]["name"]
			author_url = data["primary_artist"]["url"]
			thumbnail = data["header_image_url"]

			embed = discord.Embed(title=title, description=album, url=url, colour=discord.Colour.from_hsv(random(), 1, 1))
			embed.set_author(name=author, url=author_url)
			# embed.add_field(name="Lyrics", value="words, words, words", inline=False)
			embed.set_thumbnail(url=thumbnail)
			# embed.set_footer(text="Record Label")
			try:
				await ctx.send(embed=embed)
			except Exception as error:
				await self.send_random_metadata(ctx)
		except TypeError as t_error:
			await self.send_random_metadata(ctx)


	@commands.command(decription='Jeffery greets you')
	async def hello(self, ctx):
		await ctx.send(choice(jeffreyActions.greetings))

	@commands.command(decription='Jeffery greets you')
	async def hello(self, ctx):
		await ctx.send(choice(jeffreyActions.greetings))

	@commands.command(description='Jeffrey does a flip')
	async def flip(self, ctx):
		await ctx.send(choice(jeffreyActions.flip))

	@commands.command(description='Jeffrey spins')
	async def spin(self, ctx):
		await ctx.send(choice(jeffreyActions.spin))

	@commands.command(description='Jeffrey sends a gif')
	async def gif(self, ctx):
		await ctx.send(choice(jeffreyActions.randomGif))

	@commands.command(description='Jeffrey steals')
	async def steal(self, ctx):
		await ctx.send(choice(jeffreyActions.steal))

	@commands.command(description='Jeffrey fights')
	async def fight(self, ctx):
		await ctx.send(choice(jeffreyActions.fight))
	
	@commands.command(description='Jeffrey says a random fact')
	async def fact(self, ctx):
		await ctx.send(facts.getFact())

	@commands.command(description='Jeffrey translates phrase to monkey language')
	async def monkify(self, ctx, phrase):
		await ctx.send(translate.translateToMonkey(phrase))

	@commands.command(description='Jeffrey translates monkey language to English')
	async def demonkify(self, ctx, phrase):
		await ctx.send(translate.translateToEnglish(phrase))

	@commands.command(description='Jeffrey sends a random Roblox profile')
	async def roblox(self, ctx):
		url = f'https://www.roblox.com/users/{randint(1, 2000000000)}/profile'
		status = get(url).status_code
		if status == 200:
			await ctx.send(url)
		else:
			print("Roblox user doesn't exist; retrying...")
			self.roblox(ctx)

	@commands.command(description='Jeffrey sends a random wikipedia article')
	async def wikipedia(self, ctx):
		base_url = 'https://en.wikipedia.org/wiki/Special:Random'
		url = get(base_url).url
		await ctx.send(url)

	@commands.command()
	async def status(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		for activity in user.activities:
			if isinstance(activity, discord.activity.CustomActivity):
				title = activity.name
				thumbnail = user.avatar_url
				icon = discord.Embed.Empty
				if hasattr(activity, 'emoji'):
					emoji = activity.emoji
					if hasattr(emoji, 'url'):
						emoji_url = emoji.url
						author_icon = emoji_url
					if emoji: # In case it's None
						title = f"{emoji} {title}"

				embed = discord.Embed(title=title, colour=discord.Colour.from_hsv(random(), 1, 1))
				embed.set_author(name=user, icon_url=icon)
				embed.set_thumbnail(url=thumbnail)
				await ctx.send(embed=embed)

	@commands.command(description="Jeffrey sends a user's Spotify activity.")
	async def spotify(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		if user.activities:
			for activity in user.activities:
				if isinstance(activity, discord.Spotify):
					title = activity.title
					album = activity.album
					# url = activity.track_id
					author = activity.artist
					# author_url = 
					thumbnail = user.avatar_url
					album_cover = activity.album_cover_url
					duration = activity.duration
					start_time = activity.created_at

					embed = discord.Embed(title=title, description=author, colour=activity.color)
					embed.set_author(name=album)
					# embed.add_field(name="Lyrics", value="words, words, words", inline=False)
					embed.set_thumbnail(url=thumbnail)
					embed.set_image(url=album_cover)
					embed.set_footer(text=duration)
					await ctx.send(embed=embed)

	@commands.command(aliases=["activity"], description="Jeffrey sends a user's general Discord activity.")
	async def activities(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		if user.activities:
			pfp = user.avatar_url
			for activity in user.activities:
				print(activity, activity.type)
				EMPTY = discord.Embed.Empty
				title = activity.name
				desc = None
				embed_url = None
				# video = None # Possibly add video options later?
				color = None
				timestamp = None

				name = None
				author_icon = None
				author_url = None

				thumbnail = user.avatar_url

				image_url = None

				footer = None
				footer_icon = None

				embed = discord.Embed()

				# FIELDS ARE SET MANUALLY
				if activity.type == discord.ActivityType.listening:
					name = activity.album
					title = activity.title
					desc = activity.artist
					color = activity.color
					timestamp = activity.start
					
					image_url = activity.album_cover_url

				elif activity.type == discord.ActivityType.playing:
					name = user
					title = activity.name

					# GET ALL IMAGES (SOME AREN'T DISPLAYING)

					if hasattr(activity, 'url'):
						embed_url = activity.url
					if hasattr(activity, 'details'):
						desc = activity.details
					if hasattr(activity, 'application_id'):
						footer = activity.application_id
					if hasattr(activity, 'large_image_url'):
						image_url = activity.large_image_url
					elif hasattr(activity, 'small_image_url'):
						image_url = activity.small_image_url
					if hasattr(activity, 'timestamps'):
						if hasattr(activity.timestamps, 'start'):
							timestamp = activity.timestamps.start
					if hasattr(activity, 'emoji'):
						emoji = activity.emoji
						if hasattr(emoji, 'url'):
							emoji_url = emoji.url
							author_icon = emoji_url
						if emoji: # In case it's None
							title = f"{emoji} {title}"
					
				elif activity.type == discord.ActivityType.streaming:
					name = user
					title = activity.name

				elif activity.type == discord.ActivityType.watching:
					name = user
					title = activity.name

				elif activity.type == discord.ActivityType.custom:
					name = user
					title = activity.name

					if hasattr(activity, 'emoji'):
						emoji = activity.emoji
						if hasattr(emoji, 'url'):
							emoji_url = emoji.url
							author_icon = emoji_url
						else:
							title = f"{emoji} {title}"

				embed.title = title
				embed.description = desc or EMPTY
				embed.url = embed_url or EMPTY
				embed.colour = color or discord.Colour.from_hsv(random(), 1, 1)
				embed.timestamp = timestamp or EMPTY
				# (title=title, description=desc or EMPTY, url=embed_url or EMPTY, color=color or discord.Colour.from_hsv(random(), 1, 1), timestamp=timestamp)
				if name:
					embed.set_author(name=name, icon_url=author_icon or EMPTY, url=author_url or EMPTY)
				if thumbnail:
					embed.set_thumbnail(url=thumbnail or user.avatar_url)
				if image_url:
					embed.set_image(url=image_url)
				if footer:
					embed.set_footer(text=footer, icon_url=footer_icon or EMPTY)
				await ctx.send(embed=embed)

	@commands.command(decription='Jeffery sends you a random song.')
	async def song(self, ctx):
		await self.send_random_metadata(ctx)

	@commands.command(decription='Jeffery sends you Spotify song lyrics.')
	async def lyrics(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		if user.activities:
			print(user.activities)

			for activity in user.activities:
				if isinstance(activity, discord.Spotify):
					artist = activity.artists[0]
					song = activity.title
					thumbnail = activity.album_cover_url

					lyrics = get_lyrics(artist, song)

					if lyrics:
						embed = discord.Embed(title=song, description=artist, colour=discord.Colour.from_hsv(random(), 1, 1))
						embed.set_thumbnail(url=thumbnail)
						# embed.set_author(name=artist)
						for verse in lyrics:
							embed.add_field(name="​", value=verse or "None, missing, or recently requested.", inline=False)
						try:
							await ctx.send(embed=embed)
						except Exception as error:
							print(error)
							await ctx.send("Lyrics too long.")
					else:
						await ctx.send("Lyrics either missing from database, or fetching error.")
		else:
			await ctx.send("Couldn't get your Spotify details.")

	@commands.command(decription='Jeffery tells you if a user has Nitro or not.')
	async def nitro(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		if user.premium_since:
			await ctx.send(f"{user} has Discord Nitro.")
		else:
			await ctx.send(f"{user} does not have Discord Nitro.")

	@commands.command(description='Turns text into emojis.')
	async def emojify(self, ctx, text):
		if text and type(text) == str:
			await ctx.send(translate.emojify(text))

	"""
	@commands.command(decription='Jeffery sends you Spotify song lyrics.')
	async def test(self, ctx):
		embed = discord.Embed(title='')
	"""

def setup(bot):
	bot.add_cog(TextCommands(bot))