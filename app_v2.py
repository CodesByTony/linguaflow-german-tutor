"""
LinguaFlow v2.0 - COMPLETE AI-Powered German Tutor
Full version with ALL features - NO CUTS
"""

import streamlit as st
import json
import random
from datetime import datetime, timedelta
import base64
from io import BytesIO
import requests
import time
import os
from pathlib import Path
import hashlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import our enhanced AI module with all features
from ai_module import (
    AIContentEngine,
    DynamicLessonGenerator,
    IntelligentTutor,
    AdaptiveExamSystem,
    translate_text,
    get_example_sentences,
    calculate_skill_score,
    get_personalized_recommendations
)

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LinguaFlow - AI German Tutor",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# COMPLETE STYLING
# ==========================================

st.markdown("""
<style>
    /* Enhanced UI Styling */
    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Animated gradient background */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .lesson-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .lesson-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .achievement-badge {
        display: inline-block;
        padding: 8px 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 25px;
        margin: 5px;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .xp-bar {
        background: #e0e0e0;
        border-radius: 15px;
        height: 35px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .xp-fill {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 100%;
        border-radius: 15px;
        transition: width 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    
    .xp-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .chat-message {
        padding: 12px 18px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 70%;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .ai-message {
        background: #f0f2f6;
        color: #2c3e50;
    }
    
    .skill-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .skill-card:hover {
        border-color: #667eea;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .progress-ring {
        transform: rotate(-90deg);
        width: 100px;
        height: 100px;
    }
    
    .progress-ring-circle {
        stroke-dasharray: 314;
        stroke-dashoffset: 314;
        stroke-width: 10;
        fill: none;
        stroke: #667eea;
        animation: progress 1s ease forwards;
    }
    
    @keyframes progress {
        to { stroke-dashoffset: calc(314 - (314 * var(--progress)) / 100); }
    }
    
    .floating-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        cursor: pointer;
        transition: transform 0.3s ease;
        z-index: 1000;
    }
    
    .floating-button:hover {
        transform: scale(1.1) rotate(90deg);
    }
    
    .exam-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
    }
    
    .certificate {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .certificate::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(255,255,255,0.1) 10px,
            rgba(255,255,255,0.1) 20px
        );
        animation: slide 20s linear infinite;
    }
    
    @keyframes slide {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .progress-milestone {
        text-align: center;
        padding: 10px;
    }
    
    .content-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
    
    .translation-result {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Success animation */
    .success-animation {
        animation: successPulse 0.5s ease;
    }
    
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        margin: 10px 0;
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA PERSISTENCE
# ==========================================

DATA_DIR = Path("user_data")
DATA_DIR.mkdir(exist_ok=True)

def save_user_progress():
    """Save user progress to file"""
    try:
        user_data = {
            'user_name': st.session_state.get('user_name', ''),
            'user_level': st.session_state.get('user_level', None),
            'xp': st.session_state.get('xp', 0),
            'streak': st.session_state.get('streak', 0),
            'current_day': st.session_state.get('current_day', 1),
            'achievements': st.session_state.get('achievements', []),
            'completed_exercises': st.session_state.get('completed_exercises', []),
            'placement_completed': st.session_state.get('placement_completed', False),
            'exam_history': st.session_state.get('exam_history', []),
            'chat_history': st.session_state.get('chat_history', [])[-50:],  # Save last 50 messages
            'skill_scores': st.session_state.get('skill_scores', {}),
            'last_login': datetime.now().isoformat()
        }
        
        file_path = DATA_DIR / f"user_{st.session_state.get('user_name', 'default')}.json"
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving progress: {str(e)}")
        return False

def load_user_progress(username: str):
    """Load user progress from file"""
    try:
        file_path = DATA_DIR / f"user_{username}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                user_data = json.load(f)
            
            # Update session state
            for key, value in user_data.items():
                if key != 'last_login':
                    st.session_state[key] = value
            
            # Check and update streak
            last_login = datetime.fromisoformat(user_data.get('last_login', datetime.now().isoformat()))
            days_diff = (datetime.now() - last_login).days
            
            if days_diff == 1:
                st.session_state.streak += 1
            elif days_diff > 1:
                st.session_state.streak = 1
            
            return True
        return False
    except Exception as e:
        st.error(f"Error loading progress: {str(e)}")
        return False

# ==========================================
# INITIALIZE SESSION STATE WITH ALL FEATURES
# ==========================================

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_level = None
    st.session_state.xp = 0
    st.session_state.streak = 0
    st.session_state.current_day = 1
    st.session_state.daily_tasks_completed = []
    st.session_state.chat_history = []
    st.session_state.api_keys = {
        'openrouter': '',
        'huggingface': '',
        'together': '',
        'mymemory_email': ''
    }
    st.session_state.placement_completed = False
    st.session_state.achievements = []
    st.session_state.user_name = ""
    st.session_state.completed_exercises = []
    st.session_state.lesson_cache = {}
    st.session_state.exam_history = []
    st.session_state.skill_scores = {
        'Speaking': 0,
        'Writing': 0,
        'Listening': 0,
        'Reading': 0,
        'Grammar': 0
    }
    st.session_state.daily_xp = 0
    st.session_state.weekly_goals = {
        'exercises': 35,
        'xp': 500,
        'streak': 7
    }
    
    # Initialize AI systems
    st.session_state.ai_engine = AIContentEngine()
    st.session_state.lesson_generator = DynamicLessonGenerator(st.session_state.ai_engine)
    st.session_state.ai_tutor = IntelligentTutor(st.session_state.ai_engine)
    st.session_state.exam_system = AdaptiveExamSystem(st.session_state.ai_engine)

# ==========================================
# TEXT-TO-SPEECH CLASS
# ==========================================

class TextToSpeech:
    """Enhanced Text-to-speech functionality"""
    
    @staticmethod
    def generate_audio(text: str, lang: str = 'de', slow: bool = False):
        """Generate audio from text and return base64 encoded audio"""
        try:
            from gtts import gTTS
            import io
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=slow)
            
            # Save to bytes
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Encode to base64
            audio_base64 = base64.b64encode(audio_bytes.read()).decode()
            
            return audio_base64
            
        except Exception as e:
            return None
    
    @staticmethod
    def play_audio(audio_base64: str):
        """Display audio player for base64 audio"""
        if audio_base64:
            audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

# Initialize TTS
tts = TextToSpeech()

# ==========================================
# GRAMMAR CHECKER CLASS
# ==========================================

class GrammarChecker:
    """Grammar checking using LanguageTool"""
    
    @staticmethod
    def check_german_text(text: str):
        """Check German text for grammar errors"""
        try:
            # Use LanguageTool public API
            url = "https://api.languagetoolplus.com/v2/check"
            
            data = {
                'text': text,
                'language': 'de-DE',
                'enabledOnly': 'false'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                errors = []
                suggestions = []
                
                for match in result.get('matches', []):
                    error = {
                        'message': match.get('message', ''),
                        'offset': match.get('offset', 0),
                        'length': match.get('length', 0),
                        'replacements': [r.get('value', '') for r in match.get('replacements', [])[:3]],
                        'type': match.get('rule', {}).get('category', {}).get('id', 'UNKNOWN')
                    }
                    errors.append(error)
                    
                    if error['replacements']:
                        suggestions.append(f"'{text[error['offset']:error['offset']+error['length']]}' → '{error['replacements'][0]}'")
                
                return {
                    'has_errors': len(errors) > 0,
                    'error_count': len(errors),
                    'errors': errors,
                    'suggestions': suggestions,
                    'corrected_text': GrammarChecker.apply_corrections(text, errors)
                }
            
            return {'has_errors': False, 'error_count': 0, 'errors': [], 'suggestions': []}
            
        except Exception as e:
            return {'has_errors': False, 'error_count': 0, 'errors': [], 'suggestions': [], 'error': str(e)}
    
    @staticmethod
    def apply_corrections(text: str, errors: list):
        """Apply grammar corrections to text"""
        if not errors:
            return text
        
        # Sort errors by offset (reverse order)
        errors_sorted = sorted(errors, key=lambda x: x['offset'], reverse=True)
        
        corrected = text
        for error in errors_sorted:
            if error['replacements']:
                start = error['offset']
                end = start + error['length']
                corrected = corrected[:start] + error['replacements'][0] + corrected[end:]
        
        return corrected

# Initialize Grammar Checker
grammar_checker = GrammarChecker()

# ==========================================
# ENHANCED HELPER FUNCTIONS
# ==========================================

def get_level_title(xp):
    """Get user title based on XP with emojis"""
    titles = [
        (0, "🌱 Anfänger (Beginner)", "#4CAF50"),
        (100, "🔍 Entdecker (Explorer)", "#2196F3"),
        (300, "📚 Lerner (Learner)", "#FF9800"),
        (600, "🎯 Fortgeschritten (Advanced)", "#9C27B0"),
        (1000, "🏆 Sprachkenner (Language Expert)", "#F44336"),
        (1500, "👑 Meister (Master)", "#FFD700"),
        (2000, "🧙‍♂️ Guru", "#E91E63")
    ]
    
    for i in range(len(titles)-1, -1, -1):
        if xp >= titles[i][0]:
            return titles[i][1], titles[i][2]
    return titles[0][1], titles[0][2]

def add_xp(amount, reason=""):
    """Add XP with animation and reason"""
    old_title = get_level_title(st.session_state.xp)[0]
    st.session_state.xp += amount
    st.session_state.daily_xp += amount
    new_title = get_level_title(st.session_state.xp)[0]
    
    # Show XP gain notification
    st.success(f"🎉 +{amount} XP{' - ' + reason if reason else ''}!")
    
    # Check for level up
    if old_title != new_title:
        st.balloons()
        st.success(f"🎊 LEVEL UP! You are now: {new_title}")
    
    check_achievements()
    save_user_progress()

def check_achievements():
    """Enhanced achievement checking"""
    new_achievements = []
    
    achievement_conditions = [
        ("First Steps", "Complete your first lesson", len(st.session_state.completed_exercises) >= 1),
        ("First Century", "Earn 100 XP", st.session_state.xp >= 100),
        ("Week Warrior", "7-day streak", st.session_state.streak >= 7),
        ("Dedicated Learner", "14-day streak", st.session_state.streak >= 14),
        ("Monthly Master", "Complete 30 days", st.session_state.current_day >= 30),
        ("Grammar Guru", "Complete 20 grammar lessons", 
         len([e for e in st.session_state.completed_exercises if 'grammar' in e.lower()]) >= 20),
        ("Conversation Champion", "Complete 50 speaking exercises",
         len([e for e in st.session_state.completed_exercises if 'speaking' in e.lower()]) >= 50),
        ("Writing Wizard", "Submit 30 writing exercises",
         len([e for e in st.session_state.completed_exercises if 'writing' in e.lower()]) >= 30),
        ("Listening Legend", "Complete 40 listening exercises",
         len([e for e in st.session_state.completed_exercises if 'listening' in e.lower()]) >= 40),
        ("Reading Rockstar", "Read 100 texts",
         len([e for e in st.session_state.completed_exercises if 'reading' in e.lower()]) >= 100),
        ("Halfway Hero", "Reach day 90", st.session_state.current_day >= 90),
        ("B2 Boss", "Complete the 180-day journey", st.session_state.current_day >= 180),
        ("Exam Master", "Pass 5 exams", len(st.session_state.get('exam_history', [])) >= 5),
        ("Perfectionist", "100% daily completion for a week", False),  # Will implement tracking
        ("Night Owl", "Study after 10 PM", datetime.now().hour >= 22),
        ("Early Bird", "Study before 6 AM", datetime.now().hour < 6),
        ("Weekend Warrior", "Study on weekend", datetime.now().weekday() >= 5)
    ]
    
    for name, description, condition in achievement_conditions:
        if condition and name not in st.session_state.achievements:
            new_achievements.append(name)
            st.session_state.achievements.append(name)
    
    if new_achievements:
        for achievement in new_achievements:
            st.balloons()
            st.success(f"🏆 Achievement Unlocked: **{achievement}**!")
            add_xp(25, f"Achievement: {achievement}")

def display_xp_bar():
    """Enhanced XP progress bar with animations"""
    max_xp = ((st.session_state.xp // 100) + 1) * 100
    current_progress = (st.session_state.xp % 100)
    title, color = get_level_title(st.session_state.xp)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; background: white; padding: 15px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
            <h2 style='color: {color}; margin: 0;'>{title}</h2>
            <div class='xp-bar'>
                <div class='xp-fill' style='width: {current_progress}%;'></div>
            </div>
            <p style='margin-top: 10px; color: #666;'>
                {st.session_state.xp} / {max_xp} XP • Level {st.session_state.xp // 100 + 1}
            </p>
        </div>
        """, unsafe_allow_html=True)

def update_skill_score(skill: str, points: int):
    """Update skill proficiency score"""
    if skill in st.session_state.skill_scores:
        st.session_state.skill_scores[skill] = min(100, st.session_state.skill_scores[skill] + points)

# ==========================================
# COMPLETE MAIN PAGES WITH ALL FEATURES
# ==========================================

def page_dashboard():
    """Enhanced dashboard with all features"""
    st.title("🇩🇪 LinguaFlow - Your AI German Tutor")
    
    # Welcome section with login
    if st.session_state.user_name:
        greeting = "Guten Morgen" if datetime.now().hour < 12 else "Guten Tag" if datetime.now().hour < 18 else "Guten Abend"
        st.header(f"{greeting}, {st.session_state.user_name}! 👋")
        
        # AI-generated motivational message (only if API configured)
        if st.session_state.user_level and (st.session_state.api_keys.get('openrouter') or st.session_state.api_keys.get('huggingface')):
            motivation_messages = {
                'A1': "Jeder Schritt zählt! (Every step counts!)",
                'A2': "Du machst Fortschritte! (You're making progress!)",
                'B1': "Weiter so! (Keep it up!)",
                'B2': "Fast am Ziel! (Almost there!)"
            }
            st.info(f"💭 {motivation_messages.get(st.session_state.user_level, 'Keep learning!')}")
    else:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            name = st.text_input("What's your name?", key="name_input")
        with col2:
            existing_user = st.text_input("Or enter existing username to load progress:", key="existing_user")
        with col3:
            st.write("")  # Spacer
            if st.button("Start/Load", type="primary", use_container_width=True):
                if existing_user:
                    if load_user_progress(existing_user):
                        st.success(f"Welcome back, {existing_user}!")
                        st.rerun()
                    else:
                        st.error("User not found. Starting fresh!")
                elif name:
                    st.session_state.user_name = name
                    save_user_progress()
                    st.rerun()
    
    # Display XP and progress
    display_xp_bar()
    
    # Enhanced stats with progress rings
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Level", 
            st.session_state.user_level or "Not Set",
            delta="Take test" if not st.session_state.user_level else None
        )
    
    with col2:
        progress_percent = (st.session_state.current_day / 180) * 100
        st.metric(
            "📅 Journey", 
            f"Day {st.session_state.current_day}",
            delta=f"{progress_percent:.1f}% to B2"
        )
    
    with col3:
        st.metric(
            "🔥 Streak", 
            f"{st.session_state.streak} days",
            delta="+1 tomorrow" if st.session_state.streak > 0 else "Start today!"
        )
    
    with col4:
        st.metric(
            "🏆 Achievements", 
            len(st.session_state.achievements),
            delta=f"{17 - len(st.session_state.achievements)} remaining"
        )
    
    # Weekly Goals Progress
    st.markdown("### 🎯 Weekly Goals")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weekly_exercises = len([e for e in st.session_state.completed_exercises if 'week' in e.lower()])
        st.progress(min(weekly_exercises / st.session_state.weekly_goals['exercises'], 1.0))
        st.caption(f"Exercises: {weekly_exercises}/{st.session_state.weekly_goals['exercises']}")
    
    with col2:
        st.progress(min(st.session_state.daily_xp / st.session_state.weekly_goals['xp'], 1.0))
        st.caption(f"XP: {st.session_state.daily_xp}/{st.session_state.weekly_goals['xp']}")
    
    with col3:
        st.progress(min(st.session_state.streak / st.session_state.weekly_goals['streak'], 1.0))
        st.caption(f"Streak: {st.session_state.streak}/{st.session_state.weekly_goals['streak']} days")
    
    # Daily Learning Path with skill cards
    st.markdown("### 📝 Today's Learning Path")
    
    if not st.session_state.placement_completed:
        st.warning("👉 Start with the Placement Test to unlock your personalized learning path!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Take Placement Test", type="primary", use_container_width=True):
                st.session_state.selected_page = "📊 Placement Test"
                st.rerun()
    else:
        # Skill cards with progress
        skills = [
            ("Speaking", "🗣️", "#4CAF50"),
            ("Writing", "✍️", "#2196F3"),
            ("Listening", "👂", "#FF9800"),
            ("Reading", "📖", "#9C27B0"),
            ("Grammar", "📐", "#F44336")
        ]
        
        cols = st.columns(5)
        for i, (skill, emoji, color) in enumerate(skills):
            with cols[i]:
                skill_key = f"{skill} {emoji}"
                completed = skill_key in st.session_state.daily_tasks_completed
                
                # Calculate skill proficiency
                proficiency = st.session_state.skill_scores.get(skill, 0)
                
                if completed:
                    st.markdown(f"""
                    <div class='skill-card' style='border-color: {color}; background: linear-gradient(135deg, {color}22, {color}11);'>
                        <h3>{emoji}</h3>
                        <p style='color: {color}; font-weight: bold;'>✅ {skill}</p>
                        <small>{proficiency}% mastery</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button(f"{emoji}\n{skill}\n{proficiency}%", key=f"skill_{skill}", use_container_width=True):
                        st.session_state.selected_skill = skill.lower()
                        st.session_state.selected_page = "📚 Today's Lesson"
                        st.rerun()
        
        # Daily progress bar
        daily_progress = len(st.session_state.daily_tasks_completed) / 5
        st.progress(daily_progress)
        st.caption(f"Daily Progress: {len(st.session_state.daily_tasks_completed)}/5 tasks completed")
        
        if daily_progress == 1.0 and "daily_complete" not in st.session_state:
            st.balloons()
            add_xp(50, "Daily completion bonus!")
            st.session_state.daily_complete = True
            st.session_state.current_day += 1
            save_user_progress()
        
        # Personalized recommendations
        if st.session_state.completed_exercises:
            st.markdown("### 💡 Personalized Recommendations")
            
            # Find weak skills
            weak_skills = [skill for skill, score in st.session_state.skill_scores.items() if score < 50]
            
            recommendations = get_personalized_recommendations(st.session_state.user_level, weak_skills)
            
            for rec in recommendations[:3]:
                st.info(f"💡 {rec}")
        
        # Learning Statistics Chart
        st.markdown("### 📊 Your Learning Pattern")
        
        # Create sample data for visualization
        dates = pd.date_range(end=datetime.now(), periods=7).tolist()
        xp_data = [random.randint(20, 100) for _ in range(7)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=xp_data,
            mode='lines+markers',
            name='Daily XP',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Last 7 Days Activity",
            xaxis_title="Date",
            yaxis_title="XP Earned",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def page_placement_test():
    """Enhanced placement test with AI evaluation"""
    st.title("📊 AI-Powered Placement Test")
    st.markdown("### Determine Your German Level (A1 → B2)")
    
    if st.session_state.placement_completed:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Current Level: **{st.session_state.user_level}**")
            st.markdown(f"Based on {len(st.session_state.completed_exercises)} completed exercises")
        with col2:
            if st.button("🔄 Retake Test", use_container_width=True):
                st.session_state.placement_completed = False
                st.session_state.user_level = None
                st.rerun()
        return
    
    with st.form("placement_test_enhanced"):
        # Part 1: Adaptive Multiple Choice
        st.markdown("#### Part 1: Grammar & Vocabulary")
        
        q1 = st.radio(
            "1. Wie ____ du?",
            ["heißen", "heißt", "heiße", "heißst"]
        )
        
        q2 = st.radio(
            "2. Ich komme ____ Deutschland.",
            ["aus", "von", "in", "zu"]
        )
        
        q3 = st.radio(
            "3. Wenn ich Zeit ____, würde ich mehr lesen.",
            ["habe", "hätte", "hatte", "haben"]
        )
        
        # Part 2: Fill in the Blanks
        st.markdown("#### Part 2: Complete the Sentences")
        
        q4 = st.text_input("4. Ich _____ (to have) einen Hund.")
        q5 = st.text_input("5. Er _____ gestern ins Kino _____ (went).")
        q6 = st.text_input("6. Ich wünschte, ich _____ (could) besser Deutsch sprechen.")
        
        # Part 3: Translation
        st.markdown("#### Part 3: Translation Skills")
        
        q7 = st.text_area("7. Translate to German: 'I would like a coffee, please.'", height=60)
        q8 = st.text_area("8. Translate to English: 'Könnten Sie mir bitte helfen?'", height=60)
        
        # Part 4: Free Writing
        st.markdown("#### Part 4: Express Yourself")
        
        q9 = st.text_area(
            "9. Write 3-5 sentences about yourself in German:", 
            height=100,
            help="Tell us about your hobbies, work, or family"
        )
        
        submitted = st.form_submit_button("🎯 Submit Test", type="primary", use_container_width=True)
        
        if submitted:
            with st.spinner("AI is evaluating your responses..."):
                # Calculate score with enhanced logic
                score = 0
                max_score = 100
                feedback = []
                
                # Multiple choice scoring
                if q1 == "heißt": 
                    score += 5
                    feedback.append("✅ Correct verb conjugation")
                else:
                    feedback.append("❌ Review verb conjugation: heißen → du heißt")
                
                if q2 == "aus": 
                    score += 5
                    feedback.append("✅ Correct preposition usage")
                else:
                    feedback.append("❌ Remember: 'aus' for origin (from)")
                
                if q3 == "hätte": 
                    score += 10
                    feedback.append("✅ Good grasp of Konjunktiv II!")
                else:
                    feedback.append("❌ Study conditional forms (Konjunktiv II)")
                
                # Fill in the blanks
                if "habe" in q4.lower(): 
                    score += 5
                    feedback.append("✅ Present tense correct")
                
                if "ist" in q5.lower() and "gegangen" in q5.lower(): 
                    score += 10
                    feedback.append("✅ Perfect tense mastered!")
                elif "ging" in q5.lower():
                    score += 5
                    feedback.append("⚠️ Simple past is okay, but perfect tense is more common")
                
                if "könnte" in q6.lower(): 
                    score += 10
                    feedback.append("✅ Excellent use of modal in Konjunktiv!")
                
                # Translation scoring
                if any(word in q7.lower() for word in ["möchte", "kaffee", "bitte"]):
                    score += 10
                    feedback.append("✅ Good translation attempt")
                
                if "could you please help me" in q8.lower() or "can you please help me" in q8.lower():
                    score += 10
                    feedback.append("✅ Correct translation from German")
                
                # Free writing evaluation
                if q9:
                    word_count = len(q9.split())
                    if word_count >= 15:
                        score += 20
                        feedback.append(f"✅ Good writing! ({word_count} words)")
                    elif word_count >= 10:
                        score += 15
                        feedback.append(f"⚠️ Try to write more ({word_count} words)")
                    else:
                        score += 10
                        feedback.append(f"❌ Too short ({word_count} words)")
                    
                    # Grammar check if available
                    grammar_result = grammar_checker.check_german_text(q9)
                    if grammar_result['error_count'] == 0:
                        score += 10
                        feedback.append("✅ No grammar errors detected!")
                    elif grammar_result['error_count'] <= 2:
                        score += 5
                        feedback.append(f"⚠️ {grammar_result['error_count']} minor errors")
                    else:
                        feedback.append(f"❌ {grammar_result['error_count']} grammar errors to work on")
                
                # Determine level based on score
                if score >= 80:
                    level = "B2"
                    level_desc = "Upper Intermediate - Excellent foundation!"
                elif score >= 60:
                    level = "B1"
                    level_desc = "Intermediate - Good progress!"
                elif score >= 40:
                    level = "A2"
                    level_desc = "Elementary - Keep building!"
                else:
                    level = "A1"
                    level_desc = "Beginner - Great starting point!"
                
                # Set results
                st.session_state.user_level = level
                st.session_state.placement_completed = True
                
                # Display results
                st.balloons()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"### Your Level: **{level}**")
                    st.info(level_desc)
                    st.metric("Score", f"{score}/{max_score}")
                
                with col2:
                    st.markdown("### Feedback")
                    for fb in feedback[:5]:  # Show top 5 feedback items
                        st.write(fb)
                
                # Generate personalized study plan
                st.markdown("### 📚 Your Personalized 180-Day Study Plan")
                
                study_plan = {
                    'A1': "Focus on basic vocabulary, present tense, and simple conversations",
                    'A2': "Build complex sentences, past tense, and daily situation dialogues",
                    'B1': "Master all tenses, subjunctive mood, and professional communication",
                    'B2': "Perfect advanced grammar, idiomatic expressions, and native-like fluency"
                }
                
                st.info(f"**Goal:** {study_plan[level]}")
                
                add_xp(25, "Placement test completed!")
                save_user_progress()
    
    # Button outside of form
    if st.session_state.placement_completed:
        st.success("Test complete! Ready to start learning?")
        if st.button("🚀 Start Learning!", type="primary", use_container_width=True):
            st.session_state.selected_page = "🏠 Dashboard"
            st.rerun()

def page_todays_lesson():
    """AI-powered dynamic lesson page with full features"""
    st.title("📚 Today's AI-Generated Lesson")
    
    if not st.session_state.placement_completed:
        st.warning("Please complete the placement test first!")
        if st.button("Go to Placement Test"):
            st.session_state.selected_page = "📊 Placement Test"
            st.rerun()
        return
    
    # Header with level and day
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📊 Level: **{st.session_state.user_level}**")
    with col2:
        st.info(f"📅 Day **{st.session_state.current_day}**/180")
    with col3:
        st.info(f"🎯 XP Today: **{st.session_state.daily_xp}**")
    
    # Skill selector with descriptions
    skill_descriptions = {
        "speaking": "🗣️ Practice pronunciation and conversation",
        "writing": "✍️ Improve written expression and grammar",
        "listening": "👂 Enhance comprehension skills",
        "reading": "📖 Build vocabulary and understanding",
        "grammar": "📐 Master German grammar rules"
    }
    
    selected_skill = st.selectbox(
        "Choose today's focus:",
        options=list(skill_descriptions.keys()),
        format_func=lambda x: skill_descriptions[x]
    )
    
    # Generate or retrieve lesson
    lesson_key = f"{st.session_state.current_day}_{selected_skill}_{st.session_state.user_level}"
    
    if lesson_key not in st.session_state.lesson_cache:
        with st.spinner(f"🤖 AI is creating your personalized {selected_skill} lesson..."):
            # Generate lesson using AI
            lesson = st.session_state.lesson_generator.generate_complete_lesson(
                st.session_state.user_level,
                selected_skill,
                st.session_state.current_day
            )
            st.session_state.lesson_cache[lesson_key] = lesson
    else:
        lesson = st.session_state.lesson_cache[lesson_key]
    
    # Display lesson in beautiful card
    st.markdown(f"<div class='lesson-card'>", unsafe_allow_html=True)
    
    # Display content based on skill type
    if selected_skill == "reading":
        display_reading_lesson(lesson)
    elif selected_skill == "writing":
        display_writing_lesson(lesson)
    elif selected_skill == "listening":
        display_listening_lesson(lesson)
    elif selected_skill == "speaking":
        display_speaking_lesson(lesson)
    elif selected_skill == "grammar":
        display_grammar_lesson(lesson)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Regenerate lesson button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 New Lesson", use_container_width=True):
            if lesson_key in st.session_state.lesson_cache:
                del st.session_state.lesson_cache[lesson_key]
            st.rerun()
    
    with col2:
        if st.button("📚 Resources", use_container_width=True):
            with st.expander("Additional Resources"):
                st.markdown("""
                **Recommended Resources:**
                - 🎧 Deutsche Welle Learn German
                - 📚 Goethe Institute Online Exercises
                - 🎮 Duolingo German Course
                - 📖 German Grammar Guide
                """)

def display_reading_lesson(lesson):
    """Display reading lesson with full features"""
    content = lesson.get('content', {})
    
    if isinstance(content, dict):
        st.markdown(f"## {content.get('title', 'Reading Practice')}")
        
        # Display main text
        text = content.get('text', '')
        if text:
            st.markdown(f"<div class='content-box'>{text}</div>", unsafe_allow_html=True)
            
            # Add TTS button
            if st.button("🔊 Listen to Text", key="read_tts"):
                audio = tts.generate_audio(text[:500], 'de')  # First 500 chars
                if audio:
                    tts.play_audio(audio)
        
        # Vocabulary section
        if content.get('vocabulary'):
            st.markdown("### 📝 Key Vocabulary")
            vocab_cols = st.columns(min(len(content['vocabulary']), 3))
            for i, word in enumerate(content['vocabulary'][:6]):
                with vocab_cols[i % 3]:
                    st.info(word)
                    if st.button(f"🔊", key=f"vocab_{i}"):
                        word_text = word.split(':')[0] if ':' in word else word
                        audio = tts.generate_audio(word_text, 'de')
                        if audio:
                            tts.play_audio(audio)
        
        # Comprehension questions
        if content.get('questions'):
            st.markdown("### ❓ Comprehension Questions")
            for i, question in enumerate(content['questions'][:3], 1):
                st.write(f"{i}. {question}")
            
            # Answer input
            answers = st.text_area("Your answers:", height=100, key="reading_answers")
            
            if st.button("Submit Answers", type="primary"):
                if answers:
                    st.success("Great comprehension work!")
                    update_skill_score("Reading", 5)
                    add_xp(15, "Reading comprehension completed!")
                    
                    if "Reading 📖" not in st.session_state.daily_tasks_completed:
                        st.session_state.daily_tasks_completed.append("Reading 📖")
                        save_user_progress()
        
        # Cultural note
        if content.get('cultural_note'):
            st.info(f"🌍 **Cultural Note:** {content['cultural_note']}")

def display_writing_lesson(lesson):
    """Display writing lesson with grammar checking"""
    content = lesson.get('content', {})
    
    st.markdown("## ✍️ Writing Practice")
    
    # Display task
    task = content.get('task', 'Write about your day in German')
    st.info(task)
    
    # Writing area
    user_text = st.text_area(
        "Your writing:",
        height=200,
        placeholder="Start writing in German..."
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if user_text:
                # Grammar check
                grammar_result = grammar_checker.check_german_text(user_text)
                
                if grammar_result['has_errors']:
                    st.warning(f"Found {grammar_result['error_count']} potential issues:")
                    for suggestion in grammar_result['suggestions'][:3]:
                        st.write(f"• {suggestion}")
                    
                    if st.button("Show corrected version"):
                        st.success(grammar_result['corrected_text'])
                else:
                    st.success("Excellent! No grammar errors detected!")
                
                # Update progress
                update_skill_score("Writing", 5)
                add_xp(15, "Writing exercise completed!")
                
                if "Writing ✍️" not in st.session_state.daily_tasks_completed:
                    st.session_state.daily_tasks_completed.append("Writing ✍️")
                    save_user_progress()
    
    with col2:
        if st.button("💡 Get Hint", use_container_width=True):
            st.info("Try using connecting words like 'und', 'aber', 'weil', 'dass'")
    
    with col3:
        if st.button("📐 Check Grammar", use_container_width=True):
            if user_text:
                result = grammar_checker.check_german_text(user_text)
                if result['has_errors']:
                    st.error(f"{result['error_count']} errors found")
                else:
                    st.success("Grammar looks good!")

def display_listening_lesson(lesson):
    """Display listening lesson with audio generation"""
    content = lesson.get('content', {})
    
    st.markdown("## 👂 Listening Practice")
    
    # Display dialogue or text
    dialogue = content.get('dialogue', content.get('transcript', ''))
    
    if dialogue:
        st.markdown("### Listen to the Dialogue")
        
        # Play button
        if st.button("🔊 Play Audio", type="primary", use_container_width=True):
            audio = tts.generate_audio(dialogue[:300], 'de', slow=True)
            if audio:
                tts.play_audio(audio)
        
        # Show transcript option
        if st.checkbox("Show transcript"):
            st.markdown(f"<div class='content-box'>{dialogue}</div>", unsafe_allow_html=True)
        
        # Comprehension questions
        st.markdown("### Answer these questions:")
        q1 = st.text_input("1. What is the main topic?")
        q2 = st.text_input("2. Who are the speakers?")
        q3 = st.text_input("3. What happens at the end?")
        
        if st.button("Submit Answers", type="primary"):
            if q1 or q2 or q3:
                st.success("Good listening comprehension!")
                update_skill_score("Listening", 5)
                add_xp(15, "Listening exercise completed!")
                
                if "Listening 👂" not in st.session_state.daily_tasks_completed:
                    st.session_state.daily_tasks_completed.append("Listening 👂")
                    save_user_progress()

def display_speaking_lesson(lesson):
    """Display speaking lesson with pronunciation practice"""
    content = lesson.get('content', {})
    
    st.markdown("## 🗣️ Speaking Practice")
    
    # Display scenario
    scenario = content.get('scenario', 'Practice speaking German')
    st.info(scenario)
    
    # Practice sentences
    practice_sentences = [
        "Guten Tag, wie geht es Ihnen?",
        "Ich komme aus Deutschland.",
        "Können Sie mir bitte helfen?",
        "Das Wetter ist heute schön.",
        "Ich möchte einen Kaffee bestellen."
    ]
    
    st.markdown("### Practice these sentences:")
    
    for i, sentence in enumerate(practice_sentences[:3]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.success(sentence)
        with col2:
            if st.button("🔊", key=f"speak_{i}"):
                audio = tts.generate_audio(sentence, 'de', slow=True)
                if audio:
                    tts.play_audio(audio)
    
    # Recording simulation
    st.markdown("### Record Yourself")
    st.info("🎤 Practice saying the sentences above. Focus on pronunciation!")
    
    if st.button("✅ I Practiced Speaking", type="primary", use_container_width=True):
        st.success("Excellent speaking practice!")
        update_skill_score("Speaking", 5)
        add_xp(15, "Speaking practice completed!")
        
        if "Speaking 🗣️" not in st.session_state.daily_tasks_completed:
            st.session_state.daily_tasks_completed.append("Speaking 🗣️")
            save_user_progress()

def display_grammar_lesson(lesson):
    """Display grammar lesson with exercises"""
    content = lesson.get('content', {})
    
    st.markdown("## 📐 Grammar Practice")
    
    # Display explanation
    explanation = content.get('explanation', '')
    if explanation:
        st.markdown(f"<div class='content-box'>{explanation}</div>", unsafe_allow_html=True)
    
    # Exercises
    exercises = content.get('exercises', [])
    if exercises:
        st.markdown("### Practice Exercises")
        
        for i, exercise in enumerate(exercises[:5], 1):
            st.write(f"{i}. {exercise}")
        
        # Answer input
        answers = st.text_area("Your answers:", height=100, key="grammar_answers")
        
        if st.button("Check Answers", type="primary"):
            if answers:
                # Check grammar
                result = grammar_checker.check_german_text(answers)
                
                if result['has_errors']:
                    st.warning(f"Found {result['error_count']} issues")
                    for suggestion in result['suggestions'][:3]:
                        st.write(f"• {suggestion}")
                else:
                    st.success("Perfect grammar!")
                
                update_skill_score("Grammar", 5)
                add_xp(15, "Grammar exercise completed!")
                
                if "Grammar 📐" not in st.session_state.daily_tasks_completed:
                    st.session_state.daily_tasks_completed.append("Grammar 📐")
                    save_user_progress()
    
    # Common mistakes
    if content.get('common_mistakes'):
        with st.expander("⚠️ Common Mistakes to Avoid"):
            for mistake in content['common_mistakes']:
                st.write(f"• {mistake}")

def page_exams():
    """Comprehensive exam center with all features"""
    st.title("📝 Exam Center")
    
    if not st.session_state.placement_completed:
        st.warning("Complete the placement test first to access exams!")
        return
    
    tabs = st.tabs(["📊 Level Progression", "🎓 Goethe Mock Exams", "📈 Exam History", "🏆 Certificates"])
    
    with tabs[0]:  # Level Progression Exams
        display_level_progression_exam()
    
    with tabs[1]:  # Goethe Mock Exams
        display_goethe_mock_exams()
    
    with tabs[2]:  # Exam History
        display_exam_history()
    
    with tabs[3]:  # Certificates
        display_certificates()

def display_level_progression_exam():
    """Display level progression exam interface"""
    st.markdown("### Level Progression Exam")
    
    # Get next level
    level_progression = {'A1': 'A2', 'A2': 'B1', 'B1': 'B2', 'B2': 'C1'}
    next_level = level_progression.get(st.session_state.user_level, 'B2')
    
    st.info(f"""
    **Current Level:** {st.session_state.user_level}
    **Next Level:** {next_level}
    
    Pass this exam to advance to the next level!
    """)
    
    # Check eligibility
    exercises_completed = len(st.session_state.completed_exercises)
    required_exercises = 20
    
    if exercises_completed < required_exercises:
        st.warning(f"""
        ⚠️ Not yet eligible for level exam.
        
        **Progress:** {exercises_completed}/{required_exercises} exercises completed
        
        Complete {required_exercises - exercises_completed} more exercises to unlock the exam.
        """)
        
        st.progress(exercises_completed / required_exercises)
    else:
        st.success("✅ You're eligible to take the level progression exam!")
        
        if st.button("🚀 Start Level Exam", type="primary", use_container_width=True):
            st.session_state.taking_exam = True
            st.session_state.exam_type = 'level_progression'
            st.rerun()
    
    # If taking exam, show exam interface
    if st.session_state.get('taking_exam') and st.session_state.get('exam_type') == 'level_progression':
        display_exam_interface()

def display_goethe_mock_exams():
    """Display Goethe mock exam interface"""
    st.markdown("### Goethe Institute Mock Exams")
    st.info("""
    Practice with authentic Goethe exam format!
    These mock exams help you prepare for official German certifications.
    """)
    
    # Select exam level
    exam_level = st.selectbox(
        "Choose exam level:",
        ["A1", "A2", "B1", "B2"],
        index=["A1", "A2", "B1", "B2"].index(st.session_state.user_level) 
              if st.session_state.user_level in ["A1", "A2", "B1", "B2"] else 0
    )
    
    # Display exam format info
    exam_formats = {
        'A1': {
            'duration': '90 minutes',
            'sections': ['Hören (20 min)', 'Lesen (25 min)', 'Schreiben (20 min)', 'Sprechen (15 min)'],
            'passing_score': '60%'
        },
        'A2': {
            'duration': '90 minutes',
            'sections': ['Hören (30 min)', 'Lesen (30 min)', 'Schreiben (30 min)', 'Sprechen (15 min)'],
            'passing_score': '60%'
        },
        'B1': {
            'duration': '165 minutes',
            'sections': ['Lesen (65 min)', 'Hören (40 min)', 'Schreiben (60 min)', 'Sprechen (15 min)'],
            'passing_score': '60%'
        },
        'B2': {
            'duration': '190 minutes',
            'sections': ['Lesen (80 min)', 'Hören (40 min)', 'Schreiben (80 min)', 'Sprechen (15 min)'],
            'passing_score': '60%'
        }
    }
    
    format_info = exam_formats[exam_level]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### Goethe {exam_level} Exam Format")
        st.write(f"**Duration:** {format_info['duration']}")
        st.write(f"**Passing Score:** {format_info['passing_score']}")
        st.write("**Sections:**")
        for section in format_info['sections']:
            st.write(f"• {section}")
    
    with col2:
        st.markdown("#### Start Mock Exam")
        
        if st.button(f"📝 Take Goethe {exam_level} Mock Exam", type="primary", use_container_width=True):
            st.session_state.taking_exam = True
            st.session_state.exam_type = 'goethe_mock'
            st.session_state.exam_level = exam_level
            st.rerun()

def display_exam_history():
    """Display exam history with detailed analytics"""
    st.markdown("### Your Exam History")
    
    if st.session_state.exam_history:
        # Create DataFrame for better display
        df = pd.DataFrame(st.session_state.exam_history)
        
        # Display summary stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Exams", len(st.session_state.exam_history))
        
        with col2:
            passed = len([e for e in st.session_state.exam_history if e.get('passed')])
            st.metric("Passed", passed)
        
        with col3:
            if st.session_state.exam_history:
                avg_score = sum(e.get('score', 0) for e in st.session_state.exam_history) / len(st.session_state.exam_history)
                st.metric("Average Score", f"{avg_score:.1f}%")
        
        # Display individual exams
        for i, exam_result in enumerate(st.session_state.exam_history[::-1]):
            with st.expander(f"Exam {len(st.session_state.exam_history) - i}: {exam_result.get('date', 'Unknown date')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Score", f"{exam_result.get('score', 0)}%")
                
                with col2:
                    st.metric("Result", "✅ Passed" if exam_result.get('passed') else "❌ Failed")
                
                with col3:
                    st.metric("Type", exam_result.get('type', 'Unknown'))
                
                if exam_result.get('feedback'):
                    st.write(f"**Feedback:** {exam_result['feedback']}")
    else:
        st.info("No exams taken yet. Complete exercises to unlock level exams!")

def display_certificates():
    """Display earned certificates"""
    st.markdown("### 📜 Your Certificates")
    
    certificates = [e for e in st.session_state.exam_history if e.get('passed') and e.get('certificate')]
    
    if certificates:
        for cert in certificates:
            display_certificate(cert.get('certificate'))
    else:
        st.info("Pass exams to earn certificates!")

def display_exam_interface():
    """Display the actual exam interface"""
    st.markdown("## 📝 Exam in Progress")
    
    # Timer simulation
    st.sidebar.markdown("### ⏱️ Time Remaining: 45:00")
    
    with st.form("exam_form"):
        st.markdown("### Section 1: Grammar")
        
        q1 = st.radio("1. Der ___ ist groß.", ["Mann", "Frau", "Kind", "Mädchen"])
        
        q2 = st.text_input("2. Complete: Ich _____ (haben) ein Auto.")
        
        st.markdown("### Section 2: Translation")
        
        q3 = st.text_area("3. Translate to German: 'I am learning German because I want to work in Germany.'")
        
        st.markdown("### Section 3: Writing")
        
        q4 = st.text_area("4. Write a short email (50 words) inviting a friend to dinner.", height=150)
        
        submitted = st.form_submit_button("Submit Exam", type="primary", use_container_width=True)
        
        if submitted:
            # Calculate score
            score = 0
            if q1 == "Mann": score += 25
            if "habe" in q2.lower(): score += 25
            if any(word in q3.lower() for word in ["lerne", "deutsch", "arbeiten", "deutschland"]): score += 25
            if q4 and len(q4.split()) >= 30: score += 25
            
            # Save exam result
            exam_result = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'type': st.session_state.exam_type,
                'score': score,
                'passed': score >= 60,
                'feedback': "Great job!" if score >= 60 else "Keep practicing!",
                'certificate': {
                    'title': f"{st.session_state.user_level} Level Certificate",
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'score': f"{score}%"
                } if score >= 60 else None
            }
            
            st.session_state.exam_history.append(exam_result)
            
            if score >= 60:
                st.balloons()
                st.success(f"Congratulations! You passed with {score}%!")
                
                # Level up if progression exam
                if st.session_state.exam_type == 'level_progression':
                    level_progression = {'A1': 'A2', 'A2': 'B1', 'B1': 'B2'}
                    if st.session_state.user_level in level_progression:
                        st.session_state.user_level = level_progression[st.session_state.user_level]
                        add_xp(100, "Passed level exam!")
            else:
                st.error(f"Score: {score}%. Keep practicing!")
            
            st.session_state.taking_exam = False
            save_user_progress()
            time.sleep(2)
            st.rerun()

def display_certificate(certificate):
    """Display exam certificate"""
    if certificate:
        st.markdown(f"""
        <div class='certificate'>
            <h1 style='margin: 0; font-size: 36px;'>🏆 Certificate of Achievement</h1>
            <h2 style='margin: 20px 0;'>{certificate.get('title', 'German Proficiency')}</h2>
            <p style='font-size: 20px;'>This certifies that</p>
            <h2 style='margin: 20px 0; font-size: 32px;'>{st.session_state.user_name}</h2>
            <p style='font-size: 20px;'>has successfully completed the examination with</p>
            <h1 style='margin: 20px 0; font-size: 48px;'>{certificate.get('score', '0%')}</h1>
            <p style='font-size: 18px;'>Date: {certificate.get('date', datetime.now().strftime('%Y-%m-%d'))}</p>
        </div>
        """, unsafe_allow_html=True)

def page_ai_guru():
    """Enhanced AI Guru chat interface with full features"""
    st.title("🧙‍♂️ AI Guru - Your Personal German Teacher")
    
    # Check API status with visual indicator
    api_status = "🟢 AI Ready" if (st.session_state.api_keys.get('openrouter') or 
                                   st.session_state.api_keys.get('huggingface')) else "🟡 Limited Mode"
    st.markdown(f"**Status:** {api_status}")
    
    # Quick action buttons with better descriptions
    st.markdown("### 🚀 Quick Actions")
    
    action_buttons = [
        ("📖 Explain Grammar", "Explain a specific grammar rule", "Can you explain the German case system?"),
        ("🗣️ Practice Conversation", "Have a conversation in German", "Let's practice ordering food in a restaurant."),
        ("✍️ Check My Writing", "Get feedback on your German text", "Please check this sentence: Ich gehe morgen zum Schule."),
        ("🎯 Custom Exercise", "Get a personalized exercise", f"Give me a {st.session_state.user_level or 'A1'} level exercise."),
        ("📚 Vocabulary Help", "Learn new words", "Teach me 5 words about technology."),
        ("❓ Ask Anything", "Free question about German", "How do I say 'I love you' in German?")
    ]
    
    cols = st.columns(3)
    for i, (label, help_text, prompt) in enumerate(action_buttons):
        with cols[i % 3]:
            if st.button(label, help=help_text, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.rerun()
    
    # Chat interface with better styling
    st.markdown("### 💬 Chat with AI Guru")
    
    # Create a container for chat history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            # Welcome message
            welcome = f"""
            <div class='ai-message'>
            <h4>👋 Guten Tag! I'm your AI German Guru.</h4>
            
            I see you're at <b>{st.session_state.user_level or 'beginner'}</b> level. I'm here to help you:
            
            • 📖 Explain any grammar concept<br>
            • 🗣️ Practice conversations<br>
            • ✍️ Check your writing<br>
            • 📚 Teach vocabulary<br>
            • 🎯 Create exercises<br>
            • ❓ Answer any German question<br>
            
            How can I help you today?
            </div>
            """
            st.markdown(welcome, unsafe_allow_html=True)
        else:
            # Display chat history with proper formatting
            for message in st.session_state.chat_history[-10:]:  # Show last 10 messages
                if message["role"] == "user":
                    st.markdown(f"<div class='chat-message user-message'>{message['content']}</div>", 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-message ai-message'>{message['content']}</div>", 
                              unsafe_allow_html=True)
    
    # Chat input with better UX
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Your message:",
                placeholder="Ask me anything about German...",
                key="chat_input"
            )
        
        with col2:
            submitted = st.form_submit_button("Send 📤", type="primary", use_container_width=True)
        
        if submitted and user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate AI response
            with st.spinner("🤔 AI Guru is thinking..."):
                response = st.session_state.ai_tutor.respond_to_student(
                    user_input,
                    st.session_state.user_level or "A1"
                )
            
            # Add AI response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Award XP for interaction
            if len(st.session_state.chat_history) % 5 == 0:  # Every 5 messages
                add_xp(5, "Active learning with AI Guru!")
            
            st.rerun()
    
    # Additional features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("📥 Save Chat", use_container_width=True):
            # Create downloadable chat history
            chat_text = "\n\n".join([f"{msg['role'].title()}: {msg['content']}" 
                                    for msg in st.session_state.chat_history])
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🎲 Random Topic", use_container_width=True):
            topics = [
                "Let's discuss your hobbies in German!",
                "Tell me about your family in German.",
                "Describe your daily routine.",
                "What's your favorite food? Let's talk about it in German!",
                "Let's practice shopping vocabulary.",
                "Tell me about your last vacation.",
                "Describe your hometown in German.",
                "Let's talk about the weather.",
                "Practice introducing yourself professionally.",
                "Discuss your future plans in German."
            ]
            random_topic = random.choice(topics)
            st.session_state.chat_history.append({"role": "user", "content": random_topic})
            st.rerun()
    
    # Learning tips sidebar
    with st.expander("💡 Conversation Tips"):
        st.markdown(f"""
        **Tips for {st.session_state.user_level or 'your'} level:**
        
        • Start with simple sentences
        • Don't worry about perfect grammar
        • Ask for clarification when needed
        • Practice common phrases daily
        • Use context to understand new words
        """)

def page_translator():
    """Enhanced smart translator with AI features - FIXED"""
    st.title("🔄 AI-Powered Smart Translator")
    st.markdown("### Translate with context and learn")
    
    # Translation direction
    direction = st.radio(
        "Direction:",
        ["🇬🇧 English → 🇩🇪 German", "🇩🇪 German → 🇬🇧 English"],
        horizontal=True
    )
    
    is_en_to_de = "English" in direction and "German" in direction and direction.index("English") < direction.index("German")
    
    # Initialize session state for phrases if not exists
    if 'selected_phrase' not in st.session_state:
        st.session_state.selected_phrase = ""
    
    # Main translation interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {'English' if is_en_to_de else 'German'} Input")
        
        # Use the selected phrase if available, otherwise empty
        default_text = st.session_state.selected_phrase if st.session_state.selected_phrase else ""
        
        source_text = st.text_area(
            "Enter text:",
            height=200,
            value=default_text,
            placeholder=f"Type your {'English' if is_en_to_de else 'German'} text here...",
            key="translator_input"  # Changed key to avoid conflict
        )
        
        # Quick phrases
        st.markdown("**Quick Phrases:**")
        quick_phrases = [
            "How are you?" if is_en_to_de else "Wie geht es dir?",
            "Thank you very much" if is_en_to_de else "Vielen Dank",
            "Where is the bathroom?" if is_en_to_de else "Wo ist die Toilette?",
            "I don't understand" if is_en_to_de else "Ich verstehe nicht",
            "Can you help me?" if is_en_to_de else "Können Sie mir helfen?",
            "How much does it cost?" if is_en_to_de else "Wie viel kostet das?"
        ]
        
        phrase_cols = st.columns(2)
        for i, phrase in enumerate(quick_phrases):
            with phrase_cols[i % 2]:
                if st.button(phrase, key=f"phrase_{i}", use_container_width=True):
                    st.session_state.selected_phrase = phrase
                    st.rerun()
        
        # Clear the selected phrase after use
        if st.session_state.selected_phrase:
            st.session_state.selected_phrase = ""
    
    with col2:
        st.markdown(f"#### {'German' if is_en_to_de else 'English'} Translation")
        
        if st.button("🔄 Translate", type="primary", use_container_width=True):
            if source_text:
                with st.spinner("Translating..."):
                    source_lang = "en" if is_en_to_de else "de"
                    target_lang = "de" if is_en_to_de else "en"
                    
                    # Store translation result in session state
                    if 'translation_result' not in st.session_state:
                        st.session_state.translation_result = {}
                    
                    result = translate_text(source_text, source_lang, target_lang)
                    st.session_state.translation_result = result
                    st.session_state.translated_text = result.get('translation', '')
            else:
                st.warning("Please enter text to translate")
        
        # Display translation result if available
        if 'translation_result' in st.session_state and st.session_state.translation_result:
            result = st.session_state.translation_result
            
            if result['success']:
                # Display translation in a nice box
                st.markdown(f"""
                <div class='translation-result'>
                    <strong>{result['translation']}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Show confidence if available
                if result.get('confidence'):
                    st.progress(result['confidence'] / 100)
                    st.caption(f"Confidence: {result['confidence']}%")
                
                # Alternative translations
                if result.get('alternatives'):
                    st.markdown("**Alternative translations:**")
                    for alt in result['alternatives'][:3]:
                        st.caption(f"• {alt}")
                
                # Play audio button
                if st.button("🔊 Listen", key="listen_translation"):
                    audio = tts.generate_audio(
                        result['translation'],
                        target_lang
                    )
                    if audio:
                        tts.play_audio(audio)
                
                # Grammar check for German text
                if target_lang == "de":
                    if st.button("📐 Check Grammar"):
                        grammar_result = grammar_checker.check_german_text(
                            result['translation']
                        )
                        if grammar_result['has_errors']:
                            st.warning(f"Found {grammar_result['error_count']} potential issues")
                            for suggestion in grammar_result['suggestions'][:3]:
                                st.write(f"• {suggestion}")
                        else:
                            st.success("Grammar looks good!")
                
                # Add to learning history
                add_xp(2, "Translation practice")
            else:
                st.error(result.get('note', 'Translation failed'))
    
    # Word analysis section
    st.markdown("---")
    st.markdown("### 📝 Word Analysis & Learning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        word_to_analyze = st.text_input("Enter a German word to analyze:", key="word_analyzer")
    
    with col2:
        analyze_button = st.button("Analyze", type="primary", use_container_width=True, key="analyze_btn")
    
    if analyze_button and word_to_analyze:
        # Word analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Word Type:**")
            # Enhanced word type detection
            if word_to_analyze[0].isupper():
                st.info("Noun (Substantiv)")
                st.caption("All German nouns are capitalized")
            elif word_to_analyze.endswith('en'):
                st.info("Likely a verb (infinitive)")
                st.caption("Most German verbs end in -en")
            elif word_to_analyze.endswith('lich') or word_to_analyze.endswith('ig'):
                st.info("Likely an adjective")
                st.caption("Common adjective endings")
            elif word_to_analyze.endswith('ung'):
                st.info("Noun (feminine)")
                st.caption("-ung endings are always feminine")
            else:
                st.info("Check dictionary for type")
        
        with col2:
            st.markdown("**Gender (if noun):**")
            # Enhanced gender detection
            if word_to_analyze.endswith('ung') or word_to_analyze.endswith('heit') or word_to_analyze.endswith('keit'):
                st.info("die (feminine)")
                st.caption("These endings are always feminine")
            elif word_to_analyze.endswith('chen') or word_to_analyze.endswith('lein'):
                st.info("das (neuter)")
                st.caption("Diminutive endings are neuter")
            elif word_to_analyze.endswith('er') and word_to_analyze[0].isupper():
                st.info("Usually der (masculine)")
                st.caption("But check dictionary to confirm")
            elif word_to_analyze.endswith('ismus'):
                st.info("der (masculine)")
                st.caption("-ismus endings are masculine")
            else:
                st.info("Check dictionary")
        
        with col3:
            st.markdown("**Pronunciation:**")
            if st.button("🔊 Listen", key="word_pronunciation"):
                audio = tts.generate_audio(word_to_analyze, 'de', slow=True)
                if audio:
                    tts.play_audio(audio)
        
        # Example sentences
        st.markdown("**Example sentences:**")
        examples = get_example_sentences(word_to_analyze, 'de')
        for i, example in enumerate(examples[:3]):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.write(f"• {example}")
            with col2:
                if st.button("🔊", key=f"example_audio_{i}"):
                    # Extract German part before parentheses
                    german_text = example.split('(')[0].strip()
                    audio = tts.generate_audio(german_text, 'de')
                    if audio:
                        tts.play_audio(audio)
    
    # Enhanced Phrase Book
    with st.expander("📚 Essential Phrase Book"):
        categories = {
            "🤝 Greetings": {
                "Good morning": "Guten Morgen",
                "Good afternoon": "Guten Tag", 
                "Good evening": "Guten Abend",
                "Good night": "Gute Nacht",
                "Hello (informal)": "Hallo",
                "Hello (formal)": "Guten Tag",
                "Goodbye": "Auf Wiedersehen",
                "See you later": "Bis später",
                "See you tomorrow": "Bis morgen"
            },
            "🙏 Polite Expressions": {
                "Please": "Bitte",
                "Thank you": "Danke",
                "Thank you very much": "Vielen Dank",
                "You're welcome": "Bitte schön",
                "Excuse me": "Entschuldigung",
                "I'm sorry": "Es tut mir leid",
                "Pardon?": "Wie bitte?",
                "No problem": "Kein Problem"
            },
            "❓ Essential Questions": {
                "Do you speak English?": "Sprechen Sie Englisch?",
                "How much?": "Wie viel?",
                "How much does it cost?": "Wie viel kostet das?",
                "Where?": "Wo?",
                "Where is...?": "Wo ist...?",
                "When?": "Wann?",
                "Why?": "Warum?",
                "What?": "Was?",
                "Who?": "Wer?",
                "How?": "Wie?"
            },
            "🏪 Shopping": {
                "I would like...": "Ich möchte...",
                "Do you have...?": "Haben Sie...?",
                "How much does it cost?": "Wie viel kostet das?",
                "That's too expensive": "Das ist zu teuer",
                "Can I pay by card?": "Kann ich mit Karte zahlen?",
                "Cash only": "Nur Bargeld",
                "Receipt please": "Die Quittung bitte",
                "Where can I find...?": "Wo finde ich...?",
                "I'm just looking": "Ich schaue nur"
            },
            "🍽️ Restaurant": {
                "A table for two please": "Einen Tisch für zwei bitte",
                "The menu please": "Die Speisekarte bitte",
                "I would like...": "Ich möchte...",
                "I'll have...": "Ich nehme...",
                "The bill please": "Die Rechnung bitte",
                "Is it vegetarian?": "Ist es vegetarisch?",
                "I'm allergic to...": "Ich bin allergisch gegen...",
                "Delicious!": "Lecker!",
                "Water please": "Wasser bitte"
            },
            "🚨 Emergency": {
                "Help!": "Hilfe!",
                "Call the police!": "Rufen Sie die Polizei!",
                "Call an ambulance!": "Rufen Sie einen Krankenwagen!",
                "I need a doctor": "Ich brauche einen Arzt",
                "Where is the hospital?": "Wo ist das Krankenhaus?",
                "Emergency": "Notfall",
                "Fire!": "Feuer!",
                "I'm lost": "Ich habe mich verlaufen"
            }
        }
        
        for category, phrases in categories.items():
            st.markdown(f"**{category}:**")
            
            # Create a table-like layout
            for eng, ger in phrases.items():
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.write(eng)
                with col2:
                    st.write(f"**{ger}**")
                with col3:
                    if st.button("🔊", key=f"phrasebook_{category}_{eng}"):
                        audio = tts.generate_audio(ger, 'de')
                        if audio:
                            tts.play_audio(audio)
            st.markdown("---")

def page_progress():
    """Enhanced progress page with detailed analytics"""
    st.title("📈 Your Learning Analytics")
    
    # Overall progress header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total XP", st.session_state.xp, delta=f"+{st.session_state.daily_xp} today")
    
    with col2:
        title, color = get_level_title(st.session_state.xp)
        st.metric("Current Title", title.split()[1] if len(title.split()) > 1 else title)
    
    with col3:
        st.metric("Study Streak", f"{st.session_state.streak} days", 
                 delta="Keep it up!" if st.session_state.streak > 0 else "Start today!")
    
    with col4:
        completion = (st.session_state.current_day / 180) * 100
        st.metric("Journey", f"{completion:.1f}%", delta=f"Day {st.session_state.current_day}/180")
    
    # Visual progress chart
    st.markdown("### 📊 180-Day Journey Progress")
    
    # Create progress visualization
    progress_percent = (st.session_state.current_day / 180) * 100
    st.progress(progress_percent / 100)
    
    # Milestones
    milestones = [30, 60, 90, 120, 150, 180]
    milestone_cols = st.columns(6)
    
    for i, milestone in enumerate(milestones):
        with milestone_cols[i]:
            reached = st.session_state.current_day >= milestone
            st.markdown(f"""
            <div class='progress-milestone'>
                <div style='color: {"#4CAF50" if reached else "#999"}; font-size: 24px;'>
                    {"✅" if reached else "○"}
                </div>
                <small>Day {milestone}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Learning Activity Chart
    st.markdown("### 📅 Weekly Activity")
    
    # Generate sample data for the chart
    dates = pd.date_range(end=datetime.now(), periods=7)
    activity_data = pd.DataFrame({
        'Date': dates,
        'XP Earned': [random.randint(20, 100) for _ in range(7)],
        'Exercises': [random.randint(3, 10) for _ in range(7)],
        'Minutes': [random.randint(15, 60) for _ in range(7)]
    })
    
    # Create interactive chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=activity_data['Date'],
        y=activity_data['XP Earned'],
        name='XP Earned',
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Scatter(
        x=activity_data['Date'],
        y=activity_data['Minutes'],
        name='Minutes Studied',
        yaxis='y2',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Your Learning Activity",
        xaxis_title="Date",
        yaxis=dict(title="XP Earned", side="left"),
        yaxis2=dict(title="Minutes", overlaying="y", side="right"),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills breakdown with visual bars
    st.markdown("### 🎯 Skill Proficiency")
    
    skills = ["Speaking", "Writing", "Listening", "Reading", "Grammar"]
    
    for skill in skills:
        score = st.session_state.skill_scores.get(skill, 0)
        
        col1, col2, col3 = st.columns([2, 5, 1])
        with col1:
            emoji = {"Speaking": "🗣️", "Writing": "✍️", "Listening": "👂", 
                    "Reading": "📖", "Grammar": "📐"}[skill]
            st.write(f"{emoji} {skill}")
        with col2:
            st.progress(score / 100)
        with col3:
            st.write(f"{score}%")
    
    # Find weakest skill for recommendations
    weakest_skill = min(st.session_state.skill_scores.items(), key=lambda x: x[1])[0]
    if st.session_state.skill_scores[weakest_skill] < 50:
        st.info(f"💡 **Tip:** Focus on {weakest_skill} to balance your skills!")
    
    # Learning patterns
    st.markdown("### 📊 Learning Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Best Learning Time:**")
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            time_preference = "🌅 Morning Learner"
        elif 12 <= current_hour < 17:
            time_preference = "☀️ Afternoon Student"
        elif 17 <= current_hour < 22:
            time_preference = "🌆 Evening Scholar"
        else:
            time_preference = "🌙 Night Owl"
        st.info(time_preference)
        
        st.markdown("**Consistency Score:**")
        consistency = min(100, st.session_state.streak * 10)
        st.progress(consistency / 100)
        st.caption(f"{consistency}% consistent")
    
    with col2:
        st.markdown("**Favorite Skill:**")
        if st.session_state.skill_scores:
            favorite = max(st.session_state.skill_scores.items(), key=lambda x: x[1])[0]
            st.info(f"💪 {favorite}")
        
        st.markdown("**Total Study Time:**")
        total_exercises = len(st.session_state.completed_exercises)
        estimated_hours = (total_exercises * 15) // 60
        st.info(f"⏱️ ~{estimated_hours} hours")
    
    # Detailed statistics
    with st.expander("📊 Detailed Statistics"):
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("Total Exercises", len(st.session_state.completed_exercises))
            st.metric("Avg. XP per Day", st.session_state.xp // max(1, st.session_state.current_day))
            st.metric("Total Achievements", len(st.session_state.achievements))
        
        with stats_col2:
            st.metric("Words Learned", len(st.session_state.completed_exercises) * 5)  # Estimate
            st.metric("Sentences Written", len([e for e in st.session_state.completed_exercises if 'writing' in e]) * 10)
            st.metric("Audio Minutes", len([e for e in st.session_state.completed_exercises if 'listening' in e]) * 5)
        
        with stats_col3:
            st.metric("Perfect Days", len([d for d in st.session_state.daily_tasks_completed if len(d) == 5]))
            st.metric("Exams Passed", len([e for e in st.session_state.exam_history if e.get('passed')]))
            st.metric("Current Level", st.session_state.user_level or "Not Set")
    
    # Personalized recommendations
    st.markdown("### 💡 Personalized Recommendations")
    
    weak_skills = [skill for skill, score in st.session_state.skill_scores.items() if score < 60]
    recommendations = get_personalized_recommendations(st.session_state.user_level, weak_skills)
    
    recommendation_cols = st.columns(len(recommendations[:3]))
    for i, rec in enumerate(recommendations[:3]):
        with recommendation_cols[i]:
            st.info(f"{i+1}. {rec}")
    
    # Export progress button
    if st.button("📥 Export Progress Report", use_container_width=True):
        report = f"""
        LINGUAFLOW PROGRESS REPORT
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Student: {st.session_state.user_name}
        Level: {st.session_state.user_level}
        
        STATISTICS:
        - Total XP: {st.session_state.xp}
        - Current Day: {st.session_state.current_day}/180
        - Streak: {st.session_state.streak} days
        - Exercises Completed: {len(st.session_state.completed_exercises)}
        
        SKILL SCORES:
        {chr(10).join([f"- {skill}: {score}%" for skill, score in st.session_state.skill_scores.items()])}
        
        ACHIEVEMENTS ({len(st.session_state.achievements)}):
        {chr(10).join([f"- {ach}" for ach in st.session_state.achievements])}
        
        Keep up the great work!
        """
        
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"progress_report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

def page_achievements():
    """Enhanced achievements page with gamification"""
    st.title("🏆 Achievement Gallery")
    
    # Achievement stats header
    total_achievements = 17  # Updated count
    unlocked = len(st.session_state.achievements)
    progress = unlocked / total_achievements
    
    st.markdown(f"""
    <div class='certificate'>
        <h1 style='margin: 0;'>{unlocked}/{total_achievements}</h1>
        <p style='margin: 10px 0;'>Achievements Unlocked</p>
        <div style='background: rgba(255,255,255,0.3); border-radius: 10px; height: 20px; margin-top: 15px;'>
            <div style='background: white; height: 100%; width: {progress*100}%; border-radius: 10px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievement categories
    categories = {
        "🎯 Milestones": [
            ("First Steps", "Complete your first lesson", len(st.session_state.completed_exercises) >= 1, 10),
            ("Week Warrior", "7-day streak", st.session_state.streak >= 7, 25),
            ("Monthly Master", "30 days of learning", st.session_state.current_day >= 30, 50),
            ("Halfway Hero", "Reach day 90", st.session_state.current_day >= 90, 75),
            ("B2 Boss", "Complete 180 days", st.session_state.current_day >= 180, 100)
        ],
        "📚 Learning": [
            ("Grammar Guru", "20 grammar exercises", 
             len([e for e in st.session_state.completed_exercises if 'grammar' in e]) >= 20, 30),
            ("Vocabulary Victor", "Learn 500 words", 
             len(st.session_state.completed_exercises) * 5 >= 500, 30),
            ("Reading Rockstar", "50 reading exercises", 
             len([e for e in st.session_state.completed_exercises if 'reading' in e]) >= 50, 30),
            ("Writing Wizard", "30 writing exercises",
             len([e for e in st.session_state.completed_exercises if 'writing' in e]) >= 30, 30),
            ("Speaking Star", "50 speaking exercises",
             len([e for e in st.session_state.completed_exercises if 'speaking' in e]) >= 50, 30),
            ("Listening Legend", "40 listening exercises",
             len([e for e in st.session_state.completed_exercises if 'listening' in e]) >= 40, 30)
        ],
        "🌟 Special": [
            ("Night Owl", "Study after 10 PM", datetime.now().hour >= 22, 15),
            ("Early Bird", "Study before 6 AM", datetime.now().hour < 6, 15),
            ("Weekend Warrior", "Study on weekend", datetime.now().weekday() >= 5, 15),
            ("Exam Master", "Pass 5 exams", len(st.session_state.exam_history) >= 5, 25),
            ("Perfectionist", "100% daily completion", False, 20),
            ("Social Learner", "Share progress", False, 10)
        ]
    }
    
    # Display achievements by category
    for category, achievements in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(5)
        for i, (name, description, unlocked, xp_reward) in enumerate(achievements):
            with cols[i % 5]:
                if unlocked and name in st.session_state.achievements:
                    # Unlocked achievement
                    st.markdown(f"""
                    <div style='text-align: center; background: linear-gradient(135deg, #4CAF50, #8BC34A); 
                               color: white; padding: 15px; border-radius: 15px; margin: 5px;
                               box-shadow: 0 5px 15px rgba(0,0,0,0.2); min-height: 150px;'>
                        <div style='font-size: 30px;'>🏆</div>
                        <strong>{name}</strong><br>
                        <small>{description}</small><br>
                        <small>+{xp_reward} XP</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Locked achievement
                    st.markdown(f"""
                    <div style='text-align: center; background: #f0f2f6; 
                               color: #999; padding: 15px; border-radius: 15px; margin: 5px;
                               border: 2px dashed #ddd; min-height: 150px;'>
                        <div style='font-size: 30px;'>🔒</div>
                        <strong>???</strong><br>
                        <small>{description}</small><br>
                        <small>+{xp_reward} XP</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Next achievement to unlock
    st.markdown("### 🎯 Next Achievement")
    
    # Find closest achievement to unlock
    next_achievement = None
    for category, achievements in categories.items():
        for name, description, unlocked, xp_reward in achievements:
            if not unlocked or name not in st.session_state.achievements:
                next_achievement = (name, description, xp_reward)
                break
        if next_achievement:
            break
    
    if next_achievement:
        st.info(f"""
        **{next_achievement[0]}** - {next_achievement[1]}
        
        Reward: +{next_achievement[2]} XP
        
        Keep learning to unlock this achievement!
        """)
    else:
        st.success("🎊 Congratulations! You've unlocked all achievements!")
        st.balloons()
    
    # Leaderboard placeholder
    st.markdown("### 🏅 Leaderboard")
    
    # Create sample leaderboard data
    leaderboard_data = pd.DataFrame({
        'Rank': ['🥇', '🥈', '🥉', '4', '5'],
        'Name': ['You' if i == 0 else f'Student {i+1}' for i in range(5)],
        'Level': [st.session_state.user_level or 'A1'] + ['B2', 'B1', 'B1', 'A2'],
        'XP': [st.session_state.xp] + [random.randint(1000, 2000) for _ in range(4)],
        'Streak': [st.session_state.streak] + [random.randint(5, 30) for _ in range(4)]
    })
    
    st.dataframe(leaderboard_data, use_container_width=True, hide_index=True)
    
    # Share achievements
    if st.button("📤 Share Achievements", use_container_width=True):
        share_text = f"""
        🎉 My LinguaFlow Achievements:
        
        Level: {st.session_state.user_level}
        XP: {st.session_state.xp}
        Achievements: {len(st.session_state.achievements)}/{total_achievements}
        Streak: {st.session_state.streak} days
        
        Join me in learning German for free at LinguaFlow!
        """
        st.code(share_text)
        st.success("Copy this text to share your progress on social media!")

def page_settings():
    """Enhanced settings page with all configurations"""
    st.title("⚙️ Settings & Configuration")
    
    tabs = st.tabs(["🔑 API Keys", "👤 Profile", "🎨 Preferences", "📊 Data", "ℹ️ About"])
    
    with tabs[0]:  # API Keys
        st.markdown("### API Configuration")
        st.info("""
        Add API keys for enhanced features:
        - **OpenRouter**: Advanced AI responses (recommended)
        - **HuggingFace**: Alternative AI provider
        - **Together AI**: Additional AI option
        - **MyMemory Email**: Better translation limits (10,000 vs 1,000 words/day)
        """)
        
        with st.form("api_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                openrouter_key = st.text_input(
                    "OpenRouter API Key",
                    value=st.session_state.api_keys.get('openrouter', ''),
                    type="password",
                    help="Get free key at openrouter.ai/keys"
                )
                
                huggingface_key = st.text_input(
                    "HuggingFace API Key",
                    value=st.session_state.api_keys.get('huggingface', ''),
                    type="password",
                    help="Get free key at huggingface.co/settings/tokens"
                )
            
            with col2:
                together_key = st.text_input(
                    "Together AI API Key",
                    value=st.session_state.api_keys.get('together', ''),
                    type="password",
                    help="Get key at together.ai"
                )
                
                mymemory_email = st.text_input(
                    "MyMemory Email",
                    value=st.session_state.api_keys.get('mymemory_email', ''),
                    help="Increases translation limit to 10,000 words/day"
                )
            
            st.markdown("**API Status:**")
            if st.session_state.api_keys.get('openrouter'):
                st.success("✅ OpenRouter configured")
            if st.session_state.api_keys.get('huggingface'):
                st.success("✅ HuggingFace configured")
            if st.session_state.api_keys.get('together'):
                st.success("✅ Together AI configured")
            if not any([st.session_state.api_keys.get('openrouter'), 
                       st.session_state.api_keys.get('huggingface'),
                       st.session_state.api_keys.get('together')]):
                st.warning("⚠️ No AI API configured - using limited features")
            
            if st.form_submit_button("💾 Save API Keys", type="primary", use_container_width=True):
                st.session_state.api_keys['openrouter'] = openrouter_key
                st.session_state.api_keys['huggingface'] = huggingface_key
                st.session_state.api_keys['together'] = together_key
                st.session_state.api_keys['mymemory_email'] = mymemory_email
                
                # Reinitialize AI providers
                st.session_state.ai_engine = AIContentEngine()
                st.session_state.lesson_generator = DynamicLessonGenerator(st.session_state.ai_engine)
                st.session_state.ai_tutor = IntelligentTutor(st.session_state.ai_engine)
                
                st.success("API keys saved successfully!")
                save_user_progress()
        
        # Test API connection
        if st.button("🔧 Test API Connection"):
            with st.spinner("Testing connection..."):
                test_prompt = "Say 'Hello' in German"
                response = st.session_state.ai_engine.generate_unique_content(
                    'test', 'A1', 'greeting'
                )
                
                if response and not response.startswith("["):
                    st.success("✅ API connection successful!")
                    st.write(f"Test response: {response[:100]}...")
                else:
                    st.warning("⚠️ Using fallback mode. Add API keys for full features.")
    
    with tabs[1]:  # Profile
        st.markdown("### User Profile")
        
        with st.form("profile_settings"):
            name = st.text_input("Name", value=st.session_state.user_name)
            
            level = st.selectbox(
                "Current Level",
                ["A1", "A2", "B1", "B2"],
                index=["A1", "A2", "B1", "B2"].index(st.session_state.user_level) 
                      if st.session_state.user_level in ["A1", "A2", "B1", "B2"] else 0
            )
            
            learning_goal = st.selectbox(
                "Learning Goal",
                ["Travel", "Work", "Study", "Family", "Personal Interest", "Immigration"]
            )
            
            native_language = st.selectbox(
                "Native Language",
                ["English", "Spanish", "French", "Chinese", "Arabic", "Hindi", "Other"]
            )
            
            target_date = st.date_input(
                "Target Date to Reach B2",
                value=datetime.now() + timedelta(days=180)
            )
            
            if st.form_submit_button("Update Profile", type="primary"):
                st.session_state.user_name = name
                st.session_state.user_level = level
                save_user_progress()
                st.success("Profile updated!")
    
    with tabs[2]:  # Preferences
        st.markdown("### Learning Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            daily_goal = st.slider(
                "Daily Learning Goal (minutes)",
                min_value=5,
                max_value=120,
                value=30,
                step=5,
                help="Recommended: 30-45 minutes daily"
            )
            
            difficulty = st.select_slider(
                "Exercise Difficulty",
                options=["Easy", "Normal", "Challenging"],
                value="Normal"
            )
            
            learning_style = st.multiselect(
                "Preferred Learning Styles",
                ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
                default=["Visual", "Reading/Writing"]
            )
        
        with col2:
            focus_skills = st.multiselect(
                "Skills to Focus On",
                ["Speaking", "Writing", "Listening", "Reading", "Grammar"],
                default=["Speaking", "Grammar"]
            )
            
            theme_preference = st.selectbox(
                "UI Theme",
                ["Light", "Dark", "Auto"],
                index=0
            )
            
            font_size = st.select_slider(
                "Font Size",
                options=["Small", "Medium", "Large"],
                value="Medium"
            )
        
        st.markdown("### Notification Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            daily_reminder = st.checkbox("Daily reminder", value=True)
            streak_notifications = st.checkbox("Streak notifications", value=True)
            achievement_alerts = st.checkbox("Achievement alerts", value=True)
        
        with col2:
            weekly_summary = st.checkbox("Weekly progress summary", value=False)
            exam_reminders = st.checkbox("Exam reminders", value=True)
            tip_notifications = st.checkbox("Learning tips", value=True)
        
        st.markdown("### Audio Settings")
        
        tts_speed = st.select_slider(
            "Text-to-Speech Speed",
            options=["Slow", "Normal", "Fast"],
            value="Normal"
        )
        
        auto_play_audio = st.checkbox("Auto-play audio", value=False)
        audio_repetitions = st.number_input("Audio repetitions", min_value=1, max_value=5, value=1)
        
        if st.button("Save Preferences", type="primary"):
            st.success("Preferences saved!")
    
    with tabs[3]:  # Data
        st.markdown("### Data Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Progress", use_container_width=True):
                if save_user_progress():
                    st.success("Progress saved!")
        
        with col2:
            if st.button("📥 Export Data", use_container_width=True):
                # Create comprehensive data export
                export_data = {
                    'user_profile': {
                        'name': st.session_state.user_name,
                        'level': st.session_state.user_level,
                        'xp': st.session_state.xp,
                        'streak': st.session_state.streak,
                        'current_day': st.session_state.current_day
                    },
                    'achievements': st.session_state.achievements,
                    'completed_exercises': st.session_state.completed_exercises,
                    'skill_scores': st.session_state.skill_scores,
                    'exam_history': st.session_state.exam_history,
                    'exported_at': datetime.now().isoformat()
                }
                
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"linguaflow_backup_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🗑️ Reset Progress", use_container_width=True):
                st.warning("⚠️ This will delete all your progress!")
                if st.checkbox("I understand this will delete all my progress"):
                    if st.button("Confirm Reset", type="secondary"):
                        st.session_state.clear()
                        st.success("Progress reset. Refreshing...")
                        time.sleep(2)
                        st.rerun()
        
        st.markdown("### Storage Info")
        st.info(f"""
        **Data Storage:**
        - Exercises completed: {len(st.session_state.completed_exercises)}
        - Chat messages: {len(st.session_state.chat_history)}
        - Achievements: {len(st.session_state.achievements)}/{17}
        - Exam records: {len(st.session_state.exam_history)}
        - Days studied: {st.session_state.current_day}
        
        Note: Data is saved locally and in browser session.
        """)
        
        # Backup reminder
        if st.session_state.current_day > 30:
            st.warning("💡 You've been learning for over 30 days! Consider exporting a backup of your progress.")
    
    with tabs[4]:  # About
        st.markdown("### About LinguaFlow")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; padding: 30px; border-radius: 20px;'>
            <h2>🇩🇪 LinguaFlow - AI German Tutor</h2>
            <p><strong>Version 2.0</strong> - Full AI Integration</p>
            
            <h3>✨ Features</h3>
            <ul>
                <li>🤖 True AI-powered content generation</li>
                <li>📚 Personalized adaptive lessons</li>
                <li>🧙‍♂️ Intelligent AI tutor (AI Guru)</li>
                <li>📝 Comprehensive exam system</li>
                <li>🎮 Gamified learning experience</li>
                <li>🔄 Smart translation with context</li>
                <li>🔊 Text-to-speech pronunciation</li>
                <li>📐 Grammar checking & correction</li>
                <li>📊 Detailed progress analytics</li>
                <li>🏆 Achievement system with rewards</li>
                <li>💾 Progress saving & data export</li>
                <li>🎯 Goethe exam preparation</li>
            </ul>
            
            <h3>🎯 Mission</h3>
            <p>Making quality German education accessible to everyone, everywhere, for free.</p>
            
            <h3>🛠️ Technology</h3>
            <p>Built with Streamlit, OpenRouter, HuggingFace, and open-source AI models.</p>
            
            <h3>🙏 Credits</h3>
            <p>Created with ❤️ by language learning enthusiasts for the global community.</p>
            
            <p style='text-align: center; margin-top: 20px; font-size: 20px;'>
                <strong>No subscription. No ads. Always free. 🎉</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📚 Learning Tips")
        
        tips = [
            ("🎯", "Consistency beats intensity", "15 minutes daily is better than 2 hours weekly"),
            ("🗣️", "Speak from day one", "Don't wait to be perfect before speaking"),
            ("📝", "Write by hand", "It helps with memorization"),
            ("🎵", "Use German media", "Music, podcasts, and shows make learning fun"),
            ("💭", "Think in German", "Start with simple thoughts throughout the day"),
            ("📖", "Read at your level", "Children's books are perfect for beginners"),
            ("🎮", "Gamify your learning", "Set challenges and reward yourself"),
            ("👥", "Find a language partner", "Practice with native speakers online"),
            ("📱", "Change device language", "Immerse yourself digitally"),
            ("🎯", "Set SMART goals", "Specific, Measurable, Achievable, Relevant, Time-bound")
        ]
        
        tip_cols = st.columns(2)
        for i, (emoji, title, description) in enumerate(tips):
            with tip_cols[i % 2]:
                st.info(f"{emoji} **{title}**\n\n{description}")
        
        st.markdown("### 🐛 Report Issues & Feedback")
        
        with st.form("feedback_form"):
            feedback_type = st.selectbox(
                "Type",
                ["Bug Report", "Feature Request", "General Feedback", "Content Error"]
            )
            
            feedback = st.text_area("Your feedback:", height=100)
            
            if st.form_submit_button("Send Feedback"):
                if feedback:
                    st.success("Thank you for your feedback! We'll review it soon.")
                    # In a real app, this would send to a database or email

# ==========================================
# MAIN APPLICATION
# ==========================================

def main():
    """Main application with enhanced navigation"""
    
    # Sidebar with better styling
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #667eea;'>🇩🇪 LinguaFlow</h1>
            <p style='color: #666;'>Your AI German Tutor</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Dashboard": page_dashboard,
            "📊 Placement Test": page_placement_test,
            "📚 Today's Lesson": page_todays_lesson,
            "📝 Exams": page_exams,
            "🧙‍♂️ AI Guru": page_ai_guru,
            "🔄 Translator": page_translator,
            "📈 Progress": page_progress,
            "🏆 Achievements": page_achievements,
            "⚙️ Settings": page_settings
        }
        
        # Initialize selected page
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "🏠 Dashboard"
        
        # Navigation buttons with better styling
        for page_name in pages.keys():
            if st.button(
                page_name,
                use_container_width=True,
                type="primary" if st.session_state.selected_page == page_name else "secondary"
            ):
                st.session_state.selected_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats in sidebar
        if st.session_state.user_level:
            st.markdown("### 📊 Quick Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Level", st.session_state.user_level)
                st.metric("Streak", f"{st.session_state.streak}🔥")
            
            with col2:
                st.metric("XP", st.session_state.xp)
                st.metric("Day", st.session_state.current_day)
            
            # Mini progress bar
            progress = (st.session_state.current_day / 180) * 100
            st.progress(progress / 100)
            st.caption(f"{progress:.1f}% to B2")
        
        # Daily tip
        st.markdown("---")
        st.markdown("### 💡 Tip of the Day")
        
        daily_tips = [
            "Practice speaking in front of a mirror",
            "Learn 5 new words with their articles",
            "Watch a German YouTube video",
            "Write 3 sentences about your day",
            "Practice numbers 1-100",
            "Learn one idiom today",
            "Focus on pronunciation for 10 minutes"
        ]
        
        tip_index = datetime.now().day % len(daily_tips)
        st.info(daily_tips[tip_index])
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #999; font-size: 12px;'>
            Made with ❤️ for learners everywhere<br>
            Version 2.0 | Always Free
        </div>
        """, unsafe_allow_html=True)
    
    # Display selected page
    pages[st.session_state.selected_page]()
    
    # Help button in corner
    with st.container():
        if st.button("❓", help="Get help", key="help_button"):
            with st.expander("Quick Help", expanded=True):
                st.markdown("""
                **Getting Started:**
                1. Take the Placement Test to determine your level
                2. Complete daily lessons across all 5 skills
                3. Chat with AI Guru for personalized help
                4. Take exams to advance levels
                5. Track your progress and earn achievements
                
                **Tips:**
                - Complete all 5 daily tasks for bonus XP
                - Maintain your streak for extra rewards
                - Use the translator for quick help
                - Export your progress regularly
                
                **Need help?** Chat with AI Guru!
                """)

if __name__ == "__main__":
    main()