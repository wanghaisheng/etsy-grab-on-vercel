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

from selenium_stealth import stealth


with open("valid_proxy_list.txt", "r") as f:
    # read valid proxies into array
    proxies = f.read().split("\n")


bot_test_links = [
    "https://bot.sannysoft.com/",
    "https://bot.incolumitas.com/",
    "https://ipinfo.io/json",
]


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)


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


counter = 0


def bot_test(bot_test_links):
    for link in bot_test_links:
        try:
            options.add_argument(f"--proxy-server={proxies[counter]}")
            print(f"TRYING: {proxies[counter]}")
            driver.get(link)
            time.sleep(10)
        except:
            print(f"FAILED: {proxies[counter]}")

        finally:
            counter += 1
    counter = 0


def visit_links(links):
    for link in links:
        try:
            options.add_argument(f"--proxy-server={proxies[counter]}")
            print(f"TRYING: {proxies[counter]}")
            driver.get(link)
            time.sleep(10)
        except:
            print(f"FAILED: {proxies[counter]}")

        finally:
            counter += 1
    counter = 0


if __name__ == "__main__":
    pass

# time.sleep(5)
# driver.quit()


"""

what I need for stealth scraping:

proxy rotation so not all requests are coming through the same IP
    -probably rotating residential
        
random clicking

waits/sleeps

headers?
    
"""
