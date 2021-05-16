# This is just a test file to get Docker up and running.
# I'm using docker to get the flask service running.
# This geeksforgeeks article helped me out: https://www.geeksforgeeks.org/dockerize-your-flask-app/

from mongoengine import connect
from flask import Flask, Response
from database_objects.player import Player
import json

app = Flask(__name__)


class JsonResponse(Response):
    default_mimetype = "application/json"


@app.route("/")
def hello_world():
    return "<p>NBA endpoint</p>"


@app.route("/playa")
def playa():
    return "<p>You a playa!</p>"


@app.route("/players")
def players():
    player_objs = Player.objects()
    players_json = [json.loads(player.to_json()) for player in player_objs]
    return JsonResponse(json.dumps(players_json))


if __name__ == "__main__":
    connect('nba', host="mongo")
    app.run(host='0.0.0.0', port=5000, debug=True)
