from flask import jsonify


def index():
    return jsonify(
        result="In case of problems or doubts please visit the documentation available on github "
        "https://github.com/chomyczek/simple-geolocation-api"
    )
