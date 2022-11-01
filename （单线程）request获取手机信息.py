import os
import random
import time
import re
import requests
from bs4 import BeautifulSoup
# 读取所有的url
def loadData(filename):
    data = []
    with open(filename,'r',encoding='utf-8') as f:
        for line in f.readlines():
            data.append(line.strip())
    return data

phone_url = '../data/输入文档/phone_url.txt'
phone_url_list = loadData(phone_url)
print(phone_url_list)

proxy = [
    {'HTTP': '223.96.90.216:8085', 'HTTPS': 'https://223.96.90.216:8085'},
    {'HTTP': '61.216.185.88:60808', 'HTTPS': 'https://61.216.185.88:60808'},
    {'HTTP': '47.105.91.226:8118', 'HTTPS': 'https://47.105.91.226:8118'},
    {'HTTP': '115.29.170.58:8118', 'HTTPS': 'https://115.29.170.58:8118'}
]

# 获取全量数据
def get_content(phone_url_list):

    for phone_url in phone_url_list:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71'}
        response = requests.get(url=phone_url, headers=headers, proxies=random.choice(proxy), timeout=3)

        soup = BeautifulSoup(response.text, 'html.parser')

        # 导入CSV安装包D:\99.0.4844.51_chrome64_stable_windows_installer\Chrome-bin
        import csv
        # 1. 创建文件对象
        f = open('../data/输出csv/由网址爬取的手机信息test.csv', 'a', encoding='utf-8', newline='')
        # 或者：
        # with open('A.csv', 'a', encoding='utf-8', newline='') as f:
        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)

        # soup = BeautifulSoup(browser.page_source, "lxml")
        time.sleep(1)
        try:
            sim_card = soup.find(attrs={'data-spec': 'sim'}).text
        except:
            sim_card = 'not find'

        announced = soup.find(attrs={'data-spec': 'year'}).text
        network = soup.find(attrs={'data-spec': 'nettech'}).text

        try:
            nfc = soup.find(attrs={'data-spec': 'nfc'}).text
        except:
            nfc = 'not find'
        try:
            memory = soup.find(attrs={'data-spec': 'internalmemory'}).text
        except:
            memory = 'not find'
        phone_size = soup.find(attrs={'data-spec': 'dimensions'}).text
        phone_weight = soup.find(attrs={'data-spec': 'weight'}).text
        phone_displayresolution = soup.find(attrs={'data-spec': 'displayresolution'}).text
        try:
            phone_batdescription2 = \
            soup.find(attrs={'href': 'glossary.php3?term=battery-charging'}).parent.parent.find('td',
                                                                                                class_='nfo').text.splitlines()[
                0]
        except:
            phone_batdescription2 = 'not find'
        phone_batdescription1 = soup.find(attrs={'data-spec': 'batdescription1'}).text
        try:
            phone_cam2 = soup.find(attrs={'href': 'glossary.php3?term=secondary-camera'}).text
        except:
            phone_cam2 = 'not find'
        try:
            phone_cam1 = soup.find(attrs={'href': 'glossary.php3?term=camera'}).text
        except:
            phone_cam1 = 'not find'

        phone_usb = soup.find(attrs={'data-spec': 'usb'}).text
        phone_gps = soup.find(attrs={'data-spec': 'gps'}).text
        phone_bluetooth = soup.find(attrs={'data-spec': 'bluetooth'}).text
        phone_wlan = soup.find(attrs={'data-spec': 'wlan'}).text
        try:
            phone_cpu = soup.find(attrs={'data-spec': 'cpu'}).text
        except:
            phone_cpu = 'not find'
        try:
            phone_chipset = soup.find(attrs={'data-spec': 'chipset'}).text
        except:
            phone_chipset = 'not find'

        phone_os = soup.find(attrs={'data-spec': 'os-hl'}).text

        phone_info = [phone_url, sim_card, announced, network, nfc, memory, phone_size, phone_weight,
                      phone_displayresolution, phone_batdescription2, phone_batdescription1, phone_cam2, phone_cam1,
                      phone_usb, phone_gps, phone_bluetooth, phone_wlan, phone_cpu, phone_chipset, phone_os]
        print("|".join(phone_info))

        csv_writer.writerow(phone_info)
        f.close()  # with方法不需要关闭文件


if __name__=='__main__':
    get_content(phone_url_list)
