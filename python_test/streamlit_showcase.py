import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Streamlit Showcase",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            text-align: center;
            margin: 5px 0;
        }
        .metric-value { font-size: 2rem; font-weight: bold; }
        .metric-label { font-size: 0.9rem; opacity: 0.85; }
        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: #4B4B8F;
            border-left: 4px solid #667eea;
            padding-left: 10px;
            margin: 20px 0 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.svg", width=60)
    st.title("Controls")
    st.markdown("---")
    num_points = st.slider("Data points", 50, 500, 150)
    chart_theme = st.selectbox("Chart theme", ["plotly", "plotly_dark", "ggplot2", "seaborn"])
    show_raw = st.checkbox("Show raw data", value=False)
    st.markdown("---")
    st.info("Built with Streamlit + Plotly")

st.title("🚀 Streamlit Showcase")
st.markdown("#### Everything you can do in one place")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📈 Charts", "🗂️ Data", "🎛️ Widgets", "📝 Text & Media"])

# ── TAB 1: Dashboard ──────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">KPI Metrics</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", "$1.2M", "+12%")
    c2.metric("Users", "45,320", "+8.3%")
    c3.metric("Uptime", "99.9%", "+0.1%")
    c4.metric("Latency", "42 ms", "-5 ms")

    st.markdown('<p class="section-header">Live Trend</p>', unsafe_allow_html=True)
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=num_points)
    df_trend = pd.DataFrame({
        "Date": dates,
        "Revenue": np.cumsum(np.random.randn(num_points) * 500 + 200),
        "Users": np.cumsum(np.random.randn(num_points) * 100 + 50),
    })
    fig = px.line(df_trend, x="Date", y=["Revenue", "Users"],
                  template=chart_theme, title="Revenue & Users Over Time")
    fig.update_layout(height=350, legend_title="Metric")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<p class="section-header">Category Share</p>', unsafe_allow_html=True)
        pie_df = pd.DataFrame({"Category": ["Rides", "Eats", "Freight", "Other"],
                               "Value": [45, 30, 15, 10]})
        fig_pie = px.pie(pie_df, names="Category", values="Value",
                         template=chart_theme, hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    with right:
        st.markdown('<p class="section-header">Weekly Activity</p>', unsafe_allow_html=True)
        bar_df = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                               "Trips": [820, 932, 901, 934, 1290, 1330, 1320]})
        fig_bar = px.bar(bar_df, x="Day", y="Trips", template=chart_theme,
                         color="Trips", color_continuous_scale="Blues")
        st.plotly_chart(fig_bar, use_container_width=True)

# ── TAB 2: Charts ─────────────────────────────────────────────────────────────
with tab2:
    np.random.seed(0)
    df = pd.DataFrame(np.random.randn(num_points, 3), columns=["A", "B", "C"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">Scatter Plot</p>', unsafe_allow_html=True)
        fig_sc = px.scatter(df, x="A", y="B", color="C",
                            color_continuous_scale="Viridis", template=chart_theme)
        st.plotly_chart(fig_sc, use_container_width=True)

        st.markdown('<p class="section-header">Area Chart</p>', unsafe_allow_html=True)
        fig_area = px.area(df.cumsum(), template=chart_theme)
        st.plotly_chart(fig_area, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">Histogram</p>', unsafe_allow_html=True)
        fig_hist = px.histogram(df, x="A", nbins=30, template=chart_theme,
                                color_discrete_sequence=["#667eea"])
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown('<p class="section-header">Box Plot</p>', unsafe_allow_html=True)
        fig_box = px.box(df, template=chart_theme,
                         color_discrete_sequence=["#764ba2", "#667eea", "#f093fb"])
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<p class="section-header">Heatmap (Correlation)</p>', unsafe_allow_html=True)
    corr = df.corr()
    fig_heat = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                         template=chart_theme)
    st.plotly_chart(fig_heat, use_container_width=True)

# ── TAB 3: Data ───────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-header">Interactive DataFrame</p>', unsafe_allow_html=True)
    np.random.seed(5)
    big_df = pd.DataFrame({
        "Name": [f"User_{i}" for i in range(1, num_points + 1)],
        "Score": np.random.randint(50, 100, num_points),
        "Revenue": np.round(np.random.uniform(100, 5000, num_points), 2),
        "Region": np.random.choice(["North", "South", "East", "West"], num_points),
        "Active": np.random.choice([True, False], num_points),
    })

    region_filter = st.multiselect("Filter by Region", big_df["Region"].unique(),
                                   default=big_df["Region"].unique())
    filtered = big_df[big_df["Region"].isin(region_filter)]
    st.dataframe(filtered, use_container_width=True, height=300)

    dl1, dl2 = st.columns(2)
    with dl1:
        csv = filtered.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, "data.csv", "text/csv")
    with dl2:
        st.write(f"Showing **{len(filtered)}** of **{len(big_df)}** rows")

    if show_raw:
        st.markdown('<p class="section-header">Raw Stats</p>', unsafe_allow_html=True)
        st.write(filtered.describe())

# ── TAB 4: Widgets ────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-header">Input Widgets</p>', unsafe_allow_html=True)
    w1, w2 = st.columns(2)
    with w1:
        text_in = st.text_input("Your name", placeholder="Type here...")
        number = st.number_input("Pick a number", 0, 100, 42)
        color = st.color_picker("Pick a color", "#667eea")
        date = st.date_input("Pick a date")
    with w2:
        option = st.radio("Favorite chart", ["Line", "Bar", "Scatter", "Pie"])
        multi = st.multiselect("Select topics", ["ML", "Data", "Python", "SQL", "Cloud"])
        rating = st.slider("Rate this app", 1, 10, 8)

    if text_in:
        st.success(f"Hello, **{text_in}**! You rated this app **{rating}/10** and love **{option}** charts.")

    st.markdown('<p class="section-header">Progress & Status</p>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    p1.progress(0.72, text="Model accuracy 72%")
    p2.progress(0.95, text="Pipeline health 95%")
    p3.progress(0.48, text="Storage used 48%")

    with st.expander("🔍 See more widget options"):
        st.write("- `st.camera_input` — take a photo")
        st.write("- `st.file_uploader` — upload files")
        st.write("- `st.map` — render a map")
        st.write("- `st.audio` / `st.video` — media players")

# ── TAB 5: Text & Media ───────────────────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-header">Text Formatting</p>', unsafe_allow_html=True)
    st.markdown("""
    | Style | Syntax | Output |
    |---|---|---|
    | Bold | `**text**` | **text** |
    | Italic | `*text*` | *text* |
    | Code | `` `code` `` | `code` |
    | Link | `[label](url)` | [Streamlit](https://streamlit.io) |
    """)

    st.markdown('<p class="section-header">Callout Boxes</p>', unsafe_allow_html=True)
    st.success("This is a success message")
    st.info("This is an info message")
    st.warning("This is a warning message")
    st.error("This is an error message")

    st.markdown('<p class="section-header">Code Block</p>', unsafe_allow_html=True)
    st.code("""
import streamlit as st
import pandas as pd

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
st.line_chart(df.set_index("x"))
    """, language="python")

    st.markdown('<p class="section-header">Map</p>', unsafe_allow_html=True)
    map_df = pd.DataFrame(
        np.random.randn(100, 2) * [0.05, 0.05] + [37.76, -122.4],
        columns=["lat", "lon"]
    )
    st.map(map_df)
