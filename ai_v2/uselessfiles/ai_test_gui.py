"""
AI Crop Recommendation System - Interactive Testing GUI
Created for testing the enhanced AI model with previous crop and season analysis
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import traceback

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import prediction functions
try:
    from src.predict import predict_from_dict, load_all_models
    MODELS_LOADED = True
except ImportError:
    MODELS_LOADED = False
    st.error("Could not import prediction modules. Please check your installation.")

# Configure Streamlit page
st.set_page_config(
    page_title="🌾 Crop AI Testing Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme
st.markdown("""
<script>
    const stApp = window.parent.document.querySelector('.stApp');
    if (stApp) {
        stApp.setAttribute('data-theme', 'light');
    }
</script>
""", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: white !important;
        color: black !important;
    }
    
    /* Override dark mode */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .warning-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    .error-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
    
    /* Ensure text is visible in light mode */
    .stMarkdown, .stText, p, div {
        color: black !important;
    }
    
    /* Fix button colors */
    .stButton > button {
        background-color: #007bff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌾 Crop AI Testing Dashboard</h1>
    <p>Interactive testing interface for Enhanced Crop Recommendation System</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar for input parameters
st.sidebar.header("🔧 Input Parameters")

# Basic soil and climate parameters
st.sidebar.subheader("Soil Nutrients (kg/ha)")
col1, col2 = st.sidebar.columns(2)
with col1:
    nitrogen = st.number_input("Nitrogen (N)", min_value=0.0, max_value=200.0, value=60.0, step=1.0)
    phosphorus = st.number_input("Phosphorus (P)", min_value=0.0, max_value=150.0, value=45.0, step=1.0)
with col2:
    potassium = st.number_input("Potassium (K)", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
    ph = st.number_input("pH Level", min_value=3.5, max_value=9.0, value=6.5, step=0.1)

st.sidebar.subheader("Climate Conditions")
col3, col4 = st.sidebar.columns(2)
with col3:
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=55.0, value=25.0, step=0.5)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
with col4:
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=5000.0, value=800.0, step=10.0)
    area_ha = st.number_input("Area (hectares)", min_value=0.1, max_value=1000.0, value=2.0, step=0.1)

# Enhanced features
st.sidebar.subheader("🔬 Enhanced Features")
region = st.sidebar.selectbox("Region", ["default", "north", "south", "east", "west", "central"])

# Previous crop selection
previous_crops = [
    "", "rice", "wheat", "maize", "sugarcane", "cotton", "jute", "coconut", "papaya", "orange",
    "apple", "muskmelon", "watermelon", "grapes", "mango", "banana", "pomegranate", "lentil",
    "blackgram", "mungbean", "mothbeans", "pigeonpeas", "kidneybeans", "chickpea", "coffee"
]
previous_crop = st.sidebar.selectbox("Previous Crop", previous_crops)

# Season selection
season = st.sidebar.selectbox("Season", ["auto-detect", "kharif", "rabi", "zaid"])

# Planting date
planting_date = st.sidebar.date_input("Planting Date (for season detection)", value=date.today())

# Advanced options
with st.sidebar.expander("⚙️ Advanced Options"):
    include_explanations = st.checkbox("Include AI Explanations", value=True)
    show_confidence = st.checkbox("Show Confidence Scores", value=True)
    enable_comparison = st.checkbox("Enable Batch Comparison", value=False)

# Prediction button
predict_button = st.sidebar.button("🔮 Generate Prediction", type="primary", width="stretch")

# Preset examples
st.sidebar.subheader("📋 Preset Examples")
example_scenarios = {
    "Rice Farm (Kharif)": {
        "N": 80, "P": 40, "K": 40, "temperature": 27, "humidity": 80, 
        "ph": 6.0, "rainfall": 1200, "area_ha": 3.0, "season": "kharif"
    },
    "Wheat Farm (Rabi)": {
        "N": 120, "P": 60, "K": 40, "temperature": 20, "humidity": 65, 
        "ph": 7.5, "rainfall": 300, "area_ha": 5.0, "season": "rabi"
    },
    "Cotton Farm": {
        "N": 90, "P": 50, "K": 50, "temperature": 30, "humidity": 70, 
        "ph": 7.0, "rainfall": 600, "area_ha": 10.0, "season": "kharif"
    },
    "Vegetable Farm": {
        "N": 100, "P": 80, "K": 60, "temperature": 25, "humidity": 75, 
        "ph": 6.5, "rainfall": 500, "area_ha": 1.0, "season": "auto-detect"
    }
}

selected_example = st.sidebar.selectbox("Load Example", [""] + list(example_scenarios.keys()))
if st.sidebar.button("Load Example") and selected_example:
    st.rerun()

# Main content area
if MODELS_LOADED:
    # Create input dictionary
    input_data = {
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
        "area_ha": area_ha,
        "region": region,
        "previous_crop": previous_crop if previous_crop else "",
        "season": season if season != "auto-detect" else "",
        "planting_date": planting_date.isoformat() if season == "auto-detect" else ""
    }
    
    # Load example if selected
    if selected_example and selected_example in example_scenarios:
        example_data = example_scenarios[selected_example]
        for key, value in example_data.items():
            if key in input_data:
                input_data[key] = value
        st.success(f"Loaded example: {selected_example}")
    
    # Display current input summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("NPK Ratio", f"{nitrogen:.0f}-{phosphorus:.0f}-{potassium:.0f}")
    with col2:
        st.metric("Temperature", f"{temperature}°C")
    with col3:
        st.metric("Area", f"{area_ha} ha")
    
    # Make prediction when button is clicked
    if predict_button:
        with st.spinner("🔄 Generating AI prediction..."):
            try:
                # Make prediction
                result = predict_from_dict(input_data)
                
                # Store in history
                result['input_data'] = input_data.copy()
                result['timestamp'] = datetime.now().isoformat()
                st.session_state.prediction_history.append(result)
                
                # Display results
                if 'error' in result:
                    st.error(f"❌ Prediction Error: {result['error']}")
                else:
                    # Success - display comprehensive results
                    st.success("✅ Prediction Generated Successfully!")
                    
                    # Main recommendation
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "🌾 Recommended Crop", 
                            result['recommended_crop'].title(),
                            delta=f"{result['confidence']:.1%} confidence" if show_confidence else None
                        )
                    with col2:
                        st.metric(
                            "📈 Expected Yield", 
                            f"{result['expected_yield_t_per_acre']:.1f} t/acre"
                        )
                    with col3:
                        st.metric(
                            "💰 Net Profit", 
                            f"₹{result['profit_breakdown']['net']:,}"
                        )
                    with col4:
                        st.metric(
                            "📊 ROI", 
                            f"{result['profit_breakdown']['roi']:.1f}%"
                        )
                    
                    # Detailed results in tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📋 Summary", "🧪 Enhanced Analysis", "💰 Economics", 
                        "🌱 Fertilizer", "🔍 Explanations"
                    ])
                    
                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Yield Prediction")
                            yield_data = {
                                "Metric": ["Expected Yield", "Lower Bound (P10)", "Upper Bound (P90)"],
                                "Value (t/acre)": [
                                    result['expected_yield_t_per_acre'],
                                    result['yield_interval_p10_p90'][0],
                                    result['yield_interval_p10_p90'][1]
                                ]
                            }
                            st.dataframe(pd.DataFrame(yield_data), width="stretch")
                            
                        with col2:
                            st.subheader("Economic Summary")
                            profit_data = result['profit_breakdown']
                            st.write(f"**Gross Revenue:** ₹{profit_data['gross']:,}")
                            st.write(f"**Total Investment:** ₹{profit_data['investment']:,}")
                            st.write(f"**Net Profit:** ₹{profit_data['net']:,}")
                            st.write(f"**ROI:** {profit_data['roi']:.1f}%")
                    
                    with tab2:
                        st.subheader("🔬 Enhanced AI Analysis")
                        
                        # Previous crop analysis
                        if result.get('previous_crop_analysis', {}).get('previous_crop'):
                            st.markdown("**Previous Crop Impact:**")
                            pca = result['previous_crop_analysis']
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"Previous Crop: {pca['previous_crop'].title()}")
                                st.write(f"Original NPK: {pca['original_npk']}")
                            with col2:
                                st.write(f"Adjusted NPK: {pca['adjusted_npk']}")
                                st.write(f"Nutrient Impact: {pca['nutrient_impact']}")
                        
                        # Season analysis
                        st.markdown("**Season Analysis:**")
                        sa = result.get('season_analysis', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"Detected Season: {sa.get('detected_season', 'N/A').title()}")
                        with col2:
                            st.write(f"Season Suitability: {sa.get('season_suitability', 'N/A').title()}")
                        if sa.get('season_explanation'):
                            st.info(sa['season_explanation'])
                    
                    with tab3:
                        st.subheader("💰 Economic Analysis")
                        
                        # Create profit breakdown chart
                        profit_data = result['profit_breakdown']
                        fig = go.Figure(data=[
                            go.Bar(name='Revenue', x=['Financial Analysis'], y=[profit_data['gross']], marker_color='green'),
                            go.Bar(name='Investment', x=['Financial Analysis'], y=[profit_data['investment']], marker_color='red'),
                            go.Bar(name='Net Profit', x=['Financial Analysis'], y=[profit_data['net']], marker_color='blue')
                        ])
                        fig.update_layout(title="Financial Breakdown (₹)", barmode='group')
                        st.plotly_chart(fig, width="stretch")
                        
                        # ROI visualization
                        roi_fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = profit_data['roi'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Return on Investment (%)"},
                            gauge = {
                                'axis': {'range': [None, 200]},
                                'bar': {'color': "darkgreen"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 100], 'color': "yellow"},
                                    {'range': [100, 200], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 100
                                }
                            }
                        ))
                        st.plotly_chart(roi_fig, width="stretch")
                    
                    with tab4:
                        st.subheader("🌱 Fertilizer Recommendation")
                        fert = result.get('fertilizer_recommendation', {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fertilizer Type", fert.get('type', 'N/A'))
                        with col2:
                            st.metric("Dosage", f"{fert.get('dosage_kg_per_ha', 0)} kg/ha")
                        with col3:
                            st.metric("Cost", f"₹{fert.get('cost', 0):,}")
                        
                        # NPK comparison chart
                        if result.get('previous_crop_analysis'):
                            pca = result['previous_crop_analysis']
                            npk_df = pd.DataFrame({
                                'Nutrient': ['Nitrogen', 'Phosphorus', 'Potassium'],
                                'Original': pca['original_npk'],
                                'Adjusted': pca['adjusted_npk']
                            })
                            fig = px.bar(npk_df, x='Nutrient', y=['Original', 'Adjusted'], 
                                       title="NPK Values: Original vs AI-Adjusted", barmode='group')
                            st.plotly_chart(fig, width="stretch")
                    
                    with tab5:
                        if include_explanations and 'why' in result:
                            st.subheader("🔍 AI Explanations")
                            for i, explanation in enumerate(result['why'], 1):
                                st.write(f"**{i}.** {explanation}")
                        
                        # Technical details
                        with st.expander("🔧 Technical Details"):
                            st.write(f"**Model Version:** {result.get('model_version', 'N/A')}")
                            st.write(f"**Region:** {result.get('region', 'N/A')}")
                            st.write(f"**Analysis Time:** {result.get('timestamp', 'N/A')}")
                            
                            # Raw result JSON
                            st.json(result)
                            
            except Exception as e:
                st.error(f"❌ Error during prediction: {str(e)}")
                st.code(traceback.format_exc())

# Batch comparison feature
if enable_comparison and st.session_state.prediction_history:
    st.header("📊 Prediction History & Comparison")
    
    if len(st.session_state.prediction_history) > 1:
        # Create comparison dataframe
        history_data = []
        for i, pred in enumerate(st.session_state.prediction_history):
            if 'error' not in pred:
                history_data.append({
                    'Run': f"Run {i+1}",
                    'Crop': pred['recommended_crop'],
                    'Confidence': pred['confidence'],
                    'Yield (t/acre)': pred['expected_yield_t_per_acre'],
                    'Net Profit (₹)': pred['profit_breakdown']['net'],
                    'ROI (%)': pred['profit_breakdown']['roi'],
                    'NPK': f"{pred['input_data']['N']}-{pred['input_data']['P']}-{pred['input_data']['K']}"
                })
        
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df, width="stretch")
            
            # Comparison charts
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(df, x='Run', y='Yield (t/acre)', title="Yield Comparison")
                st.plotly_chart(fig1, width="stretch")
            with col2:
                fig2 = px.bar(df, x='Run', y='ROI (%)', title="ROI Comparison")
                st.plotly_chart(fig2, width="stretch")
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.prediction_history = []
        st.success("History cleared!")

# Model status and information
with st.expander("ℹ️ Model Information"):
    if MODELS_LOADED:
        st.success("✅ AI Models successfully loaded and ready")
        st.write("**Available Features:**")
        st.write("- 🌾 Crop recommendation with 20+ crops")
        st.write("- 🧪 Enhanced soil analysis with previous crop impact")
        st.write("- 🌍 Season and regional compatibility checking")
        st.write("- 💰 Profit estimation and ROI calculation")
        st.write("- 🌱 Intelligent fertilizer recommendations")
        st.write("- 🔍 AI-powered explanations")
    else:
        st.error("❌ AI Models not loaded. Please check installation.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🌾 Crop AI Testing Dashboard | Enhanced Agricultural Intelligence System<br>
    Built for Smart India Hackathon 2025 | Team HackBhoomi
</div>
""", unsafe_allow_html=True)
