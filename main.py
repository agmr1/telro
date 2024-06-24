import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import requests

client = commands.Bot(command_prefix="ai!")
token = os.getenv('DISCORD_TOKEN')

def cuaca(msg):
    try:
        location = msg
        response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=b4c828b2560f44bcbfa125319242404&q={location}&days=0&aqi=no&alerts=no")
        forecast = json.loads(response.text)

        loc = [f"{x} : {forecast['location'][x]}" for x in forecast["location"]]
        current_temp_c = forecast['current']['temp_c']
        current_condition = forecast["current"]["condition"]["text"]
        icon = forecast["current"]["condition"]["icon"]

        smr_forecastday_hour_return = []
        smr_forecastday_day_return = []

        for y in range(len(forecast["forecast"]["forecastday"])):
            smr_forecastday_hour_return.append(str(y))
            for x in range(len(forecast["forecast"]["forecastday"][y]["hour"])):
                forecatday_time = forecast["forecast"]["forecastday"][y]["hour"][x]["time"]
                forecastday_condition = forecast["forecast"]["forecastday"][y]["hour"][x]["condition"]["text"]
                forecastday_temp_c = forecast["forecast"]["forecastday"][y]["hour"][x]["temp_c"]
                smr_forecastday_hour = f"time : {forecatday_time}\ntemp_c : {forecastday_temp_c}\ncondition : {forecastday_condition}\n"
                smr_forecastday_hour_return.append(smr_forecastday_hour)

        for y in range(len(forecast["forecast"]["forecastday"])):
            smr_forecastday_day_return.append(str(y))
            for key, value in forecast["forecast"]["forecastday"][y]["day"].items():
                if isinstance(value, dict):
                    value = [f"{k}: {v}" for k, v in value.items()][0]
                smr_forecastday_day = f"{key} : {value}"
                smr_forecastday_day_return.append(smr_forecastday_day)

        locc = '\n'.join(loc)
        dayy = '\n'.join(smr_forecastday_day_return)
        hourr = '\n'.join(smr_forecastday_hour_return)

        smr_final = f"{locc}\ncurrent_temp_c : {current_temp_c}\ncurrent_condition : {current_condition}\n\nicon : {icon}"
        return smr_final
    except Exception as e:
        return e

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

'''client.command()
async def clear(ctx, amount=3):
	await ctx.channel.purge(limit=amount)'''
	
@client.command()
async def weather(ctx, arg1):
    try:
        psn = await ctx.reply(f"processing...{arg1}")
        hsl = cuaca(str(arg1))
        embed = discord.Embed(color = 0xff9900, title = hsl.split("current_condition : ")[1].split("\n\n")[0]) #  Embed'a
        embed.set_image(url = f'https:{hsl.split("icon : ")[1]}')
        await psn.edit(embed = embed,content=hsl.split("icon")[0])
    except Exception as e:
        await psn.edit(content=e)
    
client.run(token)
