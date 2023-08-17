import json
import pickle # using pickle to store confirmation as set instead of dict
import os
import constants

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
                backup(data, int(path.split("/")[-1].split("-")[0]))
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

def backup(data: dict, id: int) -> None:
    # can you tell that copilot wrote most of this?
    if not os.path.exists(constants.BACKUP_PATH):
        os.mkdir(constants.BACKUP_PATH)
    if not os.path.exists(f"{constants.BACKUP_PATH}/{id}"):
        os.mkdir(f"{constants.BACKUP_PATH}/{id}")
    files = os.listdir(f"{constants.BACKUP_PATH}/{id}")
    if len(files) >= constants.BACKUP_NUMBER:
        files.sort(key=lambda x: int(x[6:-5]))
        os.remove(f"{constants.BACKUP_PATH}/{id}/{files[0]}")
    try:
        with open(f"{constants.BACKUP_PATH}/{id}/backup{int(files[-1][6:-5]) + 1}.json", "w+") as f:
            json.dump(data, f)
    except IndexError:
        with open(f"{constants.BACKUP_PATH}/{id}/backup0.json", "w+") as f:
            json.dump(data, f)