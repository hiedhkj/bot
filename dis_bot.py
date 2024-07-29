import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)
intents.messages = True

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1266707957467451482))
    print(f'{bot.user}')

@bot.tree.command(name="ping" , description="Check the bot speed" , guild = discord.Object(id=1266707957467451482))
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)} ms")# پینگ باتو روند میکنه اعشاری نشون نمیده

bot.run('')