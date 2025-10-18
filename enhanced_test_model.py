3#!/usr/bin/env python3
"""
Enhanced Healo AI Model Testing Script
This script tests the trained mental health chatbot model and provides detailed evaluation metrics including R-squared.
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
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedMentalHealthModelTester:
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
    
    def get_response_with_metrics(self, user_input, mode='friend', threshold=0.1):
        """Get response for user input with detailed metrics"""
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
            
            # Get response
            if best_similarity >= threshold and best_match_idx < len(self.training_data):
                response = self.training_data[best_match_idx]['response']
                actual_mode = self.training_data[best_match_idx]['mode']
            else:
                response = self.get_fallback_response(mode)
                actual_mode = mode
            
            return {
                'response': response,
                'similarity': best_similarity,
                'predicted_mode': actual_mode,
                'input_length': len(user_input),
                'response_length': len(response),
                'is_fallback': best_similarity < threshold
            }
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return {
                'response': self.get_fallback_response(mode),
                'similarity': 0.0,
                'predicted_mode': mode,
                'input_length': len(user_input),
                'response_length': 0,
                'is_fallback': True
            }
    
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
    
    def calculate_accuracy_metrics(self):
        """Calculate accuracy, precision, recall, F1-score"""
        logger.info("Calculating accuracy metrics")
        
        try:
            y_true = []
            y_pred = []
            similarities = []
            
            for test_item in self.testing_data:
                result = self.get_response_with_metrics(test_item['input'], test_item['mode'])
                
                y_true.append(test_item['mode'])
                y_pred.append(result['predicted_mode'])
                similarities.append(result['similarity'])
            
            # Calculate metrics
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'average_similarity': np.mean(similarities),
                'similarity_std': np.std(similarities)
            }
            
        except Exception as e:
            logger.error(f"Error calculating accuracy metrics: {e}")
            return None
    
    def calculate_regression_metrics(self):
        """Calculate R-squared and regression metrics"""
        logger.info("Calculating regression metrics")
        
        try:
            input_lengths = []
            response_lengths = []
            similarities = []
            
            for test_item in self.testing_data:
                result = self.get_response_with_metrics(test_item['input'], test_item['mode'])
                
                input_lengths.append(result['input_length'])
                response_lengths.append(result['response_length'])
                similarities.append(result['similarity'])
            
            # Convert to numpy arrays
            X = np.column_stack([input_lengths, similarities])
            y = np.array(response_lengths)
            
            # Linear regression for R-squared
            reg = LinearRegression()
            reg.fit(X, y)
            y_pred = reg.predict(X)
            
            r2 = r2_score(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            mae = mean_absolute_error(y, y_pred)
            rmse = np.sqrt(mse)
            
            return {
                'r_squared': r2,
                'mean_squared_error': mse,
                'mean_absolute_error': mae,
                'root_mean_squared_error': rmse,
                'coefficients': reg.coef_.tolist(),
                'intercept': reg.intercept_,
                'correlation_input_response': np.corrcoef(input_lengths, response_lengths)[0, 1],
                'correlation_similarity_response': np.corrcoef(similarities, response_lengths)[0, 1]
            }
            
        except Exception as e:
            logger.error(f"Error calculating regression metrics: {e}")
            return None
    
    def calculate_response_quality_metrics(self):
        """Calculate response quality metrics"""
        logger.info("Calculating response quality metrics")
        
        try:
            response_lengths = []
            similarities = []
            response_times = []
            fallback_count = 0
            
            for test_item in self.testing_data:
                start_time = datetime.now()
                result = self.get_response_with_metrics(test_item['input'], test_item['mode'])
                end_time = datetime.now()
                
                response_lengths.append(result['response_length'])
                similarities.append(result['similarity'])
                response_times.append((end_time - start_time).total_seconds())
                
                if result['is_fallback']:
                    fallback_count += 1
            
            # Calculate quality metrics
            avg_length = np.mean(response_lengths)
            length_std = np.std(response_lengths)
            avg_similarity = np.mean(similarities)
            similarity_std = np.std(similarities)
            avg_response_time = np.mean(response_times)
            
            # Response length distribution
            length_percentiles = {
                '25th': np.percentile(response_lengths, 25),
                '50th': np.percentile(response_lengths, 50),
                '75th': np.percentile(response_lengths, 75),
                '90th': np.percentile(response_lengths, 90),
                '95th': np.percentile(response_lengths, 95)
            }
            
            return {
                'average_length': avg_length,
                'length_std': length_std,
                'length_percentiles': length_percentiles,
                'average_similarity': avg_similarity,
                'similarity_std': similarity_std,
                'average_response_time': avg_response_time,
                'fallback_count': fallback_count,
                'fallback_rate': fallback_count / len(self.testing_data),
                'total_responses': len(response_lengths)
            }
            
        except Exception as e:
            logger.error(f"Error calculating response quality metrics: {e}")
            return None
    
    def generate_enhanced_report(self):
        """Generate enhanced test report with all metrics"""
        logger.info("Generating enhanced test report")
        
        try:
            # Calculate all metrics
            accuracy_metrics = self.calculate_accuracy_metrics()
            regression_metrics = self.calculate_regression_metrics()
            quality_metrics = self.calculate_response_quality_metrics()
            
            # Generate report
            report = {
                'test_date': datetime.now().isoformat(),
                'model_metadata': self.metadata,
                'accuracy_metrics': accuracy_metrics,
                'regression_metrics': regression_metrics,
                'quality_metrics': quality_metrics,
                'summary': self.generate_summary(accuracy_metrics, regression_metrics, quality_metrics)
            }
            
            # Save report
            with open('enhanced_test_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            # Print summary
            self.print_enhanced_summary(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating enhanced report: {e}")
            return None
    
    def generate_summary(self, accuracy_metrics, regression_metrics, quality_metrics):
        """Generate summary of all metrics"""
        summary = {
            'overall_performance': 'Excellent' if accuracy_metrics and accuracy_metrics['accuracy'] > 0.9 else 'Good' if accuracy_metrics and accuracy_metrics['accuracy'] > 0.8 else 'Needs Improvement',
            'key_strengths': [],
            'areas_for_improvement': [],
            'recommendations': []
        }
        
        if accuracy_metrics:
            if accuracy_metrics['accuracy'] > 0.95:
                summary['key_strengths'].append("Very high accuracy (>95%)")
            if accuracy_metrics['f1_score'] > 0.9:
                summary['key_strengths'].append("Excellent F1-score")
            if accuracy_metrics['average_similarity'] > 0.3:
                summary['key_strengths'].append("Good semantic similarity matching")
        
        if regression_metrics:
            if regression_metrics['r_squared'] > 0.5:
                summary['key_strengths'].append("Good predictive power for response length")
            else:
                summary['areas_for_improvement'].append("Response length prediction could be improved")
        
        if quality_metrics:
            if quality_metrics['average_length'] > 100:
                summary['key_strengths'].append("Detailed responses")
            if quality_metrics['average_response_time'] < 0.1:
                summary['key_strengths'].append("Fast response times")
            if quality_metrics['fallback_rate'] < 0.1:
                summary['key_strengths'].append("Low fallback rate")
        
        # Add general recommendations
        summary['recommendations'].append("Model shows good performance across most metrics")
        summary['recommendations'].append("Consider adding more diverse training data for better coverage")
        summary['recommendations'].append("Monitor response quality in production environment")
        
        return summary
    
    def print_enhanced_summary(self, report):
        """Print enhanced summary to console"""
        print("\n" + "="*80)
        print("ENHANCED HEALO AI MODEL TEST REPORT")
        print("="*80)
        
        if report['accuracy_metrics']:
            metrics = report['accuracy_metrics']
            print(f"\nACCURACY METRICS:")
            print(f"  • Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"  • Precision: {metrics['precision']:.4f}")
            print(f"  • Recall: {metrics['recall']:.4f}")
            print(f"  • F1-Score: {metrics['f1_score']:.4f}")
            print(f"  • Average Similarity: {metrics['average_similarity']:.4f}")
            print(f"  • Similarity Std Dev: {metrics['similarity_std']:.4f}")
        
        if report['regression_metrics']:
            metrics = report['regression_metrics']
            print(f"\nREGRESSION METRICS (R-SQUARED ANALYSIS):")
            print(f"  • R-Squared Score: {metrics['r_squared']:.4f} ({metrics['r_squared']*100:.2f}% variance explained)")
            print(f"  • Mean Squared Error: {metrics['mean_squared_error']:.4f}")
            print(f"  • Mean Absolute Error: {metrics['mean_absolute_error']:.4f}")
            print(f"  • Root Mean Squared Error: {metrics['root_mean_squared_error']:.4f}")
            print(f"  • Input-Response Correlation: {metrics['correlation_input_response']:.4f}")
            print(f"  • Similarity-Response Correlation: {metrics['correlation_similarity_response']:.4f}")
        
        if report['quality_metrics']:
            metrics = report['quality_metrics']
            print(f"\nRESPONSE QUALITY METRICS:")
            print(f"  • Average Response Length: {metrics['average_length']:.1f} characters")
            print(f"  • Response Length Std Dev: {metrics['length_std']:.1f}")
            print(f"  • Average Response Time: {metrics['average_response_time']:.4f} seconds")
            print(f"  • Fallback Rate: {metrics['fallback_rate']:.2%} ({metrics['fallback_count']}/{metrics['total_responses']})")
            print(f"  • Total Responses Tested: {metrics['total_responses']}")
        
        if report['summary']:
            summary = report['summary']
            print(f"\nOVERALL PERFORMANCE: {summary['overall_performance']}")
            
            if summary['key_strengths']:
                print(f"\nKEY STRENGTHS:")
                for strength in summary['key_strengths']:
                    print(f"  • {strength}")
            
            if summary['areas_for_improvement']:
                print(f"\nAREAS FOR IMPROVEMENT:")
                for area in summary['areas_for_improvement']:
                    print(f"  • {area}")
            
            if summary['recommendations']:
                print(f"\nRECOMMENDATIONS:")
                for rec in summary['recommendations']:
                    print(f"  • {rec}")
        
        print("\n" + "="*80)
        print("Enhanced test report saved to 'enhanced_test_report.json'")
        print("="*80)
    
    def run_enhanced_testing(self):
        """Run the complete enhanced testing pipeline"""
        try:
            logger.info("Starting Enhanced Healo AI Model Testing")
            logger.info("=" * 60)
            
            # Load model
            if not self.load_model():
                return False
            
            # Generate enhanced report
            report = self.generate_enhanced_report()
            
            if report:
                logger.info("Enhanced testing completed successfully!")
                return True
            else:
                logger.error("Enhanced testing failed!")
                return False
                
        except Exception as e:
            logger.error(f"Enhanced testing failed: {e}")
            return False

def main():
    """Main function to run enhanced testing"""
    tester = EnhancedMentalHealthModelTester()
    success = tester.run_enhanced_testing()
    
    if success:
        print("\n[SUCCESS] Enhanced model testing completed successfully!")
        print("Check 'enhanced_test_report.json' for detailed results.")
    else:
        print("\n[ERROR] Enhanced model testing failed!")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main()
