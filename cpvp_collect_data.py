import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import unquote
import os
import itertools
import pandas as pd
import openpyxl

class CollectData:
    link_sort = staticmethod(lambda text: int(re.search(r"(\d*$)", text + "0").group()))
    def __init__(self, url, path):
        self.url = url
        self.path = path
        # print("Total Image File: ",self.count_files_in_folder("IMAGES/"))
        # print("Total HTML File: ",self.count_files_in_folder(""))
        
        if not self.count_files_in_folder("HTML/"):
            self.collect_pages()

        if not self.count_files_in_folder("IMAGES/"):
            self.image_extract()

        self.save_to_excel()
            
    def count_files_in_folder(self,file_path):
        return sum(bool(os.path.isfile(os.path.join(f"{self.path}/{file_path}", item)))
               for item in os.listdir(f"{self.path}/{file_path}"))
    
    @staticmethod
    def open_file(path,open_mode):
        with open(path,open_mode) as f:
            return f.read()
        
    @staticmethod
    def fetchAndSaveToFile(url, path): 
        r = requests.get(url) 
        with open(path, "w") as f: 
            f.write(r.text) 

    @staticmethod
    def cfDecodeEmail(encodedString):
        try:
            r = int(encodedString[:2],16)
            email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
        except Exception:
            email = "N/A"
        return email

    def page_navigation_link(self, first_url_list,soup):
        page_link = soup.find_all('li','a',class_="paginate_button page-item") 
        list_of_page_link = set((tuple(first_url_list)))
        url_set = {item.find("a").attrs["href"] for item in page_link}
        list_of_page_link.update(url_set)
        list_of_set = list(list_of_page_link)
        list_of_set.sort(key=CollectData.link_sort)
        return list_of_set

    def collect_pages(self):
        rc_no = 0
        write_read_path = f"{self.path}/HTML/{rc_no:04}.html"
        self.fetchAndSaveToFile(url=[self.url][rc_no],path=write_read_path)
        cpvp = self.open_file(write_read_path,"r")
        soup = BeautifulSoup(cpvp,'html.parser')
        navigation_link_set = self.page_navigation_link([self.url],soup)
        print(navigation_link_set)

        loop_status = True
        while loop_status:
            rc_no += 1
            write_read_path = f"{self.path}/HTML/{rc_no:04}.html"
            self.fetchAndSaveToFile(url=navigation_link_set[rc_no],path=write_read_path)
            cpvp = self.open_file(write_read_path,"r")
            soup = BeautifulSoup(cpvp,'html.parser')
            navigation_link_set = self.page_navigation_link(navigation_link_set,soup)
            print(navigation_link_set)

            if rc_no >= len(navigation_link_set)-1:
                loop_status = False
        return navigation_link_set
    
    def details(self):
        number_of_file_in_a_dir = len([name for name in os.listdir(f"{self.path}/HTML/") if os.path.isfile(os.path.join(f"{self.path}/HTML/", name))])
        image_list = []
        name_list = []
        occupation_list = []
        batch_list = []
        email_list = []

        for i in range(number_of_file_in_a_dir):
            read_path = f"{self.path}/HTML/{i:04}.html"
            current_file = self.open_file(read_path,"r")
            soup = BeautifulSoup(current_file,'html.parser')
            info_list = soup.select("table.table.table-striped.table-bordered>tbody>tr>td>div>div>div") #>img.img-fluid.img-thumbnail
            image_list.append([info_list[x].find("img").attrs["src"] for x in range(len(info_list)) if x%2==0])
            name_list.append([info_list[x].find("h5", class_="uppercase").find("b").text.strip().replace(":",".") for x in range(len(info_list)) if x%2==1])
            occupation_list.append([info_list[x].find("h6").text.strip() for x in range(len(info_list)) if x%2==1])
            batch_list.append([info_list[x].find_all(string=re.compile("Batch"))[0].strip() for x in range(len(info_list)) if x%2==1])
            email_code = [self.cfDecodeEmail(info_list[x].find("a").attrs["href"][len(r"/cdn-cgi/l/email-protection#"):]) for x in range(len(info_list)) if x%2==1]
            email_list.append(email_code)
        merged_image_list = list(itertools.chain(*image_list))
        merged_name_list = list(itertools.chain(*name_list))
        merged_occupation_list = list(itertools.chain(*occupation_list))
        merged_batch_list = list(itertools.chain(*batch_list))
        merged_email_list = list(itertools.chain(*email_list))
        merged_list = {"PHOTO":merged_image_list,
                        "Name":merged_name_list,
                        "Occupation":merged_occupation_list,
                        "SSC Batch":merged_batch_list,
                        "Email":merged_email_list
                        }
        return {"image_list":image_list,
                "name_list":name_list,
                "occupation_list":occupation_list,
                "batch_list":batch_list,
                "email_list":email_list,
                "merged_list":merged_list}
    
    def image_extract(self):
        detail_info = self.details()
        for i in range(len(detail_info["image_list"])):
            for y in range(len(detail_info["image_list"][i])):
                with open(f"{self.path}/IMAGES/{i}{y}_{detail_info['name_list'][i][y]}.jpg","wb") as f:
                    r = requests.get(detail_info["image_list"][i][y])
                    f.write(r.content)


    def save_to_excel(self):
        detail_info = self.details()
        # image_extract("CPVP/IMAGES",detail_info["image_list"],detail_info["name_list"])
        image_name_list_ = []

        for i in range(len(detail_info["image_list"])):
            image_name_list_.extend(
                f"{i}{j}_{detail_info['name_list'][i][j]}"
                for j in range(len(detail_info["image_list"][i]))
            )
        data = pd.DataFrame(detail_info["merged_list"]|{"Image":image_name_list_}, index=list(range(1,len(detail_info["merged_list"]["PHOTO"])+1))) #, index=list(range(1,len(detail_info["merged_list"]["PHOTO"])+1))
        data.to_excel(
            f"{self.path}/TEMP/cpvp_prahtoni_all.xlsx",
            sheet_name="cpvp_prahtoni_all",
            index=True,
            index_label="SL",
            freeze_panes=(1, 1),
        )


url = "https://www.cpvppraktoni.com/index.php/alumni/alumni_list/" 
path = "CPVP"

if __name__ == '__main__': 
    collect_data = CollectData(url,path)

#! To Run: python cpvp_collect_data.py