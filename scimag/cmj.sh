#!/bin/bash

cmj_homepage="https://www.maa.org/press/periodicals/"\
  "college-mathematics-journal/the-college-mathematics-journal"
cmj_dir=/data/user/MATH/magazine/CMJ
cmj_list=/data/user/MATH/magazine/CMJ/cmj.list
cmj_tmp=/tmp/cmj

"$crl"_l $cmj_homepage > $cmj_tmp

iss_sub_link=$(grep -A 2 "Table of Contents/Article" < /tmp/cmj \
  | sed '/archive/d' | grep -oP "[\w]*href[=\"/\w-]*" \
  | tail -n1 | sed 's/"/ /g' | awk '{print $2}')
iss_link=https://www.maa.org/$iss_sub_link

iss_month=$(cut -d- -f7 <<< $iss_sub_link)
iss_year=$(cut -d- -f8 <<< $iss_sub_link)
 
iss_dir=$cmj_dir/$iss_month-$iss_year

if [[ ! -d $iss_dir ]]; then
  mkdir -p $iss_dir
fi

if [[ ! -f $cmj_list ]]; then
  touch $cmj_list
fi

if [[ -z $(grep $iss_sub_link $cmj_list) ]]; then
  echo "$iss_sub_link\n" >> $cmj_list
else
  exit
fi

iss_curl=/tmp/cmj_iss
"$crl"_l $iss_link > $iss_curl
doi_list=$iss_dir/doi-$iss_month-$iss_year.list

grep "DOI:" < $iss_curl | sed 's/[<>]/ /g' | awk '{print $6}' > $doi_list

num_doi=$(wc -l $doi_list | awk '{print $1}')

for i in $(eval echo "{1.."$num_doi"}")
do
  doi_id=$(head -n$i $doi_list | tail -n1)
  libgen_string=$(sed "s/\//%2F/g" <<< $doi_id)
  scimag_curl=/tmp/scimag_curl
  "$crl"_l "http://gen.lib.rus.ec/scimag/index.php?s=$libgen_string&journalid=&v=&i=&p=&redirect=1" > $scimag_curl
  libgen_link=$(grep "Links:" $scimag_curl | grep -oP "http:[/?=.%&\w]*")
  libgen_curl=/tmp/libgen_curl
  "$crl"_l "$libgen_link" > $libgen_curl
  dos2unix $libgen_curl $libgen_curl
  title=$(grep "title\s=" $libgen_curl | sed "s/[{},=]//g" \
    | sed "s/ /_/g" | sed "s/^M//g" | awk '{print $2}')
  file_link=$(grep "GET" $libgen_curl | grep -oP "http:[/?=.%&\w]*")
  "$wgt"_d_l $iss_dir $file_link
  file=$(ls $iss_dir | grep $libgen_string)
  mv $iss_dir/$file $iss_dir/$title.pdf
  pdftk $iss_dir/$title.pdf cat 2-end output $iss_dir/$title.new.pdf
  mv $iss_dir/$title.new.pdf $iss_dir/$title.pdf
done


