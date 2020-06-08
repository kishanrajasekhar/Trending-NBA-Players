import argparse
from datetime import date


def setup_query_parser() -> argparse.ArgumentParser:
    """Setup the parser to read the command line arguments for querying the database

    :return: The parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--year_start', help='year of start date of the player stats to look up')
    parser.add_argument('--month_start',
                        help='month (number from 1 to 12) of start date of the player stats to look up')
    parser.add_argument('--day_start', help='day of start date of the player stats to look up')
    parser.add_argument('--year_end', help='year of end date of the player stats to look up')
    parser.add_argument('--month_end',
                        help='month (number from 1 to 12) of end date of the player stats to look up')
    parser.add_argument('--day_end', help='day of end date of the player stats to look up')
    return parser


if __name__ == '__main__':
    args = setup_query_parser().parse_args()

    try:
        year_start = int(f'{args.year_start}')
        month_start = int(f'{args.month_start}')
        day_start = int(f'{args.day_start}')
        year_end = int(f'{args.year_end}')
        month_end = int(f'{args.month_end}')
        day_end = int(f'{args.day_end}')

        start_date = date(year=year_start, month=month_start, day=day_start)
        end_date = date(year_end, month=month_end, day=day_end)

        if start_date < end_date:
            print("Query stats!")
        else:
            print("Start date must be before end date.")
            print(f"You specified start date: {start_date} and end date: {end_date}")

    except ValueError:
        print("Must specify all parameters as integers: (--year_start, --month_start, --day_start,"
              "--year_end, --month_end, --day_end)")
