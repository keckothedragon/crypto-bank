import discord

def pingtoid(ping) -> int:
    if "<@" not in ping or ">" not in ping:
        return None
    try:
        return int(ping[2:-1])
    except ValueError:
        return None

def idtoname(ctx, id) -> str:
    return discord.utils.get(ctx.guild.members, id=id).display_name