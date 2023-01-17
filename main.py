import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

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
    await ctx.send("Command List:\nrps: Choose rock, paper or scissors and see if you won\nflip: Picks a random name to flip a coin for you\nplay: Play a game of blackjack against Kings bot")

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
async def play(ctx):
    playerHand = rng() + rng()
    dealer = rng() + rng()
    options = ['hit', 'stand']
    await ctx.send(f'{playerHand} = player hand\n{dealer} = dealer hand\n Would you like to hit or stay?')
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    while response.content.lower() != options[1] and playerHand < 22:
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
    elif dealer > 21:
        await ctx.send("Dealer bust. Player wins")
    elif playerHand > dealer:
        await ctx.send(f'Player wins with a hand of {playerHand}')
    else:
         await ctx.send(f'Dealer wins with a hand of {dealer}')

bot.run(token) 
 
# think about reusability