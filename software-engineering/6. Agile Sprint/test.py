from health_data import *
import unittest

class TestHealthData(unittest.TestCase):

    def setUp(self):
        # Fake last 7 days data
        self.sample_data = [
            {'steps': 8000, 'calories': 2000, 'sleep_hours': 7.5},
            {'steps': 9000, 'calories': 2200, 'sleep_hours': 8.0},
            {'steps': 7000, 'calories': 1800, 'sleep_hours': 6.5},
            {'steps': 7500, 'calories': 2100, 'sleep_hours': 7.0},
        ]

    def test_calculate_stats_steps(self):
        stats = calculate_stats(self.sample_data, 'steps')
        self.assertEqual(stats['average'], 7875.0)
        self.assertEqual(stats['max'], 9000)
        self.assertEqual(stats['min'], 7000)

    def test_calculate_stats_calories(self):
        stats = calculate_stats(self.sample_data, 'calories')
        self.assertEqual(stats['average'], 2025.0)
        self.assertEqual(stats['max'], 2200)
        self.assertEqual(stats['min'], 1800)

    def test_calculate_stats_sleep(self):
        stats = calculate_stats(self.sample_data, 'sleep_hours')
        self.assertEqual(stats['average'], 7.25)
        self.assertEqual(stats['max'], 8.0)
        self.assertEqual(stats['min'], 6.5)

    def test_calculate_stats_empty(self):
        stats = calculate_stats([], 'steps')
        self.assertEqual(stats, "No data")

if __name__ == 'main':
    unittest.main()