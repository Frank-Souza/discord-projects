import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('DISC_DB'))
db = client["db01"]
collection = db["users"]


load_dotenv()
token = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def rps(ctx, choice: str):
    options = ['rock', 'paper', 'scissors']
    computerChoice = random.choice(options)
    if choice not in options:
        await ctx.send("Invalid choice! Please choose either rock, paper, or scissors.")
    elif choice == computerChoice:
        await ctx.send("It's a tie! We both chose {}.".format(choice))
    elif (choice == 'rock' and computerChoice == 'scissors') or (choice == 'paper' and computerChoice == 'rock') or (choice == 'scissors' and computerChoice == 'paper'):
        await ctx.send("You win! You chose {} and I chose {}.".format(choice, computerChoice))
    else:
        await ctx.send("I win! You chose {} and I chose {}.".format(choice, computerChoice))


@bot.command()
async def helper(ctx):
    await ctx.send("Command List:\nrps: Choose rock, paper or scissors and see if you won\nflip: Picks a random name to flip a coin for you\nplay: Play a game of blackjack against Kings bot\nme: Displays your username and soon other related information\nstats: Shows how many wins and losses you have in blackjack")

@bot.command()
async def flip(ctx):
    coinFlippers = ['Phil', 'Bill', 'John', 'Jill', 'Gregory', 'Gertrude']
    rFlipper = random.choice(coinFlippers)
    options = ['heads', 'tails']
    computerChoice = random.choice(options)
    await ctx.send(f'{rFlipper} flips you a coin and it lands on {computerChoice}')

def rng():
    return random.randint(2, 11)

@bot.command()
async def me(ctx):
    author = ctx.author
    await ctx.send(author)
    return author




@bot.command()
async def play(ctx):
    playerHand = rng() + rng()
    dealer = rng() + rng()
    options = ['hit', 'stand']
    win = 0
    loss = 0
    account = str(ctx.author)
    check = collection.find_one({"user": account})
    await ctx.send(f'{playerHand} = player hand\n{dealer} = dealer hand\n Would you like to hit or stay?')
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    while response.content.lower() != options[1] and playerHand < 21:
        if response.content.lower() != options[0]:
            await ctx.send("Please hit or stand.")
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        
        elif response.content.lower() == options[0] and playerHand < 22:
            playerHand += rng()
            if playerHand <21:
                await ctx.send(f"Hand is now {playerHand}. Hit or stand?")
                response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            else:
                await ctx.send(f"Hand is now {playerHand}.")
    if response.content.lower() == options[1] or playerHand > 21:
        await ctx.send(f'Player hand = {playerHand}')
    
    while dealer < 17:
        dealer += rng()
        await ctx.send(f'Dealer hits and hand is now: {dealer}')
    if playerHand > 21:
        await ctx.send("Player bust. Dealer wins")
        loss += 1
    elif dealer > 21:
        await ctx.send("Dealer bust. Player wins")
        win += 1 
    elif playerHand > dealer:
        await ctx.send(f'Player wins with a hand of {playerHand}')
        win += 1 
    else:
         await ctx.send(f'Dealer wins with a hand of {dealer}')
         loss += 1

    if check is None:
        collection.insert_one({"user": account, "win" : win, "loss" : loss})
    else:
        collection.find_one_and_update(
        {"user": account},
        {'$inc': {"win": win}}
        )
        collection.find_one_and_update(
        {"user": account},
        {'$inc': {"loss": loss}}
        )

@bot.command()
async def stats(ctx):
    account = str(ctx.author)
    check = collection.find_one({"user": account})
    if check is None:
        await ctx.send('You need to play a game first!')
    else:
        await ctx.send(f'Wins: {check["win"]}\nLosses: {check["loss"]}')


bot.run(token) 
 
# think about reusability