from flask import Flask, jsonify, render_template, request
from flask_paginate import Pagination, get_page_parameter
import requests

app = Flask(__name__)


@app.route("/")
def home():   
    return render_template('index.html')

@app.route("/search", methods=['GET'])
def search_bar():
    user = request.args.get('user', '')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    user.title()
    response = requests.get(url= f"https://api.openbrewerydb.org/v1/breweries/search?query={user}")
    response.raise_for_status
    data = response.json()
    per_page = 9 
    total = len(data)  
    pagination = Pagination(page=page, per_page=per_page, total=total,)
    start = (page - 1) * per_page
    end = start + per_page
    displayed_breweries = data[start:end]
    return render_template('search.html',data=displayed_breweries, pagination=pagination)
  

@app.route("/random")   
def random():
    response = requests.get(url="https://api.openbrewerydb.org/v1/breweries/random?size= 6")
    response.raise_for_status
    data = response.json()
    return render_template('random.html',data=data)
    
@app.route('/all', methods=['GET'])
def get_all():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    response = requests.get("https://api.openbrewerydb.org/v1/breweries")
    response.raise_for_status()
    data = response.json()
    per_page = 9 
    total = len(data)  
    pagination = Pagination(page=page, per_page=per_page, total=total,)
    start = (page - 1) * per_page
    end = start + per_page
    displayed_breweries = data[start:end]
    return render_template('all.html', data=displayed_breweries, pagination=pagination)


if __name__ == '__main__':
    app.run(debug=True)
    