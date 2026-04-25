# HelioFold Powerbank – Demand Analysis

> **Independent Work No. 2 — Constructing the Demand Function**
> Business Idea: HelioFold Powerbank ☀️ | Solar-powered, foldable, smart charging

---

## 📊 Business Overview

**HelioFold** is a next-generation portable power bank featuring:
- 30,000 mAh capacity + 100W fast charging
- Foldable solar panels for off-grid recharging
- Smart OLED display with per-device control
- Auto-stop charging at custom thresholds (e.g. stop at 80%)

**Target market:** Travelers, campers, freelancers, digital nomads

---

## 📋 Survey

A Telegram poll was conducted with **85 respondents**.

**Question:** *"At what price would you buy this product?"*

| Price ($) | Votes | Share |
|-----------|-------|-------|
| $5        | 39    | 46%   |
| $8        | 11    | 13%   |
| $10       | 11    | 13%   |
| $12       | 11    | 13%   |
| $15       | 13    | 15%   |

---

## 🗂 Project Structure

```
heliofold-demand-analysis/
├── README.md
├── main.py                  ← Run this to execute full analysis
├── analysis/
│   ├── regression.py        ← OLS least squares method
│   ├── revenue.py           ← Revenue, profit, optimal price
│   └── visualizer.py        ← Chart generation (matplotlib)
├── data/
│   └── survey_data.py       ← Survey data + demand table builder
└── output/
    ├── demand_curve.png
    ├── revenue_profit.png
    └── sensitivity_analysis.png
```

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install numpy matplotlib scipy

# 2. Run full analysis
python main.py

# 3. Or run individual modules
python data/survey_data.py
python analysis/regression.py
python analysis/revenue.py
python analysis/visualizer.py
```

---

## 📐 Methodology

### 1. Demand Construction
Consumer demand is cumulative: a buyer willing to pay $15 will also buy at $5.  
So `D(p) = number of respondents who voted for price p OR higher`.

### 2. Regression (OLS)
Linear regression: `D(p) = b0 + b1·p`

| Parameter | Formula |
|-----------|---------|
| b1 (slope) | `Cov(x,y) / Var(x)` |
| b0 (intercept) | `ȳ − b1·x̄` |
| r (correlation) | `Cov(x,y) / (σx · σy)` |
| R² | `r²` |

### 3. Revenue & Profit
- Revenue: `R(p) = p × D(p)`
- Profit: `π(p) = (p − cost) × D(p)`
- Optimal price: price that maximises `π(p)`

---

## 📈 Key Results (Cost = $3/unit)

| Metric | Value |
|--------|-------|
| Demand function | D(p) = 92.07 − 5.46·p |
| R² | ≈ 0.97 |
| Optimal price | $5 |
| Max profit | $170 |
| Market coverage | 85/85 (100%) |

---

## 💡 Economic Insight

As production costs increase, the optimal price rises and optimal quantity falls.  
A small price increase can cause a large group of price-sensitive buyers to exit,  
dramatically reducing total profit — demonstrating the **microstructure of demand**.

---

*Analysis performed using Python (numpy, matplotlib). Data sourced from Telegram poll.*
