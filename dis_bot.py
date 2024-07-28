import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)
intents.messages = True

@bot.tree.command(name="ping" , description="Check the bot speed" , guild = discord.Object(id=1266707957467451482))
async def slash_command(interaction: discord.Interaction):

    await interaction.response.send_message("Pong!")

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1266707957467451482))
    print(f'{bot.user}')

bot.run('')
