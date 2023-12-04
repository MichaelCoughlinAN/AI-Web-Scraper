import random
import discord
import openai
import config as config
import scrape as scrape
import re
import random
import bs4
import requests
import send_message as send_message

# Set the name and backstory for the AI persona
name = "Michael Coughlin"
backstory = """Age: 30
Occupation: Quantitative Analyst
Background: Benjamin's analytical prowess and deep understanding of financial models make him a leading figure in quantitative finance."""


# Function to generate AI-based news discussion
async def generate_ai_news(news):
    try:
        # Set the OpenAI API key
        openai.api_key = config.ai_key

        # Craft a message prompting the AI to discuss the news
        message = (
            f"Imagine you're diving into a discussion about the latest Minnesota news with a group of well-informed, open-minded individuals. " +
            f"As someone with this background: {backstory}, " +
            f"how would you bring up the following news in a friendly manner?\n\n" +
            f"News: {news}"
        )

        print(message)

        # Generate a response from the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": message}
            ]
        )

        # Return the response content
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return "Sorry, I couldn't generate a response. Please try again later."

# Function to remove trailing hashtags from a string
def remove_trailing_hashtags(text):
    return re.sub(r'(\s*#\w+)*$', '', text)

# Function to safeguard the length of a response
def safeguard_response(response, max_length=1024):
    if len(response) > max_length:
        return response[:max_length-3] + "..."
    return response

# Function to generate AI-driven notes on stocks
async def generate_ai_notes(stocks):
    try:
        openai.api_key = config.ai_key

        # Craft a message for the AI to analyze stocks
        message = (
            f"As a seasoned quantitative analyst with a forward-thinking and academic approach, provide an astute analysis " +
            f"on the trending stocks from Reddit: {str(stocks)}"
        )
        
        print(message)

        # Generate a response from the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        # Safeguard and return the response content
        return safeguard_response(response.choices[0].essage.content.strip())
    except Exception as e:
        print(e)

# Function to create a Discord embed with table data
def create_embed(headers, rows):
    embed = discord.Embed()
    embed.color = discord.Color.green()
    embed.title = "Table"

    # Add headers and rows to the embed
    embed.add_field(name=" ".join(headers), value="\u200b", inline=False)
    for row in rows:
        embed.add_field(name=" ".join(row), value="\u200b", inline=False)

    return embed

# Function to remove duplicate elements from a list
def remove_duplicates(input_list):
    return list(set(input_list))

# Function to scrape Minnesota news from Google News
async def get_minnesota_news():
    URL = "https://news.google.com/search?q=minnesota&hl=en-US&gl=US&ceid=US:en"
    headers = {
        "User-Agent": "Mozilla/5.0 ..."
    }

    # Make a request to the URL and parse the content with BeautifulSoup
    response = requests.get(URL, headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # Scrape and process headlines from the HTML content
    for article in soup.find_all('article', class_='...'):
        headline = article.a.text
        link = article.a['href']

    # Print top 5 headlines as an example and return a random headline
    print("\nTop 5 Headlines:")
    for headline in soup.find_all('h3', class_='...'):
        print(headline.text)
        headlines.append(headline.text)
    return random.choice(headlines) if headlines else None

# Remaining functions include various utility functions to process and format strings,
# extract elements from HTML, determine item rarity based on price, and beautify addresses.

# Function to get text from an HTML element
def get_element_text(element, selector, default=''):
    try:
        return re.sub('\s+', ' ', element.find(selector).text).strip()
    except:
        return default

# Function to get an attribute from an HTML element
def get_element_attribute(element, selector, attribute, default=''):
    try:
        return element.find(selector)[attribute].strip()
    except:
        return default

def remove_trailing_hashtags(text):
    # Remove any trailing hashtags from the text
    return re.sub(r'(\s*#\w+)*$', '', text)

def remove_hashtags(text):
    # Remove all hashtags from the text
    return re.sub(r'#\S+', '', text)

def determing_item_rarity(price):
    """
    Determine the rarity of an item based on its price. This function uses a
    set of price thresholds to assign a color code to the item, indicating its rarity.
    """
    if price == 'Auction':
        banner = 0x808080  # Grey color for auction items
        return banner

    numeric_price = convert_string_to_int(price)
    banner = 0x808080  # Default color (Grey)

    # Assigning different colors based on price ranges
    if numeric_price <= 100000:
        banner = 0x2dc50e  # Green
    elif 100000 < numeric_price < 300000:
        banner = 0x3a92ff  # Blue
    elif 300000 <= numeric_price <= 500000:
        banner = 0xa02ef7  # Purple
    elif 500000 < numeric_price < 800000:
        banner = 0xeeca2a  # Yellow
    elif numeric_price >= 800000:
        banner = 0xff8200  # Orange

    return banner

def clean_str(input_str):
    """
    Clean and format a string containing property details. It formats strings
    related to bedrooms, bathrooms, square footage, and acreage.
    """
    try:
        if 'acre' in input_str:
            # Extracting and formatting property details
            bedrooms = input_str.split('bed')[0]
            bathrooms = input_str.split('bath')[0].split('bed')[-1]
            sqft = input_str.split('sqft')[0].split('bath')[-1].split('bed')[-1]
            acre = input_str.split('acre')[0].split('sqft')[-1]
            input_str = f"{bedrooms} bed | {bathrooms} bath | {sqft} sqft. | {acre} acre lot"
        else:
            # Formatting property details without acreage
            output_str = input_str.replace('bed', ' bed | ').replace('bath', ' bath | ')
            input_str = output_str.replace('sqft', ' sqft. ')
            input_str = input_str.replace('  ', ' ')
            input_str = input_str.split('sqft.')[0] + ' sqft. |' + input_str.split('sqft.')[1] + 'sqft. lot'
            input_str = input_str.replace(' sqft. | sqft. lot', 'sqft.')
    except Exception as e:
        print(e)
 
    return input_str

def uppercase_cardinal_directions(string):
    """
    Uppercase cardinal directions (NW, NE, SW, SE) in a given string.
    """
    words = string.split()
    for i in range(len(words)):
        if words[i].lower() in ["nw", "ne", "sw", "se"]:
            words[i] = words[i].upper()
    return " ".join(words)

def capitalize_first_letter(string):
    """
    Capitalize the first letter of each word in a string.
    """
    words = string.split()
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)

def beautify_address(address):
    """
    Beautify an address by capitalizing the first letter of each component and
    joining them with commas.
    """
    components = address.strip().split(' ') 
    components = [component.capitalize() for component in components]
    beautified_address = ', '.join(components)
    return beautified_address

def convert_string_to_int(string):
    """
    Convert a string containing a numeric value to an integer. It removes
    commas and dollar signs from the string before conversion.
    """
    string = string.replace(',', '').replace('$', '')
    return int(string)