# This example requires the 'message_content' intent.

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'update':
        await message.channel.send('Here are the most recent updated mini league standings:')

client.run('MTA2NTEyODkxODIzNzA2NTI1OA.GDt07n.01itLlJCgReAbw7dcRnyr8vp24PxHFTtQTxo2E')