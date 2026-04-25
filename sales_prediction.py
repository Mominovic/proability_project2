import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

dates = ["2024.1.1", "2024.1.2", "2024.1.3", "2024.1.4", "2024.1.5", "2024.1.6"]
temperatures = [5, 7, 10, 8, 11, 9]
sales = [15, 21, 30, 20, 33, None]

X_train = np.array(temperatures[:-1]).reshape(-1, 1)
y_train = np.array(sales[:-1])
X_predict = np.array([[temperatures[-1]]])

model = LinearRegression()
model.fit(X_train, y_train)

predicted_sales = model.predict(X_predict)[0]
y_pred_train = model.predict(X_train)

mse = mean_squared_error(y_train, y_pred_train)
r2 = r2_score(y_train, y_pred_train)

print("=" * 45)
print("   SALES PREDICTION - LINEAR REGRESSION")
print("=" * 45)
print(f"\n{'Date':<12} {'Temperature':>12} {'Sales':>8}")
print("-" * 35)
for i in range(len(dates) - 1):
    print(f"{dates[i]:<12} {temperatures[i]:>12} {sales[i]:>8}")
print(f"{dates[-1]:<12} {temperatures[-1]:>12} {'?':>8}")
print("-" * 35)

print(f"\nModel Coefficients:")
print(f"  Slope     : {model.coef_[0]:.4f}")
print(f"  Intercept : {model.intercept_:.4f}")
print(f"\nModel Performance:")
print(f"  R² Score  : {r2:.4f}")
print(f"  MSE       : {mse:.4f}")

print(f"\nPrediction for 2024.1.6 (Temperature=9):")
print(f"  Predicted Sales = {predicted_sales:.2f}")
print("=" * 45)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Sales Prediction using Linear Regression", fontsize=14, fontweight="bold")

ax1 = axes[0]
temp_range = np.linspace(min(temperatures) - 1, max(temperatures) + 1, 100).reshape(-1, 1)
ax1.plot(temp_range, model.predict(temp_range), color="#2196F3", linewidth=2, label="Regression Line")
ax1.scatter(X_train, y_train, color="#FF5722", s=80, zorder=5, label="Training Data")
ax1.scatter(X_predict, predicted_sales, color="#4CAF50", s=120, zorder=6, marker="*", label=f"Prediction: {predicted_sales:.1f}")
ax1.set_xlabel("Temperature (°C)")
ax1.set_ylabel("Sales")
ax1.set_title("Temperature vs Sales")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[1]
bar_colors = ["#2196F3"] * 5 + ["#4CAF50"]
all_sales = list(sales[:-1]) + [predicted_sales]
bars = ax2.bar(range(len(dates)), all_sales, color=bar_colors, edgecolor="white", linewidth=1.2)
ax2.set_xticks(range(len(dates)))
ax2.set_xticklabels([d.split(".")[-1] for d in dates], fontsize=9)
ax2.set_xlabel("Day (January 2024)")
ax2.set_ylabel("Sales")
ax2.set_title("Daily Sales (Blue=Actual, Green=Predicted)")
ax2.grid(True, axis="y", alpha=0.3)
for bar, val in zip(bars, all_sales):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f"{val:.1f}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("/home/claude/sales_chart.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart saved: sales_chart.png")
