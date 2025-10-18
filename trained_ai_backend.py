#!/usr/bin/env python3
"""
Trained AI Backend for Healo Mental Health Chatbot
Uses pre-trained models for better performance
"""

import joblib
import json
import os
import re
import random
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import logging
from happiness_suggestions import HappinessSuggestionEngine

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrainedMentalHealthAI:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.vectorizer = None
        self.tfidf_matrix = None
        self.training_data = None
        self.metadata = None
        self.conversation_history = []
        self.happiness_engine = HappinessSuggestionEngine()
        
        # Load the trained model
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model and data"""
        try:
            logger.info("Loading pre-trained model...")
            
            # Load vectorizer
            self.vectorizer = joblib.load(os.path.join(self.model_dir, 'tfidf_vectorizer.pkl'))
            logger.info("Vectorizer loaded successfully")
            
            # Load TF-IDF matrix
            self.tfidf_matrix = joblib.load(os.path.join(self.model_dir, 'tfidf_matrix.pkl'))
            logger.info("TF-IDF matrix loaded successfully")
            
            # Load training data
            self.training_data = joblib.load(os.path.join(self.model_dir, 'training_data.pkl'))
            logger.info("Training data loaded successfully")
            
            # Load metadata
            with open(os.path.join(self.model_dir, 'training_metadata.json'), 'r') as f:
                self.metadata = json.load(f)
            logger.info("Metadata loaded successfully")
            
            logger.info(f"Model loaded with {len(self.training_data)} training examples")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to basic responses
            self.vectorizer = None
            self.tfidf_matrix = None
            self.training_data = []
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_response(self, user_input, mode='friend', threshold=0.1):
        """Generate response using the trained model"""
        try:
            # Clean input
            clean_input = self.clean_text(user_input)
            
            if not clean_input:
                return self.get_fallback_response(mode)
            
            # If model is not loaded, use fallback
            if not self.vectorizer or not self.tfidf_matrix:
                return self.get_fallback_response(mode)
            
            # Transform input
            input_vector = self.vectorizer.transform([clean_input])
            
            # Calculate similarities
            similarities = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
            
            # Find best match
            best_match_idx = similarities.argmax()
            best_similarity = similarities[best_match_idx]
            
            # Ensure best_similarity is a scalar
            if hasattr(best_similarity, 'item'):
                best_similarity = best_similarity.item()
            
            # Check if similarity is above threshold
            if best_similarity < threshold:
                return self.get_fallback_response(mode)
            
            # Get response from training data
            if best_match_idx < len(self.training_data):
                response = self.training_data[best_match_idx]['response']
                
                # Ensure response matches the requested mode
                if self.training_data[best_match_idx]['mode'] == mode:
                    return response
                else:
                    # Find a similar response in the correct mode
                    mode_responses = [item for item in self.training_data if item['mode'] == mode]
                    if mode_responses:
                        # Find the most similar response in the correct mode
                        mode_inputs = [item['input'] for item in mode_responses]
                        mode_vectorizer = self.vectorizer
                        mode_input_vector = mode_vectorizer.transform([clean_input])
                        mode_similarities = cosine_similarity(mode_input_vector, mode_vectorizer.transform(mode_inputs)).flatten()
                        best_mode_idx = mode_similarities.argmax()
                        best_mode_similarity = mode_similarities[best_mode_idx]
                        
                        # Ensure best_mode_similarity is a scalar
                        if hasattr(best_mode_similarity, 'item'):
                            best_mode_similarity = best_mode_similarity.item()
                        
                        if best_mode_similarity > threshold:
                            return mode_responses[best_mode_idx]['response']
                
                return self.get_fallback_response(mode)
            
            return self.get_fallback_response(mode)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self.get_fallback_response(mode)
    
    def get_fallback_response(self, mode='friend'):
        """Get fallback response when no good match is found"""
        fallback_responses = {
            'friend': [
                "I'm here for you. Can you tell me more about what you're going through?",
                "That sounds really tough. I'm listening and I care about how you're feeling.",
                "I understand this is difficult for you. What's on your mind right now?",
                "You're not alone in this. I'm here to support you through whatever you're facing.",
                "I can hear that you're struggling. Let's talk about what's happening.",
                "I'm sorry you're going through this. How can I help you feel better?",
                "It takes courage to share what you're feeling. I'm proud of you for reaching out.",
                "I want you to know that your feelings are valid and important to me.",
                "Let's work through this together. What would be most helpful right now?",
                "I'm here to listen without judgment. What's weighing on your heart today?"
            ],
            'professional': [
                "I understand you're experiencing some challenges. It's important to acknowledge these feelings.",
                "Thank you for sharing that with me. Can you help me understand more about your current situation?",
                "I hear that you're going through a difficult time. What strategies have you tried so far?",
                "It's completely normal to feel this way. What would be most helpful for you right now?",
                "I appreciate you opening up about this. How long have you been experiencing these feelings?",
                "Your feelings are valid and it's important to address them. What support systems do you have?",
                "I can see this is affecting you significantly. Have you considered speaking with a mental health professional?",
                "It's good that you're recognizing these feelings. What coping strategies have worked for you before?",
                "I understand this is challenging. What would you like to focus on improving first?",
                "Thank you for trusting me with this. How can we work together to address these concerns?"
            ]
        }
        
        return random.choice(fallback_responses.get(mode, fallback_responses['friend']))
    
    def analyze_mood(self, text):
        """Analyze mood from text using keyword detection"""
        try:
            text = self.clean_text(text)
            
            # Mood keywords
            mood_keywords = {
                'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'delighted', 'cheerful', 'content'],
                'sad': ['sad', 'depressed', 'down', 'blue', 'miserable', 'unhappy', 'gloomy', 'melancholy', 'dejected', 'sorrowful'],
                'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'fear', 'scared', 'uneasy', 'restless', 'tense'],
                'angry': ['angry', 'mad', 'furious', 'irritated', 'frustrated', 'annoyed', 'rage', 'livid', 'outraged', 'fuming'],
                'confused': ['confused', 'lost', 'uncertain', 'unsure', 'bewildered', 'puzzled', 'perplexed', 'disoriented', 'mixed up'],
                'lonely': ['lonely', 'alone', 'isolated', 'empty', 'disconnected', 'abandoned', 'forgotten', 'secluded', 'solitary'],
                'overwhelmed': ['overwhelmed', 'stressed', 'burdened', 'swamped', 'drowning', 'crushed', 'exhausted', 'drained', 'burned out']
            }
            
            # Count keyword matches
            mood_scores = {}
            for mood, keywords in mood_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text)
                mood_scores[mood] = score
            
            # Find the mood with highest score
            if mood_scores:
                best_mood = max(mood_scores, key=mood_scores.get)
                if mood_scores[best_mood] > 0:
                    return best_mood
            
            return 'neutral'
            
        except Exception as e:
            logger.error(f"Error analyzing mood: {e}")
            return 'neutral'
    
    def get_suggestions(self, mood):
        """Get mood-based suggestions with enhanced happiness focus"""
        # Get base mood suggestions
        base_suggestions = {
            'happy': [
                "Keep doing what makes you feel good!",
                "Share your positive energy with others.",
                "Consider journaling about what's making you happy.",
                "Try to maintain this positive mindset."
            ],
            'sad': [
                "It's okay to feel sad. Allow yourself to process these emotions.",
                "Consider talking to a trusted friend or family member.",
                "Try engaging in activities you usually enjoy.",
                "Remember that feelings are temporary and this will pass.",
                "Consider seeking professional help if sadness persists."
            ],
            'anxious': [
                "Try deep breathing exercises to calm your mind.",
                "Practice mindfulness or meditation.",
                "Break down overwhelming tasks into smaller steps.",
                "Consider limiting caffeine and getting enough sleep.",
                "Try progressive muscle relaxation techniques."
            ],
            'angry': [
                "Take a step back and count to ten before responding.",
                "Try physical exercise to release tension.",
                "Express your feelings in a journal or to a trusted person.",
                "Practice deep breathing to calm down.",
                "Consider what's really causing your anger."
            ],
            'confused': [
                "Take time to organize your thoughts.",
                "Write down what you're confused about.",
                "Ask for clarification from others when needed.",
                "Break complex problems into smaller parts.",
                "Give yourself time to process information."
            ],
            'lonely': [
                "Reach out to friends or family members.",
                "Consider joining a club or group with similar interests.",
                "Volunteer in your community to meet new people.",
                "Practice self-compassion and self-care.",
                "Consider professional counseling if loneliness persists."
            ],
            'overwhelmed': [
                "Make a list and prioritize your tasks.",
                "Don't be afraid to ask for help.",
                "Take breaks and practice self-care.",
                "Focus on one thing at a time.",
                "Consider what you can delegate or postpone."
            ],
            'neutral': [
                "How are you feeling today?",
                "Is there anything specific on your mind?",
                "What would you like to talk about?",
                "How can I help you today?"
            ]
        }
        
        # Get base suggestions
        suggestions = base_suggestions.get(mood, base_suggestions['neutral'])
        
        # Add happiness-focused suggestions
        happiness_suggestions = self.happiness_engine.get_mood_based_suggestions(mood)
        
        # Combine and return unique suggestions
        all_suggestions = suggestions + happiness_suggestions
        return list(set(all_suggestions))[:8]  # Return up to 8 unique suggestions
    
    def get_happiness_suggestions(self, user_input, conversation_history=None):
        """Get contextual happiness suggestions based on user input and conversation"""
        try:
            if conversation_history is None:
                conversation_history = self.conversation_history
            
            # Get contextual suggestions
            contextual_suggestions = self.happiness_engine.analyze_conversation_context(
                user_input, conversation_history
            )
            
            return contextual_suggestions
            
        except Exception as e:
            logger.error(f"Error getting happiness suggestions: {e}")
            return ["Try doing something that makes you smile today!"]
    
    def get_quick_happiness_boost(self):
        """Get a quick happiness boost suggestion"""
        return self.happiness_engine.get_quick_happiness_boost()
    
    def get_happiness_habits(self):
        """Get suggested happiness-building habits"""
        return self.happiness_engine.suggest_happiness_habits()
    
    def generate_happiness_plan(self, user_goals=None):
        """Generate a personalized happiness plan"""
        if user_goals is None:
            user_goals = []
        return self.happiness_engine.generate_happiness_plan(user_goals)
    
    def save_conversation(self, conversation):
        """Save conversation history"""
        try:
            self.conversation_history.extend(conversation)
            
            # Keep only last 100 conversations to prevent memory issues
            if len(self.conversation_history) > 100:
                self.conversation_history = self.conversation_history[-100:]
            
            logger.info(f"Saved {len(conversation)} conversation entries")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.metadata:
            return {
                'status': 'loaded',
                'training_size': self.metadata.get('training_size', 0),
                'testing_size': self.metadata.get('testing_size', 0),
                'total_features': self.metadata.get('total_features', 0),
                'training_date': self.metadata.get('training_date', 'unknown'),
                'vectorizer_params': self.metadata.get('vectorizer_params', {})
            }
        else:
            return {
                'status': 'not_loaded',
                'message': 'Model not properly loaded'
            }
