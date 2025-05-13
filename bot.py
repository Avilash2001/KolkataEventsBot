import discord
import os
from dotenv import load_dotenv
from scraper import get_events_V2

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

    msg = message.content.lower()

    if msg == '!ping':
        await message.channel.send('Pong!')

    elif msg == '!help':
        help_text = (
            "**Available Commands:**\n"
            "`!ping` - Check if the bot is alive\n"
            "`!events` - Show upcoming offline events in Bengal\n"
            "`!events all` - Show all upcoming events\n"
            "`!events online` - Show only online events\n"
            "`!events offline` - Show only offline events\n"
            "`!help` - Show this help message"
        )
        await message.channel.send(help_text)

    elif msg.startswith('!events'):
        mode = "bengal"  # default

        if msg == "!events all":
            mode = "all"
        elif msg == "!events online":
            mode = "online"
        elif msg == "!events offline":
            mode = "offline"

        await message.channel.send(f"Fetching events for: `{mode}`...")

        events = get_events_V2(mode_filter=mode)
        if not events:
            await message.channel.send("No upcoming events found.")
        else:
            for event in events:
                embed = discord.Embed(
                    title=event['title'],
                    url=event['url'],
                    color=discord.Color.blue(),
                    description=f"🌐 **Mode:** {event['mode']}"
                )
                embed.add_field(name="📍 Location", value=event['location'], inline=False)
                embed.add_field(name="🗓️ Date", value=event['start_date'], inline=False)
                if event.get('banner'):
                    embed.set_image(url=event['banner'])
                await message.channel.send(embed=embed)



client.run(TOKEN)
