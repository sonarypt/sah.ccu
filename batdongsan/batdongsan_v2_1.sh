#!/bin/bash
###############################################################################
# author        : Hoang Nguyen 
# email         : zel.zsh@gmail.com
# script name   : batdongsan_v2_1.sh
# description   : v2.1 for the crawler website batdongsan.vn
###############################################################################

set -o errexit
set -o nounset
source /home/user/scripts/shell_function.sh

########## feature in this v2.1 #########################
### single array json file
### english language only
#########################################################

# this script should run for quite long so as not to get alert from website administrator
# this script is also updated for using jq as json processor
# and use sponge from moreutils to directly update the original file without writing to extras

# define custom curl string with header for safety purpose

ddos_check () {
  # function detect anti-DDOS message

  # check .tmp file before move to .html
  # crawl with notice about DDOS feature
  # if detect anti-ddos message, then exit
  # unblock DDOS with auto send request
  if grep -Foq "DDOS" $2; then
    print_style "## CHECKING ANTI-DDOS REQUEST" "danger"
    unblock_ddos_link=$(grep -oP "http://[a-z./?=]+" $2)
    curl_l $unblock_ddos_link > /dev/null
    print_style "## UNBLOCKED ANTI-DDOS REQUEST" "success"
    rm ${2%.*}.tmp
    curl_l $1 > ${2%.*}.html
  else
    mv ${2%.*}.tmp ${2%.*}.html
  fi
  sleep "$(( ( $RANDOM % 3 ) + 2 ))s"
}

# limit number of loop to crawl
num_loop=10

# crawl dir, may specify later. faster coding
bds_dir=/data/user/crawl/batdongsanvn_v2_1
[ ! -d $bds_dir ] && mkdir $bds_dir

# initialize json file for further edit
fjson=$bds_dir/batdongsanvn_v2_1.json
[ -f $fjson ] || jq -n '[]' > $fjson

# list of category link and list
canban_list=$bds_dir/canban.list
chothue_list=$bds_dir/chothue.list

# for faster coding only. get back to automate crawl list later
if [ ! -f $canban_list ]; then
  echo -e "http://www.batdongsan.vn/giao-dich/ban-can-ho-chung-cu.html|can_ho_chung_cu|căn hộ chung cư" >> $canban_list
  echo -e "http://www.batdongsan.vn/giao-dich/ban-nha-rieng.html|nha_rieng|nhà riêng" >> $canban_list
  echo -e "http://www.batdongsan.vn/giao-dich/ban-nha-mat-pho.html|nha_mat_pho|nhà mặt phố" >> $canban_list
  echo -e "http://www.batdongsan.vn/giao-dich/ban-biet-thu-lien-ke.html|biet_thu_lien_ke|biệt thự liền kề" >> $canban_list
  echo -e "http://www.batdongsan.vn/giao-dich/ban-dat-nen.html|dat_nen|đất nền" >> $canban_list
fi

# read all leading link from list
cat $canban_list | while read line; do

  # folder name is at second column
  awk -F "|" '{print $2}' <<< $line | while read folder_name; do
    [ ! -d $bds_dir/$folder_name ] && mkdir $bds_dir/$folder_name && echo "> $folder_name"

    # empty array add to main json file
    category="$(awk -F "|" '{print $3}' <<< $line)"
    # jq --arg category "$category" ".\"$category\" += {}" $fjson | sponge $fjson

    # specify 10 time loop to crawl for data from target website
    for (( i=1; i<300; i++ )); do
      if [ ! -d $bds_dir/$folder_name/$i ]; then
        mkdir $bds_dir/$folder_name/$i
        print_style ">> maked directory $bds_dir/$folder_name/$i" "success"
      else
        print_style ">> founded directory $bds_dir/$folder_name/$i" "info"
      fi

      # find the current link and the next link from the list
      # detect the next link, trouble only with the first. ez from the second
      link_only=$(awk -F "|" '{print $1}' <<< $line)
      if (( $i == 1 )); then
        if [ -f $bds_dir/$folder_name/1.html ]; then
          echo "- founded $bds_dir/$folder_name/1.html" 
        else
          echo "+ $bds_dir/$folder_name/1.html"
          curl_l $link_only > $bds_dir/$folder_name/1.tmp
          ddos_check "$(awk -F "|" '{print $1}' <<< $link_only)" $bds_dir/$folder_name/1.tmp
        fi
        next_link=$(sed 's/.html/\/pageindex-2.html/g' <<< $link_only)
      else
        cur_link=$(sed "s/.html/\/pageindex-$i.html/g" <<< $link_only)
        if [ -f $bds_dir/$folder_name/$i.html ]; then
          echo "- founded $bds_dir/$folder_name/$i.html"
        else
          echo "+ $bds_dir/$folder_name/$i.html"
          curl_l $cur_link > $bds_dir/$folder_name/$i.tmp
          ddos_check $cur_link $bds_dir/$folder_name/$i.tmp
        fi
        next_link=$(sed "s/$i/$(($i + 1))/g" <<< $cur_link)
      fi

      next_link_no_http=${next_link:7}
      href_next_link=${next_link_no_http#*/}

      link_only_no_http=${link_only:7}
      domain=$(echo ${link_only_no_http%%/*})

      # then find data from each of index pages
      grep "class='lazy'" $bds_dir/$folder_name/$i.html | grep -oP "(?<=href=')[^']*" | while read href; do
        href_name=$(sed 's/\///g' <<< $href)
        href_tmp=${href_name%.*}.tmp
        index_href=$(grep -oP "p\d+" <<< $href)
        task_href=$(echo ${href_name%%.*} | sed "s/$index_href//g;s/-$//g")
        if [ -f $bds_dir/$folder_name/$i/$href_name ]; then
          print_style "- founded $folder_name/$i/$href_name" "success"
          continue
        else
          echo "+ $folder_name/$i/$href_name"
          curl_l "$domain$href" > $bds_dir/$folder_name/$i/$href_tmp
          ddos_check $domain$href $bds_dir/$folder_name/$i/$href_tmp
          # sleep some random second before doing anything
          sleep "$(( ( $RANDOM % 3 ) + 2 ))s"
        fi

        # get all attribute variable ready to put into json file
        href_file=$bds_dir/$folder_name/$i/$href_name
        id=$(tr -d "p" <<< $index_href)
        title="$(grep -oP '(?<=<h1>).*?(?=</h1>)' $bds_dir/$folder_name/$i/$href_name)"
        contact="$(grep -m1 -A1 "<div class=\"name\"" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | xargs | dos2unix)"
        email=$(grep "<div class=\"email\">" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)
        tel=$(grep -B3 "Gọi điện" $href_file | grep -oP "(?<=tel://)[0-9]+")
        city="$(grep -m1 -A1 "<label>Địa chỉ" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)"
        street="$(grep -m1 -A1 "<label>Đường/phố" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)"
        price=$(grep -m1 -A1 "<label>Giá cả" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)
        area=$(grep -m1 -A1 "<label>Diện tích" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)
        mfg=$(grep -m1 -A1 "<label>Ngày đăng tin" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)
        exp=$(grep -m1 -A1 "<label>Ngày hết hạn" $href_file | sed -e 's/<[^>]*>//g;s/^[ \t]*//' | tail -n1 | dos2unix)
        # description="$(grep "PD_Gioithieu col-md-7 col-md-pull-5" $href_file | sed -e 's/<br \/>/./g;s/<[^>]*>//g;s/^[ \t]*//')"

        img_link_array=$(grep -oP "http://cdn.batdongsan.vn/FileManager/Upload/[_a-z.A-Z0-9-/]+" $href_file | sort | uniq | jq --raw-input --slurp 'split("\n")')

        jq --arg category "$category" \
          --arg id "$id" \
          --arg title "$title" \
          --arg contact "$contact" \
          --arg email "$email" \
          --arg tel "$tel" \
          --arg city "$city" \
          --arg street "$street" \
          --arg price "$price" \
          --arg area "$area" \
          --arg mfg "$mfg" \
          --arg exp "$exp" \
          --arg img_link_array "$img_link_array" \
          ". += {\"title\":\"$title\", \"contact\":\"$contact\", \"email\":\"$email\", \"phone\":\"$tel\", \"city\":\"$city\", \"street\":\"$street\", \"price\":\"$price\", \"area\":\"$area\", \"start\":\"$mfg\", \"end\":\"$exp\", \"img_link\":$img_link_array}" $fjson \
          1>/dev/null 2>/dev/null

        if (( $? == 0 )); then
          jq --arg category "$category" \
            --arg id "$id" \
            --arg title "$title" \
            --arg contact "$contact" \
            --arg email "$email" \
            --arg tel "$tel" \
            --arg city "$city" \
            --arg street "$street" \
            --arg price "$price" \
            --arg area "$area" \
            --arg mfg "$mfg" \
            --arg exp "$exp" \
            --arg img_link_array "$img_link_array" \
            ". += {\"id\":\"$id\", \"category\":\"$category\", \"title\":\"$title\", \"contact\":\"$contact\", \"email\":\"$email\", \"phone\":\"$tel\", \"city\":\"$city\", \"street\":\"$street\", \"price\":\"$price\", \"area\":\"$area\", \"start\":\"$mfg\", \"end\":\"$exp\", \"img_link\":$img_link_array}" $fjson | sponge $fjson
        else
          continue
        fi

      done
      grep -Foq "$href_next_link" $bds_dir/$folder_name/$i.html || break
      # cannot directly check the existence of index site directyly by curl, duplicate
      # so get the existence of index site from source code
    done
  done
done


