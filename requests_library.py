import requests
from requests_html import HTMLSession
from requests_html import HTML
from fake_useragent import UserAgent

from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import unquote
import os
import itertools
import pandas as pd
import openpyxl

url = "https://www.zillow.com/homes/recently_sold/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-120.142035125%2C%22east%22%3A-73.560003875%2C%22south%22%3A20.620884319144793%2C%22north%22%3A52.6886545933123%7D%2C%22mapZoom%22%3A4%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/53'}
# response = requests.get(url, headers=headers)
# print(response.content)
ua = UserAgent()
# print(ua.chrome)
header = {'User-Agent':str(ua.chrome)}
# print(header)


# ! TODO: request module with proxy (Search)
#! TODO: https://oxylabs.io/products/residential-proxy-pool [masud.jgtdsl@gmail.com, PW: MStaqLZ7A9JJ@!@]
#!FIXME: BEAUTIFULLDOUP DOCUMENTATION: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# ('https://images.prothomalo.com/prothomalo-bangla%2F2024-10-03%2Fx7xp5zj4%2FPhoto-by-Malavika-Mohanan-on-December-23-2023.-1.jpg', '')
#! TODO:=====CPVP===============
rc_no:int = 0
def fetchAndSaveToFile(url, path): 
    r = requests.get(url) 
    with open(path, "w") as f: 
        f.write(r.text) 

id=""
url = "https://www.cpvppraktoni.com/alumni/alumni_list" 
path = f"CPVP/alumni_list_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"

# fetchAndSaveToFile(url, path) #TODO========

def open_file(path,open_mode):
    with open(path,open_mode) as f:
        return f.read()

cpvp = open_file("CPVP/0001.html","r")
soup = BeautifulSoup(cpvp,'html.parser')
# print(soup.prettify())
lst = soup.find_all('li',class_="paginate_button page-item")

print(lst)
link = [(item.find("a").text,item.find("a").attrs["href"]) for item in lst]
print(link)


def write_as_prettified_text(path, text):
    with open(path, "w") as f: 
        f.write(text.replace("\n\n","\n")) 

# write_as_prettified_text(f"CPVP/TEMP/Prettified{datetime.now().strftime('%Y%m%d%H%M%S')}.html",
#                          soup.prettify())    

# def link_sort(text):
#     return int(re.search(r"(\d*$)", text + "0").group())

link_sort = lambda text: int(re.search(r"(\d*$)", text + "0").group())

def page_navigation_link(first_url_list,soup):
    page_link = soup.find_all('li','a',class_="paginate_button page-item") 
    list_of_page_link = set((tuple(first_url_list)))
    url_set = {item.find("a").attrs["href"] for item in page_link}
    list_of_page_link.update(url_set)
    list_of_set = list(list_of_page_link)
    list_of_set.sort(key=link_sort)
    # print("🆗","🆗","🆗",list_of_set)
    return list_of_set

print(page_navigation_link(url,soup))


url = "https://www.cpvppraktoni.com/alumni/alumni_list" 
rc_no_1 = 0
def collect_pages(first_url_list):
    rc_no_1 = 0
    write_read_path = f"CPVP/{rc_no_1:04}.html"
    fetchAndSaveToFile(url=first_url_list[0],path=write_read_path)
    cpvp = open_file(write_read_path,"r")
    soup = BeautifulSoup(cpvp,'html.parser')
    navigation_link_set = page_navigation_link(first_url_list,soup)

    loop_status = True
    while loop_status:
        rc_no_1 += 1
        write_read_path = f"CPVP/{rc_no_1:04}.html"
        fetchAndSaveToFile(url=navigation_link_set[rc_no_1],path=write_read_path)
        cpvp = open_file(write_read_path,"r")
        soup = BeautifulSoup(cpvp,'html.parser')
        navigation_link_set = page_navigation_link(navigation_link_set,soup)
        if rc_no_1 >= len(navigation_link_set)-1:
            loop_status = False

    return navigation_link_set

# print(collect_pages([url]))

# def page_navigation_link_1():
#     page_link = soup.find_all('a',class_="page-link") 
#     list_of_page_link = {item.get("href") for item in page_link}
#     list_of_page_link_text = {item.get_text() for item in page_link}

    # print(list_of_page_link_text)
    # print(list_of_page_link)

# def page_navigation_link_2():
#     lst = soup.select("li>a.page-link")
#     # lst = soup.li.a.get("page-link")
#     list_of_page_link = {item.get("href") for item in lst}
#     print(lst)
#     print("🆗",list_of_page_link)

# page_navigation_link(url)

#! simple version for working with CWD
#! print(len([name for name in os.listdir('.') if os.path.isfile(name)]))

#! path joining version for other paths

def cfDecodeEmail(encodedString):
    try:
        r = int(encodedString[:2],16)
        email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    except:
        email = "N/A"
    return email

def details(directory):
    number_of_file_in_a_dir = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    image_list = []
    name_list = []
    occupation_list = []
    batch_list = []
    email_list = []

    for i in range(number_of_file_in_a_dir):
        read_path = f"{directory}{i:04}.html"
        current_file = open_file(read_path,"r")
        soup = BeautifulSoup(current_file,'html.parser')
        info_list = soup.select("table.table.table-striped.table-bordered>tbody>tr>td>div>div>div") #>img.img-fluid.img-thumbnail
        image_list.append([info_list[x].find("img").attrs["src"] for x in range(len(info_list)) if x%2==0])
        name_list.append([info_list[x].find("h5", class_="uppercase").find("b").text.strip() for x in range(len(info_list)) if x%2==1])
        occupation_list.append([info_list[x].find("h6").text.strip() for x in range(len(info_list)) if x%2==1])
        batch_list.append([info_list[x].find_all(string=re.compile("Batch"))[0].strip() for x in range(len(info_list)) if x%2==1])
        email_code = [cfDecodeEmail(info_list[x].find("a").attrs["href"][len(r"/cdn-cgi/l/email-protection#"):]) for x in range(len(info_list)) if x%2==1]
        email_list.append(email_code)
    marged_image_list = list(itertools.chain(*image_list))
    marged_name_list = list(itertools.chain(*name_list))
    marged_occupation_list = list(itertools.chain(*occupation_list))
    marged_batch_list = list(itertools.chain(*batch_list))
    marged_email_list = list(itertools.chain(*email_list))
    marged_list = {"PHOTO":marged_image_list,
                    "Name":marged_name_list,
                    "Occupation":marged_occupation_list,
                    "SSC Batch":marged_batch_list,
                    "Email":marged_email_list
                    }
    return {"image_list":image_list,
            "name_list":name_list,
            "occupation_list":occupation_list,
            "batch_list":batch_list,
            "email_list":email_list,
            "marged_list":marged_list}

print(details(directory='CPVP/'))

def image_extract(directory,image_list,image_name_list):
    for i in range(len(image_list)):
        for y in range(len(image_list[i])):
            with open(f"{directory}/{i}{y}_{image_name_list[i][y]}.jpg","wb") as f:
                r = requests.get(image_list[i][y])
                f.write(r.content)


detail_info = details(directory='CPVP/')
# image_extract("CPVP/IMAGES",detail_info["image_list"],detail_info["name_list"])
image_name_list_ = []

for i in range(len(detail_info["image_list"])):
    image_name_list_.extend(
        f"{i}{j}_{detail_info['name_list'][i][j]}"
        for j in range(len(detail_info["image_list"][i]))
    )

# print(image_name_list_)
def save_to_excel():
    data = pd.DataFrame(detail_info["marged_list"]|{"Image":image_name_list_}, index=list(range(1,len(detail_info["marged_list"]["PHOTO"])+1))) #, index=list(range(1,len(detail_info["marged_list"]["PHOTO"])+1))
    data.to_excel(
        "CPVP/TEMP/cpvp_prahtoni_all.xlsx",
        sheet_name="cpvp_prahtoni_all",
        index=True,
        index_label="SL",
        freeze_panes=(1, 1),
    )

save_to_excel()
# print(cfDecodeEmail('98f5f9ebedfcb6f2ffecfcebf4d8fff5f9f1f4b6fbf7f5')) # usage

# image_name_list_ = [f"{i}{j}{detail_info['image_list'][i][j]}" for i,j in range(len(detail_info["image_list"]))]
# print(detail_info["image_list"][0])
# marged_image_list =detail_info["image_list"]
# marged_image_list = list(itertools.chain(*detail_info["image_list"]))

def run():
    soup_class_image_fluid = soup.find_all(class_="img-fluid img-thumbnail")

    print("🚩",list(enumerate(soup_class_image_fluid)))
    print("🆗"*15)

    img_tags = soup.find_all('img')
    print(img_tags)
    for src in soup_class_image_fluid:
        rc_no +=1
        print(f"{rc_no}:🚩",src.get("class"),"🆗")
        print(f"{rc_no}:🚩",src.get("src"),"🆗")

# r = requests.get(f"https://www.cpvppraktoni.com/index.php/alumni/alumni_list{id}/")
# r = requests.get("https://www.cpvppraktoni.com/alumni/alumni_list")
# print(r.text)
# with open(f"CPVP/alumni_list_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html","wb") as f:
#     # r = requests.get(r)
#     f.write(r.text)

# print(r.text)
#!===========CPVP===============
# urls =re.search(r'("https?:\/\/.[^\s>{}]+\.png")',r.text) 
# print(r.json)
# print(re.findall('("https?:\/\/.[^\s>{}]+\.png")',r.text))
# all_image_list = re.findall(r'(?P<hole_url>https?:\/\/.[^\s>{}]+(?P<name>(?:\w+[^\s>{}]+))\.(?:jpg|png))\?',r.text)
# print(list(enumerate(all_image_list)))
# decoded_list = [unquote(x[0]) for x in all_image_list]
# print(list(enumerate(decoded_list)))
# print(unquote(all_image_list[20][0]))

# r1 = requests.get(all_image_list[3])
#FIXME:==============
# for i in range(len(all_image_list)):
#     with open(f"IMAGES_FROM_WEB/{i}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg","wb") as f:
#         r = requests.get(all_image_list[i][0])
#         f.write(r.content)
#FIXME:==============

# print(r1.content)

# for i in urls:
#     print(urls.group(i))

# FIXME:================
# httpbin.org
#  0.9.2 
# [ Base URL: httpbin.org/ ]
# A simple HTTP Request & Response Service.

# Run locally: $ docker run -p 80:80 kennethreitz/httpbin
# FIXME:================

#! TO RUN: python requests_library.py