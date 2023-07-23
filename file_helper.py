import json
import pickle # using pickle to store confirmation as set instead of dict
import os

def json_read(path: str) -> dict:
    try:
        with open(f"{path}", "r") as f:
            data: dict = json.load(f)
    except:
        data = {}
    
    return data


def json_write(path: str, data: dict) -> None:
    while True:
        try:
            with open(f"{path}", "w+") as f:
                json.dump(data, f)
            break
        except FileNotFoundError:
            print("File not found, creating file...")
            os.mkdir("/".join(path.split("/")[:-1]))

def pickle_read(path: str) -> set:
    try:
        with open(f"{path}", "rb") as f:
            data: set = pickle.load(f)
    except FileNotFoundError:
        data = set()
    return data

def pickle_write(path: str, data: set) -> None:
    while True:
        try:
            with open(f"{path}", "wb+") as f:
                pickle.dump(data, f)
            break
        except FileNotFoundError:
            print("File not found, creating file...")
            os.mkdir("/".join(path.split("/")[:-1]))