import os
import discord
from requests import get, Response
from discord.ext import commands, tasks
from random import randint
# from replit import db
from keep_web_alive import keep_alive

bot_token = os.environ['TOKEN']

channel_id = os.environ['CHANNEL']


class AffirmationsBot(commands.Bot):
    def __init__(
            self,
            channel_id,
            bot_prefix,
            timing=2,
            bot_description="Simple bot that sends affirmations every once in a while to certain channel",
            bot_intents=discord.Intents.default()):
        super().__init__(command_prefix=bot_prefix,
                         description=bot_description,
                         intents=bot_intents)
        self.time = timing
        self.chanel = None
        self.channel_id = channel_id
        self.postAffirmation.start()
        self.clearChannel.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def getAffirmation(self, amount=1):
        affirmations = list()
        response: Response = None
        affirmation: str = None
        for (i) in range(amount):
            choices: int = randint(1, 3)
            if choices == 1:
                response = get("https://affirmations.dev")
                affirmation = (response.json()).get("affirmation")

            elif choices == 2:
                response = get("https://zenquotes.io/api/random")
                affirmation = (response.json())[0].get("q")

            elif choices == 3:
                response = get("https://quotes.rest/qod.json?language=en")
                affirmation = ((response.json()).get("contents").get("quotes")
                               [0].get("quote"))

            affirmations.append(affirmation)
        return affirmations

    @tasks.loop(minutes=30)
    async def postAffirmation(self):
      aff=await self.getAffirmation()
      await (self.channel).send(aff[0])

    @tasks.loop(hours=48)
    async def clearChannel(self):
      try:
        await (self.channel).purge(limit=100000)
      except:
        pass

    @postAffirmation.before_loop
    async def beforePosting(self):
        await self.wait_until_ready()
        self.channel = self.get_channel(self.channel_id)
        await self.clearChannel()


bot = AffirmationsBot(int(channel_id), "..")
@bot.command(name="get")
async def gets(ctx, *, times:int):
  try:
      times=int(times)
      aff=await bot.getAffirmation(amount=times)
      for (i, affirmation) in enumerate(aff):
        await (bot.channel).send('#'+str(i+1)+':\n'+affirmation)
  except Exception as e:
    bot.channel.send(e.args)
keep_alive()
bot.run(bot_token)
