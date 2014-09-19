import os
from flask import Flask, render_template, request, Response, jsonify


app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
