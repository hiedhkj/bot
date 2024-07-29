#===Imports===>

import discord
from discord.ext import commands

#===نمیدونم اینجا چیه===>

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)
intents.messages = True

#===Login===>

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1266707957467451482))
    print(f'{bot.user}')

#===Commands===>

@bot.tree.command(name="ping" , description="Check the bot speed" , guild = discord.Object(id=1266707957467451482))
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)} ms")# پینگ باتو روند میکنه اعشاری نشون نمیده

@bot.tree.command(name="kick" , description="Kick a Member." , guild = discord.Object(id=1266707957467451482))
async def kick(interaction: discord.Interaction , member : discord.member):
    if interaction.author.guild_permissions.kick_members:
        if member.top_role < interaction.author.top_role:
            if member:
                await member.kick(reason="You have been banned.")
                embed = discord.Embed(title=":white_check_mark: Banned!", description=f"{member.name} Kicked by {interaction.author}")
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('error')
        else:
            await interaction.response.send_message(f"You Can't Kick {member.name}")
    else:
        await interaction.response.send_message("You Cant' Kick Members")

bot.run('')