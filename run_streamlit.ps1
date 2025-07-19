# AI Political Debate Simulator - Streamlit Launcher
Write-Host "🤖 AI Political Debate Simulator - Web Interface" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please run setup.py first to create the .env file." -ForegroundColor Yellow
    exit 1
}

# Check if OpenAI API key is configured
$envContent = Get-Content ".env" -Raw
if ($envContent -like "*your_openai_api_key_here*") {
    Write-Host "⚠️  OpenAI API key not configured!" -ForegroundColor Yellow
    Write-Host "Please edit the .env file and add your OpenAI API key." -ForegroundColor Yellow
    Write-Host "Get an API key from: https://platform.openai.com/api-keys" -ForegroundColor Cyan
}

Write-Host "`n🚀 Starting Streamlit web interface..." -ForegroundColor Green
Write-Host "The web interface will open in your browser automatically." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Gray

try {
    streamlit run streamlit_app.py
}
catch {
    Write-Host "❌ Error starting Streamlit: $_" -ForegroundColor Red
    Write-Host "Make sure Streamlit is installed: pip install streamlit" -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 