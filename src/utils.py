import requests


from bs4 import BeautifulSoup


def getPageCounts(url):

    # Send a GET request to the Etsy search URL
    # url = "https://www.etsy.com/search?explicit=1&q=mahjong&order=price_desc"
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the pagination element
    pagination = soup.find("nav", class_="wt-pb-lg-2")

    if pagination:
        # Find all the page links within the pagination element
        page_links = pagination.find_all("a", class_="wt-btn")

        # Extract the page numbers from the links
        page_numbers = [
            link.text.strip() for link in page_links if link.text.strip().isdigit()
        ]

        # Get the last page number
        last_page = int(page_numbers[-1]) if page_numbers else 1

        print(f"Total pages: {last_page}")
        return last_page
    else:
        print("Pagination element not found.")


def getSearchUrl(keyword):
    etsy_root_search_url = ""
    if " " in keyword:
        terms = keyword.split(" ")
        querystring = ""
        for term in terms:
            querystring = querystring + f"%20{term}"
        etsy_root_search_url = (
            f"https://www.etsy.com/search?q={querystring}&ref=search_bar"
        )

    else:

        etsy_root_search_url = f"https://www.etsy.com/search?q={keyword}&ref=search_bar"
    return etsy_root_search_url
