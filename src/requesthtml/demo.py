# https://github.com/psf/requests-html
from requests_html import HTMLSession

session = HTMLSession()
r = session.get("https://python.org/")
