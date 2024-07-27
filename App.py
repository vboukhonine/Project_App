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


@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])


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


@app.route("/vegan")
def vegan_recipes():
    url = (
        f"https://api.spoonacular.com/recipes/complexSearch?diet=vegan&apiKey={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])


@app.route("/gluten_free")
def gluten_free_recipes():
    url = f"https://api.spoonacular.com/recipes/complexSearch?diet=gluten+free&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("index.html", recipes=data["results"])

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/random_recipes")
def random_recipes():
    url = f"https://api.spoonacular.com/recipes/random?number=10&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("random_recipes.html", recipes=data[""])

if __name__ == "__main__":
    app.run(debug=True)
