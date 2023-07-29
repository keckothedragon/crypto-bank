import discord
import constants
import file_helper

def pingtoid(ping) -> int:
    if "<@" not in ping or ">" not in ping:
        return None
    try:
        return int(ping[2:-1])
    except ValueError:
        return None

def idtoname(ctx, id) -> str:
    return discord.utils.get(ctx.guild.members, id=id).display_name

def get_placement(ctx, id, coin) -> int:
    id = str(id)
    if ctx.guild.id in constants.BANK_EXCEPTIONS:
        guild_id = constants.BANK_EXCEPTIONS[ctx.guild.id]
    else:
        guild_id = ctx.guild.id
    data = file_helper.json_read(constants.DATA_PATH + str(guild_id) + "-crypto.json")
    if coin not in data:
        return None
    if id not in data[coin]["Bank"]:
        return None
    data = data[coin]["Bank"]

    val = data[id]["Amt"]
    placed = []
    for _, value in data.items():
        placed.append(value["Amt"])
    placed.sort(reverse=True)
    return placed.index(val) + 1