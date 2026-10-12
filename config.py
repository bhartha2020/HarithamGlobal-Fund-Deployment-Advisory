"""
Configuration for the 5-Agent Indian Investment Advisory Team:
- Jasoos (15 Big-Ticket Stocks + News + NSE/BSE)
- Explorer (Global Indices -> Nifty/Sensex Movement)
- GrihaLaxmi (FII & DII 15-Day Cumulative Flow vs 15-DMA)
- SafetyPriya (MFs: Equity/Debt/Hybrid/Liquid from ICICI, Kotak, Tata, JioBlackRock, HDFC + NAV Movements vs FDs)
- Buddhiman (CIO Synthesizer -> Friday 5-Instrument Recommendation for Upcoming Monday)
"""

from typing import Dict, List, Any

# Web Server Configuration
DEFAULT_WEB_PORT = 8010
DEFAULT_WEB_HOST = "127.0.0.1"

# ==========================================
# 1. JASOOS AGENT CONFIGURATION
# ==========================================
# 15 Prominent Big-Ticket Indian Stocks
BIG_15_STOCKS = [
    {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy & Conglomerate", "cap": "Large"},
    {"symbol": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT & Software", "cap": "Large"},
    {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking & Financials", "cap": "Large"},
    {"symbol": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking & Financials", "cap": "Large"},
    {"symbol": "INFY.NS", "name": "Infosys", "sector": "IT & Software", "cap": "Large"},
    {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom", "cap": "Large"},
    {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Public Sector Banking", "cap": "Large"},
    {"symbol": "ITC.NS", "name": "ITC Ltd", "sector": "FMCG & Conglomerate", "cap": "Large"},
    {"symbol": "LT.NS", "name": "Larsen & Toubro", "sector": "Capital Goods & Infrastructure", "cap": "Large"},
    {"symbol": "TATAMOTORS.NS", "name": "Tata Motors", "sector": "Automobile & EV", "cap": "Large"},
    {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical", "sector": "Pharmaceuticals", "cap": "Large"},
    {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance", "sector": "NBFC & Financials", "cap": "Large"},
    {"symbol": "MARUTI.NS", "name": "Maruti Suzuki", "sector": "Automobile", "cap": "Large"},
    {"symbol": "TITAN.NS", "name": "Titan Company", "sector": "Consumer Discretionary", "cap": "Large"},
    {"symbol": "ADANIENT.NS", "name": "Adani Enterprises", "sector": "Infrastructure & Conglomerate", "cap": "Large"},
]

NEWS_SOURCES = {
    "Economic_Times": {
        "name": "The Economic Times",
        "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "type": "rss"
    },
    "Business_Standard": {
        "name": "Business Standard",
        "url": "https://www.business-standard.com/rss/markets-106.rss",
        "type": "rss"
    },
    "NDTV_Profit": {
        "name": "NDTV Profit",
        "url": "https://feeds.feedburner.com/ndtvprofit-latest",
        "type": "rss"
    },
    "CNBC_TV18": {
        "name": "CNBC-TV18",
        "url": "https://www.cnbctv18.com/commonfeeds/v1/cns/rss/market.xml",
        "type": "rss"
    },
    "Financial_Times": {
        "name": "Financial Times (India / Asia Focus)",
        "url": "https://www.ft.com/markets?format=rss",
        "type": "rss"
    }
}

# ==========================================
# 2. EXPLORER AGENT CONFIGURATION
# ==========================================
# The 9 Key Global Indices tracked over 15 days
GLOBAL_INDICES = {
    "DOW_JONES": {"symbol": "^DJI", "name": "Dow Jones Industrial Average", "country": "USA", "region": "North America", "weight": 0.15},
    "NASDAQ": {"symbol": "^IXIC", "name": "NASDAQ Composite", "country": "USA", "region": "North America", "weight": 0.15},
    "NIKKEI_225": {"symbol": "^N225", "name": "Nikkei 225", "country": "Japan", "region": "Asia-Pacific", "weight": 0.10},
    "KOSPI": {"symbol": "^KS11", "name": "KOSPI Composite", "country": "South Korea", "region": "Asia-Pacific", "weight": 0.10},
    "SINGAPORE_STI": {"symbol": "^STI", "name": "Straits Times Index (STI)", "country": "Singapore", "region": "Asia-Pacific", "weight": 0.10},
    "HANG_SENG": {"symbol": "^HSI", "name": "Hang Seng Index", "country": "Hong Kong / China", "region": "Asia-Pacific", "weight": 0.12},
    "CAC_40": {"symbol": "^FCHI", "name": "CAC 40", "country": "France", "region": "Europe", "weight": 0.08},
    "DAX": {"symbol": "^GDAXI", "name": "DAX Performance Index", "country": "Germany", "region": "Europe", "weight": 0.10},
    "FTSE_100": {"symbol": "^FTSE", "name": "FTSE 100", "country": "United Kingdom", "region": "Europe", "weight": 0.10},
}

INDIAN_BENCHMARKS = {
    "NIFTY_50": {"symbol": "^NSEI", "name": "NIFTY 50", "country": "India"},
    "SENSEX": {"symbol": "^BSESN", "name": "BSE SENSEX", "country": "India"},
}

# Stock tiers for Benjamin Graham valuation & earnings multiple assessment
TOP_10_LARGE_CAPS = [
    {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy & Conglomerate"},
    {"symbol": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT & Software"},
    {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking & Financials"},
    {"symbol": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking & Financials"},
    {"symbol": "INFY.NS", "name": "Infosys Ltd", "sector": "IT & Software"},
    {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom & Digital"},
    {"symbol": "ITC.NS", "name": "ITC Ltd", "sector": "FMCG & Conglomerate"},
    {"symbol": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure & Capital Goods"},
    {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Public Sector Banking"},
    {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical", "sector": "Pharmaceuticals"}
]

TOP_10_MID_CAPS = [
    {"symbol": "FEDERALBNK.NS", "name": "Federal Bank", "sector": "Private Banking"},
    {"symbol": "PERSISTENT.NS", "name": "Persistent Systems", "sector": "IT Services"},
    {"symbol": "POLYCAB.NS", "name": "Polycab India", "sector": "Cables & Electricals"},
    {"symbol": "CUMMINSIND.NS", "name": "Cummins India", "sector": "Engineering & Engines"},
    {"symbol": "ASHOKLEY.NS", "name": "Ashok Leyland", "sector": "Commercial Vehicles"},
    {"symbol": "VOLTAS.NS", "name": "Voltas Ltd", "sector": "Consumer Durables & Cooling"},
    {"symbol": "DIXON.NS", "name": "Dixon Technologies", "sector": "Electronic Manufacturing"},
    {"symbol": "ASTRAL.NS", "name": "Astral Ltd", "sector": "Building Materials & Pipes"},
    {"symbol": "COFORGE.NS", "name": "Coforge Ltd", "sector": "IT Solutions"},
    {"symbol": "SUPREMEIND.NS", "name": "Supreme Industries", "sector": "Plastics & Industrial Goods"}
]

TOP_10_SMALL_CAPS = [
    {"symbol": "CDSL.NS", "name": "Central Depository Services (CDSL)", "sector": "Capital Markets Tech"},
    {"symbol": "BSE.NS", "name": "BSE Ltd", "sector": "Securities Exchange"},
    {"symbol": "KNRCON.NS", "name": "KNR Constructions", "sector": "Infrastructure & EPC"},
    {"symbol": "SONATSOFTW.NS", "name": "Sonata Software", "sector": "IT & Cloud Services"},
    {"symbol": "PRAJIND.NS", "name": "Praj Industries", "sector": "Bio-Energy & Process Engineering"},
    {"symbol": "CENTURYPLY.NS", "name": "Century Plyboards", "sector": "Wood & Building Materials"},
    {"symbol": "RADICO.NS", "name": "Radico Khaitan", "sector": "Beverages & Distilleries"},
    {"symbol": "EQUITASBNK.NS", "name": "Equitas Small Finance Bank", "sector": "Small Finance Banking"},
    {"symbol": "KARURVYSYA.NS", "name": "Karur Vysya Bank", "sector": "Regional Commercial Banking"},
    {"symbol": "CAMS.NS", "name": "Computer Age Management Services (CAMS)", "sector": "Financial Tech Services"}
]

# Sovereign 10-Year Bond Yields and Central Banks Scenarios
GLOBAL_BOND_YIELDS = {
    "US_10Y": {"symbol": "^TNX", "name": "US 10-Year Treasury Yield", "country": "USA", "benchmark_yield": 4.08},
    "INDIA_10Y": {"symbol": "IN10YT=RR", "name": "India 10-Year G-Sec Benchmark Yield", "country": "India", "benchmark_yield": 6.78},
    "GERMANY_10Y": {"symbol": "DE10YT=RR", "name": "German 10-Year Bund Yield", "country": "Germany", "benchmark_yield": 2.24},
    "UK_10Y": {"symbol": "GB10YT=RR", "name": "UK 10-Year Gilt Yield", "country": "United Kingdom", "benchmark_yield": 4.16},
    "JAPAN_10Y": {"symbol": "JP10YT=RR", "name": "Japan 10-Year JGB Yield", "country": "Japan", "benchmark_yield": 0.95},
}

# ==========================================
# 3. GRIHALAXMI AGENT CONFIGURATION
# ==========================================
# FII & DII Tracking: 15 trading days window
INSTITUTIONAL_WINDOW_DAYS = 15
NSE_FII_DII_API_URL = "https://www.nseindia.com/api/fiidiiTradeReact"

# ==========================================
# 4. SAFETYPRIYA AGENT CONFIGURATION
# ==========================================
# Target AMCs: ICICI Prudential, Kotak Mahindra, Tata, JioBlackRock, HDFC
# Categories: Equity, Debt, Hybrid, Liquid
MUTUAL_FUND_WATCHLIST = [
    # ICICI Prudential
    {
        "amc": "ICICI Prudential",
        "category": "Equity",
        "scheme_name": "ICICI Prudential Bluechip Fund - Direct Plan - Growth",
        "scheme_code": "120586",
        "risk": "Very High"
    },
    {
        "amc": "ICICI Prudential",
        "category": "Hybrid",
        "scheme_name": "ICICI Prudential Balanced Advantage Fund - Direct - Growth",
        "scheme_code": "120594",
        "risk": "Moderate High"
    },
    {
        "amc": "ICICI Prudential",
        "category": "Debt",
        "scheme_name": "ICICI Prudential All Seasons Bond Fund - Direct - Growth",
        "scheme_code": "120612",
        "risk": "Moderate Low"
    },
    {
        "amc": "ICICI Prudential",
        "category": "Liquid",
        "scheme_name": "ICICI Prudential Liquid Fund - Direct Plan - Growth",
        "scheme_code": "120626",
        "risk": "Low"
    },

    # HDFC AMC
    {
        "amc": "HDFC",
        "category": "Equity",
        "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth",
        "scheme_code": "119062",
        "risk": "Very High"
    },
    {
        "amc": "HDFC",
        "category": "Hybrid",
        "scheme_name": "HDFC Balanced Advantage Fund - Direct Plan - Growth",
        "scheme_code": "118989",
        "risk": "Moderate High"
    },
    {
        "amc": "HDFC",
        "category": "Debt",
        "scheme_name": "HDFC Short Term Debt Fund - Direct Plan - Growth",
        "scheme_code": "119097",
        "risk": "Low to Moderate"
    },
    {
        "amc": "HDFC",
        "category": "Liquid",
        "scheme_name": "HDFC Liquid Fund - Direct Plan - Growth",
        "scheme_code": "119109",
        "risk": "Low"
    },

    # Kotak Mahindra
    {
        "amc": "Kotak Mahindra",
        "category": "Equity",
        "scheme_name": "Kotak Bluechip Fund - Direct Plan - Growth",
        "scheme_code": "120152",
        "risk": "Very High"
    },
    {
        "amc": "Kotak Mahindra",
        "category": "Hybrid",
        "scheme_name": "Kotak Balanced Advantage Fund - Direct Plan - Growth",
        "scheme_code": "144180",
        "risk": "Moderate High"
    },
    {
        "amc": "Kotak Mahindra",
        "category": "Debt",
        "scheme_name": "Kotak Bond Fund - Direct Plan - Growth",
        "scheme_code": "120199",
        "risk": "Moderate"
    },
    {
        "amc": "Kotak Mahindra",
        "category": "Liquid",
        "scheme_name": "Kotak Liquid Fund - Direct Plan - Growth",
        "scheme_code": "120202",
        "risk": "Low"
    },

    # Tata AMC
    {
        "amc": "Tata",
        "category": "Equity",
        "scheme_name": "Tata Large & Mid Cap Fund - Direct Plan - Growth",
        "scheme_code": "120716",
        "risk": "Very High"
    },
    {
        "amc": "Tata",
        "category": "Hybrid",
        "scheme_name": "Tata Balanced Advantage Fund - Direct Plan - Growth",
        "scheme_code": "146030",
        "risk": "Moderate High"
    },
    {
        "amc": "Tata",
        "category": "Debt",
        "scheme_name": "Tata Short Term Bond Fund - Direct Plan - Growth",
        "scheme_code": "120760",
        "risk": "Moderate Low"
    },
    {
        "amc": "Tata",
        "category": "Liquid",
        "scheme_name": "Tata Liquid Fund - Direct Plan - Growth",
        "scheme_code": "120767",
        "risk": "Low"
    },

    # JioBlackRock (Jio Financial Services / BlackRock AMC joint initiative funds / proxies)
    {
        "amc": "JioBlackRock",
        "category": "Equity",
        "scheme_name": "JioBlackRock Digital India Growth & Core Equity Proxy",
        "scheme_code": "JBR_EQ_01",
        "risk": "Very High"
    },
    {
        "amc": "JioBlackRock",
        "category": "Hybrid",
        "scheme_name": "JioBlackRock Dynamic Multi-Asset Dynamic Fund",
        "scheme_code": "JBR_HY_01",
        "risk": "Moderate High"
    },
    {
        "amc": "JioBlackRock",
        "category": "Debt",
        "scheme_name": "JioBlackRock Government & Corporate Bond Fund",
        "scheme_code": "JBR_DB_01",
        "risk": "Low to Moderate"
    },
    {
        "amc": "JioBlackRock",
        "category": "Liquid",
        "scheme_name": "JioBlackRock Treasury Cash & Liquid Fund",
        "scheme_code": "JBR_LQ_01",
        "risk": "Low"
    },
]

# Fixed Deposit Benchmarks in India (Annual Interest Rates)
FD_BENCHMARKS = [
    {"bank": "State Bank of India (SBI)", "tenure": "1 - 2 Years", "general_rate": 6.80, "senior_rate": 7.30},
    {"bank": "HDFC Bank", "tenure": "1 - 2 Years", "general_rate": 7.10, "senior_rate": 7.60},
    {"bank": "ICICI Bank", "tenure": "1 - 2 Years", "general_rate": 7.20, "senior_rate": 7.75},
    {"bank": "Kotak Mahindra Bank", "tenure": "390 Days - 2 Years", "general_rate": 7.40, "senior_rate": 7.90},
    {"bank": "Bajaj Finance Fixed Deposit (AAA)", "tenure": "24 - 36 Months", "general_rate": 8.10, "senior_rate": 8.35},
]

# Benchmark ETFs
INDIAN_ETFS = [
    {"symbol": "NIFTYBEES.NS", "name": "Nippon India Nifty 50 BeES ETF", "category": "Large Cap Index ETF"},
    {"symbol": "BANKBEES.NS", "name": "Nippon India Bank BeES ETF", "category": "Banking Sector ETF"},
    {"symbol": "GOLDBEES.NS", "name": "Nippon India Gold BeES ETF", "category": "Commodity ETF"},
    {"symbol": "MON100.NS", "name": "Motilal Oswal Nasdaq 100 ETF", "category": "International Tech ETF"},
    {"symbol": "SILVERBEES.NS", "name": "Nippon India Silver ETF", "category": "Precious Metals ETF"}
]

# ==========================================
# 5. BUDDHIMAN ORCHESTRATION CONFIGURATION
# ==========================================
TOTAL_RECOMMENDED_PICKS = 5  # Exactly 5 picks for Friday recommendation
SCHEDULE_EVALUATION_DAY = "Friday"
SCHEDULE_ACTION_DAY = "Monday"
