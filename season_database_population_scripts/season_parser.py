import argparse


def setup_season_parser() -> argparse.ArgumentParser:
    """Setup the parser to read the command line arguments for the seasonal database population scripts. The seasonal
    script only needs user input for the fantasy point limit an the update flag (if running the script again, the
    update flag determines whether to update existing documents or just add new documents)

    :return: The parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ftpts_limit', help='fantasy limit: don\'t include players who produce below the limit')
    parser.add_argument('--update', help='whether or not to update the player_stats documents in the database')
    return parser
