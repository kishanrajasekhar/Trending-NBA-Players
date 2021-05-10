from nba_database_populator import get_date_object, populate_player_stats, populate_nba_teams, NBA_REFERENCE_URL,\
    DEFAULT_FTPTS_LIMIT
from season_database_population_scripts.season_parser import setup_season_parser
from mongoengine import connect
import datetime


def season_populator(start_date, end_date):
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

    connect('nba')
    populate_nba_teams()
    print()
    data_date = start_date
    while data_date <= end_date:
        print(data_date.year, data_date.month, data_date.day)
        populate_player_stats(url, data_date.year, data_date.month, data_date.day, ftpts_limit, update)
        data_date = data_date + datetime.timedelta(days=1)
        print()


if __name__ == '__main__':
    season_start = get_date_object(2019, 10, 22)
    # temporary end at March 11th because of Covid 19
    # I don't know if the season will resume.
    season_temporary_end = get_date_object(2020, 3, 11)

    season_populator(season_start, season_temporary_end)
