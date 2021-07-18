from mongoengine import connect
from flask import Flask, render_template
from REST_endpoints import players, stats
from database_objects.player import Player

app = Flask(__name__)


@app.route("/")
def hello_world():
    some_players = Player.objects[:10]
    player_names = [f'{p.first_name} {p.last_name}' for p in some_players]
    return render_template("test_template.html",
                           player_names=player_names)


if __name__ == "__main__":
    app.register_blueprint(players.bp)
    app.register_blueprint(stats.bp)
    connect('nba', host="mongo")
    app.run(host='0.0.0.0', port=5000, debug=True)
