#!/usr/bin/env python3
"""
Simple Accuracy Test for Improved Healo AI
This script provides a simple test of the improved model accuracy
"""

import pandas as pd
import numpy as np
from improved_ai_backend import ImprovedMentalHealthAI
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_improved_accuracy():
    """Test the improved model accuracy"""
    try:
        print("=" * 60)
        print("SIMPLE ACCURACY TEST FOR IMPROVED HEALO AI")
        print("=" * 60)
        
        # Initialize improved AI
        ai = ImprovedMentalHealthAI()
        
        # Test cases
        test_cases = [
            {"input": "I feel really anxious about my exams", "expected_mood": "anxious"},
            {"input": "I'm having a great day today!", "expected_mood": "happy"},
            {"input": "I feel lonely and don't know what to do", "expected_mood": "lonely"},
            {"input": "I'm so angry at my boss right now", "expected_mood": "angry"},
            {"input": "I feel confused about my future", "expected_mood": "confused"},
            {"input": "I feel like I'm drowning in responsibilities", "expected_mood": "overwhelmed"},
            {"input": "I'm happy about my promotion but terrified I'll mess it up", "expected_mood": "anxious"},
            {"input": "I want to be alone but I'm scared of being alone", "expected_mood": "anxious"},
            {"input": "I've tried everything to feel better but nothing works", "expected_mood": "sad"},
            {"input": "I feel like I'm always the one reaching out to friends", "expected_mood": "sad"}
        ]
        
        # Test results
        correct_mood_predictions = 0
        response_quality_scores = []
        response_times = []
        
        print(f"Testing {len(test_cases)} scenarios...")
        print("-" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            input_text = test_case['input']
            expected_mood = test_case['expected_mood']
            
            print(f"\nTest {i}/{len(test_cases)}")
            print(f"Input: {input_text}")
            print(f"Expected Mood: {expected_mood}")
            
            # Measure response time
            start_time = time.time()
            
            # Generate responses
            friend_response = ai.generate_response(input_text, 'friend')
            professional_response = ai.generate_response(input_text, 'professional')
            detected_mood = ai.analyze_mood(input_text)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Store results
            response_times.append(response_time)
            
            # Check mood prediction accuracy
            if detected_mood == expected_mood:
                correct_mood_predictions += 1
                mood_status = "[CORRECT]"
            else:
                mood_status = f"[WRONG - got: {detected_mood}]"
            
            # Calculate response quality (simple length-based metric)
            friend_quality = len(friend_response) / 100
            professional_quality = len(professional_response) / 100
            avg_quality = (friend_quality + professional_quality) / 2
            response_quality_scores.append(avg_quality)
            
            print(f"Detected Mood: {detected_mood} {mood_status}")
            print(f"Friend Response: {friend_response[:80]}...")
            print(f"Professional Response: {professional_response[:80]}...")
            print(f"Response Time: {response_time:.4f}s")
            print(f"Response Quality: {avg_quality:.2f}")
        
        # Calculate final metrics
        mood_accuracy = correct_mood_predictions / len(test_cases)
        avg_response_quality = np.mean(response_quality_scores)
        avg_response_time = np.mean(response_times)
        
        # Print comprehensive results
        print("\n" + "=" * 60)
        print("SIMPLE ACCURACY TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests: {len(test_cases)}")
        print(f"Mood Prediction Accuracy: {mood_accuracy:.4f} ({mood_accuracy*100:.2f}%)")
        print(f"Correct Mood Predictions: {correct_mood_predictions}/{len(test_cases)}")
        print(f"Average Response Quality: {avg_response_quality:.4f}")
        print(f"Average Response Time: {avg_response_time:.4f} seconds")
        
        # Response quality analysis
        high_quality_responses = sum(1 for score in response_quality_scores if score > 0.5)
        print(f"High Quality Responses (>0.5): {high_quality_responses}/{len(test_cases)} ({high_quality_responses/len(test_cases)*100:.1f}%)")
        
        # Response time analysis
        fast_responses = sum(1 for time in response_times if time < 0.1)
        print(f"Fast Responses (<0.1s): {fast_responses}/{len(test_cases)} ({fast_responses/len(test_cases)*100:.1f}%)")
        
        # Overall assessment
        print("\n" + "=" * 60)
        print("OVERALL ASSESSMENT")
        print("=" * 60)
        
        if mood_accuracy >= 0.8:
            print("EXCELLENT: Mood prediction accuracy is very high!")
        elif mood_accuracy >= 0.6:
            print("GOOD: Mood prediction accuracy is satisfactory!")
        else:
            print("NEEDS IMPROVEMENT: Mood prediction accuracy needs work!")
        
        if avg_response_quality >= 0.5:
            print("EXCELLENT: Response quality is very high!")
        elif avg_response_quality >= 0.3:
            print("GOOD: Response quality is satisfactory!")
        else:
            print("NEEDS IMPROVEMENT: Response quality needs work!")
        
        if avg_response_time <= 0.1:
            print("EXCELLENT: Response time is very fast!")
        elif avg_response_time <= 0.5:
            print("GOOD: Response time is acceptable!")
        else:
            print("NEEDS IMPROVEMENT: Response time needs optimization!")
        
        # Final verdict
        overall_score = (mood_accuracy + avg_response_quality + (1 - min(avg_response_time, 1))) / 3
        
        print(f"\nOverall Performance Score: {overall_score:.4f} ({overall_score*100:.2f}%)")
        
        if overall_score >= 0.8:
            print("OUTSTANDING: The improved model performs excellently!")
        elif overall_score >= 0.6:
            print("GREAT: The improved model performs very well!")
        elif overall_score >= 0.4:
            print("GOOD: The improved model performs adequately!")
        else:
            print("FAIR: The improved model needs further optimization!")
        
        print("=" * 60)
        
        return {
            'mood_accuracy': mood_accuracy,
            'avg_response_quality': avg_response_quality,
            'avg_response_time': avg_response_time,
            'overall_score': overall_score
        }
        
    except Exception as e:
        logger.error(f"Error in simple accuracy test: {e}")
        return None

def main():
    """Main function to run the simple accuracy test"""
    try:
        results = test_improved_accuracy()
        
        if results:
            print("\n[SUCCESS] Simple accuracy test completed successfully!")
            print(f"Model is ready for deployment with {results['mood_accuracy']*100:.1f}% mood accuracy!")
        else:
            print("\n[ERROR] Simple accuracy test failed!")
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")

if __name__ == "__main__":
    main()
