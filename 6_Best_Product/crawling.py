from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm

def get_search_page_url(keyword, page):
    return 'http://search.danawa.com/dsearch.php?query={}&volumeType=allvs&page={}&limit=30&sort=saveDESC&list=list&boost=true&addDelivery=N&tab=goods'.\
            format(keyword, page)

def get_prod_items(prod_items):
    prod_list = []
    
    for item in prod_items:
        try:
            name = item.select('p.prod_name > a')[0].text.strip()
        except:
            name = ''

        try:
            spec_list = item.select('div.spec_list')[0].text.strip()
        except:
            spec_list = ''

        try:
            price = item.select('div.prod_pricelist strong')[0].text.strip().replace(",","")
        except:
            price = 0

        prod_list.append([name, spec_list, price])

    return prod_list

driver = webdriver.Chrome('D:/DataAnalysis/chromedriver.exe')
driver.implicitly_wait(3)

keyword = '무선청소기'
total_page = 10
prod_data_total = []

for page in tqdm(range(1, total_page + 1)):
    url = get_search_page_url(keyword, page)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    prod_items = soup.select('div.main_prodlist.main_prodlist_list li.prod_item')
    prod_item_list = get_prod_items(prod_items)

    prod_data_total = prod_data_total + prod_item_list

prod_data_df = pd.DataFrame(prod_data_total)
prod_data_df.columns = ['상품명', '스펙 목록', '가격']
prod_data_df.to_excel('./files/무선청소기.xlsx', index=False)
