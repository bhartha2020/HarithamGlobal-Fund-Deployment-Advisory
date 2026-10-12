"""
Command-Line Interface (CLI) for the 5-Agent Indian Fund Deployment Advisory System.
Usage:
  py cli.py                     # Runs full Buddhiman multi-agent synthesis
  py cli.py --agent jasoos      # Runs only Jasoos (15 Big-Ticket Stocks + Press)
  py cli.py --agent explorer    # Runs only Explorer (Global Indices -> Nifty/Sensex)
  py cli.py --agent grihalaxmi  # Runs only GrihaLaxmi (FII/DII 15-day flows vs 15-DMA)
  py cli.py --agent safetypriya # Runs only SafetyPriya (MFs across 5 AMCs + FDs)
  py cli.py --export            # Runs synthesis and exports Friday-Monday dossier
"""

import sys
import argparse
import json

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from agents.jasoos import JasoosAgent
from agents.explorer import ExplorerAgent
from agents.grihalaxmi import GrihaLaxmiAgent
from agents.safetypriya import SafetyPriyaAgent
from agents.stock_bull import StockBullAgent
from agents.mf_hussain import MFHussainAgent
from agents.fd_lover import FDLoverAgent
from agents.buddhiman import BuddhimanAgent
from agents.chitragupthan import ChitragupthanAgent
from scheduler import FridayScheduler


def run_jasoos():
    print("\n" + "=" * 70)
    print("🕵️ AGENT 1: JASOOS - TOP 15 BLOCK DEALS (PREVIOUS 10 DAYS SURVEILLANCE)")
    print("=" * 70)
    agent = JasoosAgent()
    res = agent.run_investigation()
    print(f"Surveillance Window:                  {res.get('surveillance_window', 'Previous 10 Days')}")
    print(f"Total Block/Bulk Deals Scanned (10D): {res['total_block_deals_scanned']} (10-Day Turnover: Rs. {res['total_market_block_value_cr']:,.2f} Cr)")
    print(f"Top 15 Block Deals Value (10D):       Rs. {res['top_15_deal_value_cr']:,.2f} Cr")
    print(f"Largest Single Block Deal:            Rs. {res['largest_single_deal_cr']:,.2f} Cr")
    print(f"\nSummary: {res['summary']}\n")
    print(f"{'#':<3} {'Date':<12} {'Symbol':<12} {'Company':<20} {'Deal (Cr)':<12} {'Type':<6} {'Price (Rs)':<11} {'Vol Spike':<10} {'Score':<7} {'Verdict'}")
    print("-" * 125)
    for i, s in enumerate(res["all_15_stocks"], 1):
        print(f"{i:<3} {s.get('trade_date', 'Recent'):<12} {s['raw_symbol']:<12} {s['name'][:19]:<20} Rs.{s['deal_value_cr']:<9,.1f} {s['deal_type']:<6} {s['current_price']:<11.2f} {s['vol_ratio']:<10.2f} {s['jasoos_score']:<7.1f} {s['verdict']}")

    print("\n--- TOP HIGH-CONVICTION BLOCK DEAL PICKS ---")
    for s in res["top_stock_picks"]:
        print(f" * {s['name']} ({s['raw_symbol']}): Deal Rs. {s['deal_value_cr']:,.2f} Cr ({s['deal_type']} on {s.get('trade_date', 'recent')}) | Score {s['jasoos_score']}/100 | Client: {s['client_name'][:45]}")
        if s["headlines"]:
            print(f"   Headlines: \"{s['headlines'][0]}\"")


def run_explorer():
    print("\n" + "=" * 80)
    print("🌍 AGENT 2: EXPLORER - 9 GLOBAL INDICES, BROKER PREDICTIONS, GRAHAM NORMS & BOND YIELDS")
    print("=" * 80)
    agent = ExplorerAgent()
    res = agent.run_exploration()
    print(f"Global Composite Score:    {res['global_composite_score']}/100 ({res['directional_bias']})")
    print(f"Projected Nifty 50 Impact: {res['nifty_projection']['expected_bias']} (Ref: {res['nifty_projection']['current']})")
    print(f"Projected Sensex Impact:   {res['sensex_projection']['expected_bias']} (Ref: {res['sensex_projection']['current']})")
    print(f"Commentary: {res['recommendation_note']}\n")

    # 1. 9 Global Indices + 15-Day Performance
    print("--- 1. 9 GLOBAL INDICES (15-DAY, 1-WEEK, 1-DAY MOVEMENTS) ---")
    print(f"{'Index Name':<28} {'Region':<14} {'Price':<11} {'1-Day %':<9} {'1-Week %':<10} {'15-Day %':<10} {'15D Trend'}")
    print("-" * 92)
    for idx in res["tracked_markets"]:
        print(f"{idx['name'][:26]:<28} {idx['region']:<14} {idx['price']:<11.2f} {idx['day_change_pct']:<9.2f} {idx['week_ret_pct']:<10.2f} {idx['fifteen_ret_pct']:<10.2f} {idx['fifteen_trend']}")

    # 2. Indian Indices 15-Day Movement Comparison & Validation
    comp = res.get("indian_vs_global_15d_comparison", {})
    print("\n--- 2. 15-DAY MOVEMENT VALIDATION (INDIAN VS GLOBAL BENCHMARKS) ---")
    print(f"  NIFTY 50 15D Return:     {comp.get('nifty_15d_return_pct', 0):+0.2f}%")
    print(f"  SENSEX 15D Return:       {comp.get('sensex_15d_return_pct', 0):+0.2f}%")
    print(f"  Global 9 Weighted 15D:   {comp.get('global_9_indices_weighted_15d_return_pct', 0):+0.2f}%")
    print(f"  Decoupling Spread:       {comp.get('decoupling_spread_pct', 0):+0.2f}%")
    print(f"  Validation Verdict:      {comp.get('validation_status', 'N/A')}")
    print(f"  Rationale:               {comp.get('validation_rationale', 'N/A')}")

    # 3. Leading Stock Broker Predictions & Explorer Validation
    brokers = res.get("broker_predictions", {})
    print("\n--- 3. LEADING STOCK BROKER PREDICTIONS & EXPLORER VALIDATION ---")
    print(f"  Consensus Direction:     {brokers.get('consensus_direction', 'N/A')}")
    print(f"  Nifty Consensus Target:  {brokers.get('consensus_nifty_target', 'N/A')} (Range: {brokers.get('nifty_support_band', 'N/A')} - {brokers.get('nifty_resistance_band', 'N/A')})")
    print(f"  Sensex Consensus Target: {brokers.get('consensus_sensex_target', 'N/A')}")
    print(f"  Explorer Validation:     {brokers.get('validation_status', 'N/A')}")
    print(f"  Validation Rationale:    {brokers.get('validation_rationale', 'N/A')}")
    print(f"  Broker Breakdown:")
    for b in brokers.get("brokers", [])[:5]:
        b_stance = b.get("stance", b.get("directional_call", "Neutral"))
        print(f"   * {b['broker']:<20}: Nifty {b['nifty_target']:<7} | Stance: {b_stance:<12} | {b['rationale'][:45]}")

    # 4. Benjamin Graham Norms Assessment (Top 10 Large, Mid, Small Cap)
    graham = res.get("graham_valuations", {})
    tier_sums = graham.get("tier_summaries", {})
    print("\n--- 4. BENJAMIN GRAHAM VALUATION NORMS ASSESSMENT (30 STOCKS) ---")
    for tier_key, tier_label in [("large_cap", "Large Cap"), ("mid_cap", "Mid Cap"), ("small_cap", "Small Cap")]:
        ts = tier_sums.get(tier_key, {})
        print(f"  [{tier_label}] Avg P/E: {ts.get('avg_pe', 'N/A')} | Avg P/B: {ts.get('avg_pb', 'N/A')} | Graham Passes: {ts.get('graham_pass_count', 0)}/10 | Overvalued: {ts.get('frothy_count', 0)}/10")

    # 5. Global Central Banks & 10Y Sovereign Bond Market
    bonds = res.get("interest_rates_and_bonds", {})
    print("\n--- 5. GLOBAL CENTRAL BANKS POLICY RATES & 10Y SOVEREIGN BOND YIELDS ---")
    print(f"  US-India 10Y Yield Spread: {bonds.get('us_india_spread_bps', 0)} bps ({bonds.get('spread_assessment', 'N/A')})")
    print(f"  Key Central Bank Rates:")
    for cb_name, cb_data in bonds.get("central_banks", {}).items():
        print(f"   * {cb_name:<30}: {cb_data['current_rate']:<14} Stance: {cb_data['stance']:<12} ({cb_data['cycle_stage']})")
    print(f"  10Y Sovereign Bond Yields:")
    for b_item in bonds.get("bond_yields", []):
        print(f"   * {b_item['country']:<14} Yield: {b_item['current_yield_pct']}% (15D Change: {b_item['fifteen_day_change_bps']:+d} bps)")


def run_grihalaxmi():
    print("\n" + "=" * 70)
    print("🪙 AGENT 3: GRIHALAXMI - NET INSTITUTIONAL INVESTMENT (NII) DATABASE & SENTINEL")
    print("=" * 70)
    agent = GrihaLaxmiAgent()
    res = agent.run_flow_analysis()
    h = res["historical_benchmark_stats"]
    print(f"Trade Date Evaluated:         {res['trade_date']}")
    print(f"Historical Database:          {h['total_trading_days']} Trading Days (From {h['dataset_start_date']} to {h['dataset_end_date']})")
    print(f"Today's Daily NII:            Rs. {res['today_daily_nii']:,.2f} Cr (FII: Rs. {res['today_fii_net']:,.2f} Cr | DII: Rs. {res['today_dii_net']:,.2f} Cr)")
    print(f"Today's 15-Day Cum. NII (Ct): Rs. {res['today_cum_15d_nii']:,.2f} Cr")
    print(f"15-Day Avg of Cum. NIIs (Ct): Rs. {res['avg_15d_cum_nii']:,.2f} Cr")
    print(f"Difference (Spread):          Rs. {res['diff_from_avg']:,.2f} Cr ({res['spread_pct']}%)")
    print(f"Historical Percentile Rank:   {h['today_percentile_rank']}% (Min: Rs. {h['hist_min_15d_cum']:,.2f} Cr, Max: Rs. {h['hist_max_15d_cum']:,.2f} Cr)")
    print("-" * 70)
    print(f"RULE EVALUATION:")
    print(f"  Condition: Today 15D Cum. NII ({res['today_cum_15d_nii']:,.2f}) < 15-Day Avg ({res['avg_15d_cum_nii']:,.2f})")
    print(f"  Result:    {res['is_below_15_day_avg']} -> {'RECOMMEND INVESTING IN STOCK MARKET' if res['is_below_15_day_avg'] else 'CAUTION / HOLD'}")
    print(f"\nDirective: {res['rationale']}")


def run_safetypriya():
    print("\n" + "=" * 70)
    print("🛡️ AGENT 4: SAFETYPRIYA - MUTUAL FUNDS (5 AMCs) & FIXED DEPOSITS")
    print("=" * 70)
    agent = SafetyPriyaAgent()
    res = agent.run_safety_analysis()
    print(f"Summary: {res['summary']}\n")
    print("--- TOP MUTUAL FUNDS BY CATEGORY (15D & 1W NAV PERFORMANCE) ---")
    for cat, fund in res["top_picks_by_category"].items():
        print(f"[{cat.upper()}] {fund['scheme_name']}")
        print(f"  AMC: {fund['amc']} | Current NAV: Rs. {fund['current_nav']:,.2f} | 15D Return: +{fund['fifteen_chg_pct']}% | 1W Return: +{fund['week_chg_pct']}% | Risk: {fund['risk_profile']}")

    print("\n--- FIXED DEPOSIT BENCHMARKS IN INDIA ---")
    for fd in res["fd_benchmarks"]:
        print(f"  * {fd['bank']:<32} Tenure: {fd['tenure']:<18} General: {fd['general_rate']}% p.a. | Senior: {fd['senior_rate']}% p.a.")


def run_stockbull():
    print("\n" + "=" * 80)
    print("🐂 SUB-AGENT: STOCKBULL - ADVOCATE FOR 100% EQUITIES DEPLOYMENT")
    print("=" * 80)
    agent = StockBullAgent()
    res = agent.evaluate()
    print(f"Mandate: {res['mandate']}")
    print(f"\nSummary: {res['summary']}\n")
    print("--- 5 CORE ARGUMENTS FOR 100% STOCKS ---")
    for i, arg in enumerate(res.get("core_arguments_for_100_percent", []), 1):
        print(f"  {i}. {arg}")
    print("\n--- CURATED 5 BEST APPRECIATION STOCKS (100% FUND SPLIT) ---")
    print(f"{'#':<3} {'Symbol':<12} {'Company':<24} {'Weight':<8} {'Price Ref':<16} {'Upside':<12} {'Horizon'}")
    print("-" * 88)
    for i, s in enumerate(res["curated_picks"], 1):
        price_ref = s.get("entry_price_ref", "N/A")
        print(f"{i:<3} {s['symbol']:<12} {s['name'][:22]:<24} {s['recommended_weight_pct']}%     {price_ref:<16} {s['target_upside_pct']:<12} {s['target_horizon']}")
        print(f"    Thesis: {s['key_thesis']}")


def run_mfhussain():
    print("\n" + "=" * 80)
    print("🎨 SUB-AGENT: MFHUSSAIN - ADVOCATE FOR 100% MUTUAL FUNDS DEPLOYMENT")
    print("=" * 80)
    agent = MFHussainAgent()
    res = agent.evaluate()
    print(f"Mandate: {res['mandate']}")
    print(f"\nSummary: {res['summary']}\n")
    print("--- 5 CORE ARGUMENTS FOR 100% MUTUAL FUNDS ---")
    for i, arg in enumerate(res.get("core_arguments_for_100_percent", []), 1):
        print(f"  {i}. {arg}")
    print("\n--- CURATED 5 BEST PERFORMING MFs WITH BRIGHT FUTURE POTENTIAL (100% FUND SPLIT) ---")
    print(f"{'#':<3} {'Scheme Name':<38} {'AMC':<16} {'Weight':<8} {'NAV Ref':<14} {'15D Ret':<10} {'Risk'}")
    print("-" * 98)
    for i, m in enumerate(res["curated_picks"], 1):
        nav_ref = m.get("current_nav_ref", "N/A")
        ret_15d = m.get("fifteen_day_return", "N/A")
        print(f"{i:<3} {m['scheme_name'][:36]:<38} {m['amc'][:14]:<16} {m['recommended_weight_pct']}%     {nav_ref:<14} {ret_15d:<10} {m['risk_profile']}")
        print(f"    Future Potential: {m['future_potential_thesis']}")


def run_fdlover():
    print("\n" + "=" * 80)
    print("🔒 SUB-AGENT: FDLOVER - ADVOCATE FOR 100% FIXED DEPOSITS & CORPORATE BONDS")
    print("=" * 80)
    agent = FDLoverAgent()
    res = agent.evaluate()
    print(f"Mandate: {res['mandate']}")
    print(f"Blended Annual Yield: {res.get('blended_annual_yield_pct', 8.02)}% p.a.")
    print(f"\nSummary: {res['summary']}\n")
    print("--- 5 CORE ARGUMENTS FOR 100% FIXED INCOME & FDs ---")
    for i, arg in enumerate(res.get("core_arguments_for_100_percent", []), 1):
        print(f"  {i}. {arg}")
    print("\n--- CURATED TOP 5 BEST FD & CORPORATE BOND OPTIONS (100% FUND SPLIT) ---")
    print(f"{'#':<3} {'Issuer':<28} {'Instrument':<18} {'Rating':<12} {'General %':<10} {'Senior %':<10} {'Weight'}")
    print("-" * 92)
    for i, f in enumerate(res["curated_picks"], 1):
        print(f"{i:<3} {f['issuer'][:26]:<28} {f['instrument_type'][:16]:<18} {f['credit_rating']:<12} {f['annual_interest_rate_pct']}%      {f['senior_citizen_rate_pct']}%      {f['recommended_weight_pct']}%")
        print(f"    Safety Rationale: {f['safety_rationale']} (Tenure: {f['tenure']})")


def run_buddhiman(export: bool = False):
    print("\n" + "=" * 80)
    print("🧠 AGENT 5: BUDDHIMAN - SUPREME ASSET ALLOCATION & COUNCIL ARBITRATION")
    print("=" * 80)
    if export:
        scheduler = FridayScheduler()
        path = scheduler.run_friday_synthesis()
        print(f"\nDossier exported to {path}")
    else:
        agent = BuddhimanAgent()
        res = agent.synthesize_all_agents()
        dates = res["dates"]
        print(f"Recommendation Generated (Friday): {dates['friday_recommendation_date']}")
        print(f"Execution Target (Upcoming Monday):  {dates['upcoming_monday_action_date']}")
        print(f"Strategic Regime:                   {res['regime']}\n")

        # Council of Advocates Arbitration
        council = res.get("council_of_advocates", {})
        verdict = council.get("arbitration_verdict", res.get("arbitration_verdict", {}))
        if verdict:
            print("-" * 80)
            print("🏛️ BUDDHIMAN'S COUNCIL OF 3 ADVOCATES - THE 100% SINGLE-ASSET DEBATE:")
            print("-" * 80)
            print(f" • StockBull Pitch:  {verdict.get('stockbull_pitch_summary', 'N/A')}")
            print(f" • MFHussain Pitch:  {verdict.get('mfhussain_pitch_summary', 'N/A')}")
            print(f" • FDLover Pitch:    {verdict.get('fdlover_pitch_summary', 'N/A')}")
            print(f"\n ⚖️ Supreme Ruling:  {verdict.get('buddhiman_ruling', 'N/A')}\n")

        print("RECOMMENDED FRESH FUNDS ALLOCATION:")
        for asset, pct in res["allocation_percentages"].items():
            print(f"  • {asset.replace('_', ' ')}: {pct}%")

        print("\n" + "=" * 80)
        print("THE 5 ACTIONABLE PICKS FOR UPCOMING MONDAY:")
        print("=" * 80)
        for i, pick in enumerate(res["five_actionable_picks"], 1):
            print(f"\n#{i}. [{pick['type']}] {pick['name']}")
            print(f"    Weight: {pick['recommended_weight_pct']}% | Category: {pick['sector']} | Ref: {pick['entry_price_ref']}")
            print(f"    Horizon: {pick['target_horizon']} | Risk Tier: {pick['risk_profile']}")
            print(f"    Action: {pick['action']}")
            print(f"    Rationale: {pick['key_driver']}")


def run_chitragupthan(capital: float = 100000.0):
    print("\n" + "=" * 90)
    print("📜 AGENT: CHITRAGUPTHAN - CELESTIAL PORTFOLIO AUDITOR & SIMULATION LEDGER")
    print("=" * 90)
    agent = ChitragupthanAgent()
    res = agent.run_simulation(capital=capital)
    
    for i, pred in enumerate(res["prediction_simulations"], 1):
        print("\n" + "-" * 90)
        print(f"🏛️ PREDICTION #{i}: {pred['prediction_date']} (Action Monday: {pred['execution_monday']})")
        print(f"   Regime: {pred['regime']} | Active Horizon: {pred['elapsed_days']} Days")
        print("-" * 90)
        print(f"{'#':<3} {'Instrument':<28} {'Category':<15} {'Weight':<7} {'Chosen Pred Val':<16} {'Current Val':<14} {'% Change':<9} {'Status'}")
        print("-" * 110)
        for r_idx, r in enumerate(pred["table_rows"], 1):
            status_text = r['status'].replace('🟢 ', '').replace('🔴 ', '').replace('🟡 ', '')
            print(f"{r_idx:<3} {r['instrument_name'][:27]:<28} {r['asset_class'][:14]:<15} {r['weight_pct']:<5.0f}% Rs. {r['fund_value_prediction_date']:<12,.2f} Rs. {r['current_value']:<10,.2f} {r['pct_change']:>+6.2f}%   {status_text}")
        
        sum_data = pred["summary"]
        print("-" * 110)
        print(f"    TOTALS: Initial = Rs. {sum_data['total_fund_value_prediction_date']:,.2f} | Current = Rs. {sum_data['total_current_value']:,.2f} | Net Return = {sum_data['total_pct_change']:+.2f}% | P&L = Rs. {sum_data['total_pnl']:+,.2f}")
        print(f"    {sum_data['karma_verdict']}")


def run_sarathy(capital: float = 100000.0):
    print("\n" + "=" * 95)
    print("🧭 AGENT: SARATHY - STRATEGIC QUALITY ASSESSOR, WEB SCOUT & CONTINUOUS IMPROVEMENT DRIVER")
    print("=" * 95)
    from agents.sarathy import SarathyAgent
    agent = SarathyAgent()
    res = agent.run_assessment(capital=capital)
    audit = res["simulation_audit_report"]
    web_intel = res["monday_web_intelligence"]
    recs = res["improvement_recommendations"]
    delegation = res["viswakarma_delegation"]

    print(f"Mandate: {res['mandate']}")
    print(f"\nExecutive Summary: {res['executive_summary']}\n")

    # 1. Audit vs Projected Targets
    print("--- 1. SIMULATION AUDIT OF FRIDAY'S PREDICTIONS VS PROJECTED TARGET EARNINGS ---")
    print(f"  Picks Audited: {audit['total_picks_audited']} | Outperforming (+Alpha): {audit['outperforming_picks']} | On-Track: {audit['on_track_picks']} | Lagging: {audit['lagging_picks']}")
    print(f"  Average Tracking Variance: {audit['average_tracking_variance_pct']:+.2f}%\n")
    print(f"{'Instrument':<28} {'Asset Class':<18} {'Initial Val':<12} {'Curr Val':<12} {'Act %':<8} {'Exp %':<8} {'Var %':<8} {'Status'}")
    print("-" * 115)
    for p in audit["audited_predictions"]:
        for r in p["audited_rows"]:
            status_text = r['audit_status'].split('(')[0].strip()
            print(f"{r['instrument_name'][:26]:<28} {r['asset_class'][:16]:<18} Rs.{r['initial_value']:<9,.0f} Rs.{r['current_value']:<9,.0f} {r['actual_return_pct']:>+6.2f}% {r['expected_run_rate_pct']:>+6.2f}% {r['variance_pct']:>+6.2f}%  {status_text}")

    # 2. Monday Web Intelligence & Recommended Websites
    print("\n--- 2. MONDAY WEB INTELLIGENCE: RECOMMENDED SPECIALIZED FINANCIAL PORTALS ---")
    for w in web_intel["recommended_websites"]:
        print(f" • {w['website_name']} ({w['url']}):")
        print(f"    Target: {', '.join(w['recommended_for'])} | Category: {w['category']}")
        print(f"    Value-Add: {w['value_add']}")

    # 3. Monday Market Cues & Technical Analysis
    print("\n--- 3. MONDAY MARKET CUES & MAJOR PUBLISHED TECHNICAL ANALYSIS ---")
    mcues = web_intel["monday_market_cues"]
    print(f"  GIFT Nifty:       {mcues['gift_nifty_indication']}")
    print(f"  Asian Markets:    {mcues['asian_markets_cues']}")
    print(f"  Options OI Range: {mcues['options_oi_cluster']['interpretive_bias']} (Support: {mcues['options_oi_cluster']['major_put_support']} / Resistance: {mcues['options_oi_cluster']['heavy_call_resistance']})")
    tech = web_intel["major_technical_analysis"]["nifty_50_technical_setup"]
    print(f"  NIFTY 50 Tech:    {tech['primary_trend']} | RSI(14): {tech['fourteen_rsi']} ({tech['rsi_status']})")
    print(f"  Key Levels:       Support: {tech['key_support_levels'][0]} | Resistance: {tech['key_resistance_levels'][0]}")
    print(f"  Chart Pattern:    {tech['chart_pattern']}")

    # 4. Improvement Recommendations Delegated to Viswakarma
    print("\n--- 4. SARATHY'S IMPROVEMENT DIRECTIVES DELEGATED TO VISWAKARMA ---")
    print(f"  Target Cycle: {recs['cycle_objective']}")
    print("  • For StockBull:")
    for d in recs["stock_bull_directives"][:2]:
        print(f"     - {d}")
    print("  • For MFHussain:")
    for d in recs["mf_hussain_directives"][:2]:
        print(f"     - {d}")
    print("  • For FDLover:")
    for d in recs["fd_lover_directives"][:2]:
        print(f"     - {d}")
    print("  • For Buddhiman:")
    for d in recs["buddhiman_directives"][:2]:
        print(f"     - {d}")

    # 5. Viswakarma Handoff Status
    vw = delegation["viswakarma_execution_report"]
    print(f"\n  ⚙️ Viswakarma Handoff Status: {vw['status']} (Work Order: {vw['work_order_id']})")
    print(f"     {vw['engineer_summary']}")


def run_viswakarma():
    print("\n" + "=" * 95)
    print("🔨 AGENT: VISWAKARMA - LEAD SYSTEMS ENGINEER & CODE ARCHITECT")
    print("=" * 95)
    from agents.viswakarma import ViswakarmaAgent
    agent = ViswakarmaAgent()
    res = agent.run()
    reg = res["registry"]
    print(f"Mandate: {agent.mandate}")
    print(f"Current Architectural Version: {reg['version']} ({reg['status']})")
    print(f"Target Cycle: {reg['target_cycle']['next_friday_recommendation']} for {reg['target_cycle']['upcoming_monday_implementation']}")
    print("\n--- ACTIVE ENGINEERING PATCHES APPLIED TO THE 4 AGENTS ---")
    for agent_key, patch in reg["active_patches"].items():
        print(f"\n • {agent_key} Engineering Module: {patch.get('module', 'StandardPatch')}")
        print(f"   Status: {patch.get('status', 'DEPLOYED')}")
        if "data_sources_wired" in patch:
            print(f"   Data Sources Wired: {', '.join(patch['data_sources_wired'])}")
        if "technical_indicators_activated" in patch:
            print(f"   Technical Indicators: {patch['technical_indicators_activated']}")
        if "alpha_hurdles_activated" in patch:
            print(f"   Alpha Hurdles: {patch['alpha_hurdles_activated']}")
        if "spread_sentinel_activated" in patch:
            print(f"   Spread Sentinel: {patch['spread_sentinel_activated']}")
        if "market_cues_bridge_activated" in patch:
            print(f"   Market Cues Bridge: {patch['market_cues_bridge_activated']}")


def main():
    parser = argparse.ArgumentParser(description="5-Agent Indian Fund Deployment Advisory System")
    parser.add_argument(
        "--agent",
        choices=["jasoos", "explorer", "grihalaxmi", "safetypriya", "stockbull", "mfhussain", "fdlover", "chitragupthan", "sarathy", "viswakarma", "buddhiman", "all"],
        default="buddhiman",
        help="Specify which agent to execute (default: buddhiman full synthesis)"
    )
    parser.add_argument(
        "--capital",
        type=float,
        default=100000.0,
        help="Simulated capital for Chitragupthan & Sarathy (default: 100000.0)"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export recommendation dossier to Markdown & JSON in dossiers/"
    )

    args = parser.parse_args()

    if args.agent == "jasoos":
        run_jasoos()
    elif args.agent == "explorer":
        run_explorer()
    elif args.agent == "grihalaxmi":
        run_grihalaxmi()
    elif args.agent == "safetypriya":
        run_safetypriya()
    elif args.agent == "stockbull":
        run_stockbull()
    elif args.agent == "mfhussain":
        run_mfhussain()
    elif args.agent == "fdlover":
        run_fdlover()
    elif args.agent == "chitragupthan":
        run_chitragupthan(capital=args.capital)
    elif args.agent == "sarathy":
        run_sarathy(capital=args.capital)
    elif args.agent == "viswakarma":
        run_viswakarma()
    elif args.agent == "all":
        run_jasoos()
        run_explorer()
        run_grihalaxmi()
        run_safetypriya()
        run_stockbull()
        run_mfhussain()
        run_fdlover()
        run_buddhiman(export=args.export)
        run_chitragupthan(capital=args.capital)
        run_sarathy(capital=args.capital)
        run_viswakarma()
    else:
        run_buddhiman(export=args.export)


if __name__ == "__main__":
    main()
