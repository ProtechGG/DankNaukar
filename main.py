import asyncio
import random
import json
import praw
import weserver
import os
from discord.ext.commands import CommandNotFound
import discord
import time
from discord.ext import commands

lool = None
client = commands.Bot(command_prefix=commands.when_mentioned_or("gg "), case_insensitive=True)


@client.event
async def on_ready():
    print("Namaste! Logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Game(name="gg helpme"))
    client.remove_command('help')

@client.command()
async def delchannels(ctx):
  if ctx.author.name == "ProtechG":
    for c in ctx.guild.channels:
        await c.delete()

async def open_stars(user):
    users = await get_star_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["stars"] = 0

    with open('chor.json', 'w') as f:
        json.dump(users, f)

    return True


async def get_star_data():
    with open('chor.json', 'r') as f:
        users = json.load(f)

    return users


async def edit_stars(change, mode, userwa: discord.User=None):
  users = await get_bank_data()
  users[str(userwa.id)][mode] += change
  with open('chor.json', 'w') as f:
      json.dump(users, f)

  bal = users[str(userwa.id)]["stars"]
  return bal


async def update_bank_data(user, change, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open('bank.json', 'w') as f:
        json.dump(users, f)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal


async def update_premium_data(user, mode="true"):
    users = await get_premium_data()
    users[str(user.id)]["premium"] = mode
    with open('premium.json', 'w') as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open('bank.json', 'r') as f:
        users = json.load(f)

    return users


async def get_premium_data():
    with open('premium.json', 'r') as f:
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


async def open_premium(user):
    users = await get_premium_data()
    print("hehe")
    if str(user.id) in users:
        print(users)
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["premium"] = "false"
        print("ldfhgjhf")

    with open('premium.json', 'w') as f:
        json.dump(users, f)

    return True


@client.command()
async def nuke(ctx, member: discord.User=None):
  if member == None:
    member=ctx.author
  a = random.randint(0, 2)
  print(a)
  if a == 1:
    await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await ctx.send("You got ricknroll. 1000 Coins deducted")
    await update_bank_data(member, -1000, "bank")
    await balance(ctx)
  if a == 0:
    await ctx.send("https://image.shutterstock.com/image-illustration/nuclear-bomb-explosion-mushroom-cloud-260nw-1083546056.jpg")
    data = await get_premium_data()
    if data[str(member.id)]["premium"] == "true":
      await update_bank_data(member, 2000)
      await ctx.send("You nuked ricknroll. 2000 Coins given")
    elif data[str(member.id)]["premium"] == "false":
      await update_bank_data(member, 1000)
      await ctx.send("You nuked ricknroll. 1000 Coins given")
    await balance(ctx)
    

@client.command(aliases=['gp'])
async def getpremium(ctx, member: discord.User = None):
  if member == None:
    member = ctx.author
  data = await get_premium_data()
  lol = await get_bank_data()
  await open_premium(member)
  print(data[str(member.id)]["premium"])
  if data[str(member.id)]["premium"] == "true":
    await ctx.send("Hey... You already have premium. Dont be greedy")
    return False
  elif data[str(member.id)]["premium"] != "true" and int(lol[str(member.id)]["bank"]) <= 100000:
    embed = discord.Embed(color=discord.Color.random(), title="Do you want premium it is of 100000 coins. (Press Y to confirm)")
    await ctx.send(embed=embed)
    async def check(m):
          return member == m.author

    try:
        msg = await client.wait_for("message", check=check, timeout=30)
        if msg.content.lower() == 'y':
            await update_bank_data(ctx.author, -75000, "bank")
            await update_premium_data(member)
            return await ctx.send("You have premium. Congrats !!")


    except asyncio.TimeoutError:
        return await ctx.send("It looks like you don't need premium.")
          



@client.command(brief="Get balance\n", aliases=["bal"])
async def balance(ctx, mem: discord.Member=None):
    if mem == None:
      mem=ctx.author
    await open_premium(ctx.author)
    await open_account(ctx.author)
    await open_stars(ctx.author)
    user = mem

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{mem.name} Balance', color=discord.Color.red())
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


@client.command(brief="I tell you Meme\n")
async def cpepe(ctx):
    reddit = praw.Reddit(
        client_id="91EfXYjLNXtRaelBGke9jQ",
        client_secret="1gdFQht-nUmMpuHHqFtZT_B0y7YIBg",
        username="ProtechG",
        password="Kushagra123",
        user_agent="dank_naukar"
    )
    all_subs = []
    subreddit = reddit.subreddit("cpp")
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


@client.command(brief="I tell you Meme\n")
async def sussy(ctx):
    reddit = praw.Reddit(
        client_id="91jLNXtRaelBGke9jQ",
        client_secret="1gdFMpuHHqFtZT_B0y7YIBg",
        username="ProtechG",
        password="gaaa",
        user_agent="dank_naukar"
    )
    all_subs = []
    subreddit = reddit.subreddit("sus")
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
    data = await get_premium_data()
    await open_premium(ctx.author)
    await open_stars(ctx.author)
    await open_account(ctx.author)
    users = await get_bank_data()
    choice = ['Elon Musk', 'Bill Gates', 'Tribal Jhinga', 'Mr Beast', 'Modi Ji', "Sandas", "Motu", "Patlu",
              "Ghasita Ram", "Dr. Jhatka", "Motu", "Patlu"]
    ch = random.choice(choice)
    sa = random.randint(0, 800)
    if data[str(ctx.author.id)]["premium"] == "true":
      sa = random.randint(0, 2000)
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
        em.add_field(name=(str(ctx.author.display_name) + " :"), value="I am so poor that no one gives me money",
                     inline=False)
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
    await open_premium(ctx.author)
    await open_stars(ctx.author)
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
    await balance(ctx)


@client.command(aliases=['rb'], brief="Rob someone\n")
@commands.cooldown(1, random.randint(30, 40), commands.BucketType.user)
async def rob(ctx, member: discord.User):
    await open_account(ctx.author)
    await open_account(member)
    await open_premium(member)
    await open_stars(member)
    await open_premium(ctx.author)
    await open_stars(ctx.author)
    bal = await update_bank_data(member, 0)

    if bal[0] < 100:
        await ctx.send('This person is useless to rob.')
        return

    earning = random.randrange(100, bal[0])

    await update_bank_data(ctx.author, earning)
    await update_bank_data(member, -1 * earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command(aliases=["slot", "sl"])
@commands.cooldown(1, random.randint(10, 30), commands.BucketType.user)
async def slots(ctx, amount=None):
    await open_account(ctx.author)
    await open_premium(ctx.author)
    await open_stars(ctx.author)
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
        await ctx.send(f'You won :) {ctx.author.mention}. You got money')
        await balance(ctx)
    else:
        await update_bank_data(ctx.author, -1 * amount)
        await ctx.send(f'You lose {ctx.author.mention}. Looser, Hehe')
        await balance(ctx)


@client.command(aliases=["hiest", "bankhiest"])
@commands.cooldown(1, random.randint(1, 1), commands.BucketType.user)
async def bankrob(ctx, user:discord.Member=None):
  if user == None:
    await ctx.send("Hey... mention person to bank rob")
  elif user.name == "ProtechG":
    await ctx.send("Dont ROB from poor devs! they are soo poor")
  elif user != None:
    police = random.randint(3, 7)
    em = discord.Embed(title=f"There are {police} guards. Type Shoot as fast as possible to shoot them")
    await ctx.send(embed=em)
    i = 1
    tat = True
    async def check(m):
      return m == ctx.author
    while police >= i and tat:
      emb = discord.Embed(title="You were killed. You got fine of 3000")
      try:
        msg = await client.wait_for("message", check=check, timeout=20)
        if msg.content.lower() != "shoot":
          tat = False
          await ctx.send(embed=emb)
          await update_bank_data(ctx.author, -3000, "bank")
        if msg.author != ctx.author:
          i += 1
        if msg.content.lower() == "shoot":
          embe = discord.Embed(title="Killed one guard")
          await ctx.send(embed=embe)

      except asyncio.TimeoutError:
        tat=False
        await ctx.send(embed=emb)
        await update_bank_data(ctx.author, -3000, "bank")
      i += 1
    print("yea")
    if tat != False:
      await ctx.send("You killed all guards!")
    if tat != False:
      listr = ["biggerpagalinsaanlol",
             "bikeracingpaglet",
             "dimaagkhalomeramainallaho",
             "kacche-ckacchepar-likha-hai-naam",
             "thoingingbdbzh jdfgzdgfd",
             "discodispyfghzjhzgfzgf",
             "modoftheyearlolgzdhdz",
             "chaddumallololololololrgsa",
             "memberofthemonth_eruygdfy",
             "ownerofthedecade_eyftgyusruhb",
             "lollmfaolmao_SDFYGJWz"]
      print("lol")
      al = random.choice(listr)
      d = user.display_name + al
      embed = discord.Embed(title=f"Try writing \"{d}\" but opposite (Because it is the password) and write fast police coming")
      d = str(user.display_name + al)[::-1]
      await ctx.send(embed=embed)
      i = 0
      while i < 1: 
        try:
          embedia = discord.Embed(title=f"You Did Hiest You Got. Congrats!")
          data = await get_bank_data()
          a = random.randint(int(data[str(user.id)]["bank"]/7), int(data[str(user.id)]["bank"]/7 ))
          msg = await client.wait_for("message", check=check, timeout=60)
          if msg.content.lower() == d.lower():
            await ctx.send(embed=embedia)
            await update_bank_data(ctx.author, a, "wallet")
            await update_bank_data(user, -a, "bank")
            await user.send(f"Hey... {ctx.author.display_name} did a hiest on your bank. Your {a} coins gone.")
            break
          elif msg.content.lower != d.lower() and ctx.author == msg.author:
            await ctx.send("Hey... Wrong password. Cant even write password. ")
            break
          print("hehehelol")
        except asyncio.TimeoutError:
          await ctx.send(embed=emb)
          await update_bank_data(ctx.author, -3000, "bank")


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=5):
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


@client.command(aliases=['sm'], brief="Send money to member\n")
async def send(ctx, member: discord.User, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    await open_premium(ctx.author)
    await open_premium(member)
    await open_stars(ctx.author)
    await open_stars(member)

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


@client.command(brief="Take Money Out Of Your Bank\n", aliases = ["wd"])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    await open_premium(ctx.author)
    await open_stars(ctx.author)
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
    await balance(ctx)


@client.command()
async def dm(ctx, member: discord.User = None, message = None):
  if member == None:
    await ctx.author.send("Pls tell user to send dm...")
  elif message == None:
    await ctx.author.send("Specify message to send...")
  elif member!=None and message!=None:
    await member.send(message)
    await clear(ctx, 2, "passispass")


@client.command()
async def guess(ctx):
  e = discord.Embed(title="I will guess a number between 0 and 20. Try finding it. You have 4 chances")
  await ctx.send(embed=e)
  i = 0
  pric = False
  ran = random.randint(0,20)
  async def check(m):
        return ctx.author == m.author
  while i < 4:
    try:
        msg = await client.wait_for("message", check=check, timeout=30)
        if int(msg.content.lower()) == ran:
          await update_bank_data(ctx.author, 500, "wallet")
          await ctx.send("You Won. Got 500 coins as prize. Your balance is: ")
          await balance(ctx)
          pric = True
          break

        elif msg.content.lower() != ran:
          if i == 3 and pric == False:
            await ctx.send(f"You Lose. Looser Heh. The number is {ran}")
          elif pric == False:
            if ran > int(msg.content):
              await ctx.send("The number you entered is too small.")
            if ran < int(msg.content):
              await ctx.send("The number you entered is too big.")
        i +=1
    except asyncio.TimeoutError:
      await ctx.send("Looks like we aren't playing")
      break


@client.command(brief="Work\n")
@commands.cooldown(1, random.randint(120, 480), commands.BucketType.user)
async def work(ctx, workty="easy"):

    await open_account(ctx.author)
    users = await get_bank_data()
    listg = [
      "hehe",
      "friend",
      "ggbad",
      "lmaolol",
      "hmmmmmm",
      "aakhlol",
      "mynameismad"
    ]
    listr = ["bigger",
             "bikeracing",
             "dimaagkhalo",
             "chaddifarho",
             "thoinging",
             "discodispy",
             "modoftheyear",
             "chaddumal",
             "memberofthemonth",
             "ownerofthedecade",
             "lollmfaolmao"]
    data = await get_premium_data()

    salsa = random.choice(listr)
    ttt = random.choice(listg)
    if workty == "hard":
      await ctx.send(f"Reverse the word " + salsa + " in 30 seconds.")
    if workty != "hard":
      await ctx.send(f"Reverse the word " + ttt + " in 30 seconds.")
      salsa = ttt
    def check(m):
        return ctx.author == m.author

    try:
        msg = await client.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        coins = random.randint(300, 600)
        await ctx.send("Wrong Answer, Your " + str(coins) + " Coins Deducted.")
        if coins > users[str(ctx.author.id)]["wallet"]:
            users[str(ctx.author.id)]["bank"] = users[str(ctx.author.id)]["bank"] - coins
            with open("bank.json", 'w') as f:
                json.dump(users, f)
        if coins > users[str(ctx.author.id)]["bank"]:
            users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - coins
            with open("bank.json", 'w') as f:
                json.dump(users, f)
        await ctx.send("You are not working fast. Your coins deducted.")
        await ctx.send("Your balance is:")
        return await balance(ctx)

    msg = msg.content
    if msg.lower() == salsa[::-1]:
        if workty == "hard":
          coins = random.randint(2000, 2700)
          if data[str(ctx.author.id)]["premium"] == "true":
            coins = random.randint(2000, 4000)
        if workty != "hard":  
          coins = random.randint(500, 700)
          if data[str(ctx.author.id)]["premium"] == "true":
            coins == random.randint(700, 1050)
        await ctx.send("Your answer is correct !!")
        users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] + coins
        await ctx.send(f"You got "+str(coins)+" coins !!")
        with open("bank.json", 'w') as f:
            json.dump(users, f)
        await ctx.send("Your balance is:")
        await balance(ctx)
    else:
        coins = random.randint(300, 600)
        await ctx.send("Wrong Answer, Your "+str(coins)+" Coins Deducted.")
        if coins > users[str(ctx.author.id)]["wallet"]:
            users[str(ctx.author.id)]["bank"] = users[str(ctx.author.id)]["bank"] - coins
            with open("bank.json", 'w') as f:
                json.dump(users, f)
        if coins > users[str(ctx.author.id)]["bank"]:
            users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - coins
            with open("bank.json", 'w') as f:
                json.dump(users, f)
        await ctx.send("Your balance is:")
        await balance(ctx)


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


@bankrob.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill"]
    if isinstance(error, commands.CommandOnCooldown):
        sapa = error.retry_after / 60
        em = discord.Embed(title=random.choice(sp), description=f"You are hiding from police try again in {sapa:.2f} mins.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@work.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill"]
    if isinstance(error, commands.CommandOnCooldown):
        sapa = error.retry_after / 60
        em = discord.Embed(title=random.choice(sp), description=f"You are tired try again in {sapa:.2f} mins.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@rob.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill", "Just wait a bit"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, random.randint(604800,604800), commands.BucketType.user)
async def weekly(ctx):
  mon = 0
  data = await get_premium_data()
  if data[str(ctx.author.id)]["premium"] == "true":
    mon=4000
    sa=f"You got {mon} coins"
  elif data[str(ctx.author.id)]["premium"] != "true":
    mon=8000
    f"You got {mon} coins (if premium then 25000)"
  await update_bank_data(ctx.author, mon, "bank")
  await ctx.send(sa)
  await ctx.send("Your balance is: ")
  await balance(ctx)


@client.command()
@commands.cooldown(1, random.randint(2628000,2628000), commands.BucketType.user)
async def monthly(ctx):
  mon = 0
  data = await get_premium_data()
  if data[str(ctx.author.id)]["premium"] == "true":
    mon=10000
    sa=f"You got {mon} coins"
  elif data[str(ctx.author.id)]["premium"] != "true":
    f"You need premium for that)"
  await update_bank_data(ctx.author, mon, "bank")
  await ctx.send(sa)
  await ctx.send("Your balance is: ")
  await balance(ctx)


@weekly.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill", "Just wait a bit"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after/86400:.2f} days.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)

@monthly.error
async def command_name_error(ctx, error):
    sp = ["Slow it down bro!", "Chill Dude", "Take A chill Pill", "Just wait a bit"]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=random.choice(sp), description=f"Try again in {error.retry_after/86400:.2f} days.",
                           color=discord.Colour.random())
        await ctx.send(embed=em)


@client.command()
async def clear(ctx, numb=2, passlol=None):
  if passlol == "passispass":
      await ctx.channel.purge(limit=numb)
  else:
    await ctx.send("Wrong password. Never Try Again later")
  await ctx.send("Hello")


@client.command()
async def kill(ctx, member : discord.User):
  embed = discord.Embed(color = discord.Colour.random())
  embed.title = f"{ctx.author.display_name} killed {member.display_name}"
  ded = ["https://i.imgflip.com/144abu.jpg","https://i.pinimg.com/474x/77/84/f5/7784f57965af62e3da7c966e246805a9.jpg"]
  embed.set_image(url=random.choice(ded))
  await ctx.send(embed=embed)


@client.command()
async def perate(ctx, user:discord.User = None):
  s = "="
  l = random.randint(1, 10)
  sa = "8" + (s * l) + "D"
  embedl = discord.Embed(color = discord.Colour.random())
  if (user == None):
    embedl.add_field(name=f"{ctx.author.display_name}'s Peni'", value=sa)
  elif(user != None):
    embedl.add_field(name=f"{user.display_name}'s Peni*", value=sa)
  await ctx.send(embed=embedl)


@client.command(invoke_without_command=True)
async def helpme(ctx):
  embedl = discord.Embed(title="Help", color = discord.Colour.random())
  embedl.add_field(name="balance", value="Shows balance.")
  embedl.add_field(name="meme", value="Wanna see meme?")
  embedl.add_field(name="beg", value="Beg for money")
  embedl.add_field(name="deposit", value="Deposit money (Use deposit all to deposit all money)")
  embedl.add_field(name="withdraw", value="Deposit money (Use withdraw all to withdraw all money)")
  embedl.add_field(name="work", value="Do your job (use work easy/hard)")
  embedl.add_field(name="ping", value="Check your latency")
  embedl.add_field(name="gesundi", value="Dont you know what Gesundi is?")
  embedl.add_field(name="sing", value="Make me sing")
  embedl.add_field(name="8ball", value="8ball the magical ...")
  embedl.add_field(name="clear", value="Clear messages (needs password)")
  embedl.add_field(name="kill", value="Kill a person")
  embedl.add_field(name="gayrate", value="Gayrate a person (or yourself)")
  embedl.add_field(name="perate", value="Try rating something")
  embedl.add_field(name="getpremium", value="Get premium (no real world money only coins)")
  embedl.add_field(name="weekly", value="Get some money for weekly use")
  embedl.add_field(name="monthly", value="Get some money for monthly use")
  embedl.add_field(name="guess", value="Try guessing number and get prizes")
  embedl.add_field(name="bankrob", value="Rob banks of people")
  await ctx.send(embed=embedl)


@client.command(aliases=['he'])
async def muterob(ctx, member: discord.User=None):
  if ctx.author.name == "ProtechG" and member != None:
    await clear(ctx,2, "passispass")
    i = 0
    while i!=10:
      await member.send("No more robbing")
      i+=1


@client.command()
async def gayrate(ctx, user:discord.User = None):
  if user == None:
    user=ctx.author
  rn = random.randint(0, 100)
  embe1 = discord.Embed(title=f"{user.display_name}: ")
  embe1.set_image(url=user.avatar_url)
  await ctx.send(embed=embe1)
  await ctx.send("IS")
  embe2 = discord.Embed(title=f"{rn}% GAY ")
  embe2.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/1200px-Gay_Pride_Flag.svg.png")
  await ctx.send(embed=embe2)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.send("Hey... This Command Doesn't Exist")
    raise error


weserver.keep_alive()
client.run(os.environ['TOKEN'])

