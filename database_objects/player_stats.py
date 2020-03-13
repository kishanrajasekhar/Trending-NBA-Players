from mongoengine import Document, ReferenceField, BooleanField, IntField, DateTimeField, FloatField
from database_objects.player import Player
from database_objects.team import Team


class PlayerStats(Document):
    player = ReferenceField(Player, required=True, unique_with='game_date')
    game_date = DateTimeField(required=True)
    team = ReferenceField(Team, required=True)
    opponent = ReferenceField(Team, required=True)
    victory = BooleanField()
    is_home_game = BooleanField()
    minutes_played = IntField()
    field_goals_made = IntField(required=True)
    field_goals_attempted = IntField()
    three_pointers_made = IntField(required=True)
    three_pointers_attempted = IntField()
    free_throws_made = IntField(required=True)
    free_throws_attempted = IntField()
    offensive_rebounds = IntField(required=True)
    defensive_rebounds = IntField(required=True)
    assists = IntField(required=True)
    steals = IntField(required=True)
    blocks = IntField(required=True)
    turnovers = IntField(required=True)
    personal_fouls = IntField(required=True)
    plus_minus = FloatField()
    fantasy_points = FloatField(required=True)
    is_rookie = BooleanField()
