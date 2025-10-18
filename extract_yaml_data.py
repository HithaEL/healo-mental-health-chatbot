#!/usr/bin/env python3
"""
Extract YAML data and add to CSV dataset
"""

import yaml
import pandas as pd
import re
import os

def extract_yaml_data():
    """Extract data from YAML files and add to CSV"""
    
    # Read existing CSV data
    try:
        df = pd.read_csv('mental_health_responses.csv')
        print(f"Loaded existing CSV data: {len(df)} rows")
    except FileNotFoundError:
        print("Creating new CSV file...")
        df = pd.DataFrame(columns=['User Input', 'Friend Mode Response', 'Professional Mode Response'])
    
    # Extract data from YAML files
    yaml_data = []
    
    # Read NLU file
    try:
        with open('data/nlu.yml', 'r', encoding='utf-8', errors='ignore') as file:
            nlu_data = yaml.safe_load(file)
        
        # Extract intents and examples
        intents = {}
        if 'nlu' in nlu_data:
            for item in nlu_data['nlu']:
                if 'intent' in item:
                    intent_name = item['intent']
                    examples = item.get('examples', '')
                    
                    if isinstance(examples, str):
                        example_list = [ex.strip().replace('- ', '') for ex in examples.split('\n') if ex.strip()]
                    else:
                        example_list = examples if isinstance(examples, list) else []
                    
                    intents[intent_name] = example_list
                    print(f"Extracted intent '{intent_name}' with {len(example_list)} examples")
        
        # Read domain file for responses
        with open('domain.yml', 'r', encoding='utf-8', errors='ignore') as file:
            domain_data = yaml.safe_load(file)
        
        # Extract responses
        responses = {}
        if 'responses' in domain_data:
            for response_key, response_data in domain_data['responses'].items():
                if response_data and len(response_data) > 0:
                    if isinstance(response_data[0], dict):
                        response_text = response_data[0].get('text', '')
                    else:
                        response_text = str(response_data[0])
                    
                    if response_text.strip():
                        # Clean Unicode characters
                        response_text = response_text.encode('ascii', 'ignore').decode('ascii')
                        intent_name = response_key.replace('utter_', '')
                        responses[intent_name] = response_text
                        print(f"Extracted response '{response_key}' -> '{intent_name}': {response_text[:50]}...")
        
        # Create training pairs
        for intent_name, examples in intents.items():
            if intent_name in responses:
                response_text = responses[intent_name]
                
                for example in examples:
                    if example.strip():
                        # Create friend and professional responses
                        friend_response = create_friend_response(response_text, intent_name)
                        professional_response = create_professional_response(response_text, intent_name)
                        
                        yaml_data.append({
                            'User Input': example.strip(),
                            'Friend Mode Response': friend_response,
                            'Professional Mode Response': professional_response
                        })
        
        print(f"Created {len(yaml_data)} training pairs from YAML data")
        
    except Exception as e:
        print(f"Error extracting YAML data: {e}")
        return
    
    # Combine with existing data
    if yaml_data:
        new_df = pd.DataFrame(yaml_data)
        combined_df = pd.concat([df, new_df], ignore_index=True)
        
        # Remove duplicates
        combined_df = combined_df.drop_duplicates(subset=['User Input'], keep='last')
        
        # Save combined data
        combined_df.to_csv('mental_health_responses.csv', index=False)
        print(f"Saved combined dataset with {len(combined_df)} total rows")
        print(f"Added {len(yaml_data)} new rows from YAML data")
    else:
        print("No YAML data extracted")

def create_friend_response(base_response, intent_name):
    """Create friend-mode response"""
    if not base_response:
        return get_default_friend_response(intent_name)
    
    # Add friendly prefixes
    if intent_name in ['greet', 'excitement']:
        return f"Hey there! {base_response}"
    elif intent_name in ['mood_unhappy', 'depressed', 'stress']:
        return f"I'm really sorry you're feeling this way. {base_response}"
    elif intent_name in ['gratitude', 'positive_response']:
        return f"That's wonderful! {base_response}"
    elif intent_name in ['goodbye']:
        return f"Take care! {base_response}"
    else:
        return base_response

def create_professional_response(base_response, intent_name):
    """Create professional-mode response"""
    if not base_response:
        return get_default_professional_response(intent_name)
    
    # Add professional prefixes
    if intent_name in ['greet', 'excitement']:
        return f"Thank you for reaching out. {base_response}"
    elif intent_name in ['mood_unhappy', 'depressed', 'stress']:
        return f"I understand you're experiencing some challenges. {base_response}"
    elif intent_name in ['gratitude', 'positive_response']:
        return f"It's great to hear about your positive experience. {base_response}"
    elif intent_name in ['goodbye']:
        return f"Thank you for our conversation. {base_response}"
    else:
        return base_response

def get_default_friend_response(intent_name):
    """Get default friend response"""
    defaults = {
        'greet': "Hi there! How are you doing today?",
        'mood_unhappy': "I'm sorry you're feeling down. What's going on?",
        'depressed': "I'm here for you. Can you tell me more about what you're experiencing?",
        'stress': "That sounds really stressful. How can I help you work through this?",
        'gratitude': "That's wonderful to hear! I'm so happy for you!",
        'goodbye': "Take care! I'm always here if you need to talk."
    }
    return defaults.get(intent_name, "I'm here to listen and help. What's on your mind?")

def get_default_professional_response(intent_name):
    """Get default professional response"""
    defaults = {
        'greet': "Hello. I'm here to provide support. How can I help you today?",
        'mood_unhappy': "I understand you're experiencing some difficulties. Can you tell me more about your current situation?",
        'depressed': "Depression can be challenging to navigate. It's important to address these feelings. What support systems do you have in place?",
        'stress': "Stress can significantly impact your well-being. What coping strategies have you tried so far?",
        'gratitude': "It's wonderful that you're experiencing positive emotions. What factors do you think contribute to this?",
        'goodbye': "Thank you for sharing with me today. Remember that professional help is available if needed."
    }
    return defaults.get(intent_name, "I'm here to provide support and guidance. What would you like to discuss?")

if __name__ == "__main__":
    extract_yaml_data()
