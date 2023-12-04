import discord
from discord.ext import tasks
import shared as shared
import config as config

# Set up the Discord client with specific intents for more detailed control over what events your bot can track.
intents = discord.Intents.default()
intents.message_content = True  # Enable the bot to access message content
intents.members = True          # Enable the bot to track server members
intents.reactions = True        # Enable the bot to track reactions to messages
intents.guilds = True           # Enable the bot to access guild (server) information
client = discord.Client(command_prefix=",", intents=intents)  # Initialize the Discord client with these intents


@client.event
async def on_ready():
    """
    This event is called when the bot has successfully connected to Discord.
    """
    print(f'We have logged in as {client.user}')  # Print a confirmation message to the console
    await client.wait_until_ready()  # Wait until the client is fully ready
    await main.start()  # Start the main task loop


@tasks.loop(seconds=60)
async def main():
    """
    This is the main task loop that runs every 60 seconds.
    """
    try:
        # TODO:
        # - Scrape web for items using code from scrape.py
        # - Generate message about items using code from shared.py
        # - Send message to Discord server using code from send_message.py
        pass  # Placeholder for the actual implementation
    except Exception as e:
        print(e)  # Print any exceptions to the console


client.run(config.client_token)  # Start the bot using the token from the config file