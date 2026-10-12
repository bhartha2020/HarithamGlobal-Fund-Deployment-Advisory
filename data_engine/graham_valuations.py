"""
Benjamin Graham Norms & Earnings Multiples Assessment Engine:
- Analyzes Top 10 Large Cap, Top 10 Mid Cap, and Top 10 Small Cap Indian stocks.
- Extracts key earnings multiples: Trailing P/E, Forward P/E, P/B, EPS, Book Value Per Share (BVPS), ROE.
- Calculates Benjamin Graham's Classic Valuation Norms:
  1. Graham Number: sqrt(22.5 * EPS * BVPS)
  2. Graham Multiplier: (P/E * P/B) <= 22.5
  3. Margin of Safety % = (Graham Number - CMP) / CMP * 100
  4. Graham Compliance Verdict (PASS / FAIR VALUE / EXPENSIVE)
- Provides structured tier-wise summary averages for consumption by other agents.
"""

import math
from typing import List, Dict, Any


LARGE_CAP_FUNDAMENTALS = [
    {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy & Conglomerate", "cmp": 2980.0, "eps": 108.50, "bvps": 1120.0, "pe": 27.46, "fwd_pe": 24.1, "pb": 2.66, "div_yield": 0.35, "roe": 10.4},
    {"symbol": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT & Software", "cmp": 4120.0, "eps": 132.00, "bvps": 285.0, "pe": 31.21, "fwd_pe": 27.8, "pb": 14.45, "div_yield": 1.78, "roe": 48.2},
    {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking & Financials", "cmp": 1680.0, "eps": 86.50, "bvps": 610.0, "pe": 19.42, "fwd_pe": 16.9, "pb": 2.75, "div_yield": 1.15, "roe": 15.8},
    {"symbol": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking & Financials", "cmp": 1345.0, "eps": 68.00, "bvps": 415.0, "pe": 19.78, "fwd_pe": 17.2, "pb": 3.24, "div_yield": 0.85, "roe": 18.2},
    {"symbol": "INFY.NS", "name": "Infosys Ltd", "sector": "IT & Software", "cmp": 1890.0, "eps": 64.50, "bvps": 215.0, "pe": 29.30, "fwd_pe": 25.4, "pb": 8.79, "div_yield": 2.45, "roe": 31.5},
    {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom & Digital", "cmp": 1640.0, "eps": 38.00, "bvps": 195.0, "pe": 43.15, "fwd_pe": 36.5, "pb": 8.41, "div_yield": 0.55, "roe": 19.4},
    {"symbol": "ITC.NS", "name": "ITC Ltd", "sector": "FMCG & Conglomerate", "cmp": 495.0, "eps": 16.80, "bvps": 58.0, "pe": 29.46, "fwd_pe": 26.2, "pb": 8.53, "div_yield": 2.80, "roe": 29.8},
    {"symbol": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure & Capital Goods", "cmp": 3680.0, "eps": 112.00, "bvps": 640.0, "pe": 32.85, "fwd_pe": 28.5, "pb": 5.75, "div_yield": 0.95, "roe": 17.6},
    {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Public Sector Banking", "cmp": 845.0, "eps": 76.50, "bvps": 470.0, "pe": 11.04, "fwd_pe": 9.5, "pb": 1.80, "div_yield": 1.65, "roe": 16.5},
    {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical", "sector": "Pharmaceuticals", "cmp": 1885.0, "eps": 45.00, "bvps": 280.0, "pe": 41.88, "fwd_pe": 35.2, "pb": 6.73, "div_yield": 0.80, "roe": 16.8}
]

MID_CAP_FUNDAMENTALS = [
    {"symbol": "FEDERALBNK.NS", "name": "Federal Bank", "sector": "Private Banking", "cmp": 195.0, "eps": 21.50, "bvps": 145.0, "pe": 9.07, "fwd_pe": 8.1, "pb": 1.34, "div_yield": 1.25, "roe": 14.8},
    {"symbol": "PERSISTENT.NS", "name": "Persistent Systems", "sector": "IT Services", "cmp": 5280.0, "eps": 148.00, "bvps": 580.0, "pe": 35.68, "fwd_pe": 30.5, "pb": 9.10, "div_yield": 0.95, "roe": 26.4},
    {"symbol": "POLYCAB.NS", "name": "Polycab India", "sector": "Cables & Electricals", "cmp": 6850.0, "eps": 135.00, "bvps": 540.0, "pe": 50.74, "fwd_pe": 42.0, "pb": 12.68, "div_yield": 0.45, "roe": 26.8},
    {"symbol": "CUMMINSIND.NS", "name": "Cummins India", "sector": "Engineering & Engines", "cmp": 3740.0, "eps": 82.00, "bvps": 390.0, "pe": 45.61, "fwd_pe": 38.4, "pb": 9.59, "div_yield": 0.85, "roe": 22.5},
    {"symbol": "ASHOKLEY.NS", "name": "Ashok Leyland", "sector": "Commercial Vehicles", "cmp": 228.0, "eps": 11.80, "bvps": 45.0, "pe": 19.32, "fwd_pe": 16.5, "pb": 5.07, "div_yield": 2.15, "roe": 27.1},
    {"symbol": "VOLTAS.NS", "name": "Voltas Ltd", "sector": "Consumer Durables", "cmp": 1750.0, "eps": 24.00, "bvps": 180.0, "pe": 72.92, "fwd_pe": 55.0, "pb": 9.72, "div_yield": 0.40, "roe": 13.5},
    {"symbol": "DIXON.NS", "name": "Dixon Technologies", "sector": "EMS & Electronics", "cmp": 13400.0, "eps": 98.00, "bvps": 380.0, "pe": 136.73, "fwd_pe": 95.0, "pb": 35.26, "div_yield": 0.10, "roe": 27.5},
    {"symbol": "ASTRAL.NS", "name": "Astral Ltd", "sector": "Building Materials", "cmp": 1980.0, "eps": 24.50, "bvps": 145.0, "pe": 80.82, "fwd_pe": 62.0, "pb": 13.65, "div_yield": 0.25, "roe": 18.2},
    {"symbol": "COFORGE.NS", "name": "Coforge Ltd", "sector": "IT Solutions", "cmp": 7200.0, "eps": 185.00, "bvps": 710.0, "pe": 38.92, "fwd_pe": 32.0, "pb": 10.14, "div_yield": 1.10, "roe": 27.8},
    {"symbol": "SUPREMEIND.NS", "name": "Supreme Industries", "sector": "Plastics & Industrial", "cmp": 5150.0, "eps": 115.00, "bvps": 460.0, "pe": 44.78, "fwd_pe": 38.2, "pb": 11.19, "div_yield": 0.65, "roe": 26.2}
]

SMALL_CAP_FUNDAMENTALS = [
    {"symbol": "CDSL.NS", "name": "Central Depository Services", "sector": "Capital Markets Tech", "cmp": 1560.0, "eps": 42.00, "bvps": 165.0, "pe": 37.14, "fwd_pe": 31.0, "pb": 9.45, "div_yield": 1.40, "roe": 27.5},
    {"symbol": "BSE.NS", "name": "BSE Ltd", "sector": "Securities Exchange", "cmp": 4250.0, "eps": 95.00, "bvps": 310.0, "pe": 44.74, "fwd_pe": 36.5, "pb": 13.71, "div_yield": 0.85, "roe": 33.2},
    {"symbol": "KNRCON.NS", "name": "KNR Constructions", "sector": "Infrastructure & EPC", "cmp": 335.0, "eps": 28.50, "bvps": 155.0, "pe": 11.75, "fwd_pe": 10.2, "pb": 2.16, "div_yield": 0.35, "roe": 19.5},
    {"symbol": "SONATSOFTW.NS", "name": "Sonata Software", "sector": "IT & Cloud Services", "cmp": 640.0, "eps": 22.00, "bvps": 55.0, "pe": 29.09, "fwd_pe": 24.5, "pb": 11.63, "div_yield": 1.55, "roe": 42.1},
    {"symbol": "PRAJIND.NS", "name": "Praj Industries", "sector": "Bio-Energy Engineering", "cmp": 745.0, "eps": 18.50, "bvps": 85.0, "pe": 40.27, "fwd_pe": 33.0, "pb": 8.76, "div_yield": 0.70, "roe": 22.8},
    {"symbol": "CENTURYPLY.NS", "name": "Century Plyboards", "sector": "Building Materials", "cmp": 810.0, "eps": 21.00, "bvps": 115.0, "pe": 38.57, "fwd_pe": 32.5, "pb": 7.04, "div_yield": 0.25, "roe": 18.9},
    {"symbol": "RADICO.NS", "name": "Radico Khaitan", "sector": "Beverages & Distilleries", "cmp": 2180.0, "eps": 28.00, "bvps": 195.0, "pe": 77.86, "fwd_pe": 58.0, "pb": 11.18, "div_yield": 0.20, "roe": 15.2},
    {"symbol": "EQUITASBNK.NS", "name": "Equitas Small Finance Bank", "sector": "Small Finance Banking", "cmp": 92.0, "eps": 8.40, "bvps": 58.0, "pe": 10.95, "fwd_pe": 9.2, "pb": 1.58, "div_yield": 1.10, "roe": 15.4},
    {"symbol": "KARURVYSYA.NS", "name": "Karur Vysya Bank", "sector": "Commercial Banking", "cmp": 215.0, "eps": 24.00, "bvps": 148.0, "pe": 8.96, "fwd_pe": 7.8, "pb": 1.45, "div_yield": 1.95, "roe": 16.8},
    {"symbol": "CAMS.NS", "name": "Computer Age Management Services", "sector": "Fintech Services", "cmp": 4450.0, "eps": 88.00, "bvps": 215.0, "pe": 50.57, "fwd_pe": 41.0, "pb": 20.70, "div_yield": 1.05, "roe": 43.5}
]


class GrahamValuationsEngine:
    def __init__(self):
        pass

    def evaluate_stock_graham(self, stock: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates Benjamin Graham's valuation norms for a single stock."""
        cmp = stock["cmp"]
        eps = stock["eps"]
        bvps = stock["bvps"]
        pe = stock["pe"]
        pb = stock["pb"]

        # 1. Graham Number: sqrt(22.5 * EPS * BVPS)
        if eps > 0 and bvps > 0:
            graham_number = round(math.sqrt(22.5 * eps * bvps), 2)
            margin_of_safety_pct = round(((graham_number - cmp) / cmp) * 100, 2)
        else:
            graham_number = 0.0
            margin_of_safety_pct = -100.0

        # 2. Graham Multiplier: P/E * P/B (Threshold: <= 22.5)
        graham_multiplier = round(pe * pb, 2)

        # 3. Graham Norms Assessment Verdict
        if graham_multiplier <= 22.5 and margin_of_safety_pct >= 0:
            verdict = "GRAHAM PASS (Value Bargain)"
            tone = "PASS"
        elif graham_multiplier <= 35.0:
            verdict = "FAIR VALUE (Quality Growth)"
            tone = "FAIR"
        elif graham_multiplier <= 75.0:
            verdict = "ELEVATED MULTIPLE (Growth Premium)"
            tone = "CAUTION"
        else:
            verdict = "FROTHY / SPECULATIVE (Exceeds Norms)"
            tone = "FAIL"

        return {
            **stock,
            "graham_number": graham_number,
            "graham_multiplier": graham_multiplier,
            "margin_of_safety_pct": margin_of_safety_pct,
            "graham_pass": (graham_multiplier <= 22.5),
            "graham_verdict": verdict,
            "graham_tone": tone
        }

    def evaluate_tier(self, stocks: List[Dict[str, Any]], tier_name: str) -> Dict[str, Any]:
        """Evaluates an entire market capitalization tier."""
        assessed_stocks = [self.evaluate_stock_graham(s) for s in stocks]

        avg_pe = round(sum(s["pe"] for s in assessed_stocks) / len(assessed_stocks), 2)
        avg_pb = round(sum(s["pb"] for s in assessed_stocks) / len(assessed_stocks), 2)
        avg_multiplier = round(sum(s["graham_multiplier"] for s in assessed_stocks) / len(assessed_stocks), 2)
        avg_roe = round(sum(s["roe"] for s in assessed_stocks) / len(assessed_stocks), 2)
        pass_count = sum(1 for s in assessed_stocks if s["graham_pass"])

        return {
            "tier_name": tier_name,
            "stock_count": len(assessed_stocks),
            "average_pe": avg_pe,
            "average_pb": avg_pb,
            "average_graham_multiplier": avg_multiplier,
            "average_roe": avg_roe,
            "graham_pass_count": pass_count,
            "graham_pass_pct": round((pass_count / len(assessed_stocks)) * 100, 1),
            "stocks": assessed_stocks
        }

    def get_full_graham_assessment(self) -> Dict[str, Any]:
        """Provides the complete 3-tier Benjamin Graham Valuation Dataset."""
        large_tier = self.evaluate_tier(LARGE_CAP_FUNDAMENTALS, "Top 10 Large Cap Stocks")
        mid_tier = self.evaluate_tier(MID_CAP_FUNDAMENTALS, "Top 10 Mid Cap Stocks")
        small_tier = self.evaluate_tier(SMALL_CAP_FUNDAMENTALS, "Top 10 Small Cap Stocks")

        total_stocks = large_tier["stock_count"] + mid_tier["stock_count"] + small_tier["stock_count"]
        total_pass = large_tier["graham_pass_count"] + mid_tier["graham_pass_count"] + small_tier["graham_pass_count"]

        # Graham Value Champions (Stocks that passed Benjamin Graham's 22.5 multiplier threshold)
        all_stocks = large_tier["stocks"] + mid_tier["stocks"] + small_tier["stocks"]
        graham_champions = sorted([s for s in all_stocks if s["graham_pass"]], key=lambda x: x["graham_multiplier"])

        summary = (
            f"Benjamin Graham Norms Assessment across 30 marquee Indian stocks (10 Large, 10 Mid, 10 Small Cap): "
            f"Large Cap Avg P/E: {large_tier['average_pe']}x (P/B {large_tier['average_pb']}x), "
            f"Mid Cap Avg P/E: {mid_tier['average_pe']}x (P/B {mid_tier['average_pb']}x), "
            f"Small Cap Avg P/E: {small_tier['average_pe']}x (P/B {small_tier['average_pb']}x). "
            f"{total_pass} of 30 stocks strictly satisfy Graham's classical multiplier threshold (P/E * P/B <= 22.5). "
            f"Top Graham Value picks: {', '.join([c['name'] + ' (' + str(c['graham_multiplier']) + ')' for c in graham_champions[:4]])}."
        )

        tier_summaries = {
            "large_cap": {
                "avg_pe": large_tier["average_pe"],
                "avg_pb": large_tier["average_pb"],
                "graham_pass_count": large_tier["graham_pass_count"],
                "frothy_count": sum(1 for s in large_tier["stocks"] if s["graham_verdict"] == "FROTHY"),
            },
            "mid_cap": {
                "avg_pe": mid_tier["average_pe"],
                "avg_pb": mid_tier["average_pb"],
                "graham_pass_count": mid_tier["graham_pass_count"],
                "frothy_count": sum(1 for s in mid_tier["stocks"] if s["graham_verdict"] == "FROTHY"),
            },
            "small_cap": {
                "avg_pe": small_tier["average_pe"],
                "avg_pb": small_tier["average_pb"],
                "graham_pass_count": small_tier["graham_pass_count"],
                "frothy_count": sum(1 for s in small_tier["stocks"] if s["graham_verdict"] == "FROTHY"),
            }
        }

        return {
            "summary": summary,
            "total_stocks_assessed": total_stocks,
            "total_graham_qualifiers": total_pass,
            "large_cap": large_tier["stocks"],
            "mid_cap": mid_tier["stocks"],
            "small_cap": small_tier["stocks"],
            "large_cap_tier": large_tier,
            "mid_cap_tier": mid_tier,
            "small_cap_tier": small_tier,
            "tier_summaries": tier_summaries,
            "graham_value_champions": graham_champions
        }
