# User Manual · Academic Crypto Investment Simulator

This manual is intended for people with **no prior investment knowledge**. Its purpose is to explain what each simulator option does, what the results mean, and how to interpret them without confusing a simulation with a prediction.

> **Important:** the simulator is designed for educational and research purposes. It does not trade real money, does not require API keys, and does not constitute financial advice. A favorable result in the past does not guarantee that a strategy will work in the future.

---

## 1. What exactly does the simulator do?

The program compares four different ways of making cryptocurrency investment decisions:

1. **Technical agent:** follows mechanical rules based on indicators such as EMA, RSI and MACD.
2. **Holders:** buy one cryptocurrency at the beginning and do nothing else until the end.
3. **Random agents:** make decisions randomly. They serve as a control group.
4. **Human investors:** allows decisions made by real people to be entered through a CSV file.

All of them start with the same initial capital and the same study period. This makes it possible to compare their results under similar conditions.

The program performs a **backtest**, meaning that it applies these decisions to real historical market data to see what would have happened.

---

## 2. Before you start: four basic ideas

### Cryptocurrency

A cryptocurrency is a digital asset, such as Bitcoin (BTC), Ether (ETH) or Solana (SOL). Its price changes continuously according to supply and demand.

### Spot market

The simulator uses **spot** markets. This means that it works with direct buying and selling of the asset, without leverage, futures or derivatives.

### Portfolio

The portfolio is the combination of cash and cryptocurrencies held by the agent at any given moment.

For example, a €10,000 portfolio could contain:

- €3,000 in BTC,
- €2,000 in ETH,
- €5,000 in cash.

### Cash

Cash is the part of the capital that is not invested in any cryptocurrency. In the simulator, cash does not earn interest.

---

# 3. “Market and portfolio” section

## Exchange

An **exchange** is a platform where cryptocurrencies are bought and sold.

The simulator can obtain public data from:

- Kraken
- Binance
- Coinbase
- Bitstamp

No account is opened and no real trades are placed. The exchange only acts as a **source of historical data**.

It is normal for the same asset to have small price differences between exchanges.

---

## Quote currency

This is the currency in which prices are expressed.

The simulator supports:

- EUR
- USD
- USDT
- USDC

For example:

**BTC/EUR** means that the price of Bitcoin is expressed in euros.

**ETH/USD** means that the price of Ether is expressed in US dollars.

To compare several assets correctly, all selected cryptocurrencies use the same quote currency.

---

## Cryptocurrencies

This is where you choose the assets that will form the investment universe of the experiment.

For example:

- BTC/EUR
- ETH/EUR
- SOL/EUR

The technical agent can only invest in the cryptocurrencies selected here.

Selecting many cryptocurrencies does not necessarily make the simulation better. The more assets are selected, the more data must be downloaded, and the more likely it is that one of the coins has only a short price history.

---

## Select all available cryptocurrencies

This option includes all spot markets available on the selected exchange and in the chosen quote currency.

It can be useful for experimentation, but it may cause:

- slower data downloads;
- longer calculations when thousands of random agents are simulated;
- a shorter effective analysis period if one of the cryptocurrencies is very new.

For a first test, it is usually easier to work with only a few cryptocurrencies.

---

## Initial capital

This is the virtual amount of money with which each strategy starts.

For example:

**€10,000**

This money is not real. The simulator calculates what would have happened to that amount during the selected period.

For fair comparisons, all groups should start with the same capital.

---

## Trading fee

In real markets, buying or selling usually has a cost.

If we enter:

**0.10%**

a €1,000 transaction has an approximate cost of €1.

Including fees is important because a strategy that buys and sells very frequently may appear highly profitable if these costs are ignored.

---

## Start date and end date

These define the period to be studied.

Example:

**January 1, 2024 — December 31, 2025**

The simulator downloads historical data and calculates what would have happened during that interval.

This is not a prediction of the future: it is a reconstruction of the past.

---

# 4. The technical agent

The technical agent does not “think” and does not try to guess the market.

It follows mathematical rules. Each rule can award points to a cryptocurrency. When a coin reaches the required minimum score, it may enter the portfolio.

This makes the strategy **systematic**: given the same data and the same parameters, it will make the same decision.

---

# 5. EMA: detecting trend

EMA means **Exponential Moving Average**.

It is an average of past prices that gives more weight to recent prices.

The simulator compares two EMAs:

- a **short EMA**, which reacts quickly to price changes;
- a **long EMA**, which represents a longer-term trend.

### Example

Short EMA = 20 days  
Long EMA = 50 days

If:

**EMA20 > EMA50**

the simulator interprets this as the recent price trend being above the longer-term trend and awards the points assigned to this rule.

This does not mean that the price must continue rising. It only indicates that a predefined trend condition has been met.

### EMA points

These determine how much influence this rule has within the scoring system.

For example:

EMA = 2 points  
RSI = 1 point  
MACD = 2 points

In this case, EMA and MACD have more influence on the final decision than RSI.

---

# 6. RSI: measuring momentum

RSI means **Relative Strength Index**.

It is an indicator that ranges from **0 to 100** and attempts to measure the recent strength of price movements.

As a rough guide, people often refer to:

- low values: stronger selling pressure;
- high values: stronger buying pressure.

However, the simulator does not automatically interpret “low = buy” or “high = sell”. It uses the interval defined by the user.

### Example

RSI period = 14  
Minimum RSI = 50  
Maximum RSI = 70

The rule will award points when:

**50 ≤ RSI(14) ≤ 70**

This looks for positive momentum without requiring an extremely high RSI value.

### RSI period

This is the number of sessions used to calculate the indicator.

A shorter period reacts faster; a longer period is more stable.

---

# 7. MACD: trend and momentum

MACD means **Moving Average Convergence Divergence**.

It uses two exponential moving averages and a signal line.

A common parameter set is:

**MACD (12, 26, 9)**

where:

- 12 is the fast period;
- 26 is the slow period;
- 9 is the signal-line period.

In the simulator, this rule awards points when the MACD line is above its signal line.

This is interpreted as a favorable momentum condition according to this specific rule.

As with EMA and RSI, MACD is only a mathematical indicator. It does not guarantee that the price will rise.

---

# 8. Minimum score required to invest

The three rules can contribute points.

Example:

| Rule | Points |
|---|---:|
| Favorable EMA | 2 |
| RSI inside the interval | 1 |
| Favorable MACD | 2 |
| **Maximum possible score** | **5** |

If we set:

**Minimum score = 4**

a cryptocurrency can only enter the portfolio when it obtains at least 4 points.

A lower minimum score makes the agent more permissive.

A higher minimum score requires stronger agreement between the indicators.

---

# 9. Maximum weight per cryptocurrency

This determines the maximum percentage of the portfolio that can be allocated to a single asset.

For example:

**Maximum weight = 40%**

With €10,000 of capital, no cryptocurrency could initially represent more than €4,000 of the portfolio at a rebalance.

This rule prevents the entire portfolio from being concentrated in a single coin.

If there are not enough cryptocurrencies that meet the rules, part of the capital remains in **CASH**.

---

# 10. When is a signal actually executed?

This is important when interpreting the backtest.

A daily candle's indicators are only fully known after that candle has closed. To avoid using future information, v0.4.3 works as follows:

1. day **t** closes;
2. EMA, RSI, MACD and the score are calculated;
3. any portfolio change is executed at the **next available daily open**;
4. the portfolio is valued again at the daily close.

This prevents the strategy from receiving credit for a price move that occurred before the signal could have been known.

Human-investor decisions are also made effective on the first session after the date recorded in the CSV.

---

# 11. What is a rebalance?

A **rebalance** is a moment when the agent changes the composition of the portfolio.

For example, it could move from:

- BTC: 40%
- ETH: 40%
- CASH: 20%

to:

- BTC: 0%
- ETH: 40%
- SOL: 40%
- CASH: 20%

This change involves buying and selling and may therefore generate fees.

The number of rebalances indicates whether the strategy has been very active or relatively stable.

---

# 12. Control holders

A **holder** follows a very simple strategy:

1. buys one cryptocurrency at the beginning;
2. holds it for the entire period;
3. makes no further decisions.

This is also known as a **buy-and-hold** strategy or, in cryptocurrency slang, **HODL**.

### Why are holders useful?

They help answer an important question:

> Was it worth using all the technical-agent rules, or would it have been better simply to buy a cryptocurrency and wait?

If the technical agent earns 15% but a BTC holder earns 40%, the agent's result is positive, but it has not outperformed that passive alternative.

---

# 13. Random agents

Random agents are the main control group in the experiment.

They do not use EMA, RSI or MACD. They randomly decide which cryptocurrencies to hold.

The simulator can run:

- 100
- 500
- 1,000
- 5,000
- 10,000 agents

The more agents we simulate, the better we can observe the distribution of outcomes produced by chance, although the calculation takes longer.

---

## Random-agent decision interval

This determines how often random agents are allowed to change their portfolios:

- every day;
- every 7 days;
- every 14 days;
- every 30 days.

Between decision dates, they keep their positions.

This prevents the technical agent from being compared with random agents that are forced to change their portfolio every day.

---

# 14. Run simulation

When you press **Run simulation**, the program:

1. downloads public historical data;
2. calculates EMA, RSI and MACD;
3. runs the technical agent;
4. simulates the random agents;
5. calculates the holders;
6. displays the results.

The simulation may take longer if many cryptocurrencies or thousands of random agents are selected.

---

# 15. How to interpret the results

## Final capital

This is the final value of the portfolio.

If we start with €10,000 and finish with €11,500:

**Final capital = €11,500**

---

## Return

Return is the percentage change in capital.

In the previous example:

**+15%**

If the final capital were €8,500:

**−15%**

Return alone does not explain how much risk was taken.

---

# 16. Maximum drawdown

**Drawdown** measures the decline from a previous portfolio high.

Example:

The portfolio reaches:

**€12,000**

and then falls to:

**€9,000**

The decline is:

**−25%**

Even if the portfolio later recovers, maximum drawdown records that fall.

It is an important measure because two strategies may end with the same return while having experienced very different levels of risk.

In general:

- drawdown closer to 0% = smaller declines;
- strongly negative drawdown = larger declines.

---

# 17. Sharpe ratio

The **Sharpe ratio** relates return to volatility.

In very simplified terms:

> it attempts to indicate how much return was obtained relative to the amount of fluctuation experienced.

A higher Sharpe ratio indicates a better relationship between return and variability within the model being used.

It should not be interpreted as a universal grade or as a guarantee of quality.

This is especially important for cryptocurrencies, where return distributions can be highly irregular and a single metric cannot summarize all risk.

---

# 18. Percentile relative to random agents

The simulator compares the technical agent's final capital with the final capital of all random agents.

If it reports:

**90th percentile**

this means, approximately, that the technical agent obtained a better result than 90% of the random simulations in that experiment.

It does **not** mean that the agent has a 90% probability of making money in the future.

It only describes the agent's position within **the simulations carried out for that period and that configuration**.

---

# 19. Random-agent histogram

The histogram shows how the returns of the random agents are distributed.

Each bar represents the number of agents that ended within a particular return range.

The **technical agent** line makes it possible to see visually whether its result is:

- near the center of the distribution;
- in a lower region;
- or in a higher region.

This is one of the most important charts for comparing the technical strategy with chance.

---

# 20. Technical agent vs holders

This chart shows the evolution of cumulative return for:

- the technical agent;
- each selected holder.

It allows you to see not only who finishes with the best result, but also **how each strategy got there**.

Two strategies can end with similar results while following very different paths.

---

# 21. Trades and signals

## Rebalances

This table shows the dates on which the agent changed the portfolio.

It is useful for understanding:

- when assets entered or left the portfolio;
- how often the portfolio changed;
- which changes generated trading fees.

## Daily signals

This table shows indicator values and the scores calculated for the cryptocurrencies.

It helps explain **why** a coin was or was not eligible on a given date.

## Export

This section allows results to be downloaded as CSV files for analysis in Excel, LibreOffice, Python, R or other tools.

---

# 22. Human investors

The simulator can compare the technical agent with decisions made by people.

First, download the CSV template.

The columns are:

| Column | Meaning |
|---|---|
| `participant` | Name or code of the participant |
| `date` | Date of the decision |
| `choice` | Selected cryptocurrency or CASH |

Example:

```csv
participant,date,choice
Person 1,2025-01-10,BTC
Person 1,2025-02-15,ETH
Person 1,2025-03-20,CASH
```

This means that Person 1:

- chooses BTC on January 10;
- changes to ETH on February 15;
- moves to cash on March 20.

When a cryptocurrency is selected, the simulator allocates at most the percentage defined by **Maximum weight per cryptocurrency**. The rest remains in CASH.

---

# 23. What does CASH mean for human investors?

**CASH** means that the participant does not hold any cryptocurrency at that moment.

It is useful when the participant decides not to be exposed to the market.

A decision does not need to be entered every day. The most recent decision remains in effect until the participant enters a new one.

---

# 24. A simple configuration for learning

To understand the simulator before carrying out the formal experiment, you can start with the following purely educational example:

| Parameter | Example |
|---|---|
| Exchange | Kraken |
| Quote currency | EUR |
| Cryptocurrencies | BTC, ETH, SOL |
| Capital | €10,000 |
| Fee | 0.10% |
| Period | 2 years |
| EMA | enabled |
| RSI | enabled |
| MACD | enabled |
| Holders | BTC, ETH and SOL |
| Random agents | 1,000 |
| Random decision interval | every 7 days |

This configuration is **not an investment recommendation**. It is simply an easy way to become familiar with how the program works.

For the research project, the final parameters should be methodologically justified and frozen before the main test.

---

# 25. Common interpretation mistakes

### “The agent made money, so the strategy works”

Not necessarily. It should be compared with holders, random agents, the risk taken, and other periods.

### “It beat the random agents, so it will always beat them”

No. The result only applies to the period, assets and parameters used in that experiment.

### “The strategy with the highest return is the safest”

No. A high return may have involved very large declines.

### “If I keep adjusting the parameters until the chart looks good, I have found a good strategy”

This may be **overfitting**: adapting the rules too closely to past data.

For this reason, in an academic experiment it is important to define the rules before observing the test-period results.

---

# 26. Key simulator terms

| Term | Short explanation |
|---|---|
| **Backtest** | Testing a strategy using past data |
| **Exchange** | Trading platform that provides the market data |
| **Spot** | Direct purchase or sale of the asset |
| **Portfolio** | Combination of assets and cash |
| **EMA** | Exponential average used to observe trends |
| **RSI** | Momentum indicator ranging from 0 to 100 |
| **MACD** | Indicator combining trend and momentum |
| **HODL / Holder** | Buy and hold without changing position |
| **Monte Carlo** | Repeating many simulations with random decisions |
| **Return** | Percentage change in capital |
| **Drawdown** | Decline from a previous high |
| **Sharpe** | Relationship between return and volatility |
| **Rebalance** | Change in portfolio composition |
| **CASH** | Capital not invested |
| **Percentile** | Relative position within a set of results |
| **Overfitting** | Fitting a strategy too closely to past results |

---

# 27. Why is this simulator not a prediction system?

Technical indicators are calculated from past prices.

The simulator can answer questions such as:

> What would have happened if we had applied these rules during this period?

But it cannot answer with certainty:

> What will happen to Bitcoin next week?

The main purpose of the project is to **compare decision systems**, not to predict prices.

---

# 28. Recommendation for academic use

To make the results comparable and reproducible:

1. define the cryptocurrencies;
2. define the period;
3. set the trading fee;
4. set EMA, RSI and MACD parameters;
5. set the minimum score;
6. set the maximum weight;
7. define the holders and random agents;
8. save this configuration;
9. run the test;
10. do not modify the rules after seeing the main result.

If the rules are changed after observing the results, this should be treated as a new strategy and tested on a different period.

---

## Related documentation

- `README.md` — installation and project features.
- `docs/PROTOCOL_TDR.md` — suggested experimental protocol.
- `SECURITY.md` — distribution and file-verification information.
- `docs/MANUAL_USUARI.md` — Catalan version of this manual.

---

**Manual version:** compatible with Academic Crypto Investment Simulator v0.4.3.
