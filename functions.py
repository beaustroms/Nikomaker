from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import os
from discord_slash.utils.manage_commands import create_choice
import math
# Don't change this, this imports functions which are used below

def percentgen(num1, num2):
  return((num1/num2))

# \/ copied from https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd \/
def get_text_dimensions(text_string, font):
    text_string = str(text_string)
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def bettertextwrap(text, font, size):
  currentsize = 0
  outlist = []
  for i in range(len(text)):
    width, height = get_text_dimensions(i, font)
    currentsize += width
    if currentsize > size:
      outlist.append(text[:i-1])
      text = text[i:]
      currentsize = width
  return(outlist)

def maketextbox(text, expression, wrap=35):
  fontsize = 25
  if len(text) > 100:
    percent = percentgen(100, len(text))
    fontsize = math.floor((fontsize*percent)*(2))
    wrap = round((wrap/(percent)*1.3)/2)
  if fontsize > 25:
    fontsize = 25
  fontshot = ImageFont.truetype('/home/runner/Nikomaker/Font/Terminus (TTF) Bold 700.ttf', fontsize)
  # load the font, you can remove Bold and change 700 to 500 for non bold text. 35 is the font size.
  text_width, text_height = get_text_dimensions(text, fontshot)
  text = textwrap.wrap(text, width=wrap, break_long_words=True)
  # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
  textbox = Image.open('Textbox.png').convert('RGBA')
  editbox = ImageDraw.Draw(textbox)
  newlinecount = len(text)+1
  text = '\n'.join(text)
  text_width, text_height = get_text_dimensions(text, fontshot)
  
  if newlinecount > 5:
    img = Image.new('RGBA', ((450, text_height*newlinecount)), (255, 0, 0, 0))
    imgedit = ImageDraw.Draw(img)
    imgedit.text((0, 0), text, font=fontshot, fill=(255, 255, 255))
    img.save('drafts/unshifttextimg.png', 'PNG')
    img = img.resize((500, 100), Image.ANTIALIAS)
    textbox.paste(img, (20, 15), img)
    img.save('drafts/textimg.png', 'PNG')

  else:
    # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
    textbox = Image.open('Textbox.png').convert('RGBA')
    editbox = ImageDraw.Draw(textbox)
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



def makeanimatedtextbox(text, expression):
  frames = []
  durations = []
  for i in range(len(text)):
    try:
      new_frame = maketextbox(text[:i], expression, 25)
      frames.append(new_frame)
    except:
      pass
  frames.append(maketextbox(text, expression))
  for i in frames:
    durations.append(50)
  durations[-1] = 4500
  frames[0].save('drafts/animateddraft.gif', format='GIF',
               append_images=frames[1:], save_all=True, duration=durations, loop=0)

def createflasksite():
  from flask import Flask

  app = Flask(__name__)

  @app.route('/')
  def index():
    return '<h1>Nikomaker (WIP)</h1>'

  if __name__ == '__main__':
    app.run(host='0.0.0.0')

def terminaloutput(*args):
  print('-----------------------------------------')
  for i in args:
    print(i)
  print('-----------------------------------------')

