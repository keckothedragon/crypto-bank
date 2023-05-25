import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import json
import pickle # using pickle to store set instead of dict

def json_read(path: str) -> dict:
    with open(f"{path}", "r") as f:
        data: dict = json.load(f)
    return data


def json_write(path: str, data: dict) -> None:
    with open(f"{path}", "w") as f:
        json.dump(data, f)

def pickle_read(path: str) -> set:
    with open(f"{path}", "rb") as f:
        data: set = pickle.load(f)
    return data

def pickle_write(path: str, data: set) -> None:
    with open(f"{path}", "wb") as f:
        pickle.dump(data, f)

load_dotenv(".env")

client = commands.Bot(intents=constants.intents, command_prefix=constants.prefix)

@commands.Command
async def showCrypto(ctx, crypto=""):
    if crypto == "":
        await ctx.send(f"Usage: {constants.prefix}showCrypto [name of crypto]")
        return
    coins = json_read(constants.jsonFilePath)
    if crypto not in coins:
        await ctx.send("Invalid crypto name.")
        return
    bank = coins[crypto]["Bank"]
    bank = [[value, key] for key, value in bank.items()]
    # reversing key value pairs to sort
    bank.sort(reverse=True)
    msg = ""
    for user in bank:
        msg += f"{user[1]}: {user[0]}\n"
    msg = msg.strip('\n')
    if not msg:
        msg = f"There is no data for {crypto}."
    await ctx.send(msg)

@commands.Command
async def addCrypto(ctx, target="", val=0):
    if target == "":
        await ctx.send(f"Usage: {constants.prefix}addCrypto: [target] [value]")
        return
    coins = json_read(constants.jsonFilePath)
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send("You do not own a crypto.")
        return
    if target in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][target] += val
    else:
        coins[userCoin]["Bank"][target] = val

    json_write(constants.jsonFilePath, coins)
    num = coins[userCoin]["Bank"][target]
    await ctx.send(f"{val} coins added to {target}.\nThey now have {num} coins.")

@commands.Command
async def createCrypto(ctx, cryptoName=""):
    if cryptoName == "":
        await ctx.send(f"Usage: {constants.prefix}createCrypto [name]")
        return
    coins = json_read(constants.jsonFilePath)
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            await ctx.send(f"You already own a crypto: {key}")
            return
    
    coins[cryptoName] = {"Owner": ctx.author.id, "Bank": {}}

    json_write(constants.jsonFilePath, coins)

    await ctx.send(f"{cryptoName} was succesfully created.")

@commands.Command
async def deleteCrypto(ctx):
    confirmation: set = pickle_read(constants.pickleFilePath)
    if ctx.author.id in confirmation:
        await ctx.send(f"You still have an unconfirmed command. Please run {constants.prefix}confirmDeletion to confirm or {constants.prefix}cancelDeletion to cancel.")
        return
    confirmation.add(ctx.author.id)
    pickle_write(constants.pickleFilePath, confirmation)
    await ctx.send(f"This is a dangerous command. Please run {constants.prefix}confirmDeletion to confirm deletion.")

@commands.Command
async def confirmDeletion(ctx):
    """a"""
    confirmation: set = pickle_read(constants.pickleFilePath)
    if ctx.author.id not in confirmation:
        await ctx.send(f"There is nothing awaiting confirmation.")
        return
    coins = json_read(constants.jsonFilePath)
    for key, value in coins.items():
        if value["Owner"] == ctx.author.id:
            del coins[key]
            break

    json_write(constants.jsonFilePath, coins)

    confirmation.remove(ctx.author.id)
    pickle_write(constants.pickleFilePath, confirmation)

    await ctx.send(f"Successfully deleted \"{key}\".")

@commands.Command
async def cancelDeletion(ctx):
    confirmation = pickle_read(constants.pickleFilePath)
    if ctx.author.id not in confirmation:
        await ctx.send("There is nothing awaiting confirmation.")
        return
    confirmation.remove(ctx.author.id)
    pickle_write(constants.pickleFilePath, confirmation)
    await ctx.send(f"Cancelled deletion.")
    

@commands.Command
async def cryptoHelp(ctx):
    await ctx.send(constants.helpMsg)

client.add_command(showCrypto)
client.add_command(addCrypto)
client.add_command(createCrypto)
client.add_command(deleteCrypto)
client.add_command(confirmDeletion)
client.add_command(cancelDeletion)
# client.help_command.no_category = ""
client.add_command(cryptoHelp)

client.run(os.getenv("TOKEN"))