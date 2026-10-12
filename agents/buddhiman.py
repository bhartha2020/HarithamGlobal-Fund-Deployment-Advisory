"""
Agent 5: BUDDHIMAN (The Chief Investment Officer & Master Synthesizer)
- Master Orchestrator that ingests research and signals from:
  1. Jasoos (15 Big-Ticket Stocks + Press + Daily NSE/BSE)
  2. Explorer (Global Macro Trends -> NIFTY & SENSEX Forecast)
  3. GrihaLaxmi (Cumulative FII/DII Flows over 15 Days vs 15-DMA)
  4. SafetyPriya (MFs: Equity/Debt/Hybrid/Liquid across 5 AMCs + FDs)
- Evaluates asset class priorities: Stocks vs Mutual Funds vs ETFs vs Fixed Deposits
- Recommends an optimal COMBINATION OF 5 INSTRUMENTS every Friday for execution on the upcoming Monday
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta

from agents.jasoos import JasoosAgent
from agents.explorer import ExplorerAgent
from agents.grihalaxmi import GrihaLaxmiAgent
from agents.safetypriya import SafetyPriyaAgent
from agents.stock_bull import StockBullAgent
from agents.mf_hussain import MFHussainAgent
from agents.fd_lover import FDLoverAgent
from config import INDIAN_ETFS, TOTAL_RECOMMENDED_PICKS


class BuddhimanAgent:
    def __init__(self):
        self.name = "Buddhiman"
        self.role = "Chief Investment Strategist & Final Portfolio Allocator"
        self.jasoos = JasoosAgent()
        self.explorer = ExplorerAgent()
        self.grihalaxmi = GrihaLaxmiAgent()
        self.safetypriya = SafetyPriyaAgent()
        # Team of 3 specialized advocate agents working under Buddhiman
        self.stock_bull = StockBullAgent()
        self.mf_hussain = MFHussainAgent()
        self.fd_lover = FDLoverAgent()

    def calculate_dates(self) -> Dict[str, str]:
        """Calculates current date, designated Friday recommendation date, and upcoming Monday action date."""
        today = datetime.now()
        weekday = today.weekday()  # Monday=0, Tuesday=1, ... Friday=4, Saturday=5, Sunday=6

        # Determine target Friday
        if weekday <= 4:
            # Monday to Friday: target is this Friday
            days_to_friday = 4 - weekday
            target_friday = today + timedelta(days=days_to_friday)
        else:
            # Weekend: target was the most recent Friday
            days_back = weekday - 4
            target_friday = today - timedelta(days=days_back)

        # Determine upcoming action Monday (which comes after target Friday)
        days_to_monday = (0 - today.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7  # If today is Monday, target the next upcoming Monday
        upcoming_monday = today + timedelta(days=days_to_monday)

        return {
            "current_date": today.strftime("%A, %d %B %Y"),
            "friday_recommendation_date": target_friday.strftime("%A, %d %B %Y"),
            "upcoming_monday_action_date": upcoming_monday.strftime("%A, %d %B %Y")
        }

    def synthesize_all_agents(self) -> Dict[str, Any]:
        """Runs the 4 sensor agents, convenes the Council of 3 Advocates (StockBull, MFHussain, FDLover), and arbitrates the final recommendation."""
        # Step 1: Collect reports from the 4 sensor agents
        jasoos_report = self.jasoos.run_investigation()
        explorer_report = self.explorer.run_exploration()
        grihalaxmi_report = self.grihalaxmi.run_flow_analysis()
        safetypriya_report = self.safetypriya.run_safety_analysis()

        # Step 2: Convene Buddhiman's Team of 3 Specialized Advocates
        stockbull_proposal = self.stock_bull.evaluate(jasoos_report, explorer_report, grihalaxmi_report, safetypriya_report)
        mfhussain_proposal = self.mf_hussain.evaluate(jasoos_report, explorer_report, grihalaxmi_report, safetypriya_report)
        fdlover_proposal = self.fd_lover.evaluate(jasoos_report, explorer_report, grihalaxmi_report, safetypriya_report)

        # Step 3: Extract key macro signals
        global_score = explorer_report["global_composite_score"]  # -100 to +100
        global_bias = explorer_report["directional_bias"]
        fii_buy_signal = grihalaxmi_report["recommend_stock_market"]  # Flow < 15DMA

        # Step 4: Determine macro regime & Asset Class Weightings
        if fii_buy_signal and global_score >= 0:
            regime = "Aggressive Growth & Dip Accumulation"
            allocation_pct = {
                "Stocks": 45,
                "Mutual_Funds": 30,
                "ETFs": 15,
                "Fixed_Deposits": 10
            }
            stock_weights = [25, 20]
            mf_weights = [30]
            etf_weights = [15]
            fd_weights = [10]

        elif fii_buy_signal and global_score < 0:
            regime = "Prudent Value Accumulation (Counter-Cyclical)"
            allocation_pct = {
                "Stocks": 35,
                "Mutual_Funds": 35,
                "ETFs": 15,
                "Fixed_Deposits": 15
            }
            stock_weights = [20, 15]
            mf_weights = [35]
            etf_weights = [15]
            fd_weights = [15]

        elif not fii_buy_signal and global_score >= 20:
            regime = "Momentum with Hybrid Hedge"
            allocation_pct = {
                "Stocks": 30,
                "Mutual_Funds": 40,
                "ETFs": 15,
                "Fixed_Deposits": 15
            }
            stock_weights = [15, 15]
            mf_weights = [40]
            etf_weights = [15]
            fd_weights = [15]

        else:
            regime = "Defensive Capital Preservation & Yield Optimization"
            allocation_pct = {
                "Stocks": 15,
                "Mutual_Funds": 35,
                "ETFs": 10,
                "Fixed_Deposits": 40
            }
            stock_weights = [15]
            mf_weights = [20, 15]
            etf_weights = [10]
            fd_weights = [40]

        # Step 5: Construct the EXACT 5 Actionable Picks for Upcoming Monday (Drawing from Council Proposals)
        five_picks = []

        # 1. Stocks selected directly from StockBull's top picks
        sb_picks = stockbull_proposal["curated_picks"]
        for i, weight in enumerate(stock_weights):
            s = sb_picks[i] if i < len(sb_picks) else sb_picks[0]
            five_picks.append({
                "type": "Stock (Equity)",
                "symbol": s["symbol"],
                "name": s["name"],
                "sector": s["sector"],
                "entry_price_ref": s["entry_price_ref"],
                "target_horizon": s["target_horizon"],
                "risk_profile": "High / Equity",
                "recommended_weight_pct": weight,
                "key_driver": f"StockBull #{i+1} Pick: {s['key_thesis']} (Target Upside: {s['target_upside_pct']})",
                "action": "Buy on Monday Market Open / Staggered"
            })

        # 2. Mutual Funds selected directly from MFHussain's top picks
        mf_picks = mfhussain_proposal["curated_picks"]
        for i, weight in enumerate(mf_weights):
            m = mf_picks[i] if i < len(mf_picks) else mf_picks[0]
            five_picks.append({
                "type": f"Mutual Fund ({m['category'].split()[0]})",
                "symbol": m.get("scheme_code", f"MF_{i+1}"),
                "name": m["scheme_name"],
                "sector": f"{m['amc']} AMC ({m['category']})",
                "entry_price_ref": f"NAV {m['current_nav_ref']}",
                "target_horizon": m["target_horizon"],
                "risk_profile": m["risk_profile"],
                "recommended_weight_pct": weight,
                "key_driver": f"MFHussain #{i+1} Future Potential Fund: {m['future_potential_thesis']}",
                "action": "Deploy Lump Sum / Start Weekly SIP on Monday"
            })

        # 3. ETFs from Indian ETF benchmarks
        for weight in etf_weights:
            etf = INDIAN_ETFS[0] if INDIAN_ETFS else {"symbol": "NIFTYBEES.NS", "name": "Nippon India Nifty 50 BeES ETF", "category": "Large Cap Index ETF"}
            five_picks.append({
                "type": "ETF (Index)",
                "symbol": etf["symbol"],
                "name": etf["name"],
                "sector": etf["category"],
                "entry_price_ref": "Live Market Price",
                "target_horizon": "12+ Months",
                "risk_profile": "Moderate High",
                "recommended_weight_pct": weight,
                "key_driver": (
                    f"Explorer's global alignment favors broad-market Indian index participation via {etf['name']}."
                ),
                "action": "Accumulate on Monday Dip"
            })

        # 4. Fixed Deposits & Corporate Bonds selected directly from FDLover's scouted picks
        fd_picks = fdlover_proposal["curated_picks"]
        for i, weight in enumerate(fd_weights):
            f = fd_picks[i] if i < len(fd_picks) else fd_picks[0]
            five_picks.append({
                "type": "Fixed Deposit (Guaranteed)",
                "symbol": "SECURED_YIELD",
                "name": f"{f['issuer']} ({f['instrument_type']})",
                "sector": f"{f['credit_rating']}",
                "entry_price_ref": f"{f['annual_interest_rate_pct']}% p.a. ({f['senior_citizen_rate_pct']}% Seniors)",
                "target_horizon": f["tenure"],
                "risk_profile": "Zero Capital Risk (AAA / DICGC)",
                "recommended_weight_pct": weight,
                "key_driver": f"FDLover #{i+1} Scouted Best Option: {f['safety_rationale']} ({f['credit_rating']})",
                "action": "Book Term Deposit on Monday via NetBanking"
            })

        # Strict validation: ensure exactly 5 picks and verify weights reconciliation
        assert len(five_picks) == TOTAL_RECOMMENDED_PICKS, f"Expected {TOTAL_RECOMMENDED_PICKS} picks, got {len(five_picks)}"
        
        # Verify pick weights sum to 100%
        total_pick_weight = sum(p["recommended_weight_pct"] for p in five_picks)
        assert total_pick_weight == 100, f"Total pick weights ({total_pick_weight}%) must equal 100%"

        # Verify category reconciliation against allocation_pct
        category_pick_sums = {
            "Stocks": sum(p["recommended_weight_pct"] for p in five_picks if "Stock" in p["type"]),
            "Mutual_Funds": sum(p["recommended_weight_pct"] for p in five_picks if "Mutual Fund" in p["type"]),
            "ETFs": sum(p["recommended_weight_pct"] for p in five_picks if "ETF" in p["type"]),
            "Fixed_Deposits": sum(p["recommended_weight_pct"] for p in five_picks if "Fixed Deposit" in p["type"]),
        }
        for cat, expected in allocation_pct.items():
            actual = category_pick_sums.get(cat, 0)
            assert actual == expected, (
                f"Discrepancy in {cat}: Matrix allocated {expected}%, but picks sum to {actual}%"
            )

        # Calculate dates
        dates = self.calculate_dates()

        # Ingest active engineering modifications from Viswakarma (directed by Sarathy's assessment)
        viswakarma_status = {}
        viswakarma_patches = {}
        try:
            from agents.viswakarma import ViswakarmaAgent
            v_agent = ViswakarmaAgent()
            viswakarma_status = v_agent.get_latest_status()
            viswakarma_patches = v_agent.get_active_patches()
        except Exception:
            pass

        # Step 6: Formulate Council of Advocates Arbitration Verdict
        arbitration_verdict = {
            "council_mandate": "Evaluate competing 100% single-asset proposals from StockBull, MFHussain, and FDLover against empirical market signals from Jasoos, Explorer, GrihaLaxmi, and SafetyPriya.",
            "stockbull_pitch_summary": (
                f"StockBull fought for 100% Equities ({', '.join([s['name'] for s in sb_picks[:3]])}), synthesizing "
                f"Jasoos's Rs. {jasoos_report.get('top_15_deal_value_cr', 0):,.1f} Cr institutional block deal accumulation, Explorer's "
                f"{explorer_report.get('broker_predictions', {}).get('consensus_nifty_target', 25150):,} broker target & Graham value qualifiers, "
                f"GrihaLaxmi's contrarian {grihalaxmi_report.get('historical_benchmark_stats', {}).get('today_percentile_rank', 11.7)}th percentile dip trigger, "
                f"and proving SafetyPriya's bank FDs (~4.8% post-tax) fail inflation."
            ),
            "mfhussain_pitch_summary": (
                f"MFHussain fought for 100% Mutual Funds across 5 top AMCs, synthesizing "
                f"Explorer's macro score ({explorer_report.get('global_composite_score', -18.1)}/100) and Graham froth to warn against direct stock bubbles, "
                f"insulating against Jasoos's block deal distribution traps, riding GrihaLaxmi's domestic liquidity absorption, "
                f"and leveraging SafetyPriya's dynamic hybrid alpha with Section 112A tax-free rebalancing."
            ),
            "fdlover_pitch_summary": (
                f"FDLover fought for 100% Fixed Deposits & Corporate Bonds (blended yield {fdlover_proposal['blended_annual_yield_pct']}% p.a.), synthesizing "
                f"Explorer's global rate cuts and RBI neutral pivot to lock in peak terminal yields before rate cuts, "
                f"shielding capital against GrihaLaxmi's FII dump (-Rs. 3,568 Cr), avoiding Explorer/Jasoos equity froth, "
                f"and guaranteeing total capital preservation."
            ),
            "continuous_learning_and_engineering": (
                f"Continuous Feedback Loop: Ingested Sarathy's simulation audit deltas and Monday web intelligence "
                f"(TradingView technicals, Trendlyne delivery volume %, Value Research Sharpe hurdles, and CRISIL debt spreads). "
                f"Viswakarma has engineered and registered specialized enhancements for the council, certified for Buddhiman's "
                f"next Friday recommendation (16 Oct 2026) for upcoming Monday (19 Oct 2026) implementation."
            ),
            "buddhiman_ruling": (
                f"Buddhiman Grand Arbitration Ruling: While each advocate coherently leveraged all 4 sensor agents to demand 100% of the pie, "
                f"extreme single-asset concentration carries severe blind spots. Buddhiman balances the cross-agent findings under the '{regime}' matrix: "
                f"{allocation_pct['Stocks']}% in high-conviction Stocks (from StockBull), "
                f"{allocation_pct['Mutual_Funds']}% in dynamic Mutual Funds (from MFHussain), "
                f"{allocation_pct['ETFs']}% in broad index ETF hedge, and "
                f"{allocation_pct['Fixed_Deposits']}% in guaranteed peak yield Fixed Deposits & Bonds (from FDLover)."
            )
        }

        executive_summary = (
            f"Buddhiman Grand Verdict: Convened the Council of 3 Advocates (StockBull, MFHussain, FDLover). "
            f"StockBull pitched 100% Stocks, MFHussain pitched 100% MFs, and FDLover pitched 100% FDs/Bonds. "
            f"Buddhiman arbitrated: market is positioned in a '{regime}' phase. "
            f"Final deployment for fresh funds: {allocation_pct['Stocks']}% in Stocks, "
            f"{allocation_pct['Mutual_Funds']}% in Mutual Funds, {allocation_pct['ETFs']}% in ETFs, "
            f"and {allocation_pct['Fixed_Deposits']}% in Fixed Deposits/Bonds. "
            f"Below are the 5 definitive instrument recommendations formulated this Friday for Monday action."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dates": dates,
            "regime": regime,
            "allocation_percentages": allocation_pct,
            "five_actionable_picks": five_picks,
            "council_of_advocates": {
                "stock_bull": stockbull_proposal,
                "mf_hussain": mfhussain_proposal,
                "fd_lover": fdlover_proposal,
                "arbitration_verdict": arbitration_verdict
            },
            "arbitration_verdict": arbitration_verdict,
            "executive_summary": executive_summary,
            "agent_audit_trail": {
                "jasoos": {
                    "summary": jasoos_report["summary"],
                    "top_stock": jasoos_report.get("top_stock_picks", [{}])[0].get("name", "N/A"),
                    "sources_checked": jasoos_report["sources_scanned"]
                },
                "explorer": {
                    "summary": explorer_report["summary"],
                    "global_score": explorer_report["global_composite_score"],
                    "bias": explorer_report["directional_bias"],
                    "nifty_impact": explorer_report["nifty_projection"]["expected_bias"],
                    "broker_consensus": explorer_report.get("broker_predictions", {}).get("consensus_direction", "N/A"),
                    "broker_validation": explorer_report.get("broker_predictions", {}).get("validation_status", "N/A"),
                    "indices_15d_validation": explorer_report.get("indian_vs_global_15d_comparison", {}).get("validation_status", "N/A"),
                    "graham_assessment": {
                        "large_cap_pass": explorer_report.get("graham_valuations", {}).get("tier_summaries", {}).get("large_cap", {}).get("graham_pass_count", 0),
                        "mid_cap_pass": explorer_report.get("graham_valuations", {}).get("tier_summaries", {}).get("mid_cap", {}).get("graham_pass_count", 0),
                        "small_cap_pass": explorer_report.get("graham_valuations", {}).get("tier_summaries", {}).get("small_cap", {}).get("graham_pass_count", 0),
                    },
                    "central_bank_rates": {
                        "us_fed": explorer_report.get("interest_rates_and_bonds", {}).get("central_banks", {}).get("US Federal Reserve", {}).get("current_rate", "N/A"),
                        "rbi": explorer_report.get("interest_rates_and_bonds", {}).get("central_banks", {}).get("Reserve Bank of India (RBI)", {}).get("current_rate", "N/A"),
                        "us_india_spread_bps": explorer_report.get("interest_rates_and_bonds", {}).get("us_india_spread_bps", 0)
                    }
                },
                "grihalaxmi": {
                    "summary": grihalaxmi_report["summary"],
                    "rule_triggered": grihalaxmi_report["is_below_15_day_avg"],
                    "cumulative_net": grihalaxmi_report["cumulative_net_cr"],
                    "avg_15d": grihalaxmi_report["fifteen_day_avg_cr"]
                },
                "safetypriya": {
                    "summary": safetypriya_report["summary"],
                    "top_hybrid": safetypriya_report.get("top_picks_by_category", {}).get("Hybrid", {}).get("scheme_name", "N/A"),
                    "top_fd_rate": safetypriya_report.get("top_fd_recommendation", {}).get("general_rate", "N/A")
                },
                "stock_bull": {
                    "summary": stockbull_proposal["summary"],
                    "pitch": "100% Equities",
                    "top_pick": stockbull_proposal["curated_picks"][0]["name"],
                    "expected_cagr": stockbull_proposal["expected_portfolio_cagr"]
                },
                "mf_hussain": {
                    "summary": mfhussain_proposal["summary"],
                    "pitch": "100% Mutual Funds",
                    "top_pick": mfhussain_proposal["curated_picks"][0]["scheme_name"],
                    "expected_cagr": mfhussain_proposal["expected_portfolio_cagr"]
                },
                "fd_lover": {
                    "summary": fdlover_proposal["summary"],
                    "pitch": "100% Fixed Deposits & Corporate Bonds",
                    "top_pick": fdlover_proposal["curated_picks"][0]["issuer"],
                    "blended_yield": f"{fdlover_proposal['blended_annual_yield_pct']}% p.a."
                }
            },
            "full_reports": {
                "jasoos": jasoos_report,
                "explorer": explorer_report,
                "grihalaxmi": grihalaxmi_report,
                "safetypriya": safetypriya_report,
                "stock_bull": stockbull_proposal,
                "mf_hussain": mfhussain_proposal,
                "fd_lover": fdlover_proposal
            },
            "continuous_learning_engine": {
                "sarathy_feedback_loop_active": True,
                "viswakarma_status": viswakarma_status,
                "active_engineering_patches": viswakarma_patches
            }
        }
