import discord
import os
from dotenv import load_dotenv
from scraper import extract_events_from_devfolio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

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
    if message.content == '!ping':
        await message.channel.send('Pong!')
    if message.content == '!events':
        events = extract_events_from_devfolio()
        if not events:
            await message.channel.send("No upcoming events found.")
        else:
            print(events)
            for event in events:
                msg_text = f"**{event['title']}**\n" \
                           f"URL: {event['url']}\n" \
                           f"Mode: {event['mode']}\n" \
                           f"Location: {event['location']}\n" \
                           f"Date: {event['start_date']}\n"
                await message.channel.send(msg_text)


client.run(TOKEN)
