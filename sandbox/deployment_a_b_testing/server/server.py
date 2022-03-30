import os

from flask import Flask

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def hello():
    return os.getenv("SERVER_NAME")


@app.route("/health")
def healthy():
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0")
