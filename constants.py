import discord

intents = discord.Intents.all()

prefix = "$"

dataPath = "./data/"

helpMsg = f"Commands (do not include brackets around arguments):\n\
* {prefix}showCrypto [name]: Shows standings for a specific crypto. ALT: Shows all crypto of a specific user (ping them).\n\
* {prefix}listCrypto: Shows all cryptos stored.\n\
* {prefix}addCrypto [target] [amount] [reason]: Adds amount of your own crypto to a user (you must ping them). Reason is optional, and will be displayed on confirmation.\n\
* {prefix}setCrypto [target] [amount] [reason]: Same as addCrypto, but sets the value instead of adding.\n\
* {prefix}createCrypto [name]: Creates a crypto with the specified name. If you already own a crypto, you will not be able to make another. Crypto names cannot contain spaces.\n\
* {prefix}deleteCrypto: Deletes your crypto, asking first for confirmation or cancellation.\n\
* {prefix}confirmDeletion: Confirms deletion after deleteCrypto was called.\n\
* {prefix}cancelDeletion: Cancels deletion after deleteCrypto was called.\n\
* {prefix}deleteUser [target]: Deletes target from your crypto.\n\
* {prefix}transferCrypto [userFrom] [userTo] [amount] [reason]: Transfers amount of your crypto from userFrom to userTo. Both userFrom and userTo must have accounts in your crypto. Reason is optional, and will be displayed on confirmation.\n\
* {prefix}renameCrypto [newName]: Renames your crypto to newName. Crypto names cannot contain spaces.\n\
* {prefix}cryptoHelp: Shows this message."

bankExceptions = {1114372122509332651:915361057185357874}