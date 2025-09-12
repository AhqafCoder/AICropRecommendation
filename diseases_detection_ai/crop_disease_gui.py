"""
Crop Disease Detection GUI Application
User-friendly Tkinter interface for testing the AI model with image uploads
Enhanced with Grad-CAM visual explanations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import sys
import os
import json
import threading
import time
from pathlib import Path

# Try to import required packages with error handling
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: NumPy not available: {e}")
    NUMPY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Matplotlib not available: {e}")
    MATPLOTLIB_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OpenCV not available: {e}")
    OPENCV_AVAILABLE = False

# Try to import PyTorch components with error handling
try:
    import torch
    import torch.nn.functional as F
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError as e:
    print(f"Warning: PyTorch not available: {e}")
    print("The GUI will start but model functionality will be limited.")
    TORCH_AVAILABLE = False

# Add src to path for imports
sys.path.append('src')

class CropDiseaseGUI:
    """Main GUI application for crop disease detection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Crop Disease Detection AI with Visual Explanations")
        self.root.geometry("1400x800")  # Increased width for heatmap display
        self.root.configure(bg='#f0f8ff')
        
        # Initialize variables
        self.model = None
        self.class_names = []
        self.device = None
        self.current_image = None
        self.current_image_path = None
        self.disease_info = {}
        self.grad_cam = None  # For Grad-CAM explanations
        
        # Progress tracking variables
        self.progress_steps = [
            "🔄 Initializing analysis...",
            "🖼️ Processing image...", 
            "🧠 Running AI prediction...",
            "🔥 Generating heatmap...",
            "🎨 Creating overlay...",
            "📊 Analyzing attention...",
            "✅ Analysis complete!"
        ]
        self.current_step = 0
        
        # Load disease info first
        self.load_disease_info()
        
        # Create GUI
        self.create_widgets()
        
        # Load model after GUI is created (delayed start)
        self.root.after(100, self.load_model_async)
        
    def load_model_async(self):
        """Load model in background thread"""
        def load_model():
            try:
                # Check if GUI components are initialized
                if not hasattr(self, 'status_label') or not self.status_label:
                    return
                    
                if not TORCH_AVAILABLE:
                    self.root.after(0, lambda: self.status_label.config(
                        text="❌ PyTorch not available - Model functionality disabled", 
                        fg='red'
                    ))
                    return
                
                if not NUMPY_AVAILABLE:
                    self.root.after(0, lambda: self.status_label.config(
                        text="❌ NumPy not available - Model functionality disabled", 
                        fg='red'
                    ))
                    return
                
                from src.model import CropDiseaseResNet50
                
                # Try to import Grad-CAM with error handling
                try:
                    from src.explain import GradCAM
                    GRADCAM_AVAILABLE = True
                except ImportError as e:
                    print(f"Warning: Grad-CAM not available: {e}")
                    GRADCAM_AVAILABLE = False
                
                # Class names (updated for V3 model: Pepper, Potato, Tomato)
                self.class_names = [
                    'Pepper__bell___Bacterial_spot',
                    'Pepper__bell___healthy',
                    'Potato___Early_blight',
                    'Potato___healthy',
                    'Potato___Late_blight',
                    'Tomato__Target_Spot',
                    'Tomato__Tomato_mosaic_virus',
                    'Tomato__Tomato_YellowLeaf__Curl_Virus',
                    'Tomato_Bacterial_spot',
                    'Tomato_Early_blight',
                    'Tomato_healthy',
                    'Tomato_Late_blight',
                    'Tomato_Leaf_Mold',
                    'Tomato_Septoria_leaf_spot',
                    'Tomato_Spider_mites_Two_spotted_spider_mite'
                ]
                
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                
                # Load the specified model
                model_path = 'models/crop_disease_v3_model.pth'
                
                if os.path.exists(model_path):
                    try:
                        self.model = CropDiseaseResNet50(num_classes=len(self.class_names), pretrained=False)
                        checkpoint = torch.load(model_path, map_location=self.device)
                        
                        # Handle checkpoint format from crop_disease_v3_model.pth
                        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                            state_dict = checkpoint['model_state_dict']
                            # Also load class names from checkpoint if available
                            if 'class_names' in checkpoint:
                                saved_class_names = checkpoint['class_names']
                                if len(saved_class_names) != len(self.class_names):
                                    print(f"Warning: Class count mismatch. Saved: {len(saved_class_names)}, Current: {len(self.class_names)}")
                                self.class_names = saved_class_names  # Use class names from model
                        elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                            state_dict = checkpoint['state_dict']
                        else:
                            state_dict = checkpoint
                        
                        self.model.load_state_dict(state_dict, strict=True)  # Changed to strict=True for better error detection
                        self.model.to(self.device)
                        self.model.eval()
                        
                        # Initialize Grad-CAM if available
                        if GRADCAM_AVAILABLE:
                            from src.explain import GradCAM
                            self.grad_cam = GradCAM(self.model)
                            status_msg = f"✅ Model and Grad-CAM loaded from {os.path.basename(model_path)}"
                        else:
                            status_msg = f"✅ Model loaded from {os.path.basename(model_path)} (Grad-CAM unavailable)"
                        
                        # Update status
                        if hasattr(self, 'status_label') and self.status_label:
                            self.root.after(0, lambda: self.status_label.config(
                                text=status_msg, 
                                fg='green'
                            ))
                        
                    except Exception as e:
                        error_msg = f"❌ Error loading model: {str(e)}"
                        if hasattr(self, 'status_label') and self.status_label:
                            self.root.after(0, lambda: self.status_label.config(
                                text=error_msg, 
                                fg='red'
                            ))
                else:
                    error_msg = f"❌ Model file not found: {model_path}"
                    if hasattr(self, 'status_label') and self.status_label:
                        self.root.after(0, lambda: self.status_label.config(
                            text=error_msg, 
                            fg='red'
                        ))
                
                # Enable predict button
                if hasattr(self, 'predict_button') and self.predict_button:
                    self.root.after(0, lambda: self.predict_button.config(state='normal'))
                
            except Exception as e:
                # Check if GUI components are initialized before updating
                if hasattr(self, 'status_label') and self.status_label:
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"❌ Error loading model: {str(e)}", 
                        fg='red'
                    ))
        
        # Start loading in background
        threading.Thread(target=load_model, daemon=True).start()
    
    def show_progress(self, step_index=None, message=None):
        """Show progress indicator with current step"""
        # Hide heatmap display and show progress
        self.heatmap_label.pack_forget()
        self.progress_frame.pack(expand=True)
        
        if step_index is not None:
            self.current_step = step_index
            if step_index < len(self.progress_steps):
                message = self.progress_steps[step_index]
        
        if message:
            self.progress_label.config(text=message)
        
        # Draw animated progress bar
        self.draw_progress_animation()
        self.root.update_idletasks()
    
    def hide_progress(self):
        """Hide progress indicator and show heatmap area"""
        self.progress_frame.pack_forget()
        self.heatmap_label.pack(fill='both', expand=True)
        self.current_step = 0
    
    def draw_progress_animation(self):
        """Draw animated progress indicator"""
        self.progress_canvas.delete("all")
        
        # Draw progress bar background
        self.progress_canvas.create_rectangle(10, 8, 190, 12, fill='#e0e0e0', outline='')
        
        # Calculate progress percentage
        progress = (self.current_step + 1) / len(self.progress_steps)
        progress_width = int(180 * progress)
        
        # Draw progress bar fill
        if progress_width > 0:
            self.progress_canvas.create_rectangle(10, 8, 10 + progress_width, 12, 
                                                fill='#2e8b57', outline='')
        
        # Draw animated dots for current processing
        import time
        dot_count = int(time.time() * 3) % 4  # Animated dots
        dots = "." * dot_count
        
        # Update canvas
        self.root.update_idletasks()
    
    def load_disease_info(self):
        """Load disease information from knowledge base"""
        try:
            with open('knowledge_base/disease_info.json', 'r') as f:
                kb_data = json.load(f)
                for disease in kb_data['diseases']:
                    # Use the class_name field directly as the key
                    class_name = disease.get('class_name')
                    if class_name:
                        self.disease_info[class_name] = disease
        except Exception as e:
            print(f"Warning: Could not load disease info: {e}")
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f8ff')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🌱 Crop Disease Detection AI with Visual Explanations", 
            font=('Arial', 24, 'bold'),
            bg='#f0f8ff',
            fg='#2e8b57'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Upload a crop leaf image to detect diseases using AI with Grad-CAM visual explanations",
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
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
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
        
        # Original image display area
        original_label = tk.Label(left_frame, text="📷 Original Image", font=('Arial', 14, 'bold'), bg='white', fg='#2e8b57')
        original_label.pack(pady=(5, 0))
        
        self.image_frame = tk.Frame(left_frame, bg='white')
        self.image_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
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
        
        # Middle panel - Heatmap visualization
        middle_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        middle_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Heatmap header
        heatmap_label = tk.Label(middle_frame, text="🔥 Grad-CAM Heatmap", font=('Arial', 14, 'bold'), bg='white', fg='#2e8b57')
        heatmap_label.pack(pady=(10, 5))
        
        # Heatmap display area
        self.heatmap_frame = tk.Frame(middle_frame, bg='white')
        self.heatmap_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Progress indicators (initially hidden)
        self.progress_frame = tk.Frame(self.heatmap_frame, bg='white')
        self.progress_frame.pack(expand=True)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2e8b57'
        )
        self.progress_label.pack(pady=10)
        
        # Canvas for animated progress indicator
        self.progress_canvas = tk.Canvas(self.progress_frame, width=200, height=20, bg='white', highlightthickness=0)
        self.progress_canvas.pack(pady=5)
        
        # Hide progress frame initially
        self.progress_frame.pack_forget()

        self.heatmap_label = tk.Label(
            self.heatmap_frame,
            text="Visual explanation will appear here\n\nThe heatmap shows which parts of the leaf\nthe AI focuses on for disease detection",
            font=('Arial', 11),
            bg='#f9f9f9',
            fg='#666666',
            relief='ridge',
            bd=2
        )
        self.heatmap_label.pack(fill='both', expand=True)        # Explanation text
        explanation_text = tk.Label(
            middle_frame,
            text="🎯 Red regions = High attention\n🟡 Yellow regions = Medium attention\n🔵 Blue regions = Low attention",
            font=('Arial', 9),
            bg='white',
            fg='#444444',
            justify='left'
        )
        explanation_text.pack(pady=(0, 10))
        
        # Right panel - Results
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
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
            font=('Arial', 9),
            bg='#f9f9f9',
            relief='sunken',
            bd=1,
            height=25,  # Increased height for better display
            width=50    # Set width for better text wrapping
        )
        self.results_text.pack(fill='both', expand=True)
        
        # Initial results message
        self.results_text.insert('1.0', 
            "🌱 Welcome to Crop Disease Detection AI!\n\n"
            "📋 Instructions:\n"
            "1. Click 'Select Image' to upload a crop leaf image\n"
            "2. Click 'Analyze Disease' to get AI prediction\n"
            "3. View detailed results and visual explanations\n\n"
            "📊 Supported crops: Corn, Potato, Tomato\n"
            "🔬 AI Model: ResNet50 with transfer learning\n"
            "🎯 17 disease classes supported\n"
            "🔥 Visual explanations with Grad-CAM\n\n"
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
        if TORCH_AVAILABLE and NUMPY_AVAILABLE:
            device_info = f"💻 Device: {'GPU' if torch.cuda.is_available() else 'CPU'}"
        else:
            missing_packages = []
            if not TORCH_AVAILABLE:
                missing_packages.append("PyTorch")
            if not NUMPY_AVAILABLE:
                missing_packages.append("NumPy")
            device_info = f"⚠️ Missing: {', '.join(missing_packages)}"
        
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
                    "Click 'Analyze Disease' to get AI prediction and visual explanation! 🔍"
                )
                self.results_text.config(state='disabled')
                
                # Clear previous heatmap
                self.heatmap_label.config(
                    image='',
                    text="Visual explanation will appear here\n\nThe heatmap shows which parts of the leaf\nthe AI focuses on for disease detection"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def generate_gradcam_heatmap(self, input_tensor, predicted_class_idx):
        """Generate Grad-CAM heatmap for the predicted class"""
        try:
            if self.grad_cam is None:
                return None
            
            # Generate Grad-CAM
            cam, _, _ = self.grad_cam.generate_cam(input_tensor, predicted_class_idx)
            return cam
            
        except Exception as e:
            print(f"Error generating Grad-CAM: {e}")
            return None
    
    def create_heatmap_overlay(self, original_image, cam, alpha=0.4):
        """Create heatmap overlay on original image"""
        try:
            if not OPENCV_AVAILABLE or not MATPLOTLIB_AVAILABLE or not NUMPY_AVAILABLE:
                print("Warning: Required packages not available for heatmap overlay")
                return original_image
            
            # Resize CAM to match original image size
            original_size = original_image.size
            cam_resized = cv2.resize(cam, original_size)
            
            # Convert to heatmap using jet colormap
            heatmap = cm.jet(cam_resized)[:, :, :3]  # Remove alpha channel
            heatmap = (heatmap * 255).astype(np.uint8)
            
            # Convert original image to numpy
            original_np = np.array(original_image)
            
            # Ensure both images have the same number of channels
            if len(original_np.shape) == 3 and original_np.shape[2] == 3:
                # RGB image
                overlay = cv2.addWeighted(original_np, 1-alpha, heatmap, alpha, 0)
            else:
                # Convert grayscale to RGB if needed
                if len(original_np.shape) == 2:
                    original_np = cv2.cvtColor(original_np, cv2.COLOR_GRAY2RGB)
                overlay = cv2.addWeighted(original_np, 1-alpha, heatmap, alpha, 0)
            
            return Image.fromarray(overlay)
            
        except Exception as e:
            print(f"Error creating heatmap overlay: {e}")
            return original_image
    
    def display_heatmap(self, heatmap_image):
        """Display the heatmap in the GUI"""
        try:
            # Resize heatmap for display
            display_size = (280, 280)
            heatmap_display = heatmap_image.copy()
            heatmap_display.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            heatmap_photo = ImageTk.PhotoImage(heatmap_display)
            
            # Update heatmap label
            self.heatmap_label.config(image=heatmap_photo, text="")
            self.heatmap_label.image = heatmap_photo  # Keep a reference
            
        except Exception as e:
            print(f"Error displaying heatmap: {e}")
            self.heatmap_label.config(
                text=f"Error displaying heatmap:\n{str(e)}",
                image=''
            )
    
    def predict_disease_threaded(self):
        """Run prediction in a separate thread to avoid blocking UI"""
        try:
            start_time = time.time()
            
            # Step 1: Initialize
            self.root.after(0, lambda: self.show_progress(0))
            time.sleep(0.5)  # Brief pause for user to see step
            
            # Step 2: Process image
            self.root.after(0, lambda: self.show_progress(1))
            
            # Preprocess image
            img_tensor = self.preprocess_image(self.current_image_path)
            if img_tensor is None:
                self.root.after(0, lambda: self.show_error("Failed to preprocess image"))
                return
            
            # Step 3: Run prediction
            self.root.after(0, lambda: self.show_progress(2))
            time.sleep(0.3)
            
            # Get prediction
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                predicted_idx = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_idx].item()
                
                predicted_class = self.class_names[predicted_idx]
            
            # Step 4: Generate heatmap
            self.root.after(0, lambda: self.show_progress(3))
            time.sleep(0.3)
            
            # Generate Grad-CAM heatmap
            try:
                if self.grad_cam is None:
                    from src.explain import CropDiseaseExplainer
                    self.grad_cam = CropDiseaseExplainer(self.model, self.class_names, self.device)
                
                # Step 5: Create overlay
                self.root.after(0, lambda: self.show_progress(4))
                
                heatmap_data = self.grad_cam.explain_prediction(
                    self.current_image_path, 
                    return_base64=True
                )
                
                if heatmap_data and 'overlay_base64' in heatmap_data:
                    # Step 6: Analyze attention
                    self.root.after(0, lambda: self.show_progress(5))
                    time.sleep(0.2)
                    
                    # Decode and display heatmap
                    import base64
                    from io import BytesIO
                    
                    overlay_data = base64.b64decode(heatmap_data['overlay_base64'])
                    overlay_image = Image.open(BytesIO(overlay_data))
                    
                    # Step 7: Complete
                    elapsed_time = time.time() - start_time
                    self.root.after(0, lambda: self.show_progress(6))
                    time.sleep(0.3)
                    
                    # Update UI with results
                    self.root.after(0, lambda: self.display_results(
                        predicted_class, confidence, overlay_image, elapsed_time
                    ))
                else:
                    self.root.after(0, lambda: self.display_results(
                        predicted_class, confidence, None, time.time() - start_time
                    ))
                    
            except Exception as e:
                print(f"Grad-CAM error: {e}")
                # Still show prediction without heatmap
                elapsed_time = time.time() - start_time
                self.root.after(0, lambda: self.display_results(
                    predicted_class, confidence, None, elapsed_time
                ))
                
        except Exception as e:
            error_msg = f"Prediction failed: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: self.show_error(error_msg))
    
    def predict_disease(self):
        """Start prediction process with progress tracking"""
        if self.current_image_path is None:
            self.show_error("Please select an image first")
            return
        
        if self.model is None:
            self.show_error("Model not loaded. Please restart the application.")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Start prediction in background thread
        import threading
        thread = threading.Thread(target=self.predict_disease_threaded)
        thread.daemon = True
        thread.start()
    
    def display_results(self, predicted_class, confidence, heatmap_image=None, elapsed_time=0):
        """Display prediction results and heatmap"""
        # Hide progress and show results
        self.hide_progress()
        
        # Display heatmap if available
        if heatmap_image:
            # Resize heatmap to fit the frame
            display_size = (400, 300)
            heatmap_image = heatmap_image.resize(display_size, Image.Resampling.LANCZOS)
            heatmap_photo = ImageTk.PhotoImage(heatmap_image)
            
            self.heatmap_label.config(
                image=heatmap_photo,
                text="",
                compound='center'
            )
            self.heatmap_label.image = heatmap_photo  # Keep reference
        else:
            self.heatmap_label.config(
                image="",
                text="Heatmap generation failed\n\nPrediction available in results panel →",
                font=('Arial', 11),
                bg='#fff3cd',
                fg='#856404'
            )
        
        # Update prediction results
        risk_level = self.determine_risk_level(predicted_class)
        
        # Update result text
        result_text = f"🔍 PREDICTION RESULTS\n{'='*40}\n\n"
        result_text += f"Disease: {predicted_class.replace('___', ' - ')}\n"
        result_text += f"Confidence: {confidence:.1%}\n"
        result_text += f"Risk Level: {risk_level}\n\n"
        
        # Add timing info
        result_text += f"⏱️ Analysis completed in {elapsed_time:.2f}s\n"
        if heatmap_image:
            result_text += f"✅ Visual explanation generated\n\n"
        else:
            result_text += f"⚠️ Visual explanation unavailable\n\n"
        
        # Add disease information
        disease_info = self.disease_info.get(predicted_class, {})
        if disease_info:
            result_text += f"ℹ️ DISEASE INFORMATION\n{'='*40}\n\n"
            
            if 'description' in disease_info:
                result_text += f"📋 Description:\n"
                # Wrap description text to improve readability
                description = disease_info['description']
                words = description.split()
                wrapped_description = ""
                line_length = 0
                for word in words:
                    if line_length + len(word) + 1 > 50:  # Wrap at ~50 characters
                        wrapped_description += "\n"
                        line_length = 0
                    wrapped_description += word + " "
                    line_length += len(word) + 1
                result_text += wrapped_description.strip() + "\n\n"
            
            if 'symptoms' in disease_info:
                result_text += f"🔍 Key Symptoms:\n"
                for i, symptom in enumerate(disease_info['symptoms'][:5], 1):  # Show first 5
                    result_text += f"{i}. {symptom}\n"
                result_text += "\n"
            
            if 'solutions' in disease_info:
                result_text += f"💊 Solutions:\n"
                for i, solution in enumerate(disease_info['solutions'][:5], 1):  # Show first 5
                    result_text += f"{i}. {solution}\n"
                result_text += "\n"
                
            if 'prevention' in disease_info:
                result_text += f"🛡️ Prevention Tips:\n"
                for i, prevention in enumerate(disease_info['prevention'][:3], 1):  # Show first 3
                    result_text += f"{i}. {prevention}\n"
                result_text += "\n"
        else:
            result_text += f"ℹ️ DISEASE INFORMATION\n{'='*40}\n\n"
            result_text += "Detailed information not available for this disease.\n"
            result_text += "Please consult agricultural experts for more details.\n\n"
        
        # Add disclaimer
        result_text += f"⚠️ DISCLAIMER\n{'='*20}\n"
        result_text += "This AI prediction is for reference only.\n"
        result_text += "Please consult agricultural experts for\n"
        result_text += "professional diagnosis and treatment advice."
        
        # Show success message in status bar
        status_msg = f"✅ Analysis complete! {predicted_class} detected with {confidence:.1%} confidence"
        self.status_label.config(text=status_msg, fg='#2e8b57')
        
        # Update result display
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)
        self.results_text.config(state='disabled')
    
    def show_error(self, message):
        """Show error message and hide progress"""
        self.hide_progress()
        self.status_label.config(text=f"❌ {message}", fg='#dc3545')
        
        # Show error in heatmap area
        self.heatmap_label.config(
            image="",
            text=f"Error occurred:\n\n{message}",
            font=('Arial', 11),
            bg='#f8d7da',
            fg='#721c24'
        )
    
    def clear_results(self):
        """Clear previous results"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        self.status_label.config(text="Ready for analysis...", fg='#666666')

    def determine_risk_level(self, predicted_class):
        """Determine risk level based on disease prediction"""
        if 'healthy' in predicted_class.lower():
            return "🟢 Low Risk - Healthy Plant"
        elif any(term in predicted_class.lower() for term in ['blight', 'spot', 'rust', 'mold']):
            return "🔴 High Risk - Disease Detected"
        else:
            return "🟡 Medium Risk - Monitor Closely"

    def preprocess_image(self, image_path):
        """Preprocess image for model prediction"""
        try:
            if not TORCH_AVAILABLE:
                return None
                
            import torchvision.transforms as transforms
            
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            return transform(image).unsqueeze(0).to(self.device)
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None


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
    
    # Configure window resizing
    root.minsize(1200, 600)  # Minimum size for proper display
    
    # Start GUI event loop
    root.mainloop()

if __name__ == "__main__":
    print("🚀 Starting Crop Disease Detection GUI with Visual Explanations...")
    print("🔥 Features: AI Disease Detection + Grad-CAM Heatmaps")
    main()
