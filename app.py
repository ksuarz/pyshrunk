import os
from flask import Flask, render_template, request, Response, jsonify


app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/login')
def login():
    pass

@app.route('/u')
def home():
    return render_template('main.html')

@app.route('/g')
def group():
    pass

@app.route('/<hash>')
def route_to_link(hash):
    pass

@app.route('/l/<hash>')
def link_info(hash):
    pass

@app.route('/b/<hash>')
def bundle(hash):
    pass

""" 
    need a route for the /shorturl
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
