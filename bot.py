import discord, requests, creds

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
        await message.channel.send('What is your Mini League ID?')

    if message.content.isdigit():
        id = str(message.content)
        response = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/{id}/standings/?page_standings=1')
        parsed = response.json()
        standings = parsed['standings']
        results = standings['results']
        await message.channel.send('Here are the most recent standings for your mini league: \n')
        for index in range(len(results)):
            team = ("#" + str(results[index]['rank']) + " " + results[index]['player_name'] + "'s '" + results[index]['entry_name'] + "' with " + str(results[index]['total']) + " points")
            await message.channel.send(f'{team}')
client.run(creds.token)