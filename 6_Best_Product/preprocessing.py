import pandas as pd

data = pd.read_excel('./files/무선청소기.xlsx')
data.info()
data.head()

data['상품명'][:10]

company_list = []
product_list = []
for title in data['상품명']:
    title_info = title.split(' ', 1)
    company_list.append(title_info[0])
    product_list.append(title_info[1])

company_list[:5]
product_list[:5]

data['스펙 목록'][0]

category_list = []
use_time_list = []
suction_list = []

for spec_data in data['스펙 목록']:
    spec_list = spec_data.split(' / ')

    category_list.append(spec_list[0])
    use_time = None
    suction = None
    for spec in spec_list:
        if '사용시간' in spec:
            use_time = spec.split(' ')[1].strip()
        elif '흡입력' in spec:
            suction = spec.split(' ')[1].strip()
    use_time_list.append(use_time)
    suction_list.append(suction)

len(category_list)
len(use_time_list)
len(suction_list)

price_list = []
for price_data in data['가격']:
    if '일시품절' in price_data:
        price = None
    else:
        price = int(price_data)
    price_list.append(price)

def convert_time_minute(time):
    try:
        if '시간' in time:
            hour = time.split('시간')[0]
            if '분' in time:
                minute = time.split('시간')[-1].split('분')[0]
            else:
                minute = 0
        else:
            hour = 0
            minute = time.split('분')[0]
        return int(hour)*60 + int(minute)
    except:
        return None

new_use_time_list = []

for time in use_time_list:
    new_use_time_list.append(convert_time_minute(time))

use_time_list[:10]
new_use_time_list[:10]

def get_suction(value):
    try:
        value = value.upper()
        if "AW" in value or "W" in value:
            result = value.replace("AW", "").replace("W", "")
            result = int(result.replace(",", ""))
        elif "PA" in value:
            result = value.replace("PA", "")
            result = int(result.replace("," ,"")) / 100
        else:
            result = None
        return result
    except:
        return None

new_suction_list = []
for suction in suction_list:
    new_suction_list.append(get_suction(suction))

len(suction_list)
len(new_suction_list)

pd_data = pd.DataFrame()
pd_data['카테고리'] = category_list
pd_data['회사명'] = company_list
pd_data['제품'] = product_list
pd_data['가격'] = price_list
pd_data['사용시간'] = new_use_time_list
pd_data['흡입력'] = new_suction_list
pd_data.head()
pd_data.info()
pd_data['카테고리'].value_counts()

pd_data_final = pd_data[pd_data['카테고리'].isin(['핸디/스틱청소기'])]
len(pd_data_final)

pd_data_final.to_excel('./files/핸디_스틱청소기.xlsx', index=False)