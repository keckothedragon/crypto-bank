# Crypto Bank
## Setup
Thank you for downloading the code for my bot, Crypto Bank! Crypto Bank allows you to keep track of made up points with others in your Discord servers. I chose to call it Crypto Bank because it started as a joke with friends where each person had their own CryptoCurrency (ex. "John Coin", "Bob Coin", etc.).

## Explanation of commands / Usage
Here is a detailed explanation of each command available (in the order they appear in the file):

### showCrypto
showCrypto takes one argument: the name of the crypto to show. It then shows a sorted leaderboard of everyone who has this crypto, and how much of it they have.

#### Alternate version:
showCrypto takes one argument: the name of the person to show the crypto of. This must be in the form of a ping. It then lists every crypto they own, and how much of each one they have.

### addCrypto
addCrypto takes three arguments: the person to add the crypto to, the amount to add, and an optional reason. The person must be a ping. It will automatically add to the user's own crypto. If the user does not have a crypto, it will alert them. After adding the amount to the target, it shows how many coins the user now has. A negative amount of coins can also be passed through, but the message does not change (because I'm too lazy lol). The reason argument is optional, but if it is passed through, it will be diplayed to the user when the other message is sent.

### setCrypto
setCrypto takes three arguments: the person to set the value of crypto, the new value, and an optional reason. This is similar to addCrypto, except it sets the value instead of adding it. See addCrypto for full details.

### createCrypto
createCrypto takes one argument: the name of the crypto. It then creates a crypto with that name. If the user already has created a crypto, they are not allowed to make another crypto. Also keep in mind that the names cannot have spaces in them due to the way Discord's commands work.

### deleteCrypto
deleteCrypto does not take any arguments. It gives a dialogue to the user to make them confirm they want to delete their crypto, then passes the torch off to confirmDeletion and cancelDeletion. The awaiting confirmations are stored in a pickle file.

### confirmDeletion
confirmDeletion does not take any arguments. If the user has a deletion that is awaiting confirmation, it will occur. If not, the user will be notified and nothing will happen.

### cancelDeletion
cancelDeletion does not take any arguments. If the user has a deletion that is awaiting confirmation, it will be cancelled. If not, the user will be notified and nothing will happen.

### listCrypto
listCrypto does not take any arguments. listCrypto will show the names of all crypto stored.

### deleteUser
deleteUser takes one argument, the person to delete the crypto from. It will remove the person from the user's own crypto. If the user does not have a crypto, they will be alerted. Unlike deleteCrypto, this does not prompt the user to confirm deletion, so be careful when using this command. After deleting the person from the crypto, it will send a message containing their original amount of crypto, so it may be added back if the user made a mistake.

### transferCrypto
transferCrypto takes four arguments, the person to take crypto from, the person to deposit the crypto to, the amount to transfer, and an optional reason. It will automatically do this for the user's crypto. If the person to take the crypto from does not have a sufficient amount of crypto, the user will be alerted. If the person to deposit the crypto to does not have any of the user's crypto, they will still be given the amount. If the operation was successful, a message is shown detailing the transfer and the amount, and the new balances of both people involved, as well as the reason if one was provided.

### renameCrypto
renameCrypto takes one argument, the new name of the crypto. It will automatically rename the user's crypto to the new name. Crypto names cannot contain spaces.

### cryptoHelp
cryptoHelp does not take any arguments. cryptoHelp shows an abridged version of these explanations.