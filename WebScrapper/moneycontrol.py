# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:15:56 2020

@author: Pritam
"""

import requests
from bs4 import BeautifulSoup

URL = 'https://www.moneycontrol.com/stocks/marketinfo/marketcap/nse/index.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#results = soup.find('table', class_='tbldata14 bdrtpg')
results = soup.find('td')
# print(soup)

i = 0
for a in soup.find_all('a', href=True):
    link = a['href']
    if "/india/stockpricequote/" in link:
        i = i + 1
        print(link)

# for job_elem in job_elems:
#    # Each job_elem is a new BeautifulSoup object.
#    # You can use the same methods on it as you did before.
#    title_elem = job_elem.find('h2', class_='title')
#    company_elem = job_elem.find('div', class_='company')
#    location_elem = job_elem.find('div', class_='location')
#    if None in (title_elem, company_elem, location_elem):
#        continue
#    print(title_elem.text.strip())
#    print(company_elem.text.strip())
#    print(location_elem.text.strip())
#    print('---------------------------')
