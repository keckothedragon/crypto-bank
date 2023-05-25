import discord

intents = discord.Intents.all()

prefix = "$"

jsonFilePath = "./crypto.json"

pickleFilePath = "./confirmation.pickle"

helpMsg = ["Commands:", # to make easier to read
f"{prefix}showCrypto [name]: Shows standings for a specific crypto.",
f"{prefix}addCrypto [target] [amount]: Adds amount of your own crypto to a user (do not ping them in the message).",
f"{prefix}createCrypto [name]: Creates a crypto with the specified name. If you already own a crypto, you will not be able to make another. Crypto names cannot contain spaces.",
f"{prefix}deleteCrypto: Deletes the users crypto, asking first for confirmation or cancellation.",
f"{prefix}confirmDeletion: Confirms deletion after deleteCrypto was called.",
f"{prefix}cancelDeletion: Cancels deletion after deleteCrypto was called.",
f"{prefix}help: Shows this message."]
helpMsg = "\n".join(helpMsg)