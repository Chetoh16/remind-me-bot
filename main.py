import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timezone

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Set up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True
## Every single permission will be included in one of these intents

bot = commands.Bot(command_prefix='/', intents=intents)
## Handling Events
@bot.event ## decorator for events
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    ## Ignore messages from the bot itself

    if "egg" in message.content.lower():
        await message.channel.send("egg🥚")

    await bot.process_commands(message)
    ## Allows us to continue handling other messages. This is required.


@bot.command(aliases=['wl'])
async def watchlist(ctx, *, arg):  ## Accepts full message as one argument
    arg_data = {
        'content': arg,
        'author': str(ctx.author),
        'timestamp': str(ctx.message.created_at)
    }

    data = []

    # Try to load existing data
    if os.path.exists('watchlist.json'):
        try:
            with open('watchlist.json', 'r') as file:
                data = json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            await ctx.send(f"Error reading watchlist.json: {e}")
            return

    # Append new entry
    data.append(arg_data)

    # Try to write updated data
    try:
        with open('watchlist.json', 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        await ctx.send(f"Error writing to watchlist.json: {e}")
        return

    await ctx.send(f"'{arg}' saved to watchlist.")

@bot.command(aliases=['wlshow'])
async def watchlistshow(ctx):
    if not os.path.exists('watchlist.json'):
        await ctx.send("Watchlist is empty.")
        return

    try:
        with open('watchlist.json', 'r') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        await ctx.send(f"Error reading watchlist: {e}")
        return

    if not data:
        await ctx.send("Watchlist is empty.")
        return

    # Build message from entries
    message_lines = []
    for idx, entry in enumerate(data, start=1):
        try:
            # Parse as UTC if no timezone info
            dt = datetime.fromisoformat(entry['timestamp'])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            formatted_time = dt.astimezone().strftime("%d/%m/%y %H:%M")
        except Exception:
            formatted_time = entry['timestamp']

        message_lines.append(
            f"**#{idx}**\n📄 Content: {entry['content']}\n👤 Author: {entry['author']}\n⏰ Time: {formatted_time}\n"
        )
        
    # Send in chunks if too long
    for chunk in [message_lines[i:i+5] for i in range(0, len(message_lines), 5)]:
        await ctx.send("\n".join(chunk))


@bot.command(aliases=['wlremove'])
async def watchlistremove(ctx, id):
    if not os.path.exists('watchlist.json'):
        await ctx.send("Watchlist is empty.")
        return

    try:
        with open('watchlist.json', 'r') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        await ctx.send(f"Error reading watchlist: {e}")
        return

    # Check if ID is valid
    try:
        id = int(id) - 1  # Convert to zero-based index
        if id < 0 or id >= len(data):
            raise ValueError("Invalid ID")
    except ValueError:
        await ctx.send("Please provide a valid watchlist entry number.")
        return

    # Remove entry
    removed_entry = data.pop(id)

    # Write updated data back to file
    try:
        with open('watchlist.json', 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        await ctx.send(f"Error writing to watchlist: {e}")
        return

    await ctx.send(f"Removed entry #{id + 1} from watchlist:\n📄 Content: {removed_entry['content']}\n👤 Author: {removed_entry['author']}")



bot.run(token, log_handler=handler, log_level=logging.DEBUG) ## Log debug stuff in discord.log

## TO DO 
## ----------------------------------------
## Run bot without computer with Render
## Edit content in the json 
## Have new json files for booklist etc.
## Have a help command that shows all commands
## Add a limit to watchlist entries
## Should be able to remove entries by content rather than ID
## Integrate with either google sheets or a notion database