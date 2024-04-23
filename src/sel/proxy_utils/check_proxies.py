"use multiple threads to check if proxies work"



import threading
import queue
import requests
import os

q = queue.Queue()
valid_proxies = []


with open("proxy_list.txt","r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get(
                "http://ipinfo.io/json",
                proxies={"http":proxy,
                         "https:":proxy})
        except:
            continue

        if res.status_code == 200 and res.json()['country'] == 'US':
            print(f'US Proxy - Ok: {proxy}')
            valid_proxies.append(proxy)
        # country = res.json()['country']-
    # print(valid_proxies)   

            # if res.status_code == 200 and res.json()
    with open("valid_proxy_list.txt","w") as f:
        for line in valid_proxies:
            f.write(line + "\n")

# create 10 threads to check proxies
for _ in range(10):
    threading.Thread(target=check_proxies).start()


