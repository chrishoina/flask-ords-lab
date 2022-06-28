# to pip install in venv ONLY, use: "python -m pip install [library name]"

from ast import Try
import folium 
from folium import plugins, JavascriptLink, Tooltip
import flask
from flask import Flask, json, render_template, request, redirect, jsonify
import requests
import json 

app = Flask(__name__)

m = folium.Map(location=[36.085645468598855, -115.08441257156686], zoom_start=10, min_zoom=10, tiles="Stamen Terrain")

tooltip = "Click me!"

response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/museums/").json()

# for i in response.iter_content():
#     print(i)
# print(response.iter_content)

for museums in response['items']:
    # print(response['items'])
    try: 
        museum_id = museums['museum_id']
        museum_loc = museums['museum_location']
        museum_lat = museums['museum_lat']
        # print(museum_lat)
        museum_long = museums['museum_long']
        # print(museum_long)
        museum_name = museums['museum_name']
        folium.Marker(tooltip=tooltip,location=[museum_lat, museum_long], popup=folium.Popup("<i>{}</i>".format(museum_name), max_width=450),).add_to(m)
    except: 
        continue
    # list_of_museums.append(museumList)

    # folium.Marker(
    #     location=[museum_lat, museum_long],
    #     popup=folium.Popup("<i>{}</i>".format(museum_name), max_width=450),
    #     tooltip=tooltip
    #     ).add_to(m)
 
# m.save('foliummap.html') 
# m._repr_html_()
lvmap = m._repr_html_()

@app.route('/')
def index(): 
    return render_template('index.html', lvmap=lvmap)

@app.route('/get_price')
def get_product_price():
    a = request.args.get('a')
    url = " https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/price/"+a
    # print(url)
    response = requests.get(url)

    for ids in response.json()['items']:
    
        idList = dict()
        # print("ID List")
        # print(idList)
        try:
            product_price = ids['product_price']       

        except:
            pass
    print(product_price)
    print(type(product_price))
    jprod = jsonify(product_price)
    
    print(type(jprod))
    return jprod



@app.route('/get_description')
def get_product_description():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/getdescription/"+a
    # print(url)
    response = requests.get(url)

    for ids in response.json()['items']:
        
        idList = dict()
        try:
            product_description = ids['product_description']       

        except:
            pass

    return jsonify(product_description)

@app.route('/order')
def order():
    def getProducts():
        response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/")
        list_of_products = []

        for products in response.json()['items']:

            productList = dict()
            try:

                product_id = products['product_id']
                product_name = products['product_name']
                product_description = products['product_description']
             

                productList['product_id'] = product_id
                productList['product_name'] = product_name
                productList['product_description'] = product_description 

                list_of_products.append(productList)

            except:
                pass

        return list_of_products 
 
    list_of_products = getProducts()
    return render_template('order.html', list_of_products_return=list_of_products)

@app.route('/result', methods = ['POST', 'GET'])    
def result():
   url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/orders/"
   if request.method == 'POST':
        product_id = request.form.get('product_id')
        # print(type(product_id))
        product_price = request.form.get('product_price')
        
        product_description = request.form.get('product_description')
        print(product_description)
        # print(type(product_price))
        # print(product_price) 
        json_data = { "PRODUCT_ID": product_id, "PRODUCT_PRICE": product_price}
        # print(json_data)

        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        response = requests.post(url, json=json_data, headers=headers)
        print(json_data)
        return redirect('orderhistory')

@app.route('/orderhistory')
def myOrders():
    return render_template('orderhistory.html')
