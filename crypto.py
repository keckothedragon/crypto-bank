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
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
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
async def addCrypto(ctx, target="", val=None):
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.prefix}addCrypto: [target] [value]")
        return
    try:
        # making sure user didnt pass args in wrong order
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.prefix}addCrypto: [target] [value]")
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
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

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    num = coins[userCoin]["Bank"][target]
    await ctx.send(f"{val} coins added to {target}.\nThey now have {num} coins.")

@commands.Command
async def setCrypto(ctx, target="", val=None):
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.prefix}setCrypto [target] [val]")
    try:
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.prefix}setCrypto [target] [val]")
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.prefix}createCrypto.")
        return
    coins[userCoin]["Bank"][target] = val

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    num = coins[userCoin]["Bank"][target]
    await ctx.send(f"Succesfully set {target}'s coins to {num}.")

@commands.Command
async def createCrypto(ctx, cryptoName=""):
    if cryptoName == "":
        await ctx.send(f"Usage: {constants.prefix}createCrypto [name]")
        return
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            await ctx.send(f"You already own a crypto: {key}")
            return
    if cryptoName in coins:
        await ctx.send("A crypto with this name already exists.")
        return
    
    coins[cryptoName] = {"Owner": ctx.author.id, "Bank": {}}

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)

    await ctx.send(f"{cryptoName} was succesfully created.")

@commands.Command
async def deleteCrypto(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    userOwn = False
    for coin in coins:
        if coins[coin]["Owner"] == ctx.author.id:
            userOwn = True
    if not userOwn:
        await ctx.send(f"You do not own a crypto. You can create one with {constants.prefix}createCrypto.")
        return

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    confirmation: set = fileHelper.pickle_read(constants.dataPath + str(id) + "-confirmation.pickle")
    if ctx.author.id in confirmation:
        await ctx.send(f"You still have an unconfirmed command. Please run {constants.prefix}confirmDeletion to confirm or {constants.prefix}cancelDeletion to cancel.")
        return
    confirmation.add(ctx.author.id)
    fileHelper.pickle_write(constants.dataPath + str(id) + "-confirmation.pickle", confirmation)
    await ctx.send(f"This is a dangerous command. Please run {constants.prefix}confirmDeletion to confirm deletion.")

@commands.Command
async def confirmDeletion(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    confirmation: set = fileHelper.pickle_read(constants.dataPath + str(id) + "-confirmation.pickle")
    if ctx.author.id not in confirmation:
        await ctx.send(f"There is nothing awaiting confirmation.")
        return
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    for key, value in coins.items():
        if value["Owner"] == ctx.author.id:
            del coins[key]
            break

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)

    confirmation.remove(ctx.author.id)
    fileHelper.pickle_write(constants.dataPath + str(id) + "-confirmation.pickle", confirmation)

    await ctx.send(f"Successfully deleted \"{key}\".")

@commands.Command
async def cancelDeletion(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    confirmation = fileHelper.pickle_read(constants.dataPath + str(id) + "-confirmation.pickle")
    if ctx.author.id not in confirmation:
        await ctx.send("There is nothing awaiting confirmation.")
        return
    confirmation.remove(ctx.author.id)
    fileHelper.pickle_write(constants.dataPath + str(id) + "-confirmation.pickle", confirmation)
    await ctx.send(f"Cancelled deletion.")

@commands.Command
async def listCrypto(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    msg = "\n".join([str(coin) for coin in coins])
    if not msg:
        msg = "No crypto to list."
    await ctx.send(msg)

@commands.Command
async def deleteUser(ctx, target=""):
    if target == "":
        await ctx.send(f"Usage: {constants.prefix}deleteUser [target]")
        return
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]: 
            userCoin = key
    
    if userCoin == "":
        await ctx.send(f"You do not currently own a crypto. You can create one with {constants.prefix}createCrypto.")

    if target not in coins[userCoin]["Bank"]:
        await ctx.send(f"{target} does not have any of your crypto.")
        return
    
    poppedData = coins[userCoin]["Bank"].pop(target)
    fileHelper.json_write(constants.dataPath + id + "-crypto.json", coins)
    await ctx.send(f"Successfully removed {target} from your crypto.\n{target} had {poppedData} coins.")

@commands.Command
async def transferCrypto(ctx, userFrom="", userTo="", amount=None):
    if userFrom == "" or userTo == "" or amount is None:
        await ctx.send(f"Usage: {constants.prefix}transferCrypto [userFrom] [userTo] [amount]")
        return

    try:
        amount = int(amount)
    except ValueError:
        await ctx.send(f"Usage: {constants.prefix}transferCrypto [userFrom] [userTo] [amount]")
        return

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.prefix}createCrypto.")
        return
    if userFrom not in coins[userCoin]["Bank"]:
        await ctx.send(f"{userFrom} does not have any of your crypto.")
        return
    if userTo not in coins[userCoin]["Bank"]:
        await ctx.send(f"{userTo} does not have any of your crypto. To confirm transfer, use the command \"{constants.prefix}setCrypto {userTo} 0\" first.")
        return
    if coins[userCoin]["Bank"][userFrom] < amount:
        userFromAmt = coins[userCoin]["Bank"][userFrom]
        await ctx.send(f"{userFrom} only has {userFromAmt} coins. Please try again with a lower amount.")
        return
    coins[userCoin]["Bank"][userFrom] -= amount
    coins[userCoin]["Bank"][userTo] += amount

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    await ctx.send(f"Successfully transferred {amount} coins from {userFrom} to {userTo}.\n" +
                   f"{userFrom} now has {coins[userCoin]['Bank'][userFrom]} coins.\n" +
                   f"{userTo} now has {coins[userCoin]['Bank'][userTo]} coins.")
    
@commands.Command
async def cryptoHelp(ctx):
    await ctx.send(constants.helpMsg)

client.add_command(showCrypto)
client.add_command(addCrypto)
client.add_command(setCrypto)
client.add_command(createCrypto)
client.add_command(deleteCrypto)
client.add_command(confirmDeletion)
client.add_command(cancelDeletion)
client.add_command(listCrypto)
client.add_command(deleteUser)
client.add_command(transferCrypto)
client.add_command(cryptoHelp)

client.run(os.getenv("TOKEN"))