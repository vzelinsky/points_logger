import discord
import json
from discord_command_parser import *
from gsheets_updater import *
from gspread import *

config_fn = "config.json"
try:
    config = json.load(open(config_fn, "r"))
    discord_bot_token = config["discord_bot_token"]
except IOError:
    print("ERROR: {0} could not be opened.".format(config_fn))
    exit()
except KeyError:
    print("ERROR: {0} did not contain a discord token".format(config_fn))
    exit()

client = discord.Client()
sh = get_spreadsheet("Points Logger")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # disregard messages sent by the bot
    if message.author == client.user:
        return

    wk = get_worksheet(sh, get_current_month_name())
    
    if message.content.startswith('!add points'):
        try:
            author = message.author.name
            points = parse_add_points(message.content)
        except Exception as e:
            print(e)
            await message.add_reaction("❌")
            return
        print("Gave {0} points to {1}.".format(points, author))
        await message.add_reaction("✅")
    elif message.content.startswith("!add me"):
        try:
            author = message.author.name
            parse_add_me(message.content)
            add_user(wk, author)
        except Exception as e:
            print(e)
            await message.add_reaction("❌")
            return
        print("{0} added successfully.".format(author))
        await message.add_reaction("✅")

    
client.run(discord_bot_token)
