import discord
from discord.ext import commands

from reqs import jeffreyActions, facts, translate
from reqs.secrets import TOKEN

from random import choice
import youtube_dl
import os
import sys

INITIAL_EXTENTIONS = [
    'cogs.text',
	'cogs.voice'
]

INTENTS = discord.Intents().all()

class Client(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix=('monke ', 'jeffrey ', '$'),
			case_insensitive=True,
			intents=INTENTS
		)
		# super().remove_command('help')
		
		# Import the cog command groups
		for extension in INITIAL_EXTENTIONS:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(f'Failed to load extension {extension}. Because: {e}')
	
	async def on_ready(self):
		print(f'Logged in as {self.user}!')
		await self.change_presence(activity=discord.Game('humans'))

client = Client()
client.run(TOKEN)