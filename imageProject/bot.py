import discord
from PIL import Image, ImageDraw, ImageFont
import re

TOKEN = "OTc3ODUwNTQzOTIzOTI5MTc4.GclaWb.x-nGYjw2BG3bkthvsVqeokGys8YJnyjUyQMyVU"

client = discord.Client()

#makes the image for template 1
def make_image1(top_text:str, bottom_text=''):
    im = Image.open("./picture.png")
    width, height = im.size
    font = ImageFont.truetype("./impact.ttf", int(height*0.15))
    outline =ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", int(height*0.1)+3)
    top_text = top_text.upper()
    d = ImageDraw.Draw(im)

    def new_lines (text, width, font, draw):
            if not text:
                return
            lo = 0
            text= text.upper()
            hi = len(text)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                t = text[:mid]
                w, h = draw.textsize(t, font=font)
                if w <= width-(width*0.05):
                    lo = mid
                else:
                    hi = mid - 1
            t = text[:lo]
            w, h = draw.textsize(t, font=font)
            yield t, w, h
            yield from new_lines(text[lo:], width, font, draw)

    lines = list(new_lines(top_text, width, font, d))
    #only executes if bottom text isnt empty

    bottom_text = bottom_text.upper()
    y_bottom = int(height*1.14)
    lines_bottom = list(new_lines(bottom_text, width, font, d))
    
    # adjusts the height of the top line of text and then proceeds to lower the height each line
    for t,w,h in lines_bottom:
        y_bottom -= h
    for t1,w2,h in lines_bottom:
        d.text((int(width/2), y_bottom), t1, outline="black",fill="white",stroke_width= int(height*0.15*0.1), stroke_fill="black", anchor="ms", font=font)
        y_bottom += h


    y= int(height*0.13)
    
    for t,w,h in lines:
        d.text((int(width/2), y), t, outline="black",fill="white", stroke_width= int(height*0.15*0.1), stroke_fill="black", anchor="ms", font=font)
        y+= h
    im.save("newpic.png")
    print("success!")

#gets an image if there is a reply  and if the reply has an image it gets the image
async def get_image(message):
    user_message = str(message.content)
    #testing out the reply functions
    if message.reference != None:
        ref = message.reference.message_id
        reply = await message.channel.fetch_message(ref)
        if len(reply.attachments) != 0:
            image = reply.attachments[0]
            await image.save("picture.png")

            limits = re.compile(r"'")
            matches = limits.finditer(user_message)
            points=[]
            bot_text = ''
            top_text = ''
            i=0

            for match in matches:
                if i%2 == 0:
                    points.append(match.end())
                else:
                    points.append(match.start())
                i += 1
            if len(points) == 2:
                top_text = user_message[points[0]:points[1]]
                make_image1(top_text)
                await message.channel.send(file=discord.File("./newpic.png"))
                return
            elif len(points) == 4:
                top_text = user_message[points[0]:points[1]]
                bot_text = user_message[points[2]:points[3]]
                make_image1(top_text, bot_text)
                await message.channel.send(file= discord.File('./newpic.png'))
                return
            else:
                await message.channel.send("invalid format for template1 (k! template1 '{top text}' '{bottom text}(optional)')")
                return
        elif len(reply.attachments > 1):
            await message.channel.send("the message that you reply to needs to have only 1 image")
            return
        else:
            await message.channel.send("reply needs to have an image")
    else:
        await message.channel.send("you need to reply to an image")
        return

@client.event
async def  on_ready():
    print("we have logged in as user {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    userMessage = message.content
    picture = []
    key= message.id
    channel = str(message.channel.name)
    
    print(f'{username}: {userMessage} id:{key} ({channel})')


    if message.author == client.user:
        return

    if message.channel.name == "general":
        if user_message.lower() == "k! hello":
            await message.channel.send(f'hello, {username}')
            return
        elif user_message.lower() == "kys":
            await message.channel.send(f"i'm afraid i can't do that {username}")
            return
        elif user_message.lower()[:12] == "k! template1":
            await get_image(message)
            print(user_message[12])
            
client.run(TOKEN)