import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Health Monitoring Dashboard",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with animations
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 20px;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin-bottom: 20px;
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.25);
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85em;
        color: #666;
        font-weight: 500;
        margin-top: 5px;
    }
    
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }
    
    .header-title {
        color: white;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        margin: 0;
        padding: 20px 0;
    }
    
    .stAlert {
        border-radius: 12px;
        animation: slideIn 0.4s ease-out;
    }
    
    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(26, 26, 46, 0.9);
    }
    
    .sidebar-text {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="header-title">Health Monitoring Analysis Dashboard</h1>', unsafe_allow_html=True)
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("### Upload Data")
    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=['csv'],
        help="Upload health monitoring data"
    )
    
    st.divider()
    st.markdown("### Expected Columns")
    st.markdown("""
    - Thermoregulation
    - HeartRateVariation
    - BloodOxygen
    - ActivityLevel
    - SleepPatterns
    - HormoneImbalance
    """)
    
    if uploaded_file:
        st.success("File uploaded")

# Main content
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} records")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview", 
            "Distributions", 
            "Correlations", 
            "Analysis",
            "Raw Data"
        ])
        
        # TAB 1: OVERVIEW
        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("## Overview Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Avg Temperature</div>
                    <div class="metric-value">{df['Thermoregulation'].mean():.2f}°C</div>
                    <div class="metric-label" style="font-size: 0.75em; margin-top: 3px;">±{df['Thermoregulation'].std():.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Avg Heart Rate</div>
                    <div class="metric-value">{df['HeartRateVariation'].mean():.1f}</div>
                    <div class="metric-label" style="font-size: 0.75em; margin-top: 3px;">bpm ±{df['HeartRateVariation'].std():.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Avg Blood Oxygen</div>
                    <div class="metric-value">{df['BloodOxygen'].mean():.1f}%</div>
                    <div class="metric-label" style="font-size: 0.75em; margin-top: 3px;">±{df['BloodOxygen'].std():.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Avg Sleep</div>
                    <div class="metric-value">{df['SleepPatterns'].mean():.1f}</div>
                    <div class="metric-label" style="font-size: 0.75em; margin-top: 3px;">hrs ±{df['SleepPatterns'].std():.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Summary Statistics")
                st.dataframe(df.describe().round(2), use_container_width=True)
            
            with col2:
                st.subheader("Activity & Hormone Status")
                
                activity_counts = df['ActivityLevel'].value_counts().sort_index()
                fig_activity = px.pie(
                    values=activity_counts.values,
                    names=[f"Level {i}" for i in activity_counts.index],
                    title="Activity Distribution",
                    color_discrete_sequence=px.colors.sequential.Purples,
                    height=300
                )
                fig_activity.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=True)
                st.plotly_chart(fig_activity, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # TAB 2: DISTRIBUTIONS
        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("## Distribution Analysis")
            
            st.subheader("Temperature Trend")
            fig_temp = px.line(
                df.reset_index(),
                x='index',
                y='Thermoregulation',
                title='Body Temperature Over Time',
                labels={'index': 'Reading', 'Thermoregulation': 'Temp (°C)'},
                height=350
            )
            fig_temp.update_traces(line=dict(color='#ef4444', width=2))
            st.plotly_chart(fig_temp, use_container_width=True, config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Heart Rate Distribution")
                fig_hr = px.histogram(
                    df,
                    x='HeartRateVariation',
                    nbins=25,
                    title='Heart Rate Frequency',
                    height=300,
                    labels={'HeartRateVariation': 'bpm'}
                )
                fig_hr.update_traces(marker_color='#6366f1')
                st.plotly_chart(fig_hr, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                st.subheader("Blood Oxygen Distribution")
                fig_oxygen = px.histogram(
                    df,
                    x='BloodOxygen',
                    nbins=25,
                    title='Blood Oxygen Level',
                    height=300,
                    labels={'BloodOxygen': '%'}
                )
                fig_oxygen.update_traces(marker_color='#10b981')
                st.plotly_chart(fig_oxygen, use_container_width=True, config={'displayModeBar': False})
            
            st.subheader("Sleep Patterns")
            fig_sleep = px.line(
                df.reset_index(),
                x='index',
                y='SleepPatterns',
                title='Sleep Duration Over Time',
                labels={'index': 'Reading', 'SleepPatterns': 'Hours'},
                height=350
            )
            fig_sleep.update_traces(line=dict(color='#8b5cf6', width=2))
            st.plotly_chart(fig_sleep, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # TAB 3: CORRELATIONS
        with tab3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("## Correlation Analysis")
            
            numeric_cols = ['Thermoregulation', 'HeartRateVariation', 'BloodOxygen', 
                           'ActivityLevel', 'SleepPatterns', 'HormoneImbalance']
            corr_matrix = df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu_r',
                title='Correlation Heatmap',
                height=500
            )
            st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Temperature vs Heart Rate")
                fig_s1 = px.scatter(
                    df,
                    x='Thermoregulation',
                    y='HeartRateVariation',
                    color='ActivityLevel',
                    height=350,
                    labels={'Thermoregulation': 'Temp (°C)', 'HeartRateVariation': 'Heart Rate (bpm)'}
                )
                st.plotly_chart(fig_s1, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                st.subheader("Sleep vs Blood Oxygen")
                fig_s2 = px.scatter(
                    df,
                    x='SleepPatterns',
                    y='BloodOxygen',
                    color='HormoneImbalance',
                    height=350,
                    color_discrete_map={0: '#10b981', 1: '#ef4444'},
                    labels={'SleepPatterns': 'Sleep (hrs)', 'BloodOxygen': 'O2 (%)'}
                )
                st.plotly_chart(fig_s2, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # TAB 4: ANALYSIS
        with tab4:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("## Detailed Health Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Key Findings")
                
                temp_normal = df[(df['Thermoregulation'] >= 36.1) & (df['Thermoregulation'] <= 37.2)]
                temp_pct = (len(temp_normal) / len(df)) * 100
                st.markdown(f"**Temperature:** {temp_pct:.1f}% normal (36.1-37.2°C) | Mean: {df['Thermoregulation'].mean():.2f}°C")
                
                hr_normal = df[(df['HeartRateVariation'] >= 60) & (df['HeartRateVariation'] <= 100)]
                hr_pct = (len(hr_normal) / len(df)) * 100
                st.markdown(f"**Heart Rate:** {hr_pct:.1f}% normal (60-100 bpm) | Mean: {df['HeartRateVariation'].mean():.1f} bpm")
                
                oxygen_normal = df[df['BloodOxygen'] >= 95]
                oxygen_pct = (len(oxygen_normal) / len(df)) * 100
                st.markdown(f"**Blood Oxygen:** {oxygen_pct:.1f}% healthy (≥95%) | Mean: {df['BloodOxygen'].mean():.1f}%")
                
                sleep_good = df[df['SleepPatterns'] >= 7]
                sleep_pct = (len(sleep_good) / len(df)) * 100
                st.markdown(f"**Sleep:** {sleep_pct:.1f}% sufficient (≥7 hrs) | Mean: {df['SleepPatterns'].mean():.1f} hrs")
            
            with col2:
                st.markdown("### Health Alerts")
                
                alerts = []
                
                if len(df[df['Thermoregulation'] > 37.5]) > 0:
                    alerts.append((len(df[df['Thermoregulation'] > 37.5]), "High temperature (>37.5°C)"))
                if len(df[df['Thermoregulation'] < 36.0]) > 0:
                    alerts.append((len(df[df['Thermoregulation'] < 36.0]), "Low temperature (<36.0°C)"))
                if len(df[df['HeartRateVariation'] > 100]) > 0:
                    alerts.append((len(df[df['HeartRateVariation'] > 100]), "High heart rate (>100 bpm)"))
                if len(df[df['HeartRateVariation'] < 60]) > 0:
                    alerts.append((len(df[df['HeartRateVariation'] < 60]), "Low heart rate (<60 bpm)"))
                if len(df[df['BloodOxygen'] < 95]) > 0:
                    alerts.append((len(df[df['BloodOxygen'] < 95]), "Low oxygen (<95%)"))
                if len(df[df['SleepPatterns'] < 6]) > 0:
                    alerts.append((len(df[df['SleepPatterns'] < 6]), "Poor sleep (<6 hrs)"))
                if len(df[df['HormoneImbalance'] == 1]) > 0:
                    alerts.append((len(df[df['HormoneImbalance'] == 1]), "Hormone imbalance"))
                
                if alerts:
                    for count, alert in alerts:
                        st.warning(f"{count} readings: {alert}")
                else:
                    st.success("All readings within healthy ranges!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # TAB 5: RAW DATA
        with tab5:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("## Raw Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                activity_filter = st.multiselect(
                    "Activity Level",
                    sorted(df['ActivityLevel'].unique()),
                    default=sorted(df['ActivityLevel'].unique())
                )
            
            with col2:
                hormone_filter = st.multiselect(
                    "Hormone Status",
                    [0, 1],
                    format_func=lambda x: 'Balanced' if x == 0 else 'Imbalanced',
                    default=[0, 1]
                )
            
            with col3:
                temp_range = st.slider(
                    "Temperature",
                    float(df['Thermoregulation'].min()),
                    float(df['Thermoregulation'].max()),
                    (float(df['Thermoregulation'].min()), float(df['Thermoregulation'].max()))
                )
            
            filtered_df = df[
                (df['ActivityLevel'].isin(activity_filter)) &
                (df['HormoneImbalance'].isin(hormone_filter)) &
                (df['Thermoregulation'] >= temp_range[0]) &
                (df['Thermoregulation'] <= temp_range[1])
            ]
            
            st.write(f"Showing {len(filtered_df)} of {len(df)} records")
            st.dataframe(filtered_df, use_container_width=True)
            
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "filtered_data.csv",
                "text/csv"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Check CSV format and column names.")

else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Welcome to Health Monitoring Dashboard")
    st.markdown("Upload your health data CSV to begin analysis")
    st.markdown("#### Made By: Antra Patel")
    
    sample_data = {
        'Thermoregulation': [36.65, 36.01, 36.57],
        'HeartRateVariation': [77.82, 60.88, 69.80],
        'BloodOxygen': [100.47, 97.77, 97.22],
        'ActivityLevel': [0, 4, 0],
        'SleepPatterns': [3.05, 5.67, 7.75],
        'HormoneImbalance': [1, 0, 0]
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)