"""
Agent 3: GRIHALAXMI (The Institutional Capital Flow Sentinel)
- Compares the last 15 days cumulative Net Institutional Investment (NII) with
  the rolling 15 days cumulative investment database starting from 1st Jan 2023.
- Maintains persistent SQLite database (`data/grihalaxmi_flows.db`).
- At the end of each day, updates the database with the latest 15 days cumulative NII from today.
- When Multi-agent is run, compares the Cumulative NII value including today with
  the 15-day average of the Cumulative NIIs.
- Rule: If today's Cumulative NII value is less than the 15-day average,
  recommends investing in the Stock Market.
"""

from typing import Dict, List, Any
from datetime import datetime

from data_engine.nii_database import GrihaLaxmiDatabase


class GrihaLaxmiAgent:
    def __init__(self):
        self.name = "GrihaLaxmi"
        self.role = "Institutional Capital Flow Sentinel & NII Database Guardian"
        self.db = GrihaLaxmiDatabase()

    def run_flow_analysis(self) -> Dict[str, Any]:
        """
        Runs the full institutional flow analysis:
        1. Updates EOD data into SQLite DB
        2. Retrieves latest 15-day Cumulative NII including today
        3. Compares with the 15-day average of Cumulative NIIs
        4. Benchmarks against the rolling 15-day cumulative dataset from Jan 1, 2023
        5. Triggers stock market investment recommendation if flow is below average
        """
        comparison = self.db.get_latest_comparison()
        hist_stats = comparison["historical_benchmark_stats"]

        # Synthesize clear executive summary
        summary = (
            f"GrihaLaxmi Institutional Database Audit (From 1st Jan 2023 to Present: {hist_stats['total_trading_days']} trading days): "
            f"Today's 15-Day Cumulative NII = Rs. {comparison['today_cum_15d_nii']:,.2f} Cr. "
            f"15-Day Average of Cumulative NIIs = Rs. {comparison['avg_15d_cum_nii']:,.2f} Cr. "
            f"Condition 'Today Cumulative NII ({comparison['today_cum_15d_nii']:,.2f}) < 15-Day Average ({comparison['avg_15d_cum_nii']:,.2f})': "
            f"{comparison['is_below_15_day_avg']}. "
            f"Historical Percentile since Jan 2023: {hist_stats['today_percentile_rank']}%. "
            f"Recommendation: {comparison['recommendation']}."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trade_date": comparison["trade_date"],
            "today_fii_net": comparison["today_fii_net"],
            "today_dii_net": comparison["today_dii_net"],
            "today_daily_nii": comparison["today_daily_nii"],
            "today_cum_15d_nii": comparison["today_cum_15d_nii"],
            "avg_15d_cum_nii": comparison["avg_15d_cum_nii"],
            "diff_from_avg": comparison["diff_from_avg"],
            "spread_pct": comparison["spread_pct"],
            "is_below_15_day_avg": comparison["is_below_15_day_avg"],
            "recommend_stock_market": comparison["is_below_15_day_avg"],
            "status_tag": comparison["status_tag"],
            "action_code": comparison["action_code"],
            "confidence": comparison["confidence"],
            "rationale": comparison["rationale"],
            "summary": summary,
            "historical_benchmark_stats": hist_stats,
            "recent_15_trading_days": comparison["recent_15_trading_days"],
            # Backward-compatible fields for existing CLI / Buddhiman interfaces
            "cumulative_fii_cr": round(sum(d["fii_net"] for d in comparison["recent_15_trading_days"]), 2),
            "cumulative_dii_cr": round(sum(d["dii_net"] for d in comparison["recent_15_trading_days"]), 2),
            "cumulative_net_cr": comparison["today_cum_15d_nii"],
            "fifteen_day_avg_cr": comparison["avg_15d_cum_nii"],
            "latest_flow_cr": comparison["today_daily_nii"],
            "daily_series": [
                {
                    "date": d["trade_date"],
                    "fii_net": d["fii_net"],
                    "dii_net": d["dii_net"],
                    "net_total": d["daily_nii"]
                }
                for d in comparison["recent_15_trading_days"]
            ]
        }

    def update_eod_flow_database(self) -> Dict[str, Any]:
        """Explicitly triggers End-of-Day database update."""
        return self.db.update_eod_data()

    def run(self) -> Dict[str, Any]:
        return self.run_flow_analysis()
