"""
Corporate Bonds and Fixed Deposits Scouting Engine:
- Scouts top Scheduled Commercial Bank FDs, AAA-rated Corporate FDs, and AAA Corporate/PSU Bonds in India.
- Evaluates coupon yields, credit ratings, tenures, and capital safety profiles for FDLover Agent.
"""

from typing import List, Dict, Any


CORPORATE_BONDS_AND_FDS = [
    {
        "id": "BAJAJ_FD",
        "issuer": "Bajaj Finance Ltd",
        "instrument_type": "Corporate Fixed Deposit",
        "rating": "CRISIL AAA / ICRA AAA (Highest Safety)",
        "tenure": "24 - 36 Months",
        "tenure_months": 36,
        "annual_interest_rate": 8.10,
        "senior_citizen_rate": 8.35,
        "payout_frequency": "Cumulative / Monthly / Quarterly",
        "min_investment": 15000,
        "security_type": "Unsecured Deposit / NBFC Leader",
        "safety_rationale": "Highest credit quality NBFC in India with negligible NPA ratios and stellar multi-decade track record."
    },
    {
        "id": "SHRIRAM_FD",
        "issuer": "Shriram Finance Ltd",
        "instrument_type": "Corporate Fixed Deposit",
        "rating": "CRISIL AA+ / India Ratings AA+ (High Safety)",
        "tenure": "36 - 60 Months",
        "tenure_months": 36,
        "annual_interest_rate": 8.60,
        "senior_citizen_rate": 9.10,
        "payout_frequency": "Cumulative / Half-Yearly / Monthly",
        "min_investment": 10000,
        "security_type": "Secured Corporate Deposit",
        "safety_rationale": "Market-leading yield of 8.60% (9.10% for seniors) backed by retail commercial asset collateral."
    },
    {
        "id": "HDFC_BANK_FD",
        "issuer": "HDFC Bank Ltd",
        "instrument_type": "Bank Fixed Deposit",
        "rating": "Sovereign / D-SIB Systemically Important (DICGC Insured)",
        "tenure": "15 - 24 Months",
        "tenure_months": 18,
        "annual_interest_rate": 7.10,
        "senior_citizen_rate": 7.60,
        "payout_frequency": "Quarterly Compounding / Monthly",
        "min_investment": 5000,
        "security_type": "Bank Term Deposit (RBI Insured up to Rs. 5 Lakh)",
        "safety_rationale": "Largest private bank in India; domestic systemically important bank (D-SIB) with zero default probability."
    },
    {
        "id": "NABARD_BOND",
        "issuer": "National Bank for Agriculture and Rural Development (NABARD)",
        "instrument_type": "AAA PSU Sovereign-Backed Corporate Bond",
        "rating": "CRISIL AAA / ICRA AAA (Govt of India Ownership)",
        "tenure": "3 - 5 Years",
        "tenure_months": 36,
        "annual_interest_rate": 7.42,
        "senior_citizen_rate": 7.42,
        "payout_frequency": "Annual Coupon",
        "min_investment": 10000,
        "security_type": "Secured Non-Convertible Debenture (NCD)",
        "safety_rationale": "Statutory quasi-sovereign development bank fully owned by the Government of India; virtually sovereign credit risk."
    },
    {
        "id": "REC_BOND",
        "issuer": "REC Limited (Rural Electrification Corp)",
        "instrument_type": "AAA Maharatna PSU Bond",
        "rating": "CARE AAA / CRISIL AAA / ICRA AAA",
        "tenure": "3 - 5 Years",
        "tenure_months": 36,
        "annual_interest_rate": 7.55,
        "senior_citizen_rate": 7.55,
        "payout_frequency": "Annual Coupon / Semi-Annual",
        "min_investment": 10000,
        "security_type": "Listed Secured Debenture (NSE/BSE)",
        "safety_rationale": "Maharatna Central Public Sector Undertaking providing power infrastructure financing; zero historical default."
    },
    {
        "id": "LT_FIN_BOND",
        "issuer": "L&T Finance Holdings Ltd",
        "instrument_type": "AAA Corporate Secured NCD / Bond",
        "rating": "CRISIL AAA / CARE AAA",
        "tenure": "24 - 36 Months",
        "tenure_months": 24,
        "annual_interest_rate": 8.15,
        "senior_citizen_rate": 8.15,
        "payout_frequency": "Annual / Cumulative",
        "min_investment": 10000,
        "security_type": "Secured Corporate Bond",
        "safety_rationale": "Backed by Larsen & Toubro parentage with top-tier AAA rating and prime liquidity on exchange debt segments."
    },
    {
        "id": "ICICI_BANK_FD",
        "issuer": "ICICI Bank Ltd",
        "instrument_type": "Bank Fixed Deposit",
        "rating": "D-SIB Systemically Important (DICGC Insured)",
        "tenure": "12 - 24 Months",
        "tenure_months": 15,
        "annual_interest_rate": 7.20,
        "senior_citizen_rate": 7.75,
        "payout_frequency": "Quarterly Compounding",
        "min_investment": 10000,
        "security_type": "Bank Term Deposit",
        "safety_rationale": "Premier private bank with top-tier capital adequacy and high return on assets."
    },
    {
        "id": "SBI_AMRIT_FD",
        "issuer": "State Bank of India (SBI) - Amrit Vrishti / Term Deposit",
        "instrument_type": "Public Sector Bank Fixed Deposit",
        "rating": "Sovereign Proxy (Govt of India Majority Owned)",
        "tenure": "444 Days / 1-2 Years",
        "tenure_months": 15,
        "annual_interest_rate": 7.25,
        "senior_citizen_rate": 7.75,
        "payout_frequency": "Quarterly Compounding",
        "min_investment": 1000,
        "security_type": "Sovereign-backed Bank Term Deposit",
        "safety_rationale": "Nation's largest public sector bank backed by sovereign ownership and pan-India safety."
    }
]


class CorporateBondsEngine:
    def __init__(self):
        self.options = CORPORATE_BONDS_AND_FDS

    def get_all_options(self) -> List[Dict[str, Any]]:
        return self.options

    def get_top_5_fixed_income_options(self) -> List[Dict[str, Any]]:
        """
        Curates the top 5 fixed income & corporate bond options optimizing for
        yield, AAA credit rating, and institutional diversification.
        """
        # Ensure a balanced mix:
        # 1. Highest Yield Corporate FD (e.g. Shriram Finance @ 8.60%)
        # 2. AAA Flagship Corporate FD (e.g. Bajaj Finance @ 8.10%)
        # 3. AAA Secured Corporate Bond (e.g. L&T Finance @ 8.15%)
        # 4. AAA Quasi-Sovereign PSU Bond (e.g. REC Ltd @ 7.55% or NABARD @ 7.42%)
        # 5. D-SIB Systemically Important Bank FD (e.g. HDFC Bank @ 7.10% / SBI @ 7.25%)
        selected_ids = ["SHRIRAM_FD", "BAJAJ_FD", "LT_FIN_BOND", "REC_BOND", "SBI_AMRIT_FD"]
        curated = [opt for opt in self.options if opt["id"] in selected_ids]
        
        # Sort by annual interest rate descending
        curated.sort(key=lambda x: x["annual_interest_rate"], reverse=True)
        return curated
