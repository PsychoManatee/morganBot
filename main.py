import discord
import os
import math
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from pathlib import Path
from webserver import keep_alive

dotenv_path = Path('local.env') #establishes specific bot
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents(messages=True, message_content=True, reactions=True, guilds=True) #sets permissions

client = discord.Client(intents=intents) #brings into discord

async def custom_image(message, custom_text):
    #font=ImageFont.truetype("Comic Story.ttf", 400/len(custom_text))
    a_length = len(custom_text)
    font_size = int((1/math.sqrt(a_length)) * 750)
    #text_position = (300 - (a_length * 5), 300 - ((100/math.sqrt(a_length))))  # (x, y) coordinates
    text_position = (300 - (1/font_size), 300 - ((100/math.sqrt(a_length))))
    text_color = (0, 0, 0)  # RGB color
    input_image = "yes.png"  #sets file names
    output_image = "output.png"
    img = Image.open(input_image)  #open file
    draw = ImageDraw.Draw(img)
    outline = (255, 255, 255)
    font=ImageFont.truetype("Comic Story.ttf", font_size)
    draw.text(text_position, custom_text, fill=text_color, font=font, outline=outline, stroke_width=20, stroke_fill=(255, 255, 255))
    img.save(output_image)
    with open(output_image, 'rb') as img_file:
        img = discord.File(img_file)
        await message.channel.send(file=img)

async def replace_space_with_newline(text):
    nth_spaces = [2, 6, 10]
    new_text = []
    space_count = 0
    line_start = 0
    
    for i, char in enumerate(text):
        if char == ' ':
            space_count += 1
            if space_count in nth_spaces:
                line = text[line_start:i]
                centered_line = line.center(len(line) + 2 * (space_count - 1))
                new_text.append(centered_line)
                new_text.append('\n')
                line_start = i + 1
    new_text.append(text[line_start:].center(len(text) - line_start + 2 * (space_count - 1)))
    return ''.join(new_text)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(discord.__version__)

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content.startswith("$meme"):
    await message.channel.send("peepeepoopoo")

  if message.content.startswith("$hmmyes"):
    text = message.content[len("$hmmyes")+1:].strip()
    if len(text) > 15:
      text = await replace_space_with_newline(text)
    await custom_image(message, text)
  
keep_alive()
client.run(os.getenv('TOKEN'))
#print(os.getenv('TOKEN'))