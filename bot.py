import discord
import random
import os
import json
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents(messages=True, guilds= True, reactions = True, members=True, presences= True)

#get prefixes
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


#initialise prefix, intents
client = commands.Bot(command_prefix = get_prefix, intents = intents)

#initialise statuses, feel free to add more statuses
status = cycle(["Ivan's homework", "Ivan's assignments"])

#verify bot onwer
def is_ivan(ctx):
    return ctx.author.id == 348445296620994560


#LOADING AND UNLOADING WITH COGS
@client.command()
@commands.check(is_ivan)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
@commands.check(is_ivan)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
@commands.check(is_ivan)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} reloaded successfully")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename[:-3]} loaded successfully")

#EVENTS
@client.event
async def on_ready():
    #set bot status
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game("Ivan's assignments"))
    change_status.start()
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print("{} has joined the server.".format(member))

@client.event
async def on_member_remove(member):
    print("{} has left the server.".format(member))

#this 2 events manipulate the prefixes in the json file
@client.event
#when bot joins server
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    #set default prefix to "!"
    prefixes[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent = 4)

@client.event
#when bot leaves the server, remove the prefix from prefixes.json
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent = 4)

#access prefix
@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    #set default prefix to "!"
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix changed to '{prefix}'")

#COMMANDS
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")

@client.command(aliases=["ivan"])
@commands.check(is_ivan)
async def greet_ivan(ctx):
    await ctx.send("Greetings, my Lord.")

#TASKS
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#HANDLING ALL ERRORs
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Invalid command.")
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("Sorry you don't have required permissions")
    elif isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("Member not in server")
    elif isinstance(error, commands.errors.RoleNotFound):
        await ctx.send("Role is not found, please create role beforehand")
    else:
        await ctx.send("Error, pls contact ivan.")
        raise error
        
#Your bot token
client.run("NTIyMjg2ODU1NzgyMjY4OTY5.XBCfig.SewQtYg2EPLOwusD_2ke2bEwEzk")
