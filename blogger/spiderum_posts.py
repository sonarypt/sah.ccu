#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : spiderum_posts.py
# description   : crawl from spiderum.com and convert to markdown
###############################################################################

import urllib
import sys
import os
from selenium import webdriver

post_link = str(sys.argv[1])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + driver.capabilities['version'] + " Safari/537.36" 

driver.get(post_link)

title = driver.find_element_by_xpath("//div[@class='title']/h1").text
author = driver.find_element_by_xpath("//div[@class='author pull-left']/h3/a").text
arr_paragraphs = driver.find_elements_by_xpath("//div[@class='content']/div[@class='fr-element fr-view']/div")
arr_tags = driver.find_elements_by_xpath("//div[@class='tags']/ul/li")

#  print("file for writing is" + author + "_" + title + ".txt")

dir_name = "/home/user/documents/vanilla/spiderum_" + author + "_" + title 
file_name = "/home/user/documents/vanilla/spiderum_" + author + "_" + title + ".md"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")
   f.write("% " + title + "\n")
   f.write("% " + author + "\n")
   f.write(post_link + "\n")
   for i in range(len(arr_paragraphs)):
      a = driver.find_elements_by_xpath("//div[@class='content']/div[@class='fr-element fr-view']/div/figure")
      if len(a) == 0:
         line = str(arr_paragraphs[i].text)
         f.write(line + "\n")
      else:
         for e in a:
            link = e.get_attribute("src")
            file_name = link.split('/')[-1]
            #  full_directory =
            #  urllib.urlretrieve(link, full_directory)
   f.write("TAGS:")
   for i in range(len(arr_tags)):
      tag = str(arr_tags[i].text)
      f.write(tag + " | ")
   f.close()

driver.quit()
