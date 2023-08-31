import discord
from discord.ext import commands

INTENTS = discord.Intents.all()

PREFIX = "$"
# you can change this to whatever you want but keep in mind that help command may overlap with other bots

DATA_PATH = "./data/"

HELP = [
    f'{PREFIX}showCrypto [name]: Shows standings for a specific crypto. ALT: {PREFIX}showCrypto [user]: Shows all crypto of a specific user (ping them).',
    f'{PREFIX}listCrypto: Shows all cryptos stored.',
    f'{PREFIX}addCrypto [target] [amount] [reason]: Adds amount of your own crypto to a user (you must ping them). Reason is optional, and will be displayed on confirmation. OPTIONAL: -s or --show at the end will show updated standings for your crypto after command is called.',
    f'{PREFIX}setCrypto [target] [amount] [reason]: Same as addCrypto, but sets the value instead of adding.',
    f'{PREFIX}createCrypto [name]: Creates a crypto with the specified name. If you already own a crypto, you will not be able to make another. Crypto names cannot contain spaces.',
    f'{PREFIX}deleteCrypto: Deletes your crypto. Deleted cryptos can be restored with restoreCrypto.',
    f'{PREFIX}restoreCrypto: Restores a previously deleted crypto. If you use createCrypto, after deleteCrypto, you will no longer be able to restore it.',
    f'{PREFIX}deleteUser [target]: Deletes target from your crypto.',
    f'{PREFIX}transferCrypto [user_from] [user_to] [amount] [reason]: Transfers amount of your crypto from user_from to user_to. user_from must have a sufficient amount of crypto. Reason is optional, and will be displayed on confirmation. ALT: \
{PREFIX}transferCrypto [crypto] [user_to] [amount] [reason]: Transfers amount of crypto from you to user_to. You must have a succifient amount of the crypto. Reason is optional, and will be displayed on confirmation. OPTIONAL: -s or --show at the end will show updated standings for your crypto or the specified crypto after command is called.',
    f'{PREFIX}renameCrypto [new_name]: Renames your crypto to new_name. Crypto names cannot contain spaces.',
    f'{PREFIX}cryptoHelp: Shows this message. ALT: {PREFIX}cryptoHelp [command]: Shows help for a specific command.'
]

HELP_MSG = f"Commands (do not include brackets around arguments):\n* " + "\n* ".join(HELP)
HELP_MSG = HELP_MSG.strip("\n* ")

HELP_INDICES = {
    "showcrypto": 0, "show": 0,
    "listcrypto": 1, "list": 1,
    "addcrypto": 2, "add": 2,
    "setcrypto": 3, "set": 3,
    "createcrypto": 4, "create": 4,
    "deletecrypto": 5, "delete": 5,
    "restorecrypto": 6, "restore": 6,
    "deleteuser": 7,
    "transfercrypto": 8, "transfer": 8,
    "renamecrypto": 9, "rename": 9
}

BANK_EXCEPTIONS = {1114372122509332651:915361057185357874}
# you can change this to whatever you want to link to link two guilds' banks
# see README for full details

COIN_HIERARCHY = [726150411475484713]
# change this to whatever you want to make certain users' cryptos always appear at the top of listCrypto
# see README for full details

BACKUP_PATH = "./backups"

BACKUP_NUMBER = 10
# number of backups to keep

DO_FUNNY_MSG = True
# see readme

FUNNY_MSG_TOLERANCE = 5
# see readme again

FUNNY_MSG = "Listen up. You've used listCrypto wrong {} times. Every single time, I've reminded you \
how to use it. And yet, your tiny brain still can't figure out how to use it. How stupid do you have \
to be to constantly ignore my instructions? I genuinely don't understand how time and time again, you \
ignore me. I'm not even asking you to do anything difficult. I'm just asking you to use listCrypto \
to list all cryptos and showCrypto to show a specific crypto. How hard is that?"

FUNNY_MSG_DAD_BOT = {915361057185357874, 1114372122509332651, 946896976836976690}
# if you have dad-bot in your server

OWNER = 726150411475484713