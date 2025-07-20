def get_css_styles() -> str:
    """Get the complete CSS styles for the debate simulator."""
    return """
    <style>
    /* Dark theme background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #64b5f6;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Debate container styling */
    .debate-container {
        background-color: transparent;
        padding: 0.3rem;
        margin: 0.3rem 0;
        border-radius: 12px;
        max-width: 70%;
    }
    
    /* Democratic message styling */
    .democrat-message {
        background-color: rgba(13, 71, 161, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Republican message styling */
    .republican-message {
        background-color: rgba(183, 28, 28, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Redditor message styling */
    .redditor-message {
        background-color: rgba(199, 21, 133, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Marxist message styling */
    .marxist-message {
        background-color: rgba(198, 40, 40, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Anarcho message styling */
    .anarcho-message {
        background-color: rgba(230, 81, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Catholic message styling */
    .catholic-message {
        background-color: rgba(33, 33, 33, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Monarchist message styling */
    .monarchist-message {
        background-color: rgba(74, 20, 140, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Islamic message styling */
    .islamic-message {
        background-color: rgba(27, 94, 32, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Evangelist message styling */
    .evangelist-message {
        background-color: rgba(141, 110, 99, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Random American message styling */
    .random-american-message {
        background-color: rgba(230, 81, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Master Baiter message styling */
    .master-baiter-message {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Chinese Communist message styling */
    .chinese-communist-message {
        background-color: rgba(139, 0, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Speaker name styling */
    .speaker-name {
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
        color: #ffffff;
        opacity: 0.9;
    }
    
    /* Round header styling */
    .round-header {
        background-color: #2d2d2d;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
        color: #ffffff;
        border: 1px solid #444444;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    /* Chat flow improvements */
    .debate-container {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Message spacing */
    .debate-container:not(:last-child) {
        margin-bottom: 0.3rem;
    }
    
    /* Stat bubbles styling */
    .stat-bubbles {
        display: flex;
        gap: 0.3rem;
        margin-bottom: 0.2rem;
        justify-content: flex-start;
    }
    
    .stat-bubble {
        background-color: rgba(255, 255, 255, 0.9);
        color: #000000;
        border-radius: 50%;
        width: 1.5rem;
        height: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: bold;
        border: 1px solid rgba(0, 0, 0, 0.3);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .anger-bubble {
        background-color: rgba(255, 0, 0, 0.8);
        color: white;
    }
    
    .patience-bubble {
        background-color: rgba(0, 255, 0, 0.8);
        color: white;
    }
    
    .stat-label {
        font-size: 0.6rem;
        color: rgba(255, 255, 255, 0.7);
        margin-right: 0.2rem;
        font-weight: bold;
    }
    
    /* Results and summary styling */
    .results-container {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .performance-rating {
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        margin: 0.2rem 0;
    }
    
    .performance-excellent {
        background-color: rgba(76, 175, 80, 0.8);
        color: white;
    }
    
    .performance-good {
        background-color: rgba(255, 193, 7, 0.8);
        color: black;
    }
    
    .performance-average {
        background-color: rgba(255, 152, 0, 0.8);
        color: white;
    }
    
    .performance-poor {
        background-color: rgba(244, 67, 54, 0.8);
        color: white;
    }
    
    /* General text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, div, span {
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0e1117;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2d2d2d;
        border: 1px solid #666666;
        transform: translateY(-1px);
    }
    
    /* Success/warning/error styling */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .debate-container {
            max-width: 90%;
        }
        
        .main-header {
            font-size: 2rem;
        }
    }
    </style>
    """


def get_character_message_class(character_name: str) -> str:
    """Get the appropriate CSS class for a character's message."""
    character_styles = {
        "Market Liberal Democrat": "democrat-message",
        "MAGA Nationalist": "republican-message",
        "Marxist-Leninist": "marxist-message",
        "Anarcho-Capitalist Libertarian": "anarcho-message",
        "Catholic Theocrat": "catholic-message",
        "Absolute Monarchist": "monarchist-message",
        "Islamic Extremist": "islamic-message",
        "Evangelist Preacher": "evangelist-message",
        "Master Baiter": "master-baiter-message",
        "Chinese Communist Party Official": "chinese-communist-message",
    }
    
    # Check for random characters
    if "from" in character_name and "u/" not in character_name:
        return "random-american-message"
    elif "u/" in character_name:
        return "redditor-message"
    
    # Use specific character styling or default
    return character_styles.get(character_name, "democrat-message")


def get_character_emoji(character_name: str, character_metadata: dict = None) -> str:
    """Get the appropriate emoji for a character."""
    character_emojis = {
        "Market Liberal Democrat": "🔵",
        "MAGA Nationalist": "🔴",
        "Marxist-Leninist": "☭",
        "Anarcho-Capitalist Libertarian": "$",
        "Catholic Theocrat": "⛪",
        "Absolute Monarchist": "👑",
        "Islamic Extremist": "☪️",
        "Evangelist Preacher": "✝️",
        "Master Baiter": "💪",
        "Chinese Communist Party Official": "🇨🇳",
    }
    
    # Check for random characters
    if "from" in character_name and "u/" not in character_name:
        # Random American character
        if character_metadata and character_metadata.get("gender") == "female":
            return "👩"
        else:
            return "👨"
    elif "u/" in character_name:
        # Random Redditor character
        return "🤖"
    
    # Use specific character emoji or default
    return character_emojis.get(character_name, "⚫")


def get_performance_class(performance: str) -> str:
    """Get CSS class for performance rating."""
    performance_classes = {
        "EXCELLENT": "performance-excellent",
        "GOOD": "performance-good",
        "AVERAGE": "performance-average", 
        "POOR": "performance-poor",
        "VERY POOR": "performance-poor"
    }
    
    return performance_classes.get(performance.upper(), "performance-average")