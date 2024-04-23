from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementNotVisibleException,
    StaleElementReferenceException,
)
from selenium.common.exceptions import NoSuchElementException
import time

# import pandas as pd
import json
import os

from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

# Specify a specific version of the Chrome WebDriver
webdriver_version = "latest"  # or a specific version like "90.0.4430.24"
print(ChromeDriverManager(driver_version="120").install())
service = Service(ChromeDriverManager(driver_version="120").install())
# file_path = os.path.join(os.pardir, "proxy_utils", "valid_proxy_list.txt")
# with open(file_path, "r") as f:
#     # read valid proxies into array
#     proxies = f.read().split("\n")
proxies = []

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome(service=service, options=options)

stealth(
    driver,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=False,
    run_on_insecure_origins=False,
)


# UTIL AND NAV FUNCTIONS
"""READ ME _UTIL,NAV FUNCTIONS
navigate to next page - can be done using url or clicking page buttons
url for pagination: 
    https://www.etsy.com/search?q=pearl+keychain&ref=pagination&page=2

QUESTIONS:
    what if there isnt page number n? how to handle that - like if theres only 3 pages and we try to request 4? 
    if this happens:
        etsy returns a page that says "we couldnt find any resutls for pearl keychain"
    we would write conditonal logic to check for:
        -"we couldnt find any resutls for pearl keychain"
    at which point we know the page doesnt exist if we get this message
"""


def write_to_csv(file_path, data):
    pass


def get_next_page_req(next_page_num):
    """READ ME- FUNCTION DESCRIPTION
    Recieves next page num to visit, appends into url

    etsy has 21 page safety net -
        if last page is 230, and you request pg 250, it will reroute to 230,
        same if you req pg 251,
        but if you try pg 252 you get "page not found".
        and so on for any pages after range of +21 from last page

    """
    try:
        # store curr_url as prev_url before changing to new page
        prev_url = driver.current_url
        driver.get(
            f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={next_page_num}&ref=pagination"
        )
        # get curr_url after page change
        curr_url = driver.current_url

        """READ ME - LAST PAGE REDIRECT SAFETY NET
            if we are at page n and try to go to page n+1, if we are brought back to page n again - we could be in the '+21 page safety net redirect'
                try once more but with n+2 this time, if we are brought back to page n again, then we are in the safety net and page n is the LAST PAGE
        """
        # if we tried to navigate to new url and its still the same as prev_url
        if prev_url == curr_url:
            # page n+2 check
            driver.get(
                f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={next_page_num+2}&ref=pagination"
            )
            curr_url = driver.current_url
            # check again if new curr_url is still same as prev_url
            if prev_url == curr_url:
                return "last page reached"

        # check page for notice saying "page not found" - this means there are no more pages for this search
        # if this element is found, return message saying page DNE
        pg_not_found = driver.find_element(
            By.XPATH, "//p[@contains='We couldn't find any results for pearl keychain']"
        )
        if pg_not_found:
            return "Request Page DNE"

    except:
        pass


# TESTING
"""
assert function didnt throw any exceptions
assert url now has page num greater than prev url 
    Ex.
    compare:
        prev_url = (f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={2}&ref=pagination")
        curr_url = (f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={3}&ref=pagination")

"""
# term1 = 'busybabeshoppe'
# term2 = 'tote'

# # Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
# etsy_root_search_url = f'https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar'
# driver.get(etsy_root_search_url)
# print(get_next_page(250))


def scrape_results_listings(child_listing_objects, curr_pg_num):
    """READ ME

    Runs on Etsy Search result listings page
    Called for each search results page visited
    Populates child_listing_objects[] array
        each listing is encapsualted as an object and stored in the array for later use

        child_el is list element nested in parent OL
            title,price,listing_link are all extracted and put into a child_obj, which is put into a dict of child_objects

                Ex.
                child_listing_objects = [
                    {
                        'title':'Pearl keychain',
                        'price':'4.99',
                        'link':<link>},
                    }
                ]

    """

    try:
        # search_bar = driver.find_element(By.ID,"global-enhancements-search-query")
        # search_bar.send_keys(term1 + Keys.RETURN)

        time.sleep(3)
        # result_container_div = driver.find_element(By.CLASS_NAME,"wt-bg-white wt-display-block wt-pb-xs-2 wt-mt-xs-0")

        # get parent list of all listings
        listing_parent_list = driver.find_element(
            By.XPATH, "//ol[contains(@class,'wt-grid')]"
        )

        # from parent list, find all child elements
        child_listings = listing_parent_list.find_elements(
            By.CLASS_NAME, "wt-list-unstyled"
        )

        # FOR TESTING- shorten list for testing - REMOVE LATER
        child_listing_short = child_listings[:4]

        # #dict to hold child objects with desired values
        # child_listing_objects = []

        for child_el in child_listing_short:

            # GET STORE NAME, it doesnt work when combined as single statement
            # div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
            # print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)

            # free shipping indicator test - collect and mark if store offers free shipping
            promotion_badge_line = driver.find_element(
                By.CLASS_NAME, "promotion-badge-line"
            )
            # print(promotion_badge_line.text)
            free_shipping_bool = driver.find_element(
                By.XPATH,
                "//span[contains(@class,'wt-text-grey') and .//*[text()='Free shipping'])",
            )
            print(free_shipping_bool.text)

            # child_obj = {
            #     'title':child_el.find_element(By.CLASS_NAME,"v2-listing-card__title").get_attribute('title'),
            #     'price':child_el.find_element(By.CLASS_NAME,"lc-price").text,
            #     'listing_link': child_el.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
            #     # 'store_name': div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
            #     #             print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)
            #     # 'free_shipping':
            # }
            # print(f"{child_obj} \n ----------  \n")
            # child_listing_objects.append(child_obj)
            # # print(child_listing_objects)

    except NoSuchElementException as e:
        print(e)


def scrape_results_listings_url(child_listing_objects, curr_pg_num):
    """READ ME

    Runs on Etsy Search result listings page
    Called for each search results page visited
    Populates child_listing_objects[] array
        each listing is encapsualted as an object and stored in the array for later use

        child_el is list element nested in parent OL
            title,price,listing_link are all extracted and put into a child_obj, which is put into a dict of child_objects

                Ex.
                child_listing_objects = [
                    {
                        'title':'Pearl keychain',
                        'price':'4.99',
                        'link':<link>},
                    }
                ]

    """

    try:
        # search_bar = driver.find_element(By.ID,"global-enhancements-search-query")
        # search_bar.send_keys(term1 + Keys.RETURN)

        time.sleep(3)
        # result_container_div = driver.find_element(By.CLASS_NAME,"wt-bg-white wt-display-block wt-pb-xs-2 wt-mt-xs-0")

        # get parent list of all listings
        listing_parent_list = driver.find_element(
            By.XPATH, "//ol[contains(@class,'wt-grid')]"
        )

        # from parent list, find all child elements
        child_listings = listing_parent_list.find_elements(
            By.CLASS_NAME, "wt-list-unstyled"
        )

        # FOR TESTING- shorten list for testing - REMOVE LATER
        child_listing_short = child_listings[:4]

        # #dict to hold child objects with desired values
        child_listing_urls = []

        for child_el in child_listing_short:

            # GET STORE NAME, it doesnt work when combined as single statement
            # div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
            # print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)

            # free shipping indicator test - collect and mark if store offers free shipping
            promotion_badge_line = driver.find_element(
                By.CLASS_NAME, "promotion-badge-line"
            )
            # print(promotion_badge_line.text)
            free_shipping_bool = driver.find_element(
                By.XPATH,
                "//span[contains(@class,'wt-text-grey') and .//*[text()='Free shipping'])",
            )
            print(free_shipping_bool.text)

            child_obj = {
                "title": child_el.find_element(
                    By.CLASS_NAME, "v2-listing-card__title"
                ).get_attribute("title"),
                "price": child_el.find_element(By.CLASS_NAME, "lc-price").text,
                "listing_link": child_el.find_element(
                    By.CSS_SELECTOR, "a"
                ).get_attribute("href"),
                # 'store_name': div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
                #             print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)
                # 'free_shipping':
            }
            # print(f"{child_obj} \n ----------  \n")
            child_listing_urls.append(
                child_el.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
            )
            return child_listing_urls
    except NoSuchElementException as e:
        print(e)


# #TESTING
# term1 = 'busybabeshoppe'
# term2 = 'keychain'

# # Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
# etsy_root_search_url = f'https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar'
# driver.get(etsy_root_search_url)
# time.sleep(2)
# test_array = []
# scrape_results_listings(test_array)


def getlistingURLs(etsy_root_search_url, num_pages=3):

    # term1 = "busybabeshoppe"
    # term2 = "tote"

    # # Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
    # etsy_root_search_url = (
    #     f"https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar"
    # )

    proxy_counter = 0
    proxy_pg_limit = 3  # num_pages / 3
    urls = []

    try:
        # add proxy to chrome options
        # options.add_argument(f"--proxy-server={proxies[proxy_counter]}")
        # #navigate to root search URL
        # driver.get(etsy_root_search_url)
        # root url counts as page 1
        curr_pg_num = 0
        proxy_pg_count = 0

        # dict to hold child objects with scraped values
        child_listing_objects = []

        # curr pg = 1, we are on first page of search results
        while curr_pg_num < num_pages:

            try:
                driver.get(etsy_root_search_url)

                # if we reached page limit for current proxy, load new proxy from list ahead of new scrape
                # otherwise do nothing and skip to scrape
                if proxy_pg_count == proxy_pg_limit:

                    # if we are at last proxy in list, reset proxy_counter back to 0 - puts us back at beginnng of proxy list
                    # otherwise do nothing and skip to next block
                    if proxy_counter == len(proxies):
                        proxy_counter == 0

                    # get next proxy in list
                    proxy_counter += 1
                    # options.add_argument(f"--proxy-server={proxies[proxy_counter]}")
                    # reset pg count for new proxy
                    proxy_pg_count = 0

                # scrape with current proxy
                urls = scrape_results_listings_url(child_listing_objects, curr_pg_num)

                # increment pg visit count for current proxy
                proxy_pg_count += 1

                # increment page count ahead of visiting next page
                curr_pg_num += 1
                time.sleep(10)
                get_next_page_req(curr_pg_num)

            except:
                print("Error")
                break

        # write child_listing_obj to csv
        # print(child_listing_objects)
        # # Convert the array to a Pandas DataFrame
        # df = pd.DataFrame(child_listing_objects)

        # # Save the DataFrame to a CSV file
        # df.to_csv("scraped_listings.csv", index=False)

        # Write the array of objects to the JSON file
        # output_file = "scraped_listings.json"
        # with open(output_file, "w") as json_file:
        # json.dump(child_listing_objects, json_file, indent=4)

        # print("Data has been written to", output_file)
        return urls
    except:
        pass


# main_driver()


def getlistingInfos(etsy_root_search_url, num_pages=3):

    # term1 = "busybabeshoppe"
    # term2 = "tote"

    # # Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
    # etsy_root_search_url = (
    #     f"https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar"
    # )

    proxy_counter = 0
    proxy_pg_limit = 3  # num_pages / 3

    try:
        # add proxy to chrome options
        # options.add_argument(f"--proxy-server={proxies[proxy_counter]}")
        # #navigate to root search URL
        # driver.get(etsy_root_search_url)
        # root url counts as page 1
        curr_pg_num = 0
        proxy_pg_count = 0

        # dict to hold child objects with scraped values
        child_listing_objects = []

        # curr pg = 1, we are on first page of search results
        while curr_pg_num < num_pages:

            try:
                driver.get(etsy_root_search_url)

                # if we reached page limit for current proxy, load new proxy from list ahead of new scrape
                # otherwise do nothing and skip to scrape
                if proxy_pg_count == proxy_pg_limit:

                    # if we are at last proxy in list, reset proxy_counter back to 0 - puts us back at beginnng of proxy list
                    # otherwise do nothing and skip to next block
                    if proxy_counter == len(proxies):
                        proxy_counter == 0

                    # get next proxy in list
                    proxy_counter += 1
                    # options.add_argument(f"--proxy-server={proxies[proxy_counter]}")
                    # reset pg count for new proxy
                    proxy_pg_count = 0

                # scrape with current proxy
                scrape_results_listings(child_listing_objects, curr_pg_num)

                # increment pg visit count for current proxy
                proxy_pg_count += 1

                # increment page count ahead of visiting next page
                curr_pg_num += 1
                time.sleep(10)
                get_next_page_req(curr_pg_num)

            except:
                print("Error")
                break

        # write child_listing_obj to csv
        # print(child_listing_objects)
        # # Convert the array to a Pandas DataFrame
        # df = pd.DataFrame(child_listing_objects)

        # # Save the DataFrame to a CSV file
        # df.to_csv("scraped_listings.csv", index=False)

        # Write the array of objects to the JSON file
        # output_file = "scraped_listings.json"
        # with open(output_file, "w") as json_file:
        # json.dump(child_listing_objects, json_file, indent=4)

        # print("Data has been written to", output_file)
        return json.dumps(child_listing_objects, indent=4)

    except:
        pass


# main_driver()
