"""
AI Crop Recommendation System - Tkinter Desktop GUI
Created for testing the enhanced AI model with previous crop and season analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import json
import pandas as pd
from datetime import datetime, date
import traceback
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import prediction functions
try:
    from src.predict import predict_from_dict, load_all_models
    MODELS_LOADED = True
except ImportError:
    MODELS_LOADED = False

class CropAIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌾 Crop AI Testing Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.prediction_history = []
        self.setup_variables()
        self.create_widgets()
        
        # Load models status
        if not MODELS_LOADED:
            messagebox.showerror("Error", "Could not import prediction modules. Please check your installation.")
    
    def setup_variables(self):
        """Initialize all tkinter variables"""
        # Soil nutrients
        self.nitrogen = tk.DoubleVar(value=60.0)
        self.phosphorus = tk.DoubleVar(value=45.0)
        self.potassium = tk.DoubleVar(value=50.0)
        self.ph = tk.DoubleVar(value=6.5)
        
        # Climate conditions
        self.temperature = tk.DoubleVar(value=25.0)
        self.humidity = tk.DoubleVar(value=70.0)
        self.rainfall = tk.DoubleVar(value=800.0)
        self.area_ha = tk.DoubleVar(value=2.0)
        
        # Enhanced features
        self.region = tk.StringVar(value="default")
        self.previous_crop = tk.StringVar(value="")
        self.season = tk.StringVar(value="auto-detect")
        self.planting_date = tk.StringVar(value=date.today().isoformat())
        
        # Options
        self.include_explanations = tk.BooleanVar(value=True)
        self.show_confidence = tk.BooleanVar(value=True)
        self.enable_comparison = tk.BooleanVar(value=False)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main frame with scrollbar
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        self.create_header(scrollable_frame)
        
        # Main content area
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel for inputs
        left_frame = ttk.LabelFrame(content_frame, text="Input Parameters", padding=10)
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        
        self.create_input_section(left_frame)
        
        # Right panel for results
        right_frame = ttk.LabelFrame(content_frame, text="Results", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.create_results_section(right_frame)
        
        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg='#2E8B57', height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🌾 Crop AI Testing Dashboard",
            font=("Arial", 24, "bold"),
            fg="white",
            bg='#2E8B57'
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Interactive testing interface for Enhanced Crop Recommendation System",
            font=("Arial", 12),
            fg="white",
            bg='#2E8B57'
        )
        subtitle_label.pack()
    
    def create_input_section(self, parent):
        """Create the input parameters section"""
        # Soil Nutrients Section
        nutrients_frame = ttk.LabelFrame(parent, text="Soil Nutrients (kg/ha)", padding=5)
        nutrients_frame.pack(fill="x", pady=5)
        
        # Nitrogen
        ttk.Label(nutrients_frame, text="Nitrogen (N):").grid(row=0, column=0, sticky="w", padx=5)
        nitrogen_scale = ttk.Scale(nutrients_frame, from_=0, to=200, variable=self.nitrogen, orient="horizontal")
        nitrogen_scale.grid(row=0, column=1, sticky="ew", padx=5)
        nitrogen_value = ttk.Label(nutrients_frame, text="60.0")
        nitrogen_value.grid(row=0, column=2, padx=5)
        self.nitrogen.trace_add("write", lambda *args: nitrogen_value.config(text=f"{self.nitrogen.get():.1f}"))
        
        # Phosphorus
        ttk.Label(nutrients_frame, text="Phosphorus (P):").grid(row=1, column=0, sticky="w", padx=5)
        phosphorus_scale = ttk.Scale(nutrients_frame, from_=0, to=150, variable=self.phosphorus, orient="horizontal")
        phosphorus_scale.grid(row=1, column=1, sticky="ew", padx=5)
        phosphorus_value = ttk.Label(nutrients_frame, text="45.0")
        phosphorus_value.grid(row=1, column=2, padx=5)
        self.phosphorus.trace_add("write", lambda *args: phosphorus_value.config(text=f"{self.phosphorus.get():.1f}"))
        
        # Potassium
        ttk.Label(nutrients_frame, text="Potassium (K):").grid(row=2, column=0, sticky="w", padx=5)
        potassium_scale = ttk.Scale(nutrients_frame, from_=0, to=200, variable=self.potassium, orient="horizontal")
        potassium_scale.grid(row=2, column=1, sticky="ew", padx=5)
        potassium_value = ttk.Label(nutrients_frame, text="50.0")
        potassium_value.grid(row=2, column=2, padx=5)
        self.potassium.trace_add("write", lambda *args: potassium_value.config(text=f"{self.potassium.get():.1f}"))
        
        # pH
        ttk.Label(nutrients_frame, text="pH Level:").grid(row=3, column=0, sticky="w", padx=5)
        ph_scale = ttk.Scale(nutrients_frame, from_=3.5, to=9.0, variable=self.ph, orient="horizontal")
        ph_scale.grid(row=3, column=1, sticky="ew", padx=5)
        ph_value = ttk.Label(nutrients_frame, text="6.5")
        ph_value.grid(row=3, column=2, padx=5)
        self.ph.trace_add("write", lambda *args: ph_value.config(text=f"{self.ph.get():.1f}"))
        
        nutrients_frame.columnconfigure(1, weight=1)
        
        # Climate Conditions Section
        climate_frame = ttk.LabelFrame(parent, text="Climate Conditions", padding=5)
        climate_frame.pack(fill="x", pady=5)
        
        # Temperature
        ttk.Label(climate_frame, text="Temperature (°C):").grid(row=0, column=0, sticky="w", padx=5)
        temp_scale = ttk.Scale(climate_frame, from_=-10, to=55, variable=self.temperature, orient="horizontal")
        temp_scale.grid(row=0, column=1, sticky="ew", padx=5)
        temp_value = ttk.Label(climate_frame, text="25.0")
        temp_value.grid(row=0, column=2, padx=5)
        self.temperature.trace_add("write", lambda *args: temp_value.config(text=f"{self.temperature.get():.1f}"))
        
        # Humidity
        ttk.Label(climate_frame, text="Humidity (%):").grid(row=1, column=0, sticky="w", padx=5)
        humidity_scale = ttk.Scale(climate_frame, from_=0, to=100, variable=self.humidity, orient="horizontal")
        humidity_scale.grid(row=1, column=1, sticky="ew", padx=5)
        humidity_value = ttk.Label(climate_frame, text="70.0")
        humidity_value.grid(row=1, column=2, padx=5)
        self.humidity.trace_add("write", lambda *args: humidity_value.config(text=f"{self.humidity.get():.1f}"))
        
        # Rainfall
        ttk.Label(climate_frame, text="Rainfall (mm):").grid(row=2, column=0, sticky="w", padx=5)
        rainfall_scale = ttk.Scale(climate_frame, from_=0, to=5000, variable=self.rainfall, orient="horizontal")
        rainfall_scale.grid(row=2, column=1, sticky="ew", padx=5)
        rainfall_value = ttk.Label(climate_frame, text="800.0")
        rainfall_value.grid(row=2, column=2, padx=5)
        self.rainfall.trace_add("write", lambda *args: rainfall_value.config(text=f"{self.rainfall.get():.1f}"))
        
        # Area
        ttk.Label(climate_frame, text="Area (hectares):").grid(row=3, column=0, sticky="w", padx=5)
        area_scale = ttk.Scale(climate_frame, from_=0.1, to=1000, variable=self.area_ha, orient="horizontal")
        area_scale.grid(row=3, column=1, sticky="ew", padx=5)
        area_value = ttk.Label(climate_frame, text="2.0")
        area_value.grid(row=3, column=2, padx=5)
        self.area_ha.trace_add("write", lambda *args: area_value.config(text=f"{self.area_ha.get():.1f}"))
        
        climate_frame.columnconfigure(1, weight=1)
        
        # Enhanced Features Section
        enhanced_frame = ttk.LabelFrame(parent, text="Enhanced Features", padding=5)
        enhanced_frame.pack(fill="x", pady=5)
        
        # Region
        ttk.Label(enhanced_frame, text="Region:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        region_combo = ttk.Combobox(enhanced_frame, textvariable=self.region, 
                                   values=["default", "north", "south", "east", "west", "central"])
        region_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        # Previous Crop
        ttk.Label(enhanced_frame, text="Previous Crop:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        previous_crops = [
            "", "rice", "wheat", "maize", "sugarcane", "cotton", "jute", "coconut", "papaya", "orange",
            "apple", "muskmelon", "watermelon", "grapes", "mango", "banana", "pomegranate", "lentil",
            "blackgram", "mungbean", "mothbeans", "pigeonpeas", "kidneybeans", "chickpea", "coffee"
        ]
        crop_combo = ttk.Combobox(enhanced_frame, textvariable=self.previous_crop, values=previous_crops)
        crop_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        
        # Season
        ttk.Label(enhanced_frame, text="Season:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        season_combo = ttk.Combobox(enhanced_frame, textvariable=self.season, 
                                   values=["auto-detect", "kharif", "rabi", "zaid"])
        season_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        
        # Planting Date
        ttk.Label(enhanced_frame, text="Planting Date:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        date_entry = ttk.Entry(enhanced_frame, textvariable=self.planting_date)
        date_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        
        enhanced_frame.columnconfigure(1, weight=1)
        
        # Options Section
        options_frame = ttk.LabelFrame(parent, text="Options", padding=5)
        options_frame.pack(fill="x", pady=5)
        
        ttk.Checkbutton(options_frame, text="Include AI Explanations", 
                       variable=self.include_explanations).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Show Confidence Scores", 
                       variable=self.show_confidence).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Enable Batch Comparison", 
                       variable=self.enable_comparison).pack(anchor="w")
        
        # Preset Examples Section
        presets_frame = ttk.LabelFrame(parent, text="Preset Examples", padding=5)
        presets_frame.pack(fill="x", pady=5)
        
        self.example_scenarios = {
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
        
        self.selected_example = tk.StringVar(value="")
        example_combo = ttk.Combobox(presets_frame, textvariable=self.selected_example, 
                                    values=[""] + list(self.example_scenarios.keys()))
        example_combo.pack(fill="x", pady=2)
        
        ttk.Button(presets_frame, text="Load Example", 
                  command=self.load_example).pack(fill="x", pady=2)
        
        # Prediction Button
        predict_frame = ttk.Frame(parent)
        predict_frame.pack(fill="x", pady=10)
        
        self.predict_button = ttk.Button(predict_frame, text="🔮 Generate Prediction", 
                                        command=self.generate_prediction, style="Accent.TButton")
        self.predict_button.pack(fill="x")
        
        # Progress bar
        self.progress = ttk.Progressbar(predict_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=5)
    
    def create_results_section(self, parent):
        """Create the results display section"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)
        
        # Summary Tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="📋 Summary")
        
        # Enhanced Analysis Tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="🧪 Enhanced Analysis")
        
        # Economics Tab
        self.economics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.economics_frame, text="💰 Economics")
        
        # Fertilizer Tab
        self.fertilizer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fertilizer_frame, text="🌱 Fertilizer")
        
        # Explanations Tab
        self.explanations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.explanations_frame, text="🔍 Explanations")
        
        # Initialize result displays
        self.create_summary_tab()
        self.create_analysis_tab()
        self.create_economics_tab()
        self.create_fertilizer_tab()
        self.create_explanations_tab()
    
    def create_summary_tab(self):
        """Create the summary tab content"""
        # Main metrics frame
        metrics_frame = ttk.LabelFrame(self.summary_frame, text="Key Metrics", padding=10)
        metrics_frame.pack(fill="x", pady=5)
        
        # Create metric labels
        self.crop_label = ttk.Label(metrics_frame, text="Recommended Crop: -", font=("Arial", 12, "bold"))
        self.crop_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        
        self.yield_label = ttk.Label(metrics_frame, text="Expected Yield: -")
        self.yield_label.grid(row=1, column=0, sticky="w", pady=2)
        
        self.profit_label = ttk.Label(metrics_frame, text="Net Profit: -")
        self.profit_label.grid(row=1, column=1, sticky="w", pady=2)
        
        self.confidence_label = ttk.Label(metrics_frame, text="Confidence: -")
        self.confidence_label.grid(row=2, column=0, sticky="w", pady=2)
        
        self.roi_label = ttk.Label(metrics_frame, text="ROI: -")
        self.roi_label.grid(row=2, column=1, sticky="w", pady=2)
        
        # Detailed results frame
        details_frame = ttk.LabelFrame(self.summary_frame, text="Detailed Results", padding=10)
        details_frame.pack(fill="both", expand=True, pady=5)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(details_frame, height=15, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True)
    
    def create_analysis_tab(self):
        """Create the enhanced analysis tab content"""
        # Previous crop analysis
        prev_crop_frame = ttk.LabelFrame(self.analysis_frame, text="Previous Crop Analysis", padding=10)
        prev_crop_frame.pack(fill="x", pady=5)
        
        self.prev_crop_text = tk.Text(prev_crop_frame, height=6, wrap=tk.WORD)
        self.prev_crop_text.pack(fill="x")
        
        # Season analysis
        season_frame = ttk.LabelFrame(self.analysis_frame, text="Season Analysis", padding=10)
        season_frame.pack(fill="x", pady=5)
        
        self.season_text = tk.Text(season_frame, height=6, wrap=tk.WORD)
        self.season_text.pack(fill="x")
    
    def create_economics_tab(self):
        """Create the economics tab content"""
        # Economic metrics
        econ_metrics_frame = ttk.LabelFrame(self.economics_frame, text="Financial Breakdown", padding=10)
        econ_metrics_frame.pack(fill="x", pady=5)
        
        self.revenue_label = ttk.Label(econ_metrics_frame, text="Gross Revenue: -")
        self.revenue_label.pack(anchor="w")
        
        self.investment_label = ttk.Label(econ_metrics_frame, text="Total Investment: -")
        self.investment_label.pack(anchor="w")
        
        self.net_profit_label = ttk.Label(econ_metrics_frame, text="Net Profit: -")
        self.net_profit_label.pack(anchor="w")
        
        self.roi_detail_label = ttk.Label(econ_metrics_frame, text="ROI: -")
        self.roi_detail_label.pack(anchor="w")
        
        # Chart frame for matplotlib
        chart_frame = ttk.LabelFrame(self.economics_frame, text="Financial Visualization", padding=10)
        chart_frame.pack(fill="both", expand=True, pady=5)
        
        # Placeholder for matplotlib chart
        self.economics_chart_frame = chart_frame
    
    def create_fertilizer_tab(self):
        """Create the fertilizer tab content"""
        # Fertilizer recommendation
        fert_frame = ttk.LabelFrame(self.fertilizer_frame, text="Fertilizer Recommendation", padding=10)
        fert_frame.pack(fill="x", pady=5)
        
        self.fert_type_label = ttk.Label(fert_frame, text="Fertilizer Type: -")
        self.fert_type_label.pack(anchor="w")
        
        self.fert_dosage_label = ttk.Label(fert_frame, text="Dosage: -")
        self.fert_dosage_label.pack(anchor="w")
        
        self.fert_cost_label = ttk.Label(fert_frame, text="Cost: -")
        self.fert_cost_label.pack(anchor="w")
        
        # NPK comparison frame
        npk_frame = ttk.LabelFrame(self.fertilizer_frame, text="NPK Analysis", padding=10)
        npk_frame.pack(fill="both", expand=True, pady=5)
        
        self.npk_chart_frame = npk_frame
    
    def create_explanations_tab(self):
        """Create the explanations tab content"""
        # AI explanations
        explain_frame = ttk.LabelFrame(self.explanations_frame, text="AI Explanations", padding=10)
        explain_frame.pack(fill="both", expand=True, pady=5)
        
        self.explanations_text = scrolledtext.ScrolledText(explain_frame, height=20, wrap=tk.WORD)
        self.explanations_text.pack(fill="both", expand=True)
    
    def load_example(self):
        """Load selected example data"""
        example_name = self.selected_example.get()
        if example_name and example_name in self.example_scenarios:
            example_data = self.example_scenarios[example_name]
            
            # Update variables with example data
            self.nitrogen.set(example_data.get("N", 60))
            self.phosphorus.set(example_data.get("P", 45))
            self.potassium.set(example_data.get("K", 50))
            self.temperature.set(example_data.get("temperature", 25))
            self.humidity.set(example_data.get("humidity", 70))
            self.ph.set(example_data.get("ph", 6.5))
            self.rainfall.set(example_data.get("rainfall", 800))
            self.area_ha.set(example_data.get("area_ha", 2.0))
            self.season.set(example_data.get("season", "auto-detect"))
            
            messagebox.showinfo("Example Loaded", f"Loaded example: {example_name}")
    
    def generate_prediction(self):
        """Generate prediction in a separate thread"""
        if not MODELS_LOADED:
            messagebox.showerror("Error", "AI Models not loaded. Please check installation.")
            return
        
        # Disable button and start progress
        self.predict_button.config(state="disabled")
        self.progress.start()
        
        # Run prediction in separate thread
        thread = Thread(target=self.run_prediction)
        thread.daemon = True
        thread.start()
    
    def run_prediction(self):
        """Run the actual prediction"""
        try:
            # Prepare input data
            input_data = {
                "N": self.nitrogen.get(),
                "P": self.phosphorus.get(),
                "K": self.potassium.get(),
                "temperature": self.temperature.get(),
                "humidity": self.humidity.get(),
                "ph": self.ph.get(),
                "rainfall": self.rainfall.get(),
                "area_ha": self.area_ha.get(),
                "region": self.region.get(),
                "previous_crop": self.previous_crop.get() if self.previous_crop.get() else "",
                "season": self.season.get() if self.season.get() != "auto-detect" else "",
                "planting_date": self.planting_date.get() if self.season.get() == "auto-detect" else ""
            }
            
            # Make prediction
            result = predict_from_dict(input_data)
            
            # Store in history
            result['input_data'] = input_data.copy()
            result['timestamp'] = datetime.now().isoformat()
            self.prediction_history.append(result)
            
            # Update GUI in main thread
            self.root.after(0, self.update_results, result)
            
        except Exception as e:
            error_msg = f"Error during prediction: {str(e)}\n\n{traceback.format_exc()}"
            self.root.after(0, self.show_error, error_msg)
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.stop_progress)
    
    def update_results(self, result):
        """Update the GUI with prediction results"""
        if 'error' in result:
            self.show_error(f"Prediction Error: {result['error']}")
            return
        
        # Update summary tab
        self.crop_label.config(text=f"Recommended Crop: {result['recommended_crop'].title()}")
        self.yield_label.config(text=f"Expected Yield: {result['expected_yield_t_per_acre']:.1f} t/acre")
        self.profit_label.config(text=f"Net Profit: ₹{result['profit_breakdown']['net']:,}")
        
        if self.show_confidence.get():
            self.confidence_label.config(text=f"Confidence: {result['confidence']:.1%}")
        else:
            self.confidence_label.config(text="")
        
        self.roi_label.config(text=f"ROI: {result['profit_breakdown']['roi']:.1f}%")
        
        # Update detailed results
        self.results_text.delete(1.0, tk.END)
        
        # Add yield information
        self.results_text.insert(tk.END, "YIELD PREDICTION\n")
        self.results_text.insert(tk.END, "="*50 + "\n")
        self.results_text.insert(tk.END, f"Expected Yield: {result['expected_yield_t_per_acre']:.1f} t/acre\n")
        self.results_text.insert(tk.END, f"Lower Bound (P10): {result['yield_interval_p10_p90'][0]:.1f} t/acre\n")
        self.results_text.insert(tk.END, f"Upper Bound (P90): {result['yield_interval_p10_p90'][1]:.1f} t/acre\n\n")
        
        # Add economic summary
        profit_data = result['profit_breakdown']
        self.results_text.insert(tk.END, "ECONOMIC SUMMARY\n")
        self.results_text.insert(tk.END, "="*50 + "\n")
        self.results_text.insert(tk.END, f"Gross Revenue: ₹{profit_data['gross']:,}\n")
        self.results_text.insert(tk.END, f"Total Investment: ₹{profit_data['investment']:,}\n")
        self.results_text.insert(tk.END, f"Net Profit: ₹{profit_data['net']:,}\n")
        self.results_text.insert(tk.END, f"ROI: {profit_data['roi']:.1f}%\n\n")
        
        # Update analysis tab
        self.update_analysis_tab(result)
        
        # Update economics tab
        self.update_economics_tab(result)
        
        # Update fertilizer tab
        self.update_fertilizer_tab(result)
        
        # Update explanations tab
        self.update_explanations_tab(result)
        
        messagebox.showinfo("Success", "Prediction generated successfully!")
    
    def update_analysis_tab(self, result):
        """Update the enhanced analysis tab"""
        # Previous crop analysis
        self.prev_crop_text.delete(1.0, tk.END)
        if result.get('previous_crop_analysis', {}).get('previous_crop'):
            pca = result['previous_crop_analysis']
            self.prev_crop_text.insert(tk.END, f"Previous Crop: {pca['previous_crop'].title()}\n")
            self.prev_crop_text.insert(tk.END, f"Original NPK: {pca['original_npk']}\n")
            self.prev_crop_text.insert(tk.END, f"Adjusted NPK: {pca['adjusted_npk']}\n")
            self.prev_crop_text.insert(tk.END, f"Nutrient Impact: {pca['nutrient_impact']}\n")
        else:
            self.prev_crop_text.insert(tk.END, "No previous crop analysis available.\n")
        
        # Season analysis
        self.season_text.delete(1.0, tk.END)
        sa = result.get('season_analysis', {})
        self.season_text.insert(tk.END, f"Detected Season: {sa.get('detected_season', 'N/A').title()}\n")
        self.season_text.insert(tk.END, f"Season Suitability: {sa.get('season_suitability', 'N/A').title()}\n")
        if sa.get('season_explanation'):
            self.season_text.insert(tk.END, f"Explanation: {sa['season_explanation']}\n")
    
    def update_economics_tab(self, result):
        """Update the economics tab with charts"""
        profit_data = result['profit_breakdown']
        
        # Update labels
        self.revenue_label.config(text=f"Gross Revenue: ₹{profit_data['gross']:,}")
        self.investment_label.config(text=f"Total Investment: ₹{profit_data['investment']:,}")
        self.net_profit_label.config(text=f"Net Profit: ₹{profit_data['net']:,}")
        self.roi_detail_label.config(text=f"ROI: {profit_data['roi']:.1f}%")
        
        # Create financial chart
        try:
            # Clear previous charts
            for widget in self.economics_chart_frame.winfo_children():
                widget.destroy()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Bar chart for financial breakdown
            categories = ['Revenue', 'Investment', 'Net Profit']
            values = [profit_data['gross'], profit_data['investment'], profit_data['net']]
            colors = ['green', 'red', 'blue']
            
            ax1.bar(categories, values, color=colors, alpha=0.7)
            ax1.set_title('Financial Breakdown (₹)')
            ax1.set_ylabel('Amount (₹)')
            
            # Format y-axis labels
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
            
            # ROI gauge (pie chart simulation)
            roi_value = profit_data['roi']
            remaining = max(0, 200 - roi_value)  # Max ROI display of 200%
            
            if roi_value > 0:
                ax2.pie([roi_value, remaining], labels=['ROI', ''], colors=['green', 'lightgray'], 
                       startangle=90, counterclock=False)
                ax2.set_title(f'ROI: {roi_value:.1f}%')
            else:
                ax2.pie([100], labels=['Loss'], colors=['red'])
                ax2.set_title(f'Loss: {abs(roi_value):.1f}%')
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.economics_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            error_label = ttk.Label(self.economics_chart_frame, text=f"Chart error: {str(e)}")
            error_label.pack()
    
    def update_fertilizer_tab(self, result):
        """Update the fertilizer tab"""
        fert = result.get('fertilizer_recommendation', {})
        
        self.fert_type_label.config(text=f"Fertilizer Type: {fert.get('type', 'N/A')}")
        self.fert_dosage_label.config(text=f"Dosage: {fert.get('dosage_kg_per_ha', 0)} kg/ha")
        self.fert_cost_label.config(text=f"Cost: ₹{fert.get('cost', 0):,}")
        
        # NPK comparison chart
        if result.get('previous_crop_analysis'):
            try:
                # Clear previous charts
                for widget in self.npk_chart_frame.winfo_children():
                    widget.destroy()
                
                pca = result['previous_crop_analysis']
                
                fig, ax = plt.subplots(figsize=(8, 4))
                
                nutrients = ['Nitrogen', 'Phosphorus', 'Potassium']
                original = pca['original_npk']
                adjusted = pca['adjusted_npk']
                
                x = np.arange(len(nutrients))
                width = 0.35
                
                ax.bar(x - width/2, original, width, label='Original', alpha=0.7)
                ax.bar(x + width/2, adjusted, width, label='AI-Adjusted', alpha=0.7)
                
                ax.set_xlabel('Nutrients')
                ax.set_ylabel('Amount (kg/ha)')
                ax.set_title('NPK Values: Original vs AI-Adjusted')
                ax.set_xticks(x)
                ax.set_xticklabels(nutrients)
                ax.legend()
                
                plt.tight_layout()
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, self.npk_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
            except Exception as e:
                error_label = ttk.Label(self.npk_chart_frame, text=f"NPK Chart error: {str(e)}")
                error_label.pack()
    
    def update_explanations_tab(self, result):
        """Update the explanations tab"""
        self.explanations_text.delete(1.0, tk.END)
        
        if self.include_explanations.get() and 'why' in result:
            self.explanations_text.insert(tk.END, "AI EXPLANATIONS\n")
            self.explanations_text.insert(tk.END, "="*50 + "\n\n")
            
            for i, explanation in enumerate(result['why'], 1):
                self.explanations_text.insert(tk.END, f"{i}. {explanation}\n\n")
        
        # Technical details
        self.explanations_text.insert(tk.END, "TECHNICAL DETAILS\n")
        self.explanations_text.insert(tk.END, "="*50 + "\n")
        self.explanations_text.insert(tk.END, f"Model Version: {result.get('model_version', 'N/A')}\n")
        self.explanations_text.insert(tk.END, f"Region: {result.get('region', 'N/A')}\n")
        self.explanations_text.insert(tk.END, f"Analysis Time: {result.get('timestamp', 'N/A')}\n\n")
        
        # Raw result JSON
        self.explanations_text.insert(tk.END, "RAW RESULT DATA\n")
        self.explanations_text.insert(tk.END, "="*50 + "\n")
        self.explanations_text.insert(tk.END, json.dumps(result, indent=2, default=str))
    
    def show_error(self, error_msg):
        """Show error message"""
        messagebox.showerror("Error", error_msg)
    
    def stop_progress(self):
        """Stop progress bar and re-enable button"""
        self.progress.stop()
        self.predict_button.config(state="normal")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Configure ttk styles
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure("Accent.TButton", foreground="white", background="#007bff")
    style.map("Accent.TButton", background=[("active", "#0056b3")])
    
    app = CropAIGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()

