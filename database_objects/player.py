from mongoengine import Document, StringField, DateTimeField, ListField


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
