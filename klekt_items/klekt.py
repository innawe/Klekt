#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import csv
from bs4 import BeautifulSoup as bs
from datetime import datetime

s = requests.Session()

url = 'https://www.presentedbyklekt.com'
z = s.get(url)
soup = bs(z.text, "html.parser")
form = soup.find("input", {"name":"CSRFName"})["value"]
inp = soup.find("input", {"name":"CSRFToken", "type":"hidden"})["value"]

print("Checking e-mail and pass..")
with open('config.json') as data_file:
    data = json.load(data_file)

payload = {
    "CSRFName": form,
    "CSRFToken": inp,
    "page": "login",
    "action": "login_post",
    "email": data["email"],
    "password": data["pass"],
    "rememberMe": "on"
}
z2 = s.post(url, data=payload)
print(z2.status_code, "Logged in..")

user_product_url = "https://www.presentedbyklekt.com/user/items?load=all"
z1 = s.get(user_product_url)
soup1 = bs(z1.text, "html.parser")
all_divs = soup1.find_all("div", {"class":"k-panel k-panel-default"})

items = []

for index, x in enumerate(all_divs):
    i = index + 1
    a = x.find("a")["href"]
    b = x.find("img")["title"]
    c = x.find("span", {"class":"k-item--price"}).text.replace(u'\u20ac','').replace("\n","")
    d = x.find("span", {"class":"k-item--sizes"}).text
    my_dict = {'n': i, 'link': a, 'title': b, 'price': c, 'size':d}
    items.append(my_dict)
    with open('data.json', 'w') as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)
