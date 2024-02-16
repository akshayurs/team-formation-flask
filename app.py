import numpy as np
from flask import Flask, request, jsonify, render_template
import model
from flask import jsonify
from flask_cors import CORS, cross_origin

# Create flask app
flask_app = Flask(__name__)
CORS(flask_app)
flask_app.config['CORS_HEADERS'] = 'application/json'


@flask_app.route("/", methods=['GET'])
@cross_origin(origins="*")
def Home():
    return render_template("index.html")


@flask_app.route("/group", methods=["POST"])
@cross_origin(origins="*")
def group():
    content = request.get_json()
    prediction = model.group_users(
        content["candidates"], content["team_no"], content['params'])
    return jsonify({"success": True, "data": prediction})


@flask_app.route("/team", methods=["POST"])
@cross_origin(origins="*")
def team():
    content = request.get_json()
    prediction = model.recommend_candidates(
        content["candidates"], content["role"])
    return jsonify({"success": True, "data": prediction})


if __name__ == "__main__":
    flask_app.run(host='localhost', debug=True, port=8000)
