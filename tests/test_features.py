import unittest

from qmt_strategy.features import calc_close_position, calc_open_ret, calc_trend_score


class FeatureTests(unittest.TestCase):
    def test_calc_open_ret(self):
        self.assertAlmostEqual(calc_open_ret(10.6, 10.0), 0.06)

    def test_close_position(self):
        self.assertAlmostEqual(calc_close_position(10.0, 9.0, 11.0), 0.5)

    def test_trend_score(self):
        score = calc_trend_score({"ma5": 11, "ma10": 10, "ma20": 9, "close": 10})
        self.assertAlmostEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
