#!/bin/bash

wallpaper_dir=/home/user/interfacelift
brightness_info=$wallpaper_dir/brightness.info

[ ! -f $brightness_info ] && touch $brightness_info

num=$(( $(cat $wallpaper_dir/num.info) + 1 ))

for i in $(ls $wallpaper_dir/*.jpg); do
   [ -n "$(grep $i $brightness_info)" ] && continue
   Y=$(convert $i -format %c -colorspace LAB -colors 1 histogram:info:- | sort -n -r | grep -Po "\d+\,\d+\,\d+" | head -n1 | awk -F "," '{y=0.2126*$1+0.7152*$2+0.0722*$3} END {printf("%d\n", y)}')
   printf "%-100s%4d\n" $i $Y >> $brightness_info
done
