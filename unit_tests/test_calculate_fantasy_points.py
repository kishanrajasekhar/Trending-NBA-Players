import unittest

from nba_database_populator import calculate_fantasy_points


class TestMatchesESPNData(unittest.TestCase):

    def test2019To2020Season(self):
        # test Hassan Whiteside stats on March 10th (double double)
        self.assertEqual(49, calculate_fantasy_points(16, 0, 14, 1, 1, 2, 1))
        # test Luka Doncic stats on March 10th and March 11th
        self.assertEqual(65.75, calculate_fantasy_points(38, 6, 7, 8, 2, 0, 5))
        self.assertEqual(55, calculate_fantasy_points(28, 2, 6, 9, 2, 0, 2))
        # test Trae Young stats on March 11th
        self.assertEqual(67, calculate_fantasy_points(42, 6, 2, 11, 0, 0, 6))
