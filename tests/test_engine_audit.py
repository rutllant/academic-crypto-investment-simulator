from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import engine  # noqa: E402


def manual_ema(values: np.ndarray, span: int) -> np.ndarray:
    alpha = 2.0 / (span + 1.0)
    out = np.empty(len(values), dtype=float)
    out[0] = float(values[0])
    for i in range(1, len(values)):
        out[i] = alpha * float(values[i]) + (1.0 - alpha) * out[i - 1]
    return out


def manual_rsi(values: np.ndarray, period: int) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    delta = np.diff(values)
    gains = np.maximum(delta, 0.0)
    losses = np.maximum(-delta, 0.0)

    avg_gain = np.empty(len(gains), dtype=float)
    avg_loss = np.empty(len(losses), dtype=float)
    avg_gain[0] = gains[0]
    avg_loss[0] = losses[0]
    alpha = 1.0 / period

    for i in range(1, len(gains)):
        avg_gain[i] = alpha * gains[i] + (1.0 - alpha) * avg_gain[i - 1]
        avg_loss[i] = alpha * losses[i] + (1.0 - alpha) * avg_loss[i - 1]

    out = np.full(len(values), np.nan, dtype=float)
    for i in range(period, len(values)):
        g = avg_gain[i - 1]
        l = avg_loss[i - 1]
        if l == 0 and g > 0:
            out[i] = 100.0
        elif l == 0 and g == 0:
            out[i] = np.nan
        else:
            rs = g / l
            out[i] = 100.0 - (100.0 / (1.0 + rs))
    return out


def make_ohlc(
    opens: list[float],
    closes: list[float],
    scores: list[int] | None = None,
    start: str = "2025-01-01",
) -> pd.DataFrame:
    idx = pd.date_range(start, periods=len(opens), freq="D")
    o = np.asarray(opens, dtype=float)
    c = np.asarray(closes, dtype=float)
    df = pd.DataFrame(
        {
            "open": o,
            "high": np.maximum(o, c),
            "low": np.minimum(o, c),
            "close": c,
            "volume": np.full(len(o), 100.0),
        },
        index=idx,
    )
    if scores is not None:
        df["score"] = scores
    return df


class IndicatorAuditTests(unittest.TestCase):
    def test_ema_rsi_macd_against_independent_recurrences(self) -> None:
        close = np.array(
            [100, 101, 102, 101, 103, 105, 104, 106, 107, 106,
             108, 109, 110, 108, 111, 112, 113, 112, 114, 115,
             116, 114, 117, 118, 119, 121, 120, 122, 123, 124,
             122, 125, 126, 127, 128, 126, 129, 130, 131, 132,
             133, 131, 134, 135, 136, 137, 138, 136, 139, 140],
            dtype=float,
        )
        df = make_ohlc(close.tolist(), close.tolist())
        rules = dict(engine.DEFAULT_RULES)
        got = engine.indicators(df, rules)

        ema_fast = manual_ema(close, rules["ema_fast"])
        ema_slow = manual_ema(close, rules["ema_slow"])
        macd = manual_ema(close, rules["macd_fast"]) - manual_ema(close, rules["macd_slow"])
        macd_signal = manual_ema(macd, rules["macd_signal"])
        rsi = manual_rsi(close, rules["rsi_period"])

        np.testing.assert_allclose(got["ema_fast"].to_numpy(), ema_fast, rtol=0, atol=1e-10)
        np.testing.assert_allclose(got["ema_slow"].to_numpy(), ema_slow, rtol=0, atol=1e-10)
        np.testing.assert_allclose(got["macd"].to_numpy(), macd, rtol=0, atol=1e-10)
        np.testing.assert_allclose(got["macd_signal"].to_numpy(), macd_signal, rtol=0, atol=1e-10)
        np.testing.assert_allclose(
            got["rsi"].to_numpy()[rules["rsi_period"] :],
            rsi[rules["rsi_period"] :],
            rtol=0,
            atol=1e-10,
            equal_nan=True,
        )


class BacktestAccountingAuditTests(unittest.TestCase):
    def test_hodl_known_result_without_fees(self) -> None:
        df = make_ohlc([100, 110, 121], [100, 110, 121], scores=[0, 0, 0])
        out = engine.hodl_equity(
            {"BTC/EUR": df},
            initial_capital=10000.0,
            commission=0.0,
            symbols=["BTC/EUR"],
        )["HODL BTC"]
        self.assertAlmostEqual(out.iloc[0], 10000.0, places=8)
        self.assertAlmostEqual(out.iloc[-1], 12100.0, places=8)

    def test_signal_is_executed_on_next_bar_open_not_same_close(self) -> None:
        dates = pd.date_range("2025-01-01", periods=6, freq="D")
        df = pd.DataFrame(
            {
                "open": [100, 100, 200, 200, 200, 200],
                "high": [100, 100, 200, 200, 200, 200],
                "low": [100, 100, 200, 200, 200, 200],
                "close": [100, 100, 200, 200, 200, 200],
                "volume": [1, 1, 1, 1, 1, 1],
                "score": [0, 3, 0, 0, 0, 0],
            },
            index=dates,
        )
        rules = dict(engine.DEFAULT_RULES)
        rules["min_score"] = 2
        rules["max_weight"] = 1.0

        result = engine.run_agent_backtest(
            {"BTC/EUR": df},
            initial_capital=10000.0,
            commission=0.0,
            rules=rules,
            evaluation_start=dates[1],
            evaluation_end=dates[-1],
        )

        # Signal at Jan 2 is first actionable at Jan 3 open=200.
        # Therefore the gap from 100 to 200 must NOT be captured.
        self.assertAlmostEqual(result.metrics["final_value"], 10000.0, places=8)
        self.assertEqual(pd.Timestamp(result.trades.iloc[0]["signal_date"]), dates[1])
        self.assertEqual(pd.Timestamp(result.trades.iloc[0]["date"]), dates[2])

    def test_exact_transaction_cost_on_full_cash_entry(self) -> None:
        dates = pd.date_range("2025-01-01", periods=6, freq="D")
        df = make_ohlc([100] * 6, [100] * 6, scores=[3] * 6)
        df.index = dates
        rules = dict(engine.DEFAULT_RULES)
        rules["max_weight"] = 1.0
        rules["min_score"] = 2

        result = engine.run_agent_backtest(
            {"BTC/EUR": df},
            initial_capital=10000.0,
            commission=0.01,
            rules=rules,
            evaluation_start=dates[1],
            evaluation_end=dates[-1],
        )
        expected_post_trade = 10000.0 / 1.01
        self.assertAlmostEqual(result.equity.iloc[0], expected_post_trade, places=6)
        self.assertAlmostEqual(result.metrics["fees"], 10000.0 - expected_post_trade, places=6)

    def test_target_weights_respect_cap_and_total(self) -> None:
        weights = engine.target_weights(
            {"BTC/EUR": 3, "ETH/EUR": 3, "SOL/EUR": 3},
            min_score=2,
            max_weight=0.25,
        )
        self.assertLessEqual(sum(weights.values()), 1.0 + 1e-12)
        self.assertTrue(all(0.0 <= w <= 0.25 + 1e-12 for w in weights.values()))

    def test_metrics_known_drawdown_and_return(self) -> None:
        idx = pd.date_range("2025-01-01", periods=4, freq="D")
        equity = pd.Series([100.0, 120.0, 90.0, 110.0], index=idx)
        metrics = engine.calculate_metrics(equity, 100.0)
        self.assertAlmostEqual(metrics["total_return"], 0.10, places=12)
        self.assertAlmostEqual(metrics["max_drawdown"], -0.25, places=12)


class DataIntegrityAuditTests(unittest.TestCase):
    def test_invalid_ohlc_is_rejected(self) -> None:
        df = make_ohlc([100, 100, 100], [100, 100, 100])
        df.iloc[1, df.columns.get_loc("high")] = 90.0
        with self.assertRaises(ValueError):
            engine.validate_market_frame(df, "BTC/EUR")

    def test_valid_ohlc_passes(self) -> None:
        df = make_ohlc([100, 101, 99], [101, 99, 100])
        engine.validate_market_frame(df, "BTC/EUR")


class RandomAgentAuditTests(unittest.TestCase):
    def test_monte_carlo_is_reproducible_with_same_seed(self) -> None:
        df1 = make_ohlc([100] * 10, [100] * 10, scores=[0] * 10)
        df2 = make_ohlc([200] * 10, [200] * 10, scores=[0] * 10)
        data = {"BTC/EUR": df1, "ETH/EUR": df2}

        a = engine.monte_carlo_random_agents(
            data, 200, 10000.0, commission=0.001, decision_every_days=2, seed=123
        )
        b = engine.monte_carlo_random_agents(
            data, 200, 10000.0, commission=0.001, decision_every_days=2, seed=123
        )
        pd.testing.assert_frame_equal(a, b)

    def test_flat_market_drawdown_includes_transaction_costs(self) -> None:
        df1 = make_ohlc([100] * 12, [100] * 12, scores=[0] * 12)
        df2 = make_ohlc([200] * 12, [200] * 12, scores=[0] * 12)
        random = engine.monte_carlo_random_agents(
            {"BTC/EUR": df1, "ETH/EUR": df2},
            500,
            10000.0,
            commission=0.01,
            decision_every_days=1,
            seed=42,
        )
        # With flat prices and non-negative costs, wealth cannot recover above an earlier level.
        np.testing.assert_allclose(
            random["max_drawdown"].to_numpy(),
            random["total_return"].to_numpy(),
            rtol=0,
            atol=1e-10,
        )


if __name__ == "__main__":
    unittest.main()
