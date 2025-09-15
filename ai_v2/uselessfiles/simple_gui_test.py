"""
Simple AI Crop Testing Interface
A lightweight version that works with or without trained models
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
import random

# Configure Streamlit page
st.set_page_config(
    page_title="🌾 Crop AI Tester",
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

# Custom CSS
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
    .stMetric {
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
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

# Header
st.markdown("""
<div class="main-header">
    <h1>🌾 Crop AI Tester</h1>
    <p>Test your AI model with different input scenarios</p>
</div>
""", unsafe_allow_html=True)

# Check if models are available
@st.cache_data
def check_models():
    """Check if the AI models are available"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.predict import predict_from_dict
        return True, predict_from_dict
    except ImportError:
        return False, None

models_available, predict_func = check_models()

# Fallback prediction function for testing without models
def fallback_prediction(input_data):
    """Generate realistic test predictions when models aren't available"""
    import random
    
    # Define crop database with detailed requirements
    crop_database = {
        'rice': {
            'temp_range': (20, 35), 'humidity_range': (70, 100), 'rainfall_range': (1000, 3000),
            'ph_range': (5.5, 7.0), 'n_range': (50, 120), 'p_range': (30, 80), 'k_range': (30, 80),
            'score_weight': 1.0
        },
        'wheat': {
            'temp_range': (10, 25), 'humidity_range': (40, 70), 'rainfall_range': (200, 800),
            'ph_range': (6.0, 8.0), 'n_range': (80, 150), 'p_range': (40, 90), 'k_range': (30, 70),
            'score_weight': 1.0
        },
        'maize': {
            'temp_range': (18, 32), 'humidity_range': (50, 80), 'rainfall_range': (400, 1200),
            'ph_range': (5.8, 7.5), 'n_range': (60, 140), 'p_range': (40, 100), 'k_range': (40, 100),
            'score_weight': 1.0
        },
        'cotton': {
            'temp_range': (25, 35), 'humidity_range': (50, 80), 'rainfall_range': (500, 1000),
            'ph_range': (5.8, 8.0), 'n_range': (80, 160), 'p_range': (40, 120), 'k_range': (40, 120),
            'score_weight': 1.0
        },
        'sugarcane': {
            'temp_range': (20, 30), 'humidity_range': (70, 90), 'rainfall_range': (1000, 2500),
            'ph_range': (6.0, 8.0), 'n_range': (100, 200), 'p_range': (50, 150), 'k_range': (60, 150),
            'score_weight': 1.0
        },
        'jute': {
            'temp_range': (24, 35), 'humidity_range': (70, 90), 'rainfall_range': (1000, 2000),
            'ph_range': (6.0, 7.5), 'n_range': (40, 100), 'p_range': (20, 60), 'k_range': (30, 80),
            'score_weight': 1.0
        },
        'coconut': {
            'temp_range': (24, 32), 'humidity_range': (70, 90), 'rainfall_range': (1200, 3000),
            'ph_range': (5.2, 8.0), 'n_range': (30, 80), 'p_range': (20, 60), 'k_range': (40, 120),
            'score_weight': 1.0
        },
        'papaya': {
            'temp_range': (22, 32), 'humidity_range': (60, 85), 'rainfall_range': (600, 1500),
            'ph_range': (6.0, 7.5), 'n_range': (50, 120), 'p_range': (30, 80), 'k_range': (50, 130),
            'score_weight': 1.0
        },
        'banana': {
            'temp_range': (24, 30), 'humidity_range': (75, 90), 'rainfall_range': (1000, 2500),
            'ph_range': (6.0, 7.5), 'n_range': (100, 180), 'p_range': (50, 120), 'k_range': (80, 200),
            'score_weight': 1.0
        },
        'mango': {
            'temp_range': (24, 32), 'humidity_range': (50, 80), 'rainfall_range': (600, 1500),
            'ph_range': (5.5, 7.5), 'n_range': (40, 100), 'p_range': (30, 80), 'k_range': (50, 120),
            'score_weight': 1.0
        }
    }
    
    # Extract input values
    n, p, k = input_data['N'], input_data['P'], input_data['K']
    temp, humidity, rainfall = input_data['temperature'], input_data['humidity'], input_data['rainfall']
    ph = input_data['ph']
    
    def calculate_suitability_score(crop_info):
        """Calculate how suitable the input conditions are for a specific crop"""
        score = 0
        factors = 0
        
        # Temperature score
        if crop_info['temp_range'][0] <= temp <= crop_info['temp_range'][1]:
            score += 100
        else:
            deviation = min(abs(temp - crop_info['temp_range'][0]), abs(temp - crop_info['temp_range'][1]))
            score += max(0, 100 - deviation * 5)
        factors += 1
        
        # Humidity score
        if crop_info['humidity_range'][0] <= humidity <= crop_info['humidity_range'][1]:
            score += 100
        else:
            deviation = min(abs(humidity - crop_info['humidity_range'][0]), abs(humidity - crop_info['humidity_range'][1]))
            score += max(0, 100 - deviation * 2)
        factors += 1
        
        # Rainfall score
        if crop_info['rainfall_range'][0] <= rainfall <= crop_info['rainfall_range'][1]:
            score += 100
        else:
            deviation = min(abs(rainfall - crop_info['rainfall_range'][0]), abs(rainfall - crop_info['rainfall_range'][1]))
            score += max(0, 100 - deviation / 20)
        factors += 1
        
        # pH score
        if crop_info['ph_range'][0] <= ph <= crop_info['ph_range'][1]:
            score += 100
        else:
            deviation = min(abs(ph - crop_info['ph_range'][0]), abs(ph - crop_info['ph_range'][1]))
            score += max(0, 100 - deviation * 20)
        factors += 1
        
        # NPK scores
        for nutrient, value in [('n', n), ('p', p), ('k', k)]:
            nutrient_range = crop_info[f'{nutrient}_range']
            if nutrient_range[0] <= value <= nutrient_range[1]:
                score += 100
            else:
                deviation = min(abs(value - nutrient_range[0]), abs(value - nutrient_range[1]))
                score += max(0, 100 - deviation * 2)
            factors += 1
        
        return score / factors if factors > 0 else 0
    
    # Calculate suitability scores for all crops
    crop_scores = {}
    for crop_name, crop_info in crop_database.items():
        crop_scores[crop_name] = calculate_suitability_score(crop_info)
    
    # Sort crops by suitability score
    sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select the best crop
    best_crop = sorted_crops[0][0]
    best_score = sorted_crops[0][1]
    confidence = min(0.95, max(0.60, best_score / 100))
    
    # Add some randomness to avoid always getting the same result for similar inputs
    if len(sorted_crops) > 1 and abs(sorted_crops[0][1] - sorted_crops[1][1]) < 10:
        # If top 2 crops are very close, add randomness
        if random.random() < 0.3:  # 30% chance to pick second best
            best_crop = sorted_crops[1][0]
            confidence *= 0.9
    
    # Generate realistic yield based on crop and conditions
    base_yields = {
        'rice': 45, 'wheat': 35, 'maize': 55, 'cotton': 25, 'sugarcane': 650,
        'jute': 25, 'coconut': 12, 'papaya': 400, 'banana': 300, 'mango': 150
    }
    
    base_yield = base_yields.get(best_crop, 40)
    # Adjust yield based on suitability score
    yield_factor = 0.6 + (best_score / 100) * 0.8  # 60% to 140% of base yield
    actual_yield = base_yield * yield_factor
    
    # Convert to tonnes per acre (most yields are per hectare)
    if best_crop in ['sugarcane', 'papaya', 'banana', 'mango']:
        yield_per_acre = round(actual_yield * 0.4047 / 100, 2)  # Convert quintal/ha to t/acre
    else:
        yield_per_acre = round(actual_yield * 0.4047 / 10, 2)  # Convert quintal/ha to t/acre
    
    # Economic calculations
    crop_prices = {  # Price per tonne
        'rice': 25000, 'wheat': 23000, 'maize': 20000, 'cotton': 45000, 'sugarcane': 3000,
        'jute': 35000, 'coconut': 80000, 'papaya': 15000, 'banana': 12000, 'mango': 40000
    }
    
    price_per_tonne = crop_prices.get(best_crop, 25000)
    gross_revenue = int(yield_per_acre * price_per_tonne)
    
    # Investment calculation
    base_investment = 25000 + (n + p + k) * 15
    crop_investment_factor = {
        'rice': 1.0, 'wheat': 0.8, 'maize': 0.9, 'cotton': 1.3, 'sugarcane': 2.0,
        'jute': 0.7, 'coconut': 3.0, 'papaya': 1.5, 'banana': 1.8, 'mango': 2.5
    }
    
    investment = int(base_investment * crop_investment_factor.get(best_crop, 1.0))
    net_profit = gross_revenue - investment
    roi = round((net_profit / investment) * 100, 1) if investment > 0 else 0
    
    return {
        'recommended_crop': best_crop,
        'confidence': round(confidence, 3),
        'expected_yield_t_per_acre': yield_per_acre,
        'yield_interval_p10_p90': [round(yield_per_acre * 0.8, 2), round(yield_per_acre * 1.2, 2)],
        'profit_breakdown': {
            'gross': gross_revenue,
            'investment': investment,
            'net': net_profit,
            'roi': roi
        },
        'fertilizer_recommendation': {
            'type': f'NPK {int(n/8)}-{int(p/8)}-{int(k/8)}',
            'dosage_kg_per_ha': 80 + int((n + p + k) / 4),
            'cost': 1800 + int((n + p + k) * 12)
        },
        'why': [
            f"Best match: {best_crop} (suitability: {best_score:.0f}%)",
            f"Climate conditions optimal for {best_crop} cultivation",
            f"NPK levels {n}-{p}-{k} suitable for {best_crop} requirements",
            f"Expected yield: {yield_per_acre}t/acre under current conditions"
        ],
        'model_version': 'enhanced_fallback_v2.0',
        'timestamp': datetime.now().isoformat(),
        'area_analyzed_ha': input_data.get('area_ha', 1.0),
        'suitability_scores': dict(sorted_crops[:3])  # Top 3 crops with scores
    }
    
    gross_revenue = int(yield_per_acre * 40000)  # ₹40k per tonne
    investment = int(30000 + (n + p + k) * 10)
    net_profit = gross_revenue - investment
    roi = round((net_profit / investment) * 100, 1)
    
    return {
        'recommended_crop': crop,
        'confidence': round(0.7 + random.random() * 0.2, 3),
        'expected_yield_t_per_acre': yield_per_acre,
        'yield_interval_p10_p90': [yield_per_acre * 0.8, yield_per_acre * 1.2],
        'profit_breakdown': {
            'gross': gross_revenue,
            'investment': investment,
            'net': net_profit,
            'roi': roi
        },
        'fertilizer_recommendation': {
            'type': 'NPK 15-15-15',
            'dosage_kg_per_ha': 120 + int((n + p + k) / 5),
            'cost': 2500 + int((n + p + k) * 5)
        },
        'why': [
            f"Soil NPK levels: {n}-{p}-{k} suitable for {crop}",
            f"Climate conditions favor {crop} cultivation",
            f"Expected yield: {yield_per_acre}t/acre with proper management",
            "Recommendation based on agricultural best practices"
        ],
        'model_version': 'demo_v1',
        'timestamp': datetime.now().isoformat(),
        'area_analyzed_ha': input_data.get('area_ha', 1.0)
    }

# Sidebar inputs
st.sidebar.header("🔧 Input Parameters")

# Basic parameters
st.sidebar.subheader("Soil Nutrients")
col1, col2 = st.sidebar.columns(2)
with col1:
    nitrogen = st.number_input("Nitrogen (N)", 0.0, 200.0, 60.0)
    phosphorus = st.number_input("Phosphorus (P)", 0.0, 150.0, 45.0)
with col2:
    potassium = st.number_input("Potassium (K)", 0.0, 200.0, 50.0)
    ph = st.number_input("pH Level", 3.5, 9.0, 6.5)

st.sidebar.subheader("Climate")
col3, col4 = st.sidebar.columns(2)
with col3:
    temperature = st.number_input("Temperature (°C)", -10.0, 55.0, 25.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 70.0)
with col4:
    rainfall = st.number_input("Rainfall (mm)", 0.0, 5000.0, 800.0)
    area_ha = st.number_input("Area (ha)", 0.1, 1000.0, 2.0)

# Preset scenarios
st.sidebar.subheader("📋 Quick Tests")
presets = {
    "Rice Farm": {"N": 80, "P": 40, "K": 40, "temperature": 27, "humidity": 80, "ph": 6.0, "rainfall": 1200, "area_ha": 3.0},
    "Wheat Farm": {"N": 120, "P": 60, "K": 40, "temperature": 20, "humidity": 65, "ph": 7.5, "rainfall": 300, "area_ha": 5.0},
    "Cotton Farm": {"N": 90, "P": 50, "K": 50, "temperature": 30, "humidity": 70, "ph": 7.0, "rainfall": 600, "area_ha": 10.0},
    "High Nutrient": {"N": 150, "P": 100, "K": 120, "temperature": 25, "humidity": 75, "ph": 6.8, "rainfall": 600, "area_ha": 2.0},
    "Low Nutrient": {"N": 20, "P": 15, "K": 25, "temperature": 22, "humidity": 65, "ph": 6.2, "rainfall": 400, "area_ha": 1.5}
}

selected_preset = st.sidebar.selectbox("Load Preset", [""] + list(presets.keys()))

# Main content
if selected_preset:
    st.info(f"Loaded preset: {selected_preset}")

# Display current inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("NPK", f"{nitrogen:.0f}-{phosphorus:.0f}-{potassium:.0f}")
with col2:
    st.metric("Temperature", f"{temperature}°C")
with col3:
    st.metric("Humidity", f"{humidity}%")
with col4:
    st.metric("Rainfall", f"{rainfall}mm")

# Prediction button
if st.button("🔮 Generate Prediction", type="primary", width="stretch"):
    # Prepare input data
    input_data = {
        "N": nitrogen, "P": phosphorus, "K": potassium,
        "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rainfall,
        "area_ha": area_ha
    }
    
    # Apply preset if selected
    if selected_preset and selected_preset in presets:
        input_data.update(presets[selected_preset])
    
    with st.spinner("🤖 AI is analyzing your farm conditions..."):
        try:
            # Use real model if available, otherwise fallback
            if models_available:
                result = predict_func(input_data)
                st.success("✅ Real AI Model Prediction Generated!")
            else:
                result = fallback_prediction(input_data)
                st.warning("⚠️ Using Demo Mode (Install models for real predictions)")
            
            # Display results
            if 'error' not in result:
                # Main metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🌾 Recommended Crop", result['recommended_crop'].title())
                with col2:
                    st.metric("📈 Yield", f"{result['expected_yield_t_per_acre']:.1f} t/acre")
                with col3:
                    st.metric("💰 Net Profit", f"₹{result['profit_breakdown']['net']:,}")
                with col4:
                    st.metric("📊 ROI", f"{result['profit_breakdown']['roi']:.1f}%")
                
                # Detailed tabs
                tab1, tab2, tab3 = st.tabs(["📊 Economics", "🌱 Fertilizer", "🔍 Analysis"])
                
                with tab1:
                    # Profit chart
                    profit_data = result['profit_breakdown']
                    fig = go.Figure(data=[
                        go.Bar(name='Revenue', x=['Analysis'], y=[profit_data['gross']], marker_color='green'),
                        go.Bar(name='Investment', x=['Analysis'], y=[profit_data['investment']], marker_color='red'),
                        go.Bar(name='Net Profit', x=['Analysis'], y=[profit_data['net']], marker_color='blue')
                    ])
                    fig.update_layout(title="Financial Analysis (₹)", barmode='group', height=400)
                    st.plotly_chart(fig, width="stretch")
                    
                    # ROI gauge
                    roi_fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = profit_data['roi'],
                        title = {'text': "ROI (%)"},
                        gauge = {
                            'axis': {'range': [None, 200]},
                            'bar': {'color': "darkgreen"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 100], 'color': "yellow"},
                                {'range': [100, 200], 'color': "green"}
                            ]
                        }
                    ))
                    st.plotly_chart(roi_fig, width="stretch")
                
                with tab2:
                    fert = result.get('fertilizer_recommendation', {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Type", fert.get('type', 'N/A'))
                    with col2:
                        st.metric("Dosage", f"{fert.get('dosage_kg_per_ha', 0)} kg/ha")
                    with col3:
                        st.metric("Cost", f"₹{fert.get('cost', 0):,}")
                    
                    # NPK chart
                    npk_df = pd.DataFrame({
                        'Nutrient': ['Nitrogen', 'Phosphorus', 'Potassium'],
                        'Current Levels': [nitrogen, phosphorus, potassium]
                    })
                    fig = px.bar(npk_df, x='Nutrient', y='Current Levels', 
                               title="Current Soil NPK Levels")
                    st.plotly_chart(fig, width="stretch")
                
                with tab3:
                    st.subheader("🔍 AI Analysis")
                    for i, reason in enumerate(result.get('why', []), 1):
                        st.write(f"**{i}.** {reason}")
                    
                    # Input summary
                    st.subheader("📋 Input Summary")
                    input_df = pd.DataFrame([{
                        'Parameter': k.replace('_', ' ').title(),
                        'Value': f"{v} {'°C' if 'temp' in k else '%' if 'humidity' in k else 'mm' if 'rain' in k else 'ha' if 'area' in k else ''}"
                    } for k, v in input_data.items()])
                    st.dataframe(input_df, width="stretch")
                    
                    # Confidence and metadata
                    st.write(f"**Confidence:** {result.get('confidence', 0):.1%}")
                    st.write(f"**Model Version:** {result.get('model_version', 'N/A')}")
                    st.write(f"**Analysis Time:** {result.get('timestamp', 'N/A')}")
            
            else:
                st.error(f"❌ Error: {result['error']}")
                
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            with st.expander("Error Details"):
                st.code(traceback.format_exc())

# Model status
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Model Status")
if models_available:
    st.sidebar.success("✅ AI Models Loaded")
    st.sidebar.write("Using trained ML models")
else:
    st.sidebar.warning("⚠️ Demo Mode")
    st.sidebar.write("Install models for real predictions")

# Tips section
with st.expander("💡 Testing Tips"):
    st.write("""
    **Quick Testing Guide:**
    1. 🔄 Try the preset scenarios first
    2. 🌾 Test extreme values (very high/low NPK)
    3. 🌡️ Experiment with different climates
    4. 📊 Compare ROI across different inputs
    5. 🔍 Check explanations for AI reasoning
    
    **Expected Ranges:**
    - N: 20-150 kg/ha (normal farming)
    - P: 15-100 kg/ha 
    - K: 20-120 kg/ha
    - Temperature: 15-35°C (most crops)
    - Humidity: 40-90%
    - Rainfall: 200-2000mm (annual)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    🌾 Crop AI Testing Interface | Built for agricultural innovation<br>
    Test different scenarios to validate your AI model performance
</div>
""", unsafe_allow_html=True)
