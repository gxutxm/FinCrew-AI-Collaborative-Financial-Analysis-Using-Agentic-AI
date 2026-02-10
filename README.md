# FinCrew — AI-Collaborative Financial Analysis Using Agentic AI

A multi-agent AI system that simulates a Wall Street research team. Give it a stock ticker, and three specialized AI agents work together to fetch market data, crunch the numbers, research sentiment, and generate a professional financial report — all automatically.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/Framework-CrewAI-orange)
![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance-purple)


---

## How It Works

```
User: "Analyze AAPL for 2024"
            │
            ▼
    ┌───────────────┐
    │  Orchestrator  │  ← Controls agent flow
    └───────────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
┌──────────┐ ┌──────────┐
│  Market  │ │   Data   │
│ Research │ │  Analyst  │
│  Agent   │ │  Agent    │
└────┬─────┘ └────┬─────┘
     │            │
     └─────┬──────┘
           ▼
    ┌──────────────┐
    │ Report Writer │
    │    Agent      │
    └──────────────┘
           │
           ▼
      📄 Final Report
```

### The Three Agents

**Market Research Agent** — Pulls financial news and headlines, analyzes sentiment (bullish/bearish/neutral), flags potential risks, and summarizes key events affecting the stock.

**Data Analyst Agent** — Fetches historical stock prices via Yahoo Finance and computes financial metrics including total return, annualized volatility, RSI, max drawdown, and moving averages. Generates price, RSI, and drawdown charts.

**Report Writer Agent** — Combines insights from both agents into a structured, readable financial analysis report.

The **Orchestrator** controls agent execution order, manages data flow between agents, and handles error recovery.

---

## Example Output

Running the system on Apple (AAPL) for 2024:

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

**In plain English:** Apple returned 36.5% in 2024 with moderate risk (22.5% annual volatility). The worst drawdown was -15.4%. RSI of 58 indicates a neutral position — neither overbought nor oversold.

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
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
```

### 5. Run the full analysis

```bash
python orchestrator.py
```

Enter a ticker (e.g., `AAPL`), start date, and end date when prompted.

---

## Project Structure

```
FinCrew-AI-Collaborative-Financial-Analysis-Using-Agentic-AI/
│
├── data_analyst_agent/
│   ├── agent.py                 # Agent interface & orchestration hooks
│   ├── data_fetcher.py          # Yahoo Finance data retrieval
│   ├── metrics.py               # Financial metric calculations
│   ├── visualizer.py            # Chart generation (price, RSI, drawdown)
│   ├── test_agent.py            # Agent integration tests
│   ├── test_data_fetcher.py     # Data fetcher unit tests
│   ├── test_metrics.py          # Metrics unit tests
│   ├── test_visualizer.py       # Visualizer unit tests
│   └── outputs/                 # Generated charts
│
├── market_research_agent/
│   ├── market_research_agent.py # News sentiment analysis agent
│   └── fetch_news.ipynb         # News fetching notebook
│
├── report_writer/
│   ├── report_writer_agent.py   # Report generation agent
│   ├── schema.json              # Report output schema
│   ├── prompts/                 # LLM prompt templates
│   └── README.md                # Module documentation
│
├── reports/                     # Generated analysis reports
├── shared/                      # Shared utilities across agents
│
├── orchestrator.py              # Main entry point — runs all agents
├── report_generator.py          # Report formatting & export
├── test_full_pipeline.py        # End-to-end pipeline tests
├── .env                         # API keys (not committed)
├── .gitignore
└── README.md
```

---

## Metrics Reference

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Total Return** | Cumulative gain/loss over the period | Positive = profit, negative = loss |
| **Annualized Volatility** | Standard deviation of returns, annualized | < 20% low risk, 20-40% moderate, > 40% high |
| **Max Drawdown** | Largest peak-to-trough decline | Closer to 0% = more stable |
| **RSI** | Relative Strength Index (momentum) | > 70 overbought, < 30 oversold, 30-70 neutral |
| **Moving Averages** | Smoothed price trends (50-day, 200-day) | Golden cross (bullish) / death cross (bearish) |

---

## Tech Stack

- **Python 3.10+** — Core language
- **CrewAI** — Multi-agent orchestration framework
- **Yahoo Finance (yfinance)** — Market data
- **NewsAPI** — Financial news retrieval
- **Pandas / NumPy** — Data processing & metric calculations
- **Matplotlib** — Chart generation
- **OpenAI GPT** — LLM backbone for agent reasoning

---

## Key Concepts Demonstrated

- **Agentic AI** — Autonomous agents with specialized roles and tool access
- **Task delegation** — Orchestrator assigns and sequences agent work
- **Inter-agent communication** — Structured data handoff between agents
- **Tool calling** — Agents invoke external APIs (Yahoo Finance, NewsAPI)
- **Modular design** — Each agent is independently testable and swappable

---

## Future Improvements

- [ ] Streamlit dashboard for interactive analysis
- [ ] PDF report export
- [ ] Portfolio-level analysis (multi-ticker comparison)
- [ ] Options and derivatives data integration
- [ ] Historical backtesting capabilities

---

## Authors

Gautam G
Ashrith 
Abhiram
Vedika
