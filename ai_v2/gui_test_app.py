"""
Streamlit GUI for Testing Crop AI Model
Interactive interface to test all AI features including crop prediction, fertilizer recommendation, and profit estimation
"""

import streamlit as st
import pandas as pd
import json
import requests
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time
import subprocess
import sys
import os

# Set page configuration
st.set_page_config(
    page_title="Crop AI Testing Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #cc0000;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #00cc00;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌾 Crop AI Testing Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for API configuration
st.sidebar.markdown("## ⚙️ Configuration")

# API endpoint configuration
api_mode = st.sidebar.radio(
    "Select Testing Mode:",
    ["Local API (FastAPI)", "Direct Model Testing", "Mock Data"]
)

if api_mode == "Local API (FastAPI)":
    api_url = st.sidebar.text_input("API URL:", value="http://localhost:8000")
    
    # Test API connection
    if st.sidebar.button("🔍 Test API Connection"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.sidebar.success("✅ API Connected!")
            else:
                st.sidebar.error(f"❌ API Error: {response.status_code}")
        except Exception as e:
            st.sidebar.error(f"❌ Connection Failed: {str(e)}")
            st.sidebar.info("💡 Make sure to start the FastAPI server first!")

# Quick start section
with st.sidebar.expander("🚀 Quick Start"):
    st.markdown("""
    **To start the API server:**
    1. Open terminal in project directory
    2. Activate virtual environment:
       ```
       .\\venv\\Scripts\\Activate.ps1
       ```
    3. Run the server:
       ```
       python simple_app.py
       ```
    4. API will be available at http://localhost:8000
    """)

# Main content area
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌱 Crop Prediction", 
    "🧪 Fertilizer Recommendation", 
    "💰 Profit Analysis", 
    "📊 Batch Testing", 
    "🔧 Model Testing"
])

def make_api_request(endpoint, data):
    """Make API request with error handling"""
    if api_mode == "Local API (FastAPI)":
        try:
            response = requests.post(f"{api_url}/{endpoint}", json=data, timeout=30)
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, f"API Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Connection Error: {str(e)}"
    else:
        # Mock response for demonstration
        return get_mock_response(endpoint, data), None

def get_mock_response(endpoint, data):
    """Generate mock responses for testing"""
    if endpoint == "predict":
        return {
            "recommended_crop": "rice",
            "confidence": 85.5,
            "top_3_recommendations": ["rice", "wheat", "maize"],
            "fertilizer_recommendation": {
                "type": "NPK 15-15-15",
                "dosage_kg_per_ha": 130,
                "cost": 3000
            },
            "profit_analysis": {
                "predicted_yield_quintals_per_ha": 45.2,
                "gross_revenue": 180800,
                "total_investment": 75500,
                "net_profit": 105300,
                "roi_percent": 139.5
            }
        }
    return {"status": "success", "message": "Mock response"}

# Crop Prediction Tab
with tab1:
    st.markdown('<h2 class="sub-header">🌱 Crop Prediction Testing</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Input Parameters")
        
        # Create two columns for input fields
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            st.markdown("**Soil Nutrients**")
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 60, help="Nitrogen content in soil")
            phosphorus = st.slider("Phosphorus (P)", 0, 150, 45, help="Phosphorus content in soil")
            potassium = st.slider("Potassium (K)", 0, 200, 50, help="Potassium content in soil")
            ph = st.slider("Soil pH", 3.5, 9.0, 6.8, step=0.1, help="Soil pH level")
        
        with input_col2:
            st.markdown("**Environmental Conditions**")
            temperature = st.slider("Temperature (°C)", -10, 55, 28, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 75, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0, 5000, 850, help="Annual rainfall")
            area_ha = st.number_input("Area (hectares)", 0.1, 1000.0, 2.5, help="Farm area in hectares")
        
        # Enhanced parameters
        st.markdown("**Enhanced Parameters** (Optional)")
        enhanced_col1, enhanced_col2 = st.columns(2)
        
        with enhanced_col1:
            previous_crop = st.selectbox(
                "Previous Crop",
                ["", "wheat", "rice", "maize", "cotton", "sugarcane", "potato", "tomato"],
                help="Crop grown previously on this field"
            )
            season = st.selectbox(
                "Season",
                ["Auto-detect", "kharif", "rabi", "zaid"],
                help="Growing season"
            )
        
        with enhanced_col2:
            region = st.selectbox(
                "Region",
                ["default", "north_india", "south_india", "east_india", "west_india", "central_india"],
                help="Geographic region"
            )
            planting_date = st.date_input(
                "Planting Date",
                value=date.today(),
                help="Planned planting date"
            )
        
        # Predict button
        if st.button("🔮 Predict Crop", type="primary", use_container_width=True):
            # Prepare request data
            request_data = {
                "N": nitrogen,
                "P": phosphorus,
                "K": potassium,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall,
                "area_ha": area_ha,
                "previous_crop": previous_crop,
                "season": None if season == "Auto-detect" else season,
                "region": region,
                "planting_date": planting_date.strftime("%Y-%m-%d")
            }
            
            with st.spinner("🤖 AI is analyzing your soil and climate data..."):
                time.sleep(1)  # Simulate processing time
                result, error = make_api_request("predict", request_data)
            
            if error:
                st.markdown(f'<div class="error-box">❌ <strong>Error:</strong> {error}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ <strong>Prediction Successful!</strong></div>', unsafe_allow_html=True)
                
                # Store result in session state for use in other tabs
                st.session_state['last_prediction'] = result
                st.session_state['last_request'] = request_data
    
    with col2:
        st.markdown("### 📋 Sample Inputs")
        
        # Predefined test cases
        test_cases = {
            "Rice Optimal": {
                "N": 80, "P": 40, "K": 40, "temperature": 25, 
                "humidity": 80, "ph": 6.5, "rainfall": 1200, "area_ha": 1.0
            },
            "Wheat Optimal": {
                "N": 50, "P": 60, "K": 50, "temperature": 20, 
                "humidity": 65, "ph": 7.0, "rainfall": 600, "area_ha": 2.0
            },
            "Maize Optimal": {
                "N": 120, "P": 60, "K": 80, "temperature": 27, 
                "humidity": 70, "ph": 6.8, "rainfall": 800, "area_ha": 1.5
            },
            "Poor Soil": {
                "N": 20, "P": 15, "K": 20, "temperature": 35, 
                "humidity": 40, "ph": 8.5, "rainfall": 200, "area_ha": 1.0
            }
        }
        
        for case_name, values in test_cases.items():
            if st.button(f"📝 Load {case_name}", use_container_width=True):
                for key, value in values.items():
                    if key in st.session_state:
                        st.session_state[key] = value
                st.rerun()
        
        # Display current input summary
        st.markdown("### 📊 Current Input Summary")
        current_input = pd.DataFrame({
            "Parameter": ["N", "P", "K", "Temperature", "Humidity", "pH", "Rainfall"],
            "Value": [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall],
            "Unit": ["ppm", "ppm", "ppm", "°C", "%", "", "mm"]
        })
        st.dataframe(current_input, use_container_width=True)

    # Display results if available
    if 'last_prediction' in st.session_state:
        st.markdown("---")
        st.markdown('<h3 class="sub-header">📈 Prediction Results</h3>', unsafe_allow_html=True)
        
        result = st.session_state['last_prediction']
        
        # Main prediction result
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            if 'recommended_crop' in result:
                st.markdown(f'''
                <div class="metric-card">
                    <h4>🏆 Recommended Crop</h4>
                    <h2 style="color: #2E8B57;">{result.get("recommended_crop", "N/A").title()}</h2>
                    <p>Confidence: {result.get("confidence", 0):.1f}%</p>
                </div>
                ''', unsafe_allow_html=True)
        
        with result_col2:
            if 'fertilizer_recommendation' in result:
                fert = result['fertilizer_recommendation']
                st.markdown(f'''
                <div class="metric-card">
                    <h4>🧪 Fertilizer</h4>
                    <h3 style="color: #2E8B57;">{fert.get("type", "N/A")}</h3>
                    <p>Dosage: {fert.get("dosage_kg_per_ha", 0)} kg/ha</p>
                    <p>Cost: ₹{fert.get("cost", 0):,}</p>
                </div>
                ''', unsafe_allow_html=True)
        
        with result_col3:
            if 'profit_analysis' in result:
                profit = result['profit_analysis']
                st.markdown(f'''
                <div class="metric-card">
                    <h4>💰 Profit Analysis</h4>
                    <h3 style="color: #2E8B57;">₹{profit.get("net_profit", 0):,}</h3>
                    <p>ROI: {profit.get("roi_percent", 0):.1f}%</p>
                    <p>Yield: {profit.get("predicted_yield_quintals_per_ha", 0):.1f} q/ha</p>
                </div>
                ''', unsafe_allow_html=True)
        
        # Top recommendations chart
        if 'top_3_recommendations' in result:
            st.markdown("### 📊 Top 3 Crop Recommendations")
            
            # Create mock confidence scores for visualization
            crops = result['top_3_recommendations'][:3]
            confidences = [result.get('confidence', 85), 
                          result.get('confidence', 85) * 0.8, 
                          result.get('confidence', 85) * 0.6]
            
            fig = px.bar(
                x=crops, 
                y=confidences,
                title="Crop Suitability Scores",
                labels={'x': 'Crops', 'y': 'Confidence (%)'},
                color=confidences,
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

# Fertilizer Recommendation Tab
with tab2:
    st.markdown('<h2 class="sub-header">🧪 Fertilizer Recommendation Testing</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Crop & Soil Parameters")
        
        fert_col1, fert_col2 = st.columns(2)
        
        with fert_col1:
            crop_type = st.selectbox(
                "Crop Type",
                ["rice", "wheat", "maize", "cotton", "sugarcane", "potato", "tomato", "onion", "garlic"],
                help="Select the crop for fertilizer recommendation"
            )
            
            soil_n = st.slider("Current Soil Nitrogen", 0, 200, 40, key="fert_n")
            soil_p = st.slider("Current Soil Phosphorus", 0, 150, 30, key="fert_p")
            soil_k = st.slider("Current Soil Potassium", 0, 200, 35, key="fert_k")
        
        with fert_col2:
            soil_ph_fert = st.slider("Soil pH", 3.5, 9.0, 6.5, step=0.1, key="fert_ph")
            organic_matter = st.slider("Organic Matter (%)", 0.5, 10.0, 2.5, step=0.1)
            soil_type = st.selectbox("Soil Type", ["clay", "sandy", "loamy", "black", "red"])
            farm_area = st.number_input("Farm Area (hectares)", 0.1, 100.0, 1.0, key="fert_area")
        
        if st.button("🧪 Get Fertilizer Recommendation", type="primary", use_container_width=True):
            fert_request = {
                "crop": crop_type,
                "N": soil_n,
                "P": soil_p,
                "K": soil_k,
                "ph": soil_ph_fert,
                "organic_matter": organic_matter,
                "soil_type": soil_type,
                "area_ha": farm_area
            }
            
            with st.spinner("🔬 Analyzing soil nutrients and crop requirements..."):
                time.sleep(1)
                # Mock fertilizer recommendation
                fert_result = {
                    "primary_fertilizer": {
                        "type": "NPK 15-15-15",
                        "dosage_kg_per_ha": 120,
                        "cost_per_ha": 2800,
                        "total_cost": 2800 * farm_area
                    },
                    "secondary_fertilizers": [
                        {"type": "Urea", "dosage_kg_per_ha": 50, "cost_per_ha": 800},
                        {"type": "SSP", "dosage_kg_per_ha": 75, "cost_per_ha": 1200}
                    ],
                    "organic_recommendations": [
                        {"type": "Compost", "dosage_tons_per_ha": 2.5, "cost_per_ha": 1500},
                        {"type": "Vermicompost", "dosage_tons_per_ha": 1.0, "cost_per_ha": 2000}
                    ],
                    "application_schedule": {
                        "basal": "60% at planting",
                        "first_dose": "25% at 30 days",
                        "second_dose": "15% at 60 days"
                    }
                }
                
                st.session_state['fertilizer_result'] = fert_result
    
    with col2:
        st.markdown("### 🌾 Crop Requirements")
        
        # Display typical nutrient requirements for selected crop
        crop_requirements = {
            "rice": {"N": "80-120", "P": "40-60", "K": "40-60"},
            "wheat": {"N": "80-120", "P": "60-80", "K": "40-60"},
            "maize": {"N": "120-150", "P": "60-80", "K": "60-80"},
            "cotton": {"N": "120-160", "P": "60-80", "K": "60-80"},
        }
        
        if crop_type in crop_requirements:
            req = crop_requirements[crop_type]
            st.markdown(f"""
            **Typical {crop_type.title()} Requirements (kg/ha):**
            - Nitrogen: {req['N']}
            - Phosphorus: {req['P']}
            - Potassium: {req['K']}
            """)
        
        st.markdown("### 💡 Tips")
        st.info("""
        - Test soil before fertilizer application
        - Consider organic alternatives
        - Follow recommended application timing
        - Monitor crop response
        """)

    # Display fertilizer results
    if 'fertilizer_result' in st.session_state:
        st.markdown("---")
        st.markdown('<h3 class="sub-header">🧪 Fertilizer Recommendations</h3>', unsafe_allow_html=True)
        
        fert_result = st.session_state['fertilizer_result']
        
        # Primary fertilizer recommendation
        primary = fert_result['primary_fertilizer']
        fert_col1, fert_col2, fert_col3 = st.columns(3)
        
        with fert_col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🎯 Primary Fertilizer</h4>
                <h3 style="color: #2E8B57;">{primary["type"]}</h3>
                <p>Dosage: {primary["dosage_kg_per_ha"]} kg/ha</p>
                <p>Cost: ₹{primary["total_cost"]:,}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with fert_col2:
            st.markdown("**Application Schedule**")
            schedule = fert_result['application_schedule']
            for timing, amount in schedule.items():
                st.write(f"• {timing.replace('_', ' ').title()}: {amount}")
        
        with fert_col3:
            st.markdown("**Alternative Options**")
            for alt in fert_result['secondary_fertilizers'][:2]:
                st.write(f"• {alt['type']}: {alt['dosage_kg_per_ha']} kg/ha")

# Profit Analysis Tab
with tab3:
    st.markdown('<h2 class="sub-header">💰 Profit Analysis Testing</h2>', unsafe_allow_html=True)
    
    if 'last_prediction' in st.session_state and 'profit_analysis' in st.session_state['last_prediction']:
        profit_data = st.session_state['last_prediction']['profit_analysis']
        
        # Key metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "Predicted Yield", 
                f"{profit_data.get('predicted_yield_quintals_per_ha', 0):.1f} q/ha",
                help="Expected crop yield per hectare"
            )
        
        with metric_col2:
            st.metric(
                "Gross Revenue", 
                f"₹{profit_data.get('gross_revenue', 0):,}",
                help="Total revenue from crop sale"
            )
        
        with metric_col3:
            st.metric(
                "Total Investment", 
                f"₹{profit_data.get('total_investment', 0):,}",
                help="Total cost including seeds, fertilizers, labor"
            )
        
        with metric_col4:
            roi = profit_data.get('roi_percent', 0)
            st.metric(
                "ROI", 
                f"{roi:.1f}%",
                delta=f"{roi - 100:.1f}%" if roi > 100 else None,
                help="Return on Investment"
            )
        
        # Profit breakdown chart
        st.markdown("### 📊 Profit Breakdown")
        
        breakdown_data = {
            'Category': ['Revenue', 'Investment', 'Net Profit'],
            'Amount': [
                profit_data.get('gross_revenue', 0),
                -profit_data.get('total_investment', 0),  # Negative for waterfall effect
                profit_data.get('net_profit', 0)
            ],
            'Color': ['green', 'red', 'blue']
        }
        
        fig = px.bar(
            x=breakdown_data['Category'],
            y=breakdown_data['Amount'],
            title="Financial Analysis",
            labels={'x': 'Category', 'y': 'Amount (₹)'},
            color=breakdown_data['Color'],
            color_discrete_map={'green': '#2E8B57', 'red': '#DC143C', 'blue': '#4169E1'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost breakdown (mock data)
        st.markdown("### 💸 Cost Breakdown")
        cost_breakdown = pd.DataFrame({
            'Cost Category': ['Seeds', 'Fertilizers', 'Pesticides', 'Labor', 'Irrigation', 'Others'],
            'Amount (₹)': [8000, 12000, 5000, 25000, 8000, 7000],
            'Percentage': [12.3, 18.5, 7.7, 38.5, 12.3, 10.8]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(cost_breakdown, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                cost_breakdown, 
                values='Amount (₹)', 
                names='Cost Category',
                title="Cost Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    else:
        st.info("🔮 Run a crop prediction first to see profit analysis!")
        if st.button("Go to Crop Prediction"):
            # This would ideally switch to tab1, but Streamlit doesn't support programmatic tab switching
            st.info("Please click on the 'Crop Prediction' tab above.")

# Batch Testing Tab
with tab4:
    st.markdown('<h2 class="sub-header">📊 Batch Testing</h2>', unsafe_allow_html=True)
    
    st.markdown("### Upload Test Dataset")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file with test data",
        type=['csv'],
        help="Upload a CSV file with columns: N, P, K, temperature, humidity, ph, rainfall"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} test cases")
            
            # Display data preview
            st.markdown("### 📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Validate required columns
            required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {missing_cols}")
            else:
                if st.button("🚀 Run Batch Predictions", type="primary"):
                    progress_bar = st.progress(0)
                    results = []
                    
                    for i, row in df.iterrows():
                        progress_bar.progress((i + 1) / len(df))
                        
                        # Simulate API call for each row
                        request_data = row.to_dict()
                        if 'area_ha' not in request_data:
                            request_data['area_ha'] = 1.0
                        
                        result, error = make_api_request("predict", request_data)
                        if result:
                            results.append({
                                'Index': i,
                                'Recommended_Crop': result.get('recommended_crop', 'Unknown'),
                                'Confidence': result.get('confidence', 0),
                                'Fertilizer': result.get('fertilizer_recommendation', {}).get('type', 'N/A'),
                                'Net_Profit': result.get('profit_analysis', {}).get('net_profit', 0)
                            })
                        
                        time.sleep(0.1)  # Simulate processing time
                    
                    # Display results
                    if results:
                        results_df = pd.DataFrame(results)
                        st.markdown("### 📈 Batch Results")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Summary statistics
                        st.markdown("### 📊 Summary Statistics")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            crop_counts = results_df['Recommended_Crop'].value_counts()
                            fig = px.pie(
                                values=crop_counts.values,
                                names=crop_counts.index,
                                title="Recommended Crops Distribution"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            avg_confidence = results_df['Confidence'].mean()
                            avg_profit = results_df['Net_Profit'].mean()
                            
                            st.metric("Average Confidence", f"{avg_confidence:.1f}%")
                            st.metric("Average Net Profit", f"₹{avg_profit:,.0f}")
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results",
                            csv,
                            "batch_prediction_results.csv",
                            "text/csv"
                        )
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    else:
        # Generate sample data
        st.markdown("### 🎲 Generate Sample Test Data")
        
        col1, col2 = st.columns(2)
        with col1:
            num_samples = st.number_input("Number of samples", 5, 100, 20)
        with col2:
            if st.button("Generate Sample Data"):
                np.random.seed(42)
                sample_data = pd.DataFrame({
                    'N': np.random.randint(20, 150, num_samples),
                    'P': np.random.randint(15, 100, num_samples),
                    'K': np.random.randint(20, 120, num_samples),
                    'temperature': np.random.uniform(15, 40, num_samples),
                    'humidity': np.random.uniform(40, 95, num_samples),
                    'ph': np.random.uniform(5.0, 8.5, num_samples),
                    'rainfall': np.random.uniform(200, 2000, num_samples),
                    'area_ha': np.random.uniform(0.5, 5.0, num_samples)
                })
                
                st.success(f"✅ Generated {num_samples} sample records")
                st.dataframe(sample_data, use_container_width=True)
                
                # Download sample data
                csv = sample_data.to_csv(index=False)
                st.download_button(
                    "📥 Download Sample Data",
                    csv,
                    "sample_test_data.csv",
                    "text/csv"
                )

# Model Testing Tab
with tab5:
    st.markdown('<h2 class="sub-header">🔧 Model Testing & Diagnostics</h2>', unsafe_allow_html=True)
    
    # API Health Check
    st.markdown("### 🏥 API Health Check")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Check API Status"):
            if api_mode == "Local API (FastAPI)":
                try:
                    # Test different endpoints
                    endpoints = [
                        ("/health", "Health Check"),
                        ("/docs", "API Documentation"),
                        ("/", "Root Endpoint")
                    ]
                    
                    for endpoint, name in endpoints:
                        try:
                            response = requests.get(f"{api_url}{endpoint}", timeout=5)
                            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                            st.write(f"{name}: {status}")
                        except:
                            st.write(f"{name}: ❌ Failed")
                            
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
            else:
                st.info("API health check only available in Local API mode")
    
    with col2:
        st.markdown("**API Endpoints:**")
        st.code("""
        GET  /health        - Health check
        POST /predict       - Crop prediction
        POST /fertilizer    - Fertilizer recommendation
        POST /profit        - Profit analysis
        GET  /docs          - API documentation
        """)
    
    # Model Performance Testing
    st.markdown("### ⚡ Performance Testing")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        num_requests = st.slider("Number of test requests", 1, 50, 10)
        
        if st.button("🚀 Run Performance Test"):
            test_data = {
                "N": 60, "P": 45, "K": 50, "temperature": 28,
                "humidity": 75, "ph": 6.8, "rainfall": 850, "area_ha": 1.0
            }
            
            times = []
            success_count = 0
            
            progress = st.progress(0)
            for i in range(num_requests):
                start_time = time.time()
                result, error = make_api_request("predict", test_data)
                end_time = time.time()
                
                if not error:
                    success_count += 1
                times.append(end_time - start_time)
                progress.progress((i + 1) / num_requests)
            
            # Display results
            avg_time = np.mean(times)
            success_rate = success_count / num_requests * 100
            
            st.metric("Average Response Time", f"{avg_time:.3f}s")
            st.metric("Success Rate", f"{success_rate:.1f}%")
            st.metric("Requests per Second", f"{1/avg_time:.1f}")
    
    with perf_col2:
        st.markdown("### 📊 System Requirements")
        st.markdown("""
        **Recommended System:**
        - RAM: 4GB+ 
        - CPU: 2+ cores
        - Storage: 1GB+ free space
        - Python: 3.8+
        
        **Dependencies:**
        - FastAPI
        - Scikit-learn
        - Pandas, NumPy
        - Joblib
        """)
    
    # Error Testing
    st.markdown("### 🐛 Error Handling Tests")
    
    error_tests = {
        "Invalid pH": {"N": 60, "P": 45, "K": 50, "ph": 15.0, "temperature": 28, "humidity": 75, "rainfall": 850},
        "Negative Values": {"N": -10, "P": 45, "K": 50, "ph": 6.8, "temperature": 28, "humidity": 75, "rainfall": 850},
        "Extreme Temperature": {"N": 60, "P": 45, "K": 50, "ph": 6.8, "temperature": 100, "humidity": 75, "rainfall": 850},
        "Missing Fields": {"N": 60, "P": 45}  # Missing required fields
    }
    
    if st.button("🧪 Run Error Tests"):
        for test_name, test_data in error_tests.items():
            with st.expander(f"Test: {test_name}"):
                result, error = make_api_request("predict", test_data)
                if error:
                    st.error(f"❌ Expected error caught: {error}")
                else:
                    st.warning(f"⚠️ Unexpected success for invalid input")
                st.json(test_data)

# Footer
st.markdown("---")
st.markdown(
    "🌾 **Crop AI Testing Dashboard** | "
    "Built with Streamlit | "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

# Add some helpful information in the sidebar
with st.sidebar.expander("ℹ️ About"):
    st.markdown("""
    **Crop AI Testing Dashboard**
    
    This interface allows you to test all features of the Crop AI system:
    
    - 🌱 **Crop Prediction**: Get crop recommendations based on soil and climate
    - 🧪 **Fertilizer**: Get fertilizer recommendations for specific crops
    - 💰 **Profit Analysis**: Analyze potential profits and ROI
    - 📊 **Batch Testing**: Test multiple scenarios at once
    - 🔧 **Diagnostics**: Test API health and performance
    
    **Tips:**
    - Start the FastAPI server first
    - Use sample inputs for quick testing
    - Try batch testing with your own CSV data
    - Monitor API performance in the diagnostics tab
    """)

with st.sidebar.expander("🚀 Getting Started"):
    st.markdown("""
    **To start testing:**
    
    1. **Start the API server:**
       ```powershell
       cd your_project_directory
       .\venv\Scripts\Activate.ps1
       python simple_app.py
       ```
    
    2. **Test the connection** using the button above
    
    3. **Try a prediction** in the Crop Prediction tab
    
    4. **Explore other features** in the remaining tabs
    
    **Sample API calls are also available in mock mode for demonstration.**
    """)
