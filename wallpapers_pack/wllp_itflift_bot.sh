#!/bin/bash

# this script use to downloads all available wallpapers suitable for 16:9 screen and have at least FullHD resolution

# curl with Chrome Windows 10 headers - added checking empty string of url

c_ua () {
   # prx="$(shuf $vn_proxy_list | head -n1 | sed 's/ /:/g')"
   if [[ ! -z "$1" ]]; then
      # curl \
      #    --proxy $prx \
      #    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36" \
      #    --header "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
      #    --header "referer: https://www.google.com" \
      #    --header "connection: keep-alive" \
      #    --header "accept-language: en-US,en;q=0.9" \
      #    --header "upgrade-insecure-requests: 1"\
      #    $1
      curl \
         -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36" \
         --header "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
         --header "referer: https://www.google.com" \
         --header "connection: keep-alive" \
         --header "accept-language: en-US,en;q=0.9" \
         --header "upgrade-insecure-requests: 1"\
         $1
   fi
}

# wget with Chrome Windows 10 headers - added checking empty string of url

wg_ua () {
   # prx="$(shuf $vn_proxy_list | head -n1 | sed 's/ /:/g')"
   if [[ ! -z "$2" ]]; then
      # wget \
      #    -e use_proxy=yes \
      #    -e http_proxy=$prx \
      #    --no-clobber \
      #    --keep-session-cookies \
      #    --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36" \
      #    --header "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
      #    --header "referer: https://www.google.com" \
      #    --header "connection: keep-alive" \
      #    --header "accept-language: en-US,en;q=0.9" \
      #    --header "upgrade-insecure-requests: 1"\
      #    --directory-prefix=$1 \
      #    $2
      wget \
         --no-clobber \
         --keep-session-cookies \
         --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36" \
         --header "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
         --header "referer: https://www.google.com" \
         --header "connection: keep-alive" \
         --header "accept-language: en-US,en;q=0.9" \
         --header "upgrade-insecure-requests: 1"\
         --directory-prefix=$1 \
         $2
   fi
}

num=118
# choose only pictures have 4K resolution only
main_link="https://interfacelift.com/wallpaper/downloads/date/wide_16:9/3840x2160"
img_dir=/data/user/interfacelift
link_dir=/data/user/interfacelift_link
link_list=$link_dir/link_list
# declare array of wanted resolution
# res[0]=3840x2160; res[1]=3200x1800
# res[2]=2880x1620; res[3]=2560x1440
# res[4]=1920x1080

# if [ ! -d $img_dir ]; then
#    mkdir -p $img_dir
# fi
#
# if [ ! -d $link_dir ]; then
#    mkdir -p $link_dir
# fi
#
# if [ -f $link_list ]; then
#    rm $link_list
# fi

# detect number of image on a webpage when increment, get source file and add to link list file
# for i in $(eval echo "{1..${num}}")
# do
#    if [ -f $link_dir/link$i ]; then
#       grep -A3 -n "\<div id=\"list" $link_dir/link$i | sed -n 's/.*src="\([^"]*\).*/\1/p' | sed 's/previews/7yz4ma1/g' | sed 's/672x420/3840x2160/g' >> $link_list
#       continue
#    else
#       link="$main_link/index$i.html"
#       c_ua $link > $link_dir/link$i
#       grep -A3 -n "\<div id=\"list" $link_dir/link$i | sed -n 's/.*src="\([^"]*\).*/\1/p' | sed 's/previews/7yz4ma1/g' | sed 's/672x420/3840x2160/g' >> $link_list
#    fi
#    sleep "$(( ( $RANDOM % 3 ) + 3 ))s"
# done

# there is other way: get the next link from the "next page" button


# replace source link resolution step by step with highest available res
# notice that all preview image have only 672x420 resolution
# if only get full HD resolution then the things are easy
# the problem arise when we want the highest available resolution
# interfacelift have strange string 7yz4ma1, which is the only rare string
# that allow access to the image database

# wget to dir

# echo 667 > $link_dir/current_num
cur_num=$(cat $link_dir/current_num)
num_link=$(wc -l < $link_list)
for i in $(eval echo "{$cur_num..$num_link}")
do
   if (( $i < $num_link )); then
      echo "$(( $i+1 ))" > $link_dir/current_num 
   else
      exit
   fi
   img_link=$(head -n$i $link_list | tail -n1)
   wg_ua $img_dir $img_link
   sleep "$(( ( $RANDOM % 5 ) + 5 ))s"
done
