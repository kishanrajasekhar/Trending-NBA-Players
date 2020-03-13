from mongoengine import Document, StringField, DateTimeField, ListField


class Player(Document):
    first_name = StringField(required=True, unique_with='last_name')
    last_name = StringField(required=True)
    year_joined = DateTimeField()
    rookie_of_year_dates = ListField(DateTimeField(), null=True)
    mvp_year_dates = ListField(DateTimeField(), null=True)
    sixth_man_year_dates = ListField(DateTimeField(), null=True)
