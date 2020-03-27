from flask import render_template, Blueprint, redirect, jsonify
import os
import json

route = Blueprint("route", __name__)


def read_data_file():
    path = os.path.join(os.path.abspath('.'), 'result.json')
    with open(path, 'r') as file:
        data = file.read()
    return json.loads(data)


@route.route("/hello")
def say_hello():
    return jsonify(hello="hi")


@route.route("/")
def get_9ja_data():
    data = read_data_file()
    return render_template('view/home.html', data=data)


@route.route("/json")
def return_9ja_json_data():
    data = read_data_file()
    return jsonify(data=data)

