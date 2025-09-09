@echo off
echo 🚀 Starting Crop AI Streamlit GUI...
echo.
echo 📍 The app will open in your default browser
echo 🌐 URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
call "%~dp0venv\Scripts\activate.bat"
streamlit run ai_test_gui.py --server.port=8501 --server.address=localhost
