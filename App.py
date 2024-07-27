"""
Final Project - Healthy Food Planner
CST 205
Abstract: With a simple interface, Project App lets users search for recipes by keyword, filter results by categories, 
and view detailed information about each recipe. 
Each recipe includes ingredients, preparation instructions, nutritional information. 
This makes it easy for users to decide what to cook and ensures they have all the details to make a delicious meal.

Authors: Diego Valdez, Mark Roland Garban, and Vera Boukhonine
Date: 07/26/2024

Who Worked on What:
Mark and Vera worked on routes in the backend and setting up a simple UI. Mark made the index.html and search funcitonality. 
Vera worked on the recipe.html to allow users to view recipe info. Diego worked on routes in the backend as well making fixes. 
"""

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

# flask --app App --debug run
API_KEY = "14b2d074b0a84e4dacf83ae3f7036d38"

app = Flask(__name__)
app.config["SECRET_KEY"] = "csumb-otter"
bootstrap = Bootstrap5(app)


@app.route("/")
def index():
    return render_template("index.html")


# Search's for recipes by keyword
@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])

# Gets recipe info based on the id when a recipe title is clicked on
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    url = (
        f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    )
    try:
        response = requests.get(url)
        recipe_data = response.json()
        return render_template("recipe.html", recipe=recipe_data)
    except Exception as e:
        print(e)
        return "An error occurred. Please try again."


# Filters results by categories
@app.route("/vegan")
def vegan_recipes():
    url = (
        f"https://api.spoonacular.com/recipes/complexSearch?diet=vegan&apiKey={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])


# Filters results by categories
@app.route("/gluten_free")
def gluten_free_recipes():
    url = f"https://api.spoonacular.com/recipes/complexSearch?diet=gluten+free&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])


# Give a description about us
@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


# Find random recipes and displays them
@app.route("/random_recipes")
def random_recipes():
    url = f"https://api.spoonacular.com/recipes/random?number=10&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("random_recipes.html", recipes=data[""])


if __name__ == "__main__":
    app.run(debug=True)
