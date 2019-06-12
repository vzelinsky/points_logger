import discord
import json
from points_parser import s_parse_add_points

config_fn = "config.json"
try:
    config = json.load(open(config_fn, "r"))
    discord_bot_token = config["discord_bot_token"]
except IOError:
    print("ERROR: {0} could not be opened.".format(config_fn))
    exit()
except KeyError:
    print("ERROR: config.json did not contain a discord token")
    exit()

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # disregard messages sent by the bot
    if message.author == client.user:
        return
    
    if message.content.startswith('!add points'):
        try:
            author = message.author.display_name
            points = s_parse_add_points(message.content)
        except Exception as e:
            print(e)
            await message.add_reaction("❌")
            return
        print(author)
        print(points)
        await message.add_reaction("✅")
    
client.run(discord_bot_token)
