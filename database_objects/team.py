from mongoengine import Document, StringField, ListField, DateTimeField


class Team(Document):
    name = StringField(required=True, unique_with='location')
    location = StringField(required=True)
    owners = ListField(StringField())
    owner_years = ListField(ListField(DateTimeField))
    coaches = ListField(StringField())
    coaches_years = ListField(ListField(DateTimeField))
    year_founded = DateTimeField()
    abbreviation = StringField()
    conference = StringField()
