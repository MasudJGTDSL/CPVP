import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import unquote
import os
from pathlib import Path
import itertools
import pandas as pd
import openpyxl
import json


BASE_DIR = Path(__file__).resolve().parent

html_folder = BASE_DIR / "SATVAI/HTML/"
image_folder = BASE_DIR / "SATVAI/IMAGES/"
temp_dir = BASE_DIR / "SATVAI/TEMP/"


def open_file(path,open_mode):
    with open(path,open_mode) as f:
        return f.read()

def fetchAndSaveToFile(): 
    r = requests.get(url)
    with open(f"{html_folder}/0001.html", "w") as f: 
        f.write(r.text)
    for rc_no, _ in enumerate(range(38), start=2):
        r = requests.get(f"{page_url}{rc_no}/")
        with open(f"{html_folder}/{rc_no:04}.html", "w") as f: 
            f.write(r.text) 

def details():
    number_of_file_in_a_dir = len([name for name in os.listdir(f"{html_folder}") if os.path.isfile(f"{html_folder}/{name}")])
    image_list = []
    name_list = []
    price_list = []
    category_list = []

    for i in range(number_of_file_in_a_dir):
        read_path = f"{html_folder}/{i+1:04}.html"
        current_file = open_file(read_path,"r")
        soup = BeautifulSoup(current_file,'html.parser')

        info_list = soup.select("li>a.woocommerce-LoopProduct-link") #>img.img-fluid.img-thumbnail
        image_list.extend([info_list[x].find("img").attrs["src"].split("?")[0] for x in range(len(info_list))])
        name_list.extend([info_list[x].find("h2", class_="woocommerce-loop-product__title").text.replace('/','').replace(',',' ').replace(':',' ') for x in range(len(info_list))])
        price_list.extend([info_list[x].find("bdi").text[3:] if info_list[x].find("bdi") is not None else 0 for x in range(len(info_list))])

        cat_list = soup.select(".gtm4wp_productdata")
        category_list.extend([json.loads(cat_list[x]["data-gtm4wp_product_data"])["item_category"] for x in range(len(cat_list))])
        image_field_list = [f"images/{i}.jpg" for i in range(1,len(image_list)+1)]
    return {"image_list":image_list,
            "plant_name":name_list,
            "price":price_list,
            "category":category_list,
            "image": image_field_list,
            }

def image_extract():
    detail_info = details()
    for i in range(len(detail_info["image_list"])):
        with open(f"{image_folder}/{i+1}.jpg","wb") as f:
            r = requests.get(detail_info["image_list"][i])
            f.write(r.content)

def save_to_excel():
    detail_info = details()
    detail_info.pop("image_list")
    data = pd.DataFrame(detail_info, 
                        index=list(range(1,len(detail_info["plant_name"])+1)))
    data.to_excel(
        f"{temp_dir}/satavi.xlsx",
        sheet_name="satavi_all",
        index=True,
        index_label="id",
        freeze_panes=(1, 1),
    )

          
    def count_files_in_folder(self,file_path):
        return sum(bool(os.path.isfile(os.path.join(f"{self.path}/{file_path}", item)))
               for item in os.listdir(f"{self.path}/{file_path}"))






url = 'https://www.satvai.com/'
page_url = 'https://www.satvai.com/page/'
if __name__ == '__main__': 
    # fetchAndSaveToFile()
    # details()
    save_to_excel()
    # image_extract()

#! To Run: python ./nursery/collect_data.py