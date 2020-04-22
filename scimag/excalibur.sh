#!/bin/bash
# File              : excalibur.sh
# Author            : SuperUser <nvhhnvn@gmail.com>
# Date              :13 +07
# Last Modified Date: Wed 14-03-2018 13:33:50 +07
# Last Modified By  : SuperUser <nvhhnvn@gmail.com>

# always check internet

source /data/user/scripts/shell_function.template

use_proxy 0
check_internet
#random_proxy
#compare_speed 8

excalibur_link=http://www.math.ust.hk/excalibur/

excalibur_dir=/data/user/MATH/magazine/excalibur

list_file=/data/user/MATH/magazine/excalibur/excalibur_file.list

list_link=/data/user/MATH/magazine/excalibur/excalibur_link.list

if [[ ! -f $list_file ]]; then
   touch $list_file
fi

excalibur_list ()
{
   "$crl"_l $excalibur_link \
      | grep -oh "\w*.pdf\w*" \
      | sed '/>/d' \
      > $list_file
   sed "s|^|${excalibur_link}|g" $list_file > $list_link 
}

check_file ()
{
   offline_no_file=$(ls $excalibur_dir \
      | sed '/list/d' \
      | sed '/Corner/d' \
      | wc -l)
   server_no_file=$(wc -l $list_file | awk '{print $1}')
   if [[ $offline_no_file == $server_no_file ]]; then
      exit
   fi
   for i in $(eval echo "{$offline_no_file..$server_no_file}")
   do
      current_file=$(head -n$i $list_file | tail -n1)
      sudo notify-send "Mathematical Excalibur" "issue $current_file"
      if [[ -z "$(ls $excalibur_dir | grep $current_file)" ]]; then
         current_link=$(head -n$i $list_link | tail -n1)
         "$wgt"_tdl $excalibur_dir $current_link
      fi
   done
}
   
process ()
{
   excalibur_list
   check_file
}

process
