import os
import discord
import requests
import random
from replit import db
from keep_web_alive import keep_alive

client = discord.Client()
my_secret = os.environ['TOKEN']
my_words = ["!p", "!", "Hola", "Perro", '$af']
db["random_quotes"] = [
    "Everyone wants happiness, no one wants pain, but you can have a sunshine without a bit of rain",
    "When you have gone as deep as you can go, the good thing is you can only go higher"
]


def get_quote(number: int) -> str:

	if (number == 1):
		msg = (requests.get("https://www.affirmations.dev/").json().get(
		    "affirmation"))
		print("1")
	elif (number == 2):
		msg = requests.get("https://zenquotes.io/api/random").json()[0].get(
		    "q")
		print("2")
	return msg


def update_random(quote: str):
	if ("random_quotes" in db.keys()):
		random_quotes = db["random_quotes"]
		random_quotes.append(quote)
		db["random_quotes"] = random_quotes
	else:
		db["random_quotes"] = list(random_quotes)


def delete_random(index: int = 0):
	random_quotes = db["random_quotes"]
	if (len(random_quotes) > index):
		quote = random_quotes[index]
		del random_quotes[index]
		db["random_quotes"] = random_quotes
		return quote


@client.event
async def on_ready():
	print("This '{0.user}' bot is now ready to start".format(client))


@client.event
async def on_message(message: discord.Message):
	if (message.author == client.user):
		return
	if (message.content.split(" ", 1)[0] in my_words):
		msg = get_quote(random.choice(list(range(1, 3))))
		print(msg)
		await message.channel.send(msg)
	elif (message.content.startswith("random_quote")):
		await message.channel.send(random.choice(db["random_quotes"]))
	elif message.content.startswith(".add"):
		db["random_quotes"].append(message.content.split(".add ", 1)[1])
		await message.channel.send("Your quote was added\n" +
		                           random.choice(db["random_quotes"]))
	elif message.content.startswith(".del"):
		try:
			index = int(message.content.split(".del ", 1)[1])
		except:
			index = 0
		quote = delete_random(index)
		await message.channel.send("The quote {quote} was deleted\n".format(
		    **locals()) + random.choice(db["random_quotes"]))


keep_alive()
client.run(my_secret)