# Extract PWS location details using Wunderground station ID
# Developed by  Akram Ali
# Updated on 2021-01-23

import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

station = 'KILCHICA692'

# Function to get location info from Wunderground
async def main(_dt):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.wunderground.com/dashboard/pws/%s' % station)
    await page.waitForSelector('a.location-name')
    location_HTML = await page.querySelectorEval('a.location-name', '(element) => element.outerHTML')
    await browser.close()
    return location_HTML

# get HTML of location info
location_HTML = asyncio.get_event_loop().run_until_complete(main(station))

# Parse HTML tags using BS4
soup = BeautifulSoup(location_HTML, 'lxml')
city_name = soup.get_text().replace(' Forecast for ', '').strip('')
for tag in soup.findAll('a', href=True):
    url = tag['href']
url = url.replace('/weather/', '')

print (city_name)
print (url)
