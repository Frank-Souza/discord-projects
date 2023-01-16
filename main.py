import discord
from discord.ext import commands
import random

token = "bot-token"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def rps(ctx, choice: str):
    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)
    if choice not in options:
        await ctx.send("Invalid choice! Please choose either rock, paper, or scissors.")
    elif choice == computer_choice:
        await ctx.send("It's a tie! We both chose {}.".format(choice))
    elif (choice == 'rock' and computer_choice == 'scissors') or (choice == 'paper' and computer_choice == 'rock') or (choice == 'scissors' and computer_choice == 'paper'):
        await ctx.send("You win! You chose {} and I chose {}.".format(choice, computer_choice))
    else:
        await ctx.send("I win! You chose {} and I chose {}.".format(choice, computer_choice))

@bot.command()
async def cf(ctx, choice: str):
    options = ['heads', 'tails']
    computer_choice = random.choice(options)
    if choice not in options:
        await ctx.send("Please choose heads or tails.")
    elif (choice == 'heads' and computer_choice == 'heads') or (choice == 'tails' and computer_choice == 'tails'):
        await ctx.send(f'Correct! The coin landed on {computer_choice}.')
    elif (choice == 'heads' and computer_choice == 'tails') or (choice == 'tails' and computer_choice == 'heads'):
        await ctx.send(f'Sorry! The coin landed on {computer_choice} and you chose {choice}.')

@bot.command()
async def helper(ctx):
    await ctx.send("Command List:\n rps: Choose rock, paper or scissors and see if you won\n cf: Choose heads or tails and see if you guess correctly\n flip: Picks a random name to flip a coin for you")

@bot.command()
async def flip(ctx):
    coinFlippers = ['Phil', 'Bill', 'John', 'Jill', 'Gregory', 'Gertrude']
    rFlipper = random.choice(coinFlippers)
    options = ['heads', 'tails']
    computer_choice = random.choice(options)
    await ctx.send(f'{rFlipper} flips you a coin and it lands on {computer_choice}')

bot.run(token) 
 