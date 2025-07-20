# Troubleshooting Guide

## ScriptRunContext Error

If you're seeing the error `Thread 'MainThread': missing ScriptRunContext!`, this is a common Streamlit issue that occurs when Streamlit functions are called outside the proper execution context.

### Quick Fixes

1. **Use the Streamlit Wrapper (Recommended)**
   ```bash
   python streamlit_wrapper.py
   ```
   This wrapper ensures proper context initialization.

2. **Use the correct launch configuration**
   - In VS Code, select "Streamlit Wrapper (Recommended)" from the debug configurations
   - This uses the proper module execution method

3. **Run with python -m streamlit**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

### Alternative Solutions

1. **Test with the simple test script first**
   ```bash
   python -m streamlit run test_streamlit.py
   ```
   This will help verify if Streamlit is working correctly.

2. **Check your environment**
   - Make sure you're in the correct directory
   - Verify that all dependencies are installed: `pip install -r requirements.txt`
   - Check that you have a `.env` file with your OpenAI API key

3. **Clear Streamlit cache**
   ```bash
   streamlit cache clear
   ```

### Common Causes

1. **Threading Issues**: The `time.sleep()` calls in the debate simulation can cause context issues
2. **Improper Launch Method**: Running Streamlit directly instead of through the module system
3. **Environment Variables**: Missing or incorrect Streamlit environment variables
4. **File Path Issues**: Running from the wrong directory

### Debug Steps

1. **Check the logs**: Look at `debate.log` for specific error messages
2. **Test basic functionality**: Use the test script to verify Streamlit works
3. **Check dependencies**: Ensure all packages are up to date
4. **Verify environment**: Make sure your `.env` file exists and contains the API key

### Environment Variables

The following environment variables help prevent ScriptRunContext issues:

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_LOGGER_LEVEL=info
```

### Launch Configurations

The VS Code launch configurations have been updated with several options:

1. **Streamlit Wrapper (Recommended)**: Uses the wrapper script for proper context
2. **Streamlit Debug (Fixed ScriptRunContext)**: Uses module execution with proper environment
3. **Test Streamlit (Debug)**: Tests basic Streamlit functionality
4. **Streamlit Direct Run**: Direct module execution

### If Nothing Works

1. **Restart VS Code**: Sometimes the debugger gets stuck
2. **Clear Python cache**: Delete `__pycache__` directories
3. **Reinstall dependencies**: `pip install --force-reinstall -r requirements.txt`
4. **Check Python version**: Ensure you're using Python 3.8+ and the correct virtual environment

### Getting Help

If you're still experiencing issues:

1. Check the `debate.log` file for specific error messages
2. Try running the test script first to isolate the issue
3. Verify your OpenAI API key is set correctly
4. Check that all files are in the correct locations 