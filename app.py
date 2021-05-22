from mongoengine import connect
from flask import Flask
from REST_endpoints import players

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>NBA endpoint</p>"


if __name__ == "__main__":
    app.register_blueprint(players.bp)
    connect('nba', host="mongo")
    app.run(host='0.0.0.0', port=5000, debug=True)
