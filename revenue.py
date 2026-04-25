import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

from survey_data import get_survey_data, PRODUCTION_COST


def compute_revenue_table(cost=PRODUCTION_COST):
  
    prices, demand = get_survey_data()
    results = []
    for p, d in zip(prices, demand):
        revenue = p * d
        profit_per_unit = p - cost
        total_profit = profit_per_unit * d
        results.append({
            "price": p,
            "demand": d,
            "revenue": revenue,
            "cost": cost,
            "profit_per_unit": profit_per_unit,
            "total_profit": total_profit,
        })
    return results


def find_optimal(cost=PRODUCTION_COST):
    table = compute_revenue_table(cost)
    optimal = max(table, key=lambda row: row["total_profit"])
    return optimal


def sensitivity_analysis():
  
    costs = [1, 2, 3, 4, 5, 6, 7, 8]
    results = []
    for c in costs:
        opt = find_optimal(c)
        results.append({
            "cost": c,
            "optimal_quantity": opt["demand"],
            "optimal_price": opt["price"],
            "max_profit": opt["total_profit"],
            "max_revenue": opt["revenue"],
        })
    return results


def print_revenue_report(cost=PRODUCTION_COST):
    table = compute_revenue_table(cost)
    optimal = find_optimal(cost)

    print("-" * 75)
    print(f"  REVENUE & PROFIT ANALYSIS  |  Production Cost = ${cost}/unit")
    print("-" * 75)
    print(f"{'Price($)':>10} {'Demand':>8} {'Revenue($)':>12} "
          f"{'Profit/unit($)':>16} {'Total Profit($)':>16}")
    print("-" * 75)
    for row in table:
        marker = "  MAX PROFIT" if row["price"] == optimal["price"] else ""
        print(f"{row['price']:>10} {row['demand']:>8} {row['revenue']:>12} "
              f"{row['profit_per_unit']:>16} {row['total_profit']:>16}{marker}")
    print("-" * 75)
    print(f"\n   OPTIMAL PRICE:     ${optimal['price']}")
    print(f"   OPTIMAL QUANTITY:  {optimal['demand']} units")
    print(f"   MAXIMUM REVENUE:   ${optimal['revenue']}")
    print(f"   MAXIMUM PROFIT:    ${optimal['total_profit']}")
    print(f"   MARKET COVERAGE:   {optimal['demand']}/85 respondents "
          f"({optimal['demand']/85*100:.1f}%)")
    print("-" * 75)

    print("\n  SENSITIVITY ANALYSIS: Optimal Price & Quantity by Production Cost")
    print("-" * 75)
    sens = sensitivity_analysis()
    print(f"{'Cost($)':>10} {'Opt. Qty':>10} {'Opt. Price($)':>15} "
          f"{'Max Profit($)':>15} {'Max Revenue($)':>15}")
    print("-" * 75)
    for row in sens:
        print(f"{row['cost']:>10} {row['optimal_quantity']:>10} "
              f"{row['optimal_price']:>15} {row['max_profit']:>15} "
              f"{row['max_revenue']:>15}")
    print("-" * 75)


if __name__ == "__main__":
    print_revenue_report()
