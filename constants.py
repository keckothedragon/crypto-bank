import discord

INTENTS = discord.Intents.all()

PREFIX = "$"

DATAPATH = "./data/"

HELP = [
    f'{PREFIX}showCrypto [name]: Shows standings for a specific crypto. ALT: {PREFIX}showCrypto [user]: Shows all crypto of a specific user (ping them).',
    f'{PREFIX}listCrypto: Shows all cryptos stored.',
    f'{PREFIX}addCrypto [target] [amount] [reason]: Adds amount of your own crypto to a user (you must ping them). Reason is optional, and will be displayed on confirmation.',
    f'{PREFIX}setCrypto [target] [amount] [reason]: Same as addCrypto, but sets the value instead of adding.',
    f'{PREFIX}createCrypto [name]: Creates a crypto with the specified name. If you already own a crypto, you will not be able to make another. Crypto names cannot contain spaces.',
    f'{PREFIX}deleteCrypto: Deletes your crypto, asking first for confirmation or cancellation.',
    f'{PREFIX}confirmDeletion: Confirms deletion after deleteCrypto was called.',
    f'{PREFIX}cancelDeletion: Cancels deletion after deleteCrypto was called.',
    f'{PREFIX}deleteUser [target]: Deletes target from your crypto.',
    f'{PREFIX}transferCrypto [userFrom] [userTo] [amount] [reason]: Transfers amount of your crypto from userFrom to userTo. Both userFrom and userTo must have accounts in your crypto. Reason is optional, and will be displayed on confirmation. ALT: \
{PREFIX}transferCrypto [crypto] [userTo] [amount] [reason]: Transfers amount of crypto from you to userTo. You must have a succifient amount of the crypto. Reason is optional, and will be displayed on confirmation.',
    f'{PREFIX}renameCrypto [newName]: Renames your crypto to newName. Crypto names cannot contain spaces.',
    f'{PREFIX}cryptoHelp: Shows this message. ALT: {PREFIX}cryptoHelp [command]: Shows help for a specific command.'
]

HELPMSG = f"Commands (do not include brackets around arguments):\n* " + "\n* ".join(HELP)
HELPMSG = HELPMSG.strip("\n* ")

HELPINDICES = {
    "showcrypto": 0, "show": 0,
    "listcrypto": 1, "list": 1,
    "addcrypto": 2, "add": 2,
    "setcrypto": 3, "set": 3,
    "createcrypto": 4, "create": 4,
    "deletecrypto": 5, "delete": 5,
    "confirmdeletion": 6, "confirm": 6,
    "canceldeletion": 7, "cancel": 7,
    "deleteuser": 8,
    "transfercrypto": 9, "transfer": 9,
    "renamecrypto": 10, "rename": 10
}

bankExceptions = {1114372122509332651:915361057185357874} # you can change this to whatever you want