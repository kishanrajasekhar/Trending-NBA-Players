# This script is responsible for populating the database with nba player stats

from mongoengine import connect, DoesNotExist
from init_scripts.populate_data import populate_nba_teams
from nba_web_scraper import *
from database_objects.player import Player
from database_objects.team import Team


if __name__ == '__main__':
    connect('nba')
    populate_nba_teams()
    print()
    # parse nba reference
    url = NBA_REFERENCE_URL
    args=setup_parser().parse_args()

    year = f'{args.year}'
    month = f'{args.month}'
    day = f'{args.day}'
    ftpts_limit = f'{args.ftpts_limit}'
    ftpts_limit = DEFAULT_FTPTS_LIMIT if ftpts_limit == 'None' else int(ftpts_limit)

    url = get_nba_reference_url(url, year, month, day)
    print(url)

    table = get_basketball_reference_html_table(url)

    # column headers
    if len(table):
        headers = [th.getText() for th in table[0].findAll('th')]
    else:
        headers = []

    score_indices = {}
    for i in range(len(headers)):
        if headers[i] in fantasy_scores.keys():
            score_indices[headers[i]] = i - 1  # -1 since rank not included in player list

    rows = table[1:]

    if len(table):
        player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    else:
        player_stats = []

    player_ftpts = []

    # LEARNING NOTE: Unfortunately Mongodb doesn't support atomic batch CREATES and UPDATES, unlike SQL
    # MongoDB doesn't guarantee ACID, unlike SQL. I have to loop through the html table and add or update player
    # information in the database on at at time. If I accidently kill the script during the loop, it will be a
    # partial update. It's not all or nothing, like an atomic operation would be.
    for player_data in player_stats:
        if player_data == []:
            continue
        names = player_data[PLAYER_NAME_COL].split(' ')
        first_name = names[0]
        last_name = ' '.join(names[1:])

        # If a player hasn't appeared in the over 25 fantasy points list (or whatever the limit is) before, add him to
        # the database
        try:
            Player.objects.get(first_name=first_name, last_name=last_name)
        except DoesNotExist:
            player_db_obj = Player(first_name=first_name, last_name=last_name)
            player_db_obj.save()
            print(f"New Player! {first_name} {last_name} is saved to the database.")

        players_team = player_data[PLAYER_TEAM_COL]
        players_team_obj = Team.objects.get(abbreviation=players_team)
        is_away_game = player_data[IS_AWAY_COL] == '@'
        opponent_team = player_data[OPPONENT_COL]
        opponent_team_obj = Team.objects.get(abbreviation=opponent_team)
        is_win = player_data[IS_WIN_COL] == 'W'

        name = first_name + ' ' + last_name
        players_team_name = players_team_obj.location + ' ' + players_team_obj.name
        opponent_team_name = opponent_team_obj.location + ' ' + opponent_team_obj.name
        win_message = 'won' if is_win else 'lost'
        home_message = 'away' if is_away_game else 'at home'
        print(f"{name} of the {players_team_name} {win_message} against the {opponent_team_name} {home_message}")
