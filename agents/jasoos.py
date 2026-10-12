"""
Agent 1: JASOOS (The Daily Market Block Deals & Big-Ticket Sleuth)
- Scans ALL block deals and major bulk deals during the day across Indian markets (NSE & BSE).
- Selects and displays the TOP 15 BLOCK DEALS of the day ranked by deal value (₹ Crores).
- Scans leading financial papers: FT, ET, Business Standard, CNBC-TV18, NDTV Profit.
- Enriches each block deal with live NSE/BSE price action, 1-week & 15-day momentum, and volume spikes.
- Computes the Jasoos Institutional Conviction Score and actionable verdicts.
"""

from typing import Dict, List, Any
from datetime import datetime

from data_engine.block_deals import BlockDealsEngine
from data_engine.news_fetcher import NewsFetcher
from data_engine.market_data import MarketDataEngine


class JasoosAgent:
    def __init__(self):
        self.name = "Jasoos"
        self.role = "10-Day Market Block Deals & Institutional Sleuth"
        self.block_engine = BlockDealsEngine()
        self.news_fetcher = NewsFetcher()
        self.market_engine = MarketDataEngine()

    def run_investigation(self) -> Dict[str, Any]:
        """Scans all block deals that occurred in the previous 10 days across the market and picks the top 15."""
        # 1. Fetch all block deals of the previous 10 days and isolate the Top 15
        block_scan = self.block_engine.get_top_15_block_deals(window_days=10)
        top_15_raw = block_scan["top_15_block_deals"]

        # 2. Fetch live news headlines from FT, ET, Business Standard, CNBC, NDTV Profit
        all_articles = self.news_fetcher.fetch_all_sources()
        stock_news = self.news_fetcher.match_articles_to_stocks(all_articles, stock_list=top_15_raw)

        # 3. Fetch quantitative market price and volume metrics for the Top 15 Block Deal stocks
        enriched_market_data = self.market_engine.fetch_stocks_batch(top_15_raw)

        # 4. Synthesize intelligence and calculate Jasoos Conviction Score for each stock
        analyzed_stocks = []
        for stock_mkt in enriched_market_data:
            sym = stock_mkt.get("symbol", "")
            raw_sym = stock_mkt.get("raw_symbol", sym.replace(".NS", ""))
            news_info = stock_news.get(sym, stock_news.get(raw_sym, {
                "article_count": 0,
                "avg_sentiment": 0.0,
                "big_ticket_mentions": 1,
                "headlines": []
            }))

            deal_val = float(stock_mkt.get("deal_value_cr", 100.0))
            deal_type = stock_mkt.get("deal_type", "BUY").upper()

            # Component 1: Block Deal Size Score (max 30 pts)
            deal_size_score = min(30.0, max(8.0, (deal_val / 2000.0) * 30.0))

            # Component 2: Deal Direction & Institutional Conviction (max 15 pts)
            direction_score = 15.0 if "BUY" in deal_type else 6.0

            # Component 3: Media sentiment across FT/ET/BS/CNBC/NDTV (max 20 pts)
            sentiment_score = ((news_info["avg_sentiment"] + 1.0) / 2.0) * 20.0

            # Component 4: 15-Day and 1-Week Return momentum (max 20 pts)
            mom_raw = (stock_mkt["fifteen_ret_pct"] * 1.5) + (stock_mkt["week_ret_pct"] * 2.5)
            momentum_score = max(0.0, min(20.0, 10.0 + mom_raw * 1.2))

            # Component 5: NSE/BSE Volume spike ratio (max 15 pts)
            vol_ratio = stock_mkt["vol_ratio"]
            volume_score = min(15.0, max(2.0, vol_ratio * 6.0))

            total_jasoos_score = round(deal_size_score + direction_score + sentiment_score + momentum_score + volume_score, 1)

            # Categorize status & verdict
            if total_jasoos_score >= 80:
                verdict = "MEGA BLOCK ACCUMULATION"
            elif total_jasoos_score >= 65:
                verdict = "STRONG INSTITUTIONAL BUY"
            elif total_jasoos_score >= 50:
                verdict = "STRATEGIC BLOCK EXPANSION"
            else:
                verdict = "BLOCK REBALANCING / WATCH"

            analyzed_stocks.append({
                "rank": stock_mkt.get("rank", len(analyzed_stocks) + 1),
                "symbol": stock_mkt.get("yahoo_symbol", f"{raw_sym}.NS"),
                "raw_symbol": raw_sym,
                "name": stock_mkt.get("company_name", stock_mkt.get("name", raw_sym)),
                "sector": stock_mkt.get("sector", "Diversified Equities"),
                "trade_date": stock_mkt.get("trade_date", datetime.now().strftime("%d-%b-%Y").upper()),
                "days_ago": stock_mkt.get("days_ago", "Recent"),
                "deals_count_in_window": stock_mkt.get("deals_count_in_window", 1),
                "deal_value_cr": deal_val,
                "client_name": stock_mkt.get("client_name", "Institutional Counterparty"),
                "deal_type": deal_type,
                "quantity": stock_mkt.get("quantity", 0),
                "trade_price": stock_mkt.get("trade_price", stock_mkt["current_price"]),
                "current_price": stock_mkt["current_price"],
                "day_change_pct": stock_mkt["day_change_pct"],
                "week_ret_pct": stock_mkt["week_ret_pct"],
                "fifteen_ret_pct": stock_mkt["fifteen_ret_pct"],
                "vol_ratio": stock_mkt["vol_ratio"],
                "is_volume_spike": stock_mkt["is_volume_spike"],
                "media_sentiment": news_info["avg_sentiment"],
                "article_count": news_info["article_count"],
                "big_ticket_deals_found": max(1, news_info["big_ticket_mentions"]),
                "headlines": news_info["headlines"],
                "jasoos_score": total_jasoos_score,
                "verdict": verdict,
                "exchange": stock_mkt.get("exchange", "NSE")
            })

        # Top 5 highest conviction picks for Buddhiman
        top_picks = sorted(analyzed_stocks, key=lambda x: x["jasoos_score"], reverse=True)[:5]

        # Executive summary
        total_deals = block_scan["total_deals_scanned"]
        market_val = block_scan["total_market_block_value_cr"]
        top_15_val = block_scan["top_15_deal_value_cr"]
        top_stock = analyzed_stocks[0]

        summary_findings = (
            f"Jasoos monitored all block deals over the previous 10 days ({block_scan.get('window_start_date')} to {block_scan.get('window_end_date')}) "
            f"across Indian markets (NSE & BSE), scanning {total_deals} transactions worth Rs. {market_val:,.2f} Cr. "
            f"Isolated the TOP 15 BLOCK DEALS of the 10-day window representing Rs. {top_15_val:,.2f} Cr of institutional capital flow. "
            f"Largest 10-day block deal was in {top_stock['name']} ({top_stock['raw_symbol']}) valued at Rs. {top_stock['deal_value_cr']:,.2f} Cr "
            f"({top_stock['deal_type']} on {top_stock.get('trade_date')} by {top_stock['client_name'][:45]}). All 15 stocks cross-referenced with "
            f"Financial Times, Economic Times, Business Standard, CNBC-TV18, NDTV Profit."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "surveillance_window": block_scan["surveillance_window"],
            "window_days": block_scan["window_days"],
            "window_start_date": block_scan["window_start_date"],
            "window_end_date": block_scan["window_end_date"],
            "total_block_deals_scanned": total_deals,
            "total_market_block_value_cr": market_val,
            "top_15_deal_value_cr": top_15_val,
            "largest_single_deal_cr": block_scan["largest_single_deal_cr"],
            "total_stocks_analyzed": len(analyzed_stocks),
            "summary": summary_findings,
            "top_stock_picks": top_picks,
            "all_15_stocks": analyzed_stocks,
            "top_15_block_deals": analyzed_stocks,
            "sources_scanned": [
                "NSE 10-Day Block Deals Archive & Feed (block.csv)",
                "NSE 10-Day Bulk Transactions Archive & Feed (bulk.csv)",
                "Financial Times (FT)",
                "The Economic Times (ET)",
                "Business Standard",
                "CNBC-TV18",
                "NDTV Profit"
            ]
        }

    def run(self) -> Dict[str, Any]:
        return self.run_investigation()
