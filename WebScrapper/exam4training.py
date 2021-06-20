# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 22:07:36 2021

@author: Pritam

https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source

pip install selenium 

https://www.exam4training.com/amazon/exam-aws-solution-architect-associate-aws-certified-solutions-architect-associate/
https://www.exam4training.com/amazon/exam-aws-solution-architect-associate-aws-certified-solutions-architect-associate/page/2/

"""
# import requests
from bs4 import BeautifulSoup
import json

# headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405', 'Host': 'www.moneycontrol.com'}
# page = requests.get(URL, headers=headers)
# soup = BeautifulSoup(page.content, 'html.parser')
# with open("exam4training.html", "w", encoding="utf-8") as file:
#     file.write(str(soup.body))

from selenium import webdriver

def getListofQueURL():
    
    URL = 'https://www.exam4training.com/amazon/exam-aws-solution-architect-associate-aws-certified-solutions-architect-associate/'
    pageArr = [URL]
    for x in range(1,70):  # 69 max count
        pageArr.append(URL + 'page/' + str(x) + '/')
    
    aListURL = []
    browser = webdriver.Firefox(executable_path=r'E:\Software\Chromedriver\geckodriver.exe')
    
    for URL in pageArr:
        print(URL)
        try:
            browser.get(URL)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            
            # with open("exam4training.html", "w", encoding="utf-8") as file:
            #     file.write(str(html_source))
            # HtmlText = open("exam4training.html", 'r', encoding='utf-8').read()
            # soup = BeautifulSoup(HtmlText, 'html.parser')
            # print(str(soup.body))
            
            aDiv = soup.find("main", {"class": "site-main"})
            for row in aDiv.findAll('article'):
                aurl = row.find("h2", {"class": "entry-title"}).find('a')
                if(aurl['href'] != ''):
                    aListURL.append({'name': aurl.string, 'url': aurl['href']})
        except Exception as e:
            print(e)

    browser.close()
    with open('exam4trainingList.json', 'w', encoding='utf-8') as f:
        json.dump(aListURL, f, ensure_ascii=False, indent=2)   

def getListofQueAnswer():
    index = 500 
    aListQueAns = []
    aListURLArr = json.load(open('exam4trainingList.json'))
    browser = webdriver.Firefox(executable_path=r'E:\Software\Chromedriver\geckodriver.exe')
    for URLobj in aListURLArr: # [500:691]
        index += 1
        print(str(index))
        
        try:
            browser.get(URLobj['url'])
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            
            URLobj['ques'] = soup.find("h1", {"class": "entry-title"}).string
            ans = (soup.find("main",{"class": "site-main"})).find('article')
            URLobjAnsArr = (ans.find("div", {"class": "entry-content"}).findAll('p'))
            URLobjAns = []
            for pdiv in URLobjAnsArr:
                URLobjAns.append(str(pdiv))
            URLobj['answer'] = URLobjAns
                
            aListQueAns.append(URLobj)
        except Exception as e:
            print(e)
            
    with open('exam4trainingListQueAns.json', 'w', encoding='utf-8') as f:
        json.dump(aListQueAns, f, ensure_ascii=False, indent=2)   
    browser.close()

getListofQueAnswer()