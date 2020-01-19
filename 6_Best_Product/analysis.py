import pandas as pd

danawa_data = pd.read_excel('./files/핸디_스틱청소기.xlsx')
danawa_data.head()

top_list = danawa_data.sort_values(['사용시간', '흡입력'], ascending=False)
top_list.head()

price_mean_value = danawa_data['가격'].mean()
suction_mean_value = danawa_data['흡입력'].mean()
use_time_mean_value = danawa_data['사용시간'].mean()
price_mean_value
suction_mean_value
use_time_mean_value

condition_data = danawa_data[
    (danawa_data['가격'] <= price_mean_value) &
    (danawa_data['흡입력'] >= suction_mean_value) &
    (danawa_data['사용시간'] >= use_time_mean_value)
]
condition_data.sort_values(['가격'], ascending=True)

chart_data = danawa_data.dropna(axis=0)
len(chart_data)

suction_max_value = danawa_data['흡입력'].max()
use_time_max_value = danawa_data['사용시간'].max()
suction_min_value = danawa_data['흡입력'].min()
use_time_min_value = danawa_data['사용시간'].min()

import matplotlib.pyplot as plt
import seaborn as sns
import platform

plt.figure(figsize=(20,10))
plt.title("무선 핸디/스틱청소기 차트")
sns.scatterplot(x='흡입력', y='사용시간', size='가격',
                hue=chart_data['회사명'], data=chart_data,
                sizes=(10,1000), legend=False)
plt.plot([0, suction_max_value],
        [use_time_mean_value, use_time_mean_value],
        'r--',
        lw=1)
plt.plot([suction_mean_value, suction_mean_value],
        [0, use_time_max_value],
        'r--',
        lw=1)
plt.savefig('./files/무선 핸디_스틱청소기 차트', dpi=1000)

chart_data_selected = chart_data[:20]
len(chart_data_selected)

suction_max_value = chart_data_selected['흡입력'].max()
use_time_max_value = chart_data_selected['사용시간'].max()
suction_mean_value = chart_data_selected['흡입력'].mean()
use_time_mean_value = chart_data_selected['사용시간'].mean()

plt.figure(figsize=(20,10))
plt.title("무선 핸디/스틱청소기 차트")
sns.scatterplot(x='흡입력', y='사용시간', size='가격',
                hue=chart_data_selected['회사명'], data=chart_data_selected,
                sizes=(10,2000), legend=False)
plt.plot([60, suction_max_value],
        [use_time_mean_value, use_time_mean_value],
        'r--',
        lw=1)
plt.plot([suction_mean_value, suction_mean_value],
        [20, use_time_max_value],
        'r--',
        lw=1)

for index, row in chart_data_selected.iterrows():
    x = row['흡입력']
    y = row['사용시간']
    s = row['제품'].split(' ')[0]
    plt.text(x, y, s, size=20)

plt.savefig('./files/무선 핸디_스틱청소기 Top20 차트', dpi=1000)

chart_data_selected