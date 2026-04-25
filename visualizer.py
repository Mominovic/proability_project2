import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
sys.path.insert(0, os.path.dirname(__file__))

from survey_data import get_survey_data, PRODUCTION_COST
from regression import compute_regression
from revenue import compute_revenue_table, sensitivity_analysis

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GOLD    = "#F5A623"
NAVY    = "#1A2B4A"
TEAL    = "#00B4B1"
LIGHT   = "#F7F9FC"
RED     = "#E74C3C"
GREEN   = "#27AE60"
GREY    = "#7F8C8D"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.facecolor":    LIGHT,
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "grid.alpha":        0.4,
    "grid.linestyle":    "--",
})

def plot_demand_curve():
    res = compute_regression()
    prices = res["prices"]
    demand = res["demand"]
    b0, b1, R2 = res["b0"], res["b1"], res["R2"]

    x_line = np.linspace(min(prices) - 1, max(prices) + 1, 300)
    y_line = b0 + b1 * x_line

    fig, ax = plt.subplots(figsize=(9, 6))

 
    ax.plot(x_line, y_line, color=NAVY, linewidth=2.2, zorder=2,
            label=f"D(p) = {b0:.2f} − {abs(b1):.4f}·p")

  
    ax.scatter(prices, demand, color=GOLD, s=120, zorder=5,
               edgecolors=NAVY, linewidths=1.2, label="Survey data points")

  
    ax.scatter(prices, res["y_pred"], color=TEAL, s=60, zorder=4,
               marker="D", label="Predicted values")

    for xi, yi, yp in zip(prices, demand, res["y_pred"]):
        ax.plot([xi, xi], [yi, yp], color=RED, linewidth=0.8,
                linestyle=":", alpha=0.7)

    ax.text(0.97, 0.95,
            f"D(p) = {b0:.2f} − {abs(b1):.4f}·p\nR² = {R2:.4f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=NAVY, alpha=0.9))

    ax.set_xlabel("Price (USD)", fontsize=12, color=NAVY)
    ax.set_ylabel("Demand (number of buyers)", fontsize=12, color=NAVY)
    ax.set_title("HelioFold Powerbank – Demand Function\n(Least Squares Method)",
                 fontsize=14, fontweight="bold", color=NAVY, pad=14)
    ax.legend(frameon=True, framealpha=0.9, fontsize=9)
    ax.set_xlim(3, 17)
    ax.set_ylim(0, max(demand) * 1.18)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "demand_curve.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Saved: {path}")


def plot_revenue_profit():
    table = compute_revenue_table(PRODUCTION_COST)
    prices    = [r["price"]        for r in table]
    revenues  = [r["revenue"]      for r in table]
    profits   = [r["total_profit"] for r in table]

    max_profit_price = max(table, key=lambda r: r["total_profit"])["price"]
    max_rev_price    = max(table, key=lambda r: r["revenue"])["price"]

    x = np.arange(len(prices))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars_r = ax.bar(x - width/2, revenues, width, label="Revenue ($)",
                    color=TEAL, alpha=0.85, edgecolor="white", linewidth=0.6)
    bars_p = ax.bar(x + width/2, profits, width, label="Total Profit ($)",
                    color=GOLD, alpha=0.85, edgecolor="white", linewidth=0.6)

  
    for i, price in enumerate(prices):
        if price == max_profit_price:
            bars_p[i].set_edgecolor(RED)
            bars_p[i].set_linewidth(2.5)
            ax.annotate(f"Max Profit\n${profits[i]}",
                        xy=(x[i] + width/2, profits[i]),
                        xytext=(x[i] + width/2, profits[i] + 8),
                        ha="center", fontsize=8.5, color=RED, fontweight="bold")
        if price == max_rev_price:
            bars_r[i].set_edgecolor(NAVY)
            bars_r[i].set_linewidth(2.5)

   
    for bar in bars_r:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"${bar.get_height():.0f}", ha="center", va="bottom",
                fontsize=7.5, color=NAVY)
    for bar in bars_p:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"${bar.get_height():.0f}", ha="center", va="bottom",
                fontsize=7.5, color="#6B4E00")

    ax.set_xticks(x)
    ax.set_xticklabels([f"${p}" for p in prices])
    ax.set_xlabel("Price (USD)", fontsize=12, color=NAVY)
    ax.set_ylabel("Amount (USD)", fontsize=12, color=NAVY)
    ax.set_title(f"HelioFold Powerbank – Revenue & Profit Analysis\n"
                 f"(Production Cost = ${PRODUCTION_COST}/unit)",
                 fontsize=14, fontweight="bold", color=NAVY, pad=14)
    ax.legend(fontsize=10)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "revenue_profit.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Saved: {path}")



def plot_sensitivity():
    sens = sensitivity_analysis()
    costs  = [r["cost"]             for r in sens]
    qtys   = [r["optimal_quantity"] for r in sens]
    prices = [r["optimal_price"]    for r in sens]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()

    ax1.bar(costs, qtys, color=TEAL, alpha=0.75, label="Optimal Quantity",
            edgecolor="white", width=0.6)
    ax2.plot(costs, prices, color=GOLD, linewidth=2.5, marker="o",
             markersize=8, label="Optimal Price ($)", zorder=5)

    for c, q, p in zip(costs, qtys, prices):
        ax1.text(c, q + 0.5, str(q), ha="center", fontsize=8.5, color=NAVY)
        ax2.text(c, p + 0.15, f"${p}", ha="center", fontsize=8.5,
                 color="#B8860B", fontweight="bold")

    ax1.set_xlabel("Production Cost (USD/unit)", fontsize=12, color=NAVY)
    ax1.set_ylabel("Optimal Quantity (units)", fontsize=12, color=TEAL)
    ax2.set_ylabel("Optimal Price (USD)", fontsize=12, color=GOLD)
    ax1.set_title("HelioFold – Sensitivity Analysis\n"
                  "Optimal Quantity & Price vs Production Cost",
                  fontsize=14, fontweight="bold", color=NAVY, pad=14)

    lines1 = [mpatches.Patch(color=TEAL,  alpha=0.75, label="Optimal Quantity")]
    lines2 = [plt.Line2D([0], [0], color=GOLD, linewidth=2.5,
                          marker="o", label="Optimal Price ($)")]
    ax1.legend(handles=lines1 + lines2, loc="upper right", fontsize=9)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "sensitivity_analysis.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Saved: {path}")


def generate_all():
    print("\n  Generating charts …")
    plot_demand_curve()
    plot_revenue_profit()
    plot_sensitivity()
    print("  All charts saved to output/\n")


if __name__ == "__main__":
    generate_all()
