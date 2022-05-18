import functions
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask('')

@app.route('/')
def home():
    return '<h1>Nikomaker (WIP)</h1>'

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()


# app.py


nikoface = 'niko_neutral.png'
nikotext = 'asdf'

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)


'''@slash.slash(
  name = 'reload',
  description = 'reload the bot',
)

async def _reload():
  await client.reload_extension(f"cogs.{'main.py'[:-3]}")'''


@slash.slash(
  name = 'textbox',
  description = 'Puts your message in a Oneshot style textbox with the character/expression of your choosing',
  options = [
    create_option(
      name = 'text',
      description = 'The text to be put in the textbox',
      option_type = 3,
      required = True,
    ),
    create_option(
      name = 'expression',
      description = 'The expression you would like at the end of the textbox',
      option_type = 3,
      required = True,
      choices = functions.genchoices()
    ),
    create_option(
      name = 'animated',
      description = 'If you would like the text to be gradually read out.',
      option_type = 5,
      required = False,
        )
      ]
    )


# , animated:int=0
async def _textbox(ctx:SlashContext, text:str, expression:str, animated:bool=False):
  displayvars = locals()
  del displayvars['ctx']
  animated = int(animated)
  animated = int(animated)
  print('---------------------------------------')
  print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), '\n\n', displayvars, '\n\n', ctx.author)
  print('----------------------------------------\n')
  if animated == 0:
    functions.maketextbox(text, expression).save('drafts/draft.png')
    newimg = 'drafts/draft.png'
    await ctx.send(file=discord.File(newimg))
  else:
    oldtime = datetime.now()
    await ctx.defer()
    functions.makeanimatedtextbox(text, expression)
    newtime = datetime.now()
    print(f'Took {newtime-oldtime} seconds')
    newimg = 'drafts/animateddraft.gif'
    await ctx.send(file=discord.File(newimg))
#@client.event
#async def on_ready():
  #createflasksite()

#print(commands.bot.is_ws_ratelimited())

#if not commands.bot.is_ws_ratelimited():
#else:
  #print('The bot is currently being ratelimited, please wait warmly...')
client.run(os.environ['token'])
#note for people viewing source: this is a bot in the testing server, don't mind it client.run('OTc0NjYxNzI4NTE4NDE0NDM3.G8C-QY.VP-Df_QY_ZQ1puU0se0JK_09zshm7b4BPKXARo')


