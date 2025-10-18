#!/usr/bin/env python3
"""
AI Backend for Healo Mental Health Chatbot
Uses BERT-like models for enhanced response generation
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

class MentalHealthAI:
    def __init__(self, dataset_path: str = 'data/training_dataset.csv'):
        self.dataset_path = dataset_path
        self.dataset = []
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.tfidf_matrix = None
        self.mood_patterns = {
            'anxious': [
                'anxious', 'anxiety', 'worried', 'nervous', 'panic', 'scared', 
                'fear', 'afraid', 'uneasy', 'restless', 'tense', 'stressed'
            ],
            'depressed': [
                'depressed', 'depression', 'sad', 'down', 'hopeless', 'empty', 
                'worthless', 'suicidal', 'miserable', 'gloomy', 'blue', 'low'
            ],
            'stressed': [
                'stressed', 'stress', 'overwhelmed', 'pressure', 'burnout', 
                'exhausted', 'tired', 'drained', 'frazzled', 'swamped'
            ],
            'angry': [
                'angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 
                'rage', 'livid', 'upset', 'hostile', 'bitter'
            ],
            'happy': [
                'happy', 'good', 'great', 'wonderful', 'amazing', 'excited', 
                'joyful', 'positive', 'cheerful', 'content', 'pleased', 'delighted'
            ]
        }
        
        self.load_dataset()
        self.train_model()
    
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
        """Train the TF-IDF model for similarity matching"""
        if not self.dataset:
            return
        
        # Extract input texts for training
        input_texts = [item['input'] for item in self.dataset]
        
        # Fit TF-IDF vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(input_texts)
        print("TF-IDF model trained successfully")
    
    def analyze_mood(self, text: str) -> str:
        """Analyze the mood/sentiment of the input text"""
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
        """Find the best matching response from the dataset"""
        if not self.dataset or self.tfidf_matrix is None:
            return None
        
        # Clean and vectorize user input
        cleaned_input = self.clean_text(user_input)
        input_vector = self.vectorizer.transform([cleaned_input])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
        
        # Find the best match
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Only return if similarity is above threshold
        if best_similarity > 0.1:  # Lower threshold for better matching
            return self.dataset[best_match_idx]
        
        return None
    
    def generate_response(self, user_input: str, mode: str = 'friend') -> str:
        """Generate an appropriate response based on user input and mode"""
        # Find best match from dataset
        best_match = self.find_best_match(user_input)
        
        if best_match:
            return best_match[f'{mode}_response']
        
        # Generate contextual response based on mood
        mood = self.analyze_mood(user_input)
        return self.generate_contextual_response(user_input, mood, mode)
    
    def generate_contextual_response(self, user_input: str, mood: str, mode: str) -> str:
        """Generate contextual responses based on detected mood"""
        responses = {
            'anxious': {
                'friend': [
                    "I can hear that you're feeling anxious. That's totally valid! What's on your mind that's making you feel this way?",
                    "Anxiety can be really overwhelming sometimes. You're not alone in this. What's triggering these feelings for you?",
                    "I totally get that anxious feeling! It can be scary. What would help you feel more grounded right now?"
                ],
                'professional': [
                    "Anxiety can be challenging to manage. It might help to practice deep breathing or grounding techniques. What specific thoughts or situations are contributing to your anxiety?",
                    "I understand you're experiencing anxiety. It's important to identify triggers and develop coping strategies. What techniques have you tried before?",
                    "Anxiety is a common experience that can be managed with the right tools. What specific symptoms are you noticing?"
                ]
            },
            'depressed': {
                'friend': [
                    "I'm really sorry you're going through a tough time. Depression can feel isolating, but you're not alone. How long have you been feeling this way?",
                    "That sounds really hard. Depression is tough, but there are people who care about you. What's been weighing on your mind lately?",
                    "I'm here for you. Depression can make everything feel heavy. What would help you feel even a little bit better today?"
                ],
                'professional': [
                    "Depression can significantly impact your daily life. It's important to consider professional help if these feelings persist. Have you noticed changes in your sleep, appetite, or interest in activities?",
                    "I appreciate you sharing this with me. Depression is a serious condition that often requires professional support. What symptoms are you experiencing?",
                    "Depression affects many people, and seeking help is a sign of strength. Have you considered speaking with a mental health professional?"
                ]
            },
            'stressed': {
                'friend': [
                    "Stress can really take a toll on you! What's been stressing you out lately? Sometimes talking about it helps.",
                    "I hear you on the stress front! It can feel overwhelming. What's the biggest stressor for you right now?",
                    "Stress is no joke! What would help you feel more in control of the situation?"
                ],
                'professional': [
                    "Chronic stress can affect both physical and mental health. Identifying stress triggers and developing coping strategies is important. What areas of your life are causing the most stress?",
                    "Stress management is crucial for overall well-being. What stress management techniques have you tried, and which ones work best for you?",
                    "It's important to address stress before it becomes overwhelming. What specific situations are contributing to your stress levels?"
                ]
            },
            'angry': {
                'friend': [
                    "I can tell you're feeling really frustrated right now. What's got you feeling this way?",
                    "Anger can be a tough emotion to deal with. What's making you feel so upset?",
                    "I hear that you're angry. Sometimes it helps to talk through what's bothering you."
                ],
                'professional': [
                    "Anger is a natural emotion, but it's important to express it in healthy ways. What's triggering these feelings for you?",
                    "I understand you're experiencing anger. It can be helpful to identify the underlying causes and develop healthy coping strategies. What's contributing to these feelings?",
                    "Anger management is an important skill. What techniques have you used in the past to handle difficult emotions?"
                ]
            },
            'happy': {
                'friend': [
                    "That's wonderful to hear! I'm so glad you're feeling good. What's been going well for you lately?",
                    "I love hearing that you're in a good mood! What's making you feel so positive today?",
                    "That's awesome! It's great when things are going well. What's been the highlight of your day?"
                ],
                'professional': [
                    "It's wonderful that you're experiencing positive emotions. Maintaining this positive state can be beneficial for your overall well-being. What factors are contributing to your current mood?",
                    "Positive emotions are important for mental health. It's great that you're feeling good. What strategies or activities help you maintain this positive state?",
                    "I'm glad to hear you're doing well. It's important to recognize and appreciate positive moments. What's been working well for you recently?"
                ]
            },
            'neutral': {
                'friend': [
                    "Thanks for sharing that with me. I'm here to listen and help however I can. What else is on your mind?",
                    "I appreciate you opening up. What would you like to talk about today?",
                    "I'm here for you. What's going on in your world right now?"
                ],
                'professional': [
                    "I appreciate you sharing that with me. It's important to express your feelings and concerns. Is there anything specific you'd like to discuss or work through?",
                    "Thank you for being open with me. How can I best assist you in this moment?",
                    "I'm here to help you work through whatever you're experiencing. What would you like to focus on today?"
                ]
            }
        }
        
        mood_responses = responses.get(mood, responses['neutral'])
        mode_responses = mood_responses.get(mode, mood_responses['friend'])
        
        return random.choice(mode_responses)
    
    def get_suggestions(self, mood: str) -> List[str]:
        """Get contextual suggestions based on mood"""
        suggestions = {
            'anxious': [
                "Try some deep breathing exercises",
                "Practice mindfulness meditation",
                "Take a short walk outside",
                "Listen to calming music"
            ],
            'depressed': [
                "Reach out to a trusted friend",
                "Consider professional counseling",
                "Try to maintain a regular sleep schedule",
                "Engage in activities you used to enjoy"
            ],
            'stressed': [
                "Break tasks into smaller, manageable steps",
                "Practice time management techniques",
                "Try progressive muscle relaxation",
                "Take regular breaks throughout the day"
            ],
            'angry': [
                "Take a few deep breaths before responding",
                "Go for a walk to cool down",
                "Write down your feelings in a journal",
                "Try counting to ten slowly"
            ],
            'happy': [
                "Share your positive energy with others",
                "Document what's making you feel good",
                "Practice gratitude",
                "Continue doing what's working for you"
            ],
            'neutral': [
                "How are you feeling today?",
                "What's on your mind?",
                "Is there anything you'd like to talk about?",
                "How can I help you today?"
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
    """Test the AI backend"""
    ai = MentalHealthAI()
    
    # Test cases
    test_inputs = [
        "I feel really anxious about my job interview tomorrow",
        "I've been feeling down and hopeless lately",
        "Work is so stressful, I can't handle it anymore",
        "I'm so angry at my roommate for not cleaning up",
        "I had a great day today, everything went well!"
    ]
    
    print("Testing AI Backend:")
    print("=" * 50)
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        
        mood = ai.analyze_mood(user_input)
        print(f"Detected Mood: {mood}")
        
        friend_response = ai.generate_response(user_input, 'friend')
        print(f"Friend Mode: {friend_response}")
        
        professional_response = ai.generate_response(user_input, 'professional')
        print(f"Professional Mode: {professional_response}")
        
        suggestions = ai.get_suggestions(mood)
        print(f"Suggestions: {', '.join(suggestions[:2])}")
        print("-" * 50)

if __name__ == "__main__":
    main()
