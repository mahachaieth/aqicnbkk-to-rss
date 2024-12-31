import requests
from xml.etree.ElementTree import Element, SubElement, tostring

API_TOKEN = 'your_api_token'
CITY = 'your_city'
API_URL = f'https://api.waqi.info/feed/{CITY}/?token={API_TOKEN}'

def generate_rss_feed():
    # Fetch AQICN data
    response = requests.get(API_URL)
    data = response.json()

    if data.get('status') != 'ok':
        raise Exception(f"Error fetching data: {data.get('data')}")

    aqi = data['data']['aqi']
    city_name = data['data']['city']['name']
    time_updated = data['data']['time']['s']

    # Create RSS feed structure
    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')

    title = SubElement(channel, 'title')
    title.text = f'AQI for {city_name}'

    description = SubElement(channel, 'description')
    description.text = 'Real-time air quality information from AQICN'

    pub_date = SubElement(channel, 'pubDate')
    pub_date.text = time_updated

    item = SubElement(channel, 'item')
    item_title = SubElement(item, 'title')
    item_title.text = f'Current AQI: {aqi}'

    item_description = SubElement(item, 'description')
    item_description.text = f'The current AQI in {city_name} is {aqi}.'

    # Save to RSS file
    with open('rss_feed.xml', 'w') as f:
        f.write(tostring(rss, encoding='unicode'))

# Run the script
generate_rss_feed()
