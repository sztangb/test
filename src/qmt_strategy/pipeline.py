from __future__ import annotations

from typing import Dict, List

from .features import build_feature_rows
from .filters import apply_filters
from .models import StrategyConfig
from .scorer import add_scores


def select_candidates(
    auction_rows: List[Dict],
    prev_day_rows: Dict[str, Dict],
    sector_strength: Dict[str, float],
    history_rows: Dict[str, Dict],
    fundamental_risk_flags: Dict[str, int],
    config: StrategyConfig | None = None,
) -> List[Dict]:
    config = config or StrategyConfig()

    rows = build_feature_rows(
        auction_rows=auction_rows,
        prev_day_rows=prev_day_rows,
        sector_strength=sector_strength,
        history_rows=history_rows,
        fundamental_risk_flags=fundamental_risk_flags,
    )
    rows = apply_filters(rows, config)
    rows = add_scores(rows, config)
    rows.sort(key=lambda r: r["score"], reverse=True)

    return rows[: config.top_n]
