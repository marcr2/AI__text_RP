#!/bin/bash

echo "Starting AI Political Debate Simulator - Web Interface"
echo "======================================================"
echo ""
echo "This will open the web interface in your browser."
echo "Make sure you have set your OpenAI API key in the .env file."
echo ""

# Set environment variables to prevent ScriptRunContext issues
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_LOGGER_LEVEL=info

# Use python -m streamlit instead of streamlit directly to avoid context issues
python -m streamlit run streamlit_app.py --server.port=8501 --server.address=localhost --server.headless=true --browser.gatherUsageStats=false 