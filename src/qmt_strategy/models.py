from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:
    """Configuration for auction strong-stock selection."""

    top_n: int = 10
    min_open_ret: float = 0.015
    max_open_ret: float = 0.06
    min_prev_amount: float = 3e8

    w_open_ret: float = 0.18
    w_auction_amt_ratio: float = 0.24
    w_auction_vol_ratio: float = 0.20
    w_prev_day_close_pos: float = 0.13
    w_prev_day_vol_ratio: float = 0.10
    w_sector_strength: float = 0.08
    w_trend_score: float = 0.07
