from flask import Flask
from flask import render_template
from flask import request
import requests
import countryflag
import random
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template("index.html")
    
@app.route("/search", methods = ["POST"])
def search():
    query = request.form["textbox"]
    cats = requests.get("https://api.thecatapi.com/v1/breeds/search", params= {"api_key":api_key, "q":query}).json()
    for cat in cats:
        try:
            cat["nameflag"] = cat["name"] + " " + countryflag.getflag(cat["country_code"])
        except:
            cat["nameflag"] = cat["name"]
    return render_template("search.html", query = query, cats = cats)

    

@app.route("/cat/<cat>")
def getcat(cat):
    cat = requests.get("https://api.thecatapi.com/v1/breeds/search", params= {"api_key":api_key, "q":cat}).json()[0]
    return render_template("cat.html", cat = cat)

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/quizdata")
def quizdata():
    cats = requests.get("https://api.thecatapi.com/v1/breeds", params={"api_key":api_key}).json()
    quiz = []
    for i in range(4):
        catchosen = random.choice(cats)
        incorrectcats = []
        for i in range(3):
            incorrectcats.append(random.choice(cats)["name"])
        catoptions = incorrectcats
        catoptions.append(catchosen["name"])
        random.shuffle(catoptions)
        quiz.append({"que" : f"Which cat can be described as {catchosen["temperament"]}?", "opt" : catoptions, "ans" : catoptions.index(catchosen["name"]) + 1})
    return quiz


    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)