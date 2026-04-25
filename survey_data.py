RAW_VOTES = {
    5:  39,   
    8:  11,   
    10: 11,   
    12: 11,  
    15: 13,   
}

TOTAL_RESPONDENTS = 85


PRODUCTION_COST = 3 

def get_survey_data():
  
    prices = sorted(RAW_VOTES.keys())

  
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
