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

#===Commands===>
#-=-Help-=->
@bot.tree.command(name="help" , description="Get Info and Help." , guild=discord.Object(id=1266707957467451482))
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title=":white_check_mark: Commands:" , description="Help - Ping - Kick" , color = discord.Color.blue())
    embed.set_footer(text="Developers : .sirod. and pedart_mord")
    await interaction.response.send_message(embed = embed)
#-=-Ping-=->
@bot.tree.command(name="ping" , description="Check the bot speed" , guild = discord.Object(id=1266707957467451482))
async def slash_command(interaction: discord.Interaction):
    embed = discord.Embed(title=":white_check_mark: Pong!" , description=f"Latency: {round(bot.latency * 1000)} ms!" , color=discord.Color.blue())
    await interaction.response.send_message(embed = embed)
#-=-Avatar-=->
@bot.tree.command(name="avatar" , description="Get users avatar." , guild = discord.Object(id=1266707957467451482))
async def avatar(interaction: discord.Interaction , member: discord.Member):
    url = member.avatar.url
    await interaction.response.send_message(url)
#-=-Kick-=->
@bot.tree.command(name="kick" , description="Kick a Member." , guild = discord.Object(id=1266707957467451482))
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
@bot.tree.command(name="ban" , description="Ban a Member." , guild = discord.Object(id=1266707957467451482))
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
@bot.tree.command(name="unban" , description="Unban a Member." , guild = discord.Object(id=1266707957467451482))
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

#===Quis===>

@bot.tree.command(name="quiz" , description="Start Quiz Game." , guild = discord.Object(id=1266707957467451482))
async def quiz(interaction: discord.Interaction):

    btn1 = Button(label="1" , style=discord.ButtonStyle.gray)
    btn2 = Button(label="2" , style=discord.ButtonStyle.red)
    btn3 = Button(label="3" , style=discord.ButtonStyle.green)
    btn4 = Button(label="4" , style=discord.ButtonStyle.blurple)

    soalat = [
        "https://cdn.discordapp.com/attachments/1266707957467451485/1267492952674930719/soal2.png?ex=66a8fc4c&is=66a7aacc&hm=34474047074465375357deadf21e50a3e6c157810ec3b0e82cb2b6d9b05ba5b6&",
        "https://cdn.discordapp.com/attachments/1266707957467451485/1267492952343707658/soal1.png?ex=66a8fc4c&is=66a7aacc&hm=8de60524789c9de9b88cc3793cfea53b85428cc1e99797e5beade56c75ff1966&"
    ]

    b = random.choice(soalat)

    async def btn1_callback(interaction):
        embed = discord.Embed(title="❌ Wrong!" , color=discord.Color.red())
        await interaction.response.send_message(embed = embed)
        btn1.disabled = True
        btn2.disabled = True
        btn3.disabled = True
        btn4.disabled = True

    async def btn2_callback(interaction):
        if b == "https://cdn.discordapp.com/attachments/1266707957467451485/1267492952343707658/soal1.png?ex=66a8fc4c&is=66a7aacc&hm=8de60524789c9de9b88cc3793cfea53b85428cc1e99797e5beade56c75ff1966&":
            embed = discord.Embed(title=":white_check_mark: Correct!" , color=discord.Color.green())
            await interaction.response.send_message(embed = embed)
            btn1.disabled = True
            btn2.disabled = True
            btn3.disabled = True
            btn4.disabled = True
        else:
            embed = discord.Embed(title="❌ Wrong!" , color=discord.Color.red())
            await interaction.response.send_message(embed = embed)
            btn1.disabled = True
            btn2.disabled = True
            btn3.disabled = True
            btn4.disabled = True

    async def btn3_callback(interaction):
        if b == "https://cdn.discordapp.com/attachments/1266707957467451485/1267492952674930719/soal2.png?ex=66a8fc4c&is=66a7aacc&hm=34474047074465375357deadf21e50a3e6c157810ec3b0e82cb2b6d9b05ba5b6&":
            embed = discord.Embed(title=":white_check_mark: Correct!" , color=discord.Color.green())
            await interaction.response.send_message(embed = embed)
            btn1.disabled = True
            btn2.disabled = True
            btn3.disabled = True
            btn4.disabled = True
        else:
            embed = discord.Embed(title="❌ Wrong!" , color=discord.Color.red())
            await interaction.response.send_message(embed = embed)
            btn1.disabled = True
            btn2.disabled = True
            btn3.disabled = True
            btn4.disabled = True

    async def btn4_callback(interaction):
        embed = discord.Embed(title="❌ Wrong!" , color=discord.Color.red())
        await interaction.response.send_message(embed = embed)
        btn1.disabled = True
        btn2.disabled = True
        btn3.disabled = True
        btn4.disabled = True

    btn1.callback = btn1_callback
    btn2.callback = btn2_callback
    btn3.callback = btn3_callback
    btn4.callback = btn4_callback

    view = View()
    view.add_item(btn1)
    view.add_item(btn2)
    view.add_item(btn3)
    view.add_item(btn4)

    await interaction.response.send_message(b , view = view)

#===Run===>
bot.run('')