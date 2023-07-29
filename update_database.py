# use to update database if still using old bank format of user_id: value
# if you just downloaded the code, you don't need to run this

import constants
import file_helper

def main():
    id = str(input("Guild ID to update: "))
    data = file_helper.json_read(constants.DATA_PATH + id + "-crypto.json")

    if data == {}:
        print("No data found, exiting...")
        return
    
    for coin in data:
        for user in data[coin]["Bank"]:
            if type(data[coin]["Bank"][user]) == dict:
                continue
            amt = data[coin]["Bank"][user]
            data[coin]["Bank"][user] = {"Amt": amt, "Name": f"PLACEHOLDER: {user}"}

    file_helper.json_write(constants.DATA_PATH + id + "-crypto.json", data)

    print("Successfully updated data!")

if __name__ == "__main__":
    main()