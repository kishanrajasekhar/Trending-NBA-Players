from database_objects.team import Team
from mongoengine import NotUniqueError
import json


def populate_nba_teams():
    with open("init_scripts/nba_teams.json") as data_file:
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
