#import necessary libraries
import discord, requests, creds, logging

#candidly not sure what these do, but taken from documentation
intents = discord.Intents.default()
intents.message_content = True

#same as above
client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='fplbot.log', encoding='utf-8', mode='w')

#on ready, prints that we have logged in as the bot. Help prompt will only work on my personal server
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    #this next command only works on my private server
    channel = client.get_channel(1065342425540866099)
    await channel.send('Type "help" for instructions')

#starts the bot interaction with messages
@client.event
async def on_message(message):
    #if the bot reads a message from the bot, do nothing
    if message.author == client.user:
        return

    #if the bot reads 'update' ask for ML id
    if message.content == 'update':
        await message.channel.send('What is your Mini League ID?')
    
    #if bot is asked for help
    if message.content == 'help':
        await message.channel.send('- type "info" for more info about this bot\n- type your Mini League ID to get the most recent standings for your league')

    if message.content == 'info':
        await message.channel.send('This bot allows for discord users to ping the FPL API to check the most recent standings in their Mini League of choice')    

    #if bot gets digit, basically searches for mini league and prints standings in discord messages
    if message.content.isdigit():
        id = str(message.content)
        response = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/{id}/standings/?page_standings=1').json()
        results = response['standings']['results']
        league_name = response['league']['name']

        #this is where we send the messages
        await message.channel.send(f'Here are the most recent standings for {league_name}: \n')
        for index in range(len(results)):
            rank = str(results[index]['rank'])
            player_name = results[index]['player_name']
            entry_name = results[index]['entry_name']
            total = str(results[index]['total'])
            await message.channel.send(f"#{rank} {player_name}'s '{entry_name}' with {total} points")

client.run(creds.token, log_handler=handler)