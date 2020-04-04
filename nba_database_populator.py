# This script is responsible for populating the database with nba player stats

from mongoengine import connect, DoesNotExist
from init_scripts.populate_data import populate_nba_teams
from nba_web_scraper import *
from database_objects.player import Player
from database_objects.team import Team
from database_objects.player_stats import PlayerStats

THREE_POINTERS_FANTASY = 1  # 1 extra point per three pointer made
REBOUNDS_FANTASY = 1.25
ASSISTS_FANTASY = 1.5
STEALS_FANTASY = 3
BLOCKS_FANTASY = 3
TURN_OVERS_FANTASY = -1
EJECTIONS_FANTASY = -5  # downside - basketball reference doesn't give me this data
DOUBLE_DOUBLE_FANTASY = 6
TRIPLE_DOUBLE_FANTASY = 12
QUADRUPLE_DOUBLE_FANTASY = 400


def calculate_fantasy_points(two_points_made, three_points_made, free_throws_made, total_rebounds, assists, steals,
                             blocks, turnovers) -> float:
    """Calculate the number of fantasy points the player gets.

    :param two_points_made: number of 2-pointers made
    :param three_points_made: number of 3-pointers made
    :param free_throws_made: number of free throws made
    :param total_rebounds: number of rebounds
    :param assists: number of assists
    :param steals: number of steals
    :param blocks: number of blocks
    :param turnovers: number of turn overs
    :return: number of fantasy points
    """
    num_10s = 0

    fantasy_points = (two_points_made * 2) + free_throws_made + (three_points_made * 3)
    num_10s = num_10s+1 if fantasy_points >= 10 else num_10s

    fantasy_points += three_pointers_made * THREE_POINTERS_FANTASY

    fantasy_points += total_rebounds * REBOUNDS_FANTASY
    num_10s = num_10s+1 if total_rebounds >= 10 else num_10s

    fantasy_points += assists * ASSISTS_FANTASY
    num_10s = num_10s+1 if assists >= 10 else num_10s

    fantasy_points += steals * STEALS_FANTASY
    num_10s = num_10s+1 if steals >= 10 else num_10s

    fantasy_points += blocks * BLOCKS_FANTASY
    num_10s = num_10s+1 if blocks >= 10 else num_10s

    fantasy_points += turnovers * TURN_OVERS_FANTASY

    if num_10s >= 2:
        fantasy_points += DOUBLE_DOUBLE_FANTASY

    if num_10s >= 3:
        fantasy_points += TRIPLE_DOUBLE_FANTASY

    if num_10s >= 4:
        fantasy_points += QUADRUPLE_DOUBLE_FANTASY

    return fantasy_points


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
            player_db_obj = Player.objects.get(first_name=first_name, last_name=last_name)
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

        name = player_db_obj.first_name + ' ' + player_db_obj.last_name
        players_team_name = players_team_obj.location + ' ' + players_team_obj.name
        opponent_team_name = opponent_team_obj.location + ' ' + opponent_team_obj.name
        win_message = 'won' if is_win else 'lost'
        home_message = 'away' if is_away_game else 'at home'
        print(f"{name} of the {players_team_name} {win_message} against the {opponent_team_name} {home_message}")

        pts = int(player_data[POINTS_COL])
        field_goals_made = int(player_data[FIELD_GOALS_MADE_COL])
        field_goals_attempted = int(player_data[FIELD_GOALS_ATTEMPTED_COL])
        three_pointers_made = int(player_data[THREE_POINTERS_MADE_COL])
        three_pointers_attempted = int(player_data[THREE_POINTERS_ATTEMPTED_COL])
        # two point data is not provided by the table. However it still be calculated
        # TWO_POINTERS_MADE = FIELD_GOALS_MADE - THREE_POINTERS_MADE
        # TWO_POINTERS_ATTEMPTED = FIELD_GOALS_ATTEMPTED - THREE_POINTERS_ATTEMPTED
        two_pointers_made = field_goals_made - three_pointers_made
        two_pointers_attempted = field_goals_attempted - three_pointers_attempted
        free_throws_made = int(player_data[FREE_THROWS_MADE_COL])
        free_throws_attempted = int(player_data[FREE_THROWS_ATTEMPTED_COL])
        offensive_rebounds = int(player_data[OFFENSIVE_REBOUNDS_COL])
        defensive_rebounds = int(player_data[DEFENSIVE_REBOUNDS_COL])
        assists = int(player_data[ASSISTS_COL])
        steals = int(player_data[STEALS_COL])
        blocks = int(player_data[BLOCKS_COL])
        turnovers = int(player_data[TURN_OVERS_COL])
        personal_fouls = int(player_data[PERSONAL_FOULS_COL])
        plus_minus = float(player_data[PERSONAL_FOULS_COL])

        ftpts = calculate_fantasy_points(two_pointers_made, three_pointers_made, free_throws_made,
                                         offensive_rebounds+defensive_rebounds, assists, steals, blocks, turnovers)

        if ftpts < ftpts_limit:
            break

        print(f'\t2pts: {two_pointers_made}, 3pts: {three_pointers_made}, ft: {free_throws_made}, '
              f'orb: {offensive_rebounds}, drb: {defensive_rebounds} ast: {assists}, stl: {steals}, blk: {blocks}, '
              f'tov: {turnovers}, ftpts: {ftpts}')

        break
