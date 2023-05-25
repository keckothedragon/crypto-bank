# Crypto Bank
## Setup
Thank you for downloading the code for my bot, Crypto Bank! Crypto Bank allows you to keep track of made up points with others in your Discord servers. I chose to call it Crypto Bank because it started as a joke with friends where each person had their own CryptoCurrency (ex. "John Coin", "Bob Coin", etc.).

When you initially download the code, if you just try to run the file, it will not work. This is because the JSON and Pickle files must be initialized with values, since the first part of every command that writes to them first involves reading them.

Before you run the code, run the script "setup.py" to create "confirmation.pickle" and "crypto.json" files.
## Explanation of commands / Usage
Here is a detailed explanation of each command available (in the order they appear in the file):

### showCrypto
showCrypto takes one argument: the name of the crypto to show. It then shows a sorted leaderboard of everyone who has this crypto, and how much of it they have.

### addCrypto
addCrypto takes two arguments: the person to add the crypto to, and the amount to add. It will automatically add to the user's own crypto. If the user does not have a crypto, it will alert them. After adding the amount to the target, it shows how many coins the user now has. A negative amount of coins can also be passed through, but the message does not change (because I'm too lazy lol).

### createCrypto
createCrypto takes one argument: the name of the crypto. It then creates a crypto with that name. If the user already has created a crypto, they are not allowed to make another crypto. Also keep in mind that the names cannot have spaces in them due to the way Discord's commands work.

### deleteCrypto
deleteCrypto does not take any arguments. It gives a dialogue to the user to make them confirm they want to delete their crypto, then passes the torch off to confirmDeletion and cancelDeletion. The awaiting confirmations are stored in a pickle file.

### confirmDeletion
confirmDeletion does not take any arguments. If the user has a deletion that is awaiting confirmation, it will occur. If not, the user will be notified and nothing will happen.

### cancelDeletion
cancelDeletion does not take any arguments. If the user has a deletion that is awaiting confirmation, it will be cancelled. If not, the user will be notified and nothing will happen.

### help
help does not take any arguments. help shows an abridged version of these explanations.