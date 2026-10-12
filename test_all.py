"""
Comprehensive test suite verifying all 5 agents and their data engines.
"""

import unittest
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from data_engine.news_fetcher import NewsFetcher
from data_engine.market_data import MarketDataEngine
from data_engine.block_deals import BlockDealsEngine
from data_engine.global_markets import GlobalMarketsEngine
from data_engine.institutional_flows import InstitutionalFlowsEngine
from data_engine.mutual_funds import MutualFundsEngine
from data_engine.fd_benchmarks import FDBenchmarkEngine
from data_engine.corporate_bonds import CorporateBondsEngine

from agents.jasoos import JasoosAgent
from agents.explorer import ExplorerAgent
from agents.grihalaxmi import GrihaLaxmiAgent
from agents.safetypriya import SafetyPriyaAgent
from agents.stock_bull import StockBullAgent
from agents.mf_hussain import MFHussainAgent
from agents.fd_lover import FDLoverAgent
from agents.buddhiman import BuddhimanAgent
from agents.chitragupthan import ChitragupthanAgent


class Test5AgentAdvisorySystem(unittest.TestCase):

    def test_block_deals_engine(self):
        engine = BlockDealsEngine()
        result = engine.get_top_15_block_deals(window_days=10)
        self.assertEqual(result["window_days"], 10)
        self.assertIn("Previous 10 Days", result["surveillance_window"])
        self.assertGreater(result["total_deals_scanned"], 0)
        self.assertEqual(len(result["top_15_block_deals"]), 15)
        self.assertGreater(result["top_15_deal_value_cr"], 0)
        self.assertIn("deal_value_cr", result["top_15_block_deals"][0])
        self.assertIn("client_name", result["top_15_block_deals"][0])
        self.assertIn("trade_date", result["top_15_block_deals"][0])

    def test_news_fetcher(self):
        fetcher = NewsFetcher()
        sentiment = fetcher.analyze_sentiment("Company announces massive record profit and capex surge")
        self.assertGreater(sentiment, 0.0)
        neg_sentiment = fetcher.analyze_sentiment("Company suffers deep loss and revenue plunge")
        self.assertLess(neg_sentiment, 0.0)
        self.assertTrue(fetcher.check_big_ticket("Block deal reported worth 5000 crore expansion"))

    def test_global_markets_engine(self):
        engine = GlobalMarketsEngine()
        result = engine.evaluate_global_impact()
        self.assertIn("global_score", result)
        self.assertIn("directional_bias", result)
        self.assertEqual(len(result["indices_tracked"]), 9)
        self.assertIn("broker_predictions", result)
        self.assertIn("graham_valuations", result)
        self.assertIn("interest_rates_and_bonds", result)
        self.assertIn("indian_vs_global_15d_comparison", result)
        
        comp = result["indian_vs_global_15d_comparison"]
        self.assertIn("nifty_15d_return_pct", comp)
        self.assertIn("global_9_indices_weighted_15d_return_pct", comp)
        self.assertIn("validation_status", comp)

    def test_broker_predictions_engine(self):
        from data_engine.broker_predictions import BrokerPredictionsEngine
        engine = BrokerPredictionsEngine()
        res = engine.evaluate_broker_predictions(global_score=25.0, global_bias="Moderately Bullish")
        self.assertGreaterEqual(res["broker_count"], 8)
        self.assertIn("consensus_nifty_target", res)
        self.assertIn("consensus_sensex_target", res)
        self.assertIn("validation_status", res)
        self.assertIn("validation_rationale", res)

    def test_graham_valuations_engine(self):
        from data_engine.graham_valuations import GrahamValuationsEngine
        engine = GrahamValuationsEngine()
        res = engine.get_full_graham_assessment()
        self.assertEqual(len(res["large_cap"]), 10)
        self.assertEqual(len(res["mid_cap"]), 10)
        self.assertEqual(len(res["small_cap"]), 10)
        self.assertIn("tier_summaries", res)
        for tier in ["large_cap", "mid_cap", "small_cap"]:
            self.assertIn("graham_pass_count", res["tier_summaries"][tier])
            self.assertIn("avg_pe", res["tier_summaries"][tier])

    def test_interest_rates_and_bonds_engine(self):
        from data_engine.interest_rates_bonds import InterestRatesBondsEngine
        engine = InterestRatesBondsEngine()
        res = engine.evaluate_interest_rates_and_bonds()
        self.assertIn("central_banks", res)
        self.assertIn("US Federal Reserve", res["central_banks"])
        self.assertIn("Reserve Bank of India (RBI)", res["central_banks"])
        self.assertIn("bond_yields", res)
        self.assertGreaterEqual(len(res["bond_yields"]), 5)
        self.assertIn("us_india_spread_bps", res)

    def test_explorer_agent(self):
        agent = ExplorerAgent()
        res = agent.run_exploration()
        self.assertIn("global_composite_score", res)
        self.assertIn("nifty_projection", res)
        self.assertIn("sensex_projection", res)
        self.assertEqual(len(res["tracked_markets"]), 9)
        self.assertIn("broker_predictions", res)
        self.assertIn("graham_valuations", res)
        self.assertIn("interest_rates_and_bonds", res)
        self.assertIn("indian_vs_global_15d_comparison", res)

    def test_grihalaxmi_agent(self):
        from data_engine.nii_database import GrihaLaxmiDatabase
        db = GrihaLaxmiDatabase()
        comparison = db.get_latest_comparison()
        self.assertIn("today_cum_15d_nii", comparison)
        self.assertIn("avg_15d_cum_nii", comparison)
        self.assertIn("is_below_15_day_avg", comparison)
        self.assertGreaterEqual(comparison["historical_benchmark_stats"]["total_trading_days"], 900)
        self.assertEqual(comparison["historical_benchmark_stats"]["dataset_start_date"], "2023-01-02")
        
        agent = GrihaLaxmiAgent()
        res = agent.run_flow_analysis()
        self.assertIn("today_cum_15d_nii", res)
        self.assertIn("avg_15d_cum_nii", res)
        self.assertIsInstance(res["recommend_stock_market"], bool)
        self.assertEqual(res["recommend_stock_market"], res["is_below_15_day_avg"])

    def test_safetypriya_agent(self):
        agent = SafetyPriyaAgent()
        res = agent.run_safety_analysis()
        self.assertIn("Hybrid", res["top_picks_by_category"])
        self.assertIn("top_fd_recommendation", res)

    def test_corporate_bonds_engine(self):
        engine = CorporateBondsEngine()
        top_5 = engine.get_top_5_fixed_income_options()
        self.assertEqual(len(top_5), 5)
        self.assertGreaterEqual(top_5[0]["annual_interest_rate"], 8.0)
        all_instruments = engine.get_all_options()
        self.assertGreaterEqual(len(all_instruments), 8)

    def test_stock_bull_agent(self):
        agent = StockBullAgent()
        res = agent.evaluate()
        self.assertIn("core_arguments_for_100_percent", res)
        self.assertEqual(len(res["core_arguments_for_100_percent"]), 5)
        self.assertEqual(len(res["curated_picks"]), 5)
        total_weight = sum(s["recommended_weight_pct"] for s in res["curated_picks"])
        self.assertEqual(total_weight, 100)
        self.assertEqual(res["recommended_asset_allocation"]["Stocks"], 100)

    def test_mf_hussain_agent(self):
        agent = MFHussainAgent()
        res = agent.evaluate()
        self.assertIn("core_arguments_for_100_percent", res)
        self.assertEqual(len(res["core_arguments_for_100_percent"]), 5)
        self.assertEqual(len(res["curated_picks"]), 5)
        total_weight = sum(m["recommended_weight_pct"] for m in res["curated_picks"])
        self.assertEqual(total_weight, 100)
        self.assertEqual(res["recommended_asset_allocation"]["Mutual_Funds"], 100)

    def test_fd_lover_agent(self):
        agent = FDLoverAgent()
        res = agent.evaluate()
        self.assertIn("core_arguments_for_100_percent", res)
        self.assertEqual(len(res["core_arguments_for_100_percent"]), 5)
        self.assertLessEqual(len(res["curated_picks"]), 5)
        total_weight = sum(f["recommended_weight_pct"] for f in res["curated_picks"])
        self.assertEqual(total_weight, 100)
        self.assertEqual(res["recommended_asset_allocation"]["Fixed_Deposits"], 100)
        self.assertGreaterEqual(res["blended_annual_yield_pct"], 7.5)

    def test_buddhiman_agent(self):
        agent = BuddhimanAgent()
        res = agent.synthesize_all_agents()
        
        # Verify Council of Advocates integration
        self.assertIn("council_of_advocates", res)
        council = res["council_of_advocates"]
        self.assertIn("stock_bull", council)
        self.assertIn("mf_hussain", council)
        self.assertIn("fd_lover", council)
        self.assertIn("arbitration_verdict", council)
        
        # Verify 5 picks
        self.assertEqual(len(res["five_actionable_picks"]), 5)
        
        # Verify weights sum to 100%
        alloc = res["allocation_percentages"]
        total_alloc = sum(alloc.values())
        self.assertEqual(total_alloc, 100)
        
        # Verify pick weights sum to 100%
        pick_weights_sum = sum(p["recommended_weight_pct"] for p in res["five_actionable_picks"])
        self.assertEqual(pick_weights_sum, 100)

        # Verify that pick weights by category strictly equal allocation_percentages
        category_pick_sums = {
            "Stocks": sum(p["recommended_weight_pct"] for p in res["five_actionable_picks"] if "Stock" in p["type"]),
            "Mutual_Funds": sum(p["recommended_weight_pct"] for p in res["five_actionable_picks"] if "Mutual Fund" in p["type"]),
            "ETFs": sum(p["recommended_weight_pct"] for p in res["five_actionable_picks"] if "ETF" in p["type"]),
            "Fixed_Deposits": sum(p["recommended_weight_pct"] for p in res["five_actionable_picks"] if "Fixed Deposit" in p["type"]),
        }
        for cat, expected in alloc.items():
            self.assertEqual(
                category_pick_sums.get(cat, 0),
                expected,
                f"Discrepancy in {cat}: expected {expected}%, got {category_pick_sums.get(cat, 0)}%"
            )
        
        # Verify dates
        self.assertIn("friday_recommendation_date", res["dates"])
        self.assertIn("upcoming_monday_action_date", res["dates"])
        self.assertIn("Friday", res["dates"]["friday_recommendation_date"])
        self.assertIn("Monday", res["dates"]["upcoming_monday_action_date"])

    def test_chitragupthan_simulation(self):
        agent = ChitragupthanAgent()
        self.assertEqual(agent.name, "Chitragupthan")

        # Test price parser
        self.assertEqual(agent.parse_numeric_price("Rs. 1,355.00"), 1355.0)
        self.assertEqual(agent.parse_numeric_price("NAV Rs. 11.20"), 11.2)
        self.assertEqual(agent.parse_numeric_price("8.6% p.a. (9.1% Seniors)"), 8.6)

        # Run simulation with standard ₹1,00,000 capital
        capital = 100000.0
        sim = agent.run_simulation(capital=capital)
        self.assertEqual(sim["agent_name"], "Chitragupthan")
        self.assertGreater(sim["total_predictions_simulated"], 0)

        # Audit each simulated prediction table
        for pred in sim["prediction_simulations"]:
            self.assertIn("prediction_date", pred)
            self.assertIn("execution_monday", pred)
            self.assertIn("table_rows", pred)
            self.assertGreater(len(pred["table_rows"]), 0)

            # Check required columns on each row
            for row in pred["table_rows"]:
                self.assertIn("instrument_name", row)
                self.assertIn("fund_value_prediction_date", row)
                self.assertIn("current_value", row)
                self.assertIn("pct_change", row)
                self.assertGreater(row["fund_value_prediction_date"], 0)
                self.assertGreater(row["current_value"], 0)

                # Verify % change calculation consistency
                expected_pct = round(((row["current_value"] - row["fund_value_prediction_date"]) / row["fund_value_prediction_date"]) * 100.0, 2)
                self.assertAlmostEqual(row["pct_change"], expected_pct, delta=0.05)

            # Check prediction portfolio summary
            summary = pred["summary"]
            self.assertAlmostEqual(summary["total_fund_value_prediction_date"], capital, delta=1.0)
            self.assertGreater(summary["total_current_value"], 0)
            self.assertIn("karma_verdict", summary)

    def test_sarathy_agent(self):
        from agents.sarathy import SarathyAgent
        agent = SarathyAgent()
        res = agent.run_assessment(capital=100000.0)
        self.assertIn("simulation_audit_report", res)
        self.assertIn("monday_web_intelligence", res)
        self.assertIn("improvement_recommendations", res)
        self.assertIn("viswakarma_delegation", res)

        audit = res["simulation_audit_report"]
        self.assertGreater(audit["total_picks_audited"], 0)
        self.assertIn("average_tracking_variance_pct", audit)
        self.assertGreaterEqual(len(audit["strategic_lessons_learned"]), 3)

        web = res["monday_web_intelligence"]
        self.assertGreaterEqual(len(web["recommended_websites"]), 4)
        self.assertIn("nifty_50_technical_setup", web["major_technical_analysis"])
        self.assertIn("gift_nifty_indication", web["monday_market_cues"])

        recs = res["improvement_recommendations"]
        self.assertIn("stock_bull_directives", recs)
        self.assertIn("mf_hussain_directives", recs)
        self.assertIn("fd_lover_directives", recs)
        self.assertIn("buddhiman_directives", recs)

    def test_viswakarma_agent(self):
        from agents.viswakarma import ViswakarmaAgent
        agent = ViswakarmaAgent()
        res = agent.run()
        self.assertIn("registry", res)
        reg = res["registry"]
        self.assertIn("active_patches", reg)
        patches = reg["active_patches"]
        self.assertIn("StockBull", patches)
        self.assertIn("MFHussain", patches)
        self.assertIn("FDLover", patches)
        self.assertIn("Buddhiman", patches)

        status = agent.get_latest_status()
        self.assertIn("version", status)
        self.assertIn("target_cycle", status)


if __name__ == "__main__":
    unittest.main()
