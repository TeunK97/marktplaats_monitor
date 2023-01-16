from scrapingFuncs import Scraper
from fileMonitor import fileMonitor
from telegramBot import telegramNotifications
import time
import json
import asyncio
## This is a test line
import sys

async def main(args):
    CONFIG = getConfigFromFile()
    fileWatcher = fileMonitor()
    print("we found {} query.".format(len(fileWatcher.getFiles())))
    notifications = telegramNotifications(CONFIG['telegram_api_token'],CONFIG['telegram_chat_id'])
    scraper = Scraper(CONFIG['webdriverpath'])
    try:
        while True:
            files = fileWatcher.getFiles()
            for file in files:
                query = files[file]['query']
                filepath = files[file]['listing_filepath']
                await check_for_updates(filepath, query, scraper, notifications)
            time.sleep(CONFIG['scanning_interval'])
    except KeyboardInterrupt:
        exit()

def getConfigFromFile():
    with open('config.json' , "r") as json_file:
        config = json.load(json_file)
        json_file.close()
    return config

async def check_for_updates(filename, url, scraper, notifications):
    listings, filtered = scraper.Scrape(url)
    new_listings = scraper.compareScrapes(listings, filename)
    print("{} new listings found for {}".format(len(new_listings), filename))
    for new_listing in new_listings:
        data = new_listings[new_listing]
        title = 'New: ' + data['title']
        message = data['description'] + "\n\nPrice: " + data['price'] + "\n\nLocation: " + data['location']
        link = data['url']
        link_title = 'Open in browser'
        print(f"""
        {title}\n
        {message}\n
        {link}\n
        {link_title}\n
        """)
        await notifications.notif(title, message, link, link_title)
    scraper.saveScrapes(listings, filename)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
