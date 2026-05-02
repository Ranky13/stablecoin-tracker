import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from src.pipeline.load import get_psycopg2_connection

load_dotenv()


st.set_page_config(
    page_title="Stablecoin Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: #0d1117;
        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        padding: 2rem 3rem;
    }

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border: 1px solid rgba(99, 179, 237, 0.3);
    }

    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.5) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    div[data-testid="metric-container"]
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    h1 {
        background: linear-gradient(90deg, #63b3ed, #76e4f7, #68d391);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
    }

    h2, h3 {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
        margin: 1.5rem 0 !important;
    }

    div[data-testid="stSelectbox"] > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    div[data-testid="stSlider"] {
        padding: 0.5rem 0;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(90deg, #63b3ed, #76e4f7) !important;
        color: #0d1117 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        transition: opacity 0.2s ease !important;
    }

    div[data-testid="stDownloadButton"] button:hover {
        opacity: 0.85 !important;
    }

    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 179, 237, 0.3);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 179, 237, 0.5);
    }

    p, span, label {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    section[data-testid="stSidebar"] {
        background: #161b22 !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }

    div[data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


def glass_chart_layout(fig, title=""):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(
                family="Inter",
                size=15,
                color="rgba(255,255,255,0.85)"
            )
        ),
        paper_bgcolor="rgba(255,255,255,0.02)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(
            family="Inter",
            color="rgba(255,255,255,0.6)"
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="rgba(255,255,255,0.5)")
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="rgba(255,255,255,0.5)")
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.03)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(color="rgba(255,255,255,0.6)")
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        hoverlabel=dict(
            bgcolor="rgba(13,17,23,0.95)",
            bordercolor="rgba(99,179,237,0.4)",
            font=dict(
                family="Inter",
                color="white"
            )
        )
    )
    return fig


@st.cache_data(ttl=300)
def load_data():
    conn = get_psycopg2_connection()

    prices    = pd.read_sql("SELECT * FROM stablecoin_prices",  conn)
    supply    = pd.read_sql("SELECT * FROM supply_metrics",     conn)
    activity  = pd.read_sql("SELECT * FROM activity_metrics",   conn)
    liquidity = pd.read_sql("SELECT * FROM liquidity_metrics",  conn)
    risk      = pd.read_sql("SELECT * FROM risk_metrics",       conn)

    conn.close()

    df = prices.merge(supply,    on='symbol', suffixes=('', '_supply'))
    df = df.merge(activity,      on='symbol', suffixes=('', '_activity'))
    df = df.merge(liquidity,     on='symbol', suffixes=('', '_liquidity'))
    df = df.merge(risk,          on='symbol', suffixes=('', '_risk'))

    return df



col_title, col_time = st.columns([3, 1])
with col_title:
    st.title("📊 Stablecoin Intelligence")
with col_time:
    st.markdown(
        f"""
        <div style='text-align:right; padding-top:1.5rem;
        color:rgba(255,255,255,0.4); font-size:0.85rem;'>
        🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


with st.spinner("⏳ Loading stablecoin data..."):
    df = load_data()

if df is None or len(df) == 0:
    st.error("❌ No data available. Run the pipeline first.")
    st.stop()

# Fill NaN values
df = df.fillna(0)
df = df[df['depeg_score'] <= 5.0]


st.subheader("📈 Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🪙 Total Stablecoins",
        value=f"{len(df):,}"
    )

with col2:
    total_market_cap = df['market_cap'].sum()
    st.metric(
        label="💰 Total Market Cap",
        value=f"${total_market_cap:,.0f}"
    )

with col3:
    avg_depeg = df['depeg_score'].mean()
    if 'price_change_24h' in df.columns:
        avg_price_change = df['price_change_24h'].mean()
        st.metric(
            label="📉 Avg Depeg Score",
            value=f"{avg_depeg:.4f}%",
            delta=f"{avg_price_change:.6f} 24h",
            delta_color="inverse"
        )
    else:
        st.metric(
            label="📉 Avg Depeg Score",
            value=f"{avg_depeg:.4f}%"
        )

with col4:
    avg_stress = df['stress_index'].mean()
    st.metric(
        label="⚠️ Avg Stress Index",
        value=f"{avg_stress:.2f}"
    )


st.divider()

st.subheader("🔍 Filter Stablecoins")

col1, col2 = st.columns(2)

with col1:
    selected_symbol = st.selectbox(
        "Select Stablecoin",
        options=["All"] + sorted(df['symbol'].tolist())
    )

with col2:
    stress_filter = st.slider(
        "Max Stress Index",
        min_value=0,
        max_value=100,
        value=100
    )

# Apply filters
filtered_df = df.copy()
if selected_symbol != "All":
    filtered_df = filtered_df[
        filtered_df['symbol'] == selected_symbol
    ]
filtered_df = filtered_df[
    filtered_df['stress_index'] <= stress_filter
]

st.divider()


st.subheader("📊 Market Share & Depeg Analysis")

col1, col2 = st.columns(2)

with col1:
    top_10 = df.nlargest(10, 'market_cap')
    fig_pie = px.pie(
        top_10,
        values='market_cap',
        names='symbol',
        hole=0.5,
        color_discrete_sequence=[
    'rgba(99, 179, 237, 0.9)',   
    'rgba(118, 228, 247, 0.9)',  # cyan
    'rgba(104, 211, 145, 0.9)',  # green
    'rgba(154, 117, 245, 0.9)',  # purple
    'rgba(252, 129, 129, 0.9)',  # red
    'rgba(246, 173, 85, 0.9)',   # orange
    'rgba(129, 230, 217, 0.9)',  # teal
    'rgba(183, 148, 246, 0.9)',  # light purple
    'rgba(154, 230, 180, 0.9)',  # light green
    'rgba(144, 205, 244, 0.9)',  # light blue
]
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Market Cap: $%{value:,.0f}<br>Share: %{percent}',
        marker=dict(
            line=dict(
                color='rgba(255,255,255,0.1)',
                width=1
            )
        )
    )
    fig_pie = glass_chart_layout(
        fig_pie,
        "Top 10 Stablecoins by Market Share"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Area chart for depeg score
    depeg_df = filtered_df[['symbol', 'depeg_score']].copy()
    depeg_df = depeg_df.dropna()
    depeg_df = depeg_df.sort_values(
        'depeg_score', ascending=False
    ).head(15)

    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=depeg_df['symbol'],
        y=depeg_df['depeg_score'],
        mode='lines+markers',
        fill='tozeroy',
        fillcolor='rgba(99, 179, 237, 0.1)',
        line=dict(
            color='rgba(99, 179, 237, 0.8)',
            width=2
        ),
        marker=dict(
            color='rgba(99, 179, 237, 1)',
            size=8,
            line=dict(
                color='white',
                width=1
            )
        ),
        hovertemplate='<b>%{x}</b><br>Depeg Score: %{y:.4f}%<extra></extra>'
    ))
    fig_area.update_layout(xaxis_tickangle=-45)
    fig_area = glass_chart_layout(
        fig_area,
        "Top 15 Stablecoins by Depeg Score"
    )
    st.plotly_chart(fig_area, use_container_width=True)

st.divider()


st.subheader("⚠️ Risk & Activity Analysis")

col1, col2 = st.columns(2)

with col1:
    top_stress = filtered_df.nlargest(15, 'stress_index')
    fig_stress = px.bar(
        top_stress,
        x='symbol',
        y='stress_index',
        color='stress_index',
        color_continuous_scale='RdYlGn_r',
        labels={
            'symbol':       'Stablecoin',
            'stress_index': 'Stress Index'
        }
    )
    fig_stress.update_layout(xaxis_tickangle=-45)
    fig_stress = glass_chart_layout(
        fig_stress,
        "Top 15 Stablecoins by Stress Index"
    )
    st.plotly_chart(fig_stress, use_container_width=True)

with col2:
    # Funnel chart for velocity
    velocity_df = filtered_df[['symbol', 'velocity']].copy()
    velocity_df = velocity_df.dropna()
    velocity_df = velocity_df.nlargest(15, 'velocity')

    fig_funnel = go.Figure(go.Funnel(
        y=velocity_df['symbol'],
        x=velocity_df['velocity'],
        textinfo="value+percent initial",
        marker=dict(
            color=[
                f'rgba(99, 179, 237, {0.4 + 0.04*i})'
                for i in range(len(velocity_df))
            ],
            line=dict(
                color='rgba(255,255,255,0.1)',
                width=1
            )
        ),
        connector=dict(
            line=dict(
                color='rgba(255,255,255,0.05)',
                width=1
            )
        )
    ))
    fig_funnel = glass_chart_layout(
        fig_funnel,
        "Top 15 Stablecoins by Velocity"
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

st.divider()

st.subheader("💧 Liquidity & Utilization Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_liquidity = px.bar(
        filtered_df.nlargest(15, 'liquidity_ratio'),
        x='symbol',
        y='liquidity_ratio',
        color='liquidity_ratio',
        color_continuous_scale='Teal',
        labels={
            'symbol':          'Stablecoin',
            'liquidity_ratio': 'Liquidity Ratio'
        }
    )
    fig_liquidity.update_layout(xaxis_tickangle=-45)
    fig_liquidity = glass_chart_layout(
        fig_liquidity,
        "Top 15 Stablecoins by Liquidity Ratio"
    )
    st.plotly_chart(fig_liquidity, use_container_width=True)

with col2:
    # Heatmap showing all metrics for top 15 coins
    heatmap_df = filtered_df.nlargest(15, 'market_cap')[
        [
            'symbol',
            'depeg_score',
            'market_share',
            'velocity',
            'liquidity_ratio',
            'utilization',
            'supply_change',
            'stress_index'
        ]
    ].copy()


    cols_to_normalize = [
        'depeg_score',
        'market_share',
        'velocity',
        'liquidity_ratio',
        'utilization',
        'supply_change',
        'stress_index'
    ]

    for col in cols_to_normalize:
        col_min = heatmap_df[col].min()
        col_max = heatmap_df[col].max()
        if col_max - col_min > 0:
            heatmap_df[col] = (
                heatmap_df[col] - col_min
            ) / (col_max - col_min)
        else:
            heatmap_df[col] = 0

    # Set symbol as index
    heatmap_df = heatmap_df.set_index('symbol')

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_df.values,
        x=[
            'Depeg Score',
            'Market Share',
            'Velocity',
            'Liquidity',
            'Utilization',
            'Supply Change',
            'Stress Index'
        ],
        y=heatmap_df.index.tolist(),
        colorscale=[
            [0.0,  'rgba(13, 17, 23, 0.9)'],
            [0.25, 'rgba(99, 179, 237, 0.4)'],
            [0.5,  'rgba(99, 179, 237, 0.7)'],
            [0.75, 'rgba(118, 228, 247, 0.85)'],
            [1.0,  'rgba(104, 211, 145, 1.0)']
        ],
        hoverongaps=False,
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Metric: %{x}<br>'
            'Score: %{z:.2f}<extra></extra>'
        ),
        xgap=3,
        ygap=3
    ))

    fig_heatmap.update_layout(
        xaxis=dict(
            side='bottom',
            tickfont=dict(
                color='rgba(255,255,255,0.6)',
                size=11
            )
        ),
        yaxis=dict(
            tickfont=dict(
                color='rgba(255,255,255,0.6)',
                size=11
            )
        )
    )

    fig_heatmap = glass_chart_layout(
        fig_heatmap,
        "Top 15 Stablecoins — Metrics Heatmap"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()


st.subheader("🔄 Supply Change Analysis")

# Waterfall chart for supply change
supply_df = filtered_df.nlargest(15, 'supply_change')[
    ['symbol', 'supply_change']
].copy()

fig_waterfall = go.Figure(go.Waterfall(
    name="Supply Change",
    orientation="v",
    x=supply_df['symbol'],
    y=supply_df['supply_change'],
    connector=dict(
        line=dict(
            color='rgba(255,255,255,0.1)',
            width=1
        )
    ),
    increasing=dict(
        marker=dict(color='rgba(104, 211, 145, 0.8)')
    ),
    decreasing=dict(
        marker=dict(color='rgba(252, 129, 129, 0.8)')
    ),
    totals=dict(
        marker=dict(color='rgba(99, 179, 237, 0.8)')
    )
))
fig_waterfall.update_layout(xaxis_tickangle=-45)
fig_waterfall = glass_chart_layout(
    fig_waterfall,
    "Top 15 Stablecoins by Supply Change"
)
st.plotly_chart(fig_waterfall, use_container_width=True)

st.divider()

st.subheader("📋 Full Stablecoin Data")

display_cols = [
    'symbol',
    'price',
    'depeg_score',
    'market_share',
    'velocity',
    'liquidity_ratio',
    'utilization',
    'supply_change',
    'stress_index'
]

available_cols = [
    col for col in display_cols
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[available_cols]
    .sort_values('stress_index', ascending=False)
    .reset_index(drop=True),
    use_container_width=True
)

st.divider()


csv = filtered_df[available_cols].to_csv(index=False)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name=f"stablecoins_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

st.divider()
st.markdown(
    """
    <div style='text-align:center;
    color:rgba(255,255,255,0.25);
    font-size:0.8rem; padding:1rem;'>
    📊 Stablecoin Intelligence Dashboard
    • Data sourced from CoinGecko
    • Refreshes every 5 minutes
    </div>
    """,
    unsafe_allow_html=True
)