"""
Global Interest Rates & Bond Markets Engine for Explorer Agent:
- Evaluates interest rate scenarios and latest monetary policy changes considered by major Central Banks:
  * US Federal Reserve (Fed)
  * Reserve Bank of India (RBI)
  * European Central Bank (ECB)
  * Bank of Japan (BOJ)
  * Bank of England (BOE)
  * People's Bank of China (PBOC)
- Tracks 10-Year Sovereign Bond Yields (US 10Y Treasury, India 10Y G-Sec, German Bund, UK Gilt, Japan JGB).
- Computes yield spreads, sovereign risk differentials, and capital flow implications for Indian equities.
"""

from typing import Dict, List, Any
from datetime import datetime


CENTRAL_BANKS_SCENARIOS = [
    {
        "central_bank": "US Federal Reserve (Fed)",
        "country": "United States",
        "current_rate": "4.75% - 5.00%",
        "current_rate_num": 4.875,
        "recent_action": "50 bps rate cut at September FOMC (Commenced Easing Cycle)",
        "policy_cycle": "Active Monetary Easing",
        "future_changes_considered": "FOMC members project an additional 25 to 50 bps cuts over upcoming meetings; targeting terminal neutral rate of ~3.25% - 3.50% by late 2025.",
        "inflation_gdp_context": "Core PCE cooling toward 2.2%; labor market cooling with non-farm payrolls returning to pre-pandemic trends; real policy rate remains restrictive.",
        "equity_impact": "Favorable global liquidity tailwind; dollar index softening aids emerging market foreign portfolio investments (FPI)."
    },
    {
        "central_bank": "Reserve Bank of India (RBI)",
        "country": "India",
        "current_rate": "6.50% (Repo)",
        "current_rate_num": 6.50,
        "recent_action": "Shifted monetary policy stance from 'Withdrawal of Accommodation' to 'NEUTRAL' at October MPC",
        "policy_cycle": "Neutral Pivot / Easing Preparation",
        "future_changes_considered": "MPC paving way for first 25 bps repo rate cut in upcoming December/February meetings as headline CPI softens post-monsoon harvest.",
        "inflation_gdp_context": "FY25 GDP growth robust at 7.2%; core inflation subdued at ~3.5%; food inflation volatility monitored as base effects normalize.",
        "equity_impact": "High positive driver for rate-sensitive sectors (Private Banks, NBFCs, Real Estate, Automobile, Capital Goods); lowers corporate cost of debt."
    },
    {
        "central_bank": "European Central Bank (ECB)",
        "country": "Eurozone",
        "current_rate": "3.25% (Deposit Rate)",
        "current_rate_num": 3.25,
        "recent_action": "Delivered consecutive 25 bps cuts in September and October (Total 75 bps easing in 2024)",
        "policy_cycle": "Accelerating Easing Cycle",
        "future_changes_considered": "Back-to-back 25 bps rate cuts considered at every upcoming meeting through H1 2025 to stimulate stalled Eurozone growth.",
        "inflation_gdp_context": "Eurozone inflation plummeted to 1.7% - 1.8%, below the 2.0% target; German manufacturing PMI in contraction territory.",
        "equity_impact": "European yield suppression diverts global yield-seeking capital toward higher-yielding Asian and Indian sovereign bonds and equities."
    },
    {
        "central_bank": "Bank of Japan (BOJ)",
        "country": "Japan",
        "current_rate": "0.25%",
        "current_rate_num": 0.25,
        "recent_action": "Raised policy rate from 0.10% to 0.25% (Historic exit from 8 years of negative interest rates)",
        "policy_cycle": "Monetary Tightening / Normalization (Contrarian Global Shift)",
        "future_changes_considered": "Further rate hikes toward 0.50% - 0.75% actively considered; Governor Ueda monitoring domestic wage-price spiral and Yen stability.",
        "inflation_gdp_context": "Inflation exceeding 2.5% target for over two years; Spring Shunto wage negotiations secured strongest wage increases in 33 years (5.1%).",
        "equity_impact": "Key global macro risk: Yen carry-trade unwinding triggers periodic sharp volatility spikes across global indices, as observed in Nikkei and tech stocks."
    },
    {
        "central_bank": "Bank of England (BOE)",
        "country": "United Kingdom",
        "current_rate": "5.00%",
        "current_rate_num": 5.00,
        "recent_action": "Initiated rate cut cycle with 25 bps reduction from 5.25% in August",
        "policy_cycle": "Cautious & Gradual Easing",
        "future_changes_considered": "Quarter-point rate reductions considered once every quarter; cautious on services inflation and public sector wage awards.",
        "inflation_gdp_context": "Headline CPI near 2.2%, but UK services inflation and wage growth remain stickier than US and Eurozone.",
        "equity_impact": "Moderate UK rate easing supports multinational FTSE exporters and stabilizes global debt yields."
    },
    {
        "central_bank": "People's Bank of China (PBOC)",
        "country": "China",
        "current_rate": "3.35% (1Y LPR) / 3.85% (5Y LPR)",
        "current_rate_num": 3.35,
        "recent_action": "Unveiled aggressive 'Bazooka' stimulus package: cut RRR by 50 bps, lowered mortgage rates by 50 bps, launched swap facility for equities",
        "policy_cycle": "Aggressive Stimulus & Credit Expansion",
        "future_changes_considered": "Further 20 to 50 bps rate cuts and trillions in sovereign fiscal debt issuance under active review to tackle deflation and property crisis.",
        "inflation_gdp_context": "China facing prolonged disinflation / deflationary pressure; consumer spending sluggish, property investment contracting.",
        "equity_impact": "Massive liquidity injection sparked historic rally in Hang Seng & CSI 300; causes short-term tactical FPI portfolio rebalancing between India and China."
    }
]

SOVEREIGN_BONDS = [
    {
        "country": "United States",
        "instrument": "US 10-Year Treasury Note",
        "symbol": "^TNX",
        "current_yield_pct": 4.08,
        "fifteen_day_change_bps": +14,
        "trend": "Slightly Rising / Rangebound (4.00% - 4.15%)",
        "rating": "AAA (Stable)",
        "implication": "Anchor for global cost of capital; yields holding near 4% limit extreme equity multiple expansion."
    },
    {
        "country": "India",
        "instrument": "India 10-Year Benchmark G-Sec",
        "symbol": "IN10YT=RR",
        "current_yield_pct": 6.78,
        "fifteen_day_change_bps": -8,
        "trend": "Softening / Bullish (6.75% - 6.85%)",
        "rating": "BBB- (Positive Outlook)",
        "implication": "Yield softening reflects RBI neutral stance and strong domestic PF/Insurance/MF demand; reduces corporate borrowing costs."
    },
    {
        "country": "Germany",
        "instrument": "German 10-Year Federal Bund",
        "symbol": "DE10YT=RR",
        "current_yield_pct": 2.24,
        "fifteen_day_change_bps": +6,
        "trend": "Suppressed (2.15% - 2.30%)",
        "rating": "AAA (Stable)",
        "implication": "European risk-free anchor remains deeply suppressed due to recessionary drag in German industrial base."
    },
    {
        "country": "United Kingdom",
        "instrument": "UK 10-Year Gilt",
        "symbol": "GB10YT=RR",
        "current_yield_pct": 4.16,
        "fifteen_day_change_bps": +18,
        "trend": "Firm (4.05% - 4.25%)",
        "rating": "AA (Stable)",
        "implication": "Reflects UK fiscal borrowing announcements and sticky domestic services inflation."
    },
    {
        "country": "Japan",
        "instrument": "Japan 10-Year JGB",
        "symbol": "JP10YT=RR",
        "current_yield_pct": 0.95,
        "fifteen_day_change_bps": +7,
        "trend": "Rising toward 1.00%",
        "rating": "A+ (Stable)",
        "implication": "Approaching 1.00% psychologically critical ceiling; prompts Japanese domestic institutions to repatriate foreign assets."
    }
]


class InterestRatesBondsEngine:
    def __init__(self):
        pass

    def evaluate_interest_rates_and_bonds(self) -> Dict[str, Any]:
        """
        Compiles the global central bank interest rate landscape and sovereign bond market dynamics.
        """
        us_yield = 4.08
        india_yield = 6.78

        # US-India 10-Year Yield Spread
        yield_spread_bps = round((india_yield - us_yield) * 100)  # in basis points (e.g. 270 bps)
        yield_spread_pct = round(india_yield - us_yield, 2)

        # Historical benchmark: normal spread is 350 - 450 bps
        if yield_spread_bps < 300:
            spread_status = "Narrow Spread (270 bps) vs Historical 350-450 bps"
            spread_implication = (
                "The narrow US-India 10Y yield spread reduces foreign debt carry-trade incentives. "
                "Consequently, FPI inflows into India are heavily contingent on corporate earnings growth and equity multiples "
                "rather than fixed-income arbitrage."
            )
        else:
            spread_status = "Normal / Wide Spread"
            spread_implication = "Healthy interest rate buffer providing strong support for the Indian Rupee and debt inflows."

        # Global Central Bank Directional Summary
        easing_banks = ["US Federal Reserve (Fed)", "European Central Bank (ECB)", "Bank of England (BOE)", "People's Bank of China (PBOC)"]
        neutral_pivot_banks = ["Reserve Bank of India (RBI)"]
        hiking_banks = ["Bank of Japan (BOJ)"]

        summary = (
            f"Global Interest Rate & Bond Scenario: 4 of 6 major central banks (Fed, ECB, BOE, PBOC) are in active rate-cutting cycles. "
            f"RBI has pivoted its stance to 'NEUTRAL', laying groundwork for rate cuts in late 2024 / early 2025. "
            f"BOJ remains the sole tightening central bank (Rate: 0.25%, with further hikes considered), maintaining Yen volatility risk. "
            f"US 10Y Treasury yield stands at {us_yield}%, while India 10Y G-Sec yield has eased to {india_yield}%. "
            f"US-India yield spread of {yield_spread_bps} bps ({yield_spread_pct}%) keeps domestic equity earnings delivery paramount."
        )

        # Build keyed dictionary with standardized names and aliases
        cb_dict = {}
        for item in CENTRAL_BANKS_SCENARIOS:
            cb = dict(item)
            cb["stance"] = cb.get("stance", cb.get("policy_cycle", "Neutral"))
            cb["cycle_stage"] = cb.get("cycle_stage", cb.get("policy_cycle", "Neutral"))
            cb_dict[cb["central_bank"]] = cb
            if "US Federal Reserve" in cb["central_bank"]:
                cb_dict["US Federal Reserve"] = cb
            if "Reserve Bank of India" in cb["central_bank"]:
                cb_dict["Reserve Bank of India (RBI)"] = cb
            if "European Central Bank" in cb["central_bank"]:
                cb_dict["European Central Bank (ECB)"] = cb
            if "Bank of Japan" in cb["central_bank"]:
                cb_dict["Bank of Japan (BOJ)"] = cb
            if "Bank of England" in cb["central_bank"]:
                cb_dict["Bank of England (BOE)"] = cb
            if "China" in cb["central_bank"]:
                cb_dict["People's Bank of China (PBOC)"] = cb

        bonds_list = []
        for b_item in SOVEREIGN_BONDS:
            b = dict(b_item)
            b["name"] = b.get("name", b.get("instrument", b.get("country", "Bond")))
            b["implication_for_india"] = b.get("implication_for_india", b.get("implication", ""))
            bonds_list.append(b)

        return {
            "summary": summary,
            "central_banks": cb_dict,
            "central_banks_list": list(cb_dict.values()),
            "bond_yields": bonds_list,
            "sovereign_bonds": bonds_list,
            "us_india_spread_bps": yield_spread_bps,
            "spread_assessment": spread_status,
            "yield_spread_analysis": {
                "us_10y_yield_pct": us_yield,
                "india_10y_yield_pct": india_yield,
                "spread_bps": yield_spread_bps,
                "spread_pct": yield_spread_pct,
                "spread_status": spread_status,
                "implication": spread_implication
            },
            "macro_regime_taxonomy": {
                "easing_cycle_banks": easing_banks,
                "neutral_pivot_banks": neutral_pivot_banks,
                "tightening_cycle_banks": hiking_banks
            }
        }
