"""
Agent: FDLOVER (The Capital Preservation Champion & Fixed Income Strategist)
- Works under Buddhiman as the dedicated champion for Fixed Income, Fixed Deposits, and Bonds.
- Ingests reports from:
  * SafetyPriya: Bank FD benchmarks (SBI, HDFC Bank, ICICI Bank, Kotak Bank, Bajaj Finance).
  * Explorer: Global central bank policy rate trajectories (Fed easing, RBI neutral pivot, 10Y sovereign yields).
  * Corporate Bonds Engine: Scouts top AAA Corporate FDs, Bank FDs, and Corporate/PSU Bonds.
- Formulates rock-solid arguments for 100% investment in Fixed Deposits and Corporate Bonds.
- Recommends how to split 100% of the fresh funds into a maximum of 5 best options with peak yields and pristine credit ratings.
"""

from typing import Dict, List, Any
from datetime import datetime

from data_engine.corporate_bonds import CorporateBondsEngine
from data_engine.fd_benchmarks import FDBenchmarkEngine


class FDLoverAgent:
    def __init__(self):
        self.name = "FDLover"
        self.role = "Capital Preservation Champion & Fixed Income Strategist"
        self.mandate = "Scouts Best FDs & Corporate Bonds; Splits 100% of Funds across Maximum 5 Best Options"
        self.bonds_engine = CorporateBondsEngine()
        self.fd_engine = FDBenchmarkEngine()

    def evaluate(
        self,
        jasoos_report: Dict[str, Any] = None,
        explorer_report: Dict[str, Any] = None,
        grihalaxmi_report: Dict[str, Any] = None,
        safetypriya_report: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Scouts the best FD and corporate bond options, formulates arguments for 100% capital preservation,
        and splits 100% of fresh funds across the maximum 5 best options.
        """
        # Lazy imports if run standalone
        if jasoos_report is None:
            from agents.jasoos import JasoosAgent
            jasoos_report = JasoosAgent().run_investigation()
        if explorer_report is None:
            from agents.explorer import ExplorerAgent
            explorer_report = ExplorerAgent().run_exploration()
        if grihalaxmi_report is None:
            from agents.grihalaxmi import GrihaLaxmiAgent
            grihalaxmi_report = GrihaLaxmiAgent().run_flow_analysis()
        if safetypriya_report is None:
            from agents.safetypriya import SafetyPriyaAgent
            safetypriya_report = SafetyPriyaAgent().run_safety_analysis()

        # Retrieve scouted options
        top_5_options = self.bonds_engine.get_top_5_fixed_income_options()

        # Extract intelligence from upstream agents
        bonds_data = explorer_report.get("interest_rates_and_bonds", {})
        rbi_cb = bonds_data.get("central_banks", {}).get("Reserve Bank of India (RBI)", {})
        rbi_rate = rbi_cb.get("current_rate", "6.50%")
        rbi_stance = rbi_cb.get("stance", "Neutral")
        fed_cb = bonds_data.get("central_banks", {}).get("US Federal Reserve", {})
        fed_rate = fed_cb.get("current_rate", "4.75% - 5.00%")
        spread_bps = bonds_data.get("us_india_spread_bps", 270)
        global_score = explorer_report.get("global_composite_score", -18.1)
        graham = explorer_report.get("graham_valuations", {})
        graham_frothy = graham.get("tier_summaries", {}).get("large_cap", {}).get("frothy_count", 8)
        graham_pass = graham.get("tier_summaries", {}).get("large_cap", {}).get("graham_pass_count", 0)

        fii_flow = grihalaxmi_report.get("today_flow", {}).get("fii_net_cr", -3568.0)
        cum_percentile = grihalaxmi_report.get("historical_benchmark_stats", {}).get("today_percentile_rank", 11.7)

        deal_value_cr = jasoos_report.get("top_15_deal_value_cr", 17718.5)

        debt_mf = safetypriya_report.get("top_picks_by_category", {}).get("Debt", {})
        debt_15d = debt_mf.get("fifteen_chg_pct", 0.38)

        # Ingest active engineering modifications from Viswakarma (directed by Sarathy)
        viswakarma_patch = {}
        try:
            from agents.viswakarma import ViswakarmaAgent
            viswakarma_patch = ViswakarmaAgent().get_active_patches("FDLover")
        except Exception:
            pass

        # 1. Formulate Rock-Solid Arguments for 100% Fixed Income / FD / Bond Deployment synthesizing all 4 agents
        arguments_for_100_percent_fds = [
            (
                f"🔒 Lock In Peak Terminal Yields Before RBI Rate Cuts (Explorer Synthesis): Explorer confirms global "
                f"central banks are cutting rates aggressively (Fed {fed_rate} after -50 bps cut, ECB -75 bps) and RBI "
                f"({rbi_rate}) has officially pivoted its stance to '{rbi_stance}'. With the US-India yield spread compressed at "
                f"{spread_bps} bps, India is at the cyclical peak of terminal interest rates (8.10%–8.60% p.a.). Once RBI commences "
                f"repo rate reductions, deposit rates will collapse. Locking in 100% fresh funds into AAA corporate FDs and bonds today "
                f"secures generational guaranteed yields before rates drop."
            ),
            (
                f"🛡️ Shield Against Relentless FII Capital Flight (GrihaLaxmi Synthesis): GrihaLaxmi reveals that foreign "
                f"institutional investors dumped Rs. {abs(fii_flow):,.0f} Cr today alone, driving cumulative NII to the "
                f"{cum_percentile}th percentile. StockBull and MFHussain want to absorb this toxic FII selling with fresh retail "
                f"capital. FDLover refuses to catch falling knives: AAA Fixed Deposits and secured bonds offer 100% absolute capital "
                f"preservation with ZERO mark-to-market drawdown risk regardless of foreign flight."
            ),
            (
                f"⚠️ Extreme Equity Froth & Distribution Reality (Explorer & Jasoos Synthesis): Explorer's Graham assessment "
                f"revealed {graham_frothy}/10 large caps trade at dangerous bubble valuations with {graham_pass}/10 passing Graham "
                f"value norms. Concurrently, Jasoos tracked Rs. {deal_value_cr:,.1f} Cr in block deals characterized by heavy promoter "
                f"profit-taking and institutional churn. Equities are vulnerable to sharp multi-quarter mean reversion, while Explorer's "
                f"composite score sits deep in negative territory ({global_score}/100)."
            ),
            (
                f"💰 Guaranteed 8.03%–8.54% Yield vs Fee-Drained MFs (SafetyPriya Synthesis): SafetyPriya shows debt mutual "
                f"funds generated an underwhelming +{debt_15d}% over 15 days while exposing investors to duration volatility and "
                f"AMC expense deductions. In stark contrast, our curated AAA Corporate FDs (Shriram Finance 8.60%, L&T Finance 8.15%, "
                f"Bajaj Finance 8.10%) yield a blended 8.03% to 8.54% p.a. (up to 9.00% for senior citizens) legally guaranteed with "
                f"zero fees and zero volatility."
            ),
            (
                "🎯 Why 100% Fixed Income Demolishes StockBull & MFHussain: StockBull asks investors to gamble on unhedged "
                "single equities at all-time valuation highs; MFHussain offers fee-laden funds that still suffer equity beta crashes. "
                "Over 80% of retail investors fail to beat fixed deposits after adjusting for volatility and panic selling. 100% "
                "deployment into AAA Corporate FDs and Bank FDs delivers mathematically guaranteed compounding, DICGC insurance, "
                "and complete immunity to market crashes."
            )
        ]

        # 2. Recommend how to split 100% of the fund into maximum of 5 best options
        # Weights: 25%, 25%, 20%, 15%, 15% = 100%
        fd_weights = [25, 25, 20, 15, 15]
        curated_picks = []

        total_yield_accrual = 0.0
        total_senior_yield_accrual = 0.0

        for i, opt in enumerate(top_5_options[:5]):
            weight = fd_weights[i]
            curated_picks.append({
                "rank": i + 1,
                "issuer": opt["issuer"],
                "instrument_type": opt["instrument_type"],
                "credit_rating": opt["rating"],
                "recommended_weight_pct": weight,
                "annual_interest_rate_pct": opt["annual_interest_rate"],
                "senior_citizen_rate_pct": opt["senior_citizen_rate"],
                "tenure": opt["tenure"],
                "payout_frequency": opt["payout_frequency"],
                "security_type": opt["security_type"],
                "safety_rationale": opt["safety_rationale"]
            })
            total_yield_accrual += (opt["annual_interest_rate"] * weight) / 100.0
            total_senior_yield_accrual += (opt["senior_citizen_rate"] * weight) / 100.0

        # Verify weights sum to 100%
        assert sum(p["recommended_weight_pct"] for p in curated_picks) == 100, "Fixed income weights must sum to 100%"
        assert len(curated_picks) <= 5, "Must recommend maximum 5 options"

        blended_yield = round(total_yield_accrual, 2)
        blended_senior_yield = round(total_senior_yield_accrual, 2)

        summary = (
            f"FDLover Advocate Pitch: Strongly fights for 100% deployment into Fixed Deposits and Corporate Bonds, synthesizing cross-agent intelligence: "
            f"locking in peak terminal yields ({rbi_stance} at {rbi_rate}) before RBI rate cuts, shielding capital against GrihaLaxmi's Rs. {abs(fii_flow):,.0f} Cr FII dump, "
            f"avoiding Explorer's {graham_frothy}/10 Graham large-cap froth and Jasoos's Rs. {deal_value_cr:,.1f} Cr block deal distribution churn, "
            f"and outperforming SafetyPriya's debt MFs (+{debt_15d}%) with guaranteed blended {blended_yield}% p.a. yield ({blended_senior_yield}% Seniors). "
            f"Recommended 100% fund split across 5 premier options: "
            f"{', '.join([p['issuer'] + ' @ ' + str(p['annual_interest_rate_pct']) + '% (' + str(p['recommended_weight_pct']) + '%)' for p in curated_picks])}."
        )

        return {
            "advocate_name": self.name,
            "role": self.role,
            "mandate": self.mandate,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommended_asset_allocation": {"Stocks": 0, "Mutual_Funds": 0, "ETFs": 0, "Fixed_Deposits": 100},
            "core_arguments_for_100_percent": arguments_for_100_percent_fds,
            "curated_picks": curated_picks,
            "blended_annual_yield_pct": blended_yield,
            "blended_senior_yield_pct": blended_senior_yield,
            "risk_profile": "Zero Capital Risk (AAA / Sovereign / DICGC)",
            "engineering_enhancements_applied": viswakarma_patch,
            "summary": summary
        }

    def run(self) -> Dict[str, Any]:
        return self.evaluate()
