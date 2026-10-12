# 🏦 5-Agent Indian Fund Deployment Advisory System

An autonomous, multi-agent AI investment intelligence system designed to advise on deploying fresh funds across **Stocks**, **Mutual Funds (MFs)**, **Exchange Traded Funds (ETFs)**, and **Fixed Deposits (FDs)** in India.

The team operates on a **Friday-to-Monday cadence**: every Friday, the system synthesizes data across all 5 agents and formulates an actionable recommendation of **5 specific instruments** ready for execution on the **upcoming Monday**.

---

## 👥 The 5 Specialized Agents

```
                             ┌───────────────────────┐
                             │       BUDDHIMAN       │
                             │  (Chief CIO Allocator) │
                             └───────────┬───────────┘
                                         │
        ┌───────────────────┬────────────┴────────────┬───────────────────┐
        ▼                   ▼                         ▼                   ▼
┌───────────────┐   ┌───────────────┐         ┌───────────────┐   ┌───────────────┐
│    JASOOS     │   │   EXPLORER    │         │  GRIHALAXMI   │   │  SAFETYPRIYA  │
│ 10D Block Deal│   │ 9 Global Macro│         │ FII/DII Flows │   │ 5 AMCs & FDs  │
│ Top 15 Deals  │   │ Graham & Bonds│         │ SQLite EOD DB │   │ 15D/1W NAVs   │
└───────┬───────┘   └───────┬───────┘         └───────┬───────┘   └───────┬───────┘
        │                   │                         │                   │
        └───────────────────┴────────────┬────────────┴───────────────────┘
                                         │  (Feeds Intelligence To)
                                         ▼
                     ┌───────────────────────────────────────┐
                     │     COUNCIL OF 3 ADVOCATES            │
                     │  (Specialized Sub-Agents)             │
                     ├───────────────────┬───────────────────┤
                     │ 🐂 StockBull      │ 100% Equities     │
                     │ 🎨 MFHussain      │ 100% Mutual Funds │
                     │ 🔒 FDLover        │ 100% FDs & Bonds  │
                     └───────────────────┴───────────────────┘
```

### 1. 🕵️ Agent "Jasoos" (The Block Deals Sleuth)
* **Mission**: Scans all block and bulk deals executed across NSE & BSE over the **previous 10 trading days** and isolates the **Top 15 Block Deals** by transaction value.
* **Sources Scanned**:
  * Leading Financial Media: Financial Times (FT), The Economic Times (ET), Business Standard, CNBC-TV18, NDTV Profit.
  * Exchange Data: Daily NSE and BSE published reports (volume spike ratios, delivery percentages, 1-week and 15-day return momentum, institutional transaction value).
* **Output**: Top 15 Block Deals, institutional accumulation score (0–100), and high-conviction equity picks.

### 2. 🌍 Agent "Explorer" (Global Macro, Broker Consensus & Graham Valuations)
* **Mission**: Evaluates 9 global indices across US, Asia, and Europe over 15 days, validates leading stock broker consensus, conducts Benjamin Graham valuation norms, and assesses central bank interest rate policies.
* **Global Indices**: Dow Jones, NASDAQ, Nikkei 225, KOSPI, STI, Hang Seng, CAC 40, DAX, FTSE 100 vs NIFTY 50 & SENSEX.
* **Broker Predictions**: Consensus Nifty/Sensex targets from 8 leading brokerages (ICICI Direct, Motilal Oswal, HDFC Securities, Kotak Securities, Axis Direct, Sharekhan, Angel One, IIFL).
* **Benjamin Graham Valuation Norms**: Assesses top 10 large cap, mid cap, and small cap stocks (Graham Multiplier $P/E \times P/B \le 22.5$, Graham Number, Margin of Safety).
* **Sovereign Bond & Central Bank Sentinel**: US Fed, ECB, BoJ, BoE, and RBI policy rates + 10Y sovereign bond yields and US-India spread.

### 3. 🪙 Agent "GrihaLaxmi" (Net Institutional Investment Database & Sentinel)
* **Mission**: Compares the last 15 days cumulative Net Institutional Investment (NII = FII Net + DII Net) with the rolling 15 days cumulative investment database starting from 1st Jan 2023.
* **Persistent Database**: Automatically extracts and maintains an indexed SQLite database (`data/grihalaxmi_flows.db`) storing every trading day's FII Net, DII Net, Daily NII, Rolling 15-Day Cumulative NII, and 15-Day Average of Cumulative NIIs.
* **End-of-Day (EOD) Auto-Update**: At the end of each day, GrihaLaxmi pulls today's published FII/DII data, recalculates the rolling 15-day cumulative NII, and updates the database.
* **User's Explicit Decision Rule**:
  > *"When the Multi-agent is run, GrihaLaxmi will compare the cumulative NII value including today with the 15 day average of the Cumulative NIIs. If today's Cumulative NII value is less than the 15 day average, then GrihaLaxmi suggests investing in the stock market."*

### 4. 🛡️ Agent "SafetyPriya" (Mutual Funds & Fixed Deposits Specialist)
* **Mission**: Analyzes Mutual Fund schemes across 4 asset classes from 5 mandated Asset Management Companies (AMCs) and compares against Fixed Deposits:
  * **AMCs**: ICICI Prudential, Kotak Mahindra, Tata, JioBlackRock, and HDFC.
  * **Categories**: Equity, Debt, Hybrid (Balanced Advantage), and Liquid Funds.
* **Metrics Tracked**: Last 15 days and 1 week NAV movements and return performance.
* **Safe Benchmark**: Compares mutual fund yields against top Indian Bank Fixed Deposit rates (SBI, HDFC Bank, ICICI Bank, Kotak Mahindra Bank, Bajaj Finance AAA FD: ~7.0% - 8.1% p.a.).

### 5. 🏛️ The Council of 3 Advocates (Working Under Buddhiman)
* **🐂 StockBull**: Formulates 5 empirical arguments for 100% Equities deployment and curates 5 best appreciation stocks (ICICI Bank, Bharti Airtel, Federal Bank, Persistent Systems, CDSL) summing strictly to 100%. Expected CAGR: 18% - 24% p.a.
* **🎨 MFHussain**: Formulates 5 arguments for 100% Mutual Funds deployment and curates 5 best performing funds across top AMCs (JioBlackRock Dynamic Multi-Asset, JioBlackRock Digital India, ICICI Prudential Balanced Advantage, ICICI Prudential All Seasons Bond, Tata Liquid) summing to 100%. Expected Return: 14% - 17% p.a.
* **🔒 FDLover**: Formulates 5 arguments for 100% Fixed Deposits & Corporate Bonds (Shriram Finance 8.60%, L&T Finance AAA Bond 8.15%, Bajaj Finance 8.10%, REC Ltd AAA Bond 7.55%, SBI 7.25%) splitting 100% across maximum 5 options. Blended Yield: 8.03% p.a. (8.28% Seniors).

### 6. 🧠 Agent "Buddhiman" (The Chief Investment Officer)
* **Mission**: Convenes the Council of 3 Advocates, ingests their competing 100% pitches, and issues his **Supreme Arbitration Ruling**. Rejects single-asset extremes, adopting a calibrated balanced allocation:
  1. Asset Class Allocation Matrix (% in Stocks, Mutual Funds, ETFs, and Fixed Deposits).
  2. The **Top 5 Actionable Picks** (combination of Stocks, MFs, or FDs) generated every **Friday** for execution on the **upcoming Monday**.
  3. Step-by-step Monday execution playbook.

### 7. 📜 Agent "Chitragupthan" (Simulation Ledger Agent)
* **Mission**: Tracks and audits every Friday prediction against live market performance starting from **9th October 2026**.
* **Features**:
  * Records fund value chosen on the prediction date and live current valuation.
  * Calculates exact Rupee and percentage changes per instrument.
  * Interactive "Simulate" popup modal and dedicated web ledger tab.

### 8. 🧭 Agent "Sarathy" (Strategic Quality Assessor & Monday Web Scout)
* **Mission**: Drives continuous improvements in Buddhiman and his council by auditing simulated returns against projected target run-rates.
* **Scouting Cadence**: Scouts the web every Monday for:
  1. **5 Specialized Financial Portals**: TradingView India, Trendlyne/Screener.in, Value Research, CRISIL Debt, Livemint/ET.
  2. **Fresh Business News**: Corporate earnings, capex announcements, and regulatory cues.
  3. **Monday Market Cues**: GIFT Nifty indications, Asian market opening cues, and Options Open Interest (OI) cluster analysis.
  4. **Major Technical Analysis**: NIFTY 50 20-DMA, 50-DMA, 200-DMA, RSI, and key support/resistance levels.
* **Delegation**: Formulates concrete improvement requirements and delegates them to Engineer Agent **Viswakarma**.

### 9. 🔨 Agent "Viswakarma" (Lead Systems Engineer & Code Modifying Agent)
* **Mission**: Autonomous software engineer that receives work orders from Sarathy, programs architectural enhancements, and patches the council agents.
* **Active Patches Deployed**:
  * **StockBull**: 20-DMA moving average confirmation, Trendlyne delivery volume % ($\ge 45\%$) check, TradingView chart support.
  * **MFHussain**: Value Research rolling 3Y Sharpe hurdle ($\ge 1.15$), Morningstar cross-scheme overlap filter ($< 35\%$).
  * **FDLover**: CRISIL corporate bond yield spread sentinel ($\ge 140$ bps over 10Y G-Sec), credit rating downgrade watch.
  * **Buddhiman**: Monday market cues bridge, continuous feedback loop, target cycle set for next Friday (**16 Oct 2026**) for implementation on **Monday, 19 Oct 2026**.

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.10+ (verified on Python 3.14)
* Installed packages: `fastapi`, `uvicorn`, `requests`, `beautifulsoup4`, `yfinance`, `pandas`

### Installation
```powershell
py -3.14 -m pip install -r requirements.txt
```

---

## 💻 How to Run

### 1. Interactive Web Dashboard (FastAPI SPA)
Launch the modern, responsive web dashboard:
```powershell
py run.py --web
```
Then open your browser at **[http://127.0.0.1:8010](http://127.0.0.1:8010)**.
* Click **"Run Friday Synthesis"** for instant real-time multi-agent arbitration.
* Click **"Download Dossier (.md)"** to save the recommendation report.
* Inspect tabs for Jasoos, Explorer, GrihaLaxmi, SafetyPriya, StockBull, MFHussain, and FDLover.

### 2. Command-Line Interface (CLI)
Run individual agents, advocates, or the entire team from the terminal:
```powershell
# Run the complete Buddhiman 5-pick Monday portfolio & Council arbitration
py cli.py

# Run Council Advocates
py cli.py --agent stockbull    # 100% Equities proposal & 5 stocks
py cli.py --agent mfhussain    # 100% Mutual Funds proposal & 5 funds
py cli.py --agent fdlover      # 100% Fixed Income & top 5 FD/Bond options

# Run Sensor Agents
py cli.py --agent jasoos       # 10-day Top 15 Block Deals surveillance
py cli.py --agent explorer     # 9 Global indices, broker consensus & Graham norms
py cli.py --agent grihalaxmi   # 15-day NII flows vs 15-DMA rule check
py cli.py --agent safetypriya  # 5 AMCs & FD benchmarks
py cli.py --agent stockbull    # 100% Equities advocate pitch
py cli.py --agent mfhussain    # 100% Mutual Funds advocate pitch
py cli.py --agent fdlover      # 100% Fixed Income advocate pitch
py cli.py --agent chitragupthan # Celestial Portfolio Simulation & Prediction Ledger

# Run all agents, synthesis, and simulation
py cli.py --agent all --export
```

### 3. Chitragupthan Prediction Simulation (New Window)
Click the **"Simulate"** button on the web app or browse to:
```text
http://127.0.0.1:8010/simulate
```
* **Chitragupthan** creates an empirical audit table for each prediction date:
  1. **Fund Value Chosen on Prediction Date (₹)**
  2. **Current Value (₹)**
  3. **% Change (%)**
  4. Real-time stock quotes, live AMFI NAVs, and compound interest accrual for Fixed Deposits.

### 4. Automated Friday Scheduler
Run the Friday evaluation and save the upcoming Monday dossier:
```powershell
py run.py --friday
```
This generates:
* `dossiers/recommendation_dossier_<timestamp>.json`
* `dossiers/recommendation_dossier_<timestamp>.md`

### 4. Running the Test Suite
Run the automated test suite verifying all agents and engines:
```powershell
py test_all.py
```

---

## 📂 Project Architecture

```
AgenticAI_Trials/
├── config.py                     # Central configuration for stocks, AMCs, indices, FDs
├── requirements.txt              # Project dependencies
├── run.py                        # Unified launcher (--web, --cli, --friday)
├── cli.py                        # Terminal CLI tool
├── scheduler.py                  # Weekly Friday scheduler & dossier generator
├── test_all.py                   # Automated test suite
├── dossiers/                     # Persisted Friday-to-Monday recommendation reports
├── data_engine/
│   ├── news_fetcher.py           # FT, ET, Business Standard, CNBC, NDTV Profit scraper & RSS
│   ├── market_data.py            # NSE/BSE stock quotes, 1W & 15D returns, volume spikes
│   ├── global_markets.py         # Dow Jones, Nasdaq, Nikkei, KOSPI, STI & Nifty impact
│   ├── institutional_flows.py    # 15-day FII & DII cumulative flows & 15-DMA check
│   ├── mutual_funds.py           # NAV tracking across ICICI, Kotak, Tata, JioBlackRock, HDFC
│   └── fd_benchmarks.py          # Top Indian bank fixed deposit benchmark yields
├── agents/
│   ├── jasoos.py                 # Agent 1: Big-ticket stock investigator
│   ├── explorer.py               # Agent 2: Global macro & Nifty/Sensex predictor
│   ├── grihalaxmi.py             # Agent 3: Institutional flow sentinel & contrarian trigger
│   ├── safetypriya.py            # Agent 4: Capital preservation & MF/FD specialist
│   └── buddhiman.py              # Agent 5: CIO synthesizer & 5-pick Monday portfolio allocator
└── web/
    ├── server.py                 # FastAPI backend server
    └── static/
        └── index.html            # Single-page dashboard UI (Tailwind CSS)
```

---

## 🛡️ Resilience & Reliability

* **Live Data with Calibrated Fallbacks**: The data engine connects to live endpoints (NSE API, AMFI / MFAPI, Yahoo Finance, and financial RSS feeds) while maintaining calibrated historical baselines so the system never crashes during market holidays, network drops, or rate limits.
* **Deterministic Windows Compatibility**: Formatted strings avoid Windows console cp1252 character mapping issues (using `Rs.` currency notation with utf-8 reconfigure support).
* **Zero External API Cost**: Fully functional algorithmic and quantitative reasoning out of the box without requiring paid proprietary API subscriptions.
