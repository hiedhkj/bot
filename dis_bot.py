#===Imports===>

import discord
import random
from discord.ext import commands
from discord.ext import commands, tasks 
from discord.ui import Button , View
from datetime import datetime, timedelta, timezone
import re

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
#-=-Banner-=->
@bot.tree.command(name="banner", description="Get Users Banner.", guild=g)
async def banner(interaction: discord.Interaction, member: discord.Member):
    if member.banner:
        burl = member.banner.url
        await interaction.response.send_message(burl)
    else:
        await interaction.response.send_message("This member does not have a banner.")
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
#-=-Timeout-=->
@bot.tree.command(name="timeout", description="Timeout Members with custom duration.", guild=g)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: str):
    if not interaction.user.guild_permissions.mute_members:
        embed = discord.Embed(title=":x: You can't timeout members.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if member is None or interaction.user.top_role <= member.top_role:
        embed = discord.Embed(title=":x: Your role is too low or member is invalid.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    match = re.match(r"(\d+)([dhm])", duration)
    if not match:
        embed = discord.Embed(title=":x: Invalid duration format. Use 'd' for days, 'h' for hours, or 'm' for minutes.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    value, unit = int(match.group(1)), match.group(2)
    if unit == 'd': timeout_duration = timedelta(days=value)
    elif unit == 'h': timeout_duration = timedelta(hours=value)
    elif unit == 'm': timeout_duration = timedelta(minutes=value)

    until_time = datetime.now(timezone.utc) + timeout_duration
    await member.timeout(until_time, reason="You have been timeouted.")
    embed = discord.Embed(title=":white_check_mark: Timeouted!", description=f"{member.name} has been timeouted for {duration} by {interaction.user}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
#-=-Add Role-=->
@bot.tree.command(name="add-role" , description="Add role to members." , guild = g)
async def addrole(interaction: discord.Interaction , member : discord.Member , role : discord.Role):
    if interaction.user.guild_permissions.manage_roles:
        if member.top_role < interaction.user.top_role:
            if member:
                await member.add_roles(role)
                embed = discord.Embed(title=f":white_check_mark: @{role.name} Added To {member.name}" , color = discord.Color.green())
                await interaction.response.send_message(embed = embed)
            else:
                embed = discord.Embed(title=":x: Error!" , color = discord.Color.red())
                await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(title=":x: Your role is low." , color = discord.Color.red())
            await interaction.response.send_message(embed = embed)
    else:
        embed = discord.Embed(title=":x: You can't give role to members." , color = discord.Color.red())
        await interaction.response.send_message(embed = embed)
#-=-Remove Role-=->
@bot.tree.command(name="remove-role" , description="Remove role to members." , guild = g)
async def removerole(interaction: discord.Interaction , member : discord.Member , role : discord.Role):
    if interaction.user.guild_permissions.manage_roles:
        if member.top_role < interaction.user.top_role:
            if member:
                await member.remove_roles(role)
                embed = discord.Embed(title=f":white_check_mark: @{role.name} Removed from {member.name}." , color = discord.Color.green())
                await interaction.response.send_message(embed = embed)
            else:
                embed = discord.Embed(title=":x: Error!" , color = discord.Color.red())
                await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(title=":x: Your role is low." , color = discord.Color.red())
            await interaction.response.send_message(embed = embed)
    else:
        embed = discord.Embed(title=":x: You can't remove role from members." , color = discord.Color.red())
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
#-=-Ticket-=->
async def b_e_callback(interaction: discord.Interaction):
    # پیدا کردن رول
    role_name = "Support Team"
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    # پیدا کردن کتگوری
    category_id = 1266707957467451483 
    category = interaction.guild.get_channel(category_id)
    if category:
        #پرمیشن هایی کهداخل چنل قرار میگیره
        over = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False), 
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)}
        # ساخت چنل
        channel = await interaction.guild.create_text_channel(
            name=f'ticket-{interaction.user.name}',
            category=category,
            overwrites=over
        )
        await interaction.response.send_message(f'*Your ticket has been created in {channel.mention}*', ephemeral=True)
    else:
        await interaction.response.send_message('Category not found.', ephemeral=True)

@bot.tree.command(name="ticket", description="Create a ticket platform.", guild=g)
async def Ticket(interaction: discord.Interaction):
    embed_t = discord.Embed(
        title="Click on the button to make a ticket :white_check_mark:",
        description="**`1 - Do not disturb `**:x:\n**`2 - Do not spam    `**:x:\n**`3 - do not mention `**:x:",
        color=discord.Color.blue()
    )
    embed_t.set_image(url="https://media.lordicon.com/icons/wired/outline/759-ticket-coupon.gif")
    embed_t.set_footer(text="J i M i Team", icon_url="https://images-ext-1.discordapp.net/external/QGxX2l_m03nfw28FarkniIlMQ5riVt8h5wqJ0kmBhAo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1266704692650446930/0d12eb3e3807c2ddf9518a9b27e9b7ca.png?format=webp&quality=lossless&width=417&height=417")

    b_e = Button(label="Create Ticket", style=discord.ButtonStyle.blurple)
    b_e.callback = b_e_callback

    view = View()
    view.add_item(b_e)
    await interaction.response.send_message(embed=embed_t, view=view)

#===Run===>
bot.run('')