from __future__ import annotations

from typing import Dict, List


def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    return a / b if b else default


def calc_open_ret(open_price: float, prev_close: float) -> float:
    return _safe_div(open_price, prev_close, 1.0) - 1.0


def calc_close_position(close: float, low: float, high: float) -> float:
    return _safe_div(close - low, high - low)


def calc_trend_score(history: Dict[str, float]) -> float:
    """Simple trend score in [0, 1]."""
    ma5 = history.get("ma5", 0.0)
    ma10 = history.get("ma10", 0.0)
    ma20 = history.get("ma20", 0.0)
    close = history.get("close", 0.0)

    score = 0.0
    if ma5 > ma10 > ma20:
        score += 0.6
    if close >= ma20:
        score += 0.4
    return score


def build_feature_rows(
    auction_rows: List[Dict],
    prev_day_rows: Dict[str, Dict],
    sector_strength: Dict[str, float],
    history_rows: Dict[str, Dict],
    fundamental_risk_flags: Dict[str, int],
) -> List[Dict]:
    """Merge multiple sources into model-ready rows."""
    out: List[Dict] = []

    for row in auction_rows:
        code = row["code"]
        prev = prev_day_rows[code]
        hist = history_rows.get(code, {})

        out.append(
            {
                "code": code,
                "open_ret": calc_open_ret(row["open"], prev["prev_close"]),
                "auction_amt_ratio": _safe_div(row["auction_amt"], row.get("avg_auction_amt_n", 0.0)),
                "auction_vol_ratio": _safe_div(row["auction_vol"], row.get("avg_auction_vol_n", 0.0)),
                "prev_day_close_pos": calc_close_position(prev["close"], prev["low"], prev["high"]),
                "prev_day_vol_ratio": _safe_div(prev["volume"], prev.get("avg_volume_n", 0.0)),
                "sector_strength": sector_strength.get(code, 0.0),
                "trend_score": calc_trend_score(hist),
                "fundamental_risk_flag": fundamental_risk_flags.get(code, 0),
                "is_st": prev.get("is_st", False),
                "is_new": prev.get("is_new", False),
                "prev_amount": prev.get("amount", 0.0),
            }
        )

    return out
