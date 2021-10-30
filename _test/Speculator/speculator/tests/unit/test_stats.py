from speculator.utils import stats
import unittest

class StatsTest(unittest.TestCase):
    def test_avg(self):
        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(stats.avg(nums), 0.39269)

        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(stats.avg(nums, count=8), 0.24543125)
