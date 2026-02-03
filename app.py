import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# Page configuration
st.set_page_config(
    page_title="Health Monitoring Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with warm vintage color scheme
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f5dc 0%, #faf8f3 100%);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #2c2c2c;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Health Monitoring Analysis Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your health monitoring data CSV file"
    )
    
    st.markdown("---")
    st.subheader("Expected Format")
    st.markdown("""
    The CSV should contain:
    - Thermoregulation
    - HeartRateVariation
    - BloodOxygen
    - ActivityLevel
    - SleepPatterns
    - HormoneImbalance
    """)
    
    if uploaded_file:
        st.success("File uploaded successfully!")

# Main content
if uploaded_file is not None:
    try:
        # Read the data
        df = pd.read_csv(uploaded_file)
        
        # Display basic info
        st.success(f"Loaded {len(df)} records")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview", 
            "Distributions", 
            "Correlations", 
            "Detailed Analysis",
            "Raw Data"
        ])
        
        # TAB 1: OVERVIEW
        with tab1:
            st.header("Overview Statistics")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Avg Temperature",
                    f"{df['Thermoregulation'].mean():.2f}°C",
                    delta=f"±{df['Thermoregulation'].std():.2f}"
                )
            
            with col2:
                st.metric(
                    "Avg Heart Rate",
                    f"{df['HeartRateVariation'].mean():.1f} bpm",
                    delta=f"±{df['HeartRateVariation'].std():.1f}"
                )
            
            with col3:
                st.metric(
                    "Avg Blood Oxygen",
                    f"{df['BloodOxygen'].mean():.1f}%",
                    delta=f"±{df['BloodOxygen'].std():.1f}"
                )
            
            with col4:
                st.metric(
                    "Avg Sleep",
                    f"{df['SleepPatterns'].mean():.1f} hrs",
                    delta=f"±{df['SleepPatterns'].std():.1f}"
                )
            
            st.markdown("---")
            
            # Summary statistics table
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Summary Statistics")
                summary_stats = df.describe().round(2)
                st.dataframe(summary_stats, width='stretch')
            
            with col2:
                st.subheader("Health Indicators")
                
                # Activity level distribution
                activity_counts = df['ActivityLevel'].value_counts().sort_index()
                fig_activity = px.pie(
                    values=activity_counts.values,
                    names=[f"Level {i}" for i in activity_counts.index],
                    title="Activity Level Distribution",
                    color_discrete_sequence=px.colors.sequential.Purples
                )
                fig_activity.update_layout(
                    margin=dict(t=50, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_activity, config={'displayModeBar': False})
                
                # Hormone imbalance
                hormone_counts = df['HormoneImbalance'].value_counts()
                hormone_labels = ['Balanced', 'Imbalanced']
                fig_hormone = px.pie(
                    values=hormone_counts.values,
                    names=[hormone_labels[i] for i in hormone_counts.index],
                    title="Hormone Balance Status",
                    color_discrete_map={'Balanced': '#10b981', 'Imbalanced': '#ec4899'}
                )
                fig_hormone.update_layout(
                    margin=dict(t=50, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_hormone, config={'displayModeBar': False})
        
        # TAB 2: DISTRIBUTIONS
        with tab2:
            st.header("Distribution Analysis")
            
            # Thermoregulation over time
            st.subheader("Thermoregulation Trend")
            fig_temp = px.line(
                df.reset_index(),
                x='index',
                y='Thermoregulation',
                title='Body Temperature Over Time',
                labels={'index': 'Reading Number', 'Thermoregulation': 'Temperature (°C)'}
            )
            fig_temp.update_traces(line_color='#ec4899', line_width=2)
            st.plotly_chart(fig_temp, config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Heart Rate Variation
                st.subheader("Heart Rate Distribution")
                fig_hr = px.histogram(
                    df,
                    x='HeartRateVariation',
                    nbins=30,
                    title='Heart Rate Frequency Distribution',
                    labels={'HeartRateVariation': 'Heart Rate (bpm)'}
                )
                fig_hr.update_traces(marker_color='#6366f1')
                st.plotly_chart(fig_hr, config={'displayModeBar': False})
            
            with col2:
                # Blood Oxygen
                st.subheader("Blood Oxygen Distribution")
                fig_oxygen = px.histogram(
                    df,
                    x='BloodOxygen',
                    nbins=30,
                    title='Blood Oxygen Level Distribution',
                    labels={'BloodOxygen': 'Blood Oxygen (%)'}
                )
                fig_oxygen.update_traces(marker_color='#10b981')
                st.plotly_chart(fig_oxygen, config={'displayModeBar': False})
            
            # Sleep patterns
            st.subheader("Sleep Patterns")
            fig_sleep = px.line(
                df.reset_index(),
                x='index',
                y='SleepPatterns',
                title='Sleep Duration Over Time',
                labels={'index': 'Reading Number', 'SleepPatterns': 'Sleep (hours)'}
            )
            fig_sleep.update_traces(line_color='#8b5cf6', line_width=2)
            st.plotly_chart(fig_sleep, config={'displayModeBar': False})
        
        # TAB 3: CORRELATIONS
        with tab3:
            st.header("Correlation Analysis")
            
            # Correlation matrix
            st.subheader("Correlation Matrix")
            numeric_cols = ['Thermoregulation', 'HeartRateVariation', 'BloodOxygen', 
                           'ActivityLevel', 'SleepPatterns', 'HormoneImbalance']
            corr_matrix = df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                title='Correlation Heatmap'
            )
            st.plotly_chart(fig_corr, config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter: Temperature vs Heart Rate
                st.subheader("Temperature vs Heart Rate")
                fig_scatter1 = px.scatter(
                    df,
                    x='Thermoregulation',
                    y='HeartRateVariation',
                    color='ActivityLevel',
                    title='Temperature vs Heart Rate (colored by Activity)',
                    labels={
                        'Thermoregulation': 'Temperature (°C)',
                        'HeartRateVariation': 'Heart Rate (bpm)'
                    }
                )
                st.plotly_chart(fig_scatter1, config={'displayModeBar': False})
            
            with col2:
                # Scatter: Sleep vs Blood Oxygen
                st.subheader("Sleep vs Blood Oxygen")
                fig_scatter2 = px.scatter(
                    df,
                    x='SleepPatterns',
                    y='BloodOxygen',
                    color='HormoneImbalance',
                    title='Sleep Patterns vs Blood Oxygen',
                    labels={
                        'SleepPatterns': 'Sleep (hours)',
                        'BloodOxygen': 'Blood Oxygen (%)'
                    },
                    color_discrete_map={0: '#10b981', 1: '#ec4899'}
                )
                st.plotly_chart(fig_scatter2, config={'displayModeBar': False})
            
            # 3D Scatter
            st.subheader("3D Relationship View")
            fig_3d = px.scatter_3d(
                df.sample(min(500, len(df))),
                x='Thermoregulation',
                y='HeartRateVariation',
                z='BloodOxygen',
                color='SleepPatterns',
                title='3D View: Temperature, Heart Rate & Blood Oxygen',
                labels={
                    'Thermoregulation': 'Temperature',
                    'HeartRateVariation': 'Heart Rate',
                    'BloodOxygen': 'Blood Oxygen'
                }
            )
            st.plotly_chart(fig_3d, config={'displayModeBar': False})
        
        # TAB 4: DETAILED ANALYSIS
        with tab4:
            st.header("Detailed Health Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Key Findings")
                
                # Temperature analysis
                temp_normal = df[(df['Thermoregulation'] >= 36.1) & (df['Thermoregulation'] <= 37.2)]
                temp_pct = (len(temp_normal) / len(df)) * 100
                
                st.markdown(f"""
                **Thermoregulation:**
                - {temp_pct:.1f}% readings in normal range (36.1-37.2°C)
                - Mean: {df['Thermoregulation'].mean():.2f}°C
                - Range: {df['Thermoregulation'].min():.2f} - {df['Thermoregulation'].max():.2f}°C
                """)
                
                # Heart rate analysis
                hr_normal = df[(df['HeartRateVariation'] >= 60) & (df['HeartRateVariation'] <= 100)]
                hr_pct = (len(hr_normal) / len(df)) * 100
                
                st.markdown(f"""
                **Heart Rate:**
                - {hr_pct:.1f}% readings in normal range (60-100 bpm)
                - Mean: {df['HeartRateVariation'].mean():.1f} bpm
                - Range: {df['HeartRateVariation'].min():.1f} - {df['HeartRateVariation'].max():.1f} bpm
                """)
                
                # Blood oxygen
                oxygen_normal = df[df['BloodOxygen'] >= 95]
                oxygen_pct = (len(oxygen_normal) / len(df)) * 100
                
                st.markdown(f"""
                **Blood Oxygen:**
                - {oxygen_pct:.1f}% readings above 95% (healthy)
                - Mean: {df['BloodOxygen'].mean():.1f}%
                - Range: {df['BloodOxygen'].min():.1f} - {df['BloodOxygen'].max():.1f}%
                """)
                
                # Sleep analysis
                sleep_good = df[df['SleepPatterns'] >= 7]
                sleep_pct = (len(sleep_good) / len(df)) * 100
                
                st.markdown(f"""
                **Sleep Patterns:**
                - {sleep_pct:.1f}% nights with 7+ hours (recommended)
                - Mean: {df['SleepPatterns'].mean():.1f} hours
                - Range: {df['SleepPatterns'].min():.1f} - {df['SleepPatterns'].max():.1f} hours
                """)
            
            with col2:
                st.subheader("Health Alerts")
                
                # Find anomalies
                alerts = []
                
                # Temperature alerts
                temp_high = df[df['Thermoregulation'] > 37.5]
                if len(temp_high) > 0:
                    alerts.append(f"{len(temp_high)} readings with elevated temperature (>37.5°C)")
                
                temp_low = df[df['Thermoregulation'] < 36.0]
                if len(temp_low) > 0:
                    alerts.append(f"{len(temp_low)} readings with low temperature (<36.0°C)")
                
                # Heart rate alerts
                hr_high = df[df['HeartRateVariation'] > 100]
                if len(hr_high) > 0:
                    alerts.append(f"{len(hr_high)} readings with high heart rate (>100 bpm)")
                
                hr_low = df[df['HeartRateVariation'] < 60]
                if len(hr_low) > 0:
                    alerts.append(f"{len(hr_low)} readings with low heart rate (<60 bpm)")
                
                # Oxygen alerts
                oxygen_low = df[df['BloodOxygen'] < 95]
                if len(oxygen_low) > 0:
                    alerts.append(f"{len(oxygen_low)} readings with low oxygen (<95%)")
                
                # Sleep alerts
                sleep_poor = df[df['SleepPatterns'] < 6]
                if len(sleep_poor) > 0:
                    alerts.append(f"{len(sleep_poor)} nights with insufficient sleep (<6 hours)")
                
                # Hormone alerts
                hormone_issues = df[df['HormoneImbalance'] == 1]
                if len(hormone_issues) > 0:
                    alerts.append(f"{len(hormone_issues)} readings with hormone imbalance")
                
                if alerts:
                    for alert in alerts:
                        st.warning(alert)
                else:
                    st.success("All readings within healthy ranges!")
            
            # Activity vs Health Metrics
            st.subheader("Activity Level Impact")
            
            activity_metrics = df.groupby('ActivityLevel').agg({
                'Thermoregulation': 'mean',
                'HeartRateVariation': 'mean',
                'BloodOxygen': 'mean',
                'SleepPatterns': 'mean'
            }).reset_index()
            
            fig_activity = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Temperature', 'Heart Rate', 'Blood Oxygen', 'Sleep')
            )
            
            fig_activity.add_trace(
                go.Bar(x=activity_metrics['ActivityLevel'], 
                       y=activity_metrics['Thermoregulation'],
                       marker_color='#ec4899'),
                row=1, col=1
            )
            
            fig_activity.add_trace(
                go.Bar(x=activity_metrics['ActivityLevel'], 
                       y=activity_metrics['HeartRateVariation'],
                       marker_color='#6366f1'),
                row=1, col=2
            )
            
            fig_activity.add_trace(
                go.Bar(x=activity_metrics['ActivityLevel'], 
                       y=activity_metrics['BloodOxygen'],
                       marker_color='#10b981'),
                row=2, col=1
            )
            
            fig_activity.add_trace(
                go.Bar(x=activity_metrics['ActivityLevel'], 
                       y=activity_metrics['SleepPatterns'],
                       marker_color='#8b5cf6'),
                row=2, col=2
            )
            
            fig_activity.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_activity, config={'displayModeBar': False})
        
        # TAB 5: RAW DATA
        with tab5:
            st.header("Raw Data View")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                activity_filter = st.multiselect(
                    "Filter by Activity Level",
                    options=sorted(df['ActivityLevel'].unique()),
                    default=sorted(df['ActivityLevel'].unique())
                )
            
            with col2:
                hormone_filter = st.multiselect(
                    "Filter by Hormone Status",
                    options=[0, 1],
                    format_func=lambda x: 'Balanced' if x == 0 else 'Imbalanced',
                    default=[0, 1]
                )
            
            with col3:
                temp_range = st.slider(
                    "Temperature Range (°C)",
                    float(df['Thermoregulation'].min()),
                    float(df['Thermoregulation'].max()),
                    (float(df['Thermoregulation'].min()), float(df['Thermoregulation'].max()))
                )
            
            # Apply filters
            filtered_df = df[
                (df['ActivityLevel'].isin(activity_filter)) &
                (df['HormoneImbalance'].isin(hormone_filter)) &
                (df['Thermoregulation'] >= temp_range[0]) &
                (df['Thermoregulation'] <= temp_range[1])
            ]
            
            st.write(f"Showing {len(filtered_df)} of {len(df)} records")
            st.dataframe(filtered_df, width='stretch')
            
            # Download filtered data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name="filtered_health_data.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please ensure your CSV has the correct format and column names.")

else:
    # Welcome message
    st.info("Please upload a CSV file to begin analysis")
    
    # Sample data format
    st.subheader("Sample Data Format")
    sample_data = {
        'Thermoregulation': [36.65, 36.01, 36.57],
        'HeartRateVariation': [77.82, 60.88, 69.80],
        'BloodOxygen': [100.47, 97.77, 97.22],
        'ActivityLevel': [0, 4, 0],
        'SleepPatterns': [3.05, 5.67, 7.75],
        'HormoneImbalance': [1, 0, 0]
    }
    st.dataframe(pd.DataFrame(sample_data), width='stretch')
    
    st.markdown("""
    ### How to Use
    1. Prepare your CSV file with the health monitoring data
    2. Upload the file using the sidebar
    3. Explore different tabs for comprehensive analysis:
       - **Overview**: Key metrics and summary statistics
       - **Distributions**: Visual patterns in your data
       - **Correlations**: Relationships between variables
       - **Detailed Analysis**: Health insights and alerts
       - **Raw Data**: View and filter the complete dataset
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Health Monitoring Dashboard | Built with Streamlit & Plotly</div>",
    unsafe_allow_html=True
)