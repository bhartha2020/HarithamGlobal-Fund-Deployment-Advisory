"""
Weekly Friday Scheduler for 5-Agent Investment Advisory Team.
- Automatically triggers every Friday after Indian market close (16:00 IST)
- Can also be executed on-demand
- Generates and persists the Monday Action Dossier to disk (JSON & Markdown)
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

from agents.buddhiman import BuddhimanAgent

DOSSIER_DIR = Path("dossiers")
DOSSIER_DIR.mkdir(exist_ok=True)


class FridayScheduler:
    def __init__(self):
        self.buddhiman = BuddhimanAgent()

    def run_friday_synthesis(self) -> str:
        """Executes the full 5-agent pipeline and saves Friday-to-Monday dossier."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering Friday Multi-Agent Synthesis...")
        result = self.buddhiman.synthesize_all_agents()

        timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = DOSSIER_DIR / f"recommendation_dossier_{timestamp_slug}.json"
        md_path = DOSSIER_DIR / f"recommendation_dossier_{timestamp_slug}.md"

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Generate and save formatted Markdown Report
        md_content = self.generate_markdown_report(result)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Dossier successfully saved to:")
        print(f" - JSON: {json_path}")
        print(f" - Markdown: {md_path}")
        return str(md_path)

    def generate_markdown_report(self, result: dict) -> str:
        dates = result["dates"]
        alloc = result["allocation_percentages"]
        picks = result["five_actionable_picks"]
        audit = result["agent_audit_trail"]

        lines = [
            "# 🏦 5-Agent Indian Fund Deployment Advisory Dossier",
            f"**Generation Date (Friday)**: {dates['friday_recommendation_date']}",
            f"**Action Date (Upcoming Monday)**: {dates['upcoming_monday_action_date']}",
            f"**Market Regime**: `{result['regime']}`",
            "",
            "---",
            "## 🎯 Recommended Fresh Funds Asset Allocation",
            f"- **Individual Stocks**: `{alloc['Stocks']}%`",
            f"- **Mutual Funds**: `{alloc['Mutual_Funds']}%`",
            f"- **Index & Sector ETFs**: `{alloc['ETFs']}%`",
            f"- **Fixed Deposits (FDs)**: `{alloc['Fixed_Deposits']}%`",
            "",
            "---",
            "## 🏆 The 5 Actionable Picks for Upcoming Monday",
            "| # | Instrument | Name | Category / AMC | Reference Price / NAV | Weight | Action | Key Driver |",
            "|---|---|---|---|---|---|---|---|"
        ]

        for i, p in enumerate(picks, 1):
            lines.append(
                f"| {i} | {p['type']} | **{p['name']}** | {p['sector']} | {p['entry_price_ref']} | "
                f"**{p['recommended_weight_pct']}%** | {p['action']} | {p['key_driver']} |"
            )

        lines.extend([
            "",
            "---",
            "## 🕵️ Multi-Agent Audit Trail & Research Syntheses",
            "",
            f"### 1. Jasoos (10-Day Market Block Deals Sleuth)",
            f"- **Sources Evaluated**: {', '.join(audit['jasoos']['sources_checked'])}",
            f"- **Top Stock**: `{audit['jasoos']['top_stock']}`",
            f"- **Finding**: {audit['jasoos']['summary']}",
            "",
            f"### 2. Explorer (Global Macro & Index Predictor)",
            f"- **Global Composite Score**: `{audit['explorer']['global_score']}/100` ({audit['explorer']['bias']})",
            f"- **Predicted Impact on NIFTY 50**: `{audit['explorer']['nifty_impact']}`",
            f"- **Finding**: {audit['explorer']['summary']}",
            "",
            f"### 3. GrihaLaxmi (Institutional Flow Sentinel)",
            f"- **15-Day Cumulative Net Flow**: `Rs. {audit['grihalaxmi']['cumulative_net']:,.2f} Cr`",
            f"- **15-Day Moving Average**: `Rs. {audit['grihalaxmi']['avg_15d']:,.2f} Cr`",
            f"- **Rule Status ('Flow < 15-DMA')**: `{audit['grihalaxmi']['rule_triggered']}` (Stock Market Buy Trigger)",
            f"- **Finding**: {audit['grihalaxmi']['summary']}",
            "",
            f"### 4. SafetyPriya (Capital Preservation & MFs)",
            f"- **AMCs Screened**: ICICI Prudential, Kotak Mahindra, Tata, JioBlackRock, HDFC",
            f"- **Top Defensive/Hybrid Pick**: `{audit['safetypriya']['top_hybrid']}`",
            f"- **Benchmark Bank FD Rate**: `{audit['safetypriya']['top_fd_rate']}% p.a.`",
            f"- **Finding**: {audit['safetypriya']['summary']}",
            "",
            "---",
            "## ⚖️ Executive Monday Execution Playbook",
            "1. **Pre-Market (09:00 - 09:08 IST)**: Cross-check GIFT Nifty and Explorer global morning cue.",
            "2. **Market Open (09:15 - 10:30 IST)**: Execute designated equity/ETF limits using staggered limit orders.",
            "3. **Mutual Fund Order Window (Before 14:00 IST)**: Place lump sum or register weekly SIP for same-day NAV allocation.",
            "4. **Fixed Deposits**: Book term deposit allocation online to guarantee capital lock-in yield.",
            "",
            "_Generated autonomously by the 5-Agent Advisory System (Jasoos, Explorer, GrihaLaxmi, SafetyPriya, Buddhiman)._"
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    scheduler = FridayScheduler()
    scheduler.run_friday_synthesis()
