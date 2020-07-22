#!/usr/bin/env python3

import glob
import html
import html2markdown
import os
import random
import re
import requests
from selenium import webdriver
import shutil
import time

chrome_options = webdriver.ChromeOptions()
#  chrome_options.add_argument('--window-size=1920,1080')
#  chrome_options.add_argument('--start-maximized')
#  chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

def check_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d)

def check_move(f1, f2):
    if os.path.isfile(f1):
        shutil.move(f1, f2)


blinkist_homepage = "https://www.blinkist.com"
categories_list_file = "./data/categories_list.txt"
categories_dir = "./categorized"
list_dir = "./list"

# MAKE DIR IF CATEFORIES DIR DOES NOT EXIST
check_dir(list_dir)
check_dir(categories_dir)

downloaded_books_name_1 = [i.split("/")[-1].split(".")[0].split("_")[0] for i in glob.glob("*/*/*/*.md")]
downloaded_books_name_2 = [i.split("/")[-1].split(".")[0] for i in glob.glob("*/*.md")]
downloaded_books_name = list(dict.fromkeys(downloaded_books_name_1 + downloaded_books_name_2))

driver.get(blinkist_homepage)

print("Please login to process next step. You have 120 seconds to fill the information and solve the captcha.")
time.sleep(122)

# GET CATEGORIES NAME FROM LIST FILE, THEN GET ALL THE BOOKS LIST FROM THE FULL LINK
categories_list = open(categories_list_file, "r").read().splitlines()
for category in categories_list:
    print("CATEGORY: " + category)
    category_dir = categories_dir + "/" + category
    check_dir(category_dir)
    
    category_data_file = list_dir + "/" + category + ".txt"
    if os.path.isfile(category_data_file):
        print("This category exists")
    else:
        category_site = blinkist_homepage + "/en/nc/categories/" + category + "/books"
        driver.get(category_site)
        category_books_links = driver.find_elements_by_xpath("//a[@class='letter-book-list__item']")
        f = open(category_data_file, "a+")
        for a in category_books_links:
            book_name = a.get_attribute("href").split("/")[-1]
            f.write(book_name + "\n")
        f.close()
        print("Downloaded books list from this category")
        time.sleep(2)

    category_books_list = open(category_data_file, "r").read().splitlines()
    for book_name in category_books_list:
        print("Checking " + book_name + ": ", end = "")
        book_dir = category_dir + "/" + book_name
        check_dir(book_dir)
        
        # MOVE EXISTING FILES FROM MAIN FOLDER TO SPECIFIC FOLDER
        if book_name in downloaded_books_name:
            print("Exists => Moved file.")
            
            check_move("./long_skim/" + book_name + ".md", 
                    book_dir + "/" + book_name + "_long.md")
            check_move("./short_skim/" + book_name + ".md", 
                    book_dir + "/" + book_name + "_short.md")
            check_move("./long_skim_docx/" + book_name + ".docx", 
                    book_dir + "/" + book_name + "_long.docx")
            check_move("./short_skim_docx/" + book_name + ".docx", 
                    book_dir + "/" + book_name + "_short.docx")
        else:
        # FOR EACH BOOK, CREATE A FOLDER CONTAINS LONG AND SHORT SKIMMING PARAGRAPHS
        # IF IT DOES NOT EXIST, THEN DOWNLOAD
            print("Downloading ...")
            long_skim_url = blinkist_homepage + "/en/nc/reader/" + book_name
            short_skim_url = blinkist_homepage + "/en/books/" + book_name
            long_skim_md_path = book_dir + "/" + book_name + "_long.md"
            long_skim_docx_path = book_dir + "/" + book_name + "_long.docx"
            short_skim_md_path = book_dir + "/" + book_name + "_short.md"
            short_skim_docx_path = book_dir + "/" + book_name + "_short.docx"
            
            random_sleep_interval = random.randint(1,10)
            print("Sleep for " + str(random_sleep_interval) + " s.")
            time.sleep(random_sleep_interval)
            
            f = open(long_skim_md_path, "a+")
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

            f = open(short_skim_md_path, "a+")
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

            # CONVERT MARKDOWN TO DOCX
            convert_long_command = "pandoc " + long_skim_md_path + " -o " + long_skim_docx_path
            convert_short_command = "pandoc " + short_skim_md_path + " -o " + short_skim_docx_path

            os.system(convert_long_command)
            os.system(convert_short_command)

driver.close()
