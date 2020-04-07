#!/usr/bin/env python3

import re
import os
import sys
import pytz
import time
import random
import requests
import datetime
from lxml import html
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import fromstring

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
mummy = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=options)
user_agent = mummy.execute_script("return navigator.userAgent;")
mummy.close()

print(user_agent)

main_d = "/home/user/writing/theWebs/aeon_01"
article_d = main_d + "/articles"
imgs_d = main_d + "/images" 

# get link from argv

# check current index number in log file
#  idLog_path = main_d + "/index.log"
#  if not os.path.exists(log_path):
#      os.mknod(idLog_path)
#      cur_index = 0
#  else:
#      cur_index = open(idLog_path, "r").read().splitlines()[0]
# UNFINISHED: RECORD URL NAME

# crawl
alink = sys.argv[1]
aar = alink.split("/")
aname = aar[-1]     # string name from url
host = aar[2]
main_url = aar[0] + "//" + aar[2]

headers = { # specify headers for requests
      'Host': host,
      'Connection': 'keep-alive',
      'User-Agent': user_agent,
      'Accept': '*/*',
      'Referer': main_url + '/',
      'Accept-Language': 'en-US,en;q=0.9'
      }

main = requests.get(alink, headers=headers)
h = html.fromstring(main.content)

fname = article_d + "/" + aname + ".tex"    # write to tex file

global f
f = open(fname, "a")
f.writelines(
        ["\documentclass[../main.tex]{subfiles}", 
            "\n", 
            "\\begin{document}", 
            "\n"])
    
########################
# METADATA OF ARTICLES #
########################

if not os.path.exists(imgs_d + "/" + aname + ".jpg"):
    i_url = h.xpath("//div[@class='article-card__image-wrap']/figure")[0].attrib['style']
    print(i_url)
    img_url = i_url.split("'")[1]                                           # match only for background image
    il = requests.get(img_url)
    img = open(imgs_d + "/" + aname + ".jpg", 'wb')
    img.write(il.content)             # download to images folder
    img.close()

f.write("\chapterpicture{images/" + aname + ".jpg};\n")
# f.write("\\tikz[remember picture,overlay] \\node[opacity=0.4,inner sep=0pt,yshift=-5.5cm] at (current page.north){\includegraphics[scale=0.25]{images/" + aname + ".jpg}};\n")

title = h.xpath("//h1[@class='article-card__title']")[0].text.strip()              # title
f.writelines(["\chapter{" + title + "}", "\n"])
print(title)

f.write("\\begin{subtitle}\n")                                          # subtitle section
subt = h.xpath("//h2[@class='article-card__standfirst']")[0].text.strip()
print(subt)
f.write(subt + "\n")
f.write("\end{subtitle}\n\n")

f.write("\\begin{metadata}\n")                                          # start metadata section

date = h.xpath("//time[@class='article__date published']")[0].text.strip()      # date publish
print(date)
f.write(date + "\n\n")

banner_list = h.xpath("//div[@class='topics-banner']/a")                # array of topics banner
bt_list = []
for banner in banner_list:
    bt_list.append(banner.text)
banner_str = " - ".join(bt_list).strip()
print(banner_str)
f.write(banner_str + "\n\n")

author_list = h.xpath("//div[@class='article__body__author-details']")  # multiple authors
for author in author_list:
    tt = author.text_content()
    print(tt)
    f.write(tt + "\n")

# partner information if exists
#  xpath("//div[@class='article__body__partner-bio']")

wc = h.xpath("//p[@class='article__word-count']")[0].text.strip()                  # words count
f.write(wc + "\n")

editor = h.xpath("//p[@class='article__body__editor']")[0].text_content()            # editor
f.write(editor + "\n")

f.write("\end{metadata}\n\n")

########################
# WORK WITH PARAGRAPHS #
########################

def merge(a_tag, p_array):                  # add footnote and underline under the phrase
    try:
        a_href = a_tag.attrib['href']
        firstw_a = a_tag.text_content().split(" ")[0]     # first word in href
        lastw_a = a_tag.text_content().split(" ")[-1]     # last word in href
        for n, i in enumerate(p_array):          # find position of this word
            if i == firstw_a:
                p_array[n] = "\href{" + a_href + "}{" + p_array[n]              # hyper text
            if i == lastw_a:
                p_array[n] = p_array[n] + "}\\footnote{\\url{" + a_href + "}}"   # add footnote
    except KeyError:
        pass

def alpha_dcap(array):    # detect non-aphabetical char at beginning of paragraph array
    l = array[0][0]         # first character of paragraph
    if l.isalpha():
        return array[0][0], array[0][1:]    # manually cut the first char
    else:
        return array[0][0:2], array[0][2:]  # cut first 2 chars

def dcap(array):                # dch_span: list of dropcap <span> merge dropcap characters
    wa, nextw_a = alpha_dcap(array)
    array[0] = "\lettrine{" + wa + "}{" + nextw_a + "}"                         # insert lettrine into first word

# loop through all paragraphs
# search for available text decoration and url

e_list = h.xpath("//div[@class='has-dropcap']/p | //div[@class='has-dropcap']/blockquote")   # element list
for e in e_list:
    # seperate array to search for url or text decoration
    e_arr = e.text_content().split(" ")
    
    # check for leading dollar $ sign
    for ee_ind, ee in enumerate(e_arr):
        eel = list(ee)
        if eel[0] == "$":
            eel[0] = "\$"
            e_arr[ee_ind] = "".join(eel) 

    # check if LINK exists, put to footnote and underline that phrase
    ea = e.xpath("./a")    # list of url in this paragraph
    if ea == []:
        pass
    else:
        for a in ea:    # find this item from text inside the list
            merge(a, e_arr)         # then merge
     
    # check if LETTRINE words exist
    ind = e_list.index(e)
    la = e.xpath("./span[@class='ld-dropcap' or @class='drop']")
    if la != [] or ind == 0:
        dcap(e_arr)     # la[0] since la is a list
    else:
        pass

    # PULLQUOTE
    try:
        if e.attrib['class'] == "pullquote":
            e_arr.insert(0, "\\begin{pullquote}\n")
            e_arr.append("\n\end{pullquote}\n\n")
    except KeyError:    # key error with normal <p> tag
        e_arr.append("\n\n")

    # BLOCKQUOTE
    if e.tag == "blockquote":
        e_arr.insert(0, "\\begin{blockquote}\n")
        e_arr.append("\n\end{blockquote}\n\n")

    # furthur information
    # check if text nested in <em> tag
    
    # finally write p_arr to TEX file
    estr = " ".join(e_arr)
    print(estr)
    print("----------")
    f.write(estr)

f.write("\n\end{document}")
f.close() # finish writing to TEX file

# update index number in index file
#  i = open(idLog_path, "w")
#  i.write(cur_index)

