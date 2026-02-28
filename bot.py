print("Bot file is running...")
import discord
from discord.ext import commands
import re
OWNER_ID = 794425897561489440

import os
client.run(os.getenv("MTQ3NzE4NzI3MTI1NzA5NjMyNA.GYE75U.KNEMvaZEEhLKKYAQYAWDxcvAvWS3LVbxEiuLZs"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.presences = False
intents.members = True

braincoins = {}
cooldowns = {}
daily_claim = {}

bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm working 😄")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f"{member} has been kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)

from datetime import timedelta

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration)
    await ctx.send(f"{member} has been timed out for {minutes} minutes.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"{member} timeout removed.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Deleted {amount} messages.", delete_after=3)

import re

bad_words = [
    "fuck", "fucking", "shit", "bitch", "asshole",
    "bastard", "damn", "dick", "pussy", "slut",
    "whore", "retard", "stupid", "idiot",
    "nigga", "nigger", "faggot",
    "cunt", "motherfucker", "porn", "sex"
]

block_links = True
block_invites = True

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    for word in bad_words:
        if word in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, watch your language!",
                delete_after=5
            )
            return

    if block_invites:
        if "discord.gg/" in content or "discord.com/invite/" in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, Discord invites are not allowed!",
                delete_after=5
            )
            return

    if block_links:
        url_pattern = r"(https?://\S+)"
        if re.search(url_pattern, content):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, links are not allowed!",
                delete_after=5
            )
            return

    await bot.process_commands(message)

import random

@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on: {result}")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    owner = guild.owner
    if owner:
        owner_text = f"{"Yoyo"} ({794425897561489440})"
    else:
        owner_text = "Owner not found"

    embed = discord.Embed(
        title="📊 Server Info",
        color=discord.Color.green()
    )

    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Owner", value=owner_text, inline=False)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Channel locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Channel unlocked.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Bot Help Menu",
        description="Here are all my commands:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📌 Basic Commands",
        value="""
`$hello` - Says hello  
`$ping` - Shows bot latency  
`$coinflip` - Flip a coin  
`$serverinfo` - Shows server info  
""",
        inline=False
    )

    embed.add_field(
        name="🛡 Moderation Commands",
        value="""
`$kick @user` - Kick a member  
`$ban @user` - Ban a member  
`$unban username` - Unban a member  
`$timeout @user minutes` - Timeout a member  
`$untimeout @user` - Remove timeout  
`$clear amount` - Delete messages  
`$lock` - Lock channel  
`$unlock` - Unlock channel  
""",
        inline=False
    )

    embed.set_footer(text="Prefix: $")

    await ctx.send(embed=embed)

from collections import defaultdict

# Store up to 5 deleted messages per channel
sniped_messages = defaultdict(list)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    channel_id = message.channel.id

    sniped_messages[channel_id].append({
        "content": message.content,
        "author": message.author,
        "avatar": message.author.avatar.url if message.author.avatar else None
    })

    # Keep only last 5 messages
    if len(sniped_messages[channel_id]) > 5:
        sniped_messages[channel_id].pop(0)

@bot.command()
async def snipe(ctx, index: int = 1):
    channel_id = ctx.channel.id

    if channel_id not in sniped_messages or len(sniped_messages[channel_id]) == 0:
        await ctx.send("There's nothing to snipe.")
        return

    if index < 1 or index > len(sniped_messages[channel_id]):
        await ctx.send(f"Choose a number between 1 and {len(sniped_messages[channel_id])}")
        return

    data = sniped_messages[channel_id][-index]

    embed = discord.Embed(
        description=data["content"],
        color=discord.Color.red()
    )

    embed.set_author(
        name=str(data["author"]),
        icon_url=data["avatar"]
    )

    embed.set_footer(text=f"Snipe #{index}")

    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.purple())
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

@bot.command()
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    amount = braincoins.get(member.id, 0)
    await ctx.send(f"🧠 {member.mention} has **{amount} BrainCoins**")

import random
import time

@bot.command()
async def steal(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("You can't steal from yourself 💀")
        return

    if member.bot:
        await ctx.send("You can't steal from bots.")
        return

    # Cooldown (30 sec)
    now = time.time()
    if ctx.author.id in cooldowns:
        if now - cooldowns[ctx.author.id] < 30:
            await ctx.send("⏳ Wait before stealing again.")
            return

    cooldowns[ctx.author.id] = now

    braincoins.setdefault(ctx.author.id, 0)
    braincoins.setdefault(member.id, 0)

    if braincoins[member.id] <= 0:
        await ctx.send("They have no BrainCoins to steal.")
        return

    success = random.randint(1, 100)

    if success <= 50:
        stolen = random.randint(1, min(50, braincoins[member.id]))
        braincoins[member.id] -= stolen
        braincoins[ctx.author.id] += stolen
        await ctx.send(f"🧠 SUCCESS! You stole **{stolen} BrainCoins** from {member.mention}")
    else:
        lost = random.randint(1, 20)
        braincoins[ctx.author.id] -= lost
        await ctx.send(f"💀 You got caught! You lost **{lost} BrainCoins**")

daily_claim = {}

@bot.command()
async def daily(ctx):
    now = time.time()

    if ctx.author.id in daily_claim:
        if now - daily_claim[ctx.author.id] < 86400:
            await ctx.send("⏳ You already claimed your daily BrainCoins.")
            return

    daily_claim[ctx.author.id] = now
    reward = random.randint(50, 150)

    braincoins.setdefault(ctx.author.id, 0)
    braincoins[ctx.author.id] += reward

    await ctx.send(f"🎁 You received **{reward} BrainCoins**!")

shop_items = {
    "shield": 200,
    "boost": 500,
    "vip": 1000
}

@bot.command()
async def shop(ctx):
    text = ""
    for item, price in shop_items.items():
        text += f"{item} - {price} BrainCoins\n"

    embed = discord.Embed(
        title="🛒 Brainrot Shop",
        description=text,
        color=discord.Color.green()
    )

    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx, item):
    item = item.lower()

    if item not in shop_items:
        await ctx.send("Item not found.")
        return

    braincoins.setdefault(ctx.author.id, 0)

    if braincoins[ctx.author.id] < shop_items[item]:
        await ctx.send("Not enough BrainCoins.")
        return

    braincoins[ctx.author.id] -= shop_items[item]
    await ctx.send(f"🛒 You bought **{item}**!")

@bot.command()
async def brainleaderboard(ctx):
    global braincoins
    
    if not braincoins:
        await ctx.send("No one has BrainCoins yet.")
        return

    sorted_users = sorted(braincoins.items(), key=lambda x: x[1], reverse=True)

    text = ""
    for i, (user_id, amount) in enumerate(sorted_users[:5], start=1):
        user = await bot.fetch_user(user_id)
        text += f"{i}. {user.name} - {amount} BrainCoins\n"

    embed = discord.Embed(
        title="🏆 BrainCoin Leaderboard",
        description=text,
        color=discord.Color.gold()
    )

    await ctx.send(embed=embed)

bot.run(TOKEN)