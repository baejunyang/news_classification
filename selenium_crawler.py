import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = '/Users/noah/Documents/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get("http://www.medipana.com/news/news_list_new.asp?MainKind=B&NewsKind=103&vCount=12&vKind=1")

tag_1 = driver.find_elements_by_css_selector('a.href')
print (len(tag_1))
# print (os.getcwd())

