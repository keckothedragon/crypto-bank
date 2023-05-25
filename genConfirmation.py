import pickle
import constants

def main():
    with open(constants.pickleFilePath, "wb") as f:
        pickle.dump({1}, f)
        # creates pickles object to make sure program will know it's a set when being used later

if __name__ == '__main__':
    main()