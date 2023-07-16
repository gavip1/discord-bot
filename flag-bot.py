import discord
import random
import asyncio
import os
import pandas
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

df = pandas.read_csv("country_list.csv")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
timeout_delta = timedelta(seconds=15)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!flag":
        mention = message.author.mention

        column_con = "Country"
        column_nat = "Nationality"
        column_id = "emote_id"

        rand_index = random.randint(0, len(df[column_con]) - 1)
        rand_country = df.loc[rand_index, column_con]
        rand_nationality = df.loc[df[column_con] == rand_country, column_nat].iloc[0]
        await message.channel.send(f"{mention} what flag is this?")
        await message.channel.send(df.loc[df[column_con] == rand_country, column_id].iloc[0])

        def is_correct(m):  #ensures the answer is from op and it is a valid answers within the choices
            matched = df[column_con].str.contains(m.content, case=False, na=False) | df[column_nat].str.contains(m.content, case=False, na=False)
            if any(matched):
                valid = True
            else:
                valid = False
            return m.author == message.author and valid

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await message.author.timeout(timeout_delta, reason="lol")
            return await message.channel.send(f'Sorry, you took too long it was {rand_country}.')
        
        if random.randint(1,10) == 5:
            await message.channel.send(":wtf:")
        if str(guess.content).capitalize() in [rand_country, rand_nationality]:
            await message.channel.send('You are right!')
        else:
            await message.channel.send(f'Oops. It is actually {rand_country}.')
            await message.channel.send(":PepeLa:")
            await message.author.timeout(timeout_delta, reason="lol")

token = os.environ.get('TOKEN')   
client.run(token)