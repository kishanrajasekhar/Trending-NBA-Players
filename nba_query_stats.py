import argparse
from datetime import date
from database_objects.player_stats import PlayerStats
from database_objects.player import Player
from mongoengine import connect, DoesNotExist


def setup_query_parser() -> argparse.ArgumentParser:
    """Setup the parser to read the command line arguments for querying the database

    :return: The parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--year_start', help='year of start date of the player stats to look up', required=True,
                        type=int)
    parser.add_argument('--month_start',
                        help='month (number from 1 to 12) of start date of the player stats to look up', required=True,
                        type=int)
    parser.add_argument('--day_start', help='day of start date of the player stats to look up', required=True, type=int)
    parser.add_argument('--year_end', help='year of end date of the player stats to look up', required=True, type=int)
    parser.add_argument('--month_end',
                        help='month (number from 1 to 12) of end date of the player stats to look up', required=True,
                        type=int)
    parser.add_argument('--day_end', help='day of end date of the player stats to look up', required=True, type=int)
    parser.add_argument('--players', help='comma seperated list of player names (e.g. "Jamal Murray,Lebron James, etc"',
                        type=str)
    return parser


def query_nba_stats(start_date: date, end_date: date, players=None) -> []:
    """Query the nba stats of players from all the games starting from the specified start date to the end date
    (inclusive).

    :param start_date: start date of when to start accumulating the stats (type: datetime.datetime)
    :param end_date: end date of when to stop accumulating the stats (type: datetime.datetime)
    :param players: a list of player names. If specified, get the stats of these players.
    :return: list of dicts (format: [ {"name": "Nikola Jokić", "fantasy_points": 1784.5}, ... ])
    """
    player_stats = PlayerStats.objects(game_date__gte=start_date, game_date__lte=end_date)

    if players is not None:
        player_ids = []
        for p in players:
            try:
                first, last = p.split(" ")
                player_obj = Player.objects.get(first_name=first, last_name=last)
                player_ids.append(player_obj.id)
            except ValueError:
                print(f"Need so specify first and last name for {p}")
            except DoesNotExist:
                print(f"Player {p} does not exist")
        if len(player_ids):
            player_stats = player_stats(player__in=player_ids)

    pipeline = [
        {
            '$group': {
                '_id': '$player',
                'fantasy_points': {
                    '$sum': '$fantasy_points'
                }
            }
        }, {
            '$sort': {
                'fantasy_points': -1
            }
        }, {
            '$lookup': {
                'from': 'player',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'player'
            }
        }, {
            '$project': {
                '_id': 0,
                'fantasy_points': 1,
                'name': {
                    '$concat': [
                        {
                            '$arrayElemAt': [
                                '$player.first_name', 0
                            ]
                        }, ' ', {
                            '$arrayElemAt': [
                                '$player.last_name', 0
                            ]
                        }
                    ]
                }
            }
        }
    ]

    results = list(player_stats.aggregate(*pipeline))
    return results


if __name__ == '__main__':
    args = setup_query_parser().parse_args()

    try:
        year_start = int(f'{args.year_start}')
        month_start = int(f'{args.month_start}')
        day_start = int(f'{args.day_start}')
        year_end = int(f'{args.year_end}')
        month_end = int(f'{args.month_end}')
        day_end = int(f'{args.day_end}')

        players = f'{args.players}'
        if players is not None:
            players = players.split(",")
            players = [p.strip() for p in players]

        start_date = date(year=year_start, month=month_start, day=day_start)
        end_date = date(year_end, month=month_end, day=day_end)

        if start_date <= end_date:
            connect('nba')
            print()
            print(f"Collecting cumulative fantasy points for start date: {start_date} and end date: {end_date}")
            print()
            nba_data = query_nba_stats(start_date, end_date, players)
            for data in nba_data:
                print("Player:", data["name"]+",", "Fantasy Points:", data["fantasy_points"])
        else:
            print("End date cannot be after start date.")
            print(f"You specified start date: {start_date} and end date: {end_date}")

    except ValueError:
        print("Must specify all parameters as integers: (--year_start, --month_start, --day_start,"
              "--year_end, --month_end, --day_end)")
