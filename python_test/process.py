import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "test.csv")

def load_and_process():
    df = pd.read_csv(CSV_PATH)

    df["avg_unit_revenue"] = (df["total_revenue"] / df["total_units"]).round(2)

    region_summary = (
        df.groupby("region")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_units=("total_units", "sum"),
            num_products=("product", "nunique"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    product_summary = (
        df.groupby("product")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_units=("total_units", "sum"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    return df, region_summary, product_summary

if __name__ == "__main__":
    df, region_summary, product_summary = load_and_process()
    print("=== Raw CSV ===")
    print(df.to_string(index=False))
    print("\n=== By Region ===")
    print(region_summary.to_string(index=False))
    print("\n=== By Product ===")
    print(product_summary.to_string(index=False))
