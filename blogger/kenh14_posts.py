#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : kenh14_posts.py
# description   : crawl from kenh14.vn and convert to markdown
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

title = driver.find_element_by_xpath("//h1[@class='kbwc-title']").text
author = driver.find_element_by_xpath("//span[@class='kbwcm-author']").text
source = driver.find_element_by_xpath("//span[@class='kbwcm-source']").text
created_date = driver.find_element_by_xpath("//span[@class='kbwcm-time']").text
arr_paragraphs = driver.find_elements_by_xpath("//div[@class='knc-content']/p | //div[@class='knc-content']/h3 | //div[@class='knc-content']/h2 | //div[@class='knc-content']/div[@type='Photo'] | //div[@class='knc-content']/div[@type='content']/div/p")
h_contents = driver.find_elements_by_xpath("//div[@class='knc-content']/h3 | //div[@class='knc-content']/h2")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/kenh14_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")
   
   f.write("## " + title + "\n\n")
   f.write(post_link + "\n\n")
   f.write(author + "\n\n")
   f.write(source + "\n\n")
   f.write(created_date + "\n\n")

   sapo = driver.find_element_by_xpath("//h2[@class='knc-sapo']").text
   f.write("### " + sapo + "\n\n")

   for i in range(len(arr_paragraphs)):
      try:
         img = arr_paragraphs[i].find_element_by_xpath("./div/a/img")
         src = img.get_attribute("src")
         src_file_name = src[src.rfind("/")+1:]
         local_src_link = os.path.join(img_path, src_file_name)
         if not os.path.exists(local_src_link):
            r = requests.get(src, headers=headers)
            with open(local_src_link, 'wb') as image:
               image.write(r.content)

         try:
            caption = arr_paragraphs[i].find_element_by_xpath("./div[@class='PhotoCMS_Caption']/p").text
         except:
            caption = ""
         f.write("![" + caption + "](../img/" + src_file_name + ")\n\n")
      except:
         try:
            bold = arr_paragraphs[i].find_element_by_xpath("./b | ./span/b | ./i/b | ./strong")
            if str(bold.text) == arr_paragraphs[i].text:
               f.write("*" + bold.text + "*\n\n")
            else:
               f.write(arr_paragraphs[i].text + "\n\n")
         except:
            if arr_paragraphs[i] in h_contents:
               f.write("### " + arr_paragraphs[i].text + "\n\n")
            else:
               f.write(arr_paragraphs[i].text + "\n\n")
   
   f.close()

driver.quit()
