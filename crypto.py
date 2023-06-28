import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import fileHelper
import discordTypeConversion

load_dotenv(".env")

client = commands.Bot(intents=constants.intents, command_prefix=constants.prefix)

@commands.Command
async def showCrypto(ctx, crypto=""):
    if crypto == "":
        await ctx.send(f"Usage: {constants.prefix}showCrypto [name of crypto]")
        return
    if discordTypeConversion.pingtoid(crypto) is not None:
        if crypto == "":
            await ctx.send(f"Usage: {constants.prefix}showCryptoUser [target]")
            return
        targetID = discordTypeConversion.pingtoid(crypto)
        if targetID is None:
            await ctx.send(f"Usage: {constants.prefix}showCryptoUser [target] (target must be a ping)")
            return
        if ctx.guild.id in constants.bankExceptions:
            id = constants.bankExceptions[ctx.guild.id]
        else:
            id = ctx.guild.id
        coins = fileHelper.json_read(constants.dataPath + str(id) + "-crypto.json")
        backpack = {}
        for coin in coins:
            if str(targetID) in coins[coin]["Bank"]:
                backpack[coin] = coins[coin]["Bank"][str(targetID)]
        if len(backpack) == 0:
            await ctx.send(f"{discordTypeConversion.idtoname(ctx, targetID)} does not have any crypto.")
            return
        msg = f"{discordTypeConversion.idtoname(ctx, targetID)} has the following crypto:\n"
        for key, value in backpack.items():
            msg += f"{key}: {value}\n"
        await ctx.send(msg)
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
        msg += f"{discordTypeConversion.idtoname(ctx, int(user[1]))}: {user[0]}\n"
    msg = msg.strip('\n')
    if not msg:
        msg = f"There is no data for {crypto}."
    await ctx.send(msg)

@commands.Command
async def addCrypto(ctx, target="", val=None, *reason: tuple):
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.prefix}addCrypto: [target] [value]")
        return
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.prefix}addCrypto: [target] [value] (target must be a ping)")
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
    if str(targetID) in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][str(targetID)] += val
    else:
        coins[userCoin]["Bank"][str(targetID)] = val

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    num = coins[userCoin]["Bank"][str(targetID)]
    msg = f"{val} coins added to {discordTypeConversion.idtoname(ctx, targetID)}.\nThey now have {num} coins."
    if reason != ():
        reason = list(reason)
        for i in range(len(reason)):
            reason[i] = "".join(reason[i])
        reason = " ".join(reason)
        msg += f"\nReason: {reason}"
    await ctx.send(msg)

@commands.Command
async def setCrypto(ctx, target="", val=None, *reason: tuple):
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.prefix}setCrypto [target] [val]")
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.prefix}setCrypto: [target] [value] (target must be a ping)")
        return
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
    coins[userCoin]["Bank"][str(targetID)] = val

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    num = coins[userCoin]["Bank"][str(targetID)]

    msg = f"Succesfully set {discordTypeConversion.idtoname(ctx, targetID)}'s coins to {num}."
    if reason != ():
        reason = list(reason)
        for i in range(len(reason)):
            reason[i] = "".join(reason[i])
        reason = " ".join(reason)
        msg += f"\nReason: {reason}"
    await ctx.send(msg)

@commands.Command
async def createCrypto(ctx, cryptoName=""):
    if cryptoName == "":
        await ctx.send(f"Usage: {constants.prefix}createCrypto [name]")
        return
    if discordTypeConversion.pingtoid(cryptoName) is not None:
        await ctx.send(f"Crypto name cannot be a ping.")
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
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.prefix}deleteUser [target] (target must be a ping)")
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

    if str(targetID) not in coins[userCoin]["Bank"]:
        await ctx.send(f"{discordTypeConversion.idtoname(ctx, targetID)} does not have any of your crypto.")
        return
    
    poppedData = coins[userCoin]["Bank"].pop(str(targetID))
    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    await ctx.send(f"Successfully removed {discordTypeConversion.idtoname(ctx, targetID)} from your crypto.\n{target} had {poppedData} coins.")

@commands.Command
async def transferCrypto(ctx, userFrom="", userTo="", amount=None):
    if userFrom == "" or userTo == "" or amount is None:
        await ctx.send(f"Usage: {constants.prefix}transferCrypto [userFrom] [userTo] [amount]")
        return
    userFromID = discordTypeConversion.pingtoid(userFrom)
    userToID = discordTypeConversion.pingtoid(userTo)
    if userFromID is None or userToID is None:
        await ctx.send(f"Usage: {constants.prefix}transferCrypto [userFrom] [userTo] [amount] (userFrom and userTo must be pings)")
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
    if str(userFromID) not in coins[userCoin]["Bank"]:
        await ctx.send(f"{discordTypeConversion.idtoname(ctx, userFromID)} does not have any of your crypto.")
        return
    if str(userToID) not in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][str(userToID)] = 0
    if coins[userCoin]["Bank"][str(userFromID)] < amount:
        userFromAmt = coins[userCoin]["Bank"][str(userFromID)]
        await ctx.send(f"{discordTypeConversion.idtoname(ctx, userFromID)} only has {userFromAmt} coins. Please try again with a lower amount.")
        return
    coins[userCoin]["Bank"][str(userFromID)] -= amount
    coins[userCoin]["Bank"][str(userToID)] += amount

    fileHelper.json_write(constants.dataPath + str(id) + "-crypto.json", coins)
    userFromName = discordTypeConversion.idtoname(ctx, userFromID)
    userToName = discordTypeConversion.idtoname(ctx, userToID)
    # got tired of writing it out for this send
    await ctx.send(f"Successfully transferred {amount} coins from {userFromName} to {userTo}.\n" +
                   f"{userFromName} now has {coins[userCoin]['Bank'][str(userFromID)]} coins.\n" +
                   f"{userToName} now has {coins[userCoin]['Bank'][str(userToID)]} coins.")
    
@commands.Command
async def cryptoHelp(ctx):
    await ctx.send(constants.helpMsg)

@commands.Command
async def getName(ctx, target=""):
    if "<@" not in target or ">" not in target:
        await ctx.send(f"Usage: {constants.prefix}getName [target] (target must be a ping)")
        return
    try:
        id = target.replace("<@", "").replace(">", "")
        id = int(id)
    except ValueError:
        await ctx.send(f"Usage: {constants.prefix}getName [target] (target must be a ping)")
        return
    await ctx.send(discordTypeConversion.idtoname(ctx, id))

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
client.add_command(getName)

client.run(os.getenv("TOKEN"))