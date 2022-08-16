import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv('.env')
client = commands.Bot(command_prefix="ai!")
token = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
	await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
print("I am online")

@client.command()
async def ping(ctx):
	await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command()
async def whoami(ctx):
	await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3):
	await ctx.channel.purge(limit=amount)

@client.command(name="rubah")
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-
    json_data = json.loads(response.text) #  JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') #  Embed'a
    embed.set_image(url = json_data['link']) #   Embed'a
    await ctx.send(embed = embed) #  Embed
    
client.run(token)
