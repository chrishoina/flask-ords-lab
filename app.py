# to pip install in venv ONLY, use: "python -m pip install [library name]"

from ast import Try
from traceback import print_tb
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

for museums in response['items']:
    # print(response['items'])
    try: 
        museum_id = museums['museum_id']
        museum_loc = museums['museum_location']
        museum_lat = museums['museum_lat']     
        museum_long = museums['museum_long']
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

#This is  my index page. We'll also load the folium map here. 
@app.route('/')
def index(): 
    return render_template('index.html', lvmap=lvmap)

# All of my GET request routes/definitions 
@app.route('/get_price')
def get_product_price():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/price/"+a
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
def get_product_description():
    a = request.args.get('a')
    url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/description/"+a
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
def orderMake():
    def getPasses():    
        response = requests.get("https://ENDPOINT_URL/ords/admin/products/")
        list_of_passes = []

        for passes in response.json()['items']:
            
            passesList = dict()
            try:

                product_id = passes['product_id']
                product_name = passes['product_name']

                passesList['product_id'] = product_id
                passesList['product_name'] = product_name
                
                list_of_passes.append(passesList)
                

            except:
                pass

        return list_of_passes

    list_of_passes = getPasses()
    return render_template('orderform.html', list_of_passes_return=list_of_passes)  

@app.route('/orderhistory')
def orderHistory():
    def getOrders():
        response = requests.get("https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/orders/")
        list_of_orders = []

        for orders in response.json()['items']:

            ordersList = dict()
            try:

                order_id = orders['product_id']
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
    return render_template('orderhistory.html', list_of_orders_return=list_of_orders)

@app.route('/result', methods = ['POST', 'GET'])    
def result():
   url = "https://gf641ea24ecc468-dbmcdeebyface.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/products/orders/"
   if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        total = request.form.get('total')
      
        json_data = { "PRODUCT_ID": product_id, "QUANTITY": quantity, "TOTAL_PRICE": total}

        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        response = requests.post(url, json=json_data, headers=headers)
        print(json_data)

        return redirect('orderhistory')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)