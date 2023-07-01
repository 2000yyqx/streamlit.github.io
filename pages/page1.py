import streamlit as st

import requests

import json

st.title('重庆旅游景点分布')
import pandas as pd
url="https://github.com/2000yyqx/streamlit.github.io/blob/main/CQ.csv"
geo = pd.read_csv(url)
import geopandas as gpd
file_path="https://github.com/2000yyqx/streamlit.github.io/blob/main/locations.geojson"  # 文件路径，需要替换为实际的文件路径
geo = gpd.read_file(file_path)
Minx=min(geo.bounds["minx"])
Miny=min(geo.bounds["miny"])
Maxx=max(geo.bounds["maxx"])
Maxy=max(geo.bounds["maxy"])
import folium
from folium import Marker
from folium import FeatureGroup
from folium.plugins import MiniMap
url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
#tiles="http://api.map.baidu.com/customimage/tile?x={x}&y={y}&z={z}&udt=20190118&scale=1&ak=LZomarHPjAy7GZcZQVEcMNDTGsiQKq6B"
#attr='百度地图'
tiles = 'http://webst01.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}'
attr = '高德地图'
m = folium.Map(tiles = tiles,attr=attr,width = 1000,height = 600)
m.fit_bounds([(Miny,Minx),(Maxy,Maxx)])                           #根据获取的范围创建初始地图
arcgisonline=folium.TileLayer(tiles = url,attr="ArcGIS online")   #增加一个arcgisonline地图
arcgisonline.add_to(m)
layer = FeatureGroup(name='POI', control=True)                    #创建POI点图层并添加到地图控件对象中
for i in range(len(geo.bounds)):
    marker = Marker(location = (geo.bounds.miny[i],geo.bounds.minx[i]))
    marker.add_to(layer)
layer.add_to(m)
folium.LayerControl().add_to(m)

for j in range(len(geo)):     #赋予POI点popup属性，包括NAME、text及photo_url链接的缩略图
    name=geo.name[j]
    place = geo.places[j]
    position=geo.position[j]
    pm = geo.pm[j]
    html = f"""<h3>{name}</h3>
               <h4>{position}</h4>
               <h6>{place}</h6>
               <p>点评数量排名_全国</p>
               <h7>{pm}</h7>
            """
    popup = folium.Popup(html,max_width=200)
    folium.Marker(location=[geo.bounds.miny[j],geo.bounds.minx[j]],
                  popup=popup).add_to(m)
minimap = MiniMap(toggle_display=True)                            #在地图控件中添加索引图控件
m.add_child(minimap)
#m.save('map.html')
#st.components.v1.html(open('map.html', 'r').read(), width=800, height=600)
#st.map(m)
from streamlit_folium import folium_static
folium_static(m)
def show():
    st.title("景点分布")

