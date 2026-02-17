"""Minimal example for running the selection pipeline."""

from qmt_strategy import StrategyConfig, select_candidates


if __name__ == "__main__":
    auction_rows = [
        {"code": "000001.SZ", "open": 10.3, "auction_amt": 2_000_000, "avg_auction_amt_n": 1_000_000, "auction_vol": 100_000, "avg_auction_vol_n": 50_000},
    ]
    prev_day_rows = {
        "000001.SZ": {
            "prev_close": 10.0,
            "close": 10.0,
            "low": 9.8,
            "high": 10.1,
            "volume": 10_000_000,
            "avg_volume_n": 7_000_000,
            "amount": 500_000_000,
            "is_st": False,
            "is_new": False,
        }
    }
    sector_strength = {"000001.SZ": 0.7}
    history_rows = {"000001.SZ": {"ma5": 10.2, "ma10": 10.0, "ma20": 9.9, "close": 10.1}}
    fundamental_flags = {"000001.SZ": 0}

    candidates = select_candidates(
        auction_rows,
        prev_day_rows,
        sector_strength,
        history_rows,
        fundamental_flags,
        config=StrategyConfig(top_n=5),
    )
    print(candidates)
