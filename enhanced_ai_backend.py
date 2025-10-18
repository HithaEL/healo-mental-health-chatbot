#!/usr/bin/env python3
"""
Enhanced AI Backend for Healo Mental Health Chatbot
Improved BERT-like functionality with better response generation
"""

import json
import csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import re
import random
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

class EnhancedMentalHealthAI:
    def __init__(self, dataset_path: str = 'mental_health_responses.csv'):
        self.dataset_path = dataset_path
        self.dataset = []
        self.vectorizer = TfidfVectorizer(
            max_features=2000,  # Increased from 1000
            stop_words='english',
            ngram_range=(1, 3),  # Increased from (1, 2)
            min_df=1,  # Decreased from 2
            max_df=0.8,  # Added to filter common words
            sublinear_tf=True  # Added for better scaling
        )
        self.tfidf_matrix = None
        self.mood_patterns = {
            'anxious': [
                'anxious', 'anxiety', 'worried', 'nervous', 'panic', 'scared', 
                'fear', 'afraid', 'uneasy', 'restless', 'tense', 'stressed',
                'apprehensive', 'frightened', 'terrified', 'jittery', 'on edge'
            ],
            'depressed': [
                'depressed', 'depression', 'sad', 'down', 'hopeless', 'empty', 
                'worthless', 'suicidal', 'miserable', 'gloomy', 'blue', 'low',
                'despair', 'dejected', 'melancholy', 'sorrowful', 'grief'
            ],
            'stressed': [
                'stressed', 'stress', 'overwhelmed', 'pressure', 'burnout', 
                'exhausted', 'tired', 'drained', 'frazzled', 'swamped',
                'burdened', 'strained', 'tension', 'pressure', 'overloaded'
            ],
            'angry': [
                'angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 
                'rage', 'livid', 'upset', 'hostile', 'bitter', 'resentful',
                'enraged', 'incensed', 'outraged', 'indignant'
            ],
            'happy': [
                'happy', 'good', 'great', 'wonderful', 'amazing', 'excited', 
                'joyful', 'positive', 'cheerful', 'content', 'pleased', 'delighted',
                'elated', 'thrilled', 'ecstatic', 'blissful', 'euphoric'
            ],
            'lonely': [
                'lonely', 'alone', 'isolated', 'disconnected', 'abandoned',
                'secluded', 'solitary', 'lonesome', 'forlorn', 'desolate'
            ],
            'confused': [
                'confused', 'lost', 'uncertain', 'unclear', 'bewildered',
                'perplexed', 'puzzled', 'disoriented', 'muddled', 'mixed up'
            ]
        }
        
        self.load_dataset()
        self.train_model()
        self.add_enhanced_responses()
    
    def load_dataset(self):
        """Load and preprocess the training dataset"""
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) >= 3:
                        self.dataset.append({
                            'input': self.clean_text(row[0]),
                            'friend_response': self.clean_text(row[1]),
                            'professional_response': self.clean_text(row[2])
                        })
            
            print(f"Loaded {len(self.dataset)} training examples")
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.dataset = self.get_fallback_dataset()
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra quotes and clean up
        text = text.replace('"', '').replace("'", "'")
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        # Remove or replace problematic Unicode characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text
    
    def add_enhanced_responses(self):
        """Add more comprehensive mental health responses"""
        enhanced_responses = [
            {
                'input': 'i feel anxious about my job interview',
                'friend_response': 'job interviews can be really nerve wracking! i totally get that anxious feeling. what specifically is making you most nervous about it?',
                'professional_response': 'job interview anxiety is very common and understandable. it might help to practice common questions and prepare talking points about your experience. what aspects of the interview are causing you the most concern?'
            },
            {
                'input': 'i am feeling really depressed lately',
                'friend_response': 'i am really sorry you are going through this. depression can feel so heavy and isolating. how long have you been feeling this way? you are not alone in this.',
                'professional_response': 'depression can significantly impact your daily life and well being. it is important to consider professional help if these feelings persist. have you noticed changes in your sleep, appetite, or interest in activities you used to enjoy?'
            },
            {
                'input': 'i am stressed about work and cannot handle it',
                'friend_response': 'work stress can be absolutely overwhelming sometimes. it sounds like you are really feeling the pressure. what specific aspects of work are making you feel this way?',
                'professional_response': 'work related stress can affect both your mental and physical health. it might be helpful to identify specific stressors and develop coping strategies. have you considered discussing workload concerns with your supervisor or hr department?'
            },
            {
                'input': 'i feel lonely and have no friends',
                'friend_response': 'feeling lonely can be really tough, especially when it feels like everyone else has friends. loneliness is more common than people think. what has been making it hard to connect with others?',
                'professional_response': 'loneliness can have significant impacts on mental health. building social connections takes time and effort. have you considered joining groups or activities that align with your interests? sometimes starting with small social interactions can help build confidence.'
            },
            {
                'input': 'i am confused about my life direction',
                'friend_response': 'feeling confused about life direction is totally normal, especially during big transitions. it can be overwhelming when you are not sure which path to take. what areas of your life are you most uncertain about?',
                'professional_response': 'life transitions and uncertainty about direction are common experiences. it might help to break down your goals into smaller, manageable steps. have you considered exploring your values and interests to help guide your decisions?'
            },
            {
                'input': 'i am angry at my family',
                'friend_response': 'family conflicts can be really frustrating and hurtful. it is okay to feel angry when family relationships are difficult. what has been happening that is making you feel this way?',
                'professional_response': 'family conflicts can be emotionally challenging and complex. it is important to express your feelings in healthy ways. have you considered family therapy or individual counseling to help navigate these relationships?'
            },
            {
                'input': 'i cannot sleep at night',
                'friend_response': 'insomnia is the worst! i have been there too. not being able to sleep can make everything else feel so much harder. what do you think might be keeping you up at night?',
                'professional_response': 'sleep disturbances can significantly impact your mental and physical health. establishing a consistent bedtime routine and avoiding screens before bed can help. have you tried relaxation techniques like deep breathing or meditation?'
            },
            {
                'input': 'i feel overwhelmed by everything',
                'friend_response': 'feeling overwhelmed is so exhausting. when everything feels like too much, it can be hard to know where to start. what is making you feel most overwhelmed right now?',
                'professional_response': 'feeling overwhelmed can be a sign that you are taking on too much at once. it might help to prioritize tasks and break them down into smaller steps. have you considered using time management techniques or asking for help with some responsibilities?'
            },
            {
                'input': 'i am having relationship problems',
                'friend_response': 'relationship issues can be really tough to navigate. it sounds like you are going through a difficult time. what has been happening in your relationship?',
                'professional_response': 'relationship challenges can be emotionally taxing and complex. open communication and understanding each others perspectives are key. have you and your partner considered couples counseling to help work through these issues?'
            },
            {
                'input': 'i feel like giving up',
                'friend_response': 'i am really sorry you are feeling this way. when things feel hopeless, it can be so hard to see a way forward. you are not alone, and these feelings are valid. what has been making you feel like giving up?',
                'professional_response': 'feeling like giving up can be a sign of significant emotional distress. it is important to reach out for support during these times. have you considered speaking with a mental health professional or trusted friend about these feelings?'
            }
        ]
        
        # Add enhanced responses to dataset
        for response in enhanced_responses:
            self.dataset.append(response)
        
        print(f"Added {len(enhanced_responses)} enhanced responses. Total dataset size: {len(self.dataset)}")
    
    def get_fallback_dataset(self) -> List[Dict]:
        """Fallback dataset if CSV loading fails"""
        return [
            {
                'input': 'i feel anxious',
                'friend_response': 'i totally get that feeling! anxiety can be really overwhelming. what is making you feel anxious right now?',
                'professional_response': 'anxiety is a common experience. can you tell me more about what specific situations or thoughts are triggering these feelings?'
            },
            {
                'input': 'i am stressed about work',
                'friend_response': 'work stress is the worst! it can really take a toll on you. have you tried any relaxation techniques?',
                'professional_response': 'work related stress is very common. it might help to identify specific stressors and develop coping strategies. what aspects of work are most challenging?'
            },
            {
                'input': 'i feel depressed',
                'friend_response': 'i am really sorry you are going through this. depression is tough, but you are not alone. how long have you been feeling this way?',
                'professional_response': 'depression can significantly impact daily functioning. it is important to seek professional help if these feelings persist. have you noticed changes in sleep, appetite, or energy levels?'
            }
        ]
    
    def train_model(self):
        """Train the enhanced TF-IDF model"""
        if not self.dataset:
            return
        
        # Extract input texts for training
        input_texts = [item['input'] for item in self.dataset]
        
        # Fit TF-IDF vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(input_texts)
        print("Enhanced TF-IDF model trained successfully")
    
    def analyze_mood(self, text: str) -> str:
        """Enhanced mood analysis with more patterns"""
        text_lower = text.lower()
        mood_scores = {}
        
        for mood, keywords in self.mood_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            mood_scores[mood] = score
        
        # Return the mood with highest score, default to neutral
        if max(mood_scores.values()) > 0:
            return max(mood_scores, key=mood_scores.get)
        return 'neutral'
    
    def find_best_match(self, user_input: str) -> Dict:
        """Enhanced semantic matching with better thresholds"""
        if not self.dataset or self.tfidf_matrix is None:
            return None
        
        # Clean and vectorize user input
        cleaned_input = self.clean_text(user_input)
        input_vector = self.vectorizer.transform([cleaned_input])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
        
        # Find the best match with improved threshold
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Lower threshold for better matching
        if best_similarity > 0.05:  # Lowered from 0.1
            return self.dataset[best_match_idx]
        
        return None
    
    def generate_response(self, user_input: str, mode: str = 'friend') -> str:
        """Generate enhanced response with better fallbacks"""
        # Find best match from dataset
        best_match = self.find_best_match(user_input)
        
        if best_match:
            return best_match[f'{mode}_response']
        
        # Generate contextual response based on mood
        mood = self.analyze_mood(user_input)
        return self.generate_contextual_response(user_input, mood, mode)
    
    def generate_contextual_response(self, user_input: str, mood: str, mode: str) -> str:
        """Enhanced contextual responses with more variety"""
        responses = {
            'anxious': {
                'friend': [
                    "I can hear that you're feeling anxious. That's totally valid! What's on your mind that's making you feel this way?",
                    "Anxiety can be really overwhelming sometimes. You're not alone in this. What's triggering these feelings for you?",
                    "I totally get that anxious feeling! It can be scary. What would help you feel more grounded right now?",
                    "Feeling anxious is so hard. When my mind starts racing, it helps to take things one step at a time. What's the biggest worry on your mind?"
                ],
                'professional': [
                    "Anxiety can be challenging to manage. It might help to practice deep breathing or grounding techniques. What specific thoughts or situations are contributing to your anxiety?",
                    "I understand you're experiencing anxiety. It's important to identify triggers and develop coping strategies. What techniques have you tried before?",
                    "Anxiety is a common experience that can be managed with the right tools. What specific symptoms are you noticing?",
                    "It's helpful to understand what triggers your anxiety. Have you noticed any patterns in when these feelings occur?"
                ]
            },
            'depressed': {
                'friend': [
                    "I'm really sorry you're going through a tough time. Depression can feel isolating, but you're not alone. How long have you been feeling this way?",
                    "That sounds really hard. Depression is tough, but there are people who care about you. What's been weighing on your mind lately?",
                    "I'm here for you. Depression can make everything feel heavy. What would help you feel even a little bit better today?",
                    "I can't imagine how hard this must be for you. Depression is so much more than just feeling sad. What's been the hardest part lately?"
                ],
                'professional': [
                    "Depression can significantly impact your daily life. It's important to consider professional help if these feelings persist. Have you noticed changes in your sleep, appetite, or interest in activities?",
                    "I appreciate you sharing this with me. Depression is a serious condition that often requires professional support. What symptoms are you experiencing?",
                    "Depression affects many people, and seeking help is a sign of strength. Have you considered speaking with a mental health professional?",
                    "It's important to monitor these feelings and their impact on your daily functioning. How long have you been experiencing these symptoms?"
                ]
            },
            'stressed': {
                'friend': [
                    "Stress can really take a toll on you! What's been stressing you out lately? Sometimes talking about it helps.",
                    "I hear you on the stress front! It can feel overwhelming. What's the biggest stressor for you right now?",
                    "Stress is no joke! What would help you feel more in control of the situation?",
                    "When I'm stressed, everything feels like too much. What's making you feel most overwhelmed right now?"
                ],
                'professional': [
                    "Chronic stress can affect both physical and mental health. Identifying stress triggers and developing coping strategies is important. What areas of your life are causing the most stress?",
                    "Stress management is crucial for overall well-being. What stress management techniques have you tried, and which ones work best for you?",
                    "It's important to address stress before it becomes overwhelming. What specific situations are contributing to your stress levels?",
                    "Long-term stress can have serious health implications. Have you considered stress reduction techniques like mindfulness or time management?"
                ]
            },
            'angry': {
                'friend': [
                    "I can tell you're feeling really frustrated right now. What's got you feeling this way?",
                    "Anger can be a tough emotion to deal with. What's making you feel so upset?",
                    "I hear that you're angry. Sometimes it helps to talk through what's bothering you.",
                    "Feeling angry is totally valid. What's been building up that's making you feel this way?"
                ],
                'professional': [
                    "Anger is a natural emotion, but it's important to express it in healthy ways. What's triggering these feelings for you?",
                    "I understand you're experiencing anger. It can be helpful to identify the underlying causes and develop healthy coping strategies. What's contributing to these feelings?",
                    "Anger management is an important skill. What techniques have you used in the past to handle difficult emotions?",
                    "It's important to understand what's behind your anger. Have you noticed any patterns in what triggers these feelings?"
                ]
            },
            'lonely': {
                'friend': [
                    "Feeling lonely can be really tough. It sounds like you're craving connection. What's been making it hard to feel connected to others?",
                    "Loneliness is so much more common than people think. You're not alone in feeling alone. What would help you feel more connected?",
                    "I get that lonely feeling too sometimes. It can feel really isolating. What kind of connection are you looking for?",
                    "Being lonely is hard, especially when it feels like everyone else has people. What's been making it difficult to reach out?"
                ],
                'professional': [
                    "Loneliness can have significant impacts on mental health. Building social connections takes time and effort. Have you considered joining groups or activities that align with your interests?",
                    "Loneliness is a common experience that can be addressed. Sometimes starting with small social interactions can help build confidence. What social activities interest you?",
                    "It's important to address feelings of loneliness as they can impact overall well-being. Have you tried reaching out to existing contacts or exploring new social opportunities?",
                    "Loneliness can be both a cause and effect of mental health challenges. What barriers do you feel are preventing you from connecting with others?"
                ]
            },
            'confused': {
                'friend': [
                    "Feeling confused about life direction is totally normal! It can be overwhelming when you're not sure which path to take. What areas are you most uncertain about?",
                    "Confusion can be really frustrating. It's okay to not have all the answers. What's making you feel most lost right now?",
                    "I've been there with the confusion too. Sometimes it helps to break things down into smaller pieces. What's the biggest question on your mind?",
                    "Feeling confused is part of being human. What would help you feel more clear about your situation?"
                ],
                'professional': [
                    "Life transitions and uncertainty about direction are common experiences. It might help to break down your goals into smaller, manageable steps. What areas of your life are you most uncertain about?",
                    "Confusion about life direction can be addressed through self-reflection and goal-setting. Have you considered exploring your values and interests to help guide your decisions?",
                    "It's normal to feel uncertain during major life transitions. What specific aspects of your life are causing the most confusion?",
                    "Clarifying your goals and values can help reduce confusion about life direction. What questions are you trying to answer about your future?"
                ]
            },
            'happy': {
                'friend': [
                    "That's wonderful to hear! I'm so glad you're feeling good. What's been going well for you lately?",
                    "I love hearing that you're in a good mood! What's making you feel so positive today?",
                    "That's awesome! It's great when things are going well. What's been the highlight of your day?",
                    "I'm so happy to hear you're doing well! What's been bringing you joy lately?"
                ],
                'professional': [
                    "It's wonderful that you're experiencing positive emotions. Maintaining this positive state can be beneficial for your overall well-being. What factors are contributing to your current mood?",
                    "Positive emotions are important for mental health. It's great that you're feeling good. What strategies or activities help you maintain this positive state?",
                    "I'm glad to hear you're doing well. It's important to recognize and appreciate positive moments. What's been working well for you recently?",
                    "Maintaining positive mental health is an ongoing process. What practices or activities have been most helpful for your well-being?"
                ]
            },
            'neutral': {
                'friend': [
                    "Thanks for sharing that with me. I'm here to listen and help however I can. What else is on your mind?",
                    "I appreciate you opening up. What would you like to talk about today?",
                    "I'm here for you. What's going on in your world right now?",
                    "Thanks for reaching out. What's on your mind that you'd like to discuss?"
                ],
                'professional': [
                    "I appreciate you sharing that with me. It's important to express your feelings and concerns. Is there anything specific you'd like to discuss or work through?",
                    "Thank you for being open with me. How can I best assist you in this moment?",
                    "I'm here to help you work through whatever you're experiencing. What would you like to focus on today?",
                    "It's important to address whatever is on your mind. What would be most helpful for you to discuss right now?"
                ]
            }
        }
        
        mood_responses = responses.get(mood, responses['neutral'])
        mode_responses = mood_responses.get(mode, mood_responses['friend'])
        
        return random.choice(mode_responses)
    
    def get_suggestions(self, mood: str) -> List[str]:
        """Enhanced suggestions based on mood"""
        suggestions = {
            'anxious': [
                "Try some deep breathing exercises",
                "Practice mindfulness meditation",
                "Take a short walk outside",
                "Listen to calming music",
                "Write down your worries",
                "Try progressive muscle relaxation"
            ],
            'depressed': [
                "Reach out to a trusted friend",
                "Consider professional counseling",
                "Try to maintain a regular sleep schedule",
                "Engage in activities you used to enjoy",
                "Get some sunlight and fresh air",
                "Practice self-compassion"
            ],
            'stressed': [
                "Break tasks into smaller, manageable steps",
                "Practice time management techniques",
                "Try progressive muscle relaxation",
                "Take regular breaks throughout the day",
                "Exercise or do physical activity",
                "Practice deep breathing"
            ],
            'angry': [
                "Take a few deep breaths before responding",
                "Go for a walk to cool down",
                "Write down your feelings in a journal",
                "Try counting to ten slowly",
                "Practice assertive communication",
                "Use physical activity to release tension"
            ],
            'lonely': [
                "Join a group or club that interests you",
                "Reach out to an old friend",
                "Volunteer in your community",
                "Try online communities or forums",
                "Take a class or workshop",
                "Consider getting a pet"
            ],
            'confused': [
                "Write down your thoughts and feelings",
                "Talk to a trusted friend or mentor",
                "Break big decisions into smaller steps",
                "Research your options thoroughly",
                "Consider professional guidance",
                "Take time to reflect on your values"
            ],
            'happy': [
                "Share your positive energy with others",
                "Document what's making you feel good",
                "Practice gratitude",
                "Continue doing what's working for you",
                "Help someone else feel good",
                "Celebrate your achievements"
            ],
            'neutral': [
                "How are you feeling today?",
                "What's on your mind?",
                "Is there anything you'd like to talk about?",
                "How can I help you today?",
                "What would be helpful to discuss?",
                "What's going well for you lately?"
            ]
        }
        
        return suggestions.get(mood, suggestions['neutral'])
    
    def save_conversation(self, conversation: List[Dict], filename: str = 'conversation_log.json'):
        """Save conversation history for analysis"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)
            print(f"Conversation saved to {filename}")
        except Exception as e:
            print(f"Error saving conversation: {e}")

def main():
    """Test the enhanced AI backend"""
    ai = EnhancedMentalHealthAI()
    
    # Test cases
    test_inputs = [
        "I feel really anxious about my job interview tomorrow",
        "I've been feeling down and hopeless lately",
        "Work is so stressful, I can't handle it anymore",
        "I'm so angry at my roommate for not cleaning up",
        "I had a great day today, everything went well!",
        "I feel lonely and have no friends",
        "I'm confused about my life direction"
    ]
    
    print("Testing Enhanced AI Backend:")
    print("=" * 60)
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        
        mood = ai.analyze_mood(user_input)
        print(f"Detected Mood: {mood}")
        
        friend_response = ai.generate_response(user_input, 'friend')
        print(f"Friend Mode: {friend_response}")
        
        professional_response = ai.generate_response(user_input, 'professional')
        print(f"Professional Mode: {professional_response}")
        
        suggestions = ai.get_suggestions(mood)
        print(f"Suggestions: {', '.join(suggestions[:3])}")
        print("-" * 60)

if __name__ == "__main__":
    main()
