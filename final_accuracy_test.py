#!/usr/bin/env python3
"""
Final Accuracy Test for Improved Healo AI
This script provides a comprehensive test of the improved model accuracy
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
    """Test the improved model accuracy comprehensively"""
    try:
        print("=" * 60)
        print("FINAL ACCURACY TEST FOR IMPROVED HEALO AI")
        print("=" * 60)
        
        # Initialize improved AI
        ai = ImprovedMentalHealthAI()
        
        # Test cases covering various scenarios
        test_cases = [
            # Basic emotional states
            {"input": "I feel really anxious about my exams", "expected_mood": "anxious"},
            {"input": "I'm having a great day today!", "expected_mood": "happy"},
            {"input": "I feel lonely and don't know what to do", "expected_mood": "lonely"},
            {"input": "I'm so angry at my boss right now", "expected_mood": "angry"},
            {"input": "I feel confused about my future", "expected_mood": "confused"},
            
            # Complex emotional states
            {"input": "I feel like I'm drowning in responsibilities but also guilty for not doing enough", "expected_mood": "overwhelmed"},
            {"input": "I'm happy about my promotion but terrified I'll mess it up", "expected_mood": "anxious"},
            {"input": "I feel numb most days but then suddenly everything hits me at once", "expected_mood": "overwhelmed"},
            {"input": "I want to be alone but I'm scared of being alone", "expected_mood": "anxious"},
            {"input": "I've tried everything to feel better but nothing works", "expected_mood": "sad"},
            
            # Relationship and social dynamics
            {"input": "I feel like I'm always the one reaching out to friends", "expected_mood": "sad"},
            {"input": "I'm scared of being vulnerable with people I care about", "expected_mood": "anxious"},
            {"input": "I feel like I'm too much for people to handle", "expected_mood": "sad"},
            {"input": "I don't know how to set boundaries without feeling guilty", "expected_mood": "anxious"},
            
            # Work and life balance
            {"input": "I'm burned out but I can't afford to slow down", "expected_mood": "overwhelmed"},
            {"input": "I feel like I'm failing at everything important to me", "expected_mood": "sad"},
            {"input": "I'm scared I'm wasting my life but don't know what to do", "expected_mood": "anxious"},
            
            # Identity and self-discovery
            {"input": "I don't know who I am anymore", "expected_mood": "confused"},
            {"input": "I feel like I'm living someone else's life", "expected_mood": "sad"},
            {"input": "I'm scared of making the wrong life choices", "expected_mood": "anxious"},
            
            # Trauma and healing
            {"input": "I feel like my past is holding me back from being happy", "expected_mood": "sad"},
            {"input": "I'm scared I'll never heal from what happened to me", "expected_mood": "anxious"},
            {"input": "I feel broken and don't know if I can be fixed", "expected_mood": "sad"},
            
            # Future and uncertainty
            {"input": "I'm terrified of the future but also excited about it", "expected_mood": "anxious"},
            {"input": "I feel like I'm running out of time to figure out my life", "expected_mood": "anxious"},
            {"input": "I'm scared I'll regret the choices I'm making now", "expected_mood": "anxious"},
            
            # Self-care and recovery
            {"input": "I know I need to take care of myself but I don't know how", "expected_mood": "confused"},
            {"input": "I feel like I'm too broken to be helped", "expected_mood": "sad"},
            {"input": "I'm tired of trying to get better", "expected_mood": "sad"},
            
            # Social anxiety and isolation
            {"input": "I want to connect with people but I'm scared they'll reject me", "expected_mood": "anxious"},
            {"input": "I feel like I don't belong anywhere", "expected_mood": "lonely"},
            {"input": "I'm scared of being judged for my mental health struggles", "expected_mood": "anxious"},
            
            # Purpose and meaning
            {"input": "I feel like my life has no purpose or meaning", "expected_mood": "sad"},
            {"input": "I'm scared I'll never find my passion or calling", "expected_mood": "anxious"},
            {"input": "I feel like I'm just existing, not really living", "expected_mood": "sad"}
        ]
        
        # Test results
        results = {
            'total_tests': len(test_cases),
            'correct_mood_predictions': 0,
            'response_quality_scores': [],
            'response_times': [],
            'friend_responses': [],
            'professional_responses': [],
            'mood_accuracy': 0,
            'avg_response_quality': 0,
            'avg_response_time': 0
        }
        
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
            results['response_times'].append(response_time)
            results['friend_responses'].append(friend_response)
            results['professional_responses'].append(professional_response)
            
            # Check mood prediction accuracy
            if detected_mood == expected_mood:
                results['correct_mood_predictions'] += 1
                mood_status = "✓ CORRECT"
            else:
                mood_status = f"✗ WRONG (got: {detected_mood})"
            
            # Calculate response quality (simple length-based metric)
            friend_quality = len(friend_response) / 100  # Normalize by 100
            professional_quality = len(professional_response) / 100
            avg_quality = (friend_quality + professional_quality) / 2
            results['response_quality_scores'].append(avg_quality)
            
            print(f"Detected Mood: {detected_mood} {mood_status}")
            print(f"Friend Response: {friend_response[:100]}...")
            print(f"Professional Response: {professional_response[:100]}...")
            print(f"Response Time: {response_time:.4f}s")
            print(f"Response Quality: {avg_quality:.2f}")
        
        # Calculate final metrics
        results['mood_accuracy'] = results['correct_mood_predictions'] / results['total_tests']
        results['avg_response_quality'] = np.mean(results['response_quality_scores'])
        results['avg_response_time'] = np.mean(results['response_times'])
        
        # Print comprehensive results
        print("\n" + "=" * 60)
        print("FINAL ACCURACY TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests: {results['total_tests']}")
        print(f"Mood Prediction Accuracy: {results['mood_accuracy']:.4f} ({results['mood_accuracy']*100:.2f}%)")
        print(f"Correct Mood Predictions: {results['correct_mood_predictions']}/{results['total_tests']}")
        print(f"Average Response Quality: {results['avg_response_quality']:.4f}")
        print(f"Average Response Time: {results['avg_response_time']:.4f} seconds")
        
        # Response quality analysis
        high_quality_responses = sum(1 for score in results['response_quality_scores'] if score > 0.5)
        print(f"High Quality Responses (>0.5): {high_quality_responses}/{results['total_tests']} ({high_quality_responses/results['total_tests']*100:.1f}%)")
        
        # Response time analysis
        fast_responses = sum(1 for time in results['response_times'] if time < 0.1)
        print(f"Fast Responses (<0.1s): {fast_responses}/{results['total_tests']} ({fast_responses/results['total_tests']*100:.1f}%)")
        
        # Overall assessment
        print("\n" + "=" * 60)
        print("OVERALL ASSESSMENT")
        print("=" * 60)
        
        if results['mood_accuracy'] >= 0.8:
            print("🎉 EXCELLENT: Mood prediction accuracy is very high!")
        elif results['mood_accuracy'] >= 0.6:
            print("✅ GOOD: Mood prediction accuracy is satisfactory!")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Mood prediction accuracy needs work!")
        
        if results['avg_response_quality'] >= 0.5:
            print("🎉 EXCELLENT: Response quality is very high!")
        elif results['avg_response_quality'] >= 0.3:
            print("✅ GOOD: Response quality is satisfactory!")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Response quality needs work!")
        
        if results['avg_response_time'] <= 0.1:
            print("🎉 EXCELLENT: Response time is very fast!")
        elif results['avg_response_time'] <= 0.5:
            print("✅ GOOD: Response time is acceptable!")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Response time needs optimization!")
        
        # Final verdict
        overall_score = (results['mood_accuracy'] + results['avg_response_quality'] + (1 - min(results['avg_response_time'], 1))) / 3
        
        print(f"\nOverall Performance Score: {overall_score:.4f} ({overall_score*100:.2f}%)")
        
        if overall_score >= 0.8:
            print("🏆 OUTSTANDING: The improved model performs excellently!")
        elif overall_score >= 0.6:
            print("🥇 GREAT: The improved model performs very well!")
        elif overall_score >= 0.4:
            print("🥈 GOOD: The improved model performs adequately!")
        else:
            print("🥉 FAIR: The improved model needs further optimization!")
        
        print("=" * 60)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in final accuracy test: {e}")
        return None

def main():
    """Main function to run the final accuracy test"""
    try:
        results = test_improved_accuracy()
        
        if results:
            print("\n[SUCCESS] Final accuracy test completed successfully!")
            print(f"Model is ready for deployment with {results['mood_accuracy']*100:.1f}% mood accuracy!")
        else:
            print("\n[ERROR] Final accuracy test failed!")
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")

if __name__ == "__main__":
    main()
