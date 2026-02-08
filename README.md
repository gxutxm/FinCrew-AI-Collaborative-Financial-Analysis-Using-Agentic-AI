# FinCrew: AI-Powered Financial Analysis

A collaborative financial analysis system built with AI agents. Think of it as a mini Wall Street research team — but powered by code.

---

## What Does This Project Do?

You give it a stock ticker (like `AAPL`), and it:

1. **Fetches** real market data
2. **Analyzes** the numbers (returns, risk, momentum)
3. **Researches** relevant news and sentiment
4. **Generates** professional charts
5. **Writes** a comprehensive report

All of this happens automatically through three specialized AI agents working together.

---

## The Three Agents

### 1. Market Research Agent
**Job:** Find out what's happening with the company

- Pulls financial news and headlines
- Analyzes sentiment (bullish/bearish/neutral)
- Flags potential risks
- Summarizes key events

### 2. Data Analyst Agent
**Job:** Crunch the numbers

- Fetches historical stock prices
- Calculates financial metrics:
  - **Total Return** — How much the stock gained/lost
  - **Volatility** — How risky is it?
  - **RSI** — Is it overbought or oversold?
  - **Max Drawdown** — Worst drop from peak
  - **Moving Averages** — Trend direction
- Generates charts (price, RSI, drawdown)

### 3. Report Writer Agent
**Job:** Package everything into a readable report

- Combines insights from both agents
- Writes clear, structured analysis
- Outputs PDF or dashboard

---

## How It Works

```
User: "Analyze AAPL for 2024"
            │
            ▼
    ┌───────────────┐
    │  Orchestrator │  ← Controls the flow
    └───────────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
┌──────────┐ ┌──────────┐
│ Market   │ │ Data     │
│ Research │ │ Analyst  │
│ Agent    │ │ Agent    │
└────┬─────┘ └────┬─────┘
     │            │
     └─────┬──────┘
           ▼
    ┌──────────────┐
    │ Report Writer│
    │ Agent        │
    └──────────────┘
           │
           ▼
    📄 Final Report
```

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/gxutxm/FinCrew-AI-Collaborative-Financial-Analysis-Using-Agentic-AI.git
cd FinCrew-AI-Collaborative-Financial-Analysis-Using-Agentic-AI
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Data Analyst Agent

```bash
cd data_analyst_agent
python test_agent.py
```

You'll see metrics calculated and charts saved to the `outputs/` folder.

---

## Example Output

When you run the Data Analyst Agent on Apple stock:

```json
{
  "ticker": "AAPL",
  "period": {
    "start": "2024-01-02",
    "end": "2024-12-30",
    "trading_days": 251
  },
  "metrics": {
    "total_return": 0.3652,
    "volatility_annual": 0.2245,
    "max_drawdown": -0.1535,
    "rsi_current": 58.38,
    "avg_daily_return": 0.001345
  },
  "charts": {
    "price": "outputs/AAPL_price.png",
    "rsi": "outputs/AAPL_rsi.png",
    "drawdown": "outputs/AAPL_drawdown.png"
  },
  "success": true
}
```

**Translation:**
- Apple returned **36.5%** in 2024
- Annual volatility of **22.5%** (moderate risk)
- Worst drop was **-15.4%** (January to April)
- Current RSI of **58** (neutral — not overbought or oversold)

---

## Project Structure

```
FinCrew-AI-Collaborative-Financial-Analysis-Using-Agentic-AI/
│
├── data_analyst_agent/          # Student 2's work
│   ├── data_fetcher.py          # Fetches stock data from Yahoo Finance
│   ├── metrics.py               # Calculates financial metrics
│   ├── visualizer.py            # Generates charts
│   ├── agent.py                 # Main interface
│   ├── test_*.py                # Test files
│   └── outputs/                 # Generated charts
│
├── market_research_agent/       # Student 1's work
│   └── fetch_news.ipynb         # News fetching and sentiment
│
├── report_writer_agent/         # Student 3's work
│   └── (coming soon)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Understanding the Metrics

| Metric | What It Means | Good or Bad? |
|--------|---------------|--------------|
| **Total Return** | Overall gain/loss for the period | Higher = better |
| **Volatility** | How much the price swings | Lower = less risky |
| **Max Drawdown** | Biggest drop from a peak | Closer to 0 = better |
| **RSI** | Momentum (0-100 scale) | 30-70 = neutral |
| **Moving Averages** | Smoothed price trend | Price above MA = bullish |

---

## Understanding the Charts

### Price Chart
Shows stock price over time with two trend lines:
- **SMA 20** (orange) — 20-day average, reacts quickly
- **SMA 50** (red) — 50-day average, shows longer trend

*When price crosses above the moving averages = bullish signal*

### RSI Chart
Shows momentum on a 0-100 scale:
- **Above 70** — Overbought (might drop soon)
- **Below 30** — Oversold (might rise soon)
- **Between 30-70** — Neutral

### Drawdown Chart
Shows how far below the peak price was at each point:
- **0%** — At all-time high
- **-15%** — Currently 15% below the peak

---

## Tech Stack

- **Python 3.9+**
- **yfinance** — Stock data from Yahoo Finance
- **pandas** — Data manipulation
- **numpy** — Mathematical calculations
- **matplotlib** — Chart generation

---

## Team

| Role | Agent | Responsibilities |
|------|-------|------------------|
| Student 1 | Market Research | News, sentiment, qualitative analysis |
| Student 2 | Data Analyst | Metrics, charts, quantitative analysis |
| Student 3 | Report Writer | Final report generation |

---

## Future Improvements

- [ ] Add more technical indicators (MACD, Bollinger Bands)
- [ ] Support for multiple stocks comparison
- [ ] Real-time data streaming
- [ ] Interactive Streamlit dashboard
- [ ] PDF report generation

---

## License

This project was built for educational purposes.

