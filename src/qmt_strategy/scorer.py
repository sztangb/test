from __future__ import annotations

from statistics import mean, pstdev
from typing import Dict, List

from .models import StrategyConfig

SCORE_KEYS = [
    "open_ret",
    "auction_amt_ratio",
    "auction_vol_ratio",
    "prev_day_close_pos",
    "prev_day_vol_ratio",
    "sector_strength",
    "trend_score",
]


def _zscore_map(rows: List[Dict], key: str) -> Dict[str, float]:
    values = [r[key] for r in rows]
    mu = mean(values)
    sigma = pstdev(values)
    if sigma == 0:
        return {r["code"]: 0.0 for r in rows}
    return {r["code"]: (r[key] - mu) / sigma for r in rows}


def add_scores(rows: List[Dict], config: StrategyConfig) -> List[Dict]:
    if not rows:
        return []

    zmaps = {key: _zscore_map(rows, key) for key in SCORE_KEYS}

    for row in rows:
        code = row["code"]
        row["score"] = (
            config.w_open_ret * zmaps["open_ret"][code]
            + config.w_auction_amt_ratio * zmaps["auction_amt_ratio"][code]
            + config.w_auction_vol_ratio * zmaps["auction_vol_ratio"][code]
            + config.w_prev_day_close_pos * zmaps["prev_day_close_pos"][code]
            + config.w_prev_day_vol_ratio * zmaps["prev_day_vol_ratio"][code]
            + config.w_sector_strength * zmaps["sector_strength"][code]
            + config.w_trend_score * zmaps["trend_score"][code]
        )

    return rows
