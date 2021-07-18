from mongoengine import Document, ReferenceField, BooleanField, IntField, DateTimeField, FloatField
from database_objects.player import Player
from database_objects.team import Team
from flask import url_for
import json


# LEARNING NOTE: MongoDB allows for a flexible schema. I can add/edit/remove fields any time I want here, in Python,
# without messing with the database.
# It's been a while since I've used SQL, but the internet it's more rigid. It seems that changing a schema in SQL is
# more troublesome. I'll have to look at SQL to see if that's the case.
class PlayerStats(Document):
    """A database document of the stats of a player during a game

    Indexes:
    player + game_date - this index is formed automatically because a player's stats and the game date are unique (a
                         player's stats is unique each game). This index is also useful because I can quickly search
                         the stats of a certain player using the id of the player database object.
    game_date - I have this index because I want to quickly lookup all statistics in any date range I choose (e.g.
                January 1st 2020 to March 11th 2020)
    """
    player = ReferenceField(Player, required=True, unique_with='game_date')
    game_date = DateTimeField(required=True)
    team = ReferenceField(Team, required=True)
    opponent = ReferenceField(Team, required=True)
    victory = BooleanField()
    is_home_game = BooleanField()
    minutes_played = IntField()
    two_pointers_made = IntField(required=True)
    two_pointers_attempted = IntField()
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
    meta = {
        'indexes': [
            {
                'fields': ['game_date']
            }
        ]
    }

    def to_json(self):
        response = json.loads(super().to_json())
        response['self'] = url_for("stats.get_stats", object_id=self.id)
        response['id'] = response['_id']['$oid']
        response['player'] = {
            "self": url_for("players.get_player", object_id=self.player.id),
            "first_name": self.player.first_name,
            "last_name": self.player.last_name
        }
        del response['_id']
        return json.dumps(response)


"""
Learning Note (for the future):

I made PlayerStats a separate collection from the Player collection. That's fine and all, but in order to fully take
advantage of Mongo's document database, I should have made PlayerStats an embedded document and add an attribute 'stats'
to Player which would be a list of PlayerStats. That way, each Player document already contains its list of stats. I 
wouldn't have to to a $lookup to get a stats for a player. That's truly taking advantage of MongoDB's document database.

The design I have now, where PlayerStats has a reference to Player is known as the normalized data model. Relational 
databases use this model, where a row in a table have references to a row of another table. The Mongo preferred approach
of having embedded documents in a single document is known as the embedded data model (a.k.a. denormalized data model).

Mongo allows you to use both designs. There are certain scenarios where one design is better than the other. 
More information: https://docs.mongodb.com/manual/core/data-model-design

Furthermore, the advantage of the embedded data modal is that all you information is in one document. So if you're 
updating that document, you can do an atomic update to any of the fields. You don't have to worry about creating 
transactions for multi-collection documents. Luckily, I don't have to worry about updates for this project.
More information: https://docs.mongodb.com/manual/tutorial/model-data-for-atomic-operations/

-----------------

If Player did have a list of PlayerStats, here is how the Mongo aggregation pipeline would look like for getting the
cumulative fantasy points for a certain data range.

For example, let's say I want the cumulative fantasy points for each player from January 22, 2021 to January 26, 2021 
(inclusive).

Notes:
 - the first stage filters out the list of stats that are not in the specified date range. Hence, the $filter command.
 - the second stage sums up the fantasy points from all the remaining stats in the list
 - the third stage again filter out any players who did not get any fantasy points in the specified date range.

[
    {
        '$addFields': {
            'stats': {
                '$filter': {
                    'input': '$stats', 
                    'as': 'stat', 
                    'cond': {
                        '$and': [
                            {
                                '$gte': [
                                    '$$stat.game_date', 
                                    datetime(2021, 1, 22, 0, 0, 0, tzinfo=timezone.utc).strftime('%a %b %d %Y %H:%M:%S %Z')
                                ]
                            }, {
                                '$lte': [
                                    '$$stat.game_date', 
                                    datetime(2021, 1, 26, 0, 0, 0, tzinfo=timezone.utc).strftime('%a %b %d %Y %H:%M:%S %Z')
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            'total_fantasy_points': {
                '$sum': '$stats.fantasy_points'
            }, 
            'num_games': {
                '$size': '$stats'
            }
        }
    }, {
        '$match': {
            'total_fantasy_points': {
                '$gt': 0
            }
        }
    }
]

Of course, if you want to query on specific players, just add a $match stage at the beginning of the pipeline and query 
on first_name and/or last_name.
"""