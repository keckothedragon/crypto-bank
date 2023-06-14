import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import fileHelper

load_dotenv(".env")

client = commands.Bot(intents=constants.intents, command_prefix=constants.prefix)

@commands.Command
async def showCrypto(ctx, crypto=""):
    if crypto == "":
        await ctx.send(f"Usage: {constants.prefix}showCrypto [name of crypto]")
        return
    coins = fileHelper.json_read(constants.jsonFilePath)
    if crypto not in coins:
        await ctx.send(f"Invalid crypto name. To see a list of all crypto, use {constants.prefix}listCrypto.")
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
    coins = fileHelper.json_read(constants.jsonFilePath)
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.prefix}createCrypto.")
        return
    if target in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][target] += val
    else:
        coins[userCoin]["Bank"][target] = val

    fileHelper.json_write(constants.jsonFilePath, coins)
    num = coins[userCoin]["Bank"][target]
    await ctx.send(f"{val} coins added to {target}.\nThey now have {num} coins.")

@commands.Command
async def createCrypto(ctx, cryptoName=""):
    if cryptoName == "":
        await ctx.send(f"Usage: {constants.prefix}createCrypto [name]")
        return
    coins = fileHelper.json_read(constants.jsonFilePath)
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            await ctx.send(f"You already own a crypto: {key}")
            return
    if cryptoName in coins:
        await ctx.send("A crypto with this name already exists.")
        return
    
    coins[cryptoName] = {"Owner": ctx.author.id, "Bank": {}}

    fileHelper.json_write(constants.jsonFilePath, coins)

    await ctx.send(f"{cryptoName} was succesfully created.")

@commands.Command
async def deleteCrypto(ctx):
    coins = fileHelper.json_read(constants.jsonFilePath)
    userOwn = False
    for coin in coins:
        if coins[coin]["Owner"] == ctx.author.id:
            userOwn = True
    if not userOwn:
        await ctx.send(f"You do not own a crypto. You can create one with {constants.prefix}createCrypto.")
        return

    confirmation: set = fileHelper.pickle_read(constants.pickleFilePath)
    if ctx.author.id in confirmation:
        await ctx.send(f"You still have an unconfirmed command. Please run {constants.prefix}confirmDeletion to confirm or {constants.prefix}cancelDeletion to cancel.")
        return
    confirmation.add(ctx.author.id)
    fileHelper.pickle_write(constants.pickleFilePath, confirmation)
    await ctx.send(f"This is a dangerous command. Please run {constants.prefix}confirmDeletion to confirm deletion.")

@commands.Command
async def confirmDeletion(ctx):
    confirmation: set = fileHelper.pickle_read(constants.pickleFilePath)
    if ctx.author.id not in confirmation:
        await ctx.send(f"There is nothing awaiting confirmation.")
        return
    coins = fileHelper.json_read(constants.jsonFilePath)
    for key, value in coins.items():
        if value["Owner"] == ctx.author.id:
            del coins[key]
            break

    fileHelper.json_write(constants.jsonFilePath, coins)

    confirmation.remove(ctx.author.id)
    fileHelper.pickle_write(constants.pickleFilePath, confirmation)

    await ctx.send(f"Successfully deleted \"{key}\".")

@commands.Command
async def cancelDeletion(ctx):
    confirmation = fileHelper.pickle_read(constants.pickleFilePath)
    if ctx.author.id not in confirmation:
        await ctx.send("There is nothing awaiting confirmation.")
        return
    confirmation.remove(ctx.author.id)
    fileHelper.pickle_write(constants.pickleFilePath, confirmation)
    await ctx.send(f"Cancelled deletion.")

@commands.Command
async def listCrypto(ctx):
    coins = fileHelper.json_read(constants.jsonFilePath)
    msg = "\n".join([str(coin) for coin in coins])
    if not msg:
        msg = "No crypto to list."
    await ctx.send(msg)

@commands.Command
async def cryptoHelp(ctx):
    await ctx.send(constants.helpMsg)

client.add_command(showCrypto)
client.add_command(addCrypto)
client.add_command(createCrypto)
client.add_command(deleteCrypto)
client.add_command(confirmDeletion)
client.add_command(cancelDeletion)
client.add_command(cryptoHelp)
client.add_command(listCrypto)

client.run(os.getenv("TOKEN"))