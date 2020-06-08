from database_objects.team import Team
from mongoengine import NotUniqueError
import json
import os


def populate_nba_teams():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'nba_teams.json')
    with open(my_file) as data_file:
        nba_teams = json.load(data_file)
        for conference in nba_teams.keys():
            for team in nba_teams[conference]:
                name = team["name"]
                location = team["location"]
                abbreviation = team["abbreviation"]
                team_obj = Team(name=name, location=location, conference=conference, abbreviation=abbreviation)
                try:
                    team_obj.save()
                    print("Saved {} {} to the database".format(location, name))
                except NotUniqueError:
                    print("{} {} has already been saved to the database. Updating information".format(location, name))
                    Team.objects.get(name=name, location=location).update(conference=conference,
                                                                          abbreviation=abbreviation)
