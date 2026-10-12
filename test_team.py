"""Test script for verifying 5-Agent investment team."""

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from agents.buddhiman import BuddhimanAgent

def main():
    print("=" * 70)
    print("INITIALIZING 5-AGENT INDIAN INVESTMENT STRATEGY SYSTEM")
    print("=" * 70)
    buddhiman = BuddhimanAgent()
    print("Running multi-agent synthesis pipeline...")
    result = buddhiman.synthesize_all_agents()

    print("\n--- SCHEDULE & DATES ---")
    dates = result["dates"]
    print(f"Current Date:                {dates['current_date']}")
    print(f"Friday Recommendation Date:  {dates['friday_recommendation_date']}")
    print(f"Upcoming Monday Action Date: {dates['upcoming_monday_action_date']}")

    print("\n--- AGENT AUDIT SUMMARY ---")
    audit = result["agent_audit_trail"]
    print(f"1. Jasoos:     Top Stock -> {audit['jasoos']['top_stock']}")
    print(f"2. Explorer:   Global Bias -> {audit['explorer']['bias']} (Score: {audit['explorer']['global_score']}/100), Nifty: {audit['explorer']['nifty_impact']}")
    print(f"3. GrihaLaxmi: FII/DII Rule Triggered: {audit['grihalaxmi']['rule_triggered']}, 15-Day Net: Rs {audit['grihalaxmi']['cumulative_net']:,.2f} Cr, 15-DMA: Rs {audit['grihalaxmi']['avg_15d']:,.2f} Cr")
    print(f"4. SafetyPriya:Top Hybrid MF -> {audit['safetypriya']['top_hybrid']}, Top Bank FD: {audit['safetypriya']['top_fd_rate']}% p.a.")

    print("\n--- BUDDHIMAN ASSET ALLOCATION ---")
    print(f"Market Regime: {result['regime']}")
    for asset, weight in result["allocation_percentages"].items():
        print(f"  * {asset.replace('_', ' ')}: {weight}%")

    print("\n--- TOP 5 PICKS FOR UPCOMING MONDAY ---")
    for i, pick in enumerate(result["five_actionable_picks"], 1):
        print(f"\n{i}. [{pick['type']}] {pick['name']}")
        print(f"   Allocation: {pick['recommended_weight_pct']}% | Horizon: {pick['target_horizon']} | Risk: {pick['risk_profile']}")
        print(f"   Reference Price/NAV: {pick['entry_price_ref']}")
        print(f"   Action: {pick['action']}")
        print(f"   Rationale: {pick['key_driver']}")

    print("\n" + "=" * 70)
    print("ALL 5 AGENTS EXECUTED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
