import random
import os
import json
import praw
import discord
from discord.ext import commands

coins = 0
client = commands.Bot(command_prefix=commands.when_mentioned_or("gg "), case_insensitive=True)


@client.event
async def on_ready():
    print("Namaste! Logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Game(name="gg help"))


async def update_bank_data(user, change, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open('bank.json', 'w') as f:
        json.dump(users, f)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal


async def get_bank_data():
    with open('bank.json', 'r') as f:
        users = json.load(f)

    return users


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('bank.json', 'w') as f:
        json.dump(users, f)

    return True


@client.command(brief="Get balance\n")
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance', color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance', value=bank_amt)
    await ctx.send(embed=em)


@client.command(brief="I tell you Meme\n")
async def meme(ctx):
    reddit = praw.Reddit(
        client_id="91EfXYjLNXtRaelBGke9jQ",
        client_secret="1gdFQht-nUmMpuHHqFtZT_B0y7YIBg",
        username="ProtechG",
        password="Kushagra123",
        user_agent="dank_naukar"
    )
    all_subs = []
    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit=random.randint(10, 50))
    for submission in top:
        print(submission.title)
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title=name)
    em.set_image(url=url)
    await ctx.send(embed=em)


@client.command(brief="Beg From People\n")
@commands.cooldown(1, random.randint(10, 30), commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    choice = ['Elon Musk', 'Bill Gates', 'Tribal Jhinga', 'Mr Beast', 'Modi Ji', "Sandas", "Motu", "Patlu", "Ghasita Ram", "Dr. Jhatka"]
    ch = random.choice(choice)
    sa = random.randint(0, 800)
    chagan = random.randint(0, 2)
    print(chagan)
    if chagan >= 1:
        await ctx.send(f"{ch}: Poor Beggar, Hey Beggar Take Some Coins.\n{ch} Gave You {sa} Coins.")
        users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] + sa
        print(users)
        with open("bank.json", 'w') as f:
            json.dump(users, f)

    else:
        em = discord.Embed()
        em.set_thumbnail(url=ctx.message.author.avatar_url)
        em.add_field(name=(str(ctx.author.display_name) + " :"), value="I am so poor that no one gives me money", inline=False)
        await ctx.send(embed=em)


@beg.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@client.command(brief="Put Money Into Your Bank\n", aliases=["dep"])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    bal = await update_bank_data(ctx.author, 0)
    if str(amount).lower() == 'all':
        wallet_amt = bal[0]
        await deposit(ctx, wallet_amt)
        return
    if amount is None:
        await ctx.send("What are you doing to your life.\nEnter amount to deposit")
        return

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send(f"Poor Person, You don't have enough money to deposit\nTrying to deposit {amount}"
                       + f" coins and you have {bal[0]} coins in wallet")
        return
    if amount <= 0:
        await ctx.send("People should be positive and amount must be positive.")
        return
    await update_bank_data(ctx.author, amount, "bank")
    await update_bank_data(ctx.author, -1 * amount, "wallet")
    await ctx.send(f"You deposited {amount}. Your current Balance Is:")
    await balance(ctx=ctx)


@client.command(aliases=['rb'])
@commands.cooldown(1, random.randint(10, 30), commands.BucketType.user)
async def rob(ctx, member: discord.User):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank_data(member, 0)

    if bal[0] < 100:
        await ctx.send('This person is useless to rob.')
        return

    earning = random.randrange(100, bal[0])

    await update_bank_data(ctx.author, earning)
    await update_bank_data(member, -1 * earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command()
@commands.cooldown(1, random.randint(10, 30), commands.BucketType.user)
async def slots(ctx, amount=None):
    await open_account(ctx.author)
    if amount is None:
        await ctx.send("Please enter the amount. You Idiot")
        return

    bal = await update_bank_data(ctx.author, 0)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('So poor. No money in wallet')
        return
    if amount < 0:
        await ctx.send('People should be positive and amount must be positive')
        return
    final = []
    for i in range(3):
        a = random.choice(['X', 'O', 'Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank_data(ctx.author, 2 * amount)
        await ctx.send(f'You won :) {ctx.author.mention}. Ypu got money')
        await balance(ctx)
    else:
        await update_bank_data(ctx.author, -1 * amount)
        await ctx.send(f'You lose {ctx.author.mention}. Looser, Hehe')
        await balance(ctx)


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} Richest People",
                       footer="This is decided by bank + wallet coins",
                       color=discord.Color.random())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = await client.fetch_user(id_)
        name = member
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@client.command(aliases=['sm'])
async def send(ctx, member: discord.User, amount=None):
    await open_account(ctx.author)
    await open_account(member)

    if ctx.author.id == member.id:
        await ctx.send("It seems that you are Idiot because you are sending yourself coins. Lol Idiot")
        return

    if amount is None:
        await ctx.send("What are you doing to your life. Tell amount to send")
        return

    bal = await update_bank_data(ctx.author, 0)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send(f"Poor Person, You don't have enough money to withdraw\nTrying to take {amount}"
                       + f" coins and you have {bal[0]} coins in wallet")
        return
    if amount < 0:
        await ctx.send('People should be positive and amount must be positive.')
        return

    await update_bank_data(ctx.author, -1 * amount, 'wallet')
    await update_bank_data(member, amount, 'wallet')
    await ctx.send(f'{ctx.author.mention} You sent {member.display_name} {amount} coins')
    await balance(ctx)


@client.command(brief="Take Money Out Of Your Bank\n")
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount is None:
        await ctx.send("What are you doing to your life.\nEnter amount to withdraw")
        return

    bal = await update_bank_data(ctx.author, 0)

    if str(amount).lower() == 'all':
        wallet_amt = bal[1]
        await withdraw(ctx, wallet_amt)
        return

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send(f"Poor Person, You don't have enough money to withdraw\nTrying to take {amount}"
                       + f" coins and you have {bal[1]} coins in bank")
        return
    if amount <= 0:
        await ctx.send("People should be positive and amount must be positive.")
        return
    await update_bank_data(ctx.author, amount)
    await update_bank_data(ctx.author, -1 * amount, "bank")
    await ctx.send(f"You withdrew {amount}. Your current Balance Is:")
    await balance(ctx=ctx)


@client.command(pass_context=True, brief='Say Me Hello :)\n')
async def hello(ctx):
    await ctx.send('GG, HELLO! I am Buffalo')


@client.command(pass_context=True, brief='Say Me Wassup.\n')
async def wassup(ctx):
    await ctx.send("GG. Nothing is Up, Wassup")


@client.command(pass_context=True, brief='Say Me Bye\n')
async def bye(ctx):
    await ctx.send("Don't say bye, because I want to say Hi\n")


@client.command(pass_context=True, brief='Say Me Sup.\n')
async def sup(ctx):
    await ctx.send("Sup, sup sup sup sup. Sup")


@client.command(brief="Work\n")
async def work(ctx, job):
    pass


@client.command(pass_context=True, brief='Say Me Hi.\n')
async def hi(ctx):
    await ctx.send("GG, Hi")


@client.command(pass_context=True, brief='Check your ping.\n')
async def ping(ctx):
    print('pong')
    await ctx.send(f'Pong!{round(client.latency * 1000)} ms')


@client.command(brief="Don't you know what GESUNDI is? It is a game by ProtechG\n")
async def gesundi(ctx):
    await ctx.send("Gesundi Yay, Just play It " +
                   format(ctx.author.display_name) +
                   " https://protechg.itch.io/gesundi")


@client.command(brief='I sing you a song\n')
async def sing(ctx):
    songs = [
        "Hi Hello Tata See You", "I am Don Bolo Kaun. I am Don.",
        "I am Dank Naukar I live on mars, When i come on earth I answer your questions or do comedy"
    ]

    await ctx.send(random.choice(songs), tts=True)


@client.command(
    aliases=['asknaukar', '8ball'],
    pass_context=True,
    brief='8ball, I will answer all you questions.\n')
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.", "IDK", "Up to You",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Question not clear. Try Again Later",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.", "Batlol",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful.",
        "Oh My God, Never Never, https://tenor.com/view/suicide-gif-14427950", "Oh God Please NO"
    ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


@slots.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@rob.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


client.run("ODgyOTMxNDcyMzk3Mzg1NzQ4.YTCkAw.LwBPxxdfo1-apOXAd63YQwg87JM")
