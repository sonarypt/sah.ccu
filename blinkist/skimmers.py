#!/usr/bin/env python3

import html
import html2markdown
import os
import random
import re
import requests
from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
#  chrome_options.add_argument('--window-size=1920,1080')
#  chrome_options.add_argument('--start-maximized')
#  chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)


# file contains list of books link
book_urls_file = "./data/book_urls.txt"

long_skim_dir = "./long_skim"
if not os.path.isdir(long_skim_dir):
    os.makedirs(long_skim_dir)

short_skim_dir = "./short_skim"
if not os.path.isdir(short_skim_dir):
    os.makedirs(short_skim_dir)

blinkist_homepage = "https://www.blinkist.com"

# check if file exists, if not create for append later


# LOGIN FIRST
# first need to login first

driver.get(blinkist_homepage)

print("Please login to process next step. You have 120 seconds to fill the information and solve the captcha.")
time.sleep(120)

# GET LONG/SHORT SKIMMING PARAGRAPHS OF EACH BOOK
# define function how to get the long/short skimming paragraphs from each book
short_skim_paths = open(book_urls_file, "r").read().splitlines()
for short_skim_path in short_skim_paths:
    
    # need to find a way how to name them
    book_name = short_skim_path.split("/")[-1]
    long_skim_file_path = long_skim_dir + "/" + book_name + ".md"
    short_skim_file_path = short_skim_dir + "/" + book_name + ".md"

    # check if long file exists, skip, else, continue to crawl
    if os.path.isfile(long_skim_file_path):
        continue
    else:
        f = open(long_skim_file_path, "a+")

        random_sleep_interval = random.randint(1,10)
        print("Sleep for " + str(random_sleep_interval) + " s.")
        time.sleep(random_sleep_interval)
        long_skim_path = short_skim_path.replace("/books/", "/nc/reader/")
        long_skim_url = blinkist_homepage + long_skim_path
        driver.get(long_skim_url)
        chapters = driver.find_elements_by_xpath("//article[@class='shared__reader__blink reader__container__content']/div[@data-chapterno]")
        for chapter in chapters:
            header = chapter.find_element_by_xpath("./h1")
            header_text = header.get_attribute('textContent')
            f.write("\n\n# " + header_text + "\n\n")
            chapter_content = chapter.find_element_by_xpath("./div[@class='chapter__content']")
            chapter_content_html = chapter_content.get_attribute("innerHTML")
            chapter_content_markdown = html.unescape(html2markdown.convert(chapter_content_html))
            f.write(chapter_content_markdown)
        f.close()

    # check if long file exists, skip, else, continue to crawl
    if os.path.isfile(short_skim_file_path):
        continue
    else:
        f = open(short_skim_file_path, "a+")

        random_sleep_interval = random.randint(1,10)
        print("Sleep for " + str(random_sleep_interval) + " s.")
        time.sleep(random_sleep_interval)
        short_skim_url = blinkist_homepage + short_skim_path
        driver.get(short_skim_url)
        divs = driver.find_elements_by_xpath("//div[@class='col-xs-12 col no-padding-xs']/div")
        for div in divs:
            attrb = div.get_attribute("ref")
            if attrb == "synopsis":
                f.write("\n\n# Synopsis \n\n")
            elif attrb == "who_should_read":
                f.write("\n\n# Who is it for? \n\n")
            elif attrb == "about_the_author":
                f.write("\n\n# About the author \n\n")

            div_text = div.get_attribute('innerHTML')
            div_md = html.unescape(html2markdown.convert(div_text))
            f.write(div_md)
        f.close()


# CAN WE REQUESTS ONLY?
# Actually, blinkist only hide other paragraphs through JS, HTML source shows all available paragraphs
# But requests cannot handle this task since Blinkist block autobot
# Thus selenium with initial login




# WRITE TO MARKDOWN WITH MARKUP
# Write to markdown with bold and headers settings so as to convert to docx file later




#

