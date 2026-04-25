"""
survey_data.py
==============
HelioFold Powerbank – Telegram Poll Data
Survey question: "At what price would you buy this product?"
Total respondents: 85
"""

# Raw survey results from Telegram poll
# Format: {price_usd: vote_count}
RAW_VOTES = {
    5:  39,   # 46% → 39 votes
    8:  11,   # 13% → 11 votes
    10: 11,   # 13% → 11 votes
    12: 11,   # 13% → 11 votes
    15: 13,   # 15% → 13 votes
}

TOTAL_RESPONDENTS = 85

# Production cost per unit (USD) – assumed baseline
PRODUCTION_COST = 3  # $3 per unit baseline

def get_survey_data():
    """
    Returns survey data as sorted lists of prices and cumulative demand.

    Demand logic:
    If a consumer is willing to pay $X, they will also buy at any price <= X.
    So demand at each price = sum of votes for that price AND all higher prices.
    """
    prices = sorted(RAW_VOTES.keys())

    # Cumulative demand: willing to pay p means willing to pay anything <= p
    # So demand(p) = number of people who voted for p OR higher
    demand = []
    for p in prices:
        d = sum(v for price, v in RAW_VOTES.items() if price >= p)
        demand.append(d)

    return prices, demand

def print_survey_table():
    prices, demand = get_survey_data()
    print("=" * 55)
    print("  HelioFold Powerbank – Survey Results & Demand Table")
    print("=" * 55)
    print(f"{'Price ($)':>10} {'Votes':>8} {'Demand (cumul.)':>18}")
    print("-" * 55)
    for p in sorted(RAW_VOTES.keys()):
        d = sum(v for price, v in RAW_VOTES.items() if price >= p)
        print(f"{p:>10} {RAW_VOTES[p]:>8} {d:>18}")
    print("-" * 55)
    print(f"  Total respondents: {TOTAL_RESPONDENTS}")
    print("=" * 55)

if __name__ == "__main__":
    print_survey_table()
