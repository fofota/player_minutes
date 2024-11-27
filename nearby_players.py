import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
import time  # To avoid overwhelming the server with requests

# List of URLs to scrape
URLS = [
    "https://www.transfermarkt.co.uk/hampton-amp-richmond-borough/leistungsdaten/verein/8820",
    "https://www.transfermarkt.co.uk/fc-farnborough/leistungsdaten/verein/4279",
    "https://www.transfermarkt.co.uk/afc-wimbledon/leistungsdaten/verein/3884",
    "https://www.transfermarkt.co.uk/fc-woking/leistungsdaten/verein/2796",
    "https://www.transfermarkt.co.uk/sutton-united/leistungsdaten/verein/3052",
    "https://www.transfermarkt.co.uk/dorking-wanderers/leistungsdaten/verein/52299",
    "https://www.transfermarkt.co.uk/slough-town/leistungsdaten/verein/11310",
    "https://www.transfermarkt.co.uk/aldershot-town/leistungsdaten/verein/3717",
    "https://www.transfermarkt.co.uk/maidenhead-united/leistungsdaten/verein/7123",
    "https://www.transfermarkt.co.uk/fc-wealdstone/leistungsdaten/verein/4117",
    "https://www.transfermarkt.co.uk/hemel-hempstead-town/leistungsdaten/verein/17980",
    "https://www.transfermarkt.co.uk/st-albans-city/leistungsdaten/verein/3826",
    "https://www.transfermarkt.co.uk/fc-boreham-wood/leistungsdaten/verein/3867",
    "https://www.transfermarkt.co.uk/fc-barnet/leistungsdaten/verein/2804",
    "https://www.transfermarkt.co.uk/oxford-city-fc/leistungsdaten/verein/22563",
    "https://www.transfermarkt.co.uk/fc-bromley/leistungsdaten/verein/8981",
    "https://www.transfermarkt.co.uk/fc-dagenham-amp-redbridge/leistungsdaten/verein/3696",
    "https://www.transfermarkt.co.uk/aveley-fc/leistungsdaten/verein/26658",
    "https://www.transfermarkt.co.uk/tonbridge-angels-fc/leistungsdaten/verein/14672",
    "https://www.transfermarkt.co.uk/welling-united/leistungsdaten/verein/7454",
    "https://www.transfermarkt.co.uk/dartford-fc/leistungsdaten/verein/4074",
    "https://www.transfermarkt.co.uk/ebbsfleet-united/leistungsdaten/verein/2797",
    "https://www.transfermarkt.co.uk/chelmsford-city/leistungsdaten/verein/3698",
    "https://www.transfermarkt.co.uk/maidstone-united/leistungsdaten/verein/7047",
    "https://www.transfermarkt.co.uk/southend-united/leistungsdaten/verein/2793",
    "https://www.transfermarkt.co.uk/eastleigh-fc/leistungsdaten/verein/10391",
    "https://www.transfermarkt.co.uk/worthing-fc/leistungsdaten/verein/8123",
    "https://www.transfermarkt.co.uk/braintree-town/leistungsdaten/verein/6340",
    "https://www.transfermarkt.co.uk/eastbourne-borough/leistungsdaten/verein/3713",
    "https://www.transfermarkt.co.uk/dover-athletic/leistungsdaten/verein/3936",
    "https://www.transfermarkt.co.uk/enfield-town/leistungsdaten/verein/8665",
    "https://www.transfermarkt.co.uk/fc-salisbury/leistungsdaten/verein/56852",
    "https://www.transfermarkt.co.uk/afc-hornchurch/leistungsdaten/verein/3868",
    "https://www.transfermarkt.co.uk/chesham-united/leistungsdaten/verein/9153",
]

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Delete existing CSV files in the folder
csv_files = glob.glob("*.csv")
for file in csv_files:
    os.remove(file)

# Initialize lists for storing the scraped data
player_names = []
positions = []
player_urls = []
ages = []
minutes_played = []
transfers = []
transfer_urls = []
heights = []
foots = []
birthplaces = []
main_positions = []
second_positions = []
third_positions = []
clubs = []
club_urls = []

# Base URL for Transfermarkt
BASE_URL = "https://www.transfermarkt.co.uk"

for URL in URLS:
    print(f"Processing URL: {URL}")  # Print the current URL for progress tracking
   
    # Start timing
    start_time = time.time()
   
    # Fetch the main page
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        continue

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract club name and club URL
    club_name = soup.find("h2", class_="content-box-headline").text.strip().replace("Squad ", "")
    club_url = soup.find("link", rel="canonical")["href"]

    # Locate the table containing player data
    table = soup.find("table", class_="items")

    # Iterate through table rows and extract data
    rows = table.tbody.find_all("tr")
    for row in rows:
        # Extract player name and URL
        name_cell = row.find("td", class_="hauptlink")
        if name_cell:
            name_link = name_cell.find("a")
            if name_link:
                player_name = name_link.text.strip()
                player_url = BASE_URL + name_link["href"]  # Combine base URL with href
            else:
                player_name = "Unknown"
                player_url = ""
        else:
            continue  # Skip rows without a player name

        # Extract player's position
        position_cell = row.find("td", class_="rueckennummer")
        if position_cell and "title" in position_cell.attrs:
            position = position_cell["title"]
        else:
            position = "Unknown"

        # Extract player's age
        zentriert_cells = row.find_all("td", class_="zentriert")
        if len(zentriert_cells) > 1:  # Ensure there are enough cells to access the age
            age_text = zentriert_cells[1].text.strip()
            if age_text.isdigit():
                age = int(age_text)
            else:
                age = None
        else:
            age = None

        # Extract minutes played
        minutes_cell = row.find("td", class_="rechts")
        if minutes_cell:
            minutes_text = minutes_cell.text.strip().replace(".", "").replace("'", "")
            if minutes_text.isdigit():
                minutes = int(minutes_text)
            else:
                minutes = 0
        else:
            minutes = 0

        # Extract transfer and transfer_url
        transfer_cell = row.find("span", class_="wechsel-kader-wappen")
        if transfer_cell:
            transfer_link = transfer_cell.find("a")
            if transfer_link:
                transfer = transfer_link.get("title", "").split(";")[0]  # Get the transfer info
                transfer_url = BASE_URL + transfer_link.get("href", "")  # Combine base URL with href
            else:
                transfer = "Unknown"
                transfer_url = ""
        else:
            transfer = "Unknown"
            transfer_url = ""

        # Fetch player's profile page for height, foot, birthplace, and positions
        height = None
        foot = "Unknown"
        birthplace = "Unknown"
        main_pos = "Unknown"
        second_pos = ""
        third_pos = ""

        if player_url:
            profile_response = requests.get(player_url, headers=HEADERS)
            if profile_response.status_code == 200:
                profile_soup = BeautifulSoup(profile_response.content, "html.parser")
                # Scrape height
                height_element = profile_soup.find("span", itemprop="height")
                if height_element:
                    height_text = height_element.text.strip()
                    height = height_text.replace(",", ".").replace(" m", "").strip()
                    try:
                        height = float(height)  # Convert to a float for easier processing
                    except ValueError:
                        height = None
                # Scrape foot
                foot_label = profile_soup.find("span", string="Foot:")
                if foot_label:
                    foot_value = foot_label.find_next("span", class_="info-table__content--bold")
                    if foot_value:
                        foot = foot_value.text.strip()
                # Scrape birthplace
                birthplace_element = profile_soup.find("span", itemprop="birthPlace")
                if birthplace_element:
                    birthplace = birthplace_element.text.strip()
                # Scrape positions
                main_pos_element = profile_soup.find("dd", class_="detail-position__position")
                if main_pos_element:
                    main_pos = main_pos_element.text.strip()
                other_pos_elements = profile_soup.find_all("dd", class_="detail-position__position")
                if len(other_pos_elements) > 1:
                    second_pos = other_pos_elements[1].text.strip()
                if len(other_pos_elements) > 2:
                    third_pos = other_pos_elements[2].text.strip()
            else:
                print(f"Failed to fetch player profile for {player_name}: {profile_response.status_code}")
            time.sleep(0.1)  # Avoid overwhelming the server with requests

        # Append data if valid
        player_names.append(player_name)
        positions.append(position)
        player_urls.append(player_url)
        ages.append(age)
        minutes_played.append(minutes)
        transfers.append(transfer)
        transfer_urls.append(transfer_url)
        heights.append(height)
        foots.append(foot)
        birthplaces.append(birthplace)
        main_positions.append(main_pos)
        second_positions.append(second_pos)
        third_positions.append(third_pos)
        clubs.append(club_name)
        club_urls.append(club_url)
        
        # End timing
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Processing {URL} in {elapsed_time:.2f} seconds")

# Remove duplicates by pairing names and minutes
unique_data = {}
for name, url, position, age, minutes, transfer, transfer_url, height, foot, birthplace, main_pos, second_pos, third_pos, club, club_url in zip(player_names, player_urls, positions, ages, minutes_played, transfers, transfer_urls, heights, foots, birthplaces, main_positions, second_positions, third_positions, clubs, club_urls):
    if name not in unique_data or unique_data[name]["minutes"] < minutes:
        unique_data[name] = {
            "url": url,
            "position": position,
            "age": age,
            "minutes": minutes,
            "transfer": transfer,
            "transfer_url": transfer_url,
            "height": height,
            "foot": foot,
            "birthplace": birthplace,
            "main_pos": main_pos,
            "second_pos": second_pos,
            "third_pos": third_pos,
            "club": club,
            "club_url": club_url,
        }

# Create a DataFrame
data = {
    "name": [],
    "position": [],
    "player_url": [],
    "age": [],
    "minutes": [],
    "transfer": [],
    "transfer_url": [],
    "height": [],
    "foot": [],
    "birthplace": [],
    "main_pos": [],
    "2nd_pos": [],
    "3rd_pos": [],
    "club": [],
    "club_url": [],
}
for name, details in unique_data.items():
    data["name"].append(name)
    data["position"].append(details["position"])
    data["player_url"].append(details["url"])
    data["age"].append(details["age"])
    data["minutes"].append(details["minutes"])
    data["transfer"].append(details["transfer"])
    data["transfer_url"].append(details["transfer_url"])
    data["height"].append(details["height"])
    data["foot"].append(details["foot"])
    data["birthplace"].append(details["birthplace"])
    data["main_pos"].append(details["main_pos"])
    data["2nd_pos"].append(details["second_pos"])
    data["3rd_pos"].append(details["third_pos"])
    data["club"].append(details["club"])
    data["club_url"].append(details["club_url"])

df = pd.DataFrame(data)

# Save to CSV with column headings
df.to_csv("players_minutes.csv", index=False, header=True)
print(df)