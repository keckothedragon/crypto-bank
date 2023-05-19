import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import constants
import json

def json_read(path: str) -> dict:
    with open(f"{path}", "r") as f:
        data: dict = json.load(f)
    return data


def json_write(path: str, data: dict) -> None:
    with open(f"{path}", "w") as f:
        json.dump(data, path)

load_dotenv(".env")

client = commands.Bot(intents=constants.intents, command_prefix=constants.prefix)

@commands.Command
async def hello(ctx, times=1):
    msg = ""
    for _ in range(times):
        msg += "Hello "
    msg = msg.strip()
    await ctx.send(msg)

client.add_command(hello)

client.run(os.getenv("TOKEN"))