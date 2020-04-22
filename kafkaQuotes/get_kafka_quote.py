#!/usr/bin/env python3
###############################################################################
# author        : Hoang Nguyen 
# email         : nvhhnvn@gmail.com
# script name   : get_kafka_quote.py
# description   : crawl all Franz Kafka quotes from GoodReads
###############################################################################

import os
import time
import random
import requests
from bs4 import BeautifulSoup

# directory for kafka quote after crawl
if not os.path.exists('/home/user/scripts/python/telegram/kafka'):
   os.makedirs('/home/user/scripts/python/telegram/kafka')

# the main url for the request to begin with
main_url = 'https://www.goodreads.com/author/quotes/5223.Franz_Kafka?page='

# set the safe header for the requests to be used
headers = {
      'Host': 'www.goodreads.com',
      'Connection': 'keep-alive',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
      'Accept': '*/*',
      'Referer': 'https://www.goodreads.com/author/quotes/5223.Franz_Kafka',
      'Accept-Language': 'en-US,en;q=0.9'
      }

# open text file then able to append
kaf = open('/home/user/scripts/python/kafka/kafka.txt', 'a+')

# loop through all 43 page of goodreads to get the quotes
for i in range(43):
    link = main_url + str(i+1)
    print(link)
    r = requests.get(link, headers=headers)
    html = BeautifulSoup(r.text, "html.parser")
    for qs in html.find_all("div", {"class": "quoteText"}):
        for span_child_qs in qs.find_all("span"):
            span_child_qs.decompose()
        for script_child_qs in qs.find_all("script"):
            script_child_qs.decompose()
        qst = qs.getText().rstrip().strip().strip('    ―')
        fortune_qst = "\n%\n". join(qst.split("\n"))
        #  print(fortune_qst)
        kaf.write(fortune_qst)

kaf.close()
