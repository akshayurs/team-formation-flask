import numpy as np
from flask import Flask, request, jsonify, render_template
import model

# Create flask app
flask_app = Flask(__name__)
#model = pickle.load(open("model.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/group", methods = ["POST"])
def predict():
    team_no = 3
    content=request.get_json()
    prediction = model.group_users(content["candidates"],content["team_no"])
    return render_template("index.html", formed_team = "The team formed is {}".format(prediction))

if __name__ == "__main__":
    flask_app.run(debug=True)