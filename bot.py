print("Script has started executing...")
print("Bot file is running...")

import os
import discord
import random
import re
import time
from datetime import timedelta
from collections import defaultdict
from discord.ext import commands

# ================== TOKEN ==================
token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN environment variable is missing!")

# ================== INTENTS ==================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

# ================== DATA ==================
braincoins = defaultdict(int)
daily_claim = {}
sniped_messages = defaultdict(list)

bad_words = {
    "fuck","shit","bitch","asshole","bastard",
    "dick","slut","whore","retard","nigger",
    "faggot","cunt","motherfucker"
}

shop_items = {
    "shield": 200,
    "boost": 500,
    "vip": 1000
}

# ================== EVENTS ==================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is fully online.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    words = message.content.lower().split()

    if any(word in bad_words for word in words):
        await message.delete()
        await message.channel.send(
            f"{message.author.mention}, watch your language!",
            delete_after=5
        )
        return

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    sniped_messages[message.channel.id].append({
        "content": message.content,
        "author": str(message.author),
        "avatar": message.author.display_avatar.url
    })

    if len(sniped_messages[message.channel.id]) > 5:
        sniped_messages[message.channel.id].pop(0)

# ================== ERROR HANDLER ==================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission for that.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Try again in {round(error.retry_after)} seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing required argument.")
    else:
        print(f"Unhandled error: {error}")

# ================== BASIC ==================
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm working 😄")

@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["Heads", "Tails"]))

# ================== ECONOMY ==================
@bot.command()
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"{member.mention} has **{braincoins[member.id]} BrainCoins**")

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def steal(ctx, member: discord.Member):
    if member.bot or member == ctx.author:
        return await ctx.send("Invalid target.")

    if braincoins[member.id] <= 0:
        return await ctx.send("They have no BrainCoins.")

    if random.randint(1, 100) <= 50:
        stolen = random.randint(1, min(50, braincoins[member.id]))
        braincoins[member.id] -= stolen
        braincoins[ctx.author.id] += stolen
        await ctx.send(f"You stole {stolen} BrainCoins!")
    else:
        loss = random.randint(1, 20)
        braincoins[ctx.author.id] = max(0, braincoins[ctx.author.id] - loss)
        await ctx.send(f"You got caught and lost {loss} BrainCoins.")

@bot.command()
async def daily(ctx):
    now = time.time()

    if ctx.author.id in daily_claim and now - daily_claim[ctx.author.id] < 86400:
        return await ctx.send("You already claimed daily.")

    reward = random.randint(50, 150)
    braincoins[ctx.author.id] += reward
    daily_claim[ctx.author.id] = now

    await ctx.send(f"You received {reward} BrainCoins!")

@bot.command()
async def shop(ctx):
    description = "\n".join(
        f"{item} - {price} BrainCoins"
        for item, price in shop_items.items()
    )
    embed = discord.Embed(title="Shop", description=description)
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    if not braincoins:
        return await ctx.send("No data yet.")

    top = sorted(braincoins.items(), key=lambda x: x[1], reverse=True)[:5]

    text = ""
    for i, (user_id, amount) in enumerate(top, 1):
        user = await bot.fetch_user(user_id)
        text += f"{i}. {user.name} - {amount}\n"

    embed = discord.Embed(title="Leaderboard", description=text)
    await ctx.send(embed=embed)

# ================== START ==================
bot.run(token)

