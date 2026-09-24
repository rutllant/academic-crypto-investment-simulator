# Validation and audit · Academic Crypto Investment Simulator v0.4.3

This document describes the numerical checks used to assess whether the simulator is calculating what its methodology says it calculates.

Passing these tests does **not** prove that technical analysis is profitable, nor that future results will resemble past results. It only increases confidence that the software implements the stated rules consistently and without known look-ahead errors.

## 1. Main correction introduced in v0.4.3

Versions up to v0.4.2 calculated a signal from a daily candle's closing price and could rebalance at that same closing price.

That creates a **same-bar execution bias**: the strategy uses information that is only fully known once the candle has closed and assumes execution at the price that produced the signal.

From v0.4.3:

- indicators are calculated from completed candles;
- a signal dated **t** can only be executed on the **next common candle**;
- execution uses that next candle's **open**;
- end-of-day portfolio value is marked using the candle's **close**;
- the trade log records both `signal_date` and execution `date`.

This means the strategy no longer captures an overnight move that occurred before the signal could realistically have been acted upon.

## 2. Indicator verification

`tests/test_engine_audit.py` independently recalculates:

- EMA;
- RSI;
- MACD;
- MACD signal line.

The reference calculations use explicit recurrence formulas rather than calling the simulator's indicator function.

The test compares the independent arrays with the values returned by `engine.indicators()` using a numerical tolerance of `1e-10`.

## 3. Known-result HODL test

A synthetic asset is created with prices:

```text
100 → 110 → 121
```

With:

- initial capital = 10,000;
- commission = 0;

a HODL portfolio must finish at exactly:

```text
10,000 × 121 / 100 = 12,100
```

The automated test checks this result.

## 4. No-look-ahead execution test

A synthetic series deliberately creates a large price gap between one close and the following open.

The signal appears on the earlier candle.

The test verifies that the simulator:

- does not enter at the candle close that generated the signal;
- enters only at the next candle open;
- does not capture the artificial gap before execution was possible.

This test is designed specifically to detect the same-bar bias present in versions up to v0.4.2.

## 5. Transaction-cost accounting

Trading costs are modeled as:

```text
fee = commission_rate × traded_notional
```

Because the fee itself reduces the amount available to invest, v0.4.3 solves the post-trade portfolio value iteratively until the accounting identity converges.

For a 100% entry from cash with:

- capital = 10,000;
- commission = 1%;

the post-trade value must be:

```text
10,000 / 1.01 = 9,900.990099...
```

and the difference must equal the recorded fee.

The automated test checks this relationship.

## 6. Portfolio-weight constraints

Automated tests verify that:

- no target weight exceeds the configured maximum;
- the sum of target weights never exceeds 100%;
- unallocated capital remains as cash.

## 7. Return and drawdown verification

A known equity path is tested:

```text
100 → 120 → 90 → 110
```

Expected results include:

- total return = +10%;
- maximum drawdown = -25%.

The simulator's metric function must reproduce these values.

The audit also checks that the **initial capital is treated as the pre-test reference value**. Therefore a loss or commission in the first evaluation session is included in drawdown, daily return, volatility and Sharpe instead of disappearing because the first observed portfolio value became the initial peak.

For cryptocurrency daily data:

- annualized volatility uses `sqrt(365)`;
- Sharpe uses the same 365-day factor;
- the modeled risk-free rate is 0.

These are explicit methodological assumptions, not universal definitions.

## 8. OHLCV integrity checks

Before market data enter the backtest, `validate_market_frame()` checks:

- required OHLC columns exist;
- timestamps are ordered;
- timestamps are unique;
- OHLC values are finite and positive;
- high is not below open/close/low;
- low is not above open/close/high;
- volume is not negative when present.

Synthetic invalid candles are included in the test suite and must be rejected.

These checks can detect malformed data, but they do not prove that an exchange itself published a correct price.

## 9. Monte Carlo reproducibility

Random agents use NumPy's seeded random-number generator.

The audit executes the same Monte Carlo simulation twice with the same seed and requires the resulting tables to be exactly equal.

This makes the random benchmark reproducible.

## 10. Random-agent cost and drawdown check

A flat synthetic market is used with non-zero trading costs.

Because asset prices never move, any decline must come only from costs. Wealth cannot recover through price appreciation.

The audit therefore checks that the recorded maximum drawdown is consistent with the final loss caused by transaction costs.

## 11. Human decisions

From v0.4.3, a human decision recorded on date **t** becomes executable only on the first common market open **strictly after t**.

This prevents a daily decision from being credited with a closing price movement from the same candle.

## 12. What these tests do not validate

The audit does not establish that:

- exchange prices are economically "true";
- CCXT and the exchange will never change historical data;
- slippage is zero in real trading;
- the selected commission matches a particular account or fee tier;
- all historical cryptocurrencies are represented by today's exchange catalogue;
- the technical rules have predictive power;
- backtest performance will persist out of sample.

Potential research limitations still include:

- survivorship bias in the current exchange catalogue;
- exchange-specific market history;
- simplified transaction costs;
- absence of order-book liquidity and slippage;
- parameter overfitting if rules are adjusted after examining test results.

## 13. Continuous integration

GitHub Actions runs:

```text
python scripts/validate_project.py
python -m unittest discover -s tests -v
```

A release should only be treated as audited when both the structural validation and all numerical tests pass on the exact commit used to build that release.

## 14. Interpretation

The appropriate claim for v0.4.3 is:

> The simulator has automated checks for indicator calculations, known-result portfolios, transaction-cost accounting, no-look-ahead execution, OHLCV integrity, drawdown/return calculations and Monte Carlo reproducibility.

It should **not** be described as proof that a trading strategy is profitable or suitable for real investment.
