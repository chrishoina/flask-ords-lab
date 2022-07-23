import folium
from folium import plugins, JavascriptLink, Tooltip
import requests
import json

m = folium.Map(location=[36.085645468598855, -115.08441257156686], zoom_start=11, tiles="Stamen Terrain")

tooltip = "Click me!"

response = requests.get("https://[Your endpoint goes here].com/ords/[additional/path info/goes here]/").json() 

for museums in response['items']: 
    msm_id = museums['msm_id']
    msm_name = museums['msm_name']
    msm_loc = museums['msm_location']
    msm_lat = museums['msm_lat']
    msm_long = museums['msm_long']

    folium.Marker(
        location=[msm_lat, msm_long],
        popup=folium.Popup("<i>{}</i>".format(msm_name), max_width=450),
        tooltip=tooltip
        ).add_to(m)

m.save('folium.html')  