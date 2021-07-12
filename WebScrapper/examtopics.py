# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 15:15:54 2021

@author: Pritam

pip install selenium 


"""

from bs4 import BeautifulSoup
import json
import pandas as pd
import math

from selenium import webdriver

def getListofQueURL():
    
    URL = 'https://www.examtopics.com/discussions/amazon/'
    pageArr = []
    for x in range(2,278):  # (2,278) min & max count
        pageArr.append(URL + str(x) + '/')
    
    aListURL = []
    browser = webdriver.Firefox(executable_path=r'E:\Software\Chromedriver\geckodriver.exe')
    
    for URL in pageArr:
        print(URL)
        try:
            browser.get(URL)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            
            # with open("examtopics.html", "w", encoding="utf-8") as file:
            #     file.write(str(html_source))
            # HtmlText = open("examtopics.html", 'r', encoding='utf-8').read()
            # soup = BeautifulSoup(HtmlText, 'html.parser')
            # print(str(soup.body))
            
            aDiv = soup.find("div", {"class": "container-fluid discussion-list"})
            for row in aDiv.findAll('div', {"class": "row discussion-row"}):
    
                reply = row.find("div", {"class": "discussion-stats-replies"}).text.replace("Replies", "").strip()
                views = row.find("div", {"class": "discussion-stats-views d-none d-lg-inline-block"}).text.replace("Views", "").strip()
                username = row.find("a", {"class": "title-username"}).text.strip()
                posttime = row.find("span", {"class": "recent-post-time"}).text.strip()
    
                aurl = row.find("a", {"class": "discussion-link"})
                if(aurl['href'] != ''):
                    aListURL.append({'name': aurl.string.replace("\n", "").strip(), 'url': aurl['href'], 'reply': reply, 'views': views, 'username': username, 'posttime': posttime })
        except Exception as e:
            print(e)

    browser.close()
    with open('examtopics.json', 'w', encoding='utf-8') as f:
        json.dump(aListURL, f, ensure_ascii=False, indent=2)   

# getListofQueURL()

# df =  pd.DataFrame(json.loads(open("examtopics all.json", 'r', encoding='utf-8').read()))
# dfsort = df.drop_duplicates( keep='first', inplace=False)


def getListofQueAnswer():
    index = 0 
    aListQueAns = []
    aListURLArr = json.load(open('examtopics.json'))
    browser = webdriver.Firefox(executable_path=r'E:\Software\Chromedriver\geckodriver.exe')
    for URLobj in aListURLArr: # [500:691]
        index += 1
        print(str(index))
        
        try:
            browser.get("https://www.examtopics.com" + URLobj['url'])
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            
            # html_source = browser.page_source
            # with open("examtopics.html", "w", encoding="utf-8") as file:
            #     file.write(str(html_source))
            # HtmlText = open("examtopics.html", 'r', encoding='utf-8').read()
            # soup = BeautifulSoup(HtmlText, 'html.parser')
            
            ArrChoice = []
            URLobj['queanshtml'] = str(soup.find("div", {"class": "discussion-header-container"}))
            aListURLArr = soup.findAll("li", {"class": "multi-choice-item"})
            for URLobjchoice in aListURLArr: 
                ArrChoice.append(str(URLobjchoice.text.strip()))
            que = soup.find("div", {"class": "question-body mt-3 pt-3 border-top"})
            queArr = que.findAll('p', {"class": "card-text"})
            ArrQue = []
            for quesobj in queArr: 
                ArrQue.append(str(quesobj.text.strip()))
            URLobj['que'] = ArrQue
            URLobj['que_header'] = str(soup.find("div", {"class": "question-discussion-header"}))
            URLobj['ans'] = soup.find("span", {"class": "correct-answer-box"}).text
            URLobj['ans_details'] = soup.find("span", {"class": "answer-description"}).text  # not showing
                
            aListQueAns.append(URLobj)
            
            if(index%100 == 0):
                with open('examtopicsListQueAns.json', 'w', encoding='utf-8') as f:
                    json.dump(aListQueAns, f, ensure_ascii=False, indent=2)   
        except Exception as e:
            print(e)
            
    with open('examtopicsListQueAns.json', 'w', encoding='utf-8') as f:
        json.dump(aListQueAns, f, ensure_ascii=False, indent=2)   
    browser.close()


# getListofQueAnswer()

data = json.load(open('examtopicsListQueAns Final.json', 'r', encoding='utf-8'))
# with open('examtopicsListQueAns Final small.json', 'w', encoding='utf-8') as f:
#         json.dump(data[0:500], f, ensure_ascii=False)   
# df = pd.DataFrame(data)
index = 0
datalen = len(data)
size = 300
dataspilt = math.ceil(datalen/size)
for obj in range(dataspilt):
    index += 1
    array = data[((index-1)*size):(index*size)]
    with open('examtopics-'+str(index)+'.json', 'w', encoding='utf-8') as f:
        json.dump(array, f, ensure_ascii=False)   
    print(str(index) + ' - ' + str(len(array)))

