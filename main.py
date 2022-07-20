import functions
import os
import discord
from discord.ext import commands  # pip install git+https://github.com/rapptz/discord.py
from discord import app_commands
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask("")


@app.route("/")
def home():
    return "<h1>Nikomaker (WIP)</h1>"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()


# app.py


nikoface = "niko_neutral.png"
nikotext = "asdf"

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=discord.Intents.default(),
    help_command=None,  # wont be needing that
)


@bot.event
async def on_ready():
    print("bot up")


@bot.hybrid_command(
    name="textbox",
    description="Puts your message in a Oneshot style textbox with the character/expression of your choosing",
)
@app_commands.describe(text="The text to be put into the textbox")
@app_commands.describe(
    expression="The expression you would like at the end of the textbox"
)
@app_commands.describe(animated="If you would like the text to be gradually read out.")
@app_commands.autocomplete(expression=functions.genchoices)
async def textbox(
    ctx: commands.Context, text: str, expression: str, animated: bool = False
):
    await ctx.defer()
    if animated:
        await functions.makeanimatedtextbox(text, expression, ctx.author)
        newimg = "drafts/animateddraft.gif"
        await ctx.interaction.followup.send(file=discord.File(newimg))
    else:
        (await functions.maketextbox(text, expression, 35, ctx.author)).save(
            "drafts/draft.png"
        )
        newimg = "drafts/draft.png"
        await ctx.interaction.followup.send(file=discord.File(newimg))


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    """Sync the commands to the api
    DO NOT DO THIS AUTOMATICALLY!"""
    await bot.tree.sync()
    await ctx.reply("Synced!")


# @client.event
# async def on_ready():
# createflasksite()

# print(commands.bot.is_ws_ratelimited())

# if not commands.bot.is_ws_ratelimited():
# else:
# print('The bot is currently being ratelimited, please wait warmly...')
bot.run(os.environ["token"])
# note for people viewing source: this is a bot in the testing server, don't mind it client.run('OTc0NjYxNzI4NTE4NDE0NDM3.G8C-QY.VP-Df_QY_ZQ1puU0se0JK_09zshm7b4BPKXARo')
