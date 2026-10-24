"""Analyze the daily pharmaceutical sales by ATC category."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).parent
DATA_FILE = PROJECT_DIR / "data" / "salesdaily.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
DRUG_CATEGORIES = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
PERIODS = {
    "January 2015": ("2015-01-01", "2015-02-01"),
    "July 2016": ("2016-07-01", "2016-08-01"),
    "September 2017": ("2017-09-01", "2017-10-01"),
}


def load_sales_data(path: Path = DATA_FILE) -> pd.DataFrame:
    """Load daily sales, parse dates and numeric fields, and remove incomplete rows."""
    if not path.exists():
        raise FileNotFoundError(
            "Dataset not found. Download salesdaily.csv from the Kaggle source "
            "listed in README.md and save it as data/salesdaily.csv."
        )

    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    if "datum" not in data.columns:
        raise ValueError("Expected a 'datum' date column in salesdaily.csv.")
    missing_categories = sorted(set(DRUG_CATEGORIES) - set(data.columns))
    if missing_categories:
        raise ValueError(f"Missing ATC category columns: {', '.join(missing_categories)}")

    data = data.rename(columns={"datum": "Date"})
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y", errors="coerce")
    for category in DRUG_CATEGORIES:
        data[category] = pd.to_numeric(data[category], errors="coerce")

    data = data.dropna(subset=["Date", *DRUG_CATEGORIES])
    data = data.drop_duplicates(subset="Date", keep="last").sort_values("Date").reset_index(drop=True)
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month
    return data


def total_sales_by_category(data: pd.DataFrame) -> pd.Series:
    """Sum the daily quantity for each ATC category."""
    return data[DRUG_CATEGORIES].sum().sort_values(ascending=False)


def top_categories_for_period(data: pd.DataFrame, start: str, end: str) -> pd.Series:
    """Rank ATC categories by total sales in a half-open date interval."""
    period = data.loc[(data["Date"] >= start) & (data["Date"] < end)]
    if period.empty:
        return pd.Series(dtype="float64", name="Sales")
    return period[DRUG_CATEGORIES].sum().sort_values(ascending=False).head(3)


def average_daily_sales_by_category(data: pd.DataFrame) -> pd.Series:
    """Average daily quantity for each ATC category, including zero-sale days."""
    return data[DRUG_CATEGORIES].mean().sort_values(ascending=False)


def respiratory_sales_by_month(data: pd.DataFrame) -> pd.Series:
    """Compare average daily R03 sales across calendar months and years."""
    return data.groupby("Month")["R03"].mean().reindex(range(1, 13))


def save_outputs(data: pd.DataFrame) -> None:
    """Write summary tables and two plots to the outputs folder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total_sales_by_category(data).rename("Total Sales").to_csv(OUTPUT_DIR / "sales_by_category.csv")

    period_rows = []
    for period_name, (start, end) in PERIODS.items():
        ranked = top_categories_for_period(data, start, end)
        for rank, (category, sales) in enumerate(ranked.items(), start=1):
            period_rows.append({"Period": period_name, "Rank": rank, "ATC Category": category, "Sales": sales})
    pd.DataFrame(period_rows).to_csv(OUTPUT_DIR / "top_categories_by_period.csv", index=False)

    totals = total_sales_by_category(data).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(totals.index, totals.values, color="#3867d6")
    ax.set(title="Total Sales by ATC Drug Category", xlabel="Sales quantity", ylabel="ATC category")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "sales_by_category.png", dpi=160)
    plt.close(fig)

    average_daily_sales_by_category(data).rename("Average Daily Sales").to_csv(
        OUTPUT_DIR / "average_daily_sales_by_category.csv"
    )

    monthly = respiratory_sales_by_month(data)
    monthly.rename("Average Daily R03 Sales").to_csv(OUTPUT_DIR / "r03_average_by_month.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly.index, monthly.values, marker="o", linewidth=2, color="#20a779")
    ax.set_xticks(range(1, 13))
    ax.set(title="Average Daily R03 Sales by Month", xlabel="Month", ylabel="Average daily sales quantity")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "r03_monthly_sales.png", dpi=160)
    plt.close(fig)


def main() -> None:
    data = load_sales_data()
    save_outputs(data)

    print(f"Rows: {len(data):,} | Date range: {data['Date'].min():%Y-%m-%d} to {data['Date'].max():%Y-%m-%d}")
    print("\nTotal sales by ATC category:")
    print(total_sales_by_category(data).to_string())
    print("\nTop three ATC categories in the requested periods:")
    for period_name, (start, end) in PERIODS.items():
        print(f"\n{period_name}:")
        print(top_categories_for_period(data, start, end).to_string())
    print("\nTop category in 2017:")
    print(data.loc[data["Year"] == 2017, DRUG_CATEGORIES].sum().sort_values(ascending=False).head(1).to_string())
    print("\nHighest average daily category:")
    print(average_daily_sales_by_category(data).head(1).to_string())
    monthly = respiratory_sales_by_month(data)
    print(f"\nR03 highest average month: {monthly.idxmax()} ({monthly.max():.2f} per day)")
    print(f"\nSummary tables and plots saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

