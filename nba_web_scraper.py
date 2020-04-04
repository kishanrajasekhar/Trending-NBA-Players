# This script is responsible for scraping nba reference for nba player stats

from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse
from datetime import date, timedelta
# This url shows to top 100 players of yesterday's basketball games
# To show a specific date, append these query parameter to the url
# (e.g January 24, 2020: ?month=01&day=24&year=2020&type=all)
NBA_REFERENCE_URL = "https://www.basketball-reference.com/friv/dailyleaders.fcgi"
# players producing less fantasy points under this limit will not be shown in the list, unless a different
# fantasy points limit is specified as an argument (--ftpts_limit)
DEFAULT_FTPTS_LIMIT = 25

# basket ball reference table column titles
THREE_POINT_COL_TITLE = "3P"
POINTS_COL_TITLE = "PTS"
TOTAL_REBOUNDS_COL_TITLE = "TRB"
ASSISTS_COL_TITLE = "AST"
BLOCKS_COL_TITLE = "BLK"
STEALS_COL_TITLE = "STL"
TURN_OVERS_COL_TITLE = "TOV"

# basketball reference column indexes
PLAYER_NAME_COL = 0
PLAYER_TEAM_COL = 1
IS_AWAY_COL =  2
OPPONENT_COL = 3
IS_WIN_COL = 4
MINUTES_PLAYED_COL = 5
FIELD_GOALS_MADE_COL = 6
FIELD_GOALS_ATTEMPTED_COL = 7
THREE_POINTERS_MADE_COL = 9
THREE_POINTERS_ATTEMPTED_COL = 10
FREE_THROWS_MADE_COL = 12
FREE_THROWS_ATTEMPTED_COL = 13
OFFENSIVE_REBOUNDS_COL = 15
DEFENSIVE_REBOUNDS_COL = 16
ASSISTS_COL = 18
STEALS_COL = 19
BLOCKS_COL = 20
TURN_OVERS_COL = 21
PERSONAL_FOULS_COL = 22
POINTS_COL = 23
PLUS_MINUS_COL = 24

# fantasy points for these categories
DOUBLE_DOUBLE = 6
TRIPLE_DOUBLE = 12
QUADRUPLE_DOUBLE = 400

# map table column titles to fantasy point values
fantasy_scores = {THREE_POINT_COL_TITLE: 1, POINTS_COL_TITLE: 1, TOTAL_REBOUNDS_COL_TITLE: 1.25,
                  ASSISTS_COL_TITLE: 1.5, BLOCKS_COL_TITLE: 3, STEALS_COL_TITLE: 3, TURN_OVERS_COL_TITLE: -1}


def setup_parser() -> argparse.ArgumentParser:
    """Setup the parser to read the command line arguments

    :return: The parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help='year of date of the player stats to look up')
    parser.add_argument('--month', help='month (number from 1 to 12) of date of the player stats to look up')
    parser.add_argument('--day', help='day of date of the player stats to look up')
    parser.add_argument('--ftpts_limit', help='fantasy limit: don\'t include players who produce below the limit')
    return parser


def get_yesterday_year_month_day() -> [int, int, int]:
    """Return yesterday's year, month (a number from 1 to 12), and day (a number from 1 to 31). If a date isn't
    specified, yesterday's date will be used as the default.

    :return: [year, month, day]
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    return [yesterday.year, yesterday.month, yesterday.day]


def get_nba_reference_url(base_url, year, month, day) -> str:
    """Create the url for nba reference

    :param base_url: the url with the domain name (basketball-reference) and resource name (/friv/dailyleaders.fcgi)
           of the nba reference daily leader page
    :param year: the year parameter of the url. The value is the year number (e.g 2020)
    :param month: the month parameter of the url. The value is a number from 1 to 12
    :param day: the day parameter of the url. The value is a number from 1 to 31
    :return: The completed url
    """
    if year == 'None' and month == 'None' and day == 'None':
        # default url is used, which shows the stats of yesterday's games
        year, month, day = get_yesterday_year_month_day()
    elif year == 'None' or month == 'None' or day == 'None':
        print('Must specify entire date (year, month and day). Returning yesterday\'s stats')
        year, month, day = get_yesterday_year_month_day()
    else:
        # if the requested date is ahead of yesterday's date, use yesterday's date
        today = date.today()
        yesterday = today - timedelta(days=1)
        date_requested = date(year=int(year), month=int(month), day=int(day))
        if date_requested > yesterday:
            print("Date cannot be later than yesterday. Using yesterday's date")
            year, month, day = get_yesterday_year_month_day()

    return base_url + '?month={}&day={}&year={}'.format(month, day, year)


def get_basketball_reference_html_table(url) -> 'beautiful soup table':
    """Use beautiful soup to parse the html table on the basketball reference daily leaders page.

    :param url: the url of the basketball reference daily leader page
    :return: parsed html table
    """
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.findAll('tr')
    return table


if __name__ == '__main__':
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
    for player in player_stats:
        if player == []:
            continue
        name = player[0]

        ftpts = 0
        num_10s = 0  # keep track of double-doubles and triple-doubles

        pts = int(player[score_indices[POINTS_COL_TITLE]])
        ftpts += pts * fantasy_scores[POINTS_COL_TITLE]
        num_10s = num_10s+1 if pts >= 10 else num_10s

        rbs = int(player[score_indices[TOTAL_REBOUNDS_COL_TITLE]])
        ftpts += rbs * fantasy_scores[TOTAL_REBOUNDS_COL_TITLE]
        num_10s = num_10s+1 if rbs >= 10 else num_10s

        ast = int(player[score_indices[ASSISTS_COL_TITLE]])
        ftpts += ast * fantasy_scores[ASSISTS_COL_TITLE]
        num_10s = num_10s+1 if ast >= 10 else num_10s

        threes = int(player[score_indices[THREE_POINT_COL_TITLE]])
        ftpts += threes * fantasy_scores[THREE_POINT_COL_TITLE]
        # threes not counted for double double

        blk = int(player[score_indices[BLOCKS_COL_TITLE]])
        ftpts += blk * fantasy_scores[BLOCKS_COL_TITLE]
        num_10s = num_10s+1 if blk >= 10 else num_10s

        stl = int(player[score_indices[STEALS_COL_TITLE]])
        ftpts += stl * fantasy_scores[STEALS_COL_TITLE]
        num_10s = num_10s+1 if stl >= 10 else num_10s

        tov = int(player[score_indices[TURN_OVERS_COL_TITLE]])
        ftpts += tov * fantasy_scores[TURN_OVERS_COL_TITLE]
        # don't count turn overs for double double

        # double-double
        if num_10s >= 2:
            ftpts += DOUBLE_DOUBLE
        # triple-double
        if num_10s >= 3:
            ftpts += TRIPLE_DOUBLE
        # quadruple-double
        if num_10s >= 4:
            ftpts += QUADRUPLE_DOUBLE

    ##    print("{}:ftpts-{}, pts-{}, rb-{}, ast-{}, 3p-{}, blk-{}, stl-{}, tov-{}".format(
    ##        name, ftpts, pts, rbs, ast, threes, blk, stl, tov))

        # sort players based on ftpts
        player_ftpts.append((name, ftpts))

    player_ftpts.sort(key=lambda tup: tup[1], reverse=True)

    for player in player_ftpts:
        if player[1] < ftpts_limit:
            break
        print('{}: ftps - {}'.format(player[0], player[1]))
