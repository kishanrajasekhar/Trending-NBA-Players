import unittest
from nba_database_populator import calculate_fantasy_points
from nba_query_stats import query_nba_stats
from mongoengine import connect, disconnect
from database_objects.team import Team
from database_objects.player import Player
from database_objects.player_stats import PlayerStats
from datetime import date


class TestMatchesESPNData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test2019To2020Season(self):
        # test Hassan Whiteside stats on March 10th (double double)
        self.assertEqual(49, calculate_fantasy_points(16, 0, 14, 1, 1, 2, 1))
        # test Luka Dončić stats on March 10th and March 11th
        self.assertEqual(65.75, calculate_fantasy_points(38, 6, 7, 8, 2, 0, 5))
        self.assertEqual(55, calculate_fantasy_points(28, 2, 6, 9, 2, 0, 2))
        # test Trae Young stats on March 11th
        self.assertEqual(67, calculate_fantasy_points(42, 6, 2, 11, 0, 0, 6))

    def test_query_player_cumulative_stats(self):
        """Test the 'query_nba_stats' method in 'nba_query_stats.py'. This method accumulates the stats over a period
        of time and returns the total fantasy points for each player."""
        # create a team
        team = Team(name="whateva", location="whateva")
        team.save()
        # create a player object for Hassan Whiteside
        hassan = Player(first_name="Hassan", last_name="Whiteside")
        hassan.save()
        # make a player stats object for March 6th, March 7th and March 10th
        hassan_march_6_stats = PlayerStats(player=hassan, game_date=date(year=2020, month=3, day=6), team=team,
                                           opponent=team, two_pointers_made=10, three_pointers_made=1,
                                           free_throws_made=0, offensive_rebounds=5, defensive_rebounds=15, assists=1,
                                           steals=0, blocks=4, turnovers=3, personal_fouls=1, fantasy_points=65.5)
        hassan_march_6_stats.save()
        hassan_march_7_ftpts = PlayerStats(player=hassan, game_date=date(year=2020, month=3, day=7), team=team,
                                           opponent=team, two_pointers_made=8, three_pointers_made=0,
                                           free_throws_made=3, offensive_rebounds=2, defensive_rebounds=9, assists=0,
                                           steals=0, blocks=3, turnovers=4, personal_fouls=1, fantasy_points=43.75)
        hassan_march_7_ftpts.save()
        hassan_march_10_ftpts = PlayerStats(player=hassan, game_date=date(year=2020, month=3, day=10), team=team,
                                            opponent=team, two_pointers_made=8, three_pointers_made=0,
                                            free_throws_made=0, offensive_rebounds=5, defensive_rebounds=9, assists=1,
                                            steals=1, blocks=2, turnovers=1, personal_fouls=1, fantasy_points=49)
        hassan_march_10_ftpts.save()

        total_hassan_ftpts = 65.5 + 43.75 + 49
        march_6_to_11_stats = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=11))
        self.assertEqual([{'fantasy_points': total_hassan_ftpts, 'name': 'Hassan Whiteside'}], march_6_to_11_stats)
        march_6_to_9_stats = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=9))
        self.assertEqual([{'fantasy_points': total_hassan_ftpts-49, 'name': 'Hassan Whiteside'}], march_6_to_9_stats)

        # Create a player object for Luka Dončić
        luka = Player(first_name="Luka", last_name="Dončić")
        luka.save()
        # make player stats objects for March 6th, 8th, 10th and 11th
        luka_march_6_stats = PlayerStats(player=luka, game_date=date(year=2020, month=3, day=6), team=team,
                                           opponent=team, two_pointers_made=5, three_pointers_made=2,
                                           free_throws_made=5, offensive_rebounds=0, defensive_rebounds=4, assists=6,
                                           steals=2, blocks=0, turnovers=1, personal_fouls=1, fantasy_points=42)
        luka_march_6_stats.save()
        luka_march_8_stats = PlayerStats(player=luka, game_date=date(year=2020, month=3, day=8), team=team,
                                         opponent=team, two_pointers_made=9, three_pointers_made=4,
                                         free_throws_made=6, offensive_rebounds=1, defensive_rebounds=9, assists=8,
                                         steals=2, blocks=0, turnovers=3, personal_fouls=3, fantasy_points=73.5)
        luka_march_8_stats.save()
        luka_march_10_stats = PlayerStats(player=luka, game_date=date(year=2020, month=3, day=10), team=team,
                                         opponent=team, two_pointers_made=7, three_pointers_made=6,
                                         free_throws_made=6, offensive_rebounds=1, defensive_rebounds=6, assists=8,
                                         steals=2, blocks=0, turnovers=5, personal_fouls=3, fantasy_points=65.75)
        luka_march_10_stats.save()
        luka_march_11_stats = PlayerStats(player=luka, game_date=date(year=2020, month=3, day=11), team=team,
                                          opponent=team, two_pointers_made=8, three_pointers_made=2,
                                          free_throws_made=6, offensive_rebounds=1, defensive_rebounds=5, assists=9,
                                          steals=2, blocks=0, turnovers=2, personal_fouls=2, fantasy_points=55)
        luka_march_11_stats.save()

        total_luka_ftpts = 42 + 73.5 + 65.75 + 55
        march_6_to_11_stats = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=11))
        expected = [
            {"fantasy_points": total_luka_ftpts, "name": "Luka Dončić"},
            {"fantasy_points": total_hassan_ftpts, "name": "Hassan Whiteside"}
        ]
        self.assertEqual(expected, march_6_to_11_stats)
        march_6_to_10_stats = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=10))
        expected = [
            {"fantasy_points": total_luka_ftpts-55, "name": "Luka Dončić"},
            {"fantasy_points": total_hassan_ftpts, "name": "Hassan Whiteside"}
        ]
        self.assertEqual(expected, march_6_to_10_stats)
        # test up to march 7th. Hassan has 2 games, Luka only has 1. Hassan will have more ftpts, so he will show up
        # first
        march_6_to_7_stats = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=7))
        expected = [
            {"fantasy_points": 65.5+43.75, "name": "Hassan Whiteside"},
            {"fantasy_points": 42, "name": "Luka Dončić"}
        ]
        self.assertEqual(expected, march_6_to_7_stats)

        # test with specific player name
        march_6_to_7_stats_luka_only = query_nba_stats(date(year=2020, month=3, day=6), date(year=2020, month=3, day=7),
                                                       players=["Luka Dončić"])
        expected = [
            {"fantasy_points": 42, "name": "Luka Dončić"}
        ]
        self.assertEqual(expected, march_6_to_7_stats_luka_only)
