# this file collects video id from bilibili
from bs4 import BeautifulSoup
import requests
from crawler.scripts.video_download import download_vid
from crawler.scripts.GetAss import download_danmu
import re

#bilibili 生活区
DATA_PATH = './database/live.txt'
TMP_PATH = './database/live.txt.tmp'
URL = 'https://www.bilibili.com/ranking/all/160/0/1'

def parse_url(link):
    vid = None
    if link:
        if len(link) > 2 & (link[:2] == "//"):
            link = link[2:]
        else:
            return None
        if "video/av" in link:
            vid = link.split("/")[-2]
            if len(link != 34):
                print("exception found: {}".format(link))
    return vid


def read_data(file):
    data = {}
    f = open(file, 'r')
    for line in f.readlines():
        line = line.split("/")
        vid = line[0]
        is_d_downloaded = int(line[1])
        data[vid] = is_d_downloaded
    f.close()
    return data
    
def write_data(data):
    lines = []
    for key, value in data.items():
        line = "/".join([key,value])
        lines.append(line)
    with open(TMP_PATH, 'w') as o:
        o.writelines(lines)
    
# def process(data):
#     new_data = []
#     for line in data:
#         vid = line[0]
#         is_d_downloaded = int(line[1])
#
#         if not is_d_downloaded:
#             download_danmu(vid)
#             is_d_downloaded = 1
#         newline = "/".join([vid, str(is_d_downloaded)])
#         new_data.append(newline+'\n')
#     write_data(new_data)


    
def main():
    current_data = read_data(DATA_PATH)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in soup.find_all("a"):
        link = tag.get("href")
        vid = parse_url(link)
        if vid:
            if vid in current_data.keys():
                continue
            else:
                current_data[vid] = 0
    write_data(current_data)
    
            
            
            
            
            
            