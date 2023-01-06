import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import parse
import time

class Scraper:

    def __init__(self, webdriverpath):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument("--start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        options.headless = True
        self.driver = webdriver.Chrome(webdriverpath, chrome_options=options)
        self.driver.set_window_size(1120,550)

    def Scrape(self, url):
        print("scrape function called")
        driver = self.driver
        webpage = driver.get(url)
        driver.implicitly_wait(5)
        listings = {}
        original_count = len(driver.find_elements(By.CSS_SELECTOR, ".hz-Listing.hz-Listing--list-item"))
        action = webdriver.ActionChains(driver)
        for element in driver.find_elements(By.CSS_SELECTOR, ".hz-Listing.hz-Listing--list-item"):
            listing = {}
            listing['title'] = element.find_element(By.CSS_SELECTOR, '.hz-Listing-title').get_attribute("innerText")
            listing['description'] = element.find_element(By.CSS_SELECTOR, ".hz-Listing-description.hz-text-paragraph").get_attribute("innerText")
            listing['price'] = element.find_element(By.CSS_SELECTOR, ".hz-Listing-price.hz-text-price-label").get_attribute("innerText")
            listing['seller'] = element.find_element(By.CSS_SELECTOR, ".hz-Listing-seller-name").get_attribute("innerText")
            listing['location'] = element.find_element(By.CSS_SELECTOR, ".hz-Listing-location").get_attribute("innerText")
            action.move_to_element(element).perform()
            driver.implicitly_wait(1)
            link = element.find_element(By.CLASS_NAME, "hz-Link")
            if link.get_attribute("href") == None:
                combined = listing['title'] + ' ' + listing['location']
                combined = parse.quote_plus(combined)
                url = f"https://www.marktplaats.nl/q/{combined}/#offeredSince:Vandaag|sortBy:SORT_INDEX|sortOrder:DECREASING|searchInTitleAndDescription:true"
                listing['url'] = url
                time.sleep(10)
            else:
                url = link.get_attribute("href")
                listing['url'] = url
                time.sleep(10)
            
            listings[url] = listing
        return listings, original_count - len(listings)
    
    def saveScrapes(self, listings, filename):
        with open(filename, "r") as json_file:
            listings_in_file = json.load(json_file)
            if isinstance(listings_in_file, dict):
                listings_in_file.update(listings)
            else:
                listings_in_file = listings
            json_file.close()
        with open(filename, "w") as json_file:
            json.dump(listings_in_file, json_file)
            json_file.close()
        
    def compareScrapes(self, listings, filename):
        with open(filename, "r") as json_file:
            new_listings = {}
            saved_listings = json.load(json_file)
            json_file.close()
            for listing in listings:
                is_new = True
                for saved_listing in saved_listings:
                    if listing == saved_listing:
                        is_new = False
                if is_new:
                    new_listings[listing] = listings[listing]
            return new_listings
        

