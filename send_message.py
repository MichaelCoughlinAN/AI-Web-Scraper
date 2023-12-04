import shared as shared  # Importing the shared utilities module
import discord  # Importing the Discord module
import config as config  # Importing the configuration module


async def send_message(client, img, price, name, url, city, mileage, date, notes):
    try:
        # Printing the parameters for debugging purposes
        print(img)
        print(price)
        print(name)
        print(url)
        print(city)
        print(mileage)
        print(date)
        
        # Creating a Discord embed with the provided details
        embed = discord.Embed(title=name, color=shared.determing_item_rarity(price), url=url)

        # Adding various fields to the embed
        embed.add_field(name="Price", value=price, inline=False)
        embed.add_field(name="Location", value=city, inline=False)
        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name="Mileage", value=mileage, inline=False)
        embed.add_field(name="Notes", value=notes, inline=False)
        embed.add_field(name="Link", value=f'[Link]({url})', inline=False)
        embed.set_thumbnail(url=img)

        # Setting a footer for the embed; wrapped in a try-except block for robustness
        try:
            embed.set_footer(text='Designed by hiimmichael.com', icon_url='https://hiimmichael.com/images/main_photo.png')
        except Exception as e:
            print(f"Error setting embed footer: {e}")

        # Sending the embed to the specified Discord channel
        await client.get_channel(config.channel_id).send(embed=embed)
    except Exception as e:
        print(f"Error sending message: {e}")