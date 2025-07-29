import streamlit as st
import time
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from ..application.debate_service import DebateService, ParticipantManager
from .ui_components import UIComponents

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('debate.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StreamlitDebateApp:
    """Main Streamlit application for political debates"""
    
    def __init__(self):
        self.debate_service = None
        self.participant_manager = ParticipantManager()
        self.ui = UIComponents()
        
        # Initialize session state
        if 'debate_running' not in st.session_state:
            st.session_state.debate_running = False
        if 'debate_stopped' not in st.session_state:
            st.session_state.debate_stopped = False
        if 'current_session' not in st.session_state:
            st.session_state.current_session = None
    
    def run(self):
        """Run the Streamlit application"""
        
        # Inject CSS
        self.ui.inject_css()
        
        # Header
        st.markdown(
            '<h1 class="main-header">🤖 AI Political Debate Simulator</h1>',
            unsafe_allow_html=True
        )
        
        # Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            st.error("⚠️ OpenAI API key not configured!")
            st.info("Please set your OPENAI_API_KEY in the .env file")
            st.stop()
        
        # Initialize debate service with API key
        if self.debate_service is None:
            try:
                self.debate_service = DebateService(api_key)
                st.success("✅ OpenAI API key configured")
            except Exception as e:
                st.error(f"❌ Failed to initialize debate service: {str(e)}")
                st.stop()
        
        # Sidebar configuration
        self._render_sidebar()
        
        # Main content
        self._render_main_content()
    
    def _render_sidebar(self):
        """Render the sidebar configuration"""
        
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Debate settings
            st.subheader("Debate Settings")
            
            # Topic selection
            topics = self.debate_service.get_available_topics()
            topic_option = st.selectbox(
                "Choose debate topic:", 
                ["Select a topic..."] + topics
            )
            
            # Custom topic input
            custom_topic = st.text_input("Or enter a custom topic:")
            
            # Number of rounds
            rounds = st.slider("Number of rounds:", min_value=1, max_value=20, value=5)
            
            # Delay between responses
            delay = st.slider(
                "Delay between responses (seconds):",
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=0.5
            )
            
            # Competitive mode toggle
            st.subheader("🏆 Competitive Mode")
            competitive_mode = st.checkbox(
                "Enable Competitive Mode",
                value=False,
                help="Characters have dynamic stats that change based on their performance."
            )
            
            if competitive_mode:
                st.info("🎯 In competitive mode, characters' stats change based on AI judge feedback!")
            
            # Character selection
            selected_characters, has_selection = self.ui.show_character_selection(
                self.participant_manager
            )
            
            # Start debate button
            start_debate = st.button("🚀 Start Debate", type="primary")
            
            # Stop debate button
            if st.session_state.get("debate_running", False):
                if st.button("⏹️ Stop Debate", type="secondary"):
                    st.session_state.debate_running = False
                    st.session_state.debate_stopped = True
                    st.rerun()
            
            # Store configuration in session state
            st.session_state.config = {
                'topic_option': topic_option,
                'custom_topic': custom_topic,
                'rounds': rounds,
                'delay': delay,
                'competitive_mode': competitive_mode,
                'selected_characters': selected_characters,
                'has_selection': has_selection,
                'start_debate': start_debate
            }
            
            # Load previous session
            self._render_session_loader()
            
            # Donation section
            self._render_donation_section()
            
            # Debug options
            self._render_debug_options()
    
    def _render_main_content(self):
        """Render the main content area"""
        
        config = st.session_state.get('config', {})
        
        if config.get('start_debate', False):
            self._start_debate(config)
        
        # Display current session if running
        if st.session_state.get('current_session'):
            self._display_debate_session()
    
    def _start_debate(self, config):
        """Start a new debate session"""
        
        # Validate inputs
        topic = config.get('custom_topic') if config.get('custom_topic') else config.get('topic_option')
        
        if topic == "Select a topic..." or not topic:
            st.error("Please select a topic or enter a custom topic!")
            return
        
        if not config.get('has_selection', False):
            st.error("❌ Please select at least one character to participate in the debate!")
            return
        
        try:
            # Create debate session
            session = self.debate_service.create_debate_session(
                topic=topic,
                selected_characters=config['selected_characters'],
                rounds=config['rounds'],
                competitive_mode=config['competitive_mode']
            )
            
            # Store in session state
            st.session_state.current_session = session
            st.session_state.debate_running = True
            st.session_state.debate_stopped = False
            st.session_state.current_round = 1
            st.session_state.config = config  # Store config for the debate
            
            logger.info(f"Started debate: {topic} with {len(session.participants)} participants")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Failed to start debate: {str(e)}")
            logger.error(f"Failed to start debate: {str(e)}")
    
    def _display_debate_session(self):
        """Display the current debate session"""
        
        session = st.session_state.current_session
        config = st.session_state.get('config', {})
        
        if not session:
            return
        
        # Display topic and participants
        st.markdown(f"## 📋 Debate Topic: {session.topic}")
        self.ui.render_participants_list(session.participants)
        st.markdown("---")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Conduct debate rounds
        if st.session_state.debate_running and not st.session_state.debate_stopped:
            current_round = st.session_state.get('current_round', 1)
            
            while current_round <= session.rounds and not st.session_state.debate_stopped:
                # Update progress
                progress = (current_round - 1) / session.rounds
                progress_bar.progress(progress)
                status_text.text(f"Conducting Round {current_round}/{session.rounds}...")
                
                try:
                    # Conduct round
                    round_messages = self.debate_service.conduct_round(
                        session, 
                        current_round
                    )
                    
                    # Display messages
                    for message in round_messages:
                        # Find participant
                        participant = next(
                            (p for p in session.participants if p.name == message.speaker_name),
                            None
                        )
                        
                        if participant:
                            self.ui.render_message(
                                message, 
                                participant, 
                                current_round,
                                session.competitive_mode
                            )
                            
                            # Add delay
                            time.sleep(config.get('delay', 1.0))
                    
                    # Show judge feedback for competitive mode
                    if session.competitive_mode and round_messages:
                        self.ui.render_judge_feedback(current_round, len(round_messages))
                    
                    # Move to next round
                    current_round += 1
                    st.session_state.current_round = current_round
                    
                except Exception as e:
                    st.error(f"❌ Error in round {current_round}: {str(e)}")
                    logger.error(f"Error in round {current_round}: {str(e)}")
                    break
            
            # Complete or stopped
            if not st.session_state.debate_stopped:
                progress_bar.progress(1.0)
                status_text.text("✅ Debate complete!")
                
                # Show competitive results
                if session.competitive_mode:
                    self.ui.render_competitive_results(session.participants)
            else:
                status_text.text("⏹️ Debate stopped by user")
            
            # Reset debate state
            st.session_state.debate_running = False
            
            # Offer session download
            self._offer_session_download(session)
    
    def _offer_session_download(self, session):
        """Offer session download"""
        
        session_data = session.to_dict()
        
        st.download_button(
            label="💾 Download Debate Session",
            data=json.dumps(session_data, indent=2),
            file_name=f"political_debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def _render_session_loader(self):
        """Render session loader section"""
        
        st.subheader("📁 Load Previous Session")
        uploaded_file = st.file_uploader(
            "Upload a debate session (JSON):", 
            type=["json"]
        )
        
        if uploaded_file is not None:
            try:
                session_data = json.load(uploaded_file)
                st.success("✅ Session loaded successfully!")
                
                if st.button("📖 View Session"):
                    # Display session data (simplified)
                    st.json(session_data)
                    
            except Exception as e:
                st.error(f"❌ Invalid JSON file: {str(e)}")
    
    def _render_donation_section(self):
        """Render donation section"""
        
        st.markdown("---")
        st.markdown("""
        <div style="background-color: rgba(255, 215, 0, 0.05); padding: 0.5rem; border-radius: 8px; border: 1px solid rgba(255, 215, 0, 0.2); margin: 0.5rem 0;">
            <h4>☕ Support the Project</h4>
            <p>If you enjoy this AI debate simulator, consider buying me a coffee!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <a href="https://ko-fi.com/marcellinorau" target="_blank">
            <img height="36" style="border:0px;height:36px;" src="https://storage.ko-fi.com/cdn/kofi2.png?v=3" border="0" alt="Buy Me a Coffee at ko-fi.com" />
        </a>
        """, unsafe_allow_html=True)
    
    def _render_debug_options(self):
        """Render debug options"""
        
        st.markdown("---")
        enable_debug = st.checkbox(
            "Enable debug logging",
            value=False,
            help="Log all requests and responses to debug file"
        )
        
        if enable_debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        
        st.markdown(f"**Current log level:** {logging.getLevelName(logging.getLogger().level)}")


def main():
    """Main entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="AI Political Debate Simulator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run application
    app = StreamlitDebateApp()
    app.run()


if __name__ == "__main__":
    main()