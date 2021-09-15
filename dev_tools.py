from nba_database_populator import populate_player_stats, populate_nba_teams, NBA_REFERENCE_URL,\
    DEFAULT_FTPTS_LIMIT
from season_database_population_scripts.season_parser import setup_season_parser
from mongoengine import connect
import datetime


def database_populator(start_date, end_date):
    print('season start:', start_date)
    print('season temporary end:', end_date)
    url = NBA_REFERENCE_URL
    args = setup_season_parser().parse_args()
    ftpts_limit = f'{args.ftpts_limit}'
    ftpts_limit = DEFAULT_FTPTS_LIMIT if ftpts_limit == 'None' else int(ftpts_limit)
    update = f'{args.update}'
    update = True if update == 'True' else False
    print('ftpts_limit is', ftpts_limit)
    print('update is', update)
    print()

    connect('nba', host='mongo')
    populate_nba_teams()
    print()
    data_date = start_date
    while data_date <= end_date:
        print(data_date.year, data_date.month, data_date.day)
        populate_player_stats(url, data_date.year, data_date.month, data_date.day, ftpts_limit, update)
        data_date = data_date + datetime.timedelta(days=1)
        print()