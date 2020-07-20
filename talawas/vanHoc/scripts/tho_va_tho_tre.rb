#!/usr/bin/env ruby

require 'nokogiri'
require 'open-uri'

def convertImages(html_content, file_name)
   # re-parse to Nokogiri HTML object
   parsed_html_content = Nokogiri::HTML(html_content)
   
   # work with table - image tags
   tables_tag = parsed_html_content.xpath(".//table")
   if tables_tag.to_a.length() != 0
      tables_tag.each do |table_tag|
         img_url = table_tag.xpath(".//img").attribute('src').to_s
         img_absolute_url = $master_link + img_url
         img_name = img_url.split("/").map(&:strip)[1]
         img_caption = table_tag.xpath(".//tr[2]/td")[0].inner_html
         toLatexSyntax(img_caption)
         img_file = $master_img_dir + img_name
         File.open(img_file, 'wb') do |fo|
            fo.write \
               URI.open(img_absolute_url,
                        "Host" => "www.talawas.org",
                        "User-Agent" => "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
                        "Accept" => "*/*",
                        "Accept-Language" => "en-US,en;q=0.5",
                        "Connection" => "keep-alive",
                        "Upgrade-Insecure-Requests" => "1").read
         end
         img_latex_code = 
            "\\begin{figure}\n" +
            "\t\\centering\n" +
            "\t\\includegraphics[width=\\textwidth]{../img/" + img_name + "}\n" +
            "\t\\caption{" + img_caption + "}\n" +
            "\\end{figure}\n"

         html_content.gsub!(table_tag.to_s, img_latex_code)
      end
   end

   # work with table - image tags
   images_tag = parsed_html_content.xpath(".//img")
   if images_tag.to_a.length() != 0
      images_tag.each do |image_tag|
         img_url = image_tag.attribute('src').to_s
         img_absolute_url = $master_link + img_url
         img_name = img_url.split("/").map(&:strip)[1]
         img_caption = ""
         toLatexSyntax(img_caption)
         img_file = $master_img_dir + img_name
         File.open(img_file, 'wb') do |fo|
            fo.write \
               URI.open(img_absolute_url,
                        "Host" => "www.talawas.org",
                        "User-Agent" => "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
                        "Accept" => "*/*",
                        "Accept-Language" => "en-US,en;q=0.5",
                        "Connection" => "keep-alive",
                        "Upgrade-Insecure-Requests" => "1").read
         end
         img_latex_code = 
            "\\begin{figure}\n" +
            "\t\\centering\n" +
            "\t\\includegraphics[width=\\textwidth]{../img/" + img_name + "}\n" +
            "\t\\caption{" + img_caption + "}\n" +
            "\\end{figure}\n"

         html_content.gsub!(image_tag.to_s, img_latex_code)
      end
   end
end

def convertFootnotes(html_content, file_name)
   # re-parse to Nokogiri HTML object
   parsed_html_content = Nokogiri::HTML(html_content)
   
   # work with footnote tags
   # convert to array so as to pop later
   footnotes_tag = parsed_html_content.xpath(".//a[contains(@href, '#')]").to_a
   number_of_tags = footnotes_tag.length()
   if number_of_tags != 0
      footnotes_tag.pop(number_of_tags/2)
      footnotes_tag.each do |footnote_tag|
         # find link inside posts too
         a_link = footnote_tag.attribute('href').to_s
         
         fn_source = parsed_html_content.xpath(".//a[@name='" + a_link.to_s[1..-1] + "']")[0]

         fn_text = fn_source.next.to_s.strip
         new_tag = "\\footnote{\n" + fn_text + "}"
         
         html_content.gsub!(footnote_tag.to_s, new_tag)
      end
   end
   # TODO: remove all nodes after  node <hr> if exists

end

# always run convert links after convertFootnotes
def convertLinks(html_content, file_name)
   # re-parse to Nokogiri HTML object
   parsed_html_content = Nokogiri::HTML(html_content)

   # work with external tags
   external_links_tag = parsed_html_content.xpath(".//a[@href]")
   external_links_tag.each do |external_link_tag|
      a_link = external_link_tag.attribute('href')
      unless a_link.include? "http"
         a_link = $master_link + a_link
      end
      a_text = external_link_tag.text
      # simply just add that external link
      new_tag = a_text + "\\footnote{\\url{" + a_link + "}}"
      html_content.gsub!(external_link_tag.to_s, new_tag)
   end
end

def writeHeaders(parsed_html_content, file_name)
   File.write(file_name, 
              ["\\documentclass[../main.tex]{subfiles}",
               "\\begin{document}\n\n"].join("\n\n"), mode: "a")
   
   title = parsed_html_content.xpath("//div[@class='artikelBeitrTitel']")[0].text
   File.write(file_name, "\\chapter{#{title}}\n\n", mode: "a")
   
   # not every posts have "subtitle" part
   begin
      subtitle = parsed_html_content.xpath("//div[@class='artikelBeitrSubTitel']")[0].text
      File.write(file_name, 
                 ["\\begin{subtitle}", 
                 subtitle, 
                 "\\end{subtitle}\n\n"].join("\n\n"), mode: "a")
   rescue NoMethodError
      subtitle = ""
   end

   date = parsed_html_content.xpath("//div[@class='artikelBeitrDatum']")[0].text
   author = parsed_html_content.xpath("//div[@class='artikelBeitrAutor']")[0].text
   
   # not every posts have "source" part
   begin
      source = parsed_html_content.xpath("//div[@class='artikelBeitrRelated']")[0].content
   rescue NoMethodError
      source = ""
   end
   
   File.write(file_name, 
              ["\\begin{metadata}", 
               "\\begin{flushright}" + date + "\\end{flushright}", 
               author, 
               source, 
               "\\end{metadata}\n\n"].join("\n\n"), mode: "a")
end

def toLatexSyntax(content)
   # find text decoration tag like <em>, <strong>
   # margin left 30px convert to blockquote, end that /div with ending }
   # find <ul>, <ol> lists
   convert_hash = {
      "$" => "\$",
      "<br>" => "\n",
      "<em>" => "\\textit{",
      "</em>" => "}",
      "<strong>" => "\\textbf{",
      "</strong>" => "}",
      "</div>" => "\\end{blockquote}\n",
      "<ul>" => "\\begin{itemize}\n",
      "</ul>" => "\\end{itemize}\n",
      "<ol>" => "\\begin{enumerate}\n",
      "</ol>" => "\\end{enumerate}\n",
      "<li>" => "\item{",
      "</li>" => "}\n",
      '<p style="text-align: center">' => "\\begin{center}\n",
      "</p>" => "\\end{center}\n",
      "<sup>" => "\\small{",
      "</sup>" => "}"
   }
   convert_regex = Regexp.new(convert_hash.keys.map { |x| Regexp.escape(x) }.join('|'))
   content.gsub!(convert_regex, convert_hash)
   content.gsub!(/<div.*>/, "\\begin{blockquote}\n")
end

# list of posts from each left column
def getPostsFromTags(document)
   posts_tag = document.xpath("//div[@class='newestWrap']/a")
   posts_tag.each do |post_link|
      sub_link = post_link.attribute('href')
      category_index = sub_link.to_s.match(/(?<=rb=)\d+/)[0]
      post_index = sub_link.to_s.match(/(?<=res=)\d+/)[0]
      # file name the same as query number in res=14281&rb=0101: 0101_14281.tex
      file_name = $master_tex_dir + category_index + "_" + post_index + ".tex"
      
      if File.file?(file_name)
         puts file_name + " existed"
         next
      else
         rnd = rand(20..50)
         print "sleep for #{rnd} seconds. "
         STDOUT.flush
         sleep(rnd)
      end

      post_link_full = $master_link + sub_link
      # set headers for URI.open
      post = Nokogiri::HTML.parse(
         URI.open(post_link_full,
                 "Host" => "www.talawas.org",
                 "User-Agent" => "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
                 "Accept" => "*/*",
                 "Accept-Language" => "en-US,en;q=0.5",
                 "Connection" => "keep-alive",
                 "Upgrade-Insecure-Requests" => "1")
      )
      
      # write headers to Latex file
      writeHeaders(post, file_name)

      # use gsub to replace breakline, this is different from python
      content = post.xpath("//div[@class='artikelBeitrTextBody']")[0].inner_html
      
      toLatexSyntax(content)

      convertImages(content, file_name)
      convertFootnotes(content, file_name)
      convertLinks(content, file_name)

      # this must be after convertLinks
      content.gsub!(/^<hr>(\n.*)*/, "\n")

      File.write(file_name, "\\begin{multicols}{2}\n\n", mode: "a")
      File.write(file_name, content, mode: "a")
      File.write(file_name, ["\n\\end{multicols}", "\\end{document}"].join("\n"), mode: "a")

      puts "Done with " + file_name
   end
end

$master_link = "http://www.talawas.org/talaDB/"
$master_tex_dir = "../rawTex/"
$master_img_dir = "../img/"

# number of pages left, so as to make number of loops
$i = 1
$von = 0
$bis = 20

while $i != 0
   link = $master_link + "talaDBFront.php?rb=0101&von=" + $von.to_s + "&bis=" + $bis.to_s + "&pg=1"
   # set headers for URI.open
   document = Nokogiri::HTML.parse(
      URI.open(link,
              "Host" => "www.talawas.org",
              "User-Agent" => "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
              "Accept" => "*/*",
              "Accept-Language" => "en-US,en;q=0.5",
              "Connection" => "keep-alive",
              "Upgrade-Insecure-Requests" => "1")
   )
   
   getPostsFromTags(document)
   
   all_number_tag = document.xpath("//div[@class='newestPager']")[0].content.strip
   ant_split = all_number_tag.split(" ").map(&:strip)
   current_number = ant_split[3].to_i
   highest_number = ant_split[5].to_i

   if highest_number - current_number < 20
      $i = 0
   else
      $von += 20
      puts "von: " + $von.to_s
      $bis += 20
      puts "bis: " + $bis.to_s
   end
   
end

# TODO: allow seperate headers hash to edit later in URI.open
# TODO: merge tables_tag and images_tag D.R.Y
