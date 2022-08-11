from flask import Flask, render_template, redirect, url_for
# this line says that we'll use Flask to render a template, redirecting to another URL and creating a URL. 
from flask_pymongo import PyMongo
# this line says we'll use PyMOngo to interact with our Mongo database. 
import scraping
# this line says to use the scraping code, we will convert from Jupyter notebook to python.

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# tell python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.

mongo = PyMongo(app)
# is the URI we'll be uring to connect our app to Mongo. 

@app.route("/")
# tells Flask what to display when we're looking at the home page. This means that when we visit our web apps' HTML page we will see the home page. 
def index():
    
   mars = mongo.db.mars.find_one()
   # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python script. We will also assign the path to the mars
   # variable for use later. 
   return render_template("index.html", mars=mars)
   # tells Flask to return an HTML template using an index.html.file. 

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302) 

if __name__ == "__main__":
   app.run() 