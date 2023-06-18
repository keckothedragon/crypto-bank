import json
import pickle # using pickle to store confirmation as set instead of dict
import setup

def json_read(path: str) -> dict:
    try:
        with open(f"{path}", "r") as f:
            data: dict = json.load(f)
    except:
        setup.main()
        data = {}
    
    return data


def json_write(path: str, data: dict) -> None:
    with open(f"{path}", "w") as f:
        json.dump(data, f)

def pickle_read(path: str) -> set:
    try:
        with open(f"{path}", "rb") as f:
            data: set = pickle.load(f)
    except FileNotFoundError:
        setup.main()
        data = {}
    return data

def pickle_write(path: str, data: set) -> None:
    with open(f"{path}", "wb") as f:
        pickle.dump(data, f)