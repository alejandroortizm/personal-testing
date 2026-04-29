import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

SQL = """
SELECT
    region,
    product,
    SUM(quantity)                        AS total_units,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    COUNT(*)                             AS num_transactions
FROM sales
GROUP BY region, product
ORDER BY total_revenue DESC;
"""

@st.cache_data
def run_sql_and_get_df():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE sales (
            id         INTEGER PRIMARY KEY,
            region     TEXT,
            product    TEXT,
            quantity   INTEGER,
            unit_price REAL,
            sale_date  TEXT
        );
        INSERT INTO sales VALUES
            (1,  'North', 'Widget A', 120, 9.99,  '2024-01-05'),
            (2,  'South', 'Widget B',  85, 14.99, '2024-01-08'),
            (3,  'East',  'Widget A',  60, 9.99,  '2024-01-12'),
            (4,  'West',  'Widget C', 200, 4.99,  '2024-01-15'),
            (5,  'North', 'Widget B',  45, 14.99, '2024-02-03'),
            (6,  'South', 'Widget C', 310, 4.99,  '2024-02-10'),
            (7,  'East',  'Widget B',  70, 14.99, '2024-02-18'),
            (8,  'West',  'Widget A',  95, 9.99,  '2024-02-22'),
            (9,  'North', 'Widget C', 150, 4.99,  '2024-03-01'),
            (10, 'South', 'Widget A',  80, 9.99,  '2024-03-14'),
            (11, 'East',  'Widget C', 240, 4.99,  '2024-03-20'),
            (12, 'West',  'Widget B',  55, 14.99, '2024-03-28');
    """)
    df = pd.read_sql_query(SQL, conn)
    conn.close()
    return df

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Dashboard")
st.markdown("Data pipeline: **SQLite (in-memory) → SQL query → DataFrame → Streamlit**")
st.markdown("---")

if st.button("Re-run SQL query & refresh"):
    st.cache_data.clear()
    st.rerun()

# ── Load data ──────────────────────────────────────────────────────────────────
df = run_sql_and_get_df()
df["avg_unit_revenue"] = (df["total_revenue"] / df["total_units"]).round(2)

region_summary = (
    df.groupby("region")
    .agg(total_revenue=("total_revenue", "sum"), total_units=("total_units", "sum"))
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)
product_summary = (
    df.groupby("product")
    .agg(total_revenue=("total_revenue", "sum"), total_units=("total_units", "sum"))
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${df['total_revenue'].sum():,.2f}")
k2.metric("Total Units Sold", f"{df['total_units'].sum():,}")
k3.metric("Regions", df["region"].nunique())
k4.metric("Products", df["product"].nunique())

st.markdown("---")

# ── Charts ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    fig1 = px.bar(region_summary, x="region", y="total_revenue",
                  color="region", text_auto=".2s",
                  labels={"total_revenue": "Revenue ($)", "region": "Region"})
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Revenue by Product")
    fig2 = px.pie(product_summary, names="product", values="total_revenue", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Units Sold by Region & Product")
fig3 = px.bar(df, x="region", y="total_units", color="product", barmode="group",
              labels={"total_units": "Units Sold", "region": "Region"})
st.plotly_chart(fig3, use_container_width=True)

# ── Raw data + download ────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Raw SQL Result")
st.dataframe(df, use_container_width=True)

st.download_button("Download as CSV", df.to_csv(index=False).encode(), "test.csv", "text/csv")
