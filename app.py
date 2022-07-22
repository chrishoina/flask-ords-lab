# to pip install in venv ONLY, use: "python -m pip install [library name]"
# Folium is a library used for rendering maps, with informational overlays. It is based off of the popular map rendering library "Leaflet.js"
import folium 

# There are various functions we'll need to import. For instance, in order for the Tooltip to work, we'll need to import manually 
from folium import plugins, JavascriptLink, Tooltip, Icon

# The same applies here. We have the base flask, but then we'll need to import things like render_template, and jsonify (in this case to help us work with json objects)
import flask
from flask import Flask, json, render_template, request, redirect, jsonify

# The requests library is key. You can do much of the same with the urllib library. And you may be able to achieve similar results with Beautiful Soup. But requests is all we need to make this work. 

import requests

# Importing json manually is probably an unecessary step, as it is included in Python. But we'll leave it here for demonstrational purposes. 
import json 

app = Flask(__name__)

m = folium.Map(location=[36.085645468598855, -115.08441257156686], zoom_start=10, min_zoom=10, tiles="Stamen Toner")

tooltip = "Click me!"

response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/locations/map/data").json()

for museums in response['items']:
    try: 
        museum_id = museums['museum_id']
        museum_lat = museums['museum_lat']     
        museum_long = museums['museum_long']
        museum_name = museums['museum_name']

    except: 
        continue

    folium.Marker(
        location=[museum_lat, museum_long],
        popup=folium.Popup("<i>{}</i>".format(museum_name), max_width=450), icon=folium.Icon(color="lightred", icon="info-sign"),
        tooltip=tooltip
        ).add_to(m)
 
lvmap = m._repr_html_()

# *** Here you will see all the application routes and any associated .html they direct to *** 

@app.route('/')
def index(): 
    return render_template('index.html', lvmap=lvmap)

# All of my GET request routes/definitions 
@app.route('/get_price')
def getPrice():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/products/value/"+a
    # print(url)
    response = requests.get(url)

    for ids in response.json()['items']:
    
        idList = dict()
        try:
            product_price = ids['product_price']       

        except:
            pass
   
    return jsonify(product_price)
   
@app.route('/get_description')
def getDescription():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/products/info/"+a
    # print(url)
    response = requests.get(url)

    for ids in response.json()['items']:
        
        idList = dict()
        try:
            product_description = ids['product_description']       

        except:
            pass

    return jsonify(product_description)

@app.route('/orderform') 
def orderMake():
    def getProducts():    
        response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/")
        list_of_products = []

        for products in response.json()['items']:
            
            productList = dict()
            try: 
                product_id = products['product_id']
                product_name = products['product_name'] 

                productList['product_id'] = product_id
                productList['product_name'] = product_name
                
                list_of_products.append(productList)
                
            except:
                pass

        return list_of_products

    list_of_products = getProducts()
    return render_template('orderform.html', list_of_products_from_request=list_of_products)   

@app.route('/orderhistory')
def orderHistory():
    def getOrders():
        response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/purchases/history")
        list_of_orders = []

        for orders in response.json()['items']:

            ordersList = dict()
            try:

                order_id = orders['order_id']
                product_name = orders['product_name']
                product_description = orders['product_description']
                quantity = orders['quantity']
                total_price = orders['total_price']

                ordersList['order_id'] = order_id
                ordersList['product_name'] = product_name
                ordersList['product_description'] = product_description 
                ordersList['quantity'] = quantity
                ordersList['total_price'] = total_price

                list_of_orders.append(ordersList)

            except:
                pass

        return list_of_orders 
 
    list_of_orders = getOrders()
    return render_template('orderhistory.html', list_of_orders_from_request=list_of_orders)

@app.route('/result', methods = ['POST', 'GET'])    
def result():
   url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/purchases/history"
   if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        total = request.form.get('total_price')
      
        json_data = { "PRODUCT_ID": product_id, "QUANTITY": quantity, "TOTAL_PRICE": total}

        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        response = requests.post(url, json=json_data, headers=headers)
  
        return redirect('orderhistory')

# @app.route('/newsletter', methods = ['POST', 'GET'])    
# def newsletter(): 

#     url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/flaskordslab/outreach/list"
#     if request.method == 'POST':
#         user_email = request.form.get('email')

#         json_data = { "USER_EMAIL": user_email }

#         headers = {'Content-type':'application/json', 'Accept':'application/json'}
#         response = requests.post(url, json=json_data, headers=headers)

#         return ''

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)