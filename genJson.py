import json
import constants

def main():
    with open(constants.jsonFilePath, "w") as f:
        json.dump({}, f)
        # dumps starting val so the program doesnt have a stroke trying to read file initially

if __name__ == '__main__':
    main()