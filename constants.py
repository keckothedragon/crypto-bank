import discord

intents = discord.Intents.all()

prefix = "$"

jsonFilePath = "./crypto.json"

pickleFilePath = "./confirmation.pickle"

helpMsg = f"Commands (do not include brackets around arguments):\n \
{prefix}showCrypto [name]: Shows standings for a specific crypto.\n \
{prefix}listCrypto: Shows all cryptos stored.\n \
{prefix}addCrypto [target] [amount]: Adds amount of your own crypto to a user (do not ping them in the message).\n \
{prefix}createCrypto [name]: Creates a crypto with the specified name. If you already own a crypto, you will not be able to make another. Crypto names cannot contain spaces.\n \
{prefix}deleteCrypto: Deletes the users crypto, asking first for confirmation or cancellation.\n \
{prefix}confirmDeletion: Confirms deletion after deleteCrypto was called.\n \
{prefix}cancelDeletion: Cancels deletion after deleteCrypto was called.\n \
{prefix}cryptoHelp: Shows this message."