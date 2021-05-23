from mongoengine import Document, StringField, DateTimeField, ListField
from flask import url_for
import json


class Player(Document):
    """A database document representing an NBA player

    Indexes:
    first_name + last_name - this index is formed automatically because the first name is unique with the last name.
                             Also, this index is useful because I want to quickly search players by their name.
    """
    first_name = StringField(required=True, unique_with='last_name')
    last_name = StringField(required=True)
    year_joined = DateTimeField()
    rookie_of_year_dates = ListField(DateTimeField(), null=True)
    mvp_year_dates = ListField(DateTimeField(), null=True)
    sixth_man_year_dates = ListField(DateTimeField(), null=True)

    def to_json(self):
        response = json.loads(super().to_json())
        response['self'] = url_for("players.get_player", object_id=self.id)
        response['id'] = response['_id']['$oid']
        del response['_id']
        return json.dumps(response)
