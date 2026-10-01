import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #212529;
        margin: 5px 0;
    }
    .metric-delta-positive {
        color: #10b981;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .metric-delta-negative {
        color: #ef4444;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Header Container */
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .dashboard-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .dashboard-header p {
        margin: 5px 0 0 0;
        color: #94a3b8;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Generates a realistic multi-year dataset with region, product, and operational metrics."""
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 9, 30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America']
    categories = ['Enterprise Software', 'Hardware & Devices', 'Cloud Services', 'Professional Services']
    channels = ['Direct Sales', 'Online Store', 'Partner Network', 'Resellers']
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    
    records = []
    
    for date in dates:
        # Generate 3-8 transactions per day
        n_daily = np.random.randint(3, 9)
        for _ in range(n_daily):
            region = np.random.choice(regions, p=[0.4, 0.3, 0.2, 0.1])
            category = np.random.choice(categories, p=[0.35, 0.25, 0.25, 0.15])
            channel = np.random.choice(channels)
            segment = np.random.choice(segments, p=[0.3, 0.4, 0.3])
            
            # Base revenue influenced by category and segment
            base_val = 1200 if category == 'Enterprise Software' else (800 if category == 'Cloud Services' else 500)
            seg_mult = 2.5 if segment == 'Enterprise' else (1.4 if segment == 'Mid-Market' else 0.8)
            
            units = np.random.randint(1, 15)
            unit_price = base_val * seg_mult * np.random.uniform(0.9, 1.2)
            revenue = round(units * unit_price, 2)
            
            # Target generation
            target = round(revenue * np.random.uniform(0.85, 1.15), 2)
            
            # Financial & Operational Metrics
            cogs = round(revenue * np.random.uniform(0.35, 0.65), 2)
            profit = round(revenue - cogs, 2)
            
            cac = round(np.random.uniform(150, 600), 2)
            ltv = round(cac * np.random.uniform(3.5, 7.0), 2)
            
            lead_time_days = np.random.randint(1, 14)
            fulfillment_rate = round(np.random.uniform(88.0, 99.8), 1)
            csat_score = round(np.random.uniform(3.8, 5.0), 1)
            
            records.append({
                'Date': date,
                'YearMonth': date.strftime('%Y-%m'),
                'Year': date.year,
                'Quarter': f"Q{(date.month - 1) // 3 + 1} {date.year}",
                'Region': region,
                'Category': category,
                'Sales Channel': channel,
                'Customer Segment': segment,
                'Units Sold': units,
                'Revenue': revenue,
                'Target Revenue': target,
                'COGS': cogs,
                'Profit': profit,
                'Profit Margin %': round((profit / revenue) * 100, 2),
                'CAC ($)': cac,
                'LTV ($)': ltv,
                'Lead Time (Days)': lead_time_days,
                'Fulfillment Rate %': fulfillment_rate,
                'CSAT Score': csat_score
            })
            
    df = pd.DataFrame(records)
    return df

# Load cached data
df_raw = load_sample_data()

st.sidebar.image("https://img.icons8.com/color/96/dashboard--v1.png", width=60)
st.sidebar.title("Navigation & Filters")

# Dashboard Page Selector (Page 1 vs Page 2)
app_page = st.sidebar.radio(
    "Select Dashboard View:",
    ["Page 1: Executive Sales & Revenue", "Page 2: Operations & Customer Analytics"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filter Controls")

# Reactive Dropdown Filter 1: Date Quick Filter / Range
date_preset = st.sidebar.selectbox(
    "Date Presets:",
    ["All Time", "Year 2026", "Year 2025", "Last 90 Days", "Custom Range"]
)

min_date = df_raw['Date'].min().date()
max_date = df_raw['Date'].max().date()

if date_preset == "Year 2026":
    start_d, end_d = datetime(2026, 1, 1).date(), max_date
elif date_preset == "Year 2025":
    start_d, end_d = datetime(2025, 1, 1).date(), datetime(2025, 12, 31).date()
elif date_preset == "Last 90 Days":
    start_d, end_d = max_date - timedelta(days=90), max_date
elif date_preset == "Custom Range":
    start_d, end_d = st.sidebar.date_input("Custom Date Range:", [min_date, max_date])
else:
    start_d, end_d = min_date, max_date

# Reactive Dropdown Filter 2: Region Filter
region_list = ["All Regions"] + list(df_raw['Region'].unique())
selected_region = st.sidebar.selectbox("Region:", region_list)

# Reactive Dropdown Filter 3: Product Category Filter
category_list = ["All Categories"] + list(df_raw['Category'].unique())
selected_category = st.sidebar.selectbox("Product Category:", category_list)

# Reactive Dropdown Filter 4: Customer Segment Filter
segment_list = ["All Segments"] + list(df_raw['Customer Segment'].unique())
selected_segment = st.sidebar.selectbox("Customer Segment:", segment_list)

df_filtered = df_raw.copy()

# Date filter
df_filtered = df_filtered[(df_filtered['Date'].dt.date >= start_d) & (df_filtered['Date'].dt.date <= end_d)]

# Region filter
if selected_region != "All Regions":
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]

# Category filter
if selected_category != "All Categories":
    df_filtered = df_filtered[df_filtered['Category'] == selected_category]

# Segment filter
if selected_segment != "All Segments":
    df_filtered = df_filtered[df_filtered['Customer Segment'] == selected_segment]

# Reset button indicator
st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(df_filtered):,}** records after filtering.")
if st.sidebar.button("Reset All Filters"):
    st.rerun()


# Helper function to format metric cards
def render_metric_card(title, value, delta=None, is_positive_good=True):
    delta_html = ""
    if delta is not None:
        color_cls = "metric-delta-positive" if (delta >= 0 if is_positive_good else delta <= 0) else "metric-delta-negative"
        sign = "+" if delta > 0 else ""
        delta_html = f'<div class="{color_cls}">{sign}{delta:.1f}% vs Target/Baseline</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


if app_page == "Page 1: Executive Sales & Revenue":
    
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>Executive Revenue & Sales Performance Dashboard</h1>
        <p>Interactive overview of key financial highlights, regional breakdown, target achievements, and channel growth.</p>
    </div>
    """, unsafe_allow_html=True)

    if df_filtered.empty:
        st.warning("⚠️ No data matches your selected filter criteria. Please adjust the dropdowns in the sidebar.")
    else:
        # Calculate Key Executive Metrics
        total_rev = df_filtered['Revenue'].sum()
        total_target = df_filtered['Target Revenue'].sum()
        target_achievement = ((total_rev / total_target) - 1) * 100 if total_target > 0 else 0
        
        total_profit = df_filtered['Profit'].sum()
        overall_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
        total_units = df_filtered['Units Sold'].sum()
        avg_deal_size = df_filtered['Revenue'].mean()

        # Top Metric Cards Row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            render_metric_card("Total Revenue", f"${total_rev:,.0f}", target_achievement, True)
        with kpi_col2:
            render_metric_card("Gross Profit", f"${total_profit:,.0f}", delta=overall_margin - 45.0, is_positive_good=True)
        with kpi_col3:
            render_metric_card("Profit Margin", f"{overall_margin:.1f}%", delta=None)
        with kpi_col4:
            render_metric_card("Units Sold", f"{total_units:,}", delta=None)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 1 Charts: Revenue Trend vs Target & Regional Market Share
        c1, c2 = st.columns([6, 4])

        with c1:
            st.subheader("Monthly Revenue vs Target Trend")
            # Aggregate monthly
            monthly_df = df_filtered.groupby('YearMonth').agg({
                'Revenue': 'sum',
                'Target Revenue': 'sum',
                'Profit': 'sum'
            }).reset_index()

            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=monthly_df['YearMonth'],
                y=monthly_df['Revenue'],
                name='Actual Revenue',
                marker_color='#2563eb'
            ))
            fig_trend.add_trace(go.Scatter(
                x=monthly_df['YearMonth'],
                y=monthly_df['Target Revenue'],
                name='Target Revenue',
                mode='lines+markers',
                line=dict(color='#f59e0b', width=3, dash='dash')
            ))
            fig_trend.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=350,
                template="plotly_white",
                xaxis_title="Month",
                yaxis_title="USD ($)"
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with c2:
            st.subheader("Regional Sales Breakdown")
            reg_df = df_filtered.groupby('Region')['Revenue'].sum().reset_index()
            fig_pie = px.pie(
                reg_df,
                values='Revenue',
                names='Region',
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_pie.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=350,
                legend=dict(orientation="h", yanchor="top", y=-0.1)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Row 2 Charts: Category Performance & Sales Channel Distribution
        c3, c4 = st.columns(2)

        with c3:
            st.subheader("Category Performance by Margin")
            cat_df = df_filtered.groupby('Category').agg({
                'Revenue': 'sum',
                'Profit': 'sum'
            }).reset_index()
            cat_df['Margin %'] = (cat_df['Profit'] / cat_df['Revenue']) * 100

            fig_cat = px.bar(
                cat_df,
                x='Category',
                y='Revenue',
                color='Margin %',
                color_continuous_scale='Viridis',
                text_auto='.2s',
                title=None
            )
            fig_cat.update_layout(
                height=340,
                template="plotly_white",
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        with c4:
            st.subheader("Sales Channel Distribution")
            chan_df = df_filtered.groupby(['Sales Channel', 'Customer Segment'])['Revenue'].sum().reset_index()
            fig_chan = px.bar(
                chan_df,
                x='Sales Channel',
                y='Revenue',
                color='Customer Segment',
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_chan.update_layout(
                height=340,
                template="plotly_white",
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_chan, use_container_width=True)

elif app_page == "Page 2: Operations & Customer Analytics":
    
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>Operations & Customer Experience Analytics</h1>
        <p>In-depth metrics covering Customer Lifetime Value (LTV), Acquisition Costs (CAC), Lead Times, and CSAT benchmarks.</p>
    </div>
    """, unsafe_allow_html=True)

    if df_filtered.empty:
        st.warning("⚠️ No data matches your selected filter criteria. Please adjust the dropdowns in the sidebar.")
    else:
        # Calculate Key Operational Metrics
        avg_cac = df_filtered['CAC ($)'].mean()
        avg_ltv = df_filtered['LTV ($)'].mean()
        ltv_cac_ratio = (avg_ltv / avg_cac) if avg_cac > 0 else 0
        
        avg_lead_time = df_filtered['Lead Time (Days)'].mean()
        avg_fulfillment = df_filtered['Fulfillment Rate %'].mean()
        avg_csat = df_filtered['CSAT Score'].mean()

        # Operational KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        
        with k1:
            render_metric_card("LTV : CAC Ratio", f"{ltv_cac_ratio:.2f}x", delta=ltv_cac_ratio - 3.0, is_positive_good=True)
        with k2:
            render_metric_card("Avg Customer LTV", f"${avg_ltv:,.0f}", delta=None)
        with k3:
            render_metric_card("Avg Fulfillment Rate", f"{avg_fulfillment:.1f}%", delta=avg_fulfillment - 95.0, is_positive_good=True)
        with k4:
            render_metric_card("Customer Satisfaction (CSAT)", f"{avg_csat:.2f} / 5.0", delta=None)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 1: CAC vs LTV Scatter Analysis & Lead Time Distribution
        col_a, col_b = st.columns([6, 4])

        with col_a:
            st.subheader("LTV vs. CAC Unit Economics by Segment")
            fig_scatter = px.scatter(
                df_filtered.sample(min(500, len(df_filtered))),
                x='CAC ($)',
                y='LTV ($)',
                color='Customer Segment',
                size='Revenue',
                hover_data=['Region', 'Category'],
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_scatter.update_layout(
                height=360,
                template="plotly_white",
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_b:
            st.subheader("Order Lead Time Distribution")
            fig_box = px.box(
                df_filtered,
                x='Region',
                y='Lead Time (Days)',
                color='Region',
                points="outliers"
            )
            fig_box.update_layout(
                height=360,
                template="plotly_white",
                showlegend=False,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # Row 2: Customer Satisfaction Heatmap & Operational Sensitivity Simulator
        col_c, col_d = st.columns(2)

        with col_c:
            st.subheader("CSAT Score Matrix (Region vs Category)")
            csat_pivot = df_filtered.pivot_table(
                index='Region',
                columns='Category',
                values='CSAT Score',
                aggfunc='mean'
            ).round(2)

            fig_heat = px.imshow(
                csat_pivot,
                text_auto=True,
                color_continuous_scale='Blues',
                aspect="auto"
            )
            fig_heat.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        with col_d:
            st.subheader("Fulfillment Optimization Scenario Tool")
            st.write("Simulate operational efficiency improvements on net profitability:")
            
            fulfillment_boost = st.slider("Target Fulfillment Improvement (%)", 0, 10, 3)
            lead_time_reduction = st.slider("Lead Time Reduction (Days)", 0, 5, 2)
            
            # Scenario math
            estimated_cost_saving = (len(df_filtered) * fulfillment_boost * 12.5) + (lead_time_reduction * 1500)
            projected_profit = df_filtered['Profit'].sum() + estimated_cost_saving
            
            st.info(f"""
            💡 **Scenario Impact Projection:**
            * Calculated Cost Efficiency Gain: **+${estimated_cost_saving:,.2f}**
            * Projected Adjusted Net Profit: **${projected_profit:,.2f}**
            * Estimated CSAT Uplift: **+{(fulfillment_boost * 0.05 + lead_time_reduction * 0.08):.2f} pts**
            """)

st.markdown("---")
with st.expander("📥 View & Export Filtered Raw Data", expanded=False):
    st.write(f"Displaying **{len(df_filtered)}** transactions based on active dropdown selection:")
    
    st.dataframe(
        df_filtered[['Date', 'Region', 'Category', 'Sales Channel', 'Customer Segment', 'Revenue', 'Profit', 'CSAT Score']],
        use_container_width=True,
        height=250
    )
    
    # Export CSV Button
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
