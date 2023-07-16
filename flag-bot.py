import discord
import random
import asyncio
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

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
        choices = ["indonesia", "Indonesia", "Polish", "polish", "poland", "Poland"]
        flag_pl = ["Polish", "polish", "poland", "Poland"]
        flag_id = ["indonesia", "Indonesia", "indonesian", "Indonesian"]

        answer = random.choice(['Poland', 'Indonesia'])
        await message.channel.send(f"{mention} is this Poland or Indonesia (10s)")
        if answer == 'Poland':  #send the flag as an emote based of the random choice
            await message.channel.send(':flag_pl:')
            answer_flag = flag_pl
            not_answer = flag_id
        else:
            await message.channel.send(':flag_id:')
            answer_flag = flag_id
            not_answer = flag_pl

        def is_correct(m):  #ensures the answer is from op and it is a valid answers within the choices
            return m.author == message.author and m.content in choices

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await message.author.timeout(timeout_delta, reason="too stupid")
            return await message.channel.send(f'Sorry, you took too long it was {answer}.')
        
        if random.randint(1,10) == 5:
            await message.channel.send(":wtf:")
        if str(guess.content) in answer_flag:
            await message.channel.send('You are right!')
        elif str(guess.content) in not_answer:
            await message.channel.send(f'Oops. It is actually {answer}.')
            await message.author.timeout(timeout_delta, reason="too stupid")

token = os.environ.get('TOKEN')   
client.run(token)