import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import json

def json_read(path: str) -> dict:
    with open(f"{path}", "r") as f:
        data: dict = json.load(f)
    return data


def json_write(path: str, data: dict) -> None:
    with open(f"{path}", "w") as f:
        json.dump(data, f)

load_dotenv(".env")

client = commands.Bot(intents=constants.intents, command_prefix=constants.prefix)

@commands.Command
async def hello(ctx, times=1):
    msg = ""
    for _ in range(times):
        msg += "Hello "
    msg = msg.strip()
    await ctx.send(msg)

@commands.Command
async def showCrypto(ctx, crypto=""):
    if crypto == "":
        await ctx.send("Usage: $showCrypto [name of crypto]")
        return
    coins = json_read(".\crypto.json")
    if crypto not in coins:
        await ctx.send("Invalid crypro name.")
        return
    bank = coins[crypto]["Bank"]
    bank = [[value, key] for key, value in bank.items()]
    # reversing key value pairs to sort
    bank.sort(reverse=True)
    msg = ""
    for user in bank:
        msg += f"{user[1]}: {user[0]}\n"
    msg = msg.strip('\n')
    await ctx.send(msg)

@commands.Command
async def addCrypto(ctx, target="", val=0):
    if target == "":
        await ctx.send("Usage: $addCrypto: [target] [value]")
        return
    coins = json_read(".\crypto.json")
    userCoin = ""
    for name, coin in coins.items():
        if ctx.author.id == coin["Owner"]:
            userCoin = name
    if userCoin == "":
        await ctx.send("You do not own a crypto.")
        return
    if target in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][target] += val
    else:
        coins[userCoin]["Bank"][target] = val
    num = coins[userCoin]["Bank"][target]
    await ctx.send(f"{val} coins added to {target}.\nThey now have {num} coins.")
    json_write(".\crypto.json",coins)


client.add_command(hello)
client.add_command(showCrypto)
client.add_command(addCrypto)

client.run(os.getenv("TOKEN"))