"""
Agent 2: EXPLORER (The Global Macro Navigator)
- Monitors international market trends:
  * USA: Dow Jones Industrial Average & NASDAQ Composite
  * Asia: Nikkei 225 (Japan), KOSPI (South Korea), Singapore STI
- Evaluates overnight closes and morning Asian momentum
- Projects the expected directional movement and point ranges for NIFTY 50 and SENSEX
"""

from typing import Dict, List, Any
from datetime import datetime

from data_engine.global_markets import GlobalMarketsEngine


class ExplorerAgent:
    def __init__(self):
        self.name = "Explorer"
        self.role = "Global Macro & Benchmark Trend Evaluator"
        self.engine = GlobalMarketsEngine()

    def run_investigation(self) -> Dict[str, Any]:
        return self.run_exploration()

    def run_exploration(self) -> Dict[str, Any]:
        """Analyzes 9 global trends, validates broker predictions, computes Graham norms, and checks interest rates."""
        impact_analysis = self.engine.evaluate_global_impact()

        score = impact_analysis["global_score"]
        bias = impact_analysis["directional_bias"]
        comp = impact_analysis["indian_vs_global_15d_comparison"]
        brokers = impact_analysis["broker_predictions"]
        graham = impact_analysis["graham_valuations"]
        bonds = impact_analysis["interest_rates_and_bonds"]

        summary = (
            f"Explorer evaluated 9 global indices across US (DOW, NASDAQ), Asia (Nikkei 225, KOSPI, STI, Hang Seng), "
            f"and Europe (CAC 40, DAX, FTSE 100) over 15 days. Global Score: {score}/100 ('{bias}'). "
            f"15-Day Validation: Indian indices ({comp['indian_avg_15d_return_pct']}%) vs Global 9 ({comp['global_9_indices_weighted_15d_return_pct']}%) -> {comp['validation_status']}. "
            f"Broker Consensus: {brokers['consensus_direction']} (Target Nifty {brokers['consensus_nifty_target']}), Validation: {brokers['validation_status']}. "
            f"Benjamin Graham Norms: Pass count L-Cap ({graham['tier_summaries']['large_cap']['graham_pass_count']}/10), "
            f"M-Cap ({graham['tier_summaries']['mid_cap']['graham_pass_count']}/10), S-Cap ({graham['tier_summaries']['small_cap']['graham_pass_count']}/10). "
            f"Central Bank Policy: US Fed {bonds['central_banks']['US Federal Reserve']['current_rate']} ({bonds['central_banks']['US Federal Reserve']['cycle_stage']}), "
            f"RBI {bonds['central_banks']['Reserve Bank of India (RBI)']['current_rate']} ({bonds['central_banks']['Reserve Bank of India (RBI)']['stance']} stance). "
            f"US-India 10Y Yield Spread: {bonds['us_india_spread_bps']} bps."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "global_composite_score": score,
            "directional_bias": bias,
            "composite_day_momentum": impact_analysis["composite_day_momentum"],
            "composite_week_momentum": impact_analysis["composite_week_momentum"],
            "composite_15d_momentum": impact_analysis["composite_15d_momentum"],
            "nifty_projection": impact_analysis["nifty_projection"],
            "sensex_projection": impact_analysis["sensex_projection"],
            "recommendation_note": impact_analysis["recommendation_note"],
            "tracked_markets": impact_analysis["indices_tracked"],
            "indian_vs_global_15d_comparison": comp,
            "broker_predictions": brokers,
            "graham_valuations": graham,
            "interest_rates_and_bonds": bonds,
            "summary": summary
        }

    def run_investigation(self) -> Dict[str, Any]:
        return self.run_exploration()

    def run(self) -> Dict[str, Any]:
        return self.run_exploration()
