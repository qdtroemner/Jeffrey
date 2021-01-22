import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord import Spotify

import os
import cv2
import numpy as np
import aiohttp
from io import BytesIO
import cmapy

# PATH = os.path.dirname(__file__)

class ImageCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		"""self.color_mappings = {
			'heatmap': cv2.LUT(os.path.join(PATH, '../colormappings/heatmap.png')),
			'infrared': cv2.LUT(os.path.join(PATH, '../colormappings/infrared.png'))
		}"""

	async def url_to_image(self, url):
		# Setup and get data from URL
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as req:
				if req.status == 200:
					# Convert URL data to image
					image = np.asarray(bytearray(await req.read()), dtype="uint8")
					image = cv2.imdecode(image, cv2.IMREAD_COLOR)
					return image

	def cv2_to_file(self, img):
		image_string = cv2.imencode('.jpg', img)[1].tostring()
		return BytesIO(image_string)

	@commands.command(description='Jeffrey turns your image into an IR heatmap.')
	async def heatmap(self, ctx):
		if len(ctx.message.attachments) >= 1:
			for attachment in ctx.message.attachments:
				url = attachment.url
				# Color image as heatmap
				image = await self.url_to_image(url)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
				# Send bytes as a file
				await ctx.send(file=discord.File(self.cv2_to_file(heatmap), filename='output.jpg'))
		#elif ctx.message.mentions:
		#	for mention in ctx.message.mentions:	

	@commands.command(aliases=['ir'], description='Jeffrey turns your image infrared.')
	async def infrared(self, ctx):
		if len(ctx.message.attachments) >= 1:
			for attachment in ctx.message.attachments:
				url = attachment.url
				# Color image as heatmap
				image = await self.url_to_image(url)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
				# Send bytes as a file
				await ctx.send(file=discord.File(self.cv2_to_file(heatmap), filename='output.jpg'))

	@commands.command(aliases=['color'], description='Jeffrey colorizes your image with a cv2 colormap.')
	async def colorize(self, ctx, mapping="HSV"):
		if len(ctx.message.attachments) >= 1:
			for attachment in ctx.message.attachments:
				url = attachment.url
				# Color image as heatmap
				image = await self.url_to_image(url)
				mapping = mapping.upper()
				try:
					mapping = getattr(cv2, f"COLORMAP_{mapping}")
				except Exception:
					mapping = cv2.COLORMAP_HSV
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				heatmap = cv2.applyColorMap(gray, mapping)
				# Send bytes as a file
				await ctx.send(file=discord.File(self.cv2_to_file(heatmap), filename='output.jpg'))

	@commands.command(aliases=['mcolor'], description='Jeffrey colorizes your image with a matplotlib colormap.')
	async def matplotcolor(self, ctx, mapping="hsv"):
		if len(ctx.message.attachments) >= 1:
			for attachment in ctx.message.attachments:
				url = attachment.url
				# Color image as heatmap
				image = await self.url_to_image(url)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				try:
					mapping = cmapy.cmap(mapping)
				except Exception:
					mapping = cmapy.cmap('hsv')
				colormap = cv2.applyColorMap(gray, mapping)
				# Send bytes as a file
				await ctx.send(file=discord.File(self.cv2_to_file(colormap), filename='output.jpg'))

	@commands.command(description='Jeffrey sends a profile picture.')
	async def pfp(self, ctx):
		if ctx.message.mentions:
			user = ctx.message.mentions[0]
		else:
			user = ctx.author

		await ctx.send(user.avatar_url)

def setup(bot):
	bot.add_cog(ImageCommands(bot))