#!/usr/bin/env python3
"""
Healo AI Model Testing Script
This script tests the trained mental health chatbot model and provides detailed evaluation metrics.
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MentalHealthModelTester:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.vectorizer = None
        self.tfidf_matrix = None
        self.training_data = None
        self.testing_data = None
        self.metadata = None
        
    def load_model(self):
        """Load the trained model and data"""
        try:
            logger.info("Loading trained model and data")
            
            # Load vectorizer
            self.vectorizer = joblib.load(os.path.join(self.model_dir, 'tfidf_vectorizer.pkl'))
            logger.info("Vectorizer loaded successfully")
            
            # Load TF-IDF matrix
            self.tfidf_matrix = joblib.load(os.path.join(self.model_dir, 'tfidf_matrix.pkl'))
            logger.info("TF-IDF matrix loaded successfully")
            
            # Load training data
            self.training_data = joblib.load(os.path.join(self.model_dir, 'training_data.pkl'))
            logger.info("Training data loaded successfully")
            
            # Load testing data
            self.testing_data = pd.read_csv('data/testing_dataset.csv').to_dict('records')
            logger.info("Testing data loaded successfully")
            
            # Load metadata
            with open(os.path.join(self.model_dir, 'training_metadata.json'), 'r') as f:
                self.metadata = json.load(f)
            logger.info("Metadata loaded successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        import re
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_response(self, user_input, mode='friend', threshold=0.1):
        """Get response for user input"""
        try:
            # Clean input
            clean_input = self.clean_text(user_input)
            
            # Transform input
            input_vector = self.vectorizer.transform([clean_input])
            
            # Calculate similarities
            similarities = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
            
            # Find best match
            best_match_idx = similarities.argmax()
            best_similarity = similarities[best_match_idx]
            
            # Check if similarity is above threshold
            if best_similarity < threshold:
                return self.get_fallback_response(mode)
            
            # Get response from training data
            if best_match_idx < len(self.training_data):
                response = self.training_data[best_match_idx]['response']
                return response
            
            return self.get_fallback_response(mode)
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return self.get_fallback_response(mode)
    
    def get_fallback_response(self, mode='friend'):
        """Get fallback response when no good match is found"""
        fallback_responses = {
            'friend': [
                "I'm here for you. Can you tell me more about what you're going through?",
                "That sounds really tough. I'm listening and I care about how you're feeling.",
                "I understand this is difficult for you. What's on your mind right now?",
                "You're not alone in this. I'm here to support you through whatever you're facing.",
                "I can hear that you're struggling. Let's talk about what's happening."
            ],
            'professional': [
                "I understand you're experiencing some challenges. It's important to acknowledge these feelings.",
                "Thank you for sharing that with me. Can you help me understand more about your current situation?",
                "I hear that you're going through a difficult time. What strategies have you tried so far?",
                "It's completely normal to feel this way. What would be most helpful for you right now?",
                "I appreciate you opening up about this. How long have you been experiencing these feelings?"
            ]
        }
        
        import random
        return random.choice(fallback_responses.get(mode, fallback_responses['friend']))
    
    def test_response_quality(self):
        """Test the quality of responses"""
        logger.info("Testing response quality")
        
        try:
            quality_metrics = {
                'total_tests': len(self.testing_data),
                'successful_responses': 0,
                'empty_responses': 0,
                'fallback_responses': 0,
                'average_response_length': 0,
                'mode_accuracy': {'friend': 0, 'professional': 0}
            }
            
            response_lengths = []
            
            for test_item in self.testing_data:
                # Get response
                response = self.get_response(test_item['input'], test_item['mode'])
                
                # Check response quality
                if response and len(response.strip()) > 0:
                    quality_metrics['successful_responses'] += 1
                    response_lengths.append(len(response))
                    
                    # Check if it's a fallback response
                    if any(phrase in response.lower() for phrase in ['here for you', 'here to support', 'thank you for sharing']):
                        quality_metrics['fallback_responses'] += 1
                else:
                    quality_metrics['empty_responses'] += 1
                
                # Check mode accuracy (simplified)
                if test_item['mode'] in response.lower() or 'professional' not in response.lower():
                    quality_metrics['mode_accuracy'][test_item['mode']] += 1
            
            # Calculate averages
            if response_lengths:
                quality_metrics['average_response_length'] = sum(response_lengths) / len(response_lengths)
            
            # Calculate percentages
            quality_metrics['success_rate'] = quality_metrics['successful_responses'] / quality_metrics['total_tests']
            quality_metrics['fallback_rate'] = quality_metrics['fallback_responses'] / quality_metrics['total_tests']
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Error testing response quality: {e}")
            return None
    
    def test_similarity_thresholds(self):
        """Test different similarity thresholds"""
        logger.info("Testing different similarity thresholds")
        
        thresholds = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
        results = []
        
        for threshold in thresholds:
            successful = 0
            fallback = 0
            
            for test_item in self.testing_data[:50]:  # Test on subset for speed
                response = self.get_response(test_item['input'], test_item['mode'], threshold)
                
                if response and len(response.strip()) > 0:
                    successful += 1
                    if any(phrase in response.lower() for phrase in ['here for you', 'here to support', 'thank you for sharing']):
                        fallback += 1
            
            results.append({
                'threshold': threshold,
                'successful': successful,
                'fallback': fallback,
                'success_rate': successful / 50
            })
        
        return results
    
    def test_mode_consistency(self):
        """Test consistency between friend and professional modes"""
        logger.info("Testing mode consistency")
        
        try:
            test_inputs = [
                "I feel really anxious about my job interview tomorrow",
                "I've been having trouble sleeping lately",
                "I feel like I'm not good enough for anyone",
                "I'm struggling with depression and don't know what to do",
                "I feel overwhelmed by all my responsibilities"
            ]
            
            mode_comparisons = []
            
            for test_input in test_inputs:
                friend_response = self.get_response(test_input, 'friend')
                professional_response = self.get_response(test_input, 'professional')
                
                mode_comparisons.append({
                    'input': test_input,
                    'friend_response': friend_response,
                    'professional_response': professional_response,
                    'length_difference': abs(len(friend_response) - len(professional_response))
                })
            
            return mode_comparisons
            
        except Exception as e:
            logger.error(f"Error testing mode consistency: {e}")
            return []
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("Generating comprehensive test report")
        
        try:
            # Test response quality
            quality_metrics = self.test_response_quality()
            
            # Test similarity thresholds
            threshold_results = self.test_similarity_thresholds()
            
            # Test mode consistency
            mode_comparisons = self.test_mode_consistency()
            
            # Generate report
            report = {
                'test_date': datetime.now().isoformat(),
                'model_metadata': self.metadata,
                'quality_metrics': quality_metrics,
                'threshold_analysis': threshold_results,
                'mode_consistency': mode_comparisons,
                'recommendations': self.generate_recommendations(quality_metrics, threshold_results)
            }
            
            # Save report
            with open('test_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            # Print summary
            self.print_test_summary(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating test report: {e}")
            return None
    
    def generate_recommendations(self, quality_metrics, threshold_results):
        """Generate recommendations based on test results"""
        recommendations = []
        
        if quality_metrics:
            if quality_metrics['success_rate'] < 0.8:
                recommendations.append("Consider adding more training data to improve response quality")
            
            if quality_metrics['fallback_rate'] > 0.3:
                recommendations.append("High fallback rate detected - consider lowering similarity threshold")
            
            if quality_metrics['average_response_length'] < 50:
                recommendations.append("Responses are quite short - consider adding more detailed responses to training data")
        
        if threshold_results:
            best_threshold = max(threshold_results, key=lambda x: x['success_rate'])
            recommendations.append(f"Optimal similarity threshold appears to be {best_threshold['threshold']}")
        
        return recommendations
    
    def print_test_summary(self, report):
        """Print test summary to console"""
        print("\n" + "="*60)
        print("HEALO AI MODEL TEST REPORT")
        print("="*60)
        
        if report['quality_metrics']:
            metrics = report['quality_metrics']
            print(f"Total Tests: {metrics['total_tests']}")
            print(f"Success Rate: {metrics['success_rate']:.2%}")
            print(f"Fallback Rate: {metrics['fallback_rate']:.2%}")
            print(f"Average Response Length: {metrics['average_response_length']:.1f} characters")
        
        print("\nRECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"• {rec}")
        
        print("\n" + "="*60)
        print("Test report saved to 'test_report.json'")
        print("="*60)
    
    def run_interactive_test(self):
        """Run interactive testing session"""
        print("\n" + "="*50)
        print("HEALO AI INTERACTIVE TESTING")
        print("="*50)
        print("Type 'quit' to exit, 'mode' to switch modes")
        print("Current mode: friend")
        print("="*50)
        
        current_mode = 'friend'
        
        while True:
            try:
                user_input = input(f"\n[{current_mode.upper()}] You: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'mode':
                    current_mode = 'professional' if current_mode == 'friend' else 'friend'
                    print(f"Switched to {current_mode} mode")
                    continue
                elif not user_input:
                    continue
                
                # Get response
                response = self.get_response(user_input, current_mode)
                print(f"Healo: {response}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nInteractive testing session ended.")
    
    def run_testing(self):
        """Run the complete testing pipeline"""
        try:
            logger.info("Starting Healo AI Model Testing")
            logger.info("=" * 50)
            
            # Load model
            if not self.load_model():
                return False
            
            # Generate test report
            report = self.generate_test_report()
            
            if report:
                logger.info("Testing completed successfully!")
                
                # Ask if user wants interactive testing
                try:
                    user_input = input("\nWould you like to run interactive testing? (y/n): ").strip().lower()
                    if user_input == 'y':
                        self.run_interactive_test()
                except:
                    pass
                
                return True
            else:
                logger.error("Testing failed!")
                return False
                
        except Exception as e:
            logger.error(f"Testing failed: {e}")
            return False

def main():
    """Main function to run testing"""
    tester = MentalHealthModelTester()
    success = tester.run_testing()
    
    if success:
        print("\n[SUCCESS] Model testing completed successfully!")
        print("Check 'test_report.json' for detailed results.")
    else:
        print("\n[ERROR] Model testing failed!")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main()
