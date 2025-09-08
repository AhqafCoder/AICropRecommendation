"""
Crop Disease Detection GUI Application
User-friendly Tkinter interface for testing the AI model with image uploads
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import sys
import os
import json
import threading
from pathlib import Path

# Add src to path for imports
sys.path.append('src')

class CropDiseaseGUI:
    """Main GUI application for crop disease detection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Crop Disease Detection AI")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f8ff')
        
        # Initialize variables
        self.model = None
        self.class_names = []
        self.device = None
        self.current_image = None
        self.current_image_path = None
        self.disease_info = {}
        
        # Load model and components
        self.load_model_async()
        self.load_disease_info()
        
        # Create GUI
        self.create_widgets()
        
    def load_model_async(self):
        """Load model in background thread"""
        def load_model():
            try:
                from src.model import CropDiseaseResNet50
                
                # Class names
                self.class_names = [
                    'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
                    'Corn___Common_rust',
                    'Corn___healthy',
                    'Corn___Northern_Leaf_Blight',
                    'Potato___Early_Blight',
                    'Potato___healthy',
                    'Potato___Late_Blight',
                    'Tomato___Bacterial_spot',
                    'Tomato___Early_blight',
                    'Tomato___healthy',
                    'Tomato___Late_blight',
                    'Tomato___Leaf_Mold',
                    'Tomato___Septoria_leaf_spot',
                    'Tomato___Spider_mites_Two_spotted_spider_mite',
                    'Tomato___Target_Spot',
                    'Tomato___Tomato_mosaic_virus',
                    'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
                ]
                
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                
                # Try to load trained model
                model_paths = [
                    'models/crop_disease_v2_model.pth',
                    'models/crop_disease_resnet50.pth'
                ]
                
                model_loaded = False
                for model_path in model_paths:
                    if os.path.exists(model_path):
                        try:
                            self.model = CropDiseaseResNet50(num_classes=len(self.class_names), pretrained=False)
                            checkpoint = torch.load(model_path, map_location=self.device)
                            
                            # Handle different checkpoint formats
                            if isinstance(checkpoint, dict):
                                if 'model_state_dict' in checkpoint:
                                    state_dict = checkpoint['model_state_dict']
                                elif 'state_dict' in checkpoint:
                                    state_dict = checkpoint['state_dict']
                                else:
                                    state_dict = checkpoint
                            else:
                                state_dict = checkpoint
                            
                            self.model.load_state_dict(state_dict, strict=False)
                            self.model.to(self.device)
                            self.model.eval()
                            model_loaded = True
                            
                            # Update status
                            self.root.after(0, lambda: self.status_label.config(
                                text=f"✅ Model loaded from {model_path}", 
                                fg='green'
                            ))
                            break
                            
                        except Exception as e:
                            continue
                
                if not model_loaded:
                    # Use pretrained model as fallback
                    self.model = CropDiseaseResNet50(num_classes=len(self.class_names), pretrained=True)
                    self.model.to(self.device)
                    self.model.eval()
                    
                    self.root.after(0, lambda: self.status_label.config(
                        text="⚠️ Using pretrained model (no trained weights found)", 
                        fg='orange'
                    ))
                
                # Enable predict button
                self.root.after(0, lambda: self.predict_button.config(state='normal'))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"❌ Error loading model: {str(e)}", 
                    fg='red'
                ))
        
        # Start loading in background
        threading.Thread(target=load_model, daemon=True).start()
    
    def load_disease_info(self):
        """Load disease information from knowledge base"""
        try:
            with open('knowledge_base/disease_info.json', 'r') as f:
                kb_data = json.load(f)
                for disease in kb_data['diseases']:
                    key = f"{disease['crop']}___{disease['disease']}"
                    self.disease_info[key] = disease
        except Exception as e:
            print(f"Warning: Could not load disease info: {e}")
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f8ff')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🌱 Crop Disease Detection AI", 
            font=('Arial', 24, 'bold'),
            bg='#f0f8ff',
            fg='#2e8b57'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Upload a crop leaf image to detect diseases using AI",
            font=('Arial', 12),
            bg='#f0f8ff',
            fg='#666666'
        )
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Image upload and display
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Image upload section
        upload_frame = tk.Frame(left_frame, bg='white')
        upload_frame.pack(pady=10)
        
        upload_button = tk.Button(
            upload_frame,
            text="📁 Select Image",
            command=self.upload_image,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        upload_button.pack(pady=5)
        
        # Image display area
        self.image_frame = tk.Frame(left_frame, bg='white')
        self.image_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="No image selected\n\nClick 'Select Image' to upload a crop leaf image",
            font=('Arial', 12),
            bg='#f9f9f9',
            fg='#666666',
            relief='ridge',
            bd=2
        )
        self.image_label.pack(fill='both', expand=True)
        
        # Predict button
        self.predict_button = tk.Button(
            left_frame,
            text="🔍 Analyze Disease",
            command=self.predict_disease,
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.predict_button.pack(pady=10)
        
        # Right panel - Results
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Results header
        results_header = tk.Label(
            right_frame,
            text="🎯 Analysis Results",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2e8b57'
        )
        results_header.pack(pady=10)
        
        # Results display area
        self.results_frame = tk.Frame(right_frame, bg='white')
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollable text area for results
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='#f9f9f9',
            relief='sunken',
            bd=1
        )
        self.results_text.pack(fill='both', expand=True)
        
        # Initial results message
        self.results_text.insert('1.0', 
            "🌱 Welcome to Crop Disease Detection AI!\n\n"
            "📋 Instructions:\n"
            "1. Click 'Select Image' to upload a crop leaf image\n"
            "2. Click 'Analyze Disease' to get AI prediction\n"
            "3. View detailed results here\n\n"
            "📊 Supported crops: Corn, Potato, Tomato\n"
            "🔬 AI Model: ResNet50 with transfer learning\n"
            "🎯 17 disease classes supported\n\n"
            "Ready to analyze your crop images! 🚀"
        )
        self.results_text.config(state='disabled')
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#e0e0e0', relief='sunken', bd=1)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(
            status_frame,
            text="🔄 Loading AI model...",
            font=('Arial', 10),
            bg='#e0e0e0',
            fg='blue'
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Device info
        device_info = f"💻 Device: {'GPU' if torch.cuda.is_available() else 'CPU'}"
        device_label = tk.Label(
            status_frame,
            text=device_info,
            font=('Arial', 10),
            bg='#e0e0e0',
            fg='#666666'
        )
        device_label.pack(side='right', padx=10, pady=5)
    
    def upload_image(self):
        """Handle image upload"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.tiff *.tif'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Crop Leaf Image",
            filetypes=file_types
        )
        
        if file_path:
            try:
                # Load and display image
                image = Image.open(file_path)
                self.current_image = image
                self.current_image_path = file_path
                
                # Resize image for display
                display_size = (300, 300)
                image_display = image.copy()
                image_display.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image_display)
                
                # Update image label
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # Keep a reference
                
                # Update status
                filename = os.path.basename(file_path)
                self.status_label.config(
                    text=f"📁 Image loaded: {filename}",
                    fg='green'
                )
                
                # Clear previous results
                self.results_text.config(state='normal')
                self.results_text.delete('1.0', tk.END)
                self.results_text.insert('1.0', 
                    f"📁 Image loaded: {filename}\n"
                    f"📐 Size: {image.size[0]} x {image.size[1]} pixels\n"
                    f"🎨 Mode: {image.mode}\n\n"
                    "Click 'Analyze Disease' to get AI prediction! 🔍"
                )
                self.results_text.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def predict_disease(self):
        """Predict disease from uploaded image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        if self.model is None:
            messagebox.showerror("Error", "AI model is not loaded yet. Please wait.")
            return
        
        # Update status
        self.status_label.config(text="🔄 Analyzing image...", fg='blue')
        self.predict_button.config(state='disabled', text="🔄 Analyzing...")
        
        # Run prediction in background thread
        def run_prediction():
            try:
                # Preprocess image
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                
                input_tensor = transform(self.current_image).unsqueeze(0).to(self.device)
                
                # Make prediction
                with torch.no_grad():
                    outputs = self.model(input_tensor)
                    probabilities = F.softmax(outputs, dim=1)
                    confidence, predicted_idx = torch.max(probabilities, 1)
                    
                    predicted_class = self.class_names[predicted_idx.item()]
                    confidence_score = confidence.item()
                
                # Get top 3 predictions
                top_probs, top_indices = torch.topk(probabilities[0], 3)
                top_predictions = [
                    (self.class_names[idx], prob.item()) 
                    for prob, idx in zip(top_probs, top_indices)
                ]
                
                # Parse crop and disease
                parts = predicted_class.split('___')
                crop = parts[0] if len(parts) > 0 else "Unknown"
                disease = parts[1] if len(parts) > 1 else predicted_class
                
                # Get disease information
                disease_details = self.disease_info.get(predicted_class, {})
                
                # Calculate risk level
                if confidence_score >= 0.8:
                    risk_level = "High" if 'healthy' not in disease.lower() else "Low"
                    risk_color = "🔴" if risk_level == "High" else "🟢"
                elif confidence_score >= 0.5:
                    risk_level = "Medium"
                    risk_color = "🟡"
                else:
                    risk_level = "Low"
                    risk_color = "🟢"
                
                # Update GUI with results
                self.root.after(0, lambda: self.display_results(
                    crop, disease, confidence_score, risk_level, risk_color,
                    top_predictions, disease_details
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_prediction_error(str(e)))
        
        # Start prediction in background
        threading.Thread(target=run_prediction, daemon=True).start()
    
    def display_results(self, crop, disease, confidence, risk_level, risk_color, top_predictions, disease_details):
        """Display prediction results in GUI"""
        
        # Update results text
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        
        # Main prediction
        results = f"🎯 AI PREDICTION RESULTS\n{'='*40}\n\n"
        results += f"🌾 Crop: {crop}\n"
        results += f"🦠 Disease: {disease.replace('_', ' ')}\n"
        results += f"📊 Confidence: {confidence:.1%}\n"
        results += f"{risk_color} Risk Level: {risk_level}\n\n"
        
        # Top predictions
        results += f"🏆 TOP 3 PREDICTIONS:\n{'-'*25}\n"
        for i, (pred_class, prob) in enumerate(top_predictions, 1):
            parts = pred_class.split('___')
            crop_name = parts[0]
            disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else pred_class
            results += f"{i}. {crop_name} - {disease_name}\n"
            results += f"   Confidence: {prob:.1%}\n\n"
        
        # Disease information
        if disease_details:
            results += f"📚 DISEASE INFORMATION:\n{'-'*30}\n"
            results += f"Description: {disease_details.get('description', 'N/A')}\n\n"
            
            if 'symptoms' in disease_details:
                results += f"🔍 Symptoms:\n"
                for symptom in disease_details['symptoms'][:4]:  # Show first 4 symptoms
                    results += f"• {symptom}\n"
                results += "\n"
            
            if 'solutions' in disease_details:
                results += f"💡 Treatment Solutions:\n"
                for solution in disease_details['solutions'][:4]:  # Show first 4 solutions
                    results += f"• {solution}\n"
                results += "\n"
            
            if 'prevention' in disease_details:
                results += f"🛡️ Prevention:\n"
                for prevention in disease_details['prevention'][:3]:  # Show first 3 prevention methods
                    results += f"• {prevention}\n"
        else:
            results += f"📚 DISEASE INFORMATION:\n{'-'*30}\n"
            results += "Detailed information not available for this disease.\n"
        
        # Add disclaimer
        results += f"\n⚠️ DISCLAIMER:\n{'-'*15}\n"
        results += "This AI prediction is for reference only.\n"
        results += "Please consult agricultural experts for\n"
        results += "professional diagnosis and treatment advice.\n"
        
        self.results_text.insert('1.0', results)
        self.results_text.config(state='disabled')
        
        # Update status
        self.status_label.config(
            text=f"✅ Analysis complete: {disease.replace('_', ' ')} ({confidence:.1%})",
            fg='green'
        )
        
        # Re-enable predict button
        self.predict_button.config(state='normal', text="🔍 Analyze Disease")
    
    def handle_prediction_error(self, error_msg):
        """Handle prediction errors"""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', 
            f"❌ PREDICTION ERROR\n{'='*25}\n\n"
            f"An error occurred during analysis:\n{error_msg}\n\n"
            f"Please try:\n"
            f"• Selecting a different image\n"
            f"• Ensuring the image is a clear crop leaf photo\n"
            f"• Restarting the application\n"
        )
        self.results_text.config(state='disabled')
        
        self.status_label.config(text="❌ Analysis failed", fg='red')
        self.predict_button.config(state='normal', text="🔍 Analyze Disease")

def main():
    """Main function to run the GUI application"""
    
    # Create main window
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')  # Add icon file if available
    except:
        pass
    
    # Create application
    app = CropDiseaseGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start GUI event loop
    root.mainloop()

if __name__ == "__main__":
    print("🚀 Starting Crop Disease Detection GUI...")
    main()
