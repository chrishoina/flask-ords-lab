# to pip install in venv ONLY, use: "python -m pip install [library name]"

import folium 
from folium import plugins, JavascriptLink, Tooltip
import flask
from flask import Flask, json, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

m = folium.Map(location=[36.085645468598855, -115.08441257156686], zoom_start=10, min_zoom=10, tiles="Stamen Terrain")

tooltip = "Click me!"

response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/muesums/").json() 

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
 
    lvmap = m._repr_html_()

@app.route('/')
def index(): 
    return render_template('index.html', lvmap=lvmap)

@app.route('/get_price')
def get_hotdog_price():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/hotdogs/getprice/"+a
    print(url)
    response = requests.get(url)

    for ids in response.json()['items']:
        
        idList = dict()
        try:
            product_price = ids['product_price']       

        except:
            pass

    return jsonify(product_price)

@app.route('/order')
def order():
    def getTix():
         response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/")
         list_of_tix = []

         for tix in response.json()['items']:

            tixList = dict()
            try:

                product_id = tix['product_id']
                product_name = tix['product_name']

                tixList['product_id'] = product_id
                tixList['product_name'] = product_name
                
                list_of_tix.append(tixList)
                
            except:
                pass

            return list_of_tix

    list_of_tix = getTix()
    return render_template('order.html',list_of_tix_return=list_of_tix)

@app.route('/result', methods = ['POST', 'GET'])    
def result():
   url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/hotdogs/createorder/"
   if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        total = request.form.get('total')

        json_data = { "PRODUCT_ID": product_id, "QUANTITY": quantity, "TOTAL_PRICE": total }
    
        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        response = requests.post(url, json=json_data, headers=headers)
        return redirect('myorders')
