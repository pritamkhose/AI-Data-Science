# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:20:30 2021

@author: Pritam

pip install xmltodict

https://www.aakashweb.com/articles/google-news-rss-feed-url/

https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en

https://news.google.com/rss/search?q=infosys&hl=en-IN&gl=IN&ceid=IN:en

https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB

https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB/sections/CAQiYENCQVNRZ29JTDIwdk1EbHpNV1lTQldWdUxVZENHZ0pKVGlJUENBUWFDd29KTDIwdk1EbDVOSEJ0S2hvS0dBb1VUVUZTUzBWVVUxOVRSVU5VU1U5T1gwNUJUVVVnQVNnQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAVAB
"""

import os
import math
import numpy as np
import pandas as pd
import json
import requests
import xmltodict

BaseURL = 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB/sections/CAQiYENCQVNRZ29JTDIwdk1EbHpNV1lTQldWdUxVZENHZ0pKVGlJUENBUWFDd29KTDIwdk1EbDVOSEJ0S2hvS0dBb1VUVUZTUzBWVVUxOVRSVU5VU1U5T1gwNUJUVVVnQVNnQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAVAB?hl=en-IN&gl=IN&ceid=IN:en'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
page = requests.get(BaseURL, headers)
if(page.status_code == 200) :
    body = xmltodict.parse(page.content)
    newsList = body #['rss']['channel']['item']
    newsList = json.dumps(newsList)