import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8Ball", "eightball"])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")



    @commands.command(aliases=["rockpaperscissors"])
    async def rps(self, ctx):
        rps_selections = ["rock", "paper", "scissors"]
        await ctx.send(f"Rock, paper or scissors? Choose wisely...")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in rps_selections

        user_choice = ((await self.client.wait_for("message", check=check)).content).lower()

        comp_choice = random.choice(rps_selections)

        if user_choice == 'rock':
            if comp_choice == 'rock':
                await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'paper':
            if comp_choice == 'scissors':
                await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'rock':
                await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")


    @commands.command()
    async def insult(self, ctx, member: discord.Member):
        insults_list = ["Your face makes onions cry.",
                        "Don’t be ashamed of who you are. That’s your parents’ job.",
                        "I thought of you today. It reminded me to take out the trash.",
                        "Is your ass jealous of the amount of shit that comes out of your mouth?",
                        "Your birth certificate is an apology letter from the condom factory.",
                        "Life is full of disappointments, and I just added you to the list."
                        ]
        if member != ctx.author:
            await ctx.send(f"{member.mention} {random.choice(insults_list)}")
        else:
            await ctx.send(f"why u insult urself lol")

def setup(client):
    client.add_cog(Fun(client))
