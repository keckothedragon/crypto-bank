import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import fileHelper
import discordTypeConversion

load_dotenv(".env")

client = commands.Bot(intents=constants.INTENTS, command_prefix=constants.PREFIX)

@commands.Command
async def showCrypto(ctx, crypto=""):
    if crypto == "":
        await ctx.send(f"Usage: {constants.PREFIX}showCrypto [name of crypto]")
        return
    
    if crypto == "self":
        crypto = f"<@{ctx.author.id}>"

    if discordTypeConversion.pingtoid(crypto) is not None:
        targetID = discordTypeConversion.pingtoid(crypto)
        targetName = discordTypeConversion.idtoname(ctx, targetID)
        
        if ctx.guild.id in constants.bankExceptions:
            id = constants.bankExceptions[ctx.guild.id]
        else:
            id = ctx.guild.id
        coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
        
        backpack = {}
        for coin in coins:
            if str(targetID) in coins[coin]["Bank"]:
                val = coins[coin]["Bank"][str(targetID)]
                inverted = {value: key for key, value in coins[coin]["Bank"].items()}
                placement = sorted(list(inverted.keys()))[::-1].index(val) + 1
                backpack[coins[coin]["DisplayName"]] = [val, placement]
        
        if len(backpack) == 0:
            await ctx.send(f"{targetName} does not have any crypto.")
            return
        
        msg = f"{targetName} has the following crypto:\n"
        for key, value in backpack.items():
            msg += f"{key}: {value[0]} (#{value[1]})\n"
    else:
        crypto = crypto.lower()
        
        if ctx.guild.id in constants.bankExceptions:
            id = constants.bankExceptions[ctx.guild.id]
        else:
            id = ctx.guild.id
        coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
        
        if crypto not in coins:
            await ctx.send(f"Invalid crypto name. To see a list of all crypto, use {constants.PREFIX}listCrypto.")
            return
        
        bank = coins[crypto]["Bank"]
        bank = [[value, key] for key, value in bank.items()]
        # reversing key value pairs to sort
        bank.sort(reverse=True)
        
        msg = ""
        for user in bank:
            try:
                msg += f"{discordTypeConversion.idtoname(ctx, int(user[1]))}: {user[0]}\n"
            except:
                msg += f"(User not in server): {user[0]}\n"
        msg = msg.strip('\n')
        if not msg:
            msg = f"There is no data for {crypto}."
    
    await ctx.send(msg)

@commands.Command
async def addCrypto(ctx, target="", val=None, *reason: tuple):
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional]")
        return
    
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional] (target must be a ping)")
        return
    else:
        targetName = discordTypeConversion.idtoname(ctx, targetID)
    
    try:
        # making sure user didnt pass args in wrong order
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional] (value must be an integer)")
        return
    
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")

    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    if str(targetID) in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][str(targetID)] += val
    else:
        coins[userCoin]["Bank"][str(targetID)] = val

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    num = coins[userCoin]["Bank"][str(targetID)]
    msg = f"{val} coins added to {targetName}.\nThey now have {num} coins."
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
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto [target] [val] [reason: optional]")
        return
    
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto: [target] [value] [reason: optional] (target must be a ping)")
        return
    else:
        targetName = discordTypeConversion.idtoname(ctx, targetID)

    try:
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto [target] [val] [reason: optional] (val must be an integer)")
        return
    
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")

    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    coins[userCoin]["Bank"][str(targetID)] = val

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    num = coins[userCoin]["Bank"][str(targetID)]
    msg = f"Succesfully set {targetName}'s coins to {num}."
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
        await ctx.send(f"Usage: {constants.PREFIX}createCrypto [name]")
        return
    
    if discordTypeConversion.pingtoid(cryptoName) is not None:
        await ctx.send(f"Crypto name cannot be a ping.")

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            await ctx.send(f"You already own a crypto: {key}")
            return
    realName = cryptoName.lower()
    if realName in coins:
        await ctx.send("A crypto with this name already exists.")
        return
    
    coins[realName] = {"DisplayName": cryptoName, "Owner": ctx.author.id, "Bank": {}}

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    await ctx.send(f"{cryptoName} was succesfully created.")

@commands.Command
async def deleteCrypto(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    userOwn = False
    for coin in coins:
        if coins[coin]["Owner"] == ctx.author.id:
            userOwn = True
    if not userOwn:
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    confirmation: set = fileHelper.pickle_read(constants.DATAPATH + str(id) + "-confirmation.pickle")
    if ctx.author.id in confirmation:
        await ctx.send(f"You still have an unconfirmed command. Please run {constants.PREFIX}confirmDeletion to confirm or {constants.PREFIX}cancelDeletion to cancel.")
        return
    confirmation.add(ctx.author.id)

    fileHelper.pickle_write(constants.DATAPATH + str(id) + "-confirmation.pickle", confirmation)
    
    await ctx.send(f"This is a dangerous command. Please run {constants.PREFIX}confirmDeletion to confirm deletion.")

@commands.Command
async def confirmDeletion(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id

    confirmation: set = fileHelper.pickle_read(constants.DATAPATH + str(id) + "-confirmation.pickle")
    if ctx.author.id not in confirmation:
        await ctx.send(f"There is nothing awaiting confirmation.")
        return
    
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    for key, value in coins.items():
        if value["Owner"] == ctx.author.id:
            del coins[key]
            break

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    confirmation.remove(ctx.author.id)
    
    fileHelper.pickle_write(constants.DATAPATH + str(id) + "-confirmation.pickle", confirmation)

    await ctx.send(f"Successfully deleted \"{key}\".")

@commands.Command
async def cancelDeletion(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    confirmation = fileHelper.pickle_read(constants.DATAPATH + str(id) + "-confirmation.pickle")
    if ctx.author.id not in confirmation:
        await ctx.send("There is nothing awaiting confirmation.")
        return
    
    confirmation.remove(ctx.author.id)
    
    fileHelper.pickle_write(constants.DATAPATH + str(id) + "-confirmation.pickle", confirmation)
    
    await ctx.send(f"Cancelled deletion.")

@commands.Command
async def listCrypto(ctx):
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    msg = "\n".join([str(coins[coin]["DisplayName"]) for coin in coins])
    
    if not msg:
        msg = "No crypto to list."
    
    await ctx.send(msg)

@commands.Command
async def deleteUser(ctx, target=""):
    if target == "":
        await ctx.send(f"Usage: {constants.PREFIX}deleteUser [target]")
        return
    
    targetID = discordTypeConversion.pingtoid(target)
    if targetID is None:
        await ctx.send(f"Usage: {constants.PREFIX}deleteUser [target] (target must be a ping)")
        return
    else:
        targetName = discordTypeConversion.idtoname(ctx, targetID)
    
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]: 
            userCoin = key
    
    if userCoin == "":
        await ctx.send(f"You do not currently own a crypto. You can create one with {constants.PREFIX}createCrypto.")

    if str(targetID) not in coins[userCoin]["Bank"]:
        await ctx.send(f"{targetName} does not have any of your crypto.")
        return
    
    poppedData = coins[userCoin]["Bank"].pop(str(targetID))
    
    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)
    
    await ctx.send(f"Successfully removed {targetName} from your crypto.\n{targetName} had {poppedData} coins.")

@commands.Command
async def transferCrypto(ctx, arg1="", arg2="", amount=None, *reason: tuple):
    # exception handling fun
    try:
        amount = int(amount)
    except ValueError:
        await ctx.send(f"Usage: {constants.PREFIX}transferCrypto [userFrom] [userTo] [amount] [reason: optional]" +
                       "\nOR\n" + 
                       f"Usage: {constants.PREFIX}transferCrypto [cryptoName] [userTo] [amount] [reason: optional] (userFrom is you)" +
                       "\namount must be an integer.")
        return
    if arg1 == "" or arg2 == "" or amount is None:
        await ctx.send(f"Usage: {constants.PREFIX}transferCrypto [userFrom] [userTo] [amount] [reason: optional]" +
                       "\nOR\n" + 
                       f"Usage: {constants.PREFIX}transferCrypto [cryptoName] [userTo] [amount] [reason: optional] (userFrom is you)")
    if amount <= 0:
        await ctx.send("Amount must be greater than 0.")
        return
    
    if discordTypeConversion.pingtoid(arg1) is not None:
        await transferCryptoOwner(ctx, discordTypeConversion.pingtoid(arg1), discordTypeConversion.pingtoid(arg2), amount, reason)
    else:
        await transferCryptoUser(ctx, arg1, discordTypeConversion.pingtoid(arg2), amount, reason)

async def transferCryptoUser(ctx, cryptoName: str, userToID: str, amount: int, reason: tuple):
    userFromID = ctx.author.id

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id

    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")

    if cryptoName.lower() not in coins:
        await ctx.send(f"{cryptoName} does not exist.")
        return
    
    cryptoName = cryptoName.lower()
    displayName = coins[cryptoName]["DisplayName"]    
    
    if str(userFromID) not in coins[cryptoName]["Bank"]:
        await ctx.send(f"You do not have any {displayName}.")
        return
    if coins[cryptoName]["Bank"][str(userFromID)] < amount:
        await ctx.send(f"You do not have enough of {displayName}.")
        return
    
    if str(userToID) not in coins[cryptoName]["Bank"]:
        coins[cryptoName]["Bank"][str(userToID)] = 0

    coins[cryptoName]["Bank"][str(userFromID)] -= amount
    coins[cryptoName]["Bank"][str(userToID)] += amount

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    userToName = discordTypeConversion.idtoname(ctx, userToID)
    msg = f"Successfully transferred {amount} {displayName} to {userToName}.\n\
{userToName} now has {coins[cryptoName]['Bank'][str(userToID)]}.\n\
You now have {coins[cryptoName]['Bank'][str(userFromID)]}.\n"

    if reason != ():
        reason = list(reason)
        for i in range(len(reason)):
            reason[i] = "".join(reason[i])
        reason = " ".join(reason)
        msg += f"\nReason: {reason}"

    await ctx.send(msg)

async def transferCryptoOwner(ctx, userFromID: str, userToID: str, amount: int, reason: tuple):
    userFromName = discordTypeConversion.idtoname(ctx, userFromID)
    userToName = discordTypeConversion.idtoname(ctx, userToID)

    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    if str(userFromID) not in coins[userCoin]["Bank"]:
        await ctx.send(f"{userFromName} does not have any of your crypto.")
        return
    if str(userToID) not in coins[userCoin]["Bank"]:
        coins[userCoin]["Bank"][str(userToID)] = 0
    
    if coins[userCoin]["Bank"][str(userFromID)] < amount:
        userFromAmt = coins[userCoin]["Bank"][str(userFromID)]
        await ctx.send(f"{userFromName} only has {userFromAmt} coins. Please try again with a lower amount.")
        return
    
    coins[userCoin]["Bank"][str(userFromID)] -= amount
    coins[userCoin]["Bank"][str(userToID)] += amount

    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)

    msg = f"Successfully transferred {amount} coins from {userFromName} to {userToName}.\n\
{userFromName} now has {coins[userCoin]['Bank'][str(userFromID)]} coins.\n\
{userToName} now has {coins[userCoin]['Bank'][str(userToID)]} coins."
    if reason != ():
        reason = list(reason)
        for i in range(len(reason)):
            reason[i] = "".join(reason[i])
        reason = " ".join(reason)
        msg += f"\nReason: {reason}"
    await ctx.send(msg)
    
@commands.Command
async def renameCrypto(ctx, newName=""):
    if newName == "":
        await ctx.send(f"Usage: {constants.PREFIX}renameCrypto [newName]")
        return
    if ctx.guild.id in constants.bankExceptions:
        id = constants.bankExceptions[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fileHelper.json_read(constants.DATAPATH + str(id) + "-crypto.json")
    userCoin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            userCoin = key
    if userCoin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    oldData = coins.pop(userCoin)
    oldData["DisplayName"] = newName
    coins[newName.lower()] = oldData
    fileHelper.json_write(constants.DATAPATH + str(id) + "-crypto.json", coins)
    await ctx.send(f"Successfully renamed {userCoin} to {newName}.")

@commands.Command
async def cryptoHelp(ctx, command=""):
    if command.lower() in constants.HELPINDICES:
        await ctx.send(constants.HELP[constants.HELPINDICES[command.lower()]])
    else:
        await ctx.send(constants.HELPMSG)

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
client.add_command(renameCrypto)
client.add_command(cryptoHelp)

client.run(os.getenv("TOKEN"))