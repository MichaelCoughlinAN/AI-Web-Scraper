import random
import bs4
import requests
import re
import config
import time
import shared
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select


async def get_minnesota_news():
    """
    Asynchronously scrapes the latest news headlines about Minnesota from Google News.
    It returns a randomly selected headline from the scraped list.
    """
    URL = "https://news.google.com/search?q=minnesota&hl=en-US&gl=US&ceid=US:en"
    headers = {
        "User-Agent": "Mozilla/5.0 ..."
    }

    response = requests.get(URL, headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    
    headlines = []
    # Extract headlines from the parsed HTML content
    for article in soup.find_all('article', class_='...'):
        headline = article.a.text
        link = article.a['href']
        headlines.append(headline)  # Append headline to the list

    # Return a random headline from the list
    return random.choice(headlines) if headlines else None


async def scrape_pawnamerica():
    """
    Asynchronously scrapes the musical instruments and gear category from the Pawn America website.
    The function sets up a Selenium WebDriver to interact with the website, extracts the product details,
    and prints them. It closes the WebDriver upon completion or in case of an exception.
    """

    # Initialize the Chrome WebDriver with specified options to ensure compatibility and performance.
    s = Service(config.chromedriver_path)
    chromeOptions = webdriver.ChromeOptions() 
    chromeOptions.add_argument("--no-sandbox")  # Bypass the OS security model, generally required in a containerized environment.
    chromeOptions.add_argument("--disable-gpu")  # Disable GPU hardware acceleration, if not needed.
    driver = webdriver.Chrome(options=chromeOptions, service=s) 

    # Define the base URL and store name for the scraping.
    store_name = 'PawnAmerica'
    base_url = "https://www.pawnamerica.com"

    try:
        # Navigate to the specific category page on the Pawn America website.
        driver.get(base_url + "/Shop?category=musical-instruments-and-gear")
        driver.implicitly_wait(25)  # Wait for the page elements to load.

        # Get the page source and use BeautifulSoup to parse it.
        squadPage = driver.page_source
        soup = bs4.BeautifulSoup(squadPage, 'html.parser')

        # Find all elements that match the class pattern for product properties.
        properties = soup.find_all('div', class_=re.compile("col-xl-2"))

        # Iterate through each product property element to extract details.
        for property in properties:
            price = property.find('p', class_=re.compile("ps-product__price")).text.strip()  # Extract the product price.
            title = property.find('a', class_=re.compile("ps-product__title")).text.strip()  # Extract the product title.
            url = base_url + property.find('a', class_=re.compile("ps-product__title"))['href']  # Construct the product URL.
            location = property.find('div', class_=re.compile("ps-product__container")).find('a', class_=re.compile("ps-product__vendor")).text.strip()  # Extract the product location.
            thumbnail = property.find('div', class_=re.compile("ps-product__thumbnail")).find('img')['src']  # Extract the thumbnail image URL.

            # Print the extracted product details for verification.
            print(store_name, price, title, url, location, thumbnail)

    except Exception as e:
        # Print any exception that occurs during the web scraping.
        print(e)
    finally:
        # Close the WebDriver to free up resources and avoid memory leaks.
        driver.close()


async def scrape_10k_brew():
    """
    Asynchronously scrapes the menu items from the 10K Brew website.

    This function makes an HTTP GET request to the 10K Brew website and parses the HTML content to extract 
    details of menu items, including their description, price, title, and image source. It handles any 
    exceptions that occur during the scraping process and prints each item's details for verification.
    """

    # The URL of the 10K Brew menu board page
    url = 'https://10kbrew.com/menu-board/'

    # Headers to bypass potential 403 Forbidden error by mimicking a browser user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    # Perform a GET request to fetch the HTML content of the page
    result = requests.get(url, headers=headers)

    # Use BeautifulSoup to parse the HTML content for data extraction
    soup = bs4.BeautifulSoup(result.content, 'html.parser')

    # Locate the section of the webpage that contains the menu items
    menu_board_section = soup.find('div', class_='bt_bb_row menu_board')

    # Find all individual menu items within the menu board section
    menu_items = menu_board_section.find_all('div', class_="bt_bb_menu_item")
    
    # Iterate through each menu item and extract its details
    for item in menu_items:
        try:
            # Extract the description, price, title, and image source of each menu item
            item_description = item.find('div', class_='bt_bb_menu_item_description').text.strip()
            item_price = item.find('div', class_='bt_bb_menu_item_price').text.strip()
            item_title = item.find('div', class_='bt_bb_menu_item_title').text.strip()
            img = item.find('img')['src']  # Get the image source URL

            # Print each item's details for verification and debugging purposes
            print(item_description, item_price, item_title, img)
        except Exception as e:
            # Print any errors encountered during the scraping process
            print(f"Error encountered: {e}")


async def scrape_enki_brew():
    """
    Asynchronously scrapes beer details from the Enki Brewing website.

    The function makes an HTTP GET request to the Enki Brewing website's 'Our Beer' page and parses the HTML content 
    to extract details of each beer, including its name and description. It handles exceptions that may occur during 
    the scraping process and prints the details of each beer for verification.
    """
    try:
        # The URL of the Enki Brewing 'Our Beer' page
        url = "https://www.enkibrewing.com/our-beer"
        
        # Headers to bypass potential 403 Forbidden error by mimicking a browser user-agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # Perform a GET request to fetch the HTML content of the page
        result = requests.get(url, headers=headers)
        
        # Use BeautifulSoup to parse the HTML content for data extraction
        soup = bs4.BeautifulSoup(result.content, 'html.parser')

        # Find all elements that contain summaries of the beers
        beer_summaries = soup.find_all('div', class_='summary-content')

        # Iterate through each beer summary element to extract details
        for beer in beer_summaries:
            # Extract the beer name from the summary title
            beer_name = beer.find('div', class_='summary-title').a.text

            # Extract the beer description from the summary excerpt
            # Join paragraphs (if multiple) into a single string
            description_div = beer.find('div', class_='summary-excerpt')
            description = ' '.join([p.text for p in description_div.find_all('p')])

            # Print the beer name and description for verification
            print(beer_name)
            print("Description:", description)

    except Exception as e:
        # Print any errors encountered during the scraping process
        print(f"Error encountered: {e}")


async def scrap_waconia_brew():
    """
    Asynchronously scrapes the beer list from the Waconia Brewing Company website.

    The function sends an HTTP GET request to the website, parses the HTML content to extract
    details of the beers including their names, images, and descriptions. It also ensures no duplicate
    entries are processed. In case of errors during scraping, these are caught and printed for debugging.
    """
    try:
        # The URL of the Waconia Brewing Company 'Our Beers' page
        url = 'https://www.waconiabrewing.com/our-beers/'

        # Headers to bypass potential 403 Forbidden error by mimicking a browser user-agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # Perform a GET request to fetch the HTML content of the page
        result = requests.get(url, headers=headers)

        # Use BeautifulSoup to parse the HTML content
        soup = bs4.BeautifulSoup(result.content, 'html.parser')
        # Find the main content section of the webpage
        section = soup.find('section', class_='wpb-content-wrapper')
        content = section.find_all('div', class_="wpb_wrapper")
        
        duplicates_list = []  # List to keep track of already processed items to avoid duplicates

        # Iterate through the content to find and process each beer listing
        for line in content:
            try:
                # Check if the line contains a link to a beer's page
                link_element = line.find('a', class_='vc_single_image-wrapper vc_box_border_grey')
                if link_element and link_element['href'] not in duplicates_list:
                    # Extract and print the beer page URL and image URL
                    beer_page_url = link_element['href']
                    print(beer_page_url)
                    img_url = line.find('img')['src']
                    print(img_url)

                    # Add the URL to the duplicates list to avoid reprocessing
                    duplicates_list.append(beer_page_url)

                    # Fetch and parse the individual beer page
                    beer_page_result = requests.get(beer_page_url, headers=headers)
                    beer_page_soup = bs4.BeautifulSoup(beer_page_result.content, 'html.parser')
                    content_div = beer_page_soup.find('div', class_='ltx-wrapper')

                    # Extract the beer name
                    beer_name = content_div.find('div', class_='heading').find('h3').text.strip()
                    print(beer_name)

                    # Extract and concatenate the beer description from all paragraphs
                    description = ''
                    for paragraph in content_div.find_all('p'):
                        description += paragraph.text.strip() + '\n'

                    # Print the concatenated description
                    print(description)

            except Exception as e:
                # Print any errors encountered while processing an individual beer listing
                print(e) 
    except Exception as e:
        # Print any errors encountered while fetching or parsing the main beer list page
        print(e) 


async def scrape_wells():
    """
    Asynchronously scrapes property listings from the Wells Fargo REO (Real Estate Owned) website.

    This function sets up a Selenium WebDriver to interact with the website, navigates to the property listings page,
    and then scrapes detailed information about each property. It handles exceptions and ensures the WebDriver is closed properly.
    """
    # Initialize the Chrome WebDriver with specified options for compatibility and performance.
    s = Service(config.chromedriver_path)
    chromeOptions = webdriver.ChromeOptions() 
    chromeOptions.add_argument("--no-sandbox")  # Bypass the OS security model, usually required in containerized environments.
    chromeOptions.add_argument("--disable-gpu")  # Disable GPU hardware acceleration if it's not needed.
    driver = webdriver.Chrome(options=chromeOptions, service=s) 

    try:   
        # Navigate to the Wells Fargo REO properties page.
        driver.get("https://reo.wellsfargo.com/Properties")
        driver.implicitly_wait(25)  # Wait for the page elements to load.
       
        # Select the 'All' option in a dropdown to display all properties.
        sel = Select(driver.find_element("xpath","//select[@name='example_length']"))
        sel.select_by_visible_text("All")
        time.sleep(0.8)  # Wait for the page to update with all listings.

        # Get the page source and parse it using BeautifulSoup.
        squadPage = driver.page_source
        soup = bs4.BeautifulSoup(squadPage, 'html.parser')

        # Find all property listing elements.
        properties = soup.find_all('tr')

        # Iterate through each property listing to extract details.
        for property in properties:
            property_details = property.find_all('td')

            # Ensure the property row has details before proceeding.
            if len(property_details) > 0:
                # Extract various details such as address, price, bed, bath, etc.
                property_detail = property_details[1].find_all('li')
                address_line_1 = property_detail[0].text.strip()
                address_line_2 = property_detail[1].text.strip()
                city = property_details[2].text.strip()
                price = property_details[3].text.strip()
                bed = property_details[4].text
                bath = property_details[5].text
                property_type = property_details[6].text
                status = property_details[7].text
                url = 'https://reo.wellsfargo.com' + property_details[8].find('a', class_=re.compile("reo-link"))['href'].split('..')[1]

                # Concatenate details for a comprehensive description.
                details = property_type + " | " + bed + " Beds | " + bath + " Baths" 
                state1 = address_line_2.split(', ')[1].strip()
                state = state1.split(' ')[0].strip()
                zip = state1.split(' ')[1].strip()
                thumbnail = "https://4.bp.blogspot.com/-_HhuyBzBozA/UQRgshUOGAI/AAAAAAADpDU/-tZP2wh3-3w/s1600/Wells_Fargo_Logo9.jpeg"
                store_name = 'reo.wellsfargo.com'   

    except Exception as e:
        # Print any errors encountered during the web scraping process.
        print(e)


async def scrape_landandfarm(url='https://www.landandfarm.com/search/minnesota-land-for-sale/sort-newest'):
    """
    Asynchronously scrapes land and farm properties for sale in Minnesota from the Land and Farm website.

    Args:
    url (str): The URL of the Land and Farm website's Minnesota land for sale page.

    The function sets up a Selenium WebDriver to interact with the website, scrolls through the webpage to load all listings,
    and then scrapes details such as acres, price, URL, address, and more for each property. It handles exceptions and closes 
    the WebDriver upon completion.
    """
    # Initialize the Chrome WebDriver with specified options for compatibility and performance.
    s = Service(config.chromedriver_path)
    chromeOptions = webdriver.ChromeOptions() 
    chromeOptions.add_argument("--no-sandbox")  # Bypass the OS security model, usually required in containerized environments.
    chromeOptions.add_argument("--disable-gpu")  # Disable GPU hardware acceleration if it's not needed.
    driver = webdriver.Chrome(options=chromeOptions, service=s) 

    try:   
        # Navigate to the specified URL.
        driver.get(url)
        driver.implicitly_wait(25)  # Wait for the page elements to load.
       
        # Scroll through the webpage to ensure all properties are loaded.
        SCROLL_PAUSE_TIME = 0.5
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 5):
            driver.execute_script("window.scrollTo(0, {});".format(i))
        driver.implicitly_wait(25)  # Wait again after scrolling.

        # Get the page source and parse it using BeautifulSoup.
        squadPage = driver.page_source
        soup = bs4.BeautifulSoup(squadPage, 'html.parser')

        # Find all elements that represent property listings.
        properties = soup.find_all('div', class_="_8d3d6 d086e _153db")

        # Iterate through each property listing to extract details.
        for property in properties:
            # Initialize variables for extracted details.
            acres = None
            property_url = None
            address = None
            state = None
            postal = None
            county = None
            price = None
            thumbnail = None
            
            # Extract acres and price from the listing.
            acres_div = property.find('div', class_=re.compile("_0e5d5"))
            if acres_div:
                price = acres_div.text.strip().split('•')[0].strip()
                acres = acres_div.text.strip().split('•')[1].strip() if '•' in acres_div.text else None
            
            # Extract the URL and thumbnail image for the property.
            url_div = property.find('div', class_=re.compile("_12317"))
            if url_div:
                property_url = 'https://www.landandfarm.com' + url_div.find('a')['href']
                thumbnail = url_div.find('img', class_="_54fc3 _71f1f")['src']

            # Extract address details.
            address_div = property.find('div', class_=re.compile("_5707c"))
            if address_div:
                address_details = address_div.text.strip().split(',')
                if len(address_details) >= 4:
                    address = address_details[0].strip()
                    state = address_details[2].strip()
                    postal = address_details[3].strip()
                    city = address_details[1].strip()
                    county = address_details[4].strip() if len(address_details) > 4 else None

            # Construct the data tuple for the scraped property.
            data_homes = ('landandfarm.com', thumbnail, price, acres, property_url, 'Land', address, city, state, postal, county)

    except Exception as e:
        # Print any errors encountered during the web scraping process.
        print(e)
    finally:
        # Ensure the WebDriver is closed after the operation.
        driver.quit()


# Define an asynchronous function to scrape real estate listings from Realtor.com.
async def scrape_realtor(url='https://www.realtor.com/realestateandhomes-search/Minnesota/show-foreclosure/sby-1'):
    # Initialize the Chrome WebDriver with specific options.
    s = Service(config.chromedriver_path)
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--no-sandbox")  # Bypass OS security model, needed for certain environments.
    chromeOptions.add_argument("--disable-gpu")  # Disable GPU hardware acceleration.

    driver = webdriver.Chrome(options=chromeOptions, service=s)

    try:
        # Navigate to the specified URL.
        driver.get(url)
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be available.

        # Scroll through the page to load all the content.
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 5):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            time.sleep(0.05)  # Add a slight delay to ensure content loads.

        # Fetch the page source and parse it using BeautifulSoup.
        page_content = driver.page_source
        soup = bs4.BeautifulSoup(page_content, 'html.parser')

        # Select all property card elements from the page.
        property_cards = soup.select('.Cardstyles__StyledCard-rui__sc-6oh8yg-0')

        # Iterate over each property card to extract details.
        for card in property_cards:
            # Extract image URL, price, lot size, and other details from the card.
            img_url = card.find("img", {"data-testid": "picture-img"})["src"]
            price = card.find("div", {"data-testid": "card-price"}).text
            lot_size = card.find("li", {"data-testid": "property-meta-lot-size"}).span.text
            property_url = card.find("a", {"class": "LinkComponent_anchor__2uAhr"})["href"]
            full_address = card.find("div", {"data-testid": "card-address-1"}).text
            address_2 = card.find("div", {"data-testid": "card-address-2"}).text.split(", ")
            city = address_2[0]
            state, postal = address_2[1].split(" ")

            # County information is not provided in the HTML, so it's left empty.
            county = ""

            # Compile the extracted data into a tuple, ready for database insertion or other use.
            data_homes = ('realtor.com', img_url, price, lot_size, property_url, 'House', full_address, city, state, postal, county)
            
    except Exception as e:
        # Print any exceptions that occur during the web scraping process.
        print(f"Error scraping website: {e}")

    finally:
        # Ensure the WebDriver is closed after scraping to free resources.
        driver.close()
        driver.quit()


async def scrape_homepath(url='https://homepath.fanniemae.com/property-finder?bounds=43.499361,-97.239196,49.384358,-89.483812&state=MN'):
    """
    Asynchronously scrapes property listings from the HomePath Fannie Mae website.

    Args:
    url (str): The URL of the HomePath Fannie Mae website's property finder page.

    The function sets up a Selenium WebDriver to interact with the website, navigates to the specified URL,
    and scrapes details of each property listed. It extracts information like price, property type, address, and more. 
    It handles exceptions and ensures the WebDriver is closed properly.
    """
    # Initialize the Chrome WebDriver with specified options for compatibility and performance.
    s = Service(config.chromedriver_path)
    chromeOptions = webdriver.ChromeOptions() 
    chromeOptions.add_argument("--no-sandbox")  # Bypass the OS security model.
    chromeOptions.add_argument("--disable-gpu")  # Disable GPU hardware acceleration if it's not needed.
    driver = webdriver.Chrome(options=chromeOptions, service=s) 
    
    try:
        # Navigate to the specified URL.
        driver.get(url)
        time.sleep(5)  # Wait for 5 seconds to ensure the page has fully loaded.

        # Get the page source and parse it using BeautifulSoup.
        squadPage = driver.page_source
        soup = bs4.BeautifulSoup(squadPage, 'html.parser')

        # Find all elements that represent property listings.
        properties = soup.find_all('div', class_=re.compile("property-card"))

        # Iterate through each property listing to extract details.
        for property in properties:
            store_name = 'HomePath'  # Store name for the property listings.
            thumbnail = property.find('img')['src']  # Extract the thumbnail image URL.
            price = re.sub('\s+', ' ', property.find('span', class_=re.compile("price")).text).strip()  # Extract the price.
            property_type = re.sub('\s+', ' ', property.find('span', class_=re.compile("property-type")).text).strip()  # Extract the property type.
            details = re.sub('\s+', ' ', property.find('div', class_=re.compile("specifications")).text).strip()  # Extract property specifications.
            
            # Extract the address and split it into components.
            address = re.sub('\s+', ' ', property.find('div', class_=re.compile("address")).text).strip().split(',')
            address_line_1 = address[0].strip()
            address_line_1 = shared.uppercase_cardinal_directions(shared.capitalize_first_letter(address_line_1))  # Format the first line of the address.
            city = address[1].strip()
            state = address[2].split(' ')[1].strip()
            zip = address[2].split(' ')[2].strip()

            # Construct the URL for the individual property.
            url = 'https://www.homepath.fanniemae.com/cfl/property-detail/' + re.sub('\s+', ' ', property.find('button', class_=re.compile("button-favorite"))['id']).strip('card-')

            # Construct a primary key for the property, combining store name, details, and price.
            pk = store_name + '#' + details.replace(" ", "") + '#' + price
            county = ""  # County information isn't provided, so it's left empty.

            # Print the extracted details for each property.
            print(store_name)
            print(thumbnail)
            print(price)
            print(property_type)
            print(details)
            print(address_line_1)
            print(city)
            print(state)
            print(zip)
            print(url)
            print()

    except Exception as e:
        # Print any errors encountered during the web scraping process.
        print(e)
    finally:
        # Ensure the WebDriver is closed after scraping to free resources.
        driver.close()
        driver.quit()


async def scrape_autotempest(url='https://www.autotempest.com/results?zip=55374&radius=200'):
    """
    Asynchronously scrapes car listings from the AutoTempest website.

    Args:
    url (str): The URL of the AutoTempest search results page.

    The function sets up a Selenium WebDriver to interact with the website, scrolls through the webpage to load all car listings,
    and then scrapes details of each car listed, such as image URL, name, price, mileage, and more. It handles exceptions and
    ensures the WebDriver is closed properly.
    """
    # Initialize the Chrome WebDriver with default configurations.
    s = Service(config.chromedriver_path)
    driver = webdriver.Chrome(service=s)

    try:
        # Navigate to the specified URL.
        driver.get(url)

        # Scroll through the page to ensure all content is loaded.
        SCROLL_PAUSE_TIME = 0.5
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 10):
            driver.execute_script("window.scrollTo(0, {});".format(i))
        driver.implicitly_wait(25)  # Wait for content to load after scrolling.

        # Get the page source and parse it using BeautifulSoup.
        page_content = driver.page_source
        soup = bs4.BeautifulSoup(page_content, 'html.parser')

        # Find all elements that represent car listings.
        cars = soup.find_all('li', class_="result-list-item")

        # Iterate through each car listing to extract details.
        for car in cars:
            try:
                # Extract image URL, car name, price, mileage, etc.
                img = car.find('div', class_="image").get('data-img-fallback', 'N/A')
                name = car.find('span', class_='title-wrap').a.text if car.find('span', class_='title-wrap') and car.find('span', class_='title-wrap').a else 'N/A'
                price = car.find('div', class_='badge__labels').div.text if car.find('div', class_='badge__labels') and car.find('div', class_='badge__labels').div else 'N/A'
                mileage = car.find('span', class_='mileage').text if car.find('span', class_='mileage') else 'N/A'
                date = car.find('span', class_='date').text if car.find('span', class_='date') else 'N/A'
                city = car.find('span', class_='city').text if car.find('span', class_='city') else 'N/A'
                long_description = car.find('span', class_='extra-long').text if car.find('span', class_='extra-long') else 'N/A'
                short_description = car.find('span', class_='short').text if car.find('span', class_='short') else 'N/A'
                url = car.find('span', class_='more').a['href'] if car.find('span', class_='more') and car.find('span', class_='more').a else 'N/A'
                
                # Correct the URL if needed.
                if url.startswith("//"):
                    url = 'https:' + url
                elif url.startswith('/vehicle/carsoup/'):
                    url = 'https://www.autotempest.com' + url

                # Print the extracted details for each car.
                print(f"Name: {name}")
                print(f"Price: {price}")
                print(f"Image URL: {img}")
                print(f"Mileage: {mileage}")
                print(f"Date: {date}")
                print(f"City: {city}")
                print(f"Long Description: {long_description}")
                print(f"Short Description: {short_description}")
                print(f"URL: {url}")
                print("="*50)
            except Exception as e:
                # Print any errors encountered while processing an individual car listing.
                print(e)
    except Exception as e:
        # Print any errors encountered while fetching or parsing the car list page.
        print(e)
    finally:
        # Ensure the WebDriver is closed after scraping to free resources.
        driver.close()
        driver.quit()