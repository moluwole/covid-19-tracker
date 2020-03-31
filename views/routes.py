from flask import render_template, Blueprint, redirect, jsonify
import os
import json
import boto3
import redis

route = Blueprint("route", __name__)
REDIS_URL = os.getenv("REDIS_URL", 'redis://127.0.0.1:6379')
Store = redis.Redis.from_url(REDIS_URL)


def read_data_file():
    data = Store.get('latest')
    if data is None:
        data = read_data_file_from_s3()
    return data


def read_data_file_from_s3():
    if os.getenv('FLASK_ENV') == 'production':
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )

            result_file = s3_client.get_object(Bucket='covid-19-nigeria-tracker', Key='result.json')
            return json.loads(result_file['Body'].read())
        except Exception as e:
            print(str(e))
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
