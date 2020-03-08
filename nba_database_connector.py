from mongoengine import connect
from init_scripts.populate_data import populate_nba_teams


if __name__ == '__main__':
    connect('nba')
    print('success')
    populate_nba_teams()
