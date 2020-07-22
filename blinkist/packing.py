#!/usr/bin/env python3

import os
import glob
import shutil

def check_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d)

def check_move(f1, f2):
    if os.path.isfile(f1):
        shutil.move(f1, f2)

check_dir("./uncategorized")

books_name = [i.split("/")[-1].split(".")[0] for i in glob.glob("*/*.docx")]
print(books_name)

for book_name in books_name:
    print(book_name + ": ", end = "")
    book_dir = "./uncategorized/" + book_name
    check_dir(book_dir)
    
    ls_md_src = "./long_skim/" + book_name + ".md"
    ss_md_src = "./short_skim/" + book_name + ".md"
    ls_docx_src = "./long_skim_docx/" + book_name + ".docx"
    ss_docx_src = "./short_skim_docx/" + book_name + ".docx"

    ls_md_des = book_dir + "/" + book_name + "_long.md"
    ss_md_des = book_dir + "/" + book_name + "_short.md"
    ls_docx_des = book_dir + "/" + book_name + "_long.docx"
    ss_docx_des = book_dir + "/" + book_name + "_short.docx"

    check_move(ls_md_src, ls_md_des)
    check_move(ss_md_src, ss_md_des)
    check_move(ls_docx_src, ls_docx_des)
    check_move(ss_docx_src, ss_docx_des)

    print("Packed")
