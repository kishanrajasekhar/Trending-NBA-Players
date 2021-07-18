from flask import Blueprint, request
from mongoengine.queryset.visitor import Q
from json_response import JsonResponse
from database_objects.player import Player
from database_objects.player_stats import PlayerStats
import json

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.route("/")
def get_players():
    player_stats = PlayerStats.objects()
    if request.args.get('players'):
        player_names = request.args.get('players').split(',')
        player_ids = []
        for name in player_names:
            if " " in name:
                name_parts = name.split(' ')
                first_name = name_parts[0]
                last_name = name_parts[1]
                players = Player.objects(first_name__icontains=first_name, last_name__icontains=last_name)
            else:
                players = Player.objects(Q(first_name__icontains=name) | Q(last_name__icontains=name))
            player_ids.extend([player.id for player in players])

        player_stats = player_stats(player__in=player_ids)

    player_stats = player_stats[:100]  # limit number of results to at most 100 for now
    stats_json = [json.loads(stats.to_json()) for stats in player_stats]
    return JsonResponse(json.dumps(stats_json))


@bp.route("<object_id>", methods=['GET'])
def get_stats(object_id):
    stats = PlayerStats.objects(id=object_id).get()
    return JsonResponse(stats.to_json())
