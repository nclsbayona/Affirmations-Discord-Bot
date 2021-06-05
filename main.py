import os
import discord
import requests
import random
from replit import db

client=discord.Client()
my_secret = os.environ['TOKEN']
my_words=["!p", "!", "Hola", "Perro", '$affirmation']
db["random_quotes"]=["Hoy es un gran díía para comenzar de nuevo", "Lo bueno de tocar fondo es que ya no puedes caer mas bajo"]

def get_quote(number: int) -> str:
  
    if (number==1): 
      msg= (requests.get("https://www.affirmations.dev/").json().get("affirmation")) 
    elif (number==2):
      msg=requests.get("https://zenquotes.io/api/random").json()[0].get("q")

    return msg

def update_random(quote:str):
  if ("random_quotes" in db.keys()):
    random_quotes=db["random_quotes"]
    random_quotes.append(quote)
    db["random_quotes"]=random_quotes
  else:
    db["random_quotes"]=list(random_quotes)

def delete_random(index: int):
  random_quotes=db["random_quotes"]
  if (len(random_quotes)>index):
    del random_quotes[index]
    db["random_quotes"]=random_quotes

@client.event
async def on_ready():
  print("This '{0.user}' bot is now ready to start".format(client))

@client.event
async def on_message(message: discord.Message):
  if (message.author==client.user):
    return
  elif (message.content.startswith(str(word) for word in my_words)):
    msg=get_quote(random.choice(list(range(1,3))))
    print (msg)
    await message.channel.send(msg)
  elif (message.content.startswith("random_quote")):
    await message.channel.send(random.choice(db["random_quotes"]))
  elif message.content.startswith(".add"):
    db["random_quotes"].append(message.content.split(".add ", 1)[1])
    await message.channel.send("Your quote was added\n"+random.choice(db["random_quotes"]))
  elif message.content.startswith(".del"):
    index=int(message.content.split(".del ", 1)[1])
    delete_random(index)
    await message.channel.send("The quote was deleted\n"+random.choice(db["random_quotes"]))

client.run(my_secret)
