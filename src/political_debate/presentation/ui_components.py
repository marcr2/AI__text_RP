import streamlit as st
from typing import List, Dict, Any
from ..domain.models import Participant, Message, DebateSession


class UIComponents:
    """UI components for the Streamlit interface"""
    
    @staticmethod
    def inject_css():
        """Inject custom CSS for the debate interface"""
        st.markdown("""
        <style>
        /* Main app styling */
        .main-header {
            text-align: center;
            color: #ffffff;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Message styling base */
        .debate-container {
            animation: fadeIn 0.3s ease-in;
            margin-bottom: 0.3rem;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Democrat message styling */
        .democrat-message {
            background-color: rgba(21, 101, 192, 0.85);
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
        
        /* Additional character message styles */
        .anarcho-message { background-color: rgba(230, 81, 0, 0.85); }
        .catholic-message { background-color: rgba(33, 33, 33, 0.85); }
        .monarchist-message { background-color: rgba(74, 20, 140, 0.85); }
        .islamic-message { background-color: rgba(27, 94, 32, 0.85); }
        .evangelist-message { background-color: rgba(141, 110, 99, 0.85); }
        .master-baiter-message { background-color: rgba(0, 0, 0, 0.85); }
        .chinese-communist-message { background-color: rgba(139, 0, 0, 0.85); }
        
        /* Apply base message styling to all character types */
        .anarcho-message, .catholic-message, .monarchist-message, 
        .islamic-message, .evangelist-message, .master-baiter-message, 
        .chinese-communist-message {
            padding: 0.5rem 0.75rem;
            border-radius: 15px 15px 3px 15px;
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
        
        .anger-bubble { background-color: rgba(255, 0, 0, 0.8); color: white; }
        .patience-bubble { background-color: rgba(0, 255, 0, 0.8); color: white; }
        .uniqueness-bubble { background-color: rgba(0, 0, 255, 0.8); color: white; }
        
        .stat-label {
            font-size: 0.6rem;
            color: rgba(255, 255, 255, 0.7);
            margin-right: 0.2rem;
            font-weight: bold;
        }
        
        /* General styling improvements */
        h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
        p, div, span { color: #ffffff !important; }
        
        /* Button and form styling */
        .stButton > button {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #444444;
        }
        
        .stButton > button:hover {
            background-color: #2d2d2d;
            border: 1px solid #666666;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_message(
        message: Message, 
        participant: Participant, 
        round_number: int,
        competitive_mode: bool = False
    ):
        """Render a single debate message with appropriate styling"""
        
        # Generate stat bubbles for competitive mode
        stat_bubbles_html = ""
        if competitive_mode:
            stat_bubbles_html = f"""
            <div class="stat-bubbles">
                <span class="stat-label">A:</span>
                <div class="stat-bubble anger-bubble">{participant.stats.anger}</div>
                <span class="stat-label">P:</span>
                <div class="stat-bubble patience-bubble">{participant.stats.patience}</div>
                <span class="stat-label">U:</span>
                <div class="stat-bubble uniqueness-bubble">{participant.stats.uniqueness}</div>
            </div>
            """
        
        # Escape HTML in message content
        escaped_content = message.content.replace("<", "&lt;").replace(">", "&gt;")
        
        # Build message HTML
        if participant.position.value == "left":
            html_template = f"""
            <div style="display: flex; justify-content: flex-start;">
                <div class="debate-container">
                    <div class="round-header">Round {round_number}</div>
                    <div class="{participant.message_class}">
                        {stat_bubbles_html}
                        <div class="speaker-name">{participant.emoji} {participant.display_name}</div>
                        {escaped_content}
                    </div>
                </div>
            </div>
            """
        else:
            html_template = f"""
            <div style="display: flex; justify-content: flex-end;">
                <div class="debate-container">
                    <div class="round-header">Round {round_number}</div>
                    <div class="{participant.message_class}">
                        {stat_bubbles_html}
                        <div class="speaker-name">{participant.emoji} {participant.display_name}</div>
                        {escaped_content}
                    </div>
                </div>
            </div>
            """
        
        st.html(html_template)
    
    @staticmethod
    def render_participants_list(participants: List[Participant]):
        """Render the list of debate participants organized by position"""
        
        left_speakers = [p for p in participants if p.position.value == "left"]
        right_speakers = [p for p in participants if p.position.value == "right"]
        
        st.markdown(f"### 🎭 Participants ({len(participants)}):")
        
        # Display left side participants
        if left_speakers:
            st.markdown("**👈 Left Side:**")
            for participant in left_speakers:
                st.markdown(f"  {participant.emoji} **{participant.display_name}** - {participant.role}")
        
        # Display right side participants  
        if right_speakers:
            st.markdown("**👉 Right Side:**")
            for participant in right_speakers:
                st.markdown(f"  {participant.emoji} **{participant.display_name}** - {participant.role}")
    
    @staticmethod
    def render_competitive_results(participants: List[Participant]):
        """Render final competitive mode results"""
        
        st.markdown("## 🏆 Final Competitive Mode Results")
        st.markdown("### 📊 Character Performance Summary:")
        
        for participant in participants:
            anger = participant.stats.anger
            patience = participant.stats.patience
            uniqueness = participant.stats.uniqueness
            
            # Determine performance color
            performance_rating = participant.stats.performance_rating
            if "EXCELLENT" in performance_rating:
                color = "#00FF00"
            elif "GOOD" in performance_rating:
                color = "#FFFF00"  
            elif "AVERAGE" in performance_rating:
                color = "#FFA500"
            else:
                color = "#FF0000"
            
            st.html(f"""
            <div style="background-color: rgba(255, 255, 255, 0.05); padding: 0.5rem; border-radius: 8px; margin: 0.3rem 0;">
                <strong>{participant.display_name}</strong><br>
                Anger: {anger} | Patience: {patience} | Uniqueness: {uniqueness}<br>
                <span style="color: {color}; font-weight: bold;">{performance_rating}</span>
            </div>
            """)
    
    @staticmethod
    def render_judge_feedback(round_number: int, message_count: int):
        """Render judge feedback notification"""
        
        st.html(f"""
        <div style="background-color: rgba(255, 215, 0, 0.1); padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #FFD700;">
            <strong>🏆 Round {round_number} Judge Feedback:</strong><br>
            {message_count} responses evaluated. Stats updated based on performance.
        </div>
        """)
    
    @staticmethod
    def show_character_selection(participant_manager) -> tuple:
        """Show character selection UI and return selected characters"""
        
        characters = participant_manager.get_available_characters()
        selected = []
        
        st.subheader("🎭 Debate Participants")
        st.markdown("Select which characters to include in the debate:")
        
        # Default characters
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("🔵 Market Liberal Democrat", value=True):
                selected.append("democrat")
            if st.checkbox("🔴 MAGA Nationalist", value=True):
                selected.append("republican")
        
        with col2:
            st.markdown("**Default characters**")
            st.markdown("*(Recommended to keep at least one)*")
        
        # Additional characters
        st.markdown("**Additional characters:**")
        col1, col2 = st.columns(2)
        
        additional_chars = characters["additional"]
        char_keys = list(additional_chars.keys())
        mid_point = len(char_keys) // 2
        
        with col1:
            for key in char_keys[:mid_point]:
                char_data = additional_chars[key]
                if st.checkbox(f"{char_data['emoji']} {char_data['name']}"):
                    selected.append(key)
        
        with col2:
            for key in char_keys[mid_point:]:
                char_data = additional_chars[key]
                if st.checkbox(f"{char_data['emoji']} {char_data['name']}"):
                    selected.append(key)
        
        return selected, len(selected) > 0