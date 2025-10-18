#!/usr/bin/env python3
"""
Happiness Suggestions System for Healo Mental Health Chatbot
Provides contextual happiness suggestions based on user conversations
"""

import random
import re
from typing import List, Dict, Tuple

class HappinessSuggestionEngine:
    def __init__(self):
        self.happiness_keywords = {
            'gratitude': ['grateful', 'thankful', 'appreciate', 'blessed', 'fortunate'],
            'social': ['friends', 'family', 'lonely', 'alone', 'social', 'connection', 'relationship'],
            'activity': ['bored', 'active', 'exercise', 'hobby', 'interest', 'fun', 'enjoy'],
            'mindfulness': ['stressed', 'overwhelmed', 'mindful', 'present', 'meditation', 'calm'],
            'purpose': ['purpose', 'meaning', 'goal', 'dream', 'future', 'direction', 'motivation'],
            'self_care': ['tired', 'exhausted', 'self-care', 'rest', 'sleep', 'health', 'wellness'],
            'achievement': ['accomplish', 'success', 'proud', 'achievement', 'progress', 'goal'],
            'nature': ['nature', 'outdoor', 'walk', 'park', 'garden', 'fresh air', 'sunshine'],
            'creativity': ['creative', 'art', 'music', 'write', 'draw', 'craft', 'express'],
            'helping': ['help', 'volunteer', 'kindness', 'service', 'support', 'give']
        }
        
        self.happiness_activities = {
            'gratitude': [
                "Write down three things you're grateful for today",
                "Send a thank you message to someone who helped you",
                "Keep a gratitude journal for one week",
                "Tell someone why you appreciate them",
                "Reflect on a positive memory from this week"
            ],
            'social': [
                "Call or text a friend you haven't spoken to in a while",
                "Plan a coffee date with someone you care about",
                "Join a club or group that interests you",
                "Volunteer for a cause you believe in",
                "Host a small gathering with close friends"
            ],
            'activity': [
                "Try a new hobby or activity you've been curious about",
                "Go for a 30-minute walk in your neighborhood",
                "Dance to your favorite song for 10 minutes",
                "Learn something new online or take a class",
                "Play a game or do a puzzle"
            ],
            'mindfulness': [
                "Practice 5 minutes of deep breathing",
                "Try a 10-minute meditation or mindfulness exercise",
                "Take a mindful walk, noticing your surroundings",
                "Practice the 5-4-3-2-1 grounding technique",
                "Spend 5 minutes in nature without distractions"
            ],
            'purpose': [
                "Write down one goal you want to achieve this month",
                "Reflect on what gives your life meaning",
                "Take one small step toward a dream you have",
                "Help someone else with a task or problem",
                "Volunteer for a cause that matters to you"
            ],
            'self_care': [
                "Take a relaxing bath or shower",
                "Get 7-8 hours of sleep tonight",
                "Eat a nutritious meal that makes you feel good",
                "Spend 30 minutes doing something you love",
                "Practice saying no to something that drains you"
            ],
            'achievement': [
                "Celebrate a recent accomplishment, no matter how small",
                "Set a small, achievable goal for this week",
                "Make a list of your strengths and talents",
                "Complete one task you've been putting off",
                "Share your success with someone who supports you"
            ],
            'nature': [
                "Spend 20 minutes outside in nature",
                "Watch a sunrise or sunset",
                "Visit a local park or garden",
                "Take photos of beautiful things around you",
                "Have a picnic or outdoor meal"
            ],
            'creativity': [
                "Draw, paint, or create something artistic",
                "Write in a journal or try creative writing",
                "Listen to music that uplifts your mood",
                "Cook or bake something new and delicious",
                "Take photos or create a digital collage"
            ],
            'helping': [
                "Perform a random act of kindness for someone",
                "Volunteer your time for a good cause",
                "Help a friend or family member with something",
                "Donate items you no longer need",
                "Compliment three people today"
            ]
        }
        
        self.encouragement_phrases = [
            "You've got this!",
            "I believe in you!",
            "You're stronger than you know!",
            "Every small step counts!",
            "You're doing great!",
            "I'm proud of you for trying!",
            "You deserve happiness!",
            "You're not alone in this!",
            "Your feelings are valid!",
            "You're making progress!"
        ]
    
    def analyze_conversation_context(self, user_input: str, conversation_history: List[Dict]) -> List[str]:
        """Analyze conversation context to suggest relevant happiness activities"""
        context = user_input.lower()
        
        # Analyze recent conversation history for context
        recent_context = ""
        if conversation_history:
            recent_messages = conversation_history[-3:]  # Last 3 messages
            recent_context = " ".join([msg.get('message', '') for msg in recent_messages]).lower()
        
        full_context = f"{context} {recent_context}"
        
        # Identify relevant happiness categories
        relevant_categories = []
        for category, keywords in self.happiness_keywords.items():
            if any(keyword in full_context for keyword in keywords):
                relevant_categories.append(category)
        
        # If no specific categories found, suggest general happiness activities
        if not relevant_categories:
            relevant_categories = ['gratitude', 'activity', 'mindfulness']
        
        # Generate suggestions
        suggestions = []
        for category in relevant_categories[:3]:  # Limit to top 3 categories
            if category in self.happiness_activities:
                suggestions.extend(random.sample(self.happiness_activities[category], 2))
        
        # Add encouragement
        if suggestions:
            suggestions.append(random.choice(self.encouragement_phrases))
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def get_mood_based_suggestions(self, mood: str) -> List[str]:
        """Get happiness suggestions based on detected mood"""
        mood_suggestions = {
            'sad': [
                "Listen to uplifting music that makes you want to dance",
                "Call a friend who always makes you laugh",
                "Watch a funny movie or comedy show",
                "Write down three things that made you smile today",
                "Do something kind for someone else"
            ],
            'anxious': [
                "Practice the 4-7-8 breathing technique (inhale 4, hold 7, exhale 8)",
                "Take a walk in nature and focus on your surroundings",
                "Try progressive muscle relaxation",
                "Write down your worries and then let them go",
                "Listen to calming music or nature sounds"
            ],
            'angry': [
                "Go for a brisk walk or run to release energy",
                "Write a letter expressing your feelings (don't send it)",
                "Practice deep breathing for 5 minutes",
                "Listen to music that matches your energy level",
                "Do something physical like cleaning or organizing"
            ],
            'lonely': [
                "Reach out to someone you care about",
                "Join an online community related to your interests",
                "Volunteer for a cause you believe in",
                "Plan a virtual hangout with friends",
                "Write a letter to someone special"
            ],
            'overwhelmed': [
                "Make a simple to-do list with just 3 items",
                "Take a 10-minute break to do something you enjoy",
                "Practice the 5-4-3-2-1 grounding technique",
                "Ask for help with one task",
                "Focus on just one thing at a time"
            ],
            'confused': [
                "Write down your thoughts to organize them",
                "Talk to someone you trust about your situation",
                "Take a step back and give yourself time to think",
                "Break down big decisions into smaller parts",
                "Seek advice from someone with experience"
            ],
            'happy': [
                "Share your happiness with others",
                "Do something that makes you feel accomplished",
                "Plan something fun for the future",
                "Help someone else feel happy too",
                "Celebrate your positive mood with a special treat"
            ],
            'neutral': [
                "Try something new and exciting",
                "Connect with someone you care about",
                "Do something creative or artistic",
                "Spend time in nature",
                "Set a small goal for today"
            ]
        }
        
        return mood_suggestions.get(mood, mood_suggestions['neutral'])
    
    def generate_happiness_plan(self, user_goals: List[str]) -> Dict[str, List[str]]:
        """Generate a personalized happiness plan based on user goals"""
        plan = {
            'daily_activities': [],
            'weekly_goals': [],
            'monthly_aspirations': [],
            'encouragement': []
        }
        
        # Daily activities (quick wins)
        plan['daily_activities'] = [
            "Start each day with one thing you're grateful for",
            "Take 5 deep breaths when you wake up",
            "Do one small act of kindness",
            "Spend 10 minutes doing something you enjoy",
            "End the day by writing down one good thing that happened"
        ]
        
        # Weekly goals (moderate commitment)
        plan['weekly_goals'] = [
            "Connect with a friend or family member",
            "Try a new activity or hobby",
            "Spend time in nature",
            "Practice mindfulness or meditation",
            "Help someone else with something"
        ]
        
        # Monthly aspirations (longer-term)
        plan['monthly_aspirations'] = [
            "Set and work toward a personal goal",
            "Volunteer for a cause you care about",
            "Learn a new skill or take a class",
            "Plan a special experience or trip",
            "Reflect on your growth and progress"
        ]
        
        # Add encouragement
        plan['encouragement'] = [
            "Remember that happiness is a journey, not a destination",
            "Every small step you take matters",
            "You deserve to feel happy and fulfilled",
            "It's okay to have difficult days - they make the good ones sweeter",
            "You have the power to create positive change in your life"
        ]
        
        return plan
    
    def get_quick_happiness_boost(self) -> str:
        """Get a quick happiness boost suggestion"""
        quick_boosts = [
            "Take 3 deep breaths and smile",
            "Listen to your favorite song",
            "Text someone you love",
            "Look at photos of happy memories",
            "Do 10 jumping jacks",
            "Write down one thing you're grateful for",
            "Step outside and feel the fresh air",
            "Give yourself a compliment",
            "Call someone who makes you laugh",
            "Do something creative for 5 minutes"
        ]
        
        return random.choice(quick_boosts)
    
    def suggest_happiness_habits(self) -> List[Dict[str, str]]:
        """Suggest happiness-building habits"""
        habits = [
            {
                'habit': 'Gratitude Practice',
                'description': 'Write down 3 things you\'re grateful for each day',
                'benefit': 'Increases positive emotions and life satisfaction'
            },
            {
                'habit': 'Daily Movement',
                'description': 'Get at least 20 minutes of physical activity',
                'benefit': 'Releases endorphins and improves mood'
            },
            {
                'habit': 'Mindful Moments',
                'description': 'Take 5 minutes daily for mindfulness or meditation',
                'benefit': 'Reduces stress and increases present-moment awareness'
            },
            {
                'habit': 'Social Connection',
                'description': 'Reach out to one person each day',
                'benefit': 'Strengthens relationships and reduces loneliness'
            },
            {
                'habit': 'Acts of Kindness',
                'description': 'Do one kind thing for someone else daily',
                'benefit': 'Increases happiness and sense of purpose'
            },
            {
                'habit': 'Learning Something New',
                'description': 'Spend 15 minutes learning or practicing a skill',
                'benefit': 'Boosts confidence and provides sense of accomplishment'
            },
            {
                'habit': 'Nature Time',
                'description': 'Spend time outdoors in nature regularly',
                'benefit': 'Reduces stress and improves mental well-being'
            },
            {
                'habit': 'Quality Sleep',
                'description': 'Maintain consistent sleep schedule',
                'benefit': 'Improves mood, energy, and overall health'
            }
        ]
        
        return random.sample(habits, 3)  # Return 3 random habits
