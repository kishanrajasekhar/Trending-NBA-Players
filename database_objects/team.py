from mongoengine import Document, StringField, ListField, DateTimeField


class Team(Document):
    """A database document representing an NBA team"""
    name = StringField(required=True, unique_with='location')
    location = StringField(required=True)
    owners = ListField(StringField(), null=True)
    owner_years = ListField(ListField(DateTimeField), null=True)
    coaches = ListField(StringField(), null=True)
    coaches_years = ListField(ListField(DateTimeField), null=True)
    year_founded = DateTimeField()
    abbreviation = StringField()
    conference = StringField()
