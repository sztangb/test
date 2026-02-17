import unittest

from qmt_strategy.models import StrategyConfig
from qmt_strategy.pipeline import select_candidates


class PipelineTests(unittest.TestCase):
    def _sample_data(self):
        auction_rows = [
            {"code": "AAA", "open": 10.3, "auction_amt": 3_000_000, "avg_auction_amt_n": 1_000_000, "auction_vol": 300_000, "avg_auction_vol_n": 100_000},
            {"code": "BBB", "open": 21.0, "auction_amt": 800_000, "avg_auction_amt_n": 1_000_000, "auction_vol": 50_000, "avg_auction_vol_n": 100_000},
            {"code": "CCC", "open": 15.4, "auction_amt": 2_500_000, "avg_auction_amt_n": 1_000_000, "auction_vol": 200_000, "avg_auction_vol_n": 100_000},
        ]
        prev_day_rows = {
            "AAA": {"prev_close": 10.0, "close": 10.0, "low": 9.6, "high": 10.2, "volume": 12_000_000, "avg_volume_n": 8_000_000, "amount": 500_000_000, "is_st": False, "is_new": False},
            "BBB": {"prev_close": 20.0, "close": 19.8, "low": 19.5, "high": 20.5, "volume": 6_000_000, "avg_volume_n": 8_000_000, "amount": 500_000_000, "is_st": False, "is_new": False},
            "CCC": {"prev_close": 15.0, "close": 14.7, "low": 14.5, "high": 15.2, "volume": 9_000_000, "avg_volume_n": 8_000_000, "amount": 250_000_000, "is_st": False, "is_new": False},
        }
        sector_strength = {"AAA": 0.9, "BBB": 0.2, "CCC": 0.8}
        history_rows = {
            "AAA": {"ma5": 10.5, "ma10": 10.2, "ma20": 10.0, "close": 10.3},
            "BBB": {"ma5": 20.1, "ma10": 20.2, "ma20": 20.3, "close": 20.0},
            "CCC": {"ma5": 15.2, "ma10": 15.1, "ma20": 15.0, "close": 15.1},
        }
        fundamental_flags = {"AAA": 0, "BBB": 1, "CCC": 0}
        return auction_rows, prev_day_rows, sector_strength, history_rows, fundamental_flags

    def test_candidate_selection_filters_and_ranking(self):
        data = self._sample_data()
        config = StrategyConfig(top_n=2)

        cands = select_candidates(*data, config=config)

        self.assertEqual([c["code"] for c in cands], ["AAA"])
        self.assertIn("score", cands[0])

    def test_open_ret_filter(self):
        auction_rows, prev_day_rows, sector_strength, history_rows, fundamental_flags = self._sample_data()
        # force AAA out of open return range
        auction_rows[0]["open"] = 10.8

        cands = select_candidates(
            auction_rows,
            prev_day_rows,
            sector_strength,
            history_rows,
            fundamental_flags,
            config=StrategyConfig(top_n=2),
        )

        self.assertEqual(cands, [])


if __name__ == "__main__":
    unittest.main()
