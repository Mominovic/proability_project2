import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

from survey_data import get_survey_data
import math


def compute_regression():
    """
    Performs manual OLS regression without using numpy/scipy (for transparency).
    Returns a dict with all computed parameters.
    """
    prices, demand = get_survey_data()
    n = len(prices)

    x = prices      
    y = demand      


    x_bar = sum(x) / n
    y_bar = sum(y) / n

   
    xy_bar = sum(xi * yi for xi, yi in zip(x, y)) / n
    x2_bar = sum(xi ** 2 for xi in x) / n
    y2_bar = sum(yi ** 2 for yi in y) / n

  
    var_x = x2_bar - x_bar ** 2
    var_y = y2_bar - y_bar ** 2
    sigma_x = math.sqrt(var_x)
    sigma_y = math.sqrt(var_y)

  
    cov_xy = xy_bar - x_bar * y_bar

 
    b1 = cov_xy / var_x        
    b0 = y_bar - b1 * x_bar      

    r = cov_xy / (sigma_x * sigma_y)

  
    R2 = r ** 2

    y_pred = [b0 + b1 * xi for xi in x]
    residuals = [yi - yp for yi, yp in zip(y, y_pred)]
    ss_res = sum(e ** 2 for e in residuals)
    ss_tot = sum((yi - y_bar) ** 2 for yi in y)

    return {
        "n": n,
        "prices": x,
        "demand": y,
        "x_bar": x_bar,
        "y_bar": y_bar,
        "xy_bar": xy_bar,
        "x2_bar": x2_bar,
        "y2_bar": y2_bar,
        "var_x": var_x,
        "var_y": var_y,
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "cov_xy": cov_xy,
        "b0": b0,
        "b1": b1,
        "r": r,
        "R2": R2,
        "y_pred": y_pred,
        "residuals": residuals,
        "ss_res": ss_res,
        "ss_tot": ss_tot,
    }


def print_regression_report():
    res = compute_regression()

    print("=" * 65)
    print("          LEAST SQUARES REGRESSION ANALYSIS")
    print("          HelioFold Powerbank Demand Function")
    print("=" * 65)

   
    print(f"\n{'i':>4} {'Price(x)':>10} {'Demand(y)':>12} {'x²':>10} {'xy':>12} {'ŷ':>10} {'e=y-ŷ':>10}")
    print("-" * 70)
    for i, (xi, yi, yp, e) in enumerate(
        zip(res["prices"], res["demand"], res["y_pred"], res["residuals"]), 1
    ):
        print(f"{i:>4} {xi:>10.1f} {yi:>12.1f} {xi**2:>10.1f} {xi*yi:>12.1f} {yp:>10.2f} {e:>10.2f}")

    print("-" * 70)
    print(f"{'Σ':>4} {sum(res['prices']):>10.1f} {sum(res['demand']):>12.1f} "
          f"{sum(x**2 for x in res['prices']):>10.1f} "
          f"{sum(x*y for x,y in zip(res['prices'],res['demand'])):>12.1f}")
    print(f"{'Mean':>4} {res['x_bar']:>10.2f} {res['y_bar']:>12.2f} "
          f"{res['x2_bar']:>10.2f} {res['xy_bar']:>12.2f}")

    print(f"\n{'─'*65}")
    print("  REGRESSION PARAMETERS")
    print(f"{'─'*65}")
    print(f"  x̄ (mean price)       = {res['x_bar']:.4f}")
    print(f"  ȳ (mean demand)      = {res['y_bar']:.4f}")
    print(f"  σx (std dev price)   = {res['sigma_x']:.4f}")
    print(f"  σy (std dev demand)  = {res['sigma_y']:.4f}")
    print(f"  Cov(x,y)             = {res['cov_xy']:.4f}")
    print(f"  b1 (slope)           = {res['b1']:.4f}")
    print(f"  b0 (intercept)       = {res['b0']:.4f}")
    print(f"  r  (correlation)     = {res['r']:.4f}")
    print(f"  R² (determination)   = {res['R2']:.4f}")
    print(f"\n  ✦ Demand Function:  D(p) = {res['b0']:.2f} + ({res['b1']:.4f}) × p")
    print(f"                             = {res['b0']:.2f} - {abs(res['b1']):.4f} × p")
    print(f"\n  ✦ R² = {res['R2']:.4f}  →  {res['R2']*100:.1f}% of demand variation")
    print(f"         explained by price")
    print("=" * 65)


if __name__ == "__main__":
    print_regression_report()
