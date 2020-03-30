from flask import render_template, Blueprint, redirect, jsonify
import os
import json
import boto3

route = Blueprint("route", __name__)


def read_data_file():
    if os.getenv('FLASK_ENV') == 'production':
        s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )

        result_file = s3_client.get_object(Bucket='covid-19-nigeria-tracker', Key='result.json')
        return result_file
    else:
        path = os.path.join(os.path.abspath("."), "result.json")
        with open(path, "r") as file:
            data = file.read()
        return json.loads(data)


@route.route("/hello")
def say_hello():
    return jsonify(hello="hi")


@route.route("/")
def get_9ja_data():
    data = read_data_file()
    return render_template("view/home.html", data=data)


@route.route("/json")
def return_9ja_json_data():
    data = read_data_file()
    return jsonify(data=data)
