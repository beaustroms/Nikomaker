import functions
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import flask



# app.py
def createflasksite():
  from flask import Flask

  app = Flask(__name__)

  @app.route('/')
  def index():
    return '<h1>Nikomaker (WIP)</h1>'

  if __name__ == '__main__':
    app.run(host='0.0.0.0')


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
      choices = [
        create_choice(
          value = 1,
          name = 'True'
        ),
        create_choice(
          value = 0,
          name = 'False'
        )
      ]
    )
  ]
)



async def _textbox(ctx:SlashContext, text:str, expression:str, animation:int):
  if animation == 0:
    functions.maketextbox(text, expression).save('drafts/draft.png')
  else:
    functions.makeanimatedtextbox(text, expression, 1)
  await ctx.send(file=discord.File('drafts/draft.png'))

#print(commands.bot.is_ws_ratelimited())

#if not commands.bot.is_ws_ratelimited():
#else:
  #print('The bot is currently being ratelimited, please wait warmly...')
client.run(os.environ['token'])
createflasksite()