#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : medium_posts.py
# description   : crawl from medium.com and convert to markdown
###############################################################################

import os
import sys
import datetime
import requests
from selenium import webdriver

post_link = str(sys.argv[1])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + driver.capabilities['version'] + " Safari/537.36" 

driver.get(post_link)

title = driver.find_element_by_xpath("//h1").text
print(title)
author = driver.find_element_by_xpath("//a[@rel='author']").text
print(author)
created_date = driver.find_element_by_xpath("//div[@class='ui-caption postMetaInline u-fontSize13 u-lineHeightBase js-testPostMetaInlineSupplemental']/time").get_attribute("datetime")
print(created_date)
arr_paragraphs = driver.find_elements_by_xpath("//div[@id='content-main']/p | //div[@id='content-main']/blockquote | //div[@id='content-main']/div[@class='wp-caption aligncenter']/a/img")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/luatkhoa_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   exit()
else:
   f = open(str(file_name), "a")
   
   main_img_link = driver.find_element_by_xpath("//img[@class='progressiveMedia-image js-progressiveMedia-image']").get_attribute("src")
   main_img_name = main_img_link[main_img_link.rfind("/")+1:]
   local_img_link = os.path.join(img_path, main_img_name)
   urllib.request.urlretrieve(main_img_link, local_img_link)
   
   f.write("## " + title + "\n")
   try:
      main_img_caption = driver.find_element_by_xpath("//div[@id='post-feat-img']/div[@class='post-feat-text']/span").text
      f.write("![" + main_img_caption + "](../img/" + main_img_name + ")\n\n")
   except:
      f.write("![](../img/" + main_img_name + ")\n\n")

   f.write(post_link + "\n\n")
   f.write(author + "\n\n")
   f.write(created_date + "\n\n")
   
   for i in range(len(arr_paragraphs)):
      src = arr_paragraphs[i].get_attribute("src")
      if src is None:
         try:
            strong = arr_paragraphs[i].find_element_by_xpath("./span/strong")
            f.write("### " + strong.text + "\n\n")
         except:
            try:
               nested_img = arr_paragraphs[i].find_element_by_xpath(".//a/img")
               src_nested_img = nested_img.get_attribute("src")
               nested_img_name = src_nested_img[nested_img_name.rfind("/")+1:]
               local_nested_img_link = os.path.join(img_path, nested_img_name)
               urllib.request.urlretrieve(src_nested_img, local_nested_img_link)
               f.write("![](../img/" + nested_img_name + ")\n\n")
               f.write("![](" + ")")
               f.write
            except:
               try:
                  quote = arr_paragraphs[i].find_element_by_xpath("./p")
                  f.write("> " + quote.text + "\n\n")
               except:
                  try:
                     span = arr.paragraphs[i].find_element_by_xpath("./span")
                     f.write(span.text + "\n\n")
                  except:
                     f.write(arr_paragraphs[i].text + "\n\n")
      else:
         try:
            caption = arr_paragraphs[i].find_element_by_xpath("../../p[@class='wp-caption-text']").text
         except:
            caption = ""
         para_img_name = src[src.rfind("/")+1:]
         local_para_img_link = os.path.join(img_path, para_img_name)
         urllib.request.urlretrieve(src, local_para_img_link)
         f.write("![" + str(caption) + "](../img/" + para_img_name + ")\n\n")

   f.close()

driver.quit()
