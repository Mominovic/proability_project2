"""
main.py
=======
HelioFold Powerbank – Demand Analysis
======================================
Entry point. Runs the full analysis pipeline:
  1. Displays survey data table
  2. Computes and prints OLS regression results
  3. Computes and prints revenue / profit analysis
  4. Generates all charts → output/

Usage:
    python main.py

Requirements:
    pip install numpy matplotlib scipy
"""

import sys
import os

# Ensure sub-modules resolve correctly
BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, "data"))
sys.path.insert(0, os.path.join(BASE, "analysis"))

from survey_data   import print_survey_table
from regression    import print_regression_report
from revenue       import print_revenue_report
from visualizer    import generate_all


def run():
    print("\n" + "█" * 65)
    print("  HelioFold Powerbank – Full Demand Analysis")
    print("  Constructed from Telegram poll  (n = 85 respondents)")
    print("█" * 65)

    print("\n[1/4] SURVEY DATA")
    print_survey_table()

    print("\n[2/4] REGRESSION ANALYSIS")
    print_regression_report()

    print("\n[3/4] REVENUE & PROFIT ANALYSIS")
    print_revenue_report()

    print("\n[4/4] VISUALIZATIONS")
    generate_all()

    print("=" * 65)
    print("  ✅  Analysis complete. Charts saved to output/")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run()
