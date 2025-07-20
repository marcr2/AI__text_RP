import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Import the refactored application
from ..infrastructure.config import get_config_manager, validate_environment
from ..infrastructure.ai_client import create_ai_client
from ..infrastructure.logging_config import setup_default_logging, log_debate_start, log_debate_end
from ..application.debate_service import DebateService
from ..application.character_service import CharacterService
from ..domain.debate.models import DebateSettings
from ..domain.topics import get_default_topics
from .ui.styles import get_css_styles
from .ui.components import (
    render_debate_message, render_competitive_results,
    render_session_summary, render_character_selection
)


class StreamlitDebateApp:
    """Main Streamlit application for AI Political Debate Simulator."""
    
    def __init__(self):
        """Initialize the Streamlit application."""
        # Setup configuration and logging
        self.config_manager = get_config_manager()
        setup_default_logging()
        
        # Validate environment
        validation = validate_environment()
        if not validation["valid"]:
            st.error("Configuration errors found!")
            for error in validation["errors"]:
                st.error(f"❌ {error}")
            st.stop()
        
        # Initialize services
        ai_config = self.config_manager.get_ai_config()
        if ai_config["use_mock"]:
            self.ai_client = create_ai_client("mock")
        else:
            self.ai_client = create_ai_client("openai", api_key=ai_config["api_key"])
        
        self.character_service = CharacterService()
        self.debate_service = DebateService(self.ai_client, self.character_service)
        
        # Setup UI callbacks
        self._setup_callbacks()
        
        # Initialize session state
        self._initialize_session_state()
    
    def _setup_callbacks(self):
        """Setup callbacks for debate events."""
        self.debate_service.register_ui_callback("message_generated", self._on_message_generated)
        self.debate_service.register_ui_callback("round_completed", self._on_round_completed)
        self.debate_service.register_ui_callback("judge_feedback", self._on_judge_feedback)
        self.debate_service.register_ui_callback("session_completed", self._on_session_completed)
        self.debate_service.register_ui_callback("progress_update", self._on_progress_update)
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state."""
        if "debate_running" not in st.session_state:
            st.session_state.debate_running = False
        
        if "debate_messages" not in st.session_state:
            st.session_state.debate_messages = []
        
        if "current_session" not in st.session_state:
            st.session_state.current_session = None
        
        if "participants" not in st.session_state:
            st.session_state.participants = []
    
    def _on_message_generated(self, message, character):
        """Handle message generated callback."""
        st.session_state.debate_messages.append({
            "message": message,
            "character": character,
            "timestamp": datetime.now()
        })
        # Update UI
        self._display_new_message(message, character)
    
    def _on_round_completed(self, round_obj, round_num):
        """Handle round completed callback."""
        st.success(f"Round {round_num} completed!")
    
    def _on_judge_feedback(self, feedback, round_num):
        """Handle judge feedback callback."""
        with st.expander(f"🏆 Round {round_num} Judge Feedback"):
            st.write(f"Judge evaluated {len(feedback)} participants")
    
    def _on_session_completed(self, session):
        """Handle session completed callback."""
        st.session_state.debate_running = False
        st.balloons()
        st.success("🎉 Debate completed successfully!")
    
    def _on_progress_update(self, progress, round_num, speaker):
        """Handle progress update callback."""
        if hasattr(st.session_state, 'progress_bar'):
            st.session_state.progress_bar.progress(progress)
        if hasattr(st.session_state, 'status_text'):
            st.session_state.status_text.text(f"Round {round_num} - {speaker} responding...")
    
    def _display_new_message(self, message, character):
        """Display a new debate message."""
        # This would be called during debate to show real-time updates
        # For now, we'll handle display in the main loop
        pass
    
    def run(self):
        """Run the Streamlit application."""
        # Page configuration
        streamlit_config = self.config_manager.get_streamlit_config()
        st.set_page_config(**streamlit_config)
        
        # Apply custom CSS
        st.markdown(get_css_styles(), unsafe_allow_html=True)
        
        # Render application
        self._render_header()
        self._render_sidebar()
        self._render_main_content()
    
    def _render_header(self):
        """Render the application header."""
        st.markdown(
            '<h1 class="main-header">🤖 AI Political Debate Simulator</h1>',
            unsafe_allow_html=True
        )
    
    def _render_sidebar(self):
        """Render the sidebar configuration."""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # API Status
            self._render_api_status()
            
            # Debate Settings
            self._render_debate_settings()
            
            # Character Selection
            self._render_character_selection_sidebar()
            
            # Controls
            self._render_controls()
            
            # Additional Options
            self._render_additional_options()
    
    def _render_api_status(self):
        """Render API connection status."""
        config = self.config_manager.config
        if config.enable_mock_ai:
            st.success("✅ Mock AI enabled (for testing)")
        elif config.openai_api_key:
            st.success("✅ OpenAI API key configured")
        else:
            st.error("⚠️ OpenAI API key not configured!")
    
    def _render_debate_settings(self):
        """Render debate configuration settings."""
        st.subheader("Debate Settings")
        
        # Topic selection
        topics = get_default_topics()
        topic_option = st.selectbox(
            "Choose debate topic:",
            ["Select a topic..."] + topics
        )
        
        # Custom topic
        custom_topic = st.text_input("Or enter a custom topic:")
        
        # Store selected topic
        if custom_topic:
            st.session_state.selected_topic = custom_topic
        elif topic_option != "Select a topic...":
            st.session_state.selected_topic = topic_option
        else:
            st.session_state.selected_topic = None
        
        # Number of rounds
        st.session_state.rounds = st.slider(
            "Number of rounds:",
            min_value=1,
            max_value=20,
            value=self.config_manager.config.default_rounds
        )
        
        # Response delay
        st.session_state.delay = st.slider(
            "Delay between responses (seconds):",
            min_value=0.0,
            max_value=5.0,
            value=self.config_manager.config.default_delay,
            step=0.5
        )
        
        # Competitive mode
        st.session_state.competitive_mode = st.checkbox(
            "Enable Competitive Mode",
            value=self.config_manager.config.enable_competitive_mode,
            help="Characters have dynamic stats that change based on performance"
        )
    
    def _render_character_selection_sidebar(self):
        """Render character selection in sidebar."""
        st.subheader("🎭 Character Selection")
        
        available_characters = self.character_service.get_available_character_types()
        selected_characters = []
        
        # Default characters
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("🔵 Market Liberal Democrat", value=True):
                selected_characters.append("democratic_commentator")
            if st.checkbox("🔴 MAGA Nationalist", value=True):
                selected_characters.append("republican_commentator")
        
        with col2:
            st.markdown("**Default**")
            st.markdown("*(Recommended)*")
        
        # Additional characters
        st.markdown("**Additional Characters:**")
        
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
        
        for char_type, display_name in additional_chars:
            if st.checkbox(display_name):
                selected_characters.append(char_type)
        
        st.session_state.selected_characters = selected_characters
    
    def _render_controls(self):
        """Render debate control buttons."""
        st.subheader("🎮 Controls")
        
        # Validation
        can_start = (
            st.session_state.get("selected_topic") and
            st.session_state.get("selected_characters") and
            not st.session_state.get("debate_running", False)
        )
        
        # Start debate button
        if st.button("🚀 Start Debate", disabled=not can_start, type="primary"):
            self._start_debate()
        
        # Stop debate button
        if st.session_state.get("debate_running", False):
            if st.button("⏹️ Stop Debate", type="secondary"):
                self._stop_debate()
        
        # Validation messages
        if not can_start and not st.session_state.get("debate_running", False):
            if not st.session_state.get("selected_topic"):
                st.warning("Please select a debate topic")
            if not st.session_state.get("selected_characters"):
                st.warning("Please select at least one character")
    
    def _render_additional_options(self):
        """Render additional options."""
        st.subheader("📁 Session Management")
        
        # Load session
        uploaded_file = st.file_uploader("Upload debate session:", type=["json"])
        if uploaded_file:
            try:
                session_data = json.load(uploaded_file)
                if st.button("📖 Load Session"):
                    self._load_session(session_data)
            except Exception as e:
                st.error(f"Invalid session file: {str(e)}")
        
        # Download current session
        if st.session_state.get("current_session"):
            session_data = self.debate_service.export_session()
            if session_data:
                st.download_button(
                    "💾 Download Session",
                    data=json.dumps(session_data, indent=2),
                    file_name=f"debate_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    def _render_main_content(self):
        """Render the main content area."""
        if st.session_state.get("debate_running"):
            self._render_active_debate()
        elif st.session_state.get("current_session"):
            self._render_completed_debate()
        else:
            self._render_welcome()
    
    def _render_welcome(self):
        """Render welcome screen."""
        st.markdown("""
        ## Welcome to the AI Political Debate Simulator!
        
        This application simulates political debates between AI-powered characters with different ideological perspectives.
        
        ### How to get started:
        1. 📋 Select a debate topic from the sidebar
        2. 🎭 Choose characters to participate
        3. ⚙️ Configure debate settings
        4. 🚀 Start the debate!
        
        ### Features:
        - 🤖 Multiple AI character personalities
        - 🏆 Competitive mode with dynamic stats
        - 💾 Save and load debate sessions
        - 📊 Performance analytics
        """)
    
    def _render_active_debate(self):
        """Render active debate view."""
        st.markdown("## 🎪 Debate in Progress")
        
        # Progress indicators
        st.session_state.progress_bar = st.progress(0)
        st.session_state.status_text = st.empty()
        
        # Debate messages container
        messages_container = st.container()
        
        # Display messages as they come in
        for msg_data in st.session_state.get("debate_messages", []):
            with messages_container:
                render_debate_message(
                    msg_data["message"],
                    msg_data["character"],
                    st.session_state.get("competitive_mode", False)
                )
    
    def _render_completed_debate(self):
        """Render completed debate view."""
        st.markdown("## 📊 Debate Results")
        
        # Session summary
        session_status = self.debate_service.get_session_status()
        render_session_summary(session_status)
        
        # Competitive results
        if st.session_state.get("competitive_mode"):
            competitive_results = self.debate_service.get_competitive_results()
            if competitive_results:
                render_competitive_results(competitive_results)
        
        # Debate transcript
        with st.expander("📝 Full Debate Transcript"):
            for msg_data in st.session_state.get("debate_messages", []):
                render_debate_message(
                    msg_data["message"],
                    msg_data["character"],
                    st.session_state.get("competitive_mode", False)
                )
    
    def _start_debate(self):
        """Start a new debate."""
        try:
            # Create debate settings
            settings = DebateSettings(
                total_rounds=st.session_state.rounds,
                response_delay=st.session_state.delay,
                competitive_mode=st.session_state.competitive_mode
            )
            
            # Create debate session
            session_result = self.debate_service.create_debate_session(
                topic=st.session_state.selected_topic,
                selected_character_types=st.session_state.selected_characters,
                settings=settings
            )
            
            if not session_result["success"]:
                st.error(f"Failed to create debate: {session_result['error']}")
                return
            
            # Store session data
            st.session_state.current_session = session_result["session"]
            st.session_state.participants = session_result["participants"]
            st.session_state.debate_running = True
            st.session_state.debate_messages = []
            
            # Log debate start
            participant_names = [p.name for p in session_result["participants"]]
            log_debate_start(st.session_state.selected_topic, participant_names)
            
            # Start the debate
            start_result = self.debate_service.start_debate(session_result["participants"])
            
            if not start_result["success"]:
                st.error(f"Failed to start debate: {start_result['error']}")
                st.session_state.debate_running = False
                return
            
            # Rerun to update UI
            st.rerun()
            
        except Exception as e:
            st.error(f"Error starting debate: {str(e)}")
            st.session_state.debate_running = False
    
    def _stop_debate(self):
        """Stop the current debate."""
        try:
            result = self.debate_service.stop_debate()
            if result["success"]:
                st.session_state.debate_running = False
                st.success("Debate stopped successfully")
                
                # Log debate end
                if st.session_state.current_session:
                    participant_names = [p.name for p in st.session_state.participants]
                    log_debate_end(
                        st.session_state.current_session.topic,
                        len(st.session_state.debate_messages),
                        participant_names
                    )
                
                st.rerun()
            else:
                st.error(f"Failed to stop debate: {result['error']}")
        except Exception as e:
            st.error(f"Error stopping debate: {str(e)}")
    
    def _load_session(self, session_data):
        """Load a debate session from data."""
        try:
            result = self.debate_service.import_session(session_data)
            if result["success"]:
                st.session_state.current_session = result["session"]
                st.success("Session loaded successfully!")
                st.rerun()
            else:
                st.error(f"Failed to load session: {result['error']}")
        except Exception as e:
            st.error(f"Error loading session: {str(e)}")


def main():
    """Main entry point for the Streamlit application."""
    app = StreamlitDebateApp()
    app.run()


if __name__ == "__main__":
    main()