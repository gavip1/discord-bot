import discord
import random
import asyncio
import os
import pandas
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
timeout_delta = timedelta(seconds=15)

df = pandas.read_csv("country_list.csv")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!flag":
        mention = message.author.mention
        flags = {1: ["Poland", "Polish", "_pl:"], 2: ["Indonesia", "Indonesian", "_id:"]}

        pick = random.randint(1, len(flags))
        await message.channel.send(f"{mention} what flag is this?")
        await message.channel.send(":flag" + flags[pick][2])

        def is_correct(m):  #ensures the answer is from op and it is a valid answers within the choices
            return m.author == message.author and m.content.capitalize() in df.values

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await message.author.timeout(timeout_delta, reason="too stupid")
            return await message.channel.send(f'Sorry, you took too long it was {flags[pick][0]}.')
        
        if random.randint(1,10) == 5:
            await message.channel.send(":wtf:")
        if str(guess.content).capitalize() in flags[pick]:
            await message.channel.send('You are right!')
        else:
            await message.channel.send(f'Oops. It is actually {flags[pick][0]}.')
            await message.author.timeout(timeout_delta, reason="too stupid")

token = os.environ.get('TOKEN')   
client.run(token)