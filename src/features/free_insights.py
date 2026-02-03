"""
Free Tier Insights Generator
Rule-based insights and recommendations without OpenAI
"""

from typing import List, Dict, Any
import pandas as pd
from datetime import datetime, timedelta
import random


class FreeInsightsGenerator:
    """Generate insights using rule-based logic (no AI required)"""
    
    COPING_STRATEGIES = {
        'very_low': [
            "🌊 Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste.",
            "💙 Practice deep breathing: Inhale for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat 5 times.",
            "🚶 Take a short walk, even if it's just around your room. Movement can help shift your mood.",
            "📞 Reach out to someone you trust. Connection can make a big difference.",
            "🎵 Listen to calming music or sounds of nature.",
            "✍️ Write down your feelings without judgment. Sometimes expressing helps.",
            "🛁 Take a warm shower or bath to help relax your body and mind."
        ],
        'low': [
            "🌱 Start small: Do one tiny thing that usually makes you feel better.",
            "☀️ Get some sunlight or bright light exposure if possible.",
            "💧 Drink a glass of water - dehydration can affect mood.",
            "🧘 Try a 5-minute guided meditation or mindfulness exercise.",
            "📝 Make a list of 3 things you're grateful for today.",
            "🎨 Engage in a creative activity, even for just 10 minutes.",
            "🤗 Practice self-compassion - treat yourself as you would a good friend."
        ],
        'neutral': [
            "⚡ This is a good time to build positive habits. What small action could improve your day?",
            "📚 Learn something new or read something inspiring.",
            "🏃 Physical activity can boost your mood further. Try a quick workout or stretch.",
            "🎯 Set a small, achievable goal for today.",
            "🌟 Reflect on what's going well in your life right now.",
            "🤝 Connect with someone - send a message or make a call.",
            "🎭 Try something outside your comfort zone (in a safe way)."
        ],
        'good': [
            "🎉 Great mood! Consider what contributed to feeling this way.",
            "📸 Capture this moment - write about what made today good.",
            "💪 Use this positive energy to tackle something you've been putting off.",
            "🌈 Share your positive energy with others - it's contagious!",
            "🎁 Do something kind for yourself or someone else.",
            "🏆 Celebrate your wins, no matter how small.",
            "🌻 Spend time on activities that bring you joy."
        ],
        'excellent': [
            "✨ Wonderful! Take a moment to really savor this feeling.",
            "📝 Journal about what led to this excellent mood - it's valuable data!",
            "🎊 You're thriving! Consider how you can maintain this positive state.",
            "💫 Share your joy - positive emotions multiply when shared.",
            "🌟 This is a great time to work on your goals and dreams.",
            "🙏 Practice gratitude for the good things in your life.",
            "🎯 Set intentions for maintaining this positive momentum."
        ]
    }
    
    MINDFULNESS_EXERCISES = [
        {
            'name': 'Box Breathing',
            'duration': '2 minutes',
            'steps': [
                '1. Inhale slowly through your nose for 4 counts',
                '2. Hold your breath for 4 counts',
                '3. Exhale slowly through your mouth for 4 counts',
                '4. Hold for 4 counts',
                '5. Repeat for 2 minutes'
            ]
        },
        {
            'name': 'Body Scan',
            'duration': '5 minutes',
            'steps': [
                '1. Sit or lie down comfortably',
                '2. Close your eyes and take 3 deep breaths',
                '3. Focus on your toes, notice any sensations',
                '4. Slowly move attention up through your body',
                '5. Release tension as you notice it',
                '6. End at the top of your head'
            ]
        },
        {
            'name': 'Mindful Observation',
            'duration': '3 minutes',
            'steps': [
                '1. Choose an object nearby',
                '2. Observe it as if seeing it for the first time',
                '3. Notice colors, textures, shapes',
                '4. Let go of judgments, just observe',
                '5. Bring full attention to this moment'
            ]
        },
        {
            'name': 'Gratitude Reflection',
            'duration': '5 minutes',
            'steps': [
                '1. Think of 3 things you\'re grateful for',
                '2. For each, reflect on why it matters',
                '3. Notice how gratitude feels in your body',
                '4. Write them down if you wish',
                '5. Carry this feeling with you'
            ]
        }
    ]
    
    @staticmethod
    def generate_mood_insight(mood_data: Dict[str, Any], mood_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate personalized insight based on current mood"""
        mood_score = mood_data.get('mood_score', 5)
        mood_label = mood_data.get('mood_label', 'neutral')
        triggers = mood_data.get('triggers', [])
        
        # Get appropriate coping strategies
        strategies = FreeInsightsGenerator.COPING_STRATEGIES.get(mood_label, 
                                                                  FreeInsightsGenerator.COPING_STRATEGIES['neutral'])
        selected_strategies = random.sample(strategies, min(3, len(strategies)))
        
        # Generate acknowledgment
        acknowledgments = {
            'very_low': "I see you're going through a difficult time right now. That takes courage to acknowledge.",
            'low': "It sounds like things are challenging at the moment. Your feelings are valid.",
            'neutral': "You're in a balanced state right now. This is a good foundation to build on.",
            'good': "You're feeling positive today! That's wonderful to see.",
            'excellent': "You're experiencing an excellent mood! This is fantastic!"
        }
        
        acknowledgment = acknowledgments.get(mood_label, "Thank you for checking in with yourself.")
        
        # Analyze triggers if present
        trigger_insight = ""
        if triggers:
            trigger_insight = f"\n\n**Triggers Identified:** {', '.join(triggers)}\n"
            trigger_insight += "Being aware of your triggers is an important step in managing your mental wellness."
        
        # Get a mindfulness exercise
        exercise = random.choice(FreeInsightsGenerator.MINDFULNESS_EXERCISES)
        
        # Build insight text
        insight_text = f"""
{acknowledgment}

**Mood Score:** {mood_score}/10 ({mood_label.replace('_', ' ').title()})
{trigger_insight}

### 💡 Personalized Strategies

{chr(10).join(f'{i+1}. {strategy}' for i, strategy in enumerate(selected_strategies))}

### 🧘 Recommended Exercise: {exercise['name']}
**Duration:** {exercise['duration']}

{chr(10).join(exercise['steps'])}

### 🌟 Remember
You're taking an important step by tracking your mental wellness. Every entry helps you understand yourself better.
"""
        
        # Add trend analysis if history available
        if mood_history and len(mood_history) > 1:
            df = pd.DataFrame(mood_history)
            recent_avg = df.tail(7)['mood_score'].mean()
            older_avg = df.head(max(7, len(df)//2))['mood_score'].mean()
            
            if recent_avg > older_avg + 0.5:
                trend_text = "\n\n📈 **Positive Trend:** Your mood has been improving recently! Keep up the great work."
            elif recent_avg < older_avg - 0.5:
                trend_text = "\n\n📉 **Trend Notice:** Your mood has been lower recently. Consider reaching out for support if needed."
            else:
                trend_text = "\n\n📊 **Stable Trend:** Your mood has been relatively stable."
            
            insight_text += trend_text
        
        return {
            'success': True,
            'insight': insight_text,
            'mood_score': mood_score,
            'mood_label': mood_label,
            'strategies': selected_strategies,
            'exercise': exercise,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_weekly_report(mood_history: List[Dict[str, Any]]) -> str:
        """Generate a weekly mood report"""
        if not mood_history:
            return "Not enough data for a weekly report. Keep logging your moods!"
        
        df = pd.DataFrame(mood_history)
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        
        # Last 7 days
        week_ago = datetime.now().date() - timedelta(days=7)
        weekly_data = df[df['date'] >= week_ago]
        
        if len(weekly_data) == 0:
            return "No mood entries in the past week. Start logging to see your weekly report!"
        
        # Calculate statistics
        avg_mood = weekly_data['mood_score'].mean()
        highest_mood = weekly_data['mood_score'].max()
        lowest_mood = weekly_data['mood_score'].min()
        total_entries = len(weekly_data)
        
        # Mood distribution
        mood_counts = weekly_data['mood_label'].value_counts()
        
        # Generate report
        report = f"""
# 📊 Your Weekly Mood Report

**Period:** Last 7 Days
**Total Entries:** {total_entries}

## 📈 Statistics

- **Average Mood:** {avg_mood:.1f}/10
- **Highest Mood:** {highest_mood}/10
- **Lowest Mood:** {lowest_mood}/10
- **Mood Range:** {highest_mood - lowest_mood} points

## 🎯 Mood Distribution

{chr(10).join(f'- **{mood.replace("_", " ").title()}:** {count} days' for mood, count in mood_counts.items())}

## 💡 Insights

"""
        
        # Add personalized insights
        if avg_mood >= 7:
            report += "✨ You've had a great week! Your average mood is in the positive range. Keep doing what you're doing!\n\n"
        elif avg_mood >= 5:
            report += "⚖️ Your week has been balanced. There's room for improvement, and you're on the right track.\n\n"
        else:
            report += "💙 This week has been challenging. Remember that it's okay to have difficult periods. Consider reaching out for support.\n\n"
        
        # Consistency insight
        if total_entries >= 6:
            report += "🏆 **Great consistency!** You logged your mood {total_entries} times this week. This dedication helps you understand your patterns better.\n\n"
        elif total_entries >= 3:
            report += "📝 **Good effort!** Try to log your mood daily for even better insights.\n\n"
        else:
            report += "🌱 **Keep building the habit!** Daily logging provides the most valuable insights.\n\n"
        
        # Recommendations
        report += """
## 🎯 Recommendations for Next Week

1. Continue tracking your mood daily
2. Pay attention to patterns and triggers
3. Practice the mindfulness exercises provided
4. Celebrate your progress, no matter how small
5. Be kind to yourself throughout the journey

Remember: Progress isn't always linear, and that's okay! 💚
"""
        
        return report
