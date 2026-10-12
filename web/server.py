"""
FastAPI Server for the 5-Agent Indian Fund Deployment Advisory Dashboard.
Provides interactive REST APIs and serves the front-end SPA on Port 8010.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from agents.jasoos import JasoosAgent
from agents.explorer import ExplorerAgent
from agents.grihalaxmi import GrihaLaxmiAgent
from agents.safetypriya import SafetyPriyaAgent
from agents.stock_bull import StockBullAgent
from agents.mf_hussain import MFHussainAgent
from agents.fd_lover import FDLoverAgent
from agents.buddhiman import BuddhimanAgent
from agents.chitragupthan import ChitragupthanAgent
from agents.sarathy import SarathyAgent
from agents.viswakarma import ViswakarmaAgent
from scheduler import FridayScheduler, DOSSIER_DIR
from config import DEFAULT_WEB_PORT, DEFAULT_WEB_HOST

app = FastAPI(
    title="5-Agent Indian Fund Deployment Advisory",
    description="Multi-Agent Investment Advisory Web App with Sarathy Quality Assessor & Viswakarma Engineer",
    version="1.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate agents
jasoos_agent = JasoosAgent()
explorer_agent = ExplorerAgent()
grihalaxmi_agent = GrihaLaxmiAgent()
safetypriya_agent = SafetyPriyaAgent()
stockbull_agent = StockBullAgent()
mfhussain_agent = MFHussainAgent()
fdlover_agent = FDLoverAgent()
buddhiman_agent = BuddhimanAgent()
chitragupthan_agent = ChitragupthanAgent()
sarathy_agent = SarathyAgent()
viswakarma_agent = ViswakarmaAgent()
scheduler = FridayScheduler()

# Memory cache for fast browsing
cache = {
    "jasoos": None,
    "explorer": None,
    "grihalaxmi": None,
    "safetypriya": None,
    "stockbull": None,
    "mfhussain": None,
    "fdlover": None,
    "buddhiman": None,
    "chitragupthan": None,
    "sarathy": None,
    "viswakarma": None,
}

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True, parents=True)


class CapitalRequest(BaseModel):
    capital: float = 100000.0  # Default ₹1,00,000


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>5-Agent Investment Dashboard Loading...</h1>"


@app.get("/api/agent/jasoos")
async def get_jasoos(refresh: bool = False):
    try:
        if refresh or cache["jasoos"] is None:
            cache["jasoos"] = jasoos_agent.run_investigation()
        return cache["jasoos"]
    except Exception as e:
        if cache["jasoos"] is not None:
            return cache["jasoos"]
        raise HTTPException(status_code=500, detail=f"Jasoos Error: {e}")


@app.get("/api/agent/explorer")
async def get_explorer(refresh: bool = False):
    try:
        if refresh or cache["explorer"] is None:
            cache["explorer"] = explorer_agent.run_exploration()
        return cache["explorer"]
    except Exception as e:
        if cache["explorer"] is not None:
            return cache["explorer"]
        raise HTTPException(status_code=500, detail=f"Explorer Error: {e}")


@app.get("/api/agent/grihalaxmi")
async def get_grihalaxmi(refresh: bool = False):
    try:
        if refresh or cache["grihalaxmi"] is None:
            cache["grihalaxmi"] = grihalaxmi_agent.run_flow_analysis()
        return cache["grihalaxmi"]
    except Exception as e:
        if cache["grihalaxmi"] is not None:
            return cache["grihalaxmi"]
        raise HTTPException(status_code=500, detail=f"GrihaLaxmi Error: {e}")


@app.post("/api/agent/grihalaxmi/update-eod")
async def update_grihalaxmi_eod():
    """Triggers End-of-Day data extraction and updates the SQLite database."""
    try:
        res = grihalaxmi_agent.update_eod_flow_database()
        cache["grihalaxmi"] = grihalaxmi_agent.run_flow_analysis()
        return {"status": "success", "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EOD Update Error: {e}")


@app.get("/api/agent/safetypriya")
async def get_safetypriya(refresh: bool = False):
    try:
        if refresh or cache["safetypriya"] is None:
            cache["safetypriya"] = safetypriya_agent.run_safety_analysis()
        return cache["safetypriya"]
    except Exception as e:
        if cache["safetypriya"] is not None:
            return cache["safetypriya"]
        raise HTTPException(status_code=500, detail=f"SafetyPriya Error: {e}")


@app.get("/api/agent/stockbull")
async def get_stockbull(refresh: bool = False):
    try:
        if refresh or cache["stockbull"] is None:
            j = cache["jasoos"] or jasoos_agent.run_investigation()
            e = cache["explorer"] or explorer_agent.run_exploration()
            g = cache["grihalaxmi"] or grihalaxmi_agent.run_flow_analysis()
            s = cache["safetypriya"] or safetypriya_agent.run_safety_analysis()
            cache["stockbull"] = stockbull_agent.evaluate(j, e, g, s)
        return cache["stockbull"]
    except Exception as e:
        if cache["stockbull"] is not None:
            return cache["stockbull"]
        raise HTTPException(status_code=500, detail=f"StockBull Error: {e}")


@app.get("/api/agent/mfhussain")
async def get_mfhussain(refresh: bool = False):
    try:
        if refresh or cache["mfhussain"] is None:
            j = cache["jasoos"] or jasoos_agent.run_investigation()
            e = cache["explorer"] or explorer_agent.run_exploration()
            g = cache["grihalaxmi"] or grihalaxmi_agent.run_flow_analysis()
            s = cache["safetypriya"] or safetypriya_agent.run_safety_analysis()
            cache["mfhussain"] = mfhussain_agent.evaluate(j, e, g, s)
        return cache["mfhussain"]
    except Exception as e:
        if cache["mfhussain"] is not None:
            return cache["mfhussain"]
        raise HTTPException(status_code=500, detail=f"MFHussain Error: {e}")


@app.get("/api/agent/fdlover")
async def get_fdlover(refresh: bool = False):
    try:
        if refresh or cache["fdlover"] is None:
            j = cache["jasoos"] or jasoos_agent.run_investigation()
            e = cache["explorer"] or explorer_agent.run_exploration()
            g = cache["grihalaxmi"] or grihalaxmi_agent.run_flow_analysis()
            s = cache["safetypriya"] or safetypriya_agent.run_safety_analysis()
            cache["fdlover"] = fdlover_agent.evaluate(j, e, g, s)
        return cache["fdlover"]
    except Exception as e:
        if cache["fdlover"] is not None:
            return cache["fdlover"]
        raise HTTPException(status_code=500, detail=f"FDLover Error: {e}")


@app.get("/api/agent/chitragupthan")
async def get_chitragupthan(refresh: bool = False, capital: float = 100000.0):
    try:
        active_buddhiman = cache["buddhiman"]
        if refresh or cache["chitragupthan"] is None:
            cache["chitragupthan"] = chitragupthan_agent.run_simulation(capital=capital, active_buddhiman_data=active_buddhiman)
        return cache["chitragupthan"]
    except Exception as e:
        if cache["chitragupthan"] is not None:
            return cache["chitragupthan"]
        raise HTTPException(status_code=500, detail=f"Chitragupthan Error: {e}")


@app.get("/api/agent/sarathy")
async def get_sarathy(refresh: bool = False, capital: float = 100000.0):
    try:
        if refresh or cache["sarathy"] is None:
            cache["sarathy"] = sarathy_agent.run_assessment(capital=capital)
        return cache["sarathy"]
    except Exception as e:
        if cache["sarathy"] is not None:
            return cache["sarathy"]
        raise HTTPException(status_code=500, detail=f"Sarathy Error: {e}")


@app.get("/api/agent/viswakarma")
async def get_viswakarma(refresh: bool = False):
    try:
        if refresh or cache["viswakarma"] is None:
            cache["viswakarma"] = viswakarma_agent.run()
        return cache["viswakarma"]
    except Exception as e:
        if cache["viswakarma"] is not None:
            return cache["viswakarma"]
        raise HTTPException(status_code=500, detail=f"Viswakarma Error: {e}")


@app.get("/api/simulate")
async def simulate_portfolio(capital: float = 100000.0):
    try:
        active_buddhiman = cache["buddhiman"]
        return chitragupthan_agent.run_simulation(capital=capital, active_buddhiman_data=active_buddhiman)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation Error: {e}")


@app.get("/simulate", response_class=HTMLResponse)
async def serve_simulation_window():
    sim_file = STATIC_DIR / "simulation.html"
    if sim_file.exists():
        with open(sim_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>Chitragupthan simulation page not found</h2>", status_code=404)


@app.get("/api/synthesize")
async def run_synthesis(refresh: bool = True):
    try:
        if refresh or cache["buddhiman"] is None:
            res = buddhiman_agent.synthesize_all_agents()
            cache["buddhiman"] = res
            cache["jasoos"] = res["full_reports"]["jasoos"]
            cache["explorer"] = res["full_reports"]["explorer"]
            cache["grihalaxmi"] = res["full_reports"]["grihalaxmi"]
            cache["safetypriya"] = res["full_reports"]["safetypriya"]
            if "stockbull" in res["full_reports"]:
                cache["stockbull"] = res["full_reports"]["stockbull"]
            if "mfhussain" in res["full_reports"]:
                cache["mfhussain"] = res["full_reports"]["mfhussain"]
            if "fdlover" in res["full_reports"]:
                cache["fdlover"] = res["full_reports"]["fdlover"]
            cache["chitragupthan"] = None
        return cache["buddhiman"]
    except Exception as e:
        if cache["buddhiman"] is not None:
            return cache["buddhiman"]
        raise HTTPException(status_code=500, detail=f"Synthesis Error: {e}")


@app.post("/api/calculate-allocation")
async def calculate_allocation(req: CapitalRequest):
    """Calculates exact Rupee amounts and estimated units/shares for the 5 picks."""
    if cache["buddhiman"] is None:
        cache["buddhiman"] = buddhiman_agent.synthesize_all_agents()
    
    buddhiman_data = cache["buddhiman"]
    picks = buddhiman_data["five_actionable_picks"]
    total_capital = max(1000.0, req.capital)

    allocated_picks = []
    total_allocated = 0.0

    for p in picks:
        weight_pct = p["recommended_weight_pct"]
        target_amount = round(total_capital * (weight_pct / 100.0), 2)
        total_allocated += target_amount

        # Extract numerical price from reference string
        ref_str = p["entry_price_ref"]
        # Extract digits and decimal point
        num_str = "".join([c for c in ref_str if c.isdigit() or c == "."])
        try:
            unit_price = float(num_str) if num_str else 0.0
        except ValueError:
            unit_price = 0.0

        if unit_price > 0 and not p["type"].startswith("Fixed"):
            estimated_units = int(target_amount // unit_price)
            unit_type = "Shares" if "Stock" in p["type"] else ("ETF Units" if "ETF" in p["type"] else "MF Units")
        else:
            estimated_units = None
            unit_type = "Term Deposit"

        allocated_picks.append({
            **p,
            "allocated_rupees": target_amount,
            "estimated_units": estimated_units,
            "unit_type": unit_type,
            "unit_price_ref": unit_price
        })

    alloc_pct = buddhiman_data["allocation_percentages"]
    category_allocations = {
        "Stocks": {
            "pct": alloc_pct["Stocks"],
            "rupees": round(total_capital * (alloc_pct["Stocks"] / 100.0), 2)
        },
        "Mutual_Funds": {
            "pct": alloc_pct["Mutual_Funds"],
            "rupees": round(total_capital * (alloc_pct["Mutual_Funds"] / 100.0), 2)
        },
        "ETFs": {
            "pct": alloc_pct["ETFs"],
            "rupees": round(total_capital * (alloc_pct["ETFs"] / 100.0), 2)
        },
        "Fixed_Deposits": {
            "pct": alloc_pct["Fixed_Deposits"],
            "rupees": round(total_capital * (alloc_pct["Fixed_Deposits"] / 100.0), 2)
        }
    }

    return {
        "total_corpus": total_capital,
        "total_allocated": total_allocated,
        "picks": allocated_picks,
        "allocation_percentages": alloc_pct,
        "category_allocations": category_allocations,
        "regime": buddhiman_data["regime"],
        "monday_date": buddhiman_data["dates"]["upcoming_monday_action_date"]
    }


@app.post("/api/export")
async def export_dossier():
    saved_path = scheduler.run_friday_synthesis()
    return {"status": "success", "file_path": saved_path}


@app.get("/api/download-dossier")
async def download_dossier():
    """Returns the most recently generated Markdown dossier."""
    dossier_files = sorted(DOSSIER_DIR.glob("*.md"), key=os.path.getmtime, reverse=True)
    if not dossier_files:
        scheduler.run_friday_synthesis()
        dossier_files = sorted(DOSSIER_DIR.glob("*.md"), key=os.path.getmtime, reverse=True)
    
    latest_file = dossier_files[0]
    return FileResponse(
        path=latest_file,
        filename=latest_file.name,
        media_type="text/markdown"
    )


def start_server(port: int = DEFAULT_WEB_PORT, host: str = DEFAULT_WEB_HOST):
    import uvicorn
    uvicorn.run("web.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    start_server(port=DEFAULT_WEB_PORT)
