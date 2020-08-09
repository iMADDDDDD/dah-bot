import discord
import os
import data
from dotenv import load_dotenv

# Loading .env
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == 'DAH':
        flights = data.search_request(message.content)

        embed = discord.Embed(title="You searched " +
                              message.content, color=0x00ff00)

        for flight in flights:
            msg = flight.get('from') + " to " + flight.get('to') + \
                " | Plane: " + flight.get('plane') + " - " + \
                flight.get('plane_type')
            embed.add_field(name=flight.get('callsign'),
                            value=msg, inline=False)

        await message.channel.send(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
