import datetime
import os
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --------------------------------------------------
# Page Configuration & Custom CSS Styling
# --------------------------------------------------

st.set_page_config(
    page_title="Lahore Cantonment AQI Intelligence",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for SaaS-grade UI Design
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #070a0f;
        color: #f1f5f9;
    }

    /* Header styling */
    .dashboard-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 16px;
        margin-bottom: 24px;
    }
    
    .header-title {
        font-weight: 800;
        font-size: 2.2rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Pulsing Live Dot Animation */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .live-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #10b981;
        animation: pulse-glow 2s infinite;
        display: inline-block;
    }

    .status-badge {
        background: rgba(15, 23, 42, 0.75);
        color: #94a3b8;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* Hero Glass Box */
    .hero-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 24px;
    }

    /* Metric Glass Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 20px 22px;
        backdrop-filter: blur(12px);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.1);
    }

    /* Custom Metric Tiles */
    .pollutant-tile {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }
    .pollutant-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .pollutant-val {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
    }
    .pollutant-unit {
        font-size: 0.7rem;
        color: #475569;
    }

    /* Custom Weather Card Grid */
    .weather-card-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .weather-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 12px 16px;
        backdrop-filter: blur(12px);
        transition: border-color 0.2s ease;
    }

    .weather-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
    }

    .weather-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .weather-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }

    .weather-unit {
        font-size: 0.8rem;
        font-weight: 500;
        color: #94a3b8;
        margin-left: 2px;
    }

    /* Status Top Highlights */
    .aqi-card-good::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #10b981; box-shadow: 0 2px 10px #10b981; }
    .aqi-card-moderate::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #f59e0b; box-shadow: 0 2px 10px #f59e0b; }
    .aqi-card-sensitive::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #f97316; box-shadow: 0 2px 10px #f97316; }
    .aqi-card-unhealthy::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #ef4444; box-shadow: 0 2px 10px #ef4444; }
    .aqi-card-very-unhealthy::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #a855f7; box-shadow: 0 2px 10px #a855f7; }
    .aqi-card-hazardous::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #71717a; box-shadow: 0 2px 10px #71717a; }

    .card-title {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 8px;
    }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 10px;
    }
    
    .card-status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Modern Alert Banner */
    .custom-alert {
        padding: 14px 18px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 16px 0;
        backdrop-filter: blur(8px);
    }
    .alert-hazardous { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); color: #fca5a5; }
    .alert-warning { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); color: #fde047; }
    .alert-success { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); color: #6ee7b7; }

    /* Model Performance Day Glass Cards */
    .day-perf-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .day-perf-header {
        font-size: 0.9rem;
        font-weight: 700;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 8px;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
    }
    .metric-row-label {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    .metric-row-val {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        padding: 0 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.1);
        color: #38bdf8 !important;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------


def api_get(endpoint):
    response = requests.get(f"{API_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_prediction():
    return api_get("/predict")


@st.cache_data(ttl=300)
def get_metrics():
    try:
        return api_get("/metrics")
    except Exception:
        return None


@st.cache_data(ttl=300)
def get_history():
    history = api_get("/history")
    return pd.DataFrame(history)


@st.cache_data(ttl=300)
def get_shap():
    return pd.DataFrame(api_get("/shap"))


def get_aqi_details(aqi):
    if aqi <= 50:
        return "Good", "#10b981", "rgba(16, 185, 129, 0.15)", "aqi-card-good"
    elif aqi <= 100:
        return "Moderate", "#f59e0b", "rgba(245, 158, 11, 0.15)", "aqi-card-moderate"
    elif aqi <= 150:
        return (
            "Unhealthy (Sensitive)",
            "#f97316",
            "rgba(249, 115, 22, 0.15)",
            "aqi-card-sensitive",
        )
    elif aqi <= 200:
        return "Unhealthy", "#ef4444", "rgba(239, 68, 68, 0.15)", "aqi-card-unhealthy"
    elif aqi <= 300:
        return (
            "Very Unhealthy",
            "#a855f7",
            "rgba(168, 85, 247, 0.15)",
            "aqi-card-very-unhealthy",
        )
    return "Hazardous", "#71717a", "rgba(113, 113, 122, 0.15)", "aqi-card-hazardous"


def render_card(title, value, status, card_class, color, bg_color):
    html = f"""
    <div class="metric-card {card_class}">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        <div class="card-status-pill" style="color: {color}; background-color: {bg_color}; border: 1px solid {color}40;">
            {status}
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

try:
    data = get_prediction()
    prediction = data["prediction"]
    current = data["current"]

    last_updated = data.get("last_updated")
    if last_updated:
        last_updated = pd.to_datetime(last_updated, utc=True)
        last_updated = (
            last_updated
            .tz_convert("Asia/Karachi")
            .strftime("%Y-%m-%d %H:%M:%S PKT")
        )
except Exception as e:
    st.error(f"Unable to establish connection to processing backend.\n\n`{e}`")
    st.stop()


# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.markdown(
    """
    <div class="dashboard-header">
        <h1 class="header-title">Lahore Cantonment Air Quality Intelligence</h1>
        <p style="margin: 6px 0 0 0; color: #64748b; font-size: 0.95rem;">
            Real-time telemetry and 72-hour machine learning atmospheric forecasting.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

time_col1, time_col2 = st.columns([1, 1])
with time_col1:
    st.markdown(
        f"""
        <div class='status-badge'>
            <span class='live-dot'></span>
            <span style='color: #f8fafc;'>LIVE SYSTEM</span>
            <span style='color: #334155;'>|</span>
            <span>{datetime.datetime.now():%b %d, %H:%M:%S}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

if last_updated:
    with time_col2:
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <span class='status-badge'>Sensor Reading: {last_updated}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# --------------------------------------------------
# HERO SECTION: Current Live Gauge + Pollutants Grid
# --------------------------------------------------

curr_aqi = round(current["aqi"], 1)
cat, col_hex, bg_hex, _ = get_aqi_details(curr_aqi)

st.markdown('<div class="hero-card">', unsafe_allow_html=True)
hero_col1, hero_col2 = st.columns([0.45, 0.55])

with hero_col1:
    # Gauge Visual for Main AQI
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=curr_aqi,
            number={"suffix": " AQI", "font": {"size": 36, "color": "#f8fafc", "family": "Inter"}},
            title={"text": f"CURRENT AIR STATUS: <b style='color:{col_hex}'>{cat.upper()}</b>", "font": {"size": 12, "color": "#94a3b8"}},
            gauge={
                "axis": {"range": [0, 500], "tickwidth": 1, "tickcolor": "#334155"},
                "bar": {"color": col_hex},
                "bgcolor": "rgba(15, 23, 42, 0.5)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(16, 185, 129, 0.15)"},
                    {"range": [50, 100], "color": "rgba(245, 158, 11, 0.15)"},
                    {"range": [100, 150], "color": "rgba(249, 115, 22, 0.15)"},
                    {"range": [150, 200], "color": "rgba(239, 68, 68, 0.15)"},
                    {"range": [200, 500], "color": "rgba(168, 85, 247, 0.15)"},
                ],
            },
        )
    )
    fig_gauge.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f8fafc", "family": "Inter"},
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

with hero_col2:
    st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;'>Atmospheric Pollutants Breakdown</p>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">PM2.5</div><div class="pollutant-val">{current["pm2_5"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">NO₂</div><div class="pollutant-val">{current["nitrogen_dioxide"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">PM10</div><div class="pollutant-val">{current["pm10"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">SO₂</div><div class="pollutant-val">{current["sulphur_dioxide"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">CO</div><div class="pollutant-val">{current["carbon_monoxide"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="pollutant-tile"><div class="pollutant-label">O₃</div><div class="pollutant-val">{current["ozone"]:.1f}</div><div class="pollutant-unit">µg/m³</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 3-Day Forecast Cards
# --------------------------------------------------

st.markdown("<h3 style='font-size: 1.05rem; font-weight: 600; color: #cbd5e1; margin-bottom: 14px;'>72-Hour Predictive Outlook</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
forecast_items = [
    ("Tomorrow", "Day_1"),
    ("Day 2", "Day_2"),
    ("Day 3", "Day_3"),
]

for col, (label, key) in zip([col1, col2, col3], forecast_items):
    aqi_val = round(prediction[key])
    category, color, bg_color, card_cls = get_aqi_details(aqi_val)
    with col:
        render_card(
            label, f"{aqi_val} <span style='font-size:0.9rem; font-weight:500; color:#64748b;'>AQI</span>", category, card_cls, color, bg_color
        )

# Health Advisory Banner
tomorrow_aqi = prediction["Day_1"]
if tomorrow_aqi > 300:
    st.markdown("<div class='custom-alert alert-hazardous'><strong>Hazardous Atmosphere Forecasted:</strong> High airborne particulate density tomorrow. Avoid all outdoor activities and run indoor filtration.</div>", unsafe_allow_html=True)
elif tomorrow_aqi > 150:
    st.markdown("<div class='custom-alert alert-warning'><strong>Elevated Pollution Advisory:</strong> Sensitive groups and outdoor workers should limit prolonged physical exertion tomorrow.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='custom-alert alert-success'><strong>Favorable Air Quality:</strong> Atmospheric conditions are within safe ranges for standard outdoor activity.</div>", unsafe_allow_html=True)


# --------------------------------------------------
# Forecast Trajectory & Ambient Climate Grid
# --------------------------------------------------

st.write("")

chart_col, weather_col = st.columns([1.2, 0.8])

with chart_col:
    st.markdown("<h3 style='font-size: 1.05rem; font-weight: 600; color: #cbd5e1; margin-bottom: 12px;'>AQI Trend Projection</h3>", unsafe_allow_html=True)

    forecast_df = pd.DataFrame(
        {
            "Day": ["Tomorrow", "Day 2", "Day 3"],
            "AQI": [prediction["Day_1"], prediction["Day_2"], prediction["Day_3"]],
        }
    )

    fig = px.line(
        forecast_df,
        x="Day",
        y="AQI",
        text="AQI",
        markers=True,
    )
    fig.update_traces(
        line=dict(color="#38bdf8", width=3, shape="spline"),
        marker=dict(size=10, color="#38bdf8", line=dict(color="#070a0f", width=2)),
        textposition="top center",
        texttemplate="%{y:.0f}",
        textfont=dict(color="#38bdf8", size=13, family="Inter")
    )
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Predicted AQI", zeroline=False),
        xaxis=dict(showgrid=False, title=""),
        margin=dict(l=10, r=10, t=30, b=10),
        height=260,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with weather_col:
    st.markdown("<h3 style='font-size: 1.05rem; font-weight: 600; color: #cbd5e1; margin-bottom: 12px;'>Ambient Climate</h3>", unsafe_allow_html=True)

    weather_html = f"""
    <div class="weather-card-grid">
        <div class="weather-card">
            <div class="weather-label">🌡︎ Temp</div>
            <div class="weather-value">{current['temperature']:.1f}<span class="weather-unit">°C</span></div>
        </div>
        <div class="weather-card">
            <div class="weather-label">💧︎ Humidity</div>
            <div class="weather-value">{current['humidity']:.1f}<span class="weather-unit">%</span></div>
        </div>
        <div class="weather-card">
            <div class="weather-label">💨︎ Wind</div>
            <div class="weather-value">{current['wind_speed']:.1f}<span class="weather-unit">km/h</span></div>
        </div>
        <div class="weather-card">
            <div class="weather-label">⏲ Pressure</div>
            <div class="weather-value">{current['pressure']:.1f}<span class="weather-unit">hPa</span></div>
        </div>
        <div class="weather-card">
            <div class="weather-label">⛆ Dew Point</div>
            <div class="weather-value">{current['dew_point']:.1f}<span class="weather-unit">°C</span></div>
        </div>
        <div class="weather-card">
            <div class="weather-label">☁ Cloud Cover</div>
            <div class="weather-value">{current['cloud_cover']:.1f}<span class="weather-unit">%</span></div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(weather_html), unsafe_allow_html=True)


# --------------------------------------------------
# Historical, SHAP & Performance Analytics
# --------------------------------------------------

st.write("")

tab1, tab2, tab3 = st.tabs([
    "Historical AQI Trends", 
    "Feature Importance (SHAP Explainability)",
    "Model Performance & Health"
])

with tab1:
    try:
        history_df = get_history()
        if history_df.empty:
            st.info("No historical readings recorded.")
        else:
            history_df["datetime"] = pd.to_datetime(history_df["datetime"])

            fig_hist = px.area(
                history_df,
                x="datetime",
                y="aqi",
            )
            fig_hist.update_traces(
                line_color="#38bdf8",
                fillcolor="rgba(56, 189, 248, 0.12)",
                line=dict(width=2)
            )
            fig_hist.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="AQI Level"),
                xaxis=dict(showgrid=False, title="Timeline"),
                margin=dict(l=10, r=10, t=20, b=10),
                height=340,
            )
            st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

    except Exception as e:
        st.warning(f"Unable to render historical metrics.\n\n`{e}`")

with tab2:
    try:
        shap_df = get_shap()
        if shap_df.empty:
            st.info("SHAP values unavailable.")
        else:
            n = st.slider(
                "Filter top features:",
                min_value=5,
                max_value=len(shap_df),
                value=min(10, len(shap_df)),
            )

            top_shap = shap_df.head(n).iloc[::-1]

            fig_shap = px.bar(
                top_shap,
                x=top_shap.columns[1],
                y="feature",
                orientation="h",
                color=top_shap.columns[1],
                color_continuous_scale=["#0f172a", "#38bdf8"],
            )
            fig_shap.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Impact Score (|SHAP value|)"),
                yaxis=dict(title=""),
                height=350,
                margin=dict(l=10, r=10, t=20, b=10),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_shap, use_container_width=True, config={"displayModeBar": False})

    except Exception as e:
        st.warning(f"Unable to render SHAP explainability chart.\n\n`{e}`")

with tab3:
    try:
        raw_metrics = get_metrics()

        validation = raw_metrics["validation"]
        test = raw_metrics["test"]

        st.markdown(
            """
            <p style='font-size:0.82rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;'>
            Multi-Horizon Model Evaluation
            </p>
            """,
            unsafe_allow_html=True,
        )

        def render_metrics(title, metrics_data):
            html = f"""
            <div class="day-perf-card">
                <div class="day-perf-header">{title}</div>
                <div class="metric-row">
                    <span class="metric-row-label">Mean Absolute Error (MAE)</span>
                    <span class="metric-row-val">{metrics_data['MAE']:.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-row-label">Root Mean Squared Error (RMSE)</span>
                    <span class="metric-row-val">{metrics_data['RMSE']:.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-row-label">R² Score</span>
                    <span class="metric-row-val" style="color:#10b981;">{metrics_data['R2']:.3f}</span>
                </div>
            </div>
            """
            st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

        st.subheader("Validation Performance")
        cols = st.columns(3)
        for col, day in zip(cols, ["Day1", "Day2", "Day3"]):
            with col:
                render_metrics(day, validation[day])

        st.subheader("Test Performance")
        cols = st.columns(3)
        for col, day in zip(cols, ["Day1", "Day2", "Day3"]):
            with col:
                render_metrics(day, test[day])

        st.write("")
        st.subheader("Error & Performance Trajectory Across Horizons")

        # Dataframe for Metrics
        horizon_df = pd.DataFrame({
            "Forecast Horizon": ["Day 1", "Day 2", "Day 3"],
            "MAE": [test["Day1"]["MAE"], test["Day2"]["MAE"], test["Day3"]["MAE"]],
            "RMSE": [test["Day1"]["RMSE"], test["Day2"]["RMSE"], test["Day3"]["RMSE"]],
            "R2": [test["Day1"]["R2"], test["Day2"]["R2"], test["Day3"]["R2"]],
        })

        # Plotly Dual Y-Axis Figure
        fig_metrics = go.Figure()

        # MAE Line (Primary Y-Axis)
        fig_metrics.add_trace(go.Scatter(
            x=horizon_df["Forecast Horizon"],
            y=horizon_df["MAE"],
            name="MAE",
            mode="lines+markers",
            line=dict(color="#38bdf8", width=3),
            marker=dict(size=8),
        ))

        # RMSE Line (Primary Y-Axis)
        fig_metrics.add_trace(go.Scatter(
            x=horizon_df["Forecast Horizon"],
            y=horizon_df["RMSE"],
            name="RMSE",
            mode="lines+markers",
            line=dict(color="#f59e0b", width=3, dash="dash"),
            marker=dict(size=8),
        ))

        # R2 Line (Secondary Y-Axis)
        fig_metrics.add_trace(go.Scatter(
            x=horizon_df["Forecast Horizon"],
            y=horizon_df["R2"],
            name="R² Score",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#10b981", width=3),
            marker=dict(size=8),
        ))

        fig_metrics.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Error Score (AQI)",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)"
            ),
            yaxis2=dict(
                title="R² Score",
                overlaying="y",
                side="right",
                range=[0, 1.05],
                showgrid=False
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(
            fig_metrics,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    except Exception as e:
        st.warning(f"Unable to render model performance.\n\n`{e}`")