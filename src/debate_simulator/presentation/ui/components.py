import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

from ...domain.characters.base import Character
from ...domain.debate.models import DebateMessage
from .styles import (
    get_character_message_class, get_character_emoji, 
    get_performance_class
)


def render_debate_message(message: DebateMessage, character: Character, competitive_mode: bool = False):
    """Render a single debate message with proper styling."""
    # Get display information
    message_class = get_character_message_class(character.name)
    emoji = get_character_emoji(character.name, character.metadata)
    
    # Format display name for random characters
    display_name = _get_character_display_name(character)
    
    # Generate stat bubbles for competitive mode
    stat_bubbles_html = ""
    if competitive_mode and character.stats:
        anger = character.stats.anger
        patience = character.stats.patience
        stat_bubbles_html = f"""
        <div class="stat-bubbles">
            <span class="stat-label">A:</span>
            <div class="stat-bubble anger-bubble">{anger}</div>
            <span class="stat-label">P:</span>
            <div class="stat-bubble patience-bubble">{patience}</div>
        </div>
        """
    
    # Escape HTML in the message content
    escaped_message = message.message.replace("<", "&lt;").replace(">", "&gt;")
    
    # Determine positioning based on character position
    position = character.position or "left"
    justify_style = "flex-start" if position == "left" else "flex-end"
    
    # Build HTML template
    html_template = f"""
    <div style="display: flex; justify-content: {justify_style};">
        <div class="debate-container">
            <div class="round-header">Round {message.round_number}</div>
            <div class="{message_class}">
                {stat_bubbles_html}
                <div class="speaker-name">{emoji} {display_name}</div>
                {escaped_message}
            </div>
        </div>
    </div>
    """
    
    st.markdown(html_template, unsafe_allow_html=True)


def render_competitive_results(results: Dict[str, Any]):
    """Render competitive mode results."""
    st.markdown("### 🏆 Competitive Mode Results")
    
    if not results or not results.get("participants"):
        st.warning("No competitive results available")
        return
    
    st.markdown("#### 📊 Final Performance Rankings")
    
    for i, participant in enumerate(results["participants"], 1):
        performance_class = get_performance_class(participant["performance"])
        
        # Create result display
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"**{i}. {participant['name']}**")
            
        with col2:
            stats = participant["stats"]
            st.markdown(f"A:{stats['anger']} P:{stats['patience']} U:{stats['uniqueness']}")
            
        with col3:
            st.markdown(
                f'<div class="performance-rating {performance_class}">{participant["performance"]}</div>',
                unsafe_allow_html=True
            )
        
        # Performance details
        with st.expander(f"Details for {participant['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Score", participant["total_score"])
                st.metric("Rating", f"{participant['rating']}/5")
            with col2:
                st.metric("Messages", participant["total_messages"])
                st.metric("Avg Length", f"{participant.get('avg_message_length', 0):.1f}")


def render_session_summary(session_status: Dict[str, Any]):
    """Render a summary of the debate session."""
    if session_status["status"] == "no_session":
        st.info("No active debate session")
        return
    
    st.markdown("### 📋 Session Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Status", session_status["status"].title())
        st.metric("Progress", f"{session_status.get('progress', 0):.0%}")
    
    with col2:
        st.metric("Topic", session_status.get("topic", "Unknown")[:30] + "...")
        st.metric("Session ID", session_status.get("session_id", "Unknown")[:8])
    
    with col3:
        summary = session_status.get("summary", {})
        if summary:
            st.metric("Total Rounds", summary.get("total_rounds", 0))
            st.metric("Total Messages", summary.get("total_messages", 0))


def render_character_selection(available_characters: Dict[str, str]) -> List[str]:
    """Render character selection interface and return selected character types."""
    st.markdown("### 🎭 Select Debate Participants")
    
    selected_characters = []
    
    # Default characters section
    st.markdown("#### Default Characters")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.checkbox("🔵 Market Liberal Democrat", value=True, key="dem"):
            selected_characters.append("democratic_commentator")
        if st.checkbox("🔴 MAGA Nationalist", value=True, key="rep"):
            selected_characters.append("republican_commentator")
    
    with col2:
        st.markdown("*Recommended for every debate*")
    
    # Additional characters section
    st.markdown("#### Additional Characters")
    
    additional_chars = [
        ("random_american", "🗽 Random American"),
        ("random_redditor", "🤖 Random Redditor"),
        ("marxist_leninist", "☭ Marxist-Leninist"),
        ("anarcho_capitalist", "💰 Anarcho-Capitalist"),
        ("catholic_theocrat", "⛪ Catholic Theocrat"),
        ("absolute_monarchist", "👑 Absolute Monarchist"),
        ("islamic_extremist", "☪️ Islamic Extremist"),
        ("evangelist_preacher", "✝️ Evangelist Preacher"),
        ("master_baiter", "🧠 Master Baiter"),
        ("chinese_communist", "🇨🇳 Chinese Communist")
    ]
    
    # Organize in columns
    cols = st.columns(2)
    for i, (char_type, display_name) in enumerate(additional_chars):
        with cols[i % 2]:
            if st.checkbox(display_name, key=char_type):
                selected_characters.append(char_type)
    
    # Show selection summary
    if selected_characters:
        st.success(f"Selected {len(selected_characters)} characters for the debate")
    else:
        st.warning("Please select at least one character")
    
    return selected_characters


def render_debate_controls(can_start: bool = True, is_running: bool = False) -> str:
    """Render debate control buttons and return the action taken."""
    st.markdown("### 🎮 Debate Controls")
    
    col1, col2, col3 = st.columns(3)
    
    action = None
    
    with col1:
        if st.button("🚀 Start Debate", disabled=not can_start or is_running, type="primary"):
            action = "start"
    
    with col2:
        if st.button("⏸️ Pause Debate", disabled=not is_running):
            action = "pause"
    
    with col3:
        if st.button("⏹️ Stop Debate", disabled=not is_running):
            action = "stop"
    
    return action


def render_topic_selection(available_topics: List[str]) -> str:
    """Render topic selection interface and return selected topic."""
    st.markdown("### 📋 Debate Topic")
    
    # Topic selection dropdown
    topic_option = st.selectbox(
        "Choose a preset topic:",
        ["Select a topic..."] + available_topics,
        key="topic_select"
    )
    
    # Custom topic input
    custom_topic = st.text_input(
        "Or enter a custom topic:",
        key="custom_topic",
        help="Enter your own debate topic"
    )
    
    # Determine selected topic
    if custom_topic.strip():
        selected_topic = custom_topic.strip()
        st.success(f"Custom topic: {selected_topic}")
    elif topic_option != "Select a topic...":
        selected_topic = topic_option
        st.success(f"Selected topic: {selected_topic}")
    else:
        selected_topic = None
        st.warning("Please select or enter a debate topic")
    
    return selected_topic


def render_debate_settings() -> Dict[str, Any]:
    """Render debate settings interface and return settings dict."""
    st.markdown("### ⚙️ Debate Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rounds = st.slider(
            "Number of rounds:",
            min_value=1,
            max_value=20,
            value=5,
            help="How many rounds of debate to conduct"
        )
        
        competitive_mode = st.checkbox(
            "Competitive Mode",
            value=True,
            help="Enable dynamic character stats and AI judging"
        )
    
    with col2:
        delay = st.slider(
            "Response delay (seconds):",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.5,
            help="Delay between character responses for readability"
        )
        
        auto_judge = st.checkbox(
            "Auto-judge rounds",
            value=True,
            help="Automatically judge each round in competitive mode"
        )
    
    return {
        "total_rounds": rounds,
        "response_delay": delay,
        "competitive_mode": competitive_mode,
        "auto_judge": auto_judge
    }


def render_progress_indicator(progress: float, current_round: int, total_rounds: int, current_speaker: str = None):
    """Render debate progress indicator."""
    # Progress bar
    progress_bar = st.progress(progress)
    
    # Status text
    if current_speaker:
        status_text = f"Round {current_round}/{total_rounds} - {current_speaker} responding..."
    else:
        status_text = f"Round {current_round}/{total_rounds}"
    
    st.text(status_text)
    
    return progress_bar


def render_error_message(error: str, error_type: str = "error"):
    """Render an error message with appropriate styling."""
    if error_type == "error":
        st.error(f"❌ {error}")
    elif error_type == "warning":
        st.warning(f"⚠️ {error}")
    elif error_type == "info":
        st.info(f"ℹ️ {error}")
    else:
        st.text(error)


def render_success_message(message: str, show_balloons: bool = False):
    """Render a success message."""
    st.success(f"✅ {message}")
    if show_balloons:
        st.balloons()


def render_loading_spinner(message: str = "Loading..."):
    """Render a loading spinner with message."""
    with st.spinner(message):
        pass


def render_debate_statistics(stats: Dict[str, Any]):
    """Render debate statistics and analytics."""
    st.markdown("### 📊 Debate Statistics")
    
    if not stats:
        st.info("No statistics available")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sessions", stats.get("total_sessions", 0))
    
    with col2:
        st.metric("Active Session", "Yes" if stats.get("current_session_active") else "No")
    
    with col3:
        character_stats = stats.get("character_stats", {})
        st.metric("Available Characters", character_stats.get("total_available", 0))
    
    with col4:
        st.metric("Cached Characters", character_stats.get("cached_characters", 0))
    
    # Current session details
    if stats.get("current_session"):
        st.markdown("#### Current Session")
        current = stats["current_session"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.text(f"Topic: {current['topic']}")
            st.text(f"Status: {current['status'].title()}")
        
        with col2:
            st.text(f"Participants: {len(current['participants'])}")
            st.text(f"Progress: {current['progress']:.0%}")


def _get_character_display_name(character: Character) -> str:
    """Get formatted display name for a character."""
    if "from" in character.name and "u/" not in character.name:
        # Random American character with age
        age = character.metadata.get("age", "")
        if age:
            name_part = character.name.split(" from ")[0]
            city_part = character.name.split(" from ")[1]
            return f"{name_part} from {city_part} ({age}yo)"
    
    return character.name


def render_export_import_section():
    """Render session export/import controls."""
    st.markdown("### 💾 Session Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export Session")
        if st.button("📥 Download Current Session"):
            return "export"
    
    with col2:
        st.markdown("#### Import Session")
        uploaded_file = st.file_uploader(
            "Upload session file:",
            type=["json"],
            help="Upload a previously exported debate session"
        )
        
        if uploaded_file and st.button("📤 Load Session"):
            return ("import", uploaded_file)
    
    return None