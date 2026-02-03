"""
Enhanced Visualization Components
Advanced charts and visual analytics for mood tracking
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import calendar

def create_mood_calendar_heatmap(mood_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a calendar heatmap showing mood patterns
    """
    if not mood_data:
        return None
    
    # Prepare data
    df = pd.DataFrame(mood_data)
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['weekday'] = pd.to_datetime(df['created_at']).dt.dayofweek
    df['week'] = pd.to_datetime(df['created_at']).dt.isocalendar().week
    
    # Create calendar grid
    fig = go.Figure(data=go.Heatmap(
        z=df['mood_score'],
        x=df['weekday'],
        y=df['week'],
        colorscale=[
            [0, '#f5576c'],      # Red (low mood)
            [0.3, '#f093fb'],    # Pink
            [0.5, '#feca57'],    # Yellow
            [0.7, '#48dbfb'],    # Blue
            [1, '#38ef7d']       # Green (high mood)
        ],
        colorbar=dict(
            title="Mood",
            tickvals=[1, 3, 5, 7, 10],
            ticktext=['Very Low', 'Low', 'Neutral', 'Good', 'Excellent']
        ),
        hovertemplate='<b>Day %{x}</b><br>Week %{y}<br>Mood: %{z}/10<extra></extra>'
    ))
    
    fig.update_layout(
        title='Mood Calendar Heatmap',
        xaxis=dict(
            title='Day of Week',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ),
        yaxis=dict(title='Week'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig


def create_mood_distribution_chart(mood_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a pie chart showing mood distribution
    """
    if not mood_data:
        return None
    
    df = pd.DataFrame(mood_data)
    mood_counts = df['mood_label'].value_counts()
    
    colors = {
        'excellent': '#38ef7d',
        'good': '#48dbfb',
        'neutral': '#feca57',
        'low': '#f093fb',
        'very_low': '#f5576c'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=mood_counts.index,
        values=mood_counts.values,
        hole=0.4,
        marker=dict(colors=[colors.get(label.lower(), '#667eea') for label in mood_counts.index]),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Mood Distribution',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        height=400
    )
    
    return fig


def create_time_of_day_analysis(mood_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Analyze mood patterns by time of day
    """
    if not mood_data:
        return None
    
    df = pd.DataFrame(mood_data)
    df['hour'] = pd.to_datetime(df['created_at']).dt.hour
    
    # Group by hour
    hourly_mood = df.groupby('hour')['mood_score'].agg(['mean', 'count']).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hourly_mood['hour'],
        y=hourly_mood['mean'],
        name='Average Mood',
        marker=dict(
            color=hourly_mood['mean'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Mood Score")
        ),
        text=hourly_mood['mean'].round(1),
        textposition='outside',
        hovertemplate='<b>Hour: %{x}:00</b><br>Avg Mood: %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Mood Patterns by Time of Day',
        xaxis=dict(
            title='Hour of Day',
            tickvals=list(range(0, 24, 2)),
            ticktext=[f'{h}:00' for h in range(0, 24, 2)]
        ),
        yaxis=dict(title='Average Mood Score', range=[0, 10]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig


def create_trigger_frequency_chart(mood_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Show frequency of different mood triggers
    """
    if not mood_data:
        return None
    
    # Extract all triggers
    all_triggers = []
    for entry in mood_data:
        triggers = entry.get('triggers', [])
        if isinstance(triggers, list):
            all_triggers.extend(triggers)
    
    if not all_triggers:
        return None
    
    # Count triggers
    trigger_counts = pd.Series(all_triggers).value_counts().head(10)
    
    fig = go.Figure(data=[go.Bar(
        x=trigger_counts.values,
        y=trigger_counts.index,
        orientation='h',
        marker=dict(
            color=trigger_counts.values,
            colorscale='Viridis',
            showscale=False
        ),
        text=trigger_counts.values,
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Top Mood Triggers',
        xaxis=dict(title='Frequency'),
        yaxis=dict(title='Trigger'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig


def create_weekly_summary_chart(mood_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create weekly mood summary with trend
    """
    if not mood_data:
        return None
    
    df = pd.DataFrame(mood_data)
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['weekday'] = pd.to_datetime(df['created_at']).dt.day_name()
    
    # Calculate daily averages
    daily_avg = df.groupby(['date', 'weekday'])['mood_score'].mean().reset_index()
    daily_avg = daily_avg.sort_values('date')
    
    # Last 7 days
    last_7_days = daily_avg.tail(7)
    
    fig = go.Figure()
    
    # Bar chart
    fig.add_trace(go.Bar(
        x=last_7_days['weekday'],
        y=last_7_days['mood_score'],
        name='Daily Average',
        marker=dict(
            color=last_7_days['mood_score'],
            colorscale='RdYlGn',
            showscale=False
        ),
        text=last_7_days['mood_score'].round(1),
        textposition='outside'
    ))
    
    # Trend line
    fig.add_trace(go.Scatter(
        x=last_7_days['weekday'],
        y=last_7_days['mood_score'],
        mode='lines+markers',
        name='Trend',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#764ba2')
    ))
    
    fig.update_layout(
        title='Last 7 Days Mood Summary',
        xaxis=dict(title='Day'),
        yaxis=dict(title='Mood Score', range=[0, 10]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        height=400
    )
    
    return fig


def create_mood_streak_visual(streak_days: int) -> str:
    """
    Create visual representation of mood logging streak
    """
    if streak_days == 0:
        emoji = "🌱"
        message = "Start your journey today!"
    elif streak_days < 7:
        emoji = "🔥"
        message = f"{streak_days} day streak! Keep going!"
    elif streak_days < 30:
        emoji = "⭐"
        message = f"{streak_days} day streak! You're amazing!"
    elif streak_days < 100:
        emoji = "🏆"
        message = f"{streak_days} day streak! Incredible dedication!"
    else:
        emoji = "👑"
        message = f"{streak_days} day streak! You're a champion!"
    
    return f"{emoji} {message}"


def calculate_mood_insights(mood_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate various mood insights and statistics
    """
    if not mood_data:
        return {}
    
    df = pd.DataFrame(mood_data)
    
    insights = {
        'total_entries': len(df),
        'average_mood': df['mood_score'].mean(),
        'mood_range': df['mood_score'].max() - df['mood_score'].min(),
        'most_common_mood': df['mood_label'].mode()[0] if not df['mood_label'].mode().empty else 'N/A',
        'best_day': df.loc[df['mood_score'].idxmax(), 'created_at'] if len(df) > 0 else None,
        'worst_day': df.loc[df['mood_score'].idxmin(), 'created_at'] if len(df) > 0 else None,
        'mood_volatility': df['mood_score'].std(),
        'positive_days': len(df[df['mood_score'] >= 7]),
        'negative_days': len(df[df['mood_score'] <= 4]),
        'neutral_days': len(df[(df['mood_score'] > 4) & (df['mood_score'] < 7)])
    }
    
    # Trend calculation
    if len(df) >= 2:
        recent_avg = df.tail(7)['mood_score'].mean()
        older_avg = df.head(7)['mood_score'].mean()
        insights['trend'] = 'improving' if recent_avg > older_avg else 'declining' if recent_avg < older_avg else 'stable'
    else:
        insights['trend'] = 'insufficient_data'
    
    return insights
