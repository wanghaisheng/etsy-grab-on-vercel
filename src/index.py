from fastapi import FastAPI

from src.dtos.ISayHelloDto import ISayHelloDto
from src.utils import *
from src.sel.script.scrape_kw import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}


@app.get("/etsy/{keyword}")
async def getEtsySel(keyword: str):
    search_url = getSearchUrl(keyword)
    counts = getPageCounts(search_url)
    driver = getChomium()
    urls = getlistingURLs(driver, search_url, num_pages=counts)
    infos = getlistingInfos(driver, search_url, num_pages=counts)
    return {"links": urls, "json": infos}


@app.get("/etsy/req/{keyword}")
async def getEtsyReq(keyword: str):
    search_url = getSearchUrl(keyword)
    counts = getPageCounts(search_url)
    urls = getlistingURLs(search_url, num_pages=counts)
    infos = getlistingInfos(search_url, num_pages=counts)
    return {"links": urls, "json": infos}
