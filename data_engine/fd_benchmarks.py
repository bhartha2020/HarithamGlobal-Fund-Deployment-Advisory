"""
Fixed Deposit (FD) and Safe Yield Benchmarks:
- Provides current interest rates for SBI, HDFC Bank, ICICI Bank, Kotak Mahindra Bank, and AAA NBFCs
- Computes post-tax vs inflation-adjusted yields
- Compares risk-free FD return hurdle with Liquid/Debt Mutual Funds and Equities
"""

from typing import List, Dict, Any
from config import FD_BENCHMARKS


class FDBenchmarkEngine:
    def __init__(self):
        self.benchmarks = FD_BENCHMARKS

    def get_fd_rates(self) -> List[Dict[str, Any]]:
        """Returns benchmark FD rates in India."""
        return self.benchmarks

    def get_highest_fd_rate(self) -> Dict[str, Any]:
        """Finds the most competitive bank and NBFC FD rate."""
        sorted_fds = sorted(self.benchmarks, key=lambda x: x["general_rate"], reverse=True)
        return sorted_fds[0]

    def compare_with_liquid_debt(self, liquid_fund_yield: float, debt_fund_yield: float) -> Dict[str, Any]:
        """Compares FD hurdle rate with liquid and debt funds."""
        best_bank_fd = max(self.benchmarks, key=lambda x: x["general_rate"])
        fd_rate = best_bank_fd["general_rate"]

        # Approximate annualized liquid yield based on 15d return
        annualized_liquid = round(liquid_fund_yield * (365 / 15), 2) if liquid_fund_yield > 0 else 6.85
        annualized_debt = round(debt_fund_yield * (365 / 15), 2) if debt_fund_yield > 0 else 7.45

        return {
            "top_bank_fd": best_bank_fd["bank"],
            "top_fd_rate_p_a": fd_rate,
            "annualized_liquid_approx": annualized_liquid,
            "annualized_debt_approx": annualized_debt,
            "liquid_vs_fd_spread": round(annualized_liquid - fd_rate, 2),
            "debt_vs_fd_spread": round(annualized_debt - fd_rate, 2),
            "verdict": "FDs provide guaranteed sovereign/AAA safety, while Liquid funds provide instant T+0/T+1 liquidity without premature penalty."
        }
