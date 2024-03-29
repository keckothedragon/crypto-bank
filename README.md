# Crypto Bank
## Setup
Thank you for downloading the code for my bot, Crypto Bank! Crypto Bank allows you to keep track of made up points with others in your Discord servers. I chose to call it Crypto Bank because it started as a joke with friends where each person had their own crypto currency (ex. "John Coin", "Bob Coin", etc.). All files must be placed in the same directory. The data will automatically be stored in a "data" folder in the same directory as the rest. This can be changed by changing the DATAPATH variable in constants.py.

If you want to run the code for yourself, the main file to run is crypto.py, as you may have guessed. Before running, you must create a file called ".env" with a variable TOKEN containing the bot's token. The bot only needs read and send messages permissions in the server you are adding it to, but I generally tend to give my bots administrator to be safe.

## Explanation of commands / Usage
Here is a detailed explanation of each command available (in the order they appear in the file). Keep in mind that whenever a user needs to be passed through, the person calling the command must ping them. For example: "$addCrypto @keckothedragon 5".

### showCrypto
showCrypto takes one argument: the name of the crypto to show. It then shows a sorted leaderboard of everyone who has this crypto, and how much of it they have.

#### Alternate version:
showCrypto takes one argument: the name of the person to show the crypto of. This must be in the form of a ping. It then lists every crypto they own, and how much of each one they have.

### addCrypto
addCrypto takes three arguments: the person to add the crypto to, the amount to add, and an optional reason. It will automatically add to the user's own crypto. If the user does not have a crypto, it will alert them. After adding the amount to the target, it shows how many coins the user now has, as well as their new ranking in the user's crypto. A negative amount of coins can also be passed through, but the message does not change (because I'm too lazy lol). The reason argument is optional, but if it is passed through, it will be diplayed to the user when the other message is sent. If the command call ends in -s or --show, showCrypto will be called afterwards with the user's own crypto.

### setCrypto
setCrypto takes three arguments: the person to set the value of crypto, the new value, and an optional reason. This is similar to addCrypto, except it sets the value instead of adding it. See addCrypto for full details.

### createCrypto
createCrypto takes one argument: the name of the crypto. It then creates a crypto with that name. If the user already has created a crypto, they are not allowed to make another crypto. Also keep in mind that the names cannot have spaces in them due to the way Discord's commands work.

### deleteCrypto
deleteCrypto does not take any arguments. It will delete the user's crypto if they own one. After using this command, restoreCrypto can be used to restore a deleted crypto. Keep in mind that if a user deletes a crypto then creates a new one, it can no longer be restored.

### restoreCrypto
restoreCrypto does not take any arguments. It will restore a previously deleted crypto if the user does not have one. If the user has created a crypto since they originally deleted a crypto, they will not be able to restore it.

### listCrypto
listCrypto does not take any arguments. listCrypto will show the names of all crypto stored.

### deleteUser
deleteUser takes one argument, the person to delete the crypto from. It will remove the person from the user's own crypto. If the user does not have a crypto, they will be alerted. Unlike deleteCrypto, this does not prompt the user to confirm deletion, so be careful when using this command. After deleting the person from the crypto, it will send a message containing their original amount of crypto, so it may be added back if the user made a mistake.

### transferCrypto
There are two ways to use transferCrypto, as the owner of a crypto, transferring between users or as someone who has crypto and wants to transfer to someone else. Since these are fairly different, I made two parts to this section.
#### Owner use
transferCrypto takes four arguments, the person to take crypto from, the person to deposit the crypto to, the amount to transfer, and an optional reason. It will automatically do this for the user's crypto. If the person to take the crypto from does not have a sufficient amount of crypto, the user will be alerted. If the person to deposit the crypto to does not have any of the user's crypto, they will still be given the amount. If the operation was successful, a message is shown detailing the transfer and the amount, and the new balances of both people involved, along with both of their new rankings in the user's crypto. If a reason was provided, that will also be shown. If the command call ends in -s or --show, showCrypto will be called afterwards with the user's crypto or the crypto specified.
#### User use
transferCrypto takes four arguments, the crypto to be used in the transaction, the person to deposit the crypto to, the amount to transfer, and an optional reason. It will automatically transfer the crypto from the user to the person to deposit the crypto to. If the specified crypto does not exist, the user will be alterted. Also, if the user does not have a sufficient amount of the specified crypto, they will be alerted. If the person to deposit the crypto to does not have any of the specified crypto, they will still be given the crypto. If the operation was successful, a message is shown detailing the transfer and the amount, as well as the new balances of both people involved, along with their new ranks in the specified crypto. If a reason was provided, that will be shown. If the command call ends in -s or --show, showCrypto will be called afterwards with the user's crypto or the crypto specified.

### renameCrypto
renameCrypto takes one argument, the new name of the crypto. It will automatically rename the user's crypto to the new name. Crypto names cannot contain spaces.

### debug
This is only useful if for some reason you have an old database version and need to update. If you have just downloaded the code, there is no need to run this. If you have an old database version, you need to run update_database.py, then run this command to fetch names for all users.

### disable
This is used to disable Crypto Bank from Discord directly rather than having to manually stop the code. This can only be done by the owner of the code, set by constants.OWNER.

### cryptoHelp
cryptoHelp takes an optional argument: the command to show help for. If no argument is passed, cryptoHelp shows an abridged version of these explanations. If a command is passed, it will show help for that specific command.

## Miscellaneous stuff
### Backups
Backups are automatically saved in the backups folder at the root of wherever you run your code. By default, there will be backups for the last 10 commands run that write to crypto.json, which is pretty much all of them.
### Constants
You should not have to change too much about constants.py, but there are a few variables you may want to change. The only variables you should modify are DATA_PATH as mentioned earlier, PREFIX, BANK_EXCEPTIONS, and COIN_HIERARCHY.

#### PREFIX
PREFIX is simple. It is the prefix to be used whenever a command is called on discord. The only thing to keep in mind is that the help command may overlap with another bot, so it is recommended to keep it as "$".

#### BANK_EXCEPTIONS
BANK_EXCEPTIONS is a way to link two servers and have them share crypto information. This is stored as a dictionary, where each key is the id of the guild that will be redirected, and the value is the id of the guild it will be redirected to.

For example, if I wanted to link guild id 5 and guild id 10, I would have:

BANK_EXCEPTIONS = {5:10} or BANK_EXCEPTIONS = {10:5}

It doesn't matter what order they are in, unless you have old data from a guild that you want to link, so if guild 10 had data you wanted to preserve, you would use

BANK_EXCEPTIONS = {5:10}

to have guild id 5 use guild id 10's data instead.

#### COIN_HIERARCHY
COIN_HIERACHY is somewhat complicated and mostly mundane. I only made it so I can ensure that specific cryptos appear at the top of the list when listCrypto is used.

To use it, simply put the user id whose crypto you want to be at the top of the list. The order of the list determines the order of the redirected cryptos.

For example, if I wanted Bobcoin (belonging to user id 123) and BillyCoin (belonging to user id 422) to be at the top of the list, I would have it like this:

COIN_HIERARCHY = [123, 422]

If the list of coins was normally:

JoeCoin, JamesBucks, Bobcoin, SamCoin, BillyCoin

It would become:

Bobcoin, BillyCoin, JoeCoin, JamesBucks, SamCoin

#### BACKUP_PATH
Pretty self-explanatory. The location where backups are stored.

#### BACKUP_NUMBER
The number of backups to store. The backups will be stored in the location defined by BACKUP_PATH. The default for this is 10.

A backup is made every time the database is written to. This happens when every command is run, with the sole exception of cryptoHelp.

#### DO_FUNNY_MSG
This is a joke feature that I added because my friends were annoying me. If someone uses listCrypto as if it was showCrypto, there is normally a special dialogue to let them know to use showCrypto instead. However, if DO_FUNNY_MSG is set to True, Crypto Bank will track every time someone uses it like this, and if they do it FUNNY_MSG_TOLERANCE times, there will be a special message.

#### FUNNY_MSG_TOLERANCE
The number of times that someone can misuse listCrypto before the special message.

If DO_FUNNY_MSG is set to False, this doees not apply.

#### FUNNY_MSG
The message to display when the user misuses listCrypto FUNNY_MSG_TOLERANCE times. You can set this to whatever you want, but this is the big insult.

If you are making a custom message, the string may include up to one {} to show the number of times the user misused listCrypto. If there is more than one, it will not work as intended.

If DO_FUNNY_MSG is set to False, this doees not apply.

#### FUNNY_MSG_DAD_BOT
If the servers you are in also have my other bot, Dad-bot, this will add an extra reply at the end to reply to Dad-bot's reply to FUNNY_MSG. This is only applicable if FUNNY_MSG has "i'm", "im", "i am", or "i’m" in it and the reply would make sense.

If the reply does not make sense or Dad-bot is not in any servers you are using this in, you can simply disable this by making it an empty set ({}).

If DO_FUNNY_MSG is set to False, this does not apply.

#### OWNER
OWNER is used for the disable command so that only you can disable the bot. See disable for more details.