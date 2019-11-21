from flask import Flask, render_template, jsonify, redirect
from flask_cors import CORS
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
CORS(app)
USERNAME = 'userAdmin'
PASSWORD = 'Catpuss10!'
PORT = '27017'
HOST = 'localhost'

app.config['MONGO_DBNAME'] = 'mars'
app.config['MONGO_HOST'] = HOST
app.config['MONGO_PORT'] = PORT
app.config['MONGO_USERNAME'] = USERNAME
app.config['MONGO_PASSWORD'] = PASSWORD
app.config["MONGO_URI"] = "mongodb://localhost:27017/visipedia_annotation_toolkit"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)