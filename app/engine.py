from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


DEFAULT_RULES = {
    "ema_enabled": True,
    "ema_fast": 20,
    "ema_slow": 50,
    "ema_points": 1,
    "rsi_enabled": True,
    "rsi_period": 14,
    "rsi_min": 50.0,
    "rsi_max": 70.0,
    "rsi_points": 1,
    "macd_enabled": True,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "macd_points": 1,
    "min_score": 2,
    "max_weight": 0.40,
}

# Fallback only if the live exchange catalogue cannot be loaded.
FALLBACK_MARKETS = {
    "EUR": ["BTC/EUR", "ETH/EUR", "SOL/EUR"],
    "USD": ["BTC/USD", "ETH/USD", "SOL/USD"],
    "USDT": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
    "USDC": ["BTC/USDC", "ETH/USDC", "SOL/USDC"],
}


@dataclass
class BacktestResult:
    equity: pd.Series
    trades: pd.DataFrame
    signals: pd.DataFrame
    metrics: Dict[str, float]


def list_spot_markets(exchange_id: str, quote: str = "EUR") -> List[str]:
    """Return all active spot markets for a quote currency from CCXT."""
    import ccxt

    if not hasattr(ccxt, exchange_id):
        raise ValueError(f"Exchange no suportat per CCXT: {exchange_id}")
    exchange = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    markets = exchange.load_markets()
    quote = quote.upper().strip()

    symbols: List[str] = []
    for symbol, market in markets.items():
        if market.get("spot") is not True:
            continue
        if market.get("active") is False:
            continue
        if str(market.get("quote", "")).upper() != quote:
            continue
        if not market.get("base"):
            continue
        symbols.append(symbol)

    def sort_key(symbol: str):
        base = symbol.split("/")[0].upper()
        preferred = {"BTC": 0, "ETH": 1, "SOL": 2}
        return (preferred.get(base, 99), base, symbol)

    return sorted(set(symbols), key=sort_key)


def validate_rules(rules: Mapping[str, object]) -> None:
    enabled = [
        bool(rules.get("ema_enabled")),
        bool(rules.get("rsi_enabled")),
        bool(rules.get("macd_enabled")),
    ]
    if not any(enabled):
        raise ValueError("Activa almenys una regla tècnica.")
    if int(rules["ema_fast"]) >= int(rules["ema_slow"]):
        raise ValueError("A la regla EMA, el període curt ha de ser inferior al període llarg.")
    if float(rules["rsi_min"]) >= float(rules["rsi_max"]):
        raise ValueError("A la regla RSI, el límit inferior ha de ser menor que el superior.")
    if int(rules["macd_fast"]) >= int(rules["macd_slow"]):
        raise ValueError("Al MACD, la mitjana ràpida ha de tenir un període inferior a la lenta.")
    max_score = sum(
        int(rules[k])
        for enabled_key, k in [
            ("ema_enabled", "ema_points"),
            ("rsi_enabled", "rsi_points"),
            ("macd_enabled", "macd_points"),
        ]
        if bool(rules.get(enabled_key))
    )
    if int(rules["min_score"]) < 1 or int(rules["min_score"]) > max_score:
        raise ValueError(f"La puntuació mínima ha d'estar entre 1 i {max_score}.")
    if not 0 < float(rules["max_weight"]) <= 1:
        raise ValueError("El pes màxim per actiu ha d'estar entre 0% i 100%.")


def _validate_commission(commission: float) -> float:
    commission = float(commission)
    if not 0 <= commission < 1:
        raise ValueError("La comissió ha d'estar entre 0% i 100%.")
    return commission


def validate_market_frame(df: pd.DataFrame, symbol: str = "actiu") -> None:
    """Validate basic OHLCV integrity before a series is used by the backtest."""
    required = {"open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{symbol}: falten columnes OHLC: {', '.join(sorted(missing))}.")
    if df.empty:
        raise ValueError(f"{symbol}: sèrie buida.")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(f"{symbol}: l'índex temporal no és DatetimeIndex.")
    if df.index.has_duplicates:
        raise ValueError(f"{symbol}: hi ha timestamps duplicats.")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{symbol}: els timestamps no estan ordenats.")

    ohlc = df[["open", "high", "low", "close"]].astype(float)
    values = ohlc.to_numpy()
    if not np.isfinite(values).all():
        raise ValueError(f"{symbol}: hi ha valors OHLC no finits.")
    if (values <= 0).any():
        raise ValueError(f"{symbol}: hi ha preus OHLC nuls o negatius.")

    bad_high = (ohlc["high"] < ohlc[["open", "close", "low"]].max(axis=1)).any()
    bad_low = (ohlc["low"] > ohlc[["open", "close", "high"]].min(axis=1)).any()
    if bad_high or bad_low:
        raise ValueError(f"{symbol}: incoherència OHLC (high/low no contenen open i close).")

    if "volume" in df.columns:
        volume = pd.to_numeric(df["volume"], errors="coerce")
        finite_volume = volume.dropna()
        if (finite_volume < 0).any():
            raise ValueError(f"{symbol}: hi ha volum negatiu.")


def warmup_bars(rules: Mapping[str, object]) -> int:
    """Conservative number of daily observations required before evaluation."""
    periods = [5]
    if bool(rules.get("ema_enabled")):
        periods.append(int(rules["ema_slow"]))
    if bool(rules.get("rsi_enabled")):
        periods.append(int(rules["rsi_period"]) + 2)
    if bool(rules.get("macd_enabled")):
        periods.append(int(rules["macd_slow"]) + int(rules["macd_signal"]))
    return max(periods) + 5


def indicators(df: pd.DataFrame, rules: Optional[Mapping[str, object]] = None) -> pd.DataFrame:
    """Calculate editable indicators and the agent score."""
    rules = dict(DEFAULT_RULES if rules is None else rules)
    validate_rules(rules)

    out = df.copy().sort_index()
    close = out["close"].astype(float)
    score = pd.Series(0, index=out.index, dtype=int)

    ema_fast = int(rules["ema_fast"])
    ema_slow = int(rules["ema_slow"])
    out["ema_fast"] = close.ewm(span=ema_fast, adjust=False).mean()
    out["ema_slow"] = close.ewm(span=ema_slow, adjust=False).mean()
    if bool(rules["ema_enabled"]):
        score += (out["ema_fast"] > out["ema_slow"]).astype(int) * int(rules["ema_points"])

    rsi_period = int(rules["rsi_period"])
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / rsi_period, adjust=False, min_periods=rsi_period).mean()
    avg_loss = loss.ewm(alpha=1 / rsi_period, adjust=False, min_periods=rsi_period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    out["rsi"] = 100 - (100 / (1 + rs))
    out.loc[(avg_loss == 0) & (avg_gain > 0), "rsi"] = 100
    if bool(rules["rsi_enabled"]):
        rsi_ok = (out["rsi"] >= float(rules["rsi_min"])) & (out["rsi"] <= float(rules["rsi_max"]))
        score += rsi_ok.astype(int) * int(rules["rsi_points"])

    macd_fast = int(rules["macd_fast"])
    macd_slow = int(rules["macd_slow"])
    macd_signal = int(rules["macd_signal"])
    ema_m_fast = close.ewm(span=macd_fast, adjust=False).mean()
    ema_m_slow = close.ewm(span=macd_slow, adjust=False).mean()
    out["macd"] = ema_m_fast - ema_m_slow
    out["macd_signal"] = out["macd"].ewm(span=macd_signal, adjust=False).mean()
    if bool(rules["macd_enabled"]):
        score += (out["macd"] > out["macd_signal"]).astype(int) * int(rules["macd_points"])

    out["score"] = score
    return out


def fetch_market_data(
    exchange_id: str,
    symbols: Iterable[str],
    start: pd.Timestamp,
    end: pd.Timestamp,
    timeframe: str = "1d",
    rules: Optional[Mapping[str, object]] = None,
) -> Dict[str, pd.DataFrame]:
    """Fetch public OHLCV data through CCXT. No account or API key is used."""
    import ccxt

    if not hasattr(ccxt, exchange_id):
        raise ValueError(f"Exchange no suportat per CCXT: {exchange_id}")

    exchange = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    exchange.load_markets()

    start = pd.Timestamp(start, tz="UTC") if pd.Timestamp(start).tz is None else pd.Timestamp(start).tz_convert("UTC")
    end = pd.Timestamp(end, tz="UTC") if pd.Timestamp(end).tz is None else pd.Timestamp(end).tz_convert("UTC")
    since = int(start.timestamp() * 1000)
    end_ms = int((end + pd.Timedelta(days=1)).timestamp() * 1000)

    result: Dict[str, pd.DataFrame] = {}
    errors: List[str] = []
    for symbol in symbols:
        if symbol not in exchange.markets:
            errors.append(f"{symbol}: mercat no disponible")
            continue

        rows: List[list] = []
        cursor = since
        try:
            while cursor < end_ms:
                batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=cursor, limit=1000)
                if not batch:
                    break
                rows.extend(batch)
                newest = int(batch[-1][0])
                next_cursor = newest + 1
                if next_cursor <= cursor:
                    break
                cursor = next_cursor
                if newest >= end_ms:
                    break
        except Exception as exc:
            errors.append(f"{symbol}: {exc}")
            continue

        if not rows:
            errors.append(f"{symbol}: sense dades")
            continue

        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True).dt.tz_convert(None)
        df = df.drop_duplicates("date").set_index("date").sort_index()
        df = df.loc[(df.index >= start.tz_localize(None)) & (df.index <= end.tz_localize(None))]
        if df.empty:
            errors.append(f"{symbol}: sense dades dins del període")
            continue
        try:
            validate_market_frame(df, symbol)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        result[symbol] = indicators(df, rules)

    if not result:
        detail = "; ".join(errors[:5])
        raise RuntimeError(f"No s'han pogut obtenir dades dels actius seleccionats. {detail}")
    return result


def _common_dates(
    data: Dict[str, pd.DataFrame],
    evaluation_start: Optional[pd.Timestamp] = None,
    evaluation_end: Optional[pd.Timestamp] = None,
) -> pd.DatetimeIndex:
    idx = None
    for df in data.values():
        idx = df.index if idx is None else idx.intersection(df.index)
    if idx is None or len(idx) == 0:
        raise ValueError("No hi ha dates comunes entre els actius.")
    idx = idx.sort_values()
    if evaluation_start is not None:
        start = pd.Timestamp(evaluation_start)
        if start.tzinfo is not None:
            start = start.tz_convert(None)
        idx = idx[idx >= start]
    if evaluation_end is not None:
        end = pd.Timestamp(evaluation_end)
        if end.tzinfo is not None:
            end = end.tz_convert(None)
        idx = idx[idx <= end]
    if len(idx) == 0:
        raise ValueError("No hi ha dades comunes dins del període d'avaluació.")
    return idx


def target_weights(
    scores: Dict[str, int],
    min_score: int = 2,
    max_weight: float = 0.40,
) -> Dict[str, float]:
    eligible = [s for s, score in scores.items() if score >= min_score]
    if not eligible:
        return {s: 0.0 for s in scores}
    equal = min(1.0 / len(eligible), max_weight)
    return {s: (equal if s in eligible else 0.0) for s in scores}


def _solve_rebalance_scalar(
    total_before: float,
    current_values: Mapping[str, float],
    desired_weights: Mapping[str, float],
    commission: float,
) -> Tuple[float, Dict[str, float], float, float]:
    """Solve fee = commission * traded notional when fees reduce investable capital."""
    commission = _validate_commission(commission)
    total_before = max(float(total_before), 0.0)
    post_value = total_before

    for _ in range(100):
        targets = {s: post_value * float(desired_weights[s]) for s in desired_weights}
        turnover = sum(abs(targets[s] - float(current_values.get(s, 0.0))) for s in desired_weights)
        fee = turnover * commission
        new_post = max(total_before - fee, 0.0)
        if abs(new_post - post_value) <= 1e-12 * max(1.0, total_before):
            post_value = new_post
            break
        post_value = new_post

    targets = {s: post_value * float(desired_weights[s]) for s in desired_weights}
    turnover = sum(abs(targets[s] - float(current_values.get(s, 0.0))) for s in desired_weights)
    fee = max(total_before - post_value, 0.0)
    return post_value, targets, fee, turnover


def _solve_rebalance_vectorized(
    total_before: np.ndarray,
    current_values: np.ndarray,
    desired_weights: np.ndarray,
    commission: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    commission = _validate_commission(commission)
    post = np.maximum(np.asarray(total_before, dtype=float), 0.0).copy()

    for _ in range(100):
        targets = post[:, None] * desired_weights
        turnover = np.abs(targets - current_values).sum(axis=1)
        new_post = np.maximum(total_before - turnover * commission, 0.0)
        if np.all(np.abs(new_post - post) <= 1e-12 * np.maximum(1.0, total_before)):
            post = new_post
            break
        post = new_post

    targets = post[:, None] * desired_weights
    fees = np.maximum(total_before - post, 0.0)
    return post, targets, fees


def run_agent_backtest(
    data: Dict[str, pd.DataFrame],
    initial_capital: float = 10000.0,
    commission: float = 0.001,
    rules: Optional[Mapping[str, object]] = None,
    evaluation_start: Optional[pd.Timestamp] = None,
    evaluation_end: Optional[pd.Timestamp] = None,
) -> BacktestResult:
    """Run a no-lookahead daily backtest.

    Signals are calculated from the previous completed daily candle and executed at the
    next candle's open. Portfolio equity is marked at each candle's close.
    """
    rules = dict(DEFAULT_RULES if rules is None else rules)
    validate_rules(rules)
    commission = _validate_commission(commission)
    symbols = list(data)
    for symbol, df in data.items():
        validate_market_frame(df, symbol)

    all_dates = _common_dates(data)
    dates = _common_dates(data, evaluation_start, evaluation_end)
    if len(dates) < 5:
        raise ValueError("Període massa curt per executar el backtest.")

    locations = all_dates.get_indexer(dates)
    cash = float(initial_capital)
    units = {s: 0.0 for s in symbols}
    previous_weights = {s: 0.0 for s in symbols}
    trades: List[dict] = []
    equity_rows: List[Tuple[pd.Timestamp, float]] = []
    signal_rows: List[dict] = []

    for i, date in enumerate(dates):
        loc = int(locations[i])
        signal_date = all_dates[loc - 1] if loc > 0 else None

        open_prices = {s: float(data[s].loc[date, "open"]) for s in symbols}
        close_prices = {s: float(data[s].loc[date, "close"]) for s in symbols}

        if signal_date is None:
            scores = {s: 0 for s in symbols}
        else:
            scores = {s: int(data[s].loc[signal_date, "score"]) for s in symbols}

        desired = target_weights(
            scores,
            min_score=int(rules["min_score"]),
            max_weight=float(rules["max_weight"]),
        )

        portfolio_open = cash + sum(units[s] * open_prices[s] for s in symbols)

        if any(abs(desired[s] - previous_weights[s]) > 1e-12 for s in symbols):
            current_values = {s: units[s] * open_prices[s] for s in symbols}
            post_value, target_values, fee, turnover = _solve_rebalance_scalar(
                portfolio_open,
                current_values,
                desired,
                commission,
            )
            units = {
                s: (target_values[s] / open_prices[s] if open_prices[s] > 0 else 0.0)
                for s in symbols
            }
            cash = post_value - sum(target_values.values())

            trades.append(
                {
                    "date": date,
                    "signal_date": signal_date,
                    "portfolio_before": portfolio_open,
                    "portfolio_after": post_value,
                    "fee": fee,
                    "turnover": turnover,
                    **{f"weight_{_base(s)}": desired[s] for s in symbols},
                    **{f"score_{_base(s)}": scores[s] for s in symbols},
                    **{f"open_{_base(s)}": open_prices[s] for s in symbols},
                }
            )
            previous_weights = desired.copy()

        value_close = cash + sum(units[s] * close_prices[s] for s in symbols)
        equity_rows.append((date, value_close))

        current_scores = {s: int(data[s].loc[date, "score"]) for s in symbols}
        signal_rows.append(
            {
                "date": date,
                **{f"score_{_base(s)}": current_scores[s] for s in symbols},
                **{f"close_{_base(s)}": close_prices[s] for s in symbols},
            }
        )

    equity = pd.Series(dict(equity_rows), name="Agent tècnic").sort_index()
    metrics = calculate_metrics(equity, initial_capital)
    metrics["trades"] = float(len(trades))
    metrics["fees"] = float(sum(t["fee"] for t in trades))
    return BacktestResult(
        equity=equity,
        trades=pd.DataFrame(trades),
        signals=pd.DataFrame(signal_rows).set_index("date"),
        metrics=metrics,
    )


def calculate_metrics(equity: pd.Series, initial_capital: float) -> Dict[str, float]:
    """Calculate close-to-close portfolio metrics using a zero risk-free rate."""
    equity = equity.dropna().astype(float)
    if equity.empty:
        return {}
    daily = equity.pct_change().dropna()
    total_return = equity.iloc[-1] / initial_capital - 1
    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    annual_vol = daily.std(ddof=1) * np.sqrt(365) if len(daily) > 1 else np.nan
    days = max((equity.index[-1] - equity.index[0]).days, 1)
    annual_return = (equity.iloc[-1] / max(initial_capital, 1e-12)) ** (365 / days) - 1
    sharpe = (
        daily.mean() / daily.std(ddof=1) * np.sqrt(365)
        if len(daily) > 1 and daily.std(ddof=1) > 0
        else np.nan
    )
    return {
        "final_value": float(equity.iloc[-1]),
        "total_return": float(total_return),
        "max_drawdown": float(drawdown.min()),
        "annual_volatility": float(annual_vol) if pd.notna(annual_vol) else np.nan,
        "annual_return": float(annual_return),
        "sharpe": float(sharpe) if pd.notna(sharpe) else np.nan,
    }


def hodl_equity(
    data: Dict[str, pd.DataFrame],
    initial_capital: float,
    commission: float = 0.001,
    symbols: Optional[Sequence[str]] = None,
    evaluation_start: Optional[pd.Timestamp] = None,
    evaluation_end: Optional[pd.Timestamp] = None,
) -> Dict[str, pd.Series]:
    """Buy each HODL asset at the first evaluation open and mark equity at daily closes."""
    commission = _validate_commission(commission)
    symbols = list(symbols if symbols is not None else data.keys())
    missing = [s for s in symbols if s not in data]
    if missing:
        raise ValueError(f"No hi ha dades per als holders: {', '.join(missing)}")
    for symbol in symbols:
        validate_market_frame(data[symbol], symbol)

    dates = _common_dates(data, evaluation_start, evaluation_end)
    out: Dict[str, pd.Series] = {}
    for symbol in symbols:
        entry_price = float(data[symbol].loc[dates[0], "open"])
        post_value, targets, _, _ = _solve_rebalance_scalar(
            float(initial_capital),
            {symbol: 0.0},
            {symbol: 1.0},
            commission,
        )
        units = targets[symbol] / entry_price
        px_close = data[symbol].loc[dates, "close"].astype(float)
        name = f"HODL {_base(symbol)}"
        out[name] = (units * px_close).rename(name)
    return out


def monte_carlo_random_agents(
    data: Dict[str, pd.DataFrame],
    n_agents: int,
    initial_capital: float,
    commission: float = 0.001,
    decision_every_days: int = 7,
    max_weight: float = 0.40,
    evaluation_start: Optional[pd.Timestamp] = None,
    evaluation_end: Optional[pd.Timestamp] = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Simulate random portfolios with open execution and deterministic seeding."""
    commission = _validate_commission(commission)
    symbols = list(data)
    for symbol, df in data.items():
        validate_market_frame(df, symbol)

    dates = _common_dates(data, evaluation_start, evaluation_end)
    opens = np.column_stack([data[s].loc[dates, "open"].to_numpy(float) for s in symbols])
    closes = np.column_stack([data[s].loc[dates, "close"].to_numpy(float) for s in symbols])
    n_assets = len(symbols)

    rng = np.random.default_rng(seed)
    cash = np.full(n_agents, float(initial_capital), dtype=float)
    units = np.zeros((n_agents, n_assets), dtype=np.float64)
    max_values = np.full(n_agents, float(initial_capital), dtype=float)
    max_drawdowns = np.zeros(n_agents, dtype=float)

    for day in range(len(dates)):
        open_values = units * opens[day][None, :]
        total_open = cash + open_values.sum(axis=1)

        if day % max(int(decision_every_days), 1) == 0:
            k = rng.integers(0, n_assets + 1, size=n_agents)
            priorities = rng.random((n_agents, n_assets), dtype=np.float32)
            order = np.argsort(priorities, axis=1)
            ranks = np.empty_like(order)
            row_idx = np.arange(n_agents)[:, None]
            ranks[row_idx, order] = np.arange(n_assets)
            selected_mask = ranks < k[:, None]

            per_asset = np.zeros(n_agents, dtype=np.float64)
            nonzero = k > 0
            per_asset[nonzero] = np.minimum(1.0 / k[nonzero], float(max_weight))
            new_weights = selected_mask.astype(np.float64) * per_asset[:, None]

            post, target_values, _fees = _solve_rebalance_vectorized(
                total_open,
                open_values,
                new_weights,
                commission,
            )
            units = np.divide(
                target_values,
                opens[day][None, :],
                out=np.zeros_like(target_values),
                where=opens[day][None, :] > 0,
            )
            cash = post - target_values.sum(axis=1)

        close_values = units * closes[day][None, :]
        values = cash + close_values.sum(axis=1)
        max_values = np.maximum(max_values, values)
        dd = values / max_values - 1
        max_drawdowns = np.minimum(max_drawdowns, dd)

    values = cash + (units * closes[-1][None, :]).sum(axis=1)
    final_return = values / initial_capital - 1
    return pd.DataFrame(
        {
            "agent": np.arange(1, n_agents + 1),
            "final_value": values,
            "total_return": final_return,
            "max_drawdown": max_drawdowns,
        }
    )


def evaluate_human_decisions(
    decisions: pd.DataFrame,
    data: Dict[str, pd.DataFrame],
    initial_capital: float,
    commission: float = 0.001,
    max_weight: float = 0.40,
    evaluation_start: Optional[pd.Timestamp] = None,
    evaluation_end: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """Evaluate dated human choices without using information from the same daily candle.

    A decision dated t becomes actionable at the first common market open strictly after t.
    """
    commission = _validate_commission(commission)
    required = {"participant", "date", "choice"}
    if not required.issubset(decisions.columns):
        raise ValueError("El CSV ha de tenir les columnes participant,date,choice.")

    common = _common_dates(data, evaluation_start, evaluation_end)
    for symbol, frame in data.items():
        validate_market_frame(frame, symbol)

    base_to_symbol = {_base(s).upper(): s for s in data}
    exact_symbols = {s.upper(): s for s in data}

    df = decisions.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    if df["date"].isna().any():
        raise ValueError("Hi ha alguna data del CSV que no es pot interpretar.")
    df["choice"] = df["choice"].astype(str).str.upper().str.strip()

    def normalize_choice(choice: str) -> str:
        if choice == "CASH":
            return "CASH"
        if choice in exact_symbols:
            return exact_symbols[choice]
        if choice in base_to_symbol:
            return base_to_symbol[choice]
        raise ValueError(f"Opció no disponible: {choice}. Usa CASH o una de les monedes seleccionades.")

    df["symbol"] = df["choice"].map(normalize_choice)

    opens = pd.DataFrame({s: data[s].loc[common, "open"].astype(float) for s in data})
    closes = pd.DataFrame({s: data[s].loc[common, "close"].astype(float) for s in data})

    results = []
    symbols = list(data)
    for participant, pdec in df.groupby("participant"):
        pdec = pdec.sort_values("date")
        cash = float(initial_capital)
        units = {s: 0.0 for s in symbols}
        held_symbol = "CASH"
        max_value_seen = float(initial_capital)
        max_dd = 0.0
        n_changes = 0

        for current_date in common:
            open_values = {s: units[s] * float(opens.loc[current_date, s]) for s in symbols}
            total_open = cash + sum(open_values.values())

            eligible = pdec[pdec["date"] < current_date]
            desired_symbol = eligible.iloc[-1]["symbol"] if not eligible.empty else held_symbol

            if desired_symbol != held_symbol:
                desired_weights = {s: 0.0 for s in symbols}
                if desired_symbol != "CASH":
                    desired_weights[desired_symbol] = float(max_weight)

                post_value, target_values, _fee, _turnover = _solve_rebalance_scalar(
                    total_open,
                    open_values,
                    desired_weights,
                    commission,
                )
                units = {
                    s: target_values[s] / float(opens.loc[current_date, s])
                    if float(opens.loc[current_date, s]) > 0
                    else 0.0
                    for s in symbols
                }
                cash = post_value - sum(target_values.values())
                held_symbol = desired_symbol
                n_changes += 1

            total_close = cash + sum(
                units[s] * float(closes.loc[current_date, s]) for s in symbols
            )
            max_value_seen = max(max_value_seen, total_close)
            max_dd = min(max_dd, total_close / max_value_seen - 1)

        final_value = cash + sum(
            units[s] * float(closes.loc[common[-1], s]) for s in symbols
        )
        results.append(
            {
                "participant": participant,
                "final_value": final_value,
                "total_return": final_value / initial_capital - 1,
                "max_drawdown": max_dd,
                "changes": n_changes,
            }
        )
    return pd.DataFrame(results)


def _base(symbol: str) -> str:
    return symbol.split("/")[0].split(":")[0]
