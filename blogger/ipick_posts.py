#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : ipick_posts.py
# description   : crawl from ipick.vn and convert to markdown
###############################################################################

import os
import sys
import datetime
import requests
from selenium import webdriver

post_link = str(sys.argv[1])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + driver.capabilities['version'] + " Safari/537.36" 

driver.get(post_link)

title = driver.find_element_by_xpath("//article/header/h1").text
author = driver.find_element_by_xpath("//div[@class='author-name ']/div[@class='name']/a").get_attribute("title")
print(author)
created_date = driver.find_element_by_xpath("//div[@class='author-name ']/div/span[@class='posted-on']/time").text
arr_paragraphs = driver.find_elements_by_xpath("//article/div[@class='entry-content']/p")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/ipick_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")

   f.write("## " + title + "\n\n")
   f.write(post_link + "\n\n")
   f.write(author + "\n\n")
   try:
      job = driver.find_element_by_xpath("//div[@class='author-name ']/div[@class='job']/span").text
      f.write(job + "\n\n")
   except:
      pass
   f.write(created_date + "\n\n")
   
   for i in range(len(arr_paragraphs)):      
      try:
         span_p = arr_paragraphs[i].find_element_by_xpath(".//span")
         f.write(span_p.text + "\n\n")
      except:
         try:
            bold = arr_paragraphs[i].find_element_by_xpath("./b | ./strong")
            if str(bold.text) == str(n_text):
               f.write("### " + bold.text + "\n\n")
            else:
               f.write(arr_paragraphs[i].text + "\n\n")
         except:
            f.write(arr_paragraphs[i].text + "\n\n")
   
   f.close()

driver.quit()
