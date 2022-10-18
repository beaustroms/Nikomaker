from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
from discord_slash.utils.manage_commands import create_choice
import math
# Don't change this, this imports functions which are used below

def intersects(self, other):
    return not (self.top_right.x < other.bottom_left.x or self.bottom_left.x > other.top_right.x or self.top_right.y < other.bottom_left.y or self.bottom_left.y > other.top_right.y)

def percentgen(num1, num2):
  return((num1/num2))

# \/ copied from https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd \/
def get_text_dimensions(text_string, font):
    try:
      #print(text_string)
      text_string = str(text_string)
      # https://stackoverflow.com/a/46220683/9263761
      ascent, descent = font.getmetrics()

      text_width = font.getmask(text_string).getbbox()[2]
      text_height = font.getmask(text_string).getbbox()[3] + descent

      return (text_width, text_height)
    except:
      return(0, 0)

# function to wrap characters individually, will cut words in two
def bettertextwrap(text, size):
  text = text.replace('\n', '')
  font = ImageFont.truetype('/home/runner/Nikomaker-tester/Font/Terminus (TTF) Bold 700.ttf', 25)
  currentsize = 0
  outlist = []
  # define variables, import the font, remove newlines in input
  for i in range(len(text)):
      try:
        width, height = get_text_dimensions(text[i], font)
        currentsize, x = get_text_dimensions(text[:i], font)
        currentsize -= 7
        # -7 to let size be a nice, easily computed number
      except Exception as e: 
        pass
      try:
        width, height = get_text_dimensions(text[i], font)
      except:
        pass
      if currentsize > size:
        outlist.append(text[:i-1])
        text = text[i-1:]
        currentsize = 0
        size = 400
        # reset values when list entry is added, not sure on why I added size = 400, looks ugly will clean up later
  outlist.append(text)
  return(outlist)

# function to create a textbox using above functions. Outputs PIL image
def maketextbox(text, expression, wrap=35):
  fontsize = 25
  font = ImageFont.truetype('/home/runner/Nikomaker-tester/Font/Terminus (TTF) Bold 700.ttf', fontsize)
  # load the font, you can remove Bold and change 700 to 500 for non bold text. 35 is the font size.
  text_width, text_height = get_text_dimensions(text, font)
  #text = textwrap.wrap(text, width=wrap, break_long_words=True)
  
  # Rewriting this logic. New logic: Check if vertical size is greater than textbox size (magic numbers will be used I'm sorry), if yes, find how much bigger it is (divide by textbox size) then divide the font scale by the result.
  originaltext = text
  text = textwrap(text, 400, fontsize)
  height = len(text)*((26*fontsize)/25)
  print(height, len(text))
  if height > 100:
    
    incsize = (height/100)
    fontsize = math.floor((fontsize / (incsize))*math.sqrt(height/100))
    print(fontsize, incsize)
    font = ImageFont.truetype('/home/runner/Nikomaker-tester/Font/Terminus (TTF) Bold 700.ttf', fontsize)
    text = textwrap(originaltext, 400, fontsize)
    print(math.sqrt(height/100))
    # im so sorry ^
  # 21 is the default character height for this font, 25 is the default font size.
  # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
  textbox = Image.open('Textbox.png').convert('RGBA')
  editbox = ImageDraw.Draw(textbox)
  text = '\n'.join(text)
  text_width, text_height = get_text_dimensions(text, font)
  editbox.text((20, 15), text, font=font, fill=(255, 255, 255))
  nikoimgface = Image.open(f'/home/runner/Nikomaker-tester/Niko_expressions/{expression}').convert('RGBA')
  nikoimgface = nikoimgface.resize((96, 96))
    
  nikoimgface = Image.open(f'/home/runner/Nikomaker-tester/Niko_expressions/{expression}').convert('RGBA')
  nikoimgface = nikoimgface.resize((96, 96))
  textbox.paste(nikoimgface, (496, 15), nikoimgface)
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
  progressbar = "[□□□□□□□□□□□]"
  for i in range(len(text)):
    if i % (len(text)/11) == 0:
      progressbar = progressbar.replace(">", "■", 1)
      progressbar = progressbar.replace("□", ">", 1)
      print(text+progressbar, end = "\r")
      os.system('clear')
    try:
      new_frame = maketextbox(text[:i], expression, 35)
      frames.append(new_frame)
    except Exception as e:
      print(e)
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

def textwrap(text, size, fontsize=25):
  text = text.replace('\n', '')
  font = ImageFont.truetype('/home/runner/Nikomaker-tester/Font/Terminus (TTF) Bold 700.ttf', fontsize)
  text = text.split()
  outtext = ""
  newlinecount = 1
  outlist = []
  # removes newlines from the entered text, splits it into a list of words. Also loads the Oneshot font (Terminus (TTF) Bold 700)
  for i in enumerate(text):
    e = i[1]
    successful = False
    breakcount = 0
    while not successful:
      if get_text_dimensions(e, font)[0] > size:
        outtext = outtext + ("\n".join(bettertextwrap(e, size)))
      if (get_text_dimensions(outtext, font)[0] + get_text_dimensions(e, font)[0]) < size:
        #print("1")
        if breakcount > 0:
          #print("a")
          while breakcount > 0:
            outtext = outtext+e[-breakcount]+" "
            breakcount -= 1
            #print("b")
          successful = True
          #print("c")
        else: 
          successful = True
          outtext = outtext+e+" "
        newlinecount += 1
      else:
        #print("2")
        outlist.append(outtext)
        outtext = ""
        successful = False
    #print("\n".join(outlist))
  outlist.append(outtext)
  return(outlist)
  # Logic: Split text into list, check each value of list and make sure it is not larger than size, split off x letters to make it fit if needed. Iterate over list, check to ensure that sizeOf(string + new entry) is not larger than size, if it is larger add newline, if it is not append it.

def terminaloutput(*args):
  ('-----------------------------------------')
  for i in args:
    (i)
  ('-----------------------------------------')