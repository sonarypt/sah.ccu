#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : vnexpress_posts.py
# description   : crawl from vnexpress.net and convert to markdown
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

job = driver.find_element_by_xpath("//div[@class='box_author']/p[@class='author_name']/span").text
title = driver.find_element_by_xpath("//article/header/h1").text
author = driver.find_element_by_xpath("//div[@class='avata_box_author']/a/img").get_attribute("alt")
created_date = driver.find_element_by_xpath("//span[@class='time']").text
arr_paragraphs = driver.find_elements_by_xpath("//div[@class='fck_detail']/p")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/vnexpress_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")
   
   f.write("## " + title + "\n\n")
   f.write(post_link + "\n\n")
   
   author_img_link = driver.find_element_by_xpath("//div[@class='avata_box_author']/a/img").get_attribute("src")
   author_img_name = author_img_link[author_img_link.rfind("/")+1:]
   local_author_link = os.path.join(img_path, author_img_name)
   if not os.path.exists(local_author_link):
      r = requests.get(author_img_link, headers=headers)
      with open(local_author_link, 'wb') as image:
         image.write(r.content)
   
   f.write("![" + author + "](../img/" + author_img_name + ")\n\n")
   f.write(author + "\n\n")
   f.write(job + "\n\n")
   f.write(created_date + "\n\n")
   
   for i in range(len(arr_paragraphs)):
      try:
         bold = arr_paragraphs[i].find_element_by_xpath("./b | ./strong")
         f.write("*" + bold.text + "*\n\n")
      except:
         f.write(arr_paragraphs[i].text + "\n\n")
   
   f.close()

driver.quit()
