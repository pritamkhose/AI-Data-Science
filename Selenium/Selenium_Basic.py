# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 21:12:19 2020

@author: Pritam

https://stackoverflow.com/questions/39428042/use-selenium-with-chromedriver-on-mac

MAC OS
brew install geckodriver
which geckodriver

brew install chromedriver
which chromedriver

pip install selenium
sudo pip3 install selenium

Windows
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

https://www.guru99.com/selenium-python.html#:~:text=Selenium%20is%20an%20open%2Dsource,with%20the%20browser%20through%20Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Step 1) Open Firefox 
browser = webdriver.Firefox(executable_path=r'/opt/homebrew/bin/geckodriver')
#browser = webdriver.Firefox(executable_path=r'E:\Software\Chromedriver\geckodriver.exe')

# Step 1) Open Chrome 
# browser = webdriver.Chrome(executable_path=r'/opt/homebrew/bin/chromedriver')
#browser = webdriver.Chrome(executable_path=r"E:\Software\Chromedriver\chromedriver.exe")

def facebook():
    # Step 2) Navigate to Facebook
    browser.get("http://www.facebook.com")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    username = browser.find_element_by_id("email")
    password = browser.find_element_by_id("pass")
    submit   = browser.find_element_by_id("u_0_b")
    username.send_keys("YOUR EMAILID")
    password.send_keys("YOUR PASSWORD")
    # Step 4) Click Login
    submit.click()
    page_title = browser.title
    assert page_title == "Facebook – log in or sign up"

def google():
    # Step 2) Navigate to Google
    browser.get("http://www.google.com")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    search = browser.find_element_by_class_name("gLFyf")
    search.send_keys("Pritam Khose")
    ## Step 4) Enter key Search
    search.send_keys(Keys.RETURN)
    wait = WebDriverWait( browser, 5 )
    page_title = browser.title
    print(page_title)
    assert page_title == "Pritam Khose - Google Search" # Chrome driver
#    assert page_title == "Google" # FireFox gecko driver
    

try:
    google()
    #facebook()
except:
    print("Something went wrong")
finally:
    print("finished")
    # Step 5) Close Browser
    browser.close()

