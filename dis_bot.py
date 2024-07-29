#===Imports===>

import discord
from discord.ext import commands
from discord.ext import commands, tasks 

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

#===Commands===>

@bot.tree.command(name="help" , description="Get Info and Help." , guild=discord.Object(id=1266707957467451482))
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title=":white_check_mark: Commands:" , description="Help - Ping - Kick" , color = discord.Color.blue())
    embed.set_footer(text="Developers : .sirod. and pedart_mord")
    await interaction.response.send_message(embed = embed)

@bot.tree.command(name="ping" , description="Check the bot speed" , guild = discord.Object(id=1266707957467451482))
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)} ms")# پینگ باتو روند میکنه اعشاری نشون نمیده

@bot.tree.command(name="kick" , description="Kick a Member." , guild = discord.Object(id=1266707957467451482))
async def kick(interaction: discord.Interaction , member : discord.Member):
    if interaction.user.guild_permissions.kick_members:
        if member.top_role < interaction.user.top_role:
            if member:
                await member.kick(reason="You have been banned.")
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

bot.run('')