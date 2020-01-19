import pandas as pd

raw_total = pd.read_excel('./files/광주나주맛집.xlsx')
raw_total.head()

location_counts = raw_total['place'].value_counts()
location_counts

location_counts_df = pd.DataFrame(location_counts)
location_counts_df.head()

location_counts_df.to_excel('./files/광주나주맛집_카운트.xlsx')

locations = list(location_counts.index)
locations

import requests
import json

def find_places(searching):
    base_url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    query_string = '?query=' + searching + '&x=126.977967&y=37.566329'
    url = base_url + query_string
    
    headers = {"Authorization": "KakaoAK 87a8a63401d005b12f8f350c9393f4db"}
    places = json.loads(str(requests.get(url,headers=headers).text))['documents']

    place = places[0]
    name = place['place_name']
    x = place['x']
    y = place['y']
    data = [name, x, y, searching]
    
    return data

data = find_places('제주공항')
data

import time

locations_inform = [ ]
for location in locations:
    try:
        data = find_places(location)
        locations_inform.append(data)
        time.sleep(0.5)
    except:
        pass

locations_inform_df = pd.DataFrame(locations_inform)
locations_inform_df.columns = ['카카오맵위치명', '경도', '위도', '인스타위치명']
locations_inform_df.to_excel('./files/광주나주위치.xlsx', index=False)

location_counts_df = pd.read_excel('./files/광주나주맛집_카운트.xlsx')
location_inform_df = pd.read_excel('./files/광주나주위치.xlsx')
location_counts_df.columns = ['위치명', 'place']

location_data = pd.merge(location_inform_df, location_counts_df, how='inner', left_on='카카오맵위치명', right_on='위치명')
location_data.head()

location_data.to_excel('./files/광주나주위치정보.xlsx', index=False)

location_data = pd.read_excel('./files/광주나주위치정보.xlsx')
location_data.info()
location_data.head()

import folium

Mt_Naju_Station = [35.014250, 126.717045]
map_naju = folium.Map(location = Mt_Naju_Station, zoom_start = 11)

for i in range(len(location_data)):
    name = location_data['카카오맵위치명'][i]
    count = location_data['place'][i]
    size = int(count) * 2
    long = float(location_data['위도'][i])
    lat = float(location_data['경도'][i])
    folium.CircleMarker((long, lat), radius=size, color='red', popup=name).add_to(map_naju)

map_naju


from folium.plugins import MarkerCluster

locations = []
names = []

for i in range(len(location_data)):
    data = location_data.iloc[i]
    locations.append((float(data['위도']), float(data['경도'])))
    names.append(data['카카오맵위치명'])

icon_create_function = """\
function(cluster) {
    return L.divIcon({
    html: '<b>' + cluster.getChildCount() + '</b>',
    className: 'marker-cluster marker-cluster-large',
    iconSize: new L.Point(30, 30)
    });
}"""

Mt_Naju_Station = [35.014250, 126.717045]
map_naju2 = folium.Map(location = Mt_Naju_Station, zoom_start = 11)

marker_cluster = MarkerCluster(
    locations=locations, popups=names,
    name='Naju', overlay=True, control=True,
    icon_create_function=icon_create_function
)

marker_cluster.add_to(map_naju2)
folium.LayerControl().add_to(map_naju2)

map_naju2