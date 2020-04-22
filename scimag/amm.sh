#!/bin/bash

source /data/user/scripts/shell_function.template

use_proxy 1
check_internet
random_proxy
compare_speed 8

amm_homepage=https://www.maa.org/press/periodicals/american-mathematical-monthly
amm_dir=/data/user/MATH/magazine/AMM
amm_list=/data/user/MATH/magazine/AMM/amm.list
amm_tmp=/tmp/amm

"$crl"_l $amm_homepage > $amm_tmp

iss_sub_link=$(grep -A 2 "Table of Contents/Article" /tmp/amm \
	| tail -n1 \
	| grep -oP "[\w]*href[=\"/\w-]*" \
	| tail -n1 \
	| sed 's/"/ /g' \
	| awk '{print $2}')
iss_link=https://www.maa.org$iss_sub_link

iss_month=$(cut -d- -f6 <<< $iss_sub_link)
iss_year=$(cut -d- -f7 <<< $iss_sub_link)
 
iss_dir=$amm_dir/$iss_month-$iss_year

if [[ ! -d $iss_dir ]]; then
    mkdir -p $iss_dir
fi

if [[ ! -f $amm_list ]]; then
    touch $amm_list
fi

if [[ -z $(grep $iss_sub_link $amm_list) ]]; then
    echo "$iss_sub_link\n" >> $amm_list
else
    exit
fi

iss_curl=/tmp/amm_iss
"$crl"_l $iss_link > $iss_curl
doi_list=$iss_dir/doi-$iss_month-$iss_year.list

grep "DOI:" < $iss_curl | sed 's/[<>]/ /g' | awk '{print $5}' > $doi_list


num_doi=$(wc -l $doi_list | awk '{print $1}')

for i in $(eval echo "{1.."$num_doi"}")
do
    doi_id=$(head -n$i $doi_list | tail -n1)
    libgen_string=$(sed "s/\//%2F/g" <<< $doi_id)
    scimag_curl=/tmp/scimag_curl
    "$crl"_l "http://gen.lib.rus.ec/scimag/index.php?s=$libgen_string&journalid=&v=&i=&p=&redirect=1" > $scimag_curl
    libgen_link=$(grep "Links:" $scimag_curl \
	    | grep -oP "http:[/?=.%&\w]*")
    libgen_curl=/tmp/libgen_curl
    "$crl"_l "$libgen_link" > $libgen_curl
    file_link=$(grep "GET" $libgen_curl \
	    | grep -oP "http:[/?=.%&\w]*")
    "$wgt"_tdl $iss_dir $file_link
done

