import requests


from bs4 import BeautifulSoup

from src.utils import *


def getListings(url, counts):

    a_product = Product("https://www.etsy.com/uk/listing/1479000279/item-title-1")
    a_product.connect()

    a_product.get_all_data()

    # return {"message": f"Hello {keyword}"}
    return a_product.generate_json()
