#===Imports===>

import discord
import random
from discord.ext import commands
from discord.ext import commands, tasks 
from discord.ui import Button , View

#===create bot & permission bot===>

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)
intents.messages = True

#===Login===>
@tasks.loop(minutes=5)  # این تسک هر پنج دقیق ران میشه و اکتیوتی جدید میزاره
async def update_activity():
    guild_count = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{guild_count} servers")
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    update_activity.start() # تسک اجرا میشه
    await bot.tree.sync(guild=discord.Object(id=1266707957467451482))
    print(f'{bot.user}')

#===>
g = discord.Object(id=1266707957467451482)
#===>

#===Commands===>
#-=-Help-=->
@bot.tree.command(name="help" , description="Get Info and Help." , guild = g)
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title=":white_check_mark: Commands:" , description="Help - Ping - Kick" , color = discord.Color.blue())
    embed.set_footer(text="Developers : .sirod. and pedart_mord")
    await interaction.response.send_message(embed = embed)
#-=-Ping-=->
@bot.tree.command(name="ping" , description="Check the bot speed" , guild = g)
async def slash_command(interaction: discord.Interaction):
    embed = discord.Embed(title=":white_check_mark: Pong!" , description=f"Latency: {round(bot.latency * 1000)} ms!" , color=discord.Color.blue())
    await interaction.response.send_message(embed = embed)
#-=-Avatar-=->
@bot.tree.command(name="avatar" , description="Get users avatar." , guild = g)
async def avatar(interaction: discord.Interaction , member: discord.Member):
    url = member.avatar.url
    await interaction.response.send_message(url)
#-=-Clear-=->
@bot.tree.command(name="clear" , description="Clear Messages." , guild = g)
async def clear(interaction: discord.Interaction , number_of_message: int):
    if interaction.user.guild_permissions.manage_messages:
        if number_of_message == None:
            await interaction.channel.purge(limit=3)
        else:
            embed = discord.Embed(title=f':white_check_mark: Clearing {number_of_message} Message' , color = discord.Color.green())
            await interaction.response.send_message(embed = embed , ephemeral = True)
            await interaction.channel.purge(limit=number_of_message)
    else:
        embed = discord.Embed(title=":x: You Can't Clear Messages.")
        await interaction.response.send_message(embed = embed)
#-=-Kick-=->
@bot.tree.command(name="kick" , description="Kick a Member." , guild = g)
async def kick(interaction: discord.Interaction , member : discord.Member):
    if interaction.user.guild_permissions.kick_members:
        if member.top_role < interaction.user.top_role:
            if member:
                await member.kick(reason="You have been kicked.")
                embed = discord.Embed(title=":white_check_mark: Kicked!", description=f"{member.name} Kicked by {interaction.user}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="❌ Error!" , color = discord.Color.red())
                await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(title=f"❌ You Can't Kick {member.name}" , description="Your Role Is Low" , color = discord.Color.red())
            await interaction.response.send_message(embed = embed)
    else:
        embed = discord.Embed(title="❌ You Can't Kick Members!" , description="You have not permissions" , color = discord.Color.red())
        await interaction.response.send_message(embed = embed)
#-=-Ban-=->
@bot.tree.command(name="ban" , description="Ban a Member." , guild = g)
async def ban(interaction: discord.Interaction , member : discord.Member):
    if interaction.user.guild_permissions.ban_members:
        if member.top_role < interaction.user.top_role:
            if member:
                await member.ban(reason="You have been banned.")
                embed = discord.Embed(title=":white_check_mark: Baned!", description=f"{member.name} Baned by {interaction.user}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="❌ Error!" , color = discord.Color.red())
                await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(title=f"❌ You Can't Ban {member.name}" , description="Your Role Is Low" , color = discord.Color.red())
            await interaction.response.send_message(embed = embed)
    else:
        embed = discord.Embed(title="❌ You Can't Ban Members!" , description="You have not permissions" , color = discord.Color.red())
        await interaction.response.send_message(embed = embed)
#-=-Unban-=->
@bot.tree.command(name="unban" , description="Unban a Member." , guild = g)
async def ban(interaction: discord.Interaction , id : str):
    if interaction.user.guild_permissions.ban_members:
        async for ban_entry in interaction.guild.bans():
            user = ban_entry.user

            if user.id == int(id):
                await interaction.guild.unban(user , reason="unbaned" )
                embed = discord.Embed(title=":white_check_mark: Unbaned!", description=f"{user.name} Unaned by {interaction.user}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Member not found in the ban list.")
    else:
        await interaction.response.send_message("❌ You do not have permission")

#===Run===>
bot.run('')