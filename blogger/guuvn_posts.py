#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : guuvn_posts.py
# description   : crawl from guu.vn and convert to markdown
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

title = driver.find_element_by_xpath("//div[@class='featured-info']/h1[@class='title-detail']").text
print(title)
web_n_date = driver.find_element_by_xpath("//div[@class='featured-info']/h4[@class='meta-info-mini']").text
print(web_n_date)
author = driver.find_element_by_xpath("//h3[@class='guu-author-name-mini']/a").text
print(author)
arr_paragraphs = driver.find_elements_by_xpath("//article[@id='body']/p | //article[@id='body']/h3")
h_contents = driver.find_elements_by_xpath("//article[@id='body']/h3")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/guuvn_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")
   
   f.write("## " + title + "\n\n")
   f.write(post_link + "\n\n")
   
   author_img_link = driver.find_element_by_xpath("//div[@class='col-md-2 col-xs-2 col-sm-2 guu-avatar-mini']/img").get_attribute("src")
   print(author_img_link)
   author_img_name = author_img_link[author_img_link.rfind("/")+1:]
   local_author_link = os.path.join(img_path, author_img_name)
   if not os.path.exists(local_author_link):
      r = requests.get(author_img_link, headers=headers)
      with open(local_author_link, 'wb') as image:
         image.write(r.content)
   
   f.write("![" + author + "](../img/" + author_img_name + ")\n\n")
   f.write(web_n_date + "\n\n")
   f.write(author + "\n\n")
   
   sum_detail = driver.find_element_by_xpath("//h2[@class='summary-detail']/blockquote")
   f.write("### " + sum_detail.text + "\n\n")

   for i in range(len(arr_paragraphs)):
      list_img = arr_paragraphs[i].find_elements_by_xpath(".//img")
      print(list_img)
      if len(list_img) > 0:
         for j in range(len(list_img)):
            src = list_img[j].get_attribute("src")
            src_file_name = src[src.rfind("/")+1:]
            local_src_link = os.path.join(img_path, src_file_name)
            if not os.path.exists(local_src_link):
               r = requests.get(src, headers=headers)
               with open(local_src_link, 'wb') as image:
                  image.wirte(r.content)
            f.write("![](../img/" + src_file_name + ")\n\n")
      else:
         try:
            bold = arr_paragraphs[i].find_element_by_xpath("./b | ./strong | ./em")
            f.write("*" + bold.text + "*\n\n")
         except:
            if arr_paragraphs[i] in h_contents:
               f.write("### " + arr_paragraphs[i] + "\n\n")
            else:
               f.write(arr_paragraphs[i].text + "\n\n")
   
   f.close()

driver.quit()
