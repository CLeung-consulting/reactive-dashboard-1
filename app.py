import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="A-Flex Sentiment Dashboard - PowerBI Edition",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Background and Typography */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* PowerBI Inspired KPI Cards */
    .pbi-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #007bff;
        margin-bottom: 10px;
        transition: transform 0.15s ease-in-out;
    }
    .pbi-card:hover {
        transform: translateY(-2px);
    }
    .pbi-card-pos { border-left-color: #28a745; }
    .pbi-card-neu { border-left-color: #002060; }
    .pbi-card-neg { border-left-color: #dc3545; }
    .pbi-card-block { border-left-color: #fd7e14; }
    .pbi-card-report { border-left-color: #6f42c1; }

    .pbi-card-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .pbi-card-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
        line-height: 1.2;
    }
    .pbi-card-subtext {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* TMDL Semantic Layer Badge */
    .tmdl-badge {
        background-color: #e0f2fe;
        color: #0369a1;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #bae6fd;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Detail Page Header Box */
    .doc-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 22px 26px;
        border-radius: 10px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
        border: 1px solid #334155;
    }
    .doc-banner h2 {
        margin: 0 0 10px 0;
        font-size: 1.45rem;
        color: #38bdf8;
        font-weight: 700;
    }
    .doc-banner p {
        margin: 4px 0;
        color: #cbd5e1;
        font-size: 0.92rem;
    }

    /* Evidence Tag Badges */
    .tag-badge {
        display: inline-block;
        padding: 5px 14px;
        margin: 4px 4px 4px 0;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_tmdl_semantic_model():
    """
    Simulates the PowerBI TMDL (Tabular Model Definition Language) Semantic Layer.
    Creates Fact and Dimension tables and returns a unified relational DataFrame.
    """
    np.random.seed(42)
    
    # Dimension Tables
    depots_dim = pd.DataFrame([
        {'Depot_ID': 'D1', 'Depot_Name': 'DLU2 (LU Logistics)', 'Depot_Type': 'Logistics'},
        {'Depot_ID': 'D2', 'Depot_Name': 'ULO5 (West)', 'Depot_Type': 'Fresh'},
        {'Depot_ID': 'D3', 'Depot_Name': 'WD18 8A (Watford)', 'Depot_Type': 'Morrisons'},
        {'Depot_ID': 'D4', 'Depot_Name': 'AL7 1RY (Welwyn)', 'Depot_Type': 'Co-op'},
        {'Depot_ID': 'D5', 'Depot_Name': 'DHA2 (North)', 'Depot_Type': 'Logistics'}
    ])
    
    months_order = ["January", "February", "March", "September", "October", "November", "December"]
    doc_titles = [
        "20260207_LU_Logistics_delivery_block_LU56JH_20260207_1700_issue_report.docx",
        "Gmail - Refrain from lowering my driver rating (delivery block 5-Mar-2024).pdf",
        "Gmail - Refrain from lowering my driver rating (19-Feb-2025).pdf",
        "Gmail - Claim for the extra time of the allocated delivery block on 26-Oct-2024.pdf",
        "Gmail - Claim for the extra time of the allocated delivery block on 1-Mar-2025.pdf",
        "20251112_Fresh_Delivery_Delay_Block_Report_DLU2.docx",
        "20251005_Morrisons_App_Traffic_Closure_Issue.pdf",
        "20240920_Co-op_Package_Sorting_Trunk_Overtime.pdf"
    ]
    
    sentiments = ['Negative', 'Neutral', 'Slightly Negative', 'Slightly Positive']
    tones = ['Factual and objective, detailing issues', 'Critical & Frustrated', 'Informative & Direct']
    
    fact_rows = []
    
    # Generate Fact Table Entries (`f_SentimentReports`)
    for i in range(160):
        depot_row = depots_dim.iloc[np.random.choice(len(depots_dim), p=[0.50, 0.22, 0.14, 0.08, 0.06])]
        month = np.random.choice(months_order, p=[0.08, 0.22, 0.15, 0.15, 0.18, 0.17, 0.05])
        year = np.random.choice([2024, 2025, 2026], p=[0.3, 0.4, 0.3])
        sentiment = np.random.choice(sentiments, p=[0.68, 0.20, 0.07, 0.05])
        intensity = np.random.randint(1, 6)
        doc = doc_titles[i % len(doc_titles)]
        has_attach = np.random.choice([True, False], p=[0.85, 0.15])
        
        # TMDL Measures: Calculate exact score distributions
        if sentiment == 'Negative':
            pos_score = round(np.random.uniform(0.01, 0.08), 2)
            neu_score = round(np.random.uniform(0.15, 0.30), 2)
            neg_score = round(np.random.uniform(0.65, 0.88), 2)
            blocks, issues, reports = np.random.randint(1, 3), np.random.randint(1, 4), 1
        elif sentiment == 'Neutral':
            pos_score = round(np.random.uniform(0.02, 0.10), 2)
            neu_score = round(np.random.uniform(0.70, 0.90), 2)
            neg_score = round(np.random.uniform(0.08, 0.20), 2)
            blocks, issues, reports = 1, 0, 1
        elif sentiment == 'Slightly Negative':
            pos_score = round(np.random.uniform(0.10, 0.25), 2)
            neu_score = round(np.random.uniform(0.35, 0.50), 2)
            neg_score = round(np.random.uniform(0.35, 0.50), 2)
            blocks, issues, reports = 1, 1, 1
        else:
            pos_score = round(np.random.uniform(0.55, 0.80), 2)
            neu_score = round(np.random.uniform(0.15, 0.35), 2)
            neg_score = round(np.random.uniform(0.01, 0.10), 2)
            blocks, issues, reports = 1, 0, 1

        fact_rows.append({
            'Report_ID': f"REP-{2000 + i}",
            'Document_Title': doc,
            'Month': month,
            'Year': year,
            'Depot_ID': depot_row['Depot_ID'],
            'Depot': depot_row['Depot_Name'],
            'Depot_Type': depot_row['Depot_Type'],
            'Sentiment': sentiment,
            'Intensity_Level': intensity,
            'Has_Attachment': has_attach,
            'Pos_Score': pos_score,
            'Neu_Score': neu_score,
            'Neg_Score': neg_score,
            'Block_Count': blocks,
            'Issue_Count': issues,
            'Report_Count': reports,
            'Tone': np.random.choice(tones),
            'Complaints_Summary': "Delivery block scheduled for 5:00 PM - 9:00 PM, but app displayed orders up to 10:00 PM. Trunk package sorting delays & road closure detours.",
            'Visual_Categories': ['App Interfaces', 'Map Views', 'Route Screenshots']
        })

    f_SentimentReports = pd.DataFrame(fact_rows)
    return f_SentimentReports, depots_dim

df_fact, df_depots_dim = load_tmdl_semantic_model()

st.sidebar.image("https://img.icons8.com/color/96/delivery-truck.png", width=60)
st.sidebar.title("A-Flex Controls")
st.sidebar.markdown('<div class="tmdl-badge">📐 TMDL Model: A-Flex_Semantic_v2.0</div>', unsafe_allow_html=True)

# Page Selector
app_page = st.sidebar.radio(
    "Select Dashboard View:",
    ["Page 1: Executive Overview", "Page 2: Paginated Detail Report"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Reactive Dropdown Filters")

# Dropdown Filter 1: Depot Type
depot_type_list = ["All"] + sorted(list(df_fact['Depot_Type'].unique()))
sel_depot_type = st.sidebar.selectbox("Depot Type:", depot_type_list, index=0)

# Dropdown Filter 2: Specific Depot
if sel_depot_type != "All":
    available_depots = sorted(list(df_fact[df_fact['Depot_Type'] == sel_depot_type]['Depot'].unique()))
else:
    available_depots = sorted(list(df_fact['Depot'].unique()))
depot_list = ["All Depots"] + available_depots
sel_depot = st.sidebar.selectbox("Depot Location:", depot_list, index=0)

# Dropdown Filter 3: Sentiment Classification
sentiment_list = ["All"] + sorted(list(df_fact['Sentiment'].unique()))
sel_sentiment = st.sidebar.selectbox("Sentiment Category:", sentiment_list, index=0)

# Filter 4: Intensity Level Slider
min_int, max_int = int(df_fact['Intensity_Level'].min()), int(df_fact['Intensity_Level'].max())
sel_intensity = st.sidebar.slider("Intensity Level Range:", min_value=min_int, max_value=max_int, value=(min_int, max_int))

# Dropdown Filter 5: Date / Year
year_list = ["All Years"] + sorted([str(y) for y in df_fact['Year'].unique()], reverse=True)
sel_year = st.sidebar.selectbox("Date / Year Scope:", year_list, index=0)

# Dropdown Filter 6: Attachment Status
sel_attachment = st.sidebar.selectbox(
    "Attachment Status:",
    ["All Records", "With Attachments Only", "Without Attachments"]
)

df_filtered = df_fact.copy()

if sel_depot_type != "All":
    df_filtered = df_filtered[df_filtered['Depot_Type'] == sel_depot_type]

if sel_depot != "All Depots":
    df_filtered = df_filtered[df_filtered['Depot'] == sel_depot]

if sel_sentiment != "All":
    df_filtered = df_filtered[df_filtered['Sentiment'] == sel_sentiment]

df_filtered = df_filtered[
    (df_filtered['Intensity_Level'] >= sel_intensity[0]) & 
    (df_filtered['Intensity_Level'] <= sel_intensity[1])
]

if sel_year != "All Years":
    df_filtered = df_filtered[df_filtered['Year'] == int(sel_year)]

if sel_attachment == "With Attachments Only":
    df_filtered = df_filtered[df_filtered['Has_Attachment'] == True]
elif sel_attachment == "Without Attachments":
    df_filtered = df_filtered[df_filtered['Has_Attachment'] == False]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(df_filtered)}** of **{len(df_fact)}** reports in active model.")

if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

COLOR_PALETTE = {
    'Negative': '#007bff',
    'Neutral': '#002060',
    'Slightly Negative': '#fd7e14',
    'Slightly Positive': '#6f42c1',
    'Logistics': '#007bff',
    'Fresh': '#002060',
    'Morrisons': '#fd7e14',
    'Co-op': '#6f42c1'
}

if app_page == "Page 1: Executive Overview":
    st.title("🚛 A-Flex Sentiment Dashboard_ver2 (All) - with intensity")
    st.caption("Executive PowerBI view displaying sentiment proportions, depot breakdown, monthly delivery block trends, and word insights.")

    if df_filtered.empty:
        st.warning("⚠️ No records match your selected dropdown filter combination. Please modify the filters in the left sidebar.")
    else:
        # Calculate PowerBI TMDL Measures
        total_reports_count = len(df_filtered)
        pos_measure = (df_filtered['Sentiment'] == 'Slightly Positive').sum() / total_reports_count if total_reports_count > 0 else 0.0
        neu_measure = (df_filtered['Sentiment'] == 'Neutral').sum() / total_reports_count if total_reports_count > 0 else 0.0
        neg_measure = (df_filtered['Sentiment'] == 'Negative').sum() / total_reports_count if total_reports_count > 0 else 0.0
        
        total_blocks_measure = int(df_filtered['Block_Count'].sum())
        total_reports_measure = int(df_filtered['Report_Count'].sum())

        # Top Metric Cards Row (Matching 2-Page PowerBI PDF Layout)
        m1, m2, m3, m4, m5 = st.columns(5)

        with m1:
            st.markdown(f"""
            <div class="pbi-card pbi-card-pos">
                <div class="pbi-card-title">Positive</div>
                <div class="pbi-card-value">{pos_measure:.2f}</div>
                <div class="pbi-card-subtext">Avg Positive Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="pbi-card pbi-card-neu">
                <div class="pbi-card-title">Neutral</div>
                <div class="pbi-card-value">{neu_measure:.2f}</div>
                <div class="pbi-card-subtext">Avg Neutral Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="pbi-card pbi-card-neg">
                <div class="pbi-card-title">Negative</div>
                <div class="pbi-card-value">{neg_measure:.2f}</div>
                <div class="pbi-card-subtext">Avg Negative Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="pbi-card pbi-card-block">
                <div class="pbi-card-title"># Block</div>
                <div class="pbi-card-value">{total_blocks_measure}</div>
                <div class="pbi-card-subtext">Total Delivery Blocks</div>
            </div>
            """, unsafe_allow_html=True)

        with m5:
            st.markdown(f"""
            <div class="pbi-card pbi-card-report">
                <div class="pbi-card-title"># Report</div>
                <div class="pbi-card-value">{total_reports_measure}</div>
                <div class="pbi-card-subtext">Logged Audit Reports</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("##### # Issue by Sentiment")
            sent_agg = df_filtered.groupby('Sentiment')['Issue_Count'].sum().reset_index()
            
            fig_sent = px.pie(
                sent_agg,
                names='Sentiment',
                values='Issue_Count',
                hole=0.55,
                color='Sentiment',
                color_discrete_map=COLOR_PALETTE
            )
            fig_sent.update_traces(textposition='inside', textinfo='percent+label')
            fig_sent.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
            st.plotly_chart(fig_sent, use_container_width=True)

        with c2:
            st.markdown("##### # Report by Depot")
            depot_agg = df_filtered['Depot'].value_counts().reset_index()
            depot_agg.columns = ['Depot', 'Count']
            
            fig_depot = px.pie(
                depot_agg,
                names='Depot',
                values='Count',
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_depot.update_traces(textposition='inside', textinfo='value')
            fig_depot.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
            st.plotly_chart(fig_depot, use_container_width=True)

        with c3:
            st.markdown("##### # Report by Depot Type")
            dtype_agg = df_filtered['Depot_Type'].value_counts().reset_index()
            dtype_agg.columns = ['Depot_Type', 'Count']
            
            fig_dtype = px.pie(
                dtype_agg,
                names='Depot_Type',
                values='Count',
                hole=0.55,
                color='Depot_Type',
                color_discrete_map=COLOR_PALETTE
            )
            fig_dtype.update_traces(textposition='inside', textinfo='percent')
            fig_dtype.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
            st.plotly_chart(fig_dtype, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_trend, col_audit = st.columns([6, 4])

        with col_trend:
            st.markdown("##### # Block, # Issue, # Report by Month")
            
            months_seq = ["January", "February", "March", "September", "October", "November", "December"]
            monthly_data = df_filtered.groupby('Month').agg({
                'Block_Count': 'sum',
                'Issue_Count': 'sum',
                'Report_Count': 'sum'
            }).reindex(months_seq).fillna(0).reset_index()

            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=monthly_data['Month'], y=monthly_data['Block_Count'],
                name='# Block', fill='tozeroy', line=dict(color='#007bff', width=2)
            ))
            fig_area.add_trace(go.Scatter(
                x=monthly_data['Month'], y=monthly_data['Issue_Count'],
                name='# Issue', fill='tozeroy', line=dict(color='#002060', width=2)
            ))
            fig_area.add_trace(go.Scatter(
                x=monthly_data['Month'], y=monthly_data['Report_Count'],
                name='# Report', fill='tozeroy', line=dict(color='#fd7e14', width=2)
            ))
            fig_area.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white"
            )
            st.plotly_chart(fig_area, use_container_width=True)

        with col_audit:
            st.markdown("##### Document Audit Log")
            st.caption("Active documents matching filter scope:")
            st.dataframe(
                df_filtered[['Document_Title', 'Depot', 'Sentiment', 'Intensity_Level']].head(7),
                use_container_width=True,
                height=260,
                hide_index=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col_cat_bar, col_words = st.columns([5, 5])

        with col_cat_bar:
            st.markdown("##### Sentiment Details by Type")
            
            complaints_val = int(len(df_filtered) * 1.15)
            images_val = int(len(df_filtered) * 0.88)
            visual_val = int(len(df_filtered) * 0.52)

            df_category_metrics = pd.DataFrame({
                'Category': ['Key Complaints', 'Notable Images', 'Visual Categories'],
                'Count': [complaints_val, images_val, visual_val]
            })

            fig_cat_bar = px.bar(
                df_category_metrics,
                x='Category',
                y='Count',
                text='Count',
                color_discrete_sequence=['#007bff']
            )
            fig_cat_bar.update_layout(
                height=250,
                template="plotly_white",
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_cat_bar, use_container_width=True)

        with col_words:
            st.markdown("##### Overall Sentiment Word Cloud Insights")
            
            word_freqs = {
                "Delivery": 48, "block": 41, "app": 32, "time": 27, 
                "scheduled": 24, "road": 21, "closure": 19, "traffic": 17,
                "stops": 16, "customer": 14, "parcel": 13, "PM": 12,
                "duration": 11, "mislabeling": 10, "trunk": 8, "issues": 7
            }
            df_word_freq = pd.DataFrame(list(word_freqs.items()), columns=['Keyword', 'Frequency'])
            
            fig_words = px.bar(
                df_word_freq.sort_values(by='Frequency', ascending=True),
                x='Frequency',
                y='Keyword',
                orientation='h',
                color='Frequency',
                color_continuous_scale='Blues'
            )
            fig_words.update_layout(
                height=250,
                template="plotly_white",
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_words, use_container_width=True)

elif app_page == "Page 2: Paginated Detail Report":
    st.title("📄 Detail Sentiment Report (Paginated View)")
    st.caption("Deep-dive inspection of individual delivery block reports, specific driver complaints, and attached visual evidence.")

    if df_filtered.empty:
        st.warning("⚠️️ No records match your selected dropdown filter combination. Please modify the filters in the left sidebar.")
    else:
        # Document Selection Dropdown
        selected_doc = st.selectbox(
            "Select Document Report to Inspect:",
            df_filtered['Document_Title'].unique()
        )

        doc_data = df_filtered[df_filtered['Document_Title'] == selected_doc].iloc[0]

        # Document Header Banner
        st.markdown(f"""
        <div class="doc-banner">
            <h2>📄 {doc_data['Document_Title']}</h2>
            <p><b>Report Date:</b> {doc_data['Month']} {doc_data['Year']} &nbsp;|&nbsp; <b>Depot:</b> {doc_data['Depot']} &nbsp;|&nbsp; <b>Type:</b> {doc_data['Depot_Type']}</p>
            <p><b>Intensity Level:</b> {doc_data['Intensity_Level']}/5 &nbsp;|&nbsp; <b>Tone:</b> {doc_data['Tone']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Sentiment Scores Display
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Positive Score", f"{doc_data['Pos_Score']:.2f}")
        with sc2:
            st.metric("Neutral Score", f"{doc_data['Neu_Score']:.2f}")
        with sc3:
            st.metric("Negative Score", f"{doc_data['Neg_Score']:.2f}")

        st.markdown("---")

        col_left, col_right = st.columns([6, 4])

        with col_left:
            st.subheader("Executive Sentiment Summary")
            st.write(f"""
            This report details critical delivery block issues observed at **{doc_data['Depot']}**. 
            The document tone is categorized as **{doc_data['Tone'].lower()}**, with an overall classification of **{doc_data['Sentiment'].lower()}** (Intensity: {doc_data['Intensity_Level']}/5).
            """)

            st.subheader("Key Itemized Complaints")
            st.markdown("""
            * **Block Schedule Overrun:** Delivery block was allocated for **5:00 PM – 9:00 PM**, but app itineraries showed package delivery windows extending up to **10:00 PM**, forcing unscheduled overtime.
            * **Vehicle Package Trunk Sorting:** Substantial sorting difficulties inside the trunk due to mislabeling and incorrect stop sequence bundling.
            * **Unnotified Road Closures:** Route maps failed to incorporate live local council road closures, resulting in driver detours.
            """)

            st.subheader("Visual Evidence Categories Tagged")
            for cat in doc_data['Visual_Categories']:
                st.markdown(f'<span class="tag-badge">📌 {cat}</span>', unsafe_allow_html=True)

        with col_right:
            st.subheader("Attached Evidence Screenshots")
            
            with st.expander("📷 Map View: Road Closure & Detour", expanded=True):
                st.write("Map screenshot illustrating **'ROAD CLOSED'** signage along the designated route itinerary.")

            with st.expander("📷 Block Schedule Overrun Screenshot"):
                st.write("App schedule screenshot displaying initial 5:00 PM - 9:00 PM block alongside 10:00 PM delivery timestamps.")

            with st.expander("📷 Pickup Confirmation (42 Parcels)"):
                st.write("Confirmation timestamp proving package pickup at 5:00 PM at depot location.")

st.markdown("---")
with st.expander("📥 Export Raw Filtered Dataset", expanded=False):
    st.write(f"Exporting **{len(df_filtered)}** records matching active sidebar dropdown selections:")
    st.dataframe(df_filtered, use_container_width=True)
    
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Model as CSV",
        data=csv_data,
        file_name=f"aflex_sentiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
