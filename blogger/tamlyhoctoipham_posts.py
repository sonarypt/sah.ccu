#!/home/user/.py36/bin/python
###############################################################################
# author        : Hoang Nguyen 
#                 Université des sciences et des technologies de Hanoï (USTH)
# email         : zel.zsh@gmail.com
# script name   : tamlyhoctoipham_posts.py
# description   : crawl from tamlyhoctoipham.com and convert to markdown
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

title = driver.find_element_by_xpath("//div[@class='composs-main-article-content']/h1").text
author = driver.find_element_by_xpath("//div[@class='composs-main-article-meta']/a").text.replace("person","")
created_date = driver.find_element_by_xpath("//div[@class='composs-main-article-meta']/span[1]").text.replace("access_time","")
arr_paragraphs = driver.find_elements_by_xpath("//div[@class='shortcode-content']/blockquote | //div[@class='shortcode-content']/p | //div[@class='shortcode-content']/figure | //h2//span | //h3//span | //div[@class='shortcode-content']/ul | //div[@class='shortcode-content']/ol | //div[@class='shortcode-content']//div[@class='paragraph']/span | //div[@class='paragraph']/ul | //div[@class='shortcode-content']//div[@class='wsite-image wsite-image-border-none ']")
quote_contents = driver.find_elements_by_xpath("//blockquote")
h2_contents = driver.find_elements_by_xpath("//h2//span")
h3_contents = driver.find_elements_by_xpath("//h3//span")

year = datetime.datetime.now().year
month = datetime.datetime.now().month

if not os.path.exists("/home/user/journal/news/" + str(year) + "-" + str(month)):
   os.makedirs("/home/user/journal/news/" + str(year) + "-" + str(month))

file_name = "/home/user/journal/news/" + str(year) + "-" + str(month) + "/tamlyhoctoipham_" + author + "_" + title + ".md"
img_path = "/home/user/journal/news/img"

if os.path.exists(file_name):
   driver.quit()
   exit()
else:
   f = open(str(file_name), "a")
   
   main_img_link = driver.find_element_by_xpath("//div[@class='composs-main-article-media']/img").get_attribute("src")
   main_img_name = main_img_link[main_img_link.rfind("/")+1:]
   local_img_link = os.path.join(img_path, main_img_name)
   if not os.path.exists(local_img_link):
      r = requests.get(main_img_link, headers=headers)
      with open(local_img_link, 'wb') as image:
         image.write(r.content)
   
   f.write("## " + title + "\n")
   f.write("![](../img/" + main_img_name + ")\n\n")
   f.write(post_link + "\n\n")
   f.write(author + "\n\n")
   f.write(created_date + "\n\n")

   try:
      sum_detail = driver.find_element_by_xpath("//div[@class='composs-main-article-head']/p")
      f.write("> " + sum_detail.text + "\n\n")
   except:
      pass

   for i in range(len(arr_paragraphs)):
      if arr_paragraphs[i] in h2_contents:
         f.write("### " + arr_paragraphs[i].text + "\n\n")
      elif arr_paragraphs[i] in h3_contents:
         f.write("#### " + arr_paragraphs[i].text + "\n\n")
      elif arr_paragraphs[i] in quote_contents:
         span_list = arr_paragraphs[i].find_elements_by_xpath("./p/span")
         for j in range(len(span_list)):
            f.write("> " + span_list[j].text + "\n\n")
      else:
         items_list = arr_paragraphs[i].find_elements_by_xpath("./li")
         if len(items_list) > 0:
            for j in range(len(items_list)):
               # dont care much about h2, h3 nested in ol/li, xpath for //h2/span and //h3/span did that
               try:
                  f.write("- " + str(items_list[j].find_element_by_xpath("./span").text) + "\n\n")
               except:
                  pass
               try:
                  f.write("- " + str(items_list[j].text) + "\n\n")
               except:
                  pass
         else:
            span_list = arr_paragraphs[i].find_elements_by_xpath(".//span | .//ul")
            if len(span_list) > 0:
               for j in range(len(span_list)):
                  try:
                     img = span_list[j].find_element_by_xpath(".//img")
                     src = img.get_attribute("src")
                     if "?" in src:
                        src = src[:src.find("?")]
                     #  print(src)
                     img_name = src[src.rfind("/")+1:]
                     local_link = os.path.join(img_path, img_name)
                     if not os.path.exists(local_link):
                        r = requests.get(src, headers=headers)
                        with open(local_link, 'wb') as image:
                           image.write(r.content)
                     f.write("![](../img/" + img_name + ")\n\n")
                  except:
                     try:
                        bold = span_list[j].find_element_by_xpath(".//b | .//strong | .//em")
                        if bold.text == span_list[j].text:
                           f.write("*" + bold.text.strip() + "*\n\n")
                        else:
                           f.write(span_list[j].text + "\n\n")
                     except:
                        f.write(span_list[j].text + "\n\n")
            else:
               try:
                  img = span_list[j].find_element_by_xpath(".//img")
                  src = img.get_attribute("src")
                  if "?" in src:
                     src = src[:src.find("?")]
                  print(src)
                  img_name = src[src.rfind("/")+1:]
                  local_link = os.path.join(img_path, img_name)
                  if not os.path.exists(local_link):
                     r = requests.get(src, headers=headers)
                     with open(local_link, 'wb') as image:
                        image.write(r.content)
                  f.write("![](../img/" + img_name + ")\n\n")
               except:
                  f.write(arr_paragraphs[i].text + "\n\n")
   f.close()

driver.quit()
