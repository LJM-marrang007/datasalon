from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome('D:/DataAnalysis/chromedriver.exe')
url = 'https://www.istarbucks.co.kr/store/store_map.do?disp=locale'
driver.get(url)

junnam_btn = '#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(12) > a'
driver.find_element_by_css_selector(junnam_btn).click()

all_btn = '#mCSB_2_container > ul > li:nth-child(1) > a'
driver.find_element_by_css_selector(all_btn).click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

starbucks_soup_list = soup.select('li.quickResultLstCon')
print(len(starbucks_soup_list[0]))

starbucks_list = []
for item in starbucks_soup_list:
    name = item.select('strong')[0].text.strip()
    lat = item['data-lat'].strip()
    lng = item['data-long'].strip()
    store_type = item.select('i')[0]['class'][0][4:]
    address = str(item.select('p.result_details')[0]).split('<br/>')[0].split('>')[1]
    tel = str(item.select('p.result_details')[0]).split('<br/>')[1].split('<')[0]

    starbucks_list.append([name, lat, lng, store_type, address, tel])

starbucks_list

columns = ['매장명', '위도', '경도', '매장타입', '주소', '전화번호']
junnam_starbucks_df = pd.DataFrame(starbucks_list, columns=columns)
junnam_starbucks_df.head()

junnam_starbucks_df.info()

junnam_starbucks_df.to_excel('./files/나주스타벅스리스트.xlsx', index=False)

