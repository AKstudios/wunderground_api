# Download raw weather data from wunderground in a csv file
# Developed by  Akram Ali
# Updated on 2021-01-23

import asyncio
import pandas as pd
from pyppeteer import launch
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

start = '2021-1-1'
end = '2021-1-5'
station = 'KILCHICA692'

start_dt = datetime.strptime(start, '%Y-%m-%d')
end_dt = datetime.strptime(end, '%Y-%m-%d')
date_delta = (end_dt-start_dt).days + 1 # +1 includes the end date as well
dt = start_dt  # use temp variable so start date is preserved

# Function to get location info from Wunderground
async def location(_dt):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.wunderground.com/dashboard/pws/%s' % station)
    await page.waitForSelector('a.location-name')
    location_HTML = await page.querySelectorEval('a.location-name', '(element) => element.outerHTML')
    await browser.close()
    return location_HTML

# Function to get table from Wunderground for start date
async def table(_url, _dt):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.wunderground.com/history/daily/%s/date/%s' % (_url, _dt))
    await page.waitForSelector('span.test-.wu-unit.wu-unit-humidity.ng-star-inserted')
    # table = await page.querySelectorEval('table#history-observation-table', '(element) => element.outerHTML')
    table = await page.querySelectorEval('lib-city-history-observation', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]   # convert to table



# get HTML of location info
print ('Getting location data for ' + station)
location_HTML = asyncio.get_event_loop().run_until_complete(location(station))

# Parse HTML tags using BS4
soup = BeautifulSoup(location_HTML, 'lxml')
city_name = soup.get_text().replace(' Forecast for ', '').strip('')
for tag in soup.findAll('a', href=True):
    url = tag['href']
url = url.replace('/weather/', '')

# Run code for entire date range
print ('Extracting weather data from ' + start + ' to ' + end)
print ('Total no. of days: ' + str(date_delta))
for n in range(date_delta):
    date = str(dt.date())
    print (date)
    df = asyncio.get_event_loop().run_until_complete(table(url, date))
    df.to_csv('wunderground_%s.csv' % date, index=False)
    dt += timedelta(days=1)     # increment days by 1
    
print ('Done.')
