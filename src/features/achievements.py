"""
Achievement and Gamification System
Track user progress, streaks, and milestones
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd


class AchievementSystem:
    """Manage user achievements and gamification"""
    
    ACHIEVEMENTS = {
        'first_entry': {
            'name': 'First Step',
            'description': 'Log your first mood entry',
            'emoji': '🌱',
            'points': 10
        },
        'week_streak': {
            'name': 'Week Warrior',
            'description': 'Log mood for 7 consecutive days',
            'emoji': '🔥',
            'points': 50
        },
        'month_streak': {
            'name': 'Monthly Master',
            'description': 'Log mood for 30 consecutive days',
            'emoji': '⭐',
            'points': 200
        },
        'hundred_streak': {
            'name': 'Century Champion',
            'description': 'Log mood for 100 consecutive days',
            'emoji': '👑',
            'points': 1000
        },
        'ten_entries': {
            'name': 'Getting Started',
            'description': 'Log 10 mood entries',
            'emoji': '📝',
            'points': 25
        },
        'fifty_entries': {
            'name': 'Dedicated Tracker',
            'description': 'Log 50 mood entries',
            'emoji': '📊',
            'points': 100
        },
        'hundred_entries': {
            'name': 'Mood Master',
            'description': 'Log 100 mood entries',
            'emoji': '🏆',
            'points': 300
        },
        'positive_week': {
            'name': 'Positive Vibes',
            'description': 'Maintain mood above 7 for a week',
            'emoji': '😊',
            'points': 75
        },
        'morning_person': {
            'name': 'Early Bird',
            'description': 'Log mood before 9 AM for 7 days',
            'emoji': '🌅',
            'points': 60
        },
        'night_owl': {
            'name': 'Night Owl',
            'description': 'Log mood after 9 PM for 7 days',
            'emoji': '🌙',
            'points': 60
        },
        'journal_master': {
            'name': 'Journaling Pro',
            'description': 'Write 20 journal entries',
            'emoji': '✍️',
            'points': 80
        },
        'trigger_aware': {
            'name': 'Self-Aware',
            'description': 'Identify triggers in 15 entries',
            'emoji': '🧠',
            'points': 70
        }
    }
    
    @staticmethod
    def calculate_streak(mood_data: List[Dict[str, Any]]) -> int:
        """Calculate current consecutive day streak"""
        if not mood_data:
            return 0
        
        df = pd.DataFrame(mood_data)
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        unique_dates = sorted(df['date'].unique(), reverse=True)
        
        if not unique_dates:
            return 0
        
        # Check if today or yesterday has an entry
        today = datetime.now().date()
        if unique_dates[0] not in [today, today - timedelta(days=1)]:
            return 0
        
        # Count consecutive days
        streak = 1
        current_date = unique_dates[0]
        
        for date in unique_dates[1:]:
            expected_date = current_date - timedelta(days=1)
            if date == expected_date:
                streak += 1
                current_date = date
            else:
                break
        
        return streak
    
    @staticmethod
    def check_achievements(mood_data: List[Dict[str, Any]], user_achievements: List[str] = None) -> Dict[str, Any]:
        """
        Check which achievements have been unlocked
        
        Returns:
            Dict with newly_unlocked, total_unlocked, and total_points
        """
        if user_achievements is None:
            user_achievements = []
        
        newly_unlocked = []
        df = pd.DataFrame(mood_data) if mood_data else pd.DataFrame()
        
        # First entry
        if 'first_entry' not in user_achievements and len(mood_data) >= 1:
            newly_unlocked.append('first_entry')
        
        # Streak achievements
        streak = AchievementSystem.calculate_streak(mood_data)
        if 'week_streak' not in user_achievements and streak >= 7:
            newly_unlocked.append('week_streak')
        if 'month_streak' not in user_achievements and streak >= 30:
            newly_unlocked.append('month_streak')
        if 'hundred_streak' not in user_achievements and streak >= 100:
            newly_unlocked.append('hundred_streak')
        
        # Entry count achievements
        total_entries = len(mood_data)
        if 'ten_entries' not in user_achievements and total_entries >= 10:
            newly_unlocked.append('ten_entries')
        if 'fifty_entries' not in user_achievements and total_entries >= 50:
            newly_unlocked.append('fifty_entries')
        if 'hundred_entries' not in user_achievements and total_entries >= 100:
            newly_unlocked.append('hundred_entries')
        
        # Positive week
        if 'positive_week' not in user_achievements and len(df) >= 7:
            last_7_days = df.tail(7)
            if all(last_7_days['mood_score'] >= 7):
                newly_unlocked.append('positive_week')
        
        # Morning person
        if 'morning_person' not in user_achievements and len(df) >= 7:
            df['hour'] = pd.to_datetime(df['created_at']).dt.hour
            last_7_days = df.tail(7)
            if all(last_7_days['hour'] < 9):
                newly_unlocked.append('morning_person')
        
        # Night owl
        if 'night_owl' not in user_achievements and len(df) >= 7:
            df['hour'] = pd.to_datetime(df['created_at']).dt.hour
            last_7_days = df.tail(7)
            if all(last_7_days['hour'] >= 21):
                newly_unlocked.append('night_owl')
        
        # Journal master
        if 'journal_master' not in user_achievements:
            journal_count = sum(1 for entry in mood_data if entry.get('journal_text'))
            if journal_count >= 20:
                newly_unlocked.append('journal_master')
        
        # Trigger aware
        if 'trigger_aware' not in user_achievements:
            trigger_count = sum(1 for entry in mood_data if entry.get('triggers'))
            if trigger_count >= 15:
                newly_unlocked.append('trigger_aware')
        
        # Calculate total points
        all_unlocked = list(set(user_achievements + newly_unlocked))
        total_points = sum(
            AchievementSystem.ACHIEVEMENTS[ach]['points'] 
            for ach in all_unlocked 
            if ach in AchievementSystem.ACHIEVEMENTS
        )
        
        return {
            'newly_unlocked': newly_unlocked,
            'total_unlocked': all_unlocked,
            'total_points': total_points,
            'streak': streak
        }
    
    @staticmethod
    def get_achievement_display(achievement_id: str) -> str:
        """Get formatted display string for an achievement"""
        if achievement_id not in AchievementSystem.ACHIEVEMENTS:
            return ""
        
        ach = AchievementSystem.ACHIEVEMENTS[achievement_id]
        return f"{ach['emoji']} **{ach['name']}** - {ach['description']} (+{ach['points']} pts)"
    
    @staticmethod
    def get_next_milestones(mood_data: List[Dict[str, Any]], user_achievements: List[str]) -> List[Dict[str, Any]]:
        """Get next achievable milestones"""
        milestones = []
        total_entries = len(mood_data)
        streak = AchievementSystem.calculate_streak(mood_data)
        
        # Streak milestones
        if 'week_streak' not in user_achievements and streak < 7:
            milestones.append({
                'name': 'Week Warrior',
                'progress': streak,
                'target': 7,
                'type': 'streak'
            })
        elif 'month_streak' not in user_achievements and streak < 30:
            milestones.append({
                'name': 'Monthly Master',
                'progress': streak,
                'target': 30,
                'type': 'streak'
            })
        elif 'hundred_streak' not in user_achievements and streak < 100:
            milestones.append({
                'name': 'Century Champion',
                'progress': streak,
                'target': 100,
                'type': 'streak'
            })
        
        # Entry milestones
        if 'ten_entries' not in user_achievements and total_entries < 10:
            milestones.append({
                'name': 'Getting Started',
                'progress': total_entries,
                'target': 10,
                'type': 'entries'
            })
        elif 'fifty_entries' not in user_achievements and total_entries < 50:
            milestones.append({
                'name': 'Dedicated Tracker',
                'progress': total_entries,
                'target': 50,
                'type': 'entries'
            })
        elif 'hundred_entries' not in user_achievements and total_entries < 100:
            milestones.append({
                'name': 'Mood Master',
                'progress': total_entries,
                'target': 100,
                'type': 'entries'
            })
        
        return milestones[:3]  # Return top 3 next milestones
