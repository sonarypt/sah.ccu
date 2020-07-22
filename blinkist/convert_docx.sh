#!/bin/bash

short_skim_docx="./short_skim_docx"
long_skim_docx="./long_skim_docx"

# check if docx dir exists
[[ -d $long_skim_docx ]] || mkdir $long_skim_docx
[[ -d $short_skim_docx ]]  || mkdir $short_skim_docx


# loop through all md files, use pandoc to convert md to docx
for md in $(ls ./long_skim/)
do
    name=${md%.md}
    docx_file="./long_skim_docx/$name.docx"
    if [[ -f $docx_file ]]
    then
        continue
    else
        echo $md
        pandoc -o ./long_skim_docx/$name.docx ./long_skim/$md
    fi
done

for md in $(ls ./short_skim/)
do
    name=${md%.md}
    docx_file="./short_skim_docx/$name.docx"
    if [[ -f $docx_file ]]
    then
        continue
    else
        echo $md
        pandoc -o $docx_file ./short_skim/$md
    fi
done

