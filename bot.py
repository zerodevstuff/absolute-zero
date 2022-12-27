import discord
from discord import app_commands
from discord.ext import commands 
import requests
from requests.structures import CaseInsensitiveDict
import json
import sys
with open('config.json') as f:
    config = json.load(f)

token = config.get('token')
#from config.json import token

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())



@bot.event
async def on_ready():
    print("lunar smells")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
            print(e)


@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"hey {interaction.user.mention} the bot is working")

@bot.tree.command(name="changename")
@app_commands.describe(name = "new name")
@app_commands.describe(ssid = "session id")
async def changename(interaction: discord.Interaction, name:str, ssid: str):
    url = (f"https://api.minecraftservices.com/minecraft/profile/name/{name}")
    headers = CaseInsensitiveDict()
    headers["Authorization"] = (f"Bearer {ssid}")
    headers["Content-Type"] = "application/json"
    headers["Content-Length"] = "0" 
    resp = requests.put(url, headers=headers)
    if resp.ok:
        await interaction.response.send_message(f"{resp.status_code}\nhttps://namemc.com/profile/{name}")
    else:
        await interaction.response.send_message(f"{resp.status_code} there was an issue with the ssid please ensure the ssid is valid")


@bot.tree.command(name = "changeskin")
@app_commands.describe(skin = "link to skin (must be a png)")
@app_commands.describe(ssid = "session id")
async def changeskin(interaction: discord.Interaction, skin:str, ssid:str):
    url = ("https://api.minecraftservices.com/minecraft/profile/skins")
    
    headers = {
    'Authorization': (f"Bearer {ssid}"),
    'Content-Type': 'application/json; charset=utf-8',
}
    json_data = {
    'variant': 'classic',
    'url': (f"{skin}"),
}
    respuuid = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers).json()
    respuuidgot = respuuid.get("id")
    respnamegot = respuuid.get("name")
    resp = requests.post(url, headers=headers, json=json_data)
    if resp.ok:
        await interaction.response.send_message(f"{resp.status_code}\n changed the skin of {respnamegot} https://namemc.com/profile/{respuuidgot}")
    else:
        await interaction.response.send_message(f"{resp.status_code} there was an issue with the ssid please ensure the ssid is valid")

@bot.tree.command(name = "lookup")
@app_commands.describe(ssid = "session id")
async def lookup(interaction: discord.Interaction, ssid:str):
    headers = CaseInsensitiveDict()
    uuidheaders = {
    'Authorization': (f"Bearer {ssid}"),
    'Content-Type': 'application/json; charset=utf-8',
    }
    respuuid = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=uuidheaders).json()
    respuuidgot = respuuid.get("id")
    await interaction.response.send_message(f"{respuuidgot}")

@bot.tree.command(name = "iplookup")
@app_commands.describe(ip = "IP to search")
async def iplookup(interaction: discord.Interaction, ip:str):
    resp = requests.get(f"http://ip-api.com/json/{ip}?fields=66322431").json()
    ipcontinent = resp.get("continent")
    ipcontinentCode = resp.get("continentCode")
    ipcountry = resp.get("country")
    ipcountryCode = resp.get("countryCode")
    ipregion = resp.get("region")
    ipregionName = resp.get("regionName")
    ipcity = resp.get("city")
    ipzip = resp.get("zip")
    iptimezone = resp.get( "timezone")
    ipcurrency = resp.get("currency") 
    ipisp = resp.get("isp")
    iporg = resp.get("org")
    ipas = resp.get("as")
    ipasname = resp.get("asname")
    ipreverse = resp.get("reverse")
    ipmobile = resp.get("mobile")
    ipproxy = resp.get("proxy")
    iphosting = resp.get("hosting")
    embed=discord.Embed(title=(f"Scan for {ip} from {ipcountry} ({ipcountryCode})"))
    embed.add_field(name=(f"Continent"), value=(f"{ipcontinent} ({ipcontinentCode})"), inline=False)
    embed.add_field(name="GeoLocation", value=(f"{ipcity}, {ipregionName} ({ipzip})"), inline=False)
    embed.add_field(name="Region Info", value=(f"TimeZone: {iptimezone} \n Currency: {ipcurrency}"), inline=False)
    embed.add_field(name="Hosting Info", value=(f"Mobile: {ipmobile} \n Proxy: {ipproxy} \n Hosting: {iphosting}"), inline=False)
    await interaction.response.send_message(embed=embed)
bot.run(token)