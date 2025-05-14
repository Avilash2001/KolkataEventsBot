import discord
import os
from dotenv import load_dotenv
from scraper import get_events
import asyncio
from datetime import datetime, timedelta
import json
from pytz import timezone
from urllib.parse import quote_plus

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def create_gcal_link(title, start_date, url, location):
    try:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        except ValueError:
            import re
            match = re.search(r'([A-Za-z]+)\s+(\d{1,2})\s*-\s*(\d{1,2}),\s*(\d{4})', start_date)
            if match:
                month_str, day_start, day_end, year = match.groups()
                full_date = f"{month_str} {day_start}, {year} 10:00"
                start_dt = datetime.strptime(full_date, "%b %d, %Y %H:%M")
            else:
                try:
                    start_dt = datetime.strptime(start_date, "%b %d, %Y")
                except ValueError:
                    print("Unrecognized date format:", start_date)
                    return None

        start_str = start_dt.strftime("%Y%m%dT%H%M%SZ")
        end_dt = start_dt + timedelta(hours=2)
        end_str = end_dt.strftime("%Y%m%dT%H%M%SZ")

        link = (
            "https://www.google.com/calendar/render?"
            f"action=TEMPLATE&text={quote_plus(title)}"
            f"&dates={start_str}/{end_str}"
            f"&details={quote_plus('More info: ' + url)}"
            f"&location={quote_plus(location)}"
        )
        return link
    except Exception as e:
        print("Error creating calendar link:", e)
        return None
    
def get_msg_embed(event):
    gcal_url = create_gcal_link(event['title'], event['start_date'], event['url'], event['location'])

    embed = discord.Embed(
        title=event['title'],
        url=event['url'],
        color=discord.Color.blue(),
    )
    embed.add_field(name="🌐 Mode", value=event['mode'], inline=False)
    embed.add_field(name="➕ Add to Google Calendar", value=f"[Click Here]({gcal_url})", inline=False)
    embed.add_field(name="📍 Location", value=event['location'], inline=False)
    embed.add_field(name="🗓️ Date", value=event['start_date'], inline=False)
    if event.get('banner'):
        embed.set_image(url=event['banner'])

    return embed

async def weekly_event_update():
    await client.wait_until_ready()

    while not client.is_closed():
        config = load_config()
        channel_id = config.get("update_channel_id")
        update_days_frequency = config.get("update_days_frequency", 7)

        if not channel_id:
            print("No update channel set. Waiting until one is configured with !setchannel.")
            await asyncio.sleep(60)
            continue

        channel = client.get_channel(channel_id)
        if not channel:
            print("Invalid channel ID. Skipping.")
            await asyncio.sleep(3600)
            continue

        try:
            await channel.send("Fetching upcoming events for this week...")
            events = get_events()
            if not events:
                await channel.send("No upcoming events found this week.")
            else:
                await channel.send("Here are the upcoming events this week:")
                for event in events:
                    embed = get_msg_embed(event)
                    await channel.send(embed=embed)

        except Exception as e:
            await channel.send("Error fetching weekly events.")
            print("Weekly fetch error:", e)

        next_run_utc = datetime.utcnow() + timedelta(days=update_days_frequency)
        india_tz = timezone("Asia/Kolkata")
        next_run_ist = india_tz.normalize(india_tz.fromutc(next_run_utc))
        msg = f"Next update scheduled for {next_run_ist.strftime('%A, %d %B %Y at %I:%M %p')} IST"
        print(msg)
        await channel.send(msg)
        await asyncio.sleep(update_days_frequency * 24 * 60 * 60)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(weekly_event_update())

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
            "`!setchannel` - Set this channel to receive weekly event updates\n"
            "`!events` - Show upcoming offline events in Bengal\n"
            "`!events all` - Show all upcoming events\n"
            "`!events online` - Show only online events\n"
            "`!events offline` - Show only offline events\n"
            "`!help` - Show this help message\n"
            "`!setupdatefrequency <days>` - Set update frequency (default is 7)\n"
            "`!seeupdatedetails` - See when the next update will be sent\n"
        )
        await message.channel.send(help_text)

    elif msg == '!setchannel':
        config = load_config()
        config["update_channel_id"] = message.channel.id
        save_config(config)
        await message.channel.send(f"This channel has been set to receive weekly event updates.")

    elif msg.startswith('!setupdatefrequency'):
        try:
            _, days = msg.split()
            days = int(days)
            if days <= 0:
                raise ValueError("Days must be positive.")
            config = load_config()
            config["update_days_frequency"] = days
            save_config(config)
            await message.channel.send(f"Update frequency set to {days} days.")
        except ValueError:
            await message.channel.send("Please provide a valid number of days.")

    elif msg == '!seeupdatedetails':
        config = load_config()
        channel_id = config.get("update_channel_id")
        update_days_frequency = config.get("update_days_frequency", 7)

        if not channel_id:
            await message.channel.send("No update channel set. Use `!setchannel` to set this channel.")
            return

        channel = client.get_channel(channel_id)
        if not channel:
            await message.channel.send("Invalid channel ID. Please set a valid channel with `!setchannel`.")
            return

        next_run_utc = datetime.utcnow() + timedelta(days=update_days_frequency)
        india_tz = timezone("Asia/Kolkata")
        next_run_ist = india_tz.normalize(india_tz.fromutc(next_run_utc))
        await message.channel.send(f"Next update scheduled for {next_run_ist.strftime('%A, %d %B %Y at %I:%M %p')} IST in {channel.mention}.")

    elif msg.startswith('!events'):
        mode = "bengal"

        if msg == "!events all":
            mode = "all"
            await message.channel.send(f"Fetching all upcoming events...")
        elif msg == "!events online":
            mode = "online"
            await message.channel.send(f"Fetching all upcoming online events...")
        elif msg == "!events offline":
            mode = "offline"
            await message.channel.send(f"Fetching all upcoming offline events...")
        else:
            mode = "bengal"
            await message.channel.send(f"Fetching upcoming offline events in bengal...")

        events = get_events(mode_filter=mode)
        if not events:
            await message.channel.send("No upcoming events found.")
        else:
            for event in events:
                embed = get_msg_embed(event)
                await message.channel.send(embed=embed)

client.run(TOKEN)
