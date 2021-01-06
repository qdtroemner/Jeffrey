import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord import Spotify

from reqs import jeffreyActions, facts, translate
from reqs.random_lyrics import get_random_song
from requests import get
from random import random, choice, randint
from datetime import datetime

class TextCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def send_random_metadata(self, ctx):
		try:	
			data = get_random_song()["response"]["song"]
			# print(data)
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

	"""
	@commands.command()
	async def status(self, ctx):
		await ctx.send(ctx.author.activity)
		await ctx.send(ctx.author.avatar_url)
	"""

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
					print(start_time)

					embed = discord.Embed(title=title, description=author, colour=activity.color)
					embed.set_author(name=album)
					# embed.add_field(name="Lyrics", value="words, words, words", inline=False)
					embed.set_thumbnail(url=thumbnail)
					embed.set_image(url=album_cover)
					embed.set_footer(text=duration)
					await ctx.send(embed=embed)

	@commands.command(decription='Jeffery sends you a random song.')
	async def song(self, ctx):
		await self.send_random_metadata(ctx)

def setup(bot):
	bot.add_cog(TextCommands(bot))