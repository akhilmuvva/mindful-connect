"""
Mindful Connect - Main Streamlit Application
AI-Powered Mental Wellness Companion
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Any, Optional

# Import our modules
from src.config import settings, logger
from src.auth.firebase_auth import firebase_auth
from src.database.firestore_client import firestore_client
from src.ai.openai_client import openai_client
from src.ai.sentiment_analyzer import sentiment_analyzer
from src.ai.mood_predictor import mood_predictor


# Page configuration
st.set_page_config(
    page_title="Mindful Connect - Mental Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for beautiful UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #4ECDC4;
        --accent-color: #FF6B6B;
        --background: #0E1117;
        --surface: #1E1E2E;
        --text-primary: #FFFFFF;
        --text-secondary: #B8B8D1;
    }
    
    /* Glassmorphism effect */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Mood button styles */
    .mood-button {
        padding: 15px 30px;
        margin: 10px;
        border-radius: 50px;
        border: none;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    .mood-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Animated gradient text */
    .gradient-text {
        background: linear-gradient(45deg, #6C63FF, #4ECDC4, #FF6B6B);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card hover effect */
    .insight-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        border-left: 4px solid var(--primary-color);
    }
    
    .insight-card:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    /* Error message */
    .error-message {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    if 'mood_entries' not in st.session_state:
        st.session_state.mood_entries = []


# Authentication page
def show_auth_page():
    st.markdown("<h1 class='gradient-text' style='text-align: center; font-size: 3em;'>🧠 Mindful Connect</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #B8B8D1;'>Your AI-Powered Mental Wellness Companion</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                with st.spinner("Logging in..."):
                    result = firebase_auth.login_user(email, password)
                    
                    if result['success']:
                        st.session_state.authenticated = True
                        st.session_state.user_data = result
                        
                        # Load user data from Firestore
                        user_info = firestore_client.get_user(result['uid'])
                        if not user_info:
                            # Create new user document
                            firestore_client.create_user(result['uid'], {
                                'email': email,
                                'display_name': result.get('display_name', ''),
                                'preferences': {}
                            })
                        
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(result['message'])
        
        with tab2:
            st.markdown("### Create Account")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            display_name = st.text_input("Display Name (Optional)", key="display_name")
            
            if st.button("Sign Up", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    with st.spinner("Creating account..."):
                        result = firebase_auth.register_user(new_email, new_password, display_name)
                        
                        if result['success']:
                            # Create user document in Firestore
                            firestore_client.create_user(result['uid'], {
                                'email': new_email,
                                'display_name': display_name,
                                'preferences': {}
                            })
                            
                            st.success("Account created! Please check your email for verification.")
                        else:
                            st.error(result['message'])


# Dashboard page
def show_dashboard():
    st.markdown("<h1 class='gradient-text'>📊 Your Wellness Dashboard</h1>", unsafe_allow_html=True)
    
    uid = st.session_state.user_data['uid']
    
    # Load mood entries
    mood_entries = firestore_client.get_mood_entries(uid, limit=30)
    
    if not mood_entries:
        st.info("👋 Welcome! Start by logging your first mood entry.")
        return
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    recent_moods = [entry['mood_score'] for entry in mood_entries[:7]]
    avg_mood = sum(recent_moods) / len(recent_moods) if recent_moods else 0
    
    with col1:
        st.metric("7-Day Average", f"{avg_mood:.1f}/10", 
                 delta=f"{recent_moods[0] - avg_mood:.1f}" if recent_moods else None)
    
    with col2:
        st.metric("Total Entries", len(mood_entries))
    
    with col3:
        insights = mood_predictor.get_mood_insights(mood_entries)
        if insights['success']:
            st.metric("Trend", insights['trend'].replace('_', ' ').title())
    
    with col4:
        st.metric("Current Streak", f"{len(mood_entries)} days")
    
    # Mood trend chart
    st.markdown("### 📈 Mood Trend")
    
    df = pd.DataFrame(mood_entries)
    df['date'] = pd.to_datetime(df['created_at'])
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['mood_score'],
        mode='lines+markers',
        name='Mood Score',
        line=dict(color='#6C63FF', width=3),
        marker=dict(size=8, color='#4ECDC4')
    ))
    
    fig.update_layout(
        template='plotly_dark',
        height=400,
        xaxis_title="Date",
        yaxis_title="Mood Score",
        yaxis=dict(range=[0, 10]),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mood prediction
    if settings.ENABLE_MOOD_PREDICTION and len(mood_entries) >= 7:
        st.markdown("### 🔮 Mood Forecast")
        
        with st.spinner("Generating forecast..."):
            prediction = mood_predictor.predict_mood(mood_entries, days_ahead=7)
            
            if prediction and prediction['success']:
                pred_df = pd.DataFrame(prediction['predictions'])
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=pred_df['date'],
                    y=pred_df['predicted_mood'],
                    mode='lines+markers',
                    name='Predicted Mood',
                    line=dict(color='#FF6B6B', width=2, dash='dash'),
                    marker=dict(size=6)
                ))
                
                fig2.update_layout(
                    template='plotly_dark',
                    height=300,
                    xaxis_title="Date",
                    yaxis_title="Predicted Mood",
                    yaxis=dict(range=[0, 10])
                )
                
                st.plotly_chart(fig2, use_container_width=True)
    
    # Recent insights
    st.markdown("### 💡 Recent Insights")
    insights_list = firestore_client.get_insights(uid, limit=3)
    
    for insight in insights_list:
        with st.expander(f"Insight from {insight['created_at'].strftime('%B %d, %Y')}"):
            st.write(insight.get('insight', ''))


# Mood logging page
def show_mood_logger():
    st.markdown("<h1 class='gradient-text'>📝 Log Your Mood</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### How are you feeling today?")
        
        mood_score = st.slider(
            "Rate your mood (1-10)",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very Low, 10 = Excellent"
        )
        
        # Mood labels
        mood_labels = {
            range(1, 3): ("Very Low 😢", "#FF6B6B"),
            range(3, 5): ("Low 😕", "#FFA07A"),
            range(5, 7): ("Okay 😐", "#FFD93D"),
            range(7, 9): ("Good 😊", "#6BCF7F"),
            range(9, 11): ("Excellent 😄", "#4ECDC4")
        }
        
        for score_range, (label, color) in mood_labels.items():
            if mood_score in score_range:
                st.markdown(f"<h2 style='color: {color};'>{label}</h2>", unsafe_allow_html=True)
                break
        
        # Triggers
        st.markdown("### What's affecting your mood?")
        triggers = st.multiselect(
            "Select any triggers (optional)",
            ["Work Stress", "Relationship Issues", "Health Concerns", 
             "Financial Worries", "Social Anxiety", "Sleep Problems",
             "Family Conflict", "Loneliness", "Other"]
        )
        
        # Journal entry
        st.markdown("### Journal Entry")
        journal_text = st.text_area(
            "Write about your day, thoughts, or feelings...",
            height=200,
            placeholder="This is a safe space to express yourself..."
        )
        
        if st.button("Save Mood Entry", use_container_width=True):
            with st.spinner("Saving and analyzing..."):
                uid = st.session_state.user_data['uid']
                
                # Create mood entry
                mood_data = {
                    'mood_score': mood_score,
                    'triggers': triggers,
                    'journal_text': journal_text
                }
                
                # Analyze sentiment if journal text provided
                if journal_text:
                    sentiment_result = sentiment_analyzer.analyze_text(journal_text)
                    if sentiment_result['success']:
                        mood_data['ai_sentiment'] = sentiment_result['sentiment']
                        mood_data['ai_confidence'] = sentiment_result['confidence']
                        mood_data['mood_label'] = sentiment_result['mood_label']
                
                # Save to database
                entry_id = firestore_client.create_mood_entry(uid, mood_data)
                
                if entry_id:
                    # Generate AI insights
                    mood_history = firestore_client.get_mood_entries(uid, limit=10)
                    insight_result = openai_client.generate_coping_strategies(
                        mood_data,
                        {'recent_moods': [e['mood_score'] for e in mood_history]}
                    )
                    
                    if insight_result['success']:
                        # Save insight
                        firestore_client.save_insight(uid, {
                            'insight': insight_result['insight'],
                            'mood_score': mood_score,
                            'entry_id': entry_id
                        })
                        
                        st.success("✅ Mood entry saved successfully!")
                        
                        # Show insight
                        with col2:
                            st.markdown("### 💡 AI Insight")
                            st.info(insight_result['insight'])
                    else:
                        st.success("✅ Mood entry saved!")
                else:
                    st.error("Failed to save mood entry. Please try again.")
    
    with col2:
        st.markdown("### 🎯 Quick Tips")
        st.info("""
        **For better insights:**
        - Be honest about your feelings
        - Include specific details
        - Note what triggered your mood
        - Write regularly for patterns
        """)


# Main app
def main():
    load_custom_css()
    init_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"<h2 class='gradient-text'>Welcome back!</h2>", unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.user_data.get('email', 'User')}**")
            
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["📊 Dashboard", "📝 Log Mood", "💬 AI Chat", "📈 Insights", "⚙️ Settings"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_data = None
                st.rerun()
        
        # Show selected page
        if page == "📊 Dashboard":
            show_dashboard()
        elif page == "📝 Log Mood":
            show_mood_logger()
        elif page == "💬 AI Chat":
            st.markdown("<h1 class='gradient-text'>💬 AI Therapy Chat</h1>", unsafe_allow_html=True)
            st.info("🚧 AI Chat feature coming soon! This will provide conversational therapy support.")
        elif page == "📈 Insights":
            st.markdown("<h1 class='gradient-text'>📈 Detailed Insights</h1>", unsafe_allow_html=True)
            st.info("🚧 Detailed analytics coming soon!")
        elif page == "⚙️ Settings":
            st.markdown("<h1 class='gradient-text'>⚙️ Settings</h1>", unsafe_allow_html=True)
            st.info("🚧 Settings page coming soon!")


if __name__ == "__main__":
    main()
