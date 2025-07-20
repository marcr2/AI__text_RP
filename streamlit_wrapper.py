#!/usr/bin/env python3
"""
Streamlit wrapper to prevent ScriptRunContext issues
"""
import os
import sys
import subprocess
import signal
import time

def main():
    """Main function to run Streamlit with proper context"""
    
    # Set environment variables to prevent ScriptRunContext issues
    os.environ.setdefault('STREAMLIT_SERVER_PORT', '8501')
    os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', 'localhost')
    os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')
    os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')
    os.environ.setdefault('STREAMLIT_LOGGER_LEVEL', 'info')
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Starting AI Political Debate Simulator...")
    print("Using Streamlit wrapper to prevent ScriptRunContext issues")
    print("=" * 60)
    
    process = None
    try:
        # Use subprocess to run streamlit with proper module execution
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            'streamlit_app.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ]
        
        # Run the command
        process = subprocess.Popen(cmd, env=os.environ.copy())
        
        print(f"Streamlit started with PID: {process.pid}")
        print("Press Ctrl+C to stop the server")
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down Streamlit server...")
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("Server stopped.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 