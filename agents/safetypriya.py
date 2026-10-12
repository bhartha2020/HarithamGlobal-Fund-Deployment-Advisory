"""
Agent 4: SAFETYPRIYA (The Capital Preservation & Mutual Fund Specialist)
- Evaluates Mutual Fund schemes across 4 categories: Equity, Debt, Hybrid, and Liquid
- Covers 5 mandated AMCs: ICICI Prudential, Kotak Mahindra, Tata, JioBlackRock, and HDFC
- Tracks last 15 days & 1 week NAV movements
- Compares with Fixed Deposit (FD) yields to evaluate risk-adjusted return hurdle
"""

from typing import Dict, List, Any
from datetime import datetime

from data_engine.mutual_funds import MutualFundsEngine
from data_engine.fd_benchmarks import FDBenchmarkEngine


class SafetyPriyaAgent:
    def __init__(self):
        self.name = "SafetyPriya"
        self.role = "Capital Preservation & Mutual Fund Specialist"
        self.mf_engine = MutualFundsEngine()
        self.fd_engine = FDBenchmarkEngine()

    def run_safety_analysis(self) -> Dict[str, Any]:
        """Analyzes 15-day and 1-week NAVs across AMC portfolios and compares with FDs."""
        mf_results = self.mf_engine.analyze_all_funds()
        fd_rates = self.fd_engine.get_fd_rates()
        top_fd = self.fd_engine.get_highest_fd_rate()

        # Select top performing fund from each category based on 15d & 1w NAV momentum
        top_by_category = {}
        for category, funds in mf_results["by_category"].items():
            if funds:
                top_by_category[category] = funds[0]  # Already sorted by 15-day return

        # Formulate top MF selections
        best_equity = top_by_category.get("Equity")
        best_hybrid = top_by_category.get("Hybrid")
        best_debt = top_by_category.get("Debt")
        best_liquid = top_by_category.get("Liquid")

        # Rationale for capital safety
        summary = (
            f"SafetyPriya screened 20 Mutual Fund options across ICICI Prudential, Kotak Mahindra, "
            f"Tata, JioBlackRock, and HDFC across Equity, Debt, Hybrid, and Liquid categories. "
            f"15-Day and 1-Week NAV movements reviewed. "
            f"Best performers: Equity ({best_equity['amc']} - {best_equity['fifteen_chg_pct']}% 15D), "
            f"Hybrid ({best_hybrid['amc']} - {best_hybrid['fifteen_chg_pct']}% 15D), "
            f"Debt ({best_debt['amc']} - {best_debt['fifteen_chg_pct']}% 15D). "
            f"Benchmark Bank FD offering {top_fd['general_rate']}% p.a. provides an anchor for risk-free deployment."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "top_picks_by_category": top_by_category,
            "fd_benchmarks": fd_rates,
            "top_fd_recommendation": top_fd,
            "all_funds_analyzed": mf_results["all_funds"],
            "summary": summary
        }
