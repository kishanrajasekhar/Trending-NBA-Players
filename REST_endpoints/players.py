from flask import Blueprint
from json_response import JsonResponse
from database_objects.player import Player
import json

bp = Blueprint("players", __name__, url_prefix="/players")


@bp.route("/")
def get_players():
    player_objs = Player.objects()
    players_json = [json.loads(player.to_json()) for player in player_objs]
    return JsonResponse(json.dumps(players_json))


@bp.route("<object_id>", methods=['GET'])
def get_player(object_id):
    player = Player.objects(id=object_id).get()
    return JsonResponse(player.to_json())
