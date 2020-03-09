from mongoengine import Document, StringField, DateTimeField, ListField


class Player(Document):
    name = StringField(required=True)
    year_joined = DateTimeField()
    rookie_of_year_dates = ListField(DateTimeField(), null=True)
    mvp_year_dates = ListField(DateTimeField(), null=True)
    sixth_man_year_dates = ListField(DateTimeField(), null=True)
