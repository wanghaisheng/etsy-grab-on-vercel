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
import requests
import tarfile

# file_path = os.path.join(os.pardir, "proxy_utils", "valid_proxy_list.txt")
# with open(file_path, "r") as f:
#     # read valid proxies into array
#     proxies = f.read().split("\n")
proxies = []


def getChomium():

    # from webdriver_manager.chrome import ChromeDriverManager

    # Specify a specific version of the Chrome WebDriver
    # URL of the tar file
    url = "https://github.com/Sparticuz/chromium/releases/download/v123.0.1/chromium-v123.0.1-pack.tar"

    # Download the tar file
    response = requests.get(url)

    # Save the tar file
    with open("chromium.tar", "wb") as file:
        file.write(response.content)

    # Extract the tar file
    with tarfile.open("chromium.tar", "r") as tar:
        tar.extract
    # Remove the tar file
    os.remove("chromium.tar")

    # Locate the WebDriver executable
    webdriver_path = os.path.join(os.getcwd(), "chromium-v123.0.1-pack", "chromedriver")
    from selenium.webdriver.chrom.service import Service

    # Create a Service object with the WebDriver path
    service = Service(webdriver_path)

    # file_path = os.path.join(os.pardir, "proxy_utils", "valid_proxy_list.txt")
    # with open(file_path, "r") as f:
    #     # read valid proxies into array
    #     proxies = f.read().split("\n")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--verbose")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=options)
    from selenium_stealth import stealth

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


def getEdge():
    options = webdriver.EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--verbose")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome(options=options)

    options.add_argument("--headless")

    options.use_chromium = True

    driver = webdriver.Edge(options=options)
