#!/usr/bin/python3

import requests, os, shutil
from bs4 import BeautifulSoup

main_url = input("Enter the link of the manga to be downloaded: ")
headers  = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/121.0.0.0 Safari/537.36"}

cap_list = []

site  = requests.get(main_url, headers=headers)
soup  = BeautifulSoup(site.content, "html.parser")
title = soup.find("h1").get_text()
desc  = soup.find("p").get_text()
tags  = []
path  = os.path.join(os.getcwd(),title)

for a in soup.find_all("a", rel="tag"):
    tags.append(a.get_text())

try:
    os.makedirs(path)
    print(path)

except:
    print("Error creating main folder.")

for i in soup.select("div.episodiotitle")[::-1]:
    cap_list.append(i.select_one("a").get("href"))
    print(i.select_one("a").get("href"))

for cap in cap_list:
    site = requests.get(cap, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    cap_title = soup.find("h1").get_text()

    try:
        os.makedirs(os.path.join(os.getcwd(),title,cap_title))
        print(os.path.join(path,cap_title))

    except:
        print(f"Error creating the '{cap_title}' folder")

    paginas = []
    count = 1

    for i in soup.select(".content img"):
        response = requests.get(i["src"], stream = True)
        path_cap = os.path.join(path,cap_title,f"{count:02}.png")
        print(path_cap)
        count = count + 1

        with open(path_cap, "wb") as file:
            shutil.copyfileobj(response.raw, file)
