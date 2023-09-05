import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import file_helper as fh
import type_conversion as tc
import time

load_dotenv(".env")

client = commands.Bot(intents=constants.INTENTS, command_prefix=constants.PREFIX)

client.remove_command("help") # it freaks out if i put it at the bottom so its going up here

@client.command()
async def showCrypto(ctx, crypto=""):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if crypto == "":
        await ctx.send(f"Usage: {constants.PREFIX}showCrypto [name of crypto]")
        return
    
    if crypto == "self":
        crypto = f"<@{ctx.author.id}>"

    if tc.pingtoid(crypto) is not None:
        target_id = tc.pingtoid(crypto)
        target_name = tc.idtoname(ctx, target_id)
        
        if ctx.guild.id in constants.BANK_EXCEPTIONS:
            id = constants.BANK_EXCEPTIONS[ctx.guild.id]
        else:
            id = ctx.guild.id
        coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
        
        backpack = {}
        for coin in coins:
            if str(target_id) in coins[coin]["Bank"]:
                coins[coin]["Bank"][str(target_id)]["Name"] = target_name # updating name in database

                val = coins[coin]["Bank"][str(target_id)]["Amt"]

                placement = tc.get_placement(ctx, target_id, coin)

                backpack[coins[coin]["DisplayName"]] = [val, placement]
        
        if len(backpack) == 0:
            await ctx.send(f"{target_name} does not have any crypto.")
            return

        msg = f"{target_name} has the following crypto:\n"
        for key, value in backpack.items():
            msg += f"{key}: {value[0]} (Rank #{value[1]})\n"
        
    else:
        crypto = crypto.lower()
        
        if ctx.guild.id in constants.BANK_EXCEPTIONS:
            id = constants.BANK_EXCEPTIONS[ctx.guild.id]
        else:
            id = ctx.guild.id
        coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
        
        if crypto not in coins:
            await ctx.send(f"Invalid crypto name. To see a list of all crypto, use {constants.PREFIX}listCrypto.")
            return
        
        bank = coins[crypto]["Bank"]
        bank = [[value["Amt"], key, value["Name"]] for key, value in bank.items()]
        # reversing key value pairs to sort
        bank.sort(reverse=True)
        
        msg = ""
        for user in bank:
            try:
                msg += f"{tc.idtoname(ctx, int(user[1]))}: {user[0]}\n"
                coins[crypto]["Bank"][user[1]]["Name"] = tc.idtoname(ctx, int(user[1])) # updating name in database
            except:
                msg += f"{user[2]}: {user[0]}\n"
        msg = msg.strip('\n')
        if not msg:
            msg = f"There is no data for {crypto}."
    
    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)
    
    await ctx.send(msg)

@client.command()
async def addCrypto(ctx, target="", val=None, *reason: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional]")
        return
    
    target_id = tc.pingtoid(target)
    if target_id is None:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional] (target must be a ping)")
        return
    else:
        target_name = tc.idtoname(ctx, target_id)
    
    try:
        # making sure user didnt pass args in wrong order
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.PREFIX}addCrypto: [target] [value] [reason: optional] (value must be an integer)")
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    user_coin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            user_coin = key
    if user_coin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    if str(target_id) in coins[user_coin]["Bank"]:
        coins[user_coin]["Bank"][str(target_id)]["Amt"] += val
    else:
        coins[user_coin]["Bank"][str(target_id)] = {"Amt": val, "Name": target_name}

    coins[user_coin]["Bank"][str(target_id)]["Name"] = target_name # updating name in database

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    num = coins[user_coin]["Bank"][str(target_id)]["Amt"]
    
    placement = tc.get_placement(ctx, target_id, user_coin)

    msg = f"{val} coins added to {target_name}.\nThey now have {num} coins. (Rank #{placement} in {coins[user_coin]['DisplayName']})"

    show = False

    if reason != ():
        reason = list(reason)

        for i in range(len(reason)):
            reason[i] = "".join(reason[i])

        if reason[-1] in ["-s", "--show"]:
            reason.pop(-1)
            show = True

        if reason != []:
            reason = " ".join(reason)
            msg += f"\nReason: {reason}"

    await ctx.send(msg)

    if show:
        await ctx.send("New standings:\n")
        await showCrypto(ctx, user_coin)

@client.command()
async def setCrypto(ctx, target="", val=None, *reason: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if target == "" or val is None:
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto [target] [value] [reason: optional]")
        return
    
    target_id = tc.pingtoid(target)
    if target_id is None:
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto: [target] [value] [reason: optional] (target must be a ping)")
        return
    else:
        target_name = tc.idtoname(ctx, target_id)

    try:
        val = int(val)
    except ValueError:
        await ctx.send(f"Usage: {constants.PREFIX}setCrypto [target] [val] [reason: optional] (val must be an integer)")
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    user_coin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            user_coin = key
    if user_coin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    if str(target_id) not in coins[user_coin]["Bank"]:
        coins[user_coin]["Bank"][str(target_id)] = {"Amt": val, "Name": target_name}
    else:
        coins[user_coin]["Bank"][str(target_id)]["Amt"] = val
        coins[user_coin]["Bank"][str(target_id)]["Name"] = target_name # updating name in database

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    num = coins[user_coin]["Bank"][str(target_id)]["Amt"]

    placement = tc.get_placement(ctx, target_id, user_coin)
    
    msg = f"Succesfully set {target_name}'s coins to {num}. (Rank #{placement} in {coins[user_coin]['DisplayName']})"

    show = False

    if reason != ():
        reason = list(reason)

        for i in range(len(reason)):
            reason[i] = "".join(reason[i])

        if reason[-1] in ["-s", "--show"]:
            reason.pop(-1)
            show = True

        if reason != []:
            reason = " ".join(reason)
            msg += f"\nReason: {reason}"

    await ctx.send(msg)
    
    if show:
        await ctx.send("New standings:\n")
        await showCrypto(ctx, user_coin)

@client.command()
async def createCrypto(ctx, crypto_name=""):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if crypto_name == "":
        await ctx.send(f"Usage: {constants.PREFIX}createCrypto [name]")
        return
    
    if tc.pingtoid(crypto_name) is not None:
        await ctx.send(f"Crypto name cannot be a ping.")

    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
    
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            await ctx.send(f"You already own a crypto: {key}")
            return
    real_name = crypto_name.lower()
    if real_name in coins:
        await ctx.send("A crypto with this name already exists.")
        return
    
    coins[real_name] = {"DisplayName": crypto_name, "Owner": ctx.author.id, "Bank": {}}

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    deleted = fh.json_read(constants.DATA_PATH + str(id) + "-deleted.json")
    if str(ctx.author.id) in deleted:
        del deleted[str(ctx.author.id)]
    fh.json_write(constants.DATA_PATH + str(id) + "-deleted.json", deleted)

    await ctx.send(f"{crypto_name} was succesfully created.")

@client.command()
async def deleteCrypto(ctx):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
    
    user_own = False
    for coin in coins:
        if coins[coin]["Owner"] == ctx.author.id:
            user_own = True
    if not user_own:
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    for key, value in coins.items():
        if value["Owner"] == ctx.author.id:
            popped_data = coins.pop(key)
            break

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    deleted = fh.json_read(constants.DATA_PATH + str(id) + "-deleted.json")

    deleted[str(ctx.author.id)] = {"name": key, "data": popped_data}

    fh.json_write(constants.DATA_PATH + str(id) + "-deleted.json", deleted)

    name = deleted[str(ctx.author.id)]["data"]["DisplayName"]

    await ctx.send(f"Successfully deleted \"{name}\".\nTo restore {name}, use {constants.PREFIX}restoreCrypto.")

@client.command()
async def restoreCrypto(ctx):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    deleted = fh.json_read(constants.DATA_PATH + str(id) + "-deleted.json")

    user_id = str(ctx.author.id)

    if user_id not in deleted:
        await ctx.send("No crypto to restore.")
        return
    
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    key = deleted[user_id]["name"]
    data = deleted[user_id]["data"]
    coins[key] = data

    del deleted[user_id]

    fh.json_write(constants.DATA_PATH + str(id) + "-deleted.json", deleted)

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    name = data["DisplayName"]

    await ctx.send(f"Successfully restored \"{name}\".")

@client.command()
async def listCrypto(ctx, *args: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if len(args) > 0:
        if constants.DO_FUNNY_MSG:
            misuse_count = tc.increment_misuses(ctx, ctx.author.id)
            if misuse_count % constants.FUNNY_MSG_TOLERANCE == 0:
                await ctx.reply(constants.FUNNY_MSG.format(misuse_count))
                if ctx.guild.id in constants.FUNNY_MSG_DAD_BOT:
                    time.sleep(0.1)
                    await ctx.send("ONG DAD BOT")
                return
                    

        await ctx.send(f"Usage: {constants.PREFIX}listCrypto\nTo show a specific crypto, use {constants.PREFIX}showCrypto [crypto]")
        return
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    try:
        coins = tc.rearrange(coins)
        fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)
    except:
        # idk why there would be an error but just in case
        coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    msg = "\n".join([str(coins[coin]["DisplayName"]) for coin in coins])
    
    if not msg:
        msg = "No crypto to list."
    
    await ctx.send(msg)

@client.command()
async def deleteUser(ctx, target=""):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if target == "":
        await ctx.send(f"Usage: {constants.PREFIX}deleteUser [target]")
        return
    
    target_id = tc.pingtoid(target)
    if target_id is None:
        await ctx.send(f"Usage: {constants.PREFIX}deleteUser [target] (target must be a ping)")
        return
    else:
        target_name = tc.idtoname(ctx, target_id)
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
    
    user_coin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]: 
            user_coin = key
    
    if user_coin == "":
        await ctx.send(f"You do not currently own a crypto. You can create one with {constants.PREFIX}createCrypto.")

    if str(target_id) not in coins[user_coin]["Bank"]:
        await ctx.send(f"{target_name} does not have any of your crypto.")
        return
    
    popped_data = coins[user_coin]["Bank"].pop(str(target_id))["Amt"]
    
    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)
    
    await ctx.send(f"Successfully removed {target_name} from your crypto.\n{target_name} had {popped_data} coins.")

@client.command()
async def transferCrypto(ctx, arg1="", arg2="", amount=None, *reason: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    # exception handling fun
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        await ctx.send(f"Usage: {constants.PREFIX}transferCrypto [user_from] [user_to] [amount] [reason: optional]" +
                       "\nOR\n" + 
                       f"Usage: {constants.PREFIX}transferCrypto [crypto_name] [user_to] [amount] [reason: optional] (user_from is you)" +
                       "\namount must be an integer.")
        return
    if arg1 == "" or arg2 == "" or amount is None:
        await ctx.send(f"Usage: {constants.PREFIX}transferCrypto [user_from] [user_to] [amount] [reason: optional]" +
                       "\nOR\n" + 
                       f"Usage: {constants.PREFIX}transferCrypto [cryptoName] [user_to] [amount] [reason: optional] (user_from is you)")
    if amount <= 0:
        await ctx.send("Amount must be greater than 0.")
        return

    if tc.pingtoid(arg1) is not None:
        await transferCryptoOwner(ctx, tc.pingtoid(arg1), tc.pingtoid(arg2), amount, reason)
    else:
        await transferCryptoUser(ctx, arg1, tc.pingtoid(arg2), amount, reason)

async def transferCryptoUser(ctx, crypto_name: str, user_to_id: str, amount: int, reason: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    user_from_id = ctx.author.id

    user_to_name = tc.idtoname(ctx, user_to_id)

    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id

    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    if crypto_name.lower() not in coins:
        await ctx.send(f"{crypto_name} does not exist.")
        return
    
    crypto_name = crypto_name.lower()
    display_name = coins[crypto_name]["DisplayName"]    
    
    if str(user_from_id) not in coins[crypto_name]["Bank"]:
        await ctx.send(f"You do not have any {display_name}.")
        return
    if coins[crypto_name]["Bank"][str(user_from_id)]["Amt"] < amount:
        await ctx.send(f"You do not have enough of {display_name}.")
        return
    
    if str(user_to_id) not in coins[crypto_name]["Bank"]:
        coins[crypto_name]["Bank"][str(user_to_id)] = {"Amt": 0, "Name": user_to_name}

    coins[crypto_name]["Bank"][str(user_from_id)]["Amt"] -= amount
    coins[crypto_name]["Bank"][str(user_to_id)]["Amt"] += amount

    coins[crypto_name]["Bank"][str(user_from_id)]["Name"] = tc.idtoname(ctx, ctx.author.id) # updating name in database
    coins[crypto_name]["Bank"][str(user_to_id)]["Name"] = user_to_name # updating name in database

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    msg = f"Successfully transferred {amount} {display_name} to {user_to_name}.\n\
{user_to_name} now has {coins[crypto_name]['Bank'][str(user_to_id)]['Amt']}. (Rank #{tc.get_placement(ctx, user_to_id, crypto_name)} in {display_name})\n\
You now have {coins[crypto_name]['Bank'][str(user_from_id)]['Amt']}. (Rank #{tc.get_placement(ctx, user_from_id, crypto_name)} in {display_name})"

    show = False

    if reason != ():
        reason = list(reason)

        for i in range(len(reason)):
            reason[i] = "".join(reason[i])

        if reason[-1] in ["-s", "--show"]:
            reason.pop(-1)
            show = True

        if reason != []:
            reason = " ".join(reason)
            msg += f"\nReason: {reason}"

    await ctx.send(msg)

    if show:
        await ctx.send("New standings:\n")
        await showCrypto(ctx, crypto_name)

async def transferCryptoOwner(ctx, user_from_id: str, user_to_id: str, amount: int, reason: tuple):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    user_from_name = tc.idtoname(ctx, user_from_id)
    user_to_name = tc.idtoname(ctx, user_to_id)

    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")
    
    user_coin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            user_coin = key
    if user_coin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    if str(user_from_id) not in coins[user_coin]["Bank"]:
        await ctx.send(f"{user_from_name} does not have any of your crypto.")
        return
    if str(user_to_id) not in coins[user_coin]["Bank"]:
        coins[user_coin]["Bank"][str(user_to_id)] = {"Amt": 0, "Name": user_to_name}
    
    if coins[user_coin]["Bank"][str(user_from_id)]["Amt"] < amount:
        user_from_amt = coins[user_coin]["Bank"][str(user_from_id)]["Amt"]
        await ctx.send(f"{user_from_name} only has {user_from_amt} coins. Please try again with a lower amount.")
        return
    
    coins[user_coin]["Bank"][str(user_from_id)]["Amt"] -= amount
    coins[user_coin]["Bank"][str(user_to_id)]["Amt"] += amount

    coins[user_coin]["Bank"][str(user_from_id)]["Name"] = user_from_name # updating name in database
    coins[user_coin]["Bank"][str(user_to_id)]["Name"] = user_to_name # updating name in database

    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    msg = f"Successfully transferred {amount} coins from {user_from_name} to {user_to_name}.\n\
{user_from_name} now has {coins[user_coin]['Bank'][str(user_from_id)]['Amt']} coins. (Rank #{tc.get_placement(ctx, user_from_id, user_coin)} in {user_coin})\n\
{user_to_name} now has {coins[user_coin]['Bank'][str(user_to_id)]['Amt']} coins. (Rank #{tc.get_placement(ctx, user_to_id, user_coin)} in {user_coin})"
    
    show = False

    if reason != ():
        reason = list(reason)

        for i in range(len(reason)):
            reason[i] = "".join(reason[i])

        if reason[-1] in ["-s", "--show"]:
            reason.pop(-1)
            show = True

        if reason != []:
            reason = " ".join(reason)
            msg += f"\nReason: {reason}"
    
    await ctx.send(msg)

    if show:
        await ctx.send("New standings:\n")
        await showCrypto(ctx, user_coin)
    
@client.command()
async def renameCrypto(ctx, new_name=""):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if new_name == "":
        await ctx.send(f"Usage: {constants.PREFIX}renameCrypto [new_name]")
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    user_coin = ""
    for key, value in coins.items():
        if ctx.author.id == value["Owner"]:
            user_coin = key
    if user_coin == "":
        await ctx.send(f"You do not own a crypto. You can create one with {constants.PREFIX}createCrypto.")
        return
    
    old_data = coins.pop(user_coin)
    old_name = old_data["DisplayName"]

    old_data["DisplayName"] = new_name
    coins[new_name.lower()] = old_data
    
    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    await ctx.send(f"Successfully renamed {old_name} to {new_name}.")

@client.command()
async def debug(ctx):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        id = ctx.guild.id
    
    coins = fh.json_read(constants.DATA_PATH + str(id) + "-crypto.json")

    await ctx.send("Updating names...")

    changes = 0
    exceptions = 0
    for coin in coins:
        for user in coins[coin]["Bank"]:
            try:
                user_name = tc.idtoname(ctx, int(user))
                if user_name != coins[coin]["Bank"][user]["Name"]:
                    changes += 1
                    coins[coin]["Bank"][user]["Name"] = user_name
            except Exception as e:
                print(e)
                exceptions += 1
                pass
    
    coins = tc.rearrange(coins)
    
    fh.json_write(constants.DATA_PATH + str(id) + "-crypto.json", coins)

    await ctx.send(f"Updated {changes} names. Encountered {exceptions} exceptions.")

@client.command(aliases=['cryptoHelp'])
async def help(ctx, command=""):
    if ctx.guild.id in constants.BOYCOTT:
        await ctx.send(constants.BOYCOTT_MSG)
        return
    
    if command.lower() in constants.HELP_INDICES:
        await ctx.send(constants.HELP[constants.HELP_INDICES[command.lower()]])
    else:
        await ctx.send(constants.HELP_MSG)

client.run(os.getenv("TOKEN"))