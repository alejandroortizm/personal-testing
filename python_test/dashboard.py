import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# ── Path helpers (required for DSW / NFS) ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv(filename):
    """Load a CSV from the same folder as this script (NFS-safe)."""
    return pd.read_csv(os.path.join(BASE_DIR, filename))

# ── Inline SQL query (runs in-memory, no file needed) ─────────────────────────
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
def run_sql():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY, region TEXT, product TEXT,
            quantity INTEGER, unit_price REAL, sale_date TEXT
        );
        INSERT INTO sales VALUES
            (1,'North','Widget A',120,9.99,'2024-01-05'),
            (2,'South','Widget B',85,14.99,'2024-01-08'),
            (3,'East','Widget A',60,9.99,'2024-01-12'),
            (4,'West','Widget C',200,4.99,'2024-01-15'),
            (5,'North','Widget B',45,14.99,'2024-02-03'),
            (6,'South','Widget C',310,4.99,'2024-02-10'),
            (7,'East','Widget B',70,14.99,'2024-02-18'),
            (8,'West','Widget A',95,9.99,'2024-02-22'),
            (9,'North','Widget C',150,4.99,'2024-03-01'),
            (10,'South','Widget A',80,9.99,'2024-03-14'),
            (11,'East','Widget C',240,4.99,'2024-03-20'),
            (12,'West','Widget B',55,14.99,'2024-03-28');
    """)
    df = pd.read_sql_query(SQL, conn)
    conn.close()
    return df

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Dashboard")
st.markdown("Data pipeline: **SQLite (in-memory) → SQL query → DataFrame → Streamlit**")
st.markdown("---")

# ── Data source selector ───────────────────────────────────────────────────────
source = st.sidebar.radio(
    "Data source",
    ["SQL (built-in sample)", "Upload a CSV", "Load CSV from NFS folder"],
)

if source == "SQL (built-in sample)":
    if st.sidebar.button("Re-run SQL query"):
        st.cache_data.clear()
        st.rerun()
    df = run_sql()

elif source == "Upload a CSV":
    uploaded = st.sidebar.file_uploader("Upload your CSV", type="csv")
    if uploaded is None:
        st.info("Upload a CSV file from the sidebar to get started.")
        st.stop()
    df = pd.read_csv(uploaded)

else:  # Load from NFS folder
    csv_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".csv")]
    if not csv_files:
        st.warning(f"No CSV files found next to dashboard.py ({BASE_DIR}). Drop one there and refresh.")
        st.stop()
    chosen = st.sidebar.selectbox("Pick a CSV", csv_files)
    df = load_csv(chosen)

# ── Auto-detect numeric columns for charts ────────────────────────────────────
numeric_cols = df.select_dtypes("number").columns.tolist()
text_cols = df.select_dtypes("object").columns.tolist()

# ── KPIs ───────────────────────────────────────────────────────────────────────
if "total_revenue" in df.columns and "total_units" in df.columns:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Revenue", f"${df['total_revenue'].sum():,.2f}")
    k2.metric("Total Units", f"{df['total_units'].sum():,}")
    k3.metric("Rows", len(df))
    k4.metric("Columns", len(df.columns))
else:
    cols = st.columns(min(4, len(numeric_cols) or 1))
    for i, col in enumerate(numeric_cols[:4]):
        cols[i].metric(col, f"{df[col].sum():,.2f}")

st.markdown("---")

# ── Charts ─────────────────────────────────────────────────────────────────────
if "region" in df.columns and "total_revenue" in df.columns:
    region_summary = df.groupby("region")["total_revenue"].sum().reset_index().sort_values("total_revenue", ascending=False)
    product_summary = df.groupby("product")["total_revenue"].sum().reset_index() if "product" in df.columns else None

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Region")
        fig1 = px.bar(region_summary, x="region", y="total_revenue", color="region",
                      text_auto=".2s", labels={"total_revenue": "Revenue ($)"})
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if product_summary is not None:
            st.subheader("Revenue by Product")
            fig2 = px.pie(product_summary, names="product", values="total_revenue", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)

    if "product" in df.columns and "total_units" in df.columns:
        st.subheader("Units Sold by Region & Product")
        fig3 = px.bar(df, x="region", y="total_units", color="product", barmode="group",
                      labels={"total_units": "Units Sold"})
        st.plotly_chart(fig3, use_container_width=True)

elif len(numeric_cols) >= 1 and len(text_cols) >= 1:
    st.subheader("Data Overview")
    fig = px.bar(df, x=text_cols[0], y=numeric_cols[0], color=text_cols[0])
    st.plotly_chart(fig, use_container_width=True)

# ── Raw data + download ────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)
st.download_button("Download as CSV", df.to_csv(index=False).encode(), "result.csv", "text/csv")
