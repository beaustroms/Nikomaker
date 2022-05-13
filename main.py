import functions
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


nikoface = 'niko_neutral.png'
nikotext = 'asdf'

# Edit above ^ not below \/

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

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
    )
  ]
)



async def _textbox(ctx:SlashContext, text:str, expression:str):
  functions.maketextbox(text, expression).save('drafts/draft.png')
  await ctx.send(file=discord.File('drafts/draft.png'))


client.run(os.environ['token'])