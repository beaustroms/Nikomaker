from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
# Don't change this, this imports functions which are used below


def maketextbox(text, expression):
  fontshot = ImageFont.truetype('/home/runner/Nikomaker/Font/Terminus (TTF) Bold 700.ttf', 30)
  # load the font, you can remove Bold and change 700 to 500 for non bold text. 30 is the font size.
  text = textwrap.wrap(text, width=35)
  # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
  textbox = Image.open('Textbox.png').convert('RGBA')
  editbox = ImageDraw.Draw(textbox)
  text = ', '.join(text)
  text = text.replace(', ', '\n')
  editbox.text((20, 15), text, font=fontshot, fill=(255, 255, 255))
  
  nikoimgface = Image.open(f'/home/runner/Nikomaker/Niko_expressions/{expression}').convert('RGBA')
  nikoimgface = nikoimgface.resize((96, 96))
  textbox.paste(nikoimgface, (495, 15), nikoimgface)
  return(textbox)

def makewhitetransparent(img):
  img = Image.open(img)
  imga = img.convert("RGBA")
  datas = imga.getdata()
  newData = []
  for item in datas:
      if item[0] == 255 and item[1] == 255 and item[2] == 255:
          newData.append((255, 255, 255, 0))
      else:
          newData.append(item)
  img.putdata(newData)
  img.save("Textbox.png", "PNG")

def genchoices():
  returnlist = []
  for i in os.listdir('Niko_expressions'):
    returnlist.append(
      create_choice(
        name = (i.replace('.png', '').replace('_', ' ')),
        value = i,
    ))
  return(returnlist)

def entitytoworldmachine(directory):
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
      newname = f.replace('en_', 'TWM_')
      os.rename(f, newname)