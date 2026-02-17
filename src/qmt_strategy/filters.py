from __future__ import annotations

from typing import Dict, Iterable, List

from .models import StrategyConfig


def keep_row(row: Dict, config: StrategyConfig) -> bool:
    if row["fundamental_risk_flag"] == 1:
        return False
    if row["is_st"] or row["is_new"]:
        return False
    if row["prev_amount"] < config.min_prev_amount:
        return False
    if not (config.min_open_ret <= row["open_ret"] <= config.max_open_ret):
        return False
    return True


def apply_filters(rows: Iterable[Dict], config: StrategyConfig) -> List[Dict]:
    return [row for row in rows if keep_row(row, config)]
