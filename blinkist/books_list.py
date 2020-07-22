#!/usr/bin/env python3

import random
import re
import requests
import time

book_urls_file = "./data/book_urls.txt"

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

# GET LIST OF BOOKS FROM BLINKIST
# store them in a file, retrieve later for crawling each book
# recently added books list contains 12 books
# actually you can count exact number of books from crawling (without credentials to the link https://www.blinkist.com/en/nc/recently_added_books.json?page=XX)
# cURL is not blocked to enter this link
# record all reader link directly for long skim at /en/nc/reader/XX and short skim at /en/books/XX

json_form = "https://www.blinkist.com/en/nc/recently_added_books.json?page="
short_skim_path_regex = r"(?<=data-book-path\=\\\")[a-z0-9-\/]+"
# for loop until no available data here
for i in range(231):
    random_sleep_interval = random.randint(1,10)
    print("Sleep for " + str(random_sleep_interval) + " s.")
    time.sleep(random_sleep_interval)
    r = requests.get(json_form + str(i), headers=headers)
    print(r.status_code)
    json_data = r.text
    books_list = re.findall(short_skim_path_regex, json_data)
    print(books_list)
    f = open(book_urls_file, "a+")
    default_links_list = f.read().splitlines()
    for book in books_list:
        write_string = book + "\n"
        if book not in default_links_list:
            f.write(write_string)
    f.close()
