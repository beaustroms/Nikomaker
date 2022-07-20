import discord
from discord import app_commands
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import math
from io import BytesIO


# Don't change this, this imports functions which are used below


def intersects(self, other):
    return not (
        self.top_right.x < other.bottom_left.x
        or self.bottom_left.x > other.top_right.x
        or self.top_right.y < other.bottom_left.y
        or self.bottom_left.y > other.top_right.y
    )


def percentgen(num1, num2):
    return num1 / num2


# \/ copied from https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd \/
def get_text_dimensions(text_string, font):
    try:
        text_string = str(text_string)
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)
    except:
        return (0, 0)


"""def besttextwrap(text, font):
  text = str(text)
  ascent, descent = font.getmetrics()
  print(font.getmask(text).getbbox())"""


def bettertextwrap(text, size):
    text = text.replace("\n", "")
    fontshot = ImageFont.truetype("./Font/Terminus (TTF) Bold 700.ttf", 25)
    font = fontshot
    currentsize = 0
    outlist = []
    for i in range(len(text)):
        # try:
        try:
            width, height = get_text_dimensions(text[i], font)
            currentsize, x = get_text_dimensions(text[:i], font)
            currentsize -= 7
        except Exception as e:
            # print(e)
            pass
        try:
            width, height = get_text_dimensions(text[i], font)
        except:
            pass
        if currentsize > size:
            outlist.append(text[: i - 1])
            text = text[i - 1 :]
            currentsize = 0
            size = 400
    # except:
    # pass
    outlist.append(text)
    return outlist


async def maketextbox(text, expression, wrap=35, user: discord.User = None):
    avatar = False
    if expression == "avatar" and user is not None:
        expression = BytesIO(await user.display_avatar.read())
        avatar = True
    else:
        expression += ".png"
    fontsize = 25
    if len(text) > 100:
        percent = percentgen(100, len(text))
        fontsize = math.floor((fontsize * percent) * (2))
        wrap = round((wrap / (percent) * 1.3) / 2)
    if fontsize > 25:
        fontsize = 25
    fontshot = ImageFont.truetype("./Font/Terminus (TTF) Bold 700.ttf", fontsize)
    # load the font, you can remove Bold and change 700 to 500 for non bold text. 35 is the font size.
    text_width, text_height = get_text_dimensions(text, fontshot)
    # text = textwrap.wrap(text, width=wrap, break_long_words=True)
    text = bettertextwrap(text, 400)
    # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
    textbox = Image.open("Textbox.png").convert("RGBA")
    editbox = ImageDraw.Draw(textbox)
    newlinecount = len(text) + 1
    text = "\n".join(text)
    text_width, text_height = get_text_dimensions(text, fontshot)

    if newlinecount > 5:
        img = Image.new("RGBA", ((450, text_height * newlinecount)), (255, 0, 0, 0))
        imgedit = ImageDraw.Draw(img)
        imgedit.text((0, 0), text, font=fontshot, fill=(255, 255, 255))
        img.save("drafts/unshifttextimg.png", "PNG")
        img = img.resize((500, 100), Image.ANTIALIAS)
        textbox.paste(img, (20, 15), img)
        img.save("drafts/textimg.png", "PNG")

    else:
        # Wraps the text, lowering width wraps it earlier, increasing it wraps it later
        textbox = Image.open("Textbox.png").convert("RGBA")
        editbox = ImageDraw.Draw(textbox)
        editbox.text((20, 15), text, font=fontshot, fill=(255, 255, 255))
        if not avatar:
            nikoimgface = Image.open(f"./Niko_expressions/{expression}").convert("RGBA")
            nikoimgface = nikoimgface.resize((96, 96))
        else:
            nikoimgface = Image.open(expression).convert("RGBA").resize((96, 96))

    if not avatar:
        nikoimgface = Image.open(f"./Niko_expressions/{expression}").convert("RGBA")
        nikoimgface = nikoimgface.resize((96, 96))
    else:
        nikoimgface = Image.open(expression).convert("RGBA").resize((96, 96))
    textbox.paste(nikoimgface, (496, 15), nikoimgface)
    return textbox


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


async def genchoices(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name="avatar", value="avatar")] + [
        app_commands.Choice(name=file.split(".")[0], value=file.split(".")[0])
        for file in os.listdir("./Niko_expressions")
        if current.lower() in file.lower()
    ]


def entitytoworldmachine(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            newname = f.replace("en_", "TWM_")
            os.rename(f, newname)


async def makeanimatedtextbox(text, expression, user: discord.User = None):
    frames = []
    durations = []
    for i in range(len(text)):
        try:
            new_frame = await maketextbox(text[:i], expression, 35, user)
            frames.append(new_frame)
        except:
            pass
    frames.append(await maketextbox(text, expression, 35, user))
    for i in frames:
        durations.append(50)
    durations[-1] = 4500
    frames[0].save(
        "drafts/animateddraft.gif",
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=durations,
        loop=0,
    )


def createflasksite():
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "<h1>Nikomaker (WIP)</h1>"

    if __name__ == "__main__":
        app.run(host="0.0.0.0")


def terminaloutput(*args):
    print("-----------------------------------------")
    for i in args:
        print(i)
    print("-----------------------------------------")
