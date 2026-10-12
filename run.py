"""
Main entry point for 5-Agent Indian Fund Deployment Advisory System.
Usage:
  py run.py --web      # Starts interactive Web Dashboard on Port 8010 and opens browser
  py run.py --cli      # Runs command-line interface
  py run.py --friday   # Runs Friday evaluation & exports Monday dossier
"""

import sys
import argparse
import webbrowser
import threading
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from config import DEFAULT_WEB_PORT, DEFAULT_WEB_HOST

def open_browser_delayed(url: str, delay: float = 1.2):
    time.sleep(delay)
    webbrowser.open(url)

def main():
    parser = argparse.ArgumentParser(description="5-Agent Indian Fund Deployment Advisory Web App")
    parser.add_argument("--web", action="store_true", help=f"Launch FastAPI web dashboard on port {DEFAULT_WEB_PORT}")
    parser.add_argument("--cli", action="store_true", help="Run interactive CLI")
    parser.add_argument("--friday", action="store_true", help="Trigger Friday-to-Monday dossier synthesis")
    parser.add_argument("--port", type=int, default=DEFAULT_WEB_PORT, help=f"Web server port (default: {DEFAULT_WEB_PORT})")
    parser.add_argument("--no-browser", action="store_true", help="Do not open web browser automatically")

    args = parser.parse_args()

    if args.web or (not args.cli and not args.friday):
        # Default action is now to launch the Web App!
        import uvicorn
        target_url = f"http://{DEFAULT_WEB_HOST}:{args.port}"
        print("=" * 70)
        print("🚀 LAUNCHING 5-AGENT ADVISORY WEB APPLICATION")
        print("=" * 70)
        print(f"👉 Local URL: {target_url}")
        print("Press Ctrl+C to stop the web server.")
        
        if not args.no_browser:
            threading.Thread(target=open_browser_delayed, args=(target_url,), daemon=True).start()

        uvicorn.run("web.server:app", host=DEFAULT_WEB_HOST, port=args.port, reload=False)

    elif args.friday:
        from scheduler import FridayScheduler
        scheduler = FridayScheduler()
        scheduler.run_friday_synthesis()
    elif args.cli:
        from cli import run_buddhiman
        run_buddhiman(export=False)

if __name__ == "__main__":
    main()
