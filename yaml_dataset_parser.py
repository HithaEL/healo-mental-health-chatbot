#!/usr/bin/env python3
"""
YAML Dataset Parser for Healo Mental Health Chatbot
Parses Rasa YAML files and converts them to training data
"""

import yaml
import re
import os
from typing import List, Dict, Tuple, Any
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YAMLDatasetParser:
    def __init__(self):
        self.intents = {}
        self.responses = {}
        self.stories = []
        self.entities = set()
        
    def parse_nlu_file(self, file_path: str) -> Dict[str, List[str]]:
        """Parse NLU YAML file to extract intents and examples"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            intents = {}
            
            if 'nlu' in data:
                for item in data['nlu']:
                    if 'intent' in item:
                        intent_name = item['intent']
                        examples = item.get('examples', '')
                        
                        # Parse examples from YAML format
                        if isinstance(examples, str):
                            # Split by lines and clean up
                            example_list = [ex.strip().replace('- ', '') for ex in examples.split('\n') if ex.strip()]
                        else:
                            example_list = examples if isinstance(examples, list) else []
                        
                        intents[intent_name] = example_list
                        logger.info(f"Parsed intent '{intent_name}' with {len(example_list)} examples")
            
            return intents
            
        except Exception as e:
            logger.error(f"Error parsing NLU file {file_path}: {e}")
            return {}
    
    def parse_domain_file(self, file_path: str) -> Dict[str, Any]:
        """Parse domain YAML file to extract responses and intents"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            domain_info = {
                'intents': [],
                'responses': {},
                'entities': [],
                'slots': {}
            }
            
            # Extract intents
            if 'intents' in data:
                intents = []
                for intent in data['intents']:
                    if isinstance(intent, str):
                        intents.append(intent)
                    elif isinstance(intent, dict):
                        intents.append(list(intent.keys())[0])
                domain_info['intents'] = intents
            
            # Extract responses
            if 'responses' in data:
                domain_info['responses'] = data['responses']
                logger.info(f"Found {len(data['responses'])} responses in domain file")
            
            # Extract entities
            if 'entities' in data:
                domain_info['entities'] = data['entities']
            
            # Extract slots
            if 'slots' in data:
                domain_info['slots'] = data['slots']
            
            logger.info(f"Parsed domain with {len(domain_info['intents'])} intents, {len(domain_info['responses'])} responses")
            logger.debug(f"Domain keys: {list(data.keys())}")
            if 'responses' in data:
                logger.debug(f"Sample response keys: {list(data['responses'].keys())[:5]}")
            return domain_info
            
        except Exception as e:
            logger.error(f"Error parsing domain file {file_path}: {e}")
            return {}
    
    def parse_stories_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse stories YAML file to extract conversation flows"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            stories = []
            
            if 'stories' in data:
                for story in data['stories']:
                    if 'story' in story and 'steps' in story:
                        story_name = story['story']
                        steps = story['steps']
                        
                        # Extract conversation flow
                        conversation = []
                        for step in steps:
                            if isinstance(step, dict):
                                if 'intent' in step:
                                    conversation.append({'type': 'intent', 'value': step['intent']})
                                elif 'action' in step:
                                    conversation.append({'type': 'action', 'value': step['action']})
                        
                        stories.append({
                            'name': story_name,
                            'conversation': conversation
                        })
            
            logger.info(f"Parsed {len(stories)} stories")
            return stories
            
        except Exception as e:
            logger.error(f"Error parsing stories file {file_path}: {e}")
            return []
    
    def create_training_pairs_from_yaml(self, nlu_data: Dict, domain_data: Dict, stories_data: List) -> List[Dict[str, str]]:
        """Create training pairs from YAML data"""
        training_pairs = []
        
        try:
            # Create intent-response mappings
            intent_responses = {}
            
            # Map intents to responses from domain
            if 'responses' in domain_data:
                logger.info(f"Processing {len(domain_data['responses'])} responses from domain")
                for response_key, response_data in domain_data['responses'].items():
                    logger.debug(f"Processing response: {response_key}")
                    if response_data and len(response_data) > 0:
                        # Extract the first response text
                        if isinstance(response_data[0], dict):
                            response_text = response_data[0].get('text', '')
                        else:
                            response_text = str(response_data[0])
                        
                        logger.debug(f"Response text: '{response_text}'")
                        if response_text.strip():
                            # Try to map response key to intent
                            intent_name = response_key.replace('utter_', '')
                            intent_responses[intent_name] = response_text
                            logger.info(f"Mapped {response_key} -> {intent_name}: {response_text[:50]}...")
                        else:
                            logger.debug(f"Empty response text for {response_key}")
                    else:
                        logger.debug(f"Empty or invalid response data for {response_key}")
            else:
                logger.warning("No 'responses' key found in domain data")
            
            logger.info(f"Created {len(intent_responses)} intent-response mappings")
            
            # Create training pairs from intents and examples
            for intent_name, examples in nlu_data.items():
                if intent_name in intent_responses:
                    response_text = intent_responses[intent_name]
                    
                    for example in examples:
                        if example.strip():
                            # Create both friend and professional mode responses
                            friend_response = self.create_friend_response(response_text, intent_name)
                            professional_response = self.create_professional_response(response_text, intent_name)
                            
                            training_pairs.append({
                                'input': example.strip(),
                                'friend_response': friend_response,
                                'professional_response': professional_response,
                                'intent': intent_name
                            })
            
            # Create additional training pairs from stories
            for story in stories_data:
                conversation = story['conversation']
                for i in range(len(conversation) - 1):
                    if (conversation[i]['type'] == 'intent' and 
                        conversation[i + 1]['type'] == 'action'):
                        
                        intent_name = conversation[i]['value']
                        action_name = conversation[i + 1]['value']
                        
                        # Find examples for this intent
                        if intent_name in nlu_data:
                            examples = nlu_data[intent_name]
                            response_text = intent_responses.get(action_name.replace('utter_', ''), '')
                            
                            if response_text and examples:
                                for example in examples[:2]:  # Limit to 2 examples per story
                                    if example.strip():
                                        friend_response = self.create_friend_response(response_text, intent_name)
                                        professional_response = self.create_professional_response(response_text, intent_name)
                                        
                                        training_pairs.append({
                                            'input': example.strip(),
                                            'friend_response': friend_response,
                                            'professional_response': professional_response,
                                            'intent': intent_name
                                        })
            
            logger.info(f"Created {len(training_pairs)} training pairs from YAML data")
            return training_pairs
            
        except Exception as e:
            logger.error(f"Error creating training pairs from YAML: {e}")
            return []
    
    def create_friend_response(self, base_response: str, intent_name: str) -> str:
        """Create a friend-mode response from base response"""
        if not base_response:
            return self.get_default_friend_response(intent_name)
        
        # Make response more conversational and friendly
        friendly_response = base_response
        
        # Add friendly prefixes based on intent
        if intent_name in ['greet', 'excitement']:
            friendly_response = f"Hey there! {friendly_response}"
        elif intent_name in ['mood_unhappy', 'depressed', 'stress']:
            friendly_response = f"I'm really sorry you're feeling this way. {friendly_response}"
        elif intent_name in ['gratitude', 'positive_response']:
            friendly_response = f"That's wonderful! {friendly_response}"
        elif intent_name in ['goodbye']:
            friendly_response = f"Take care! {friendly_response}"
        
        return friendly_response
    
    def create_professional_response(self, base_response: str, intent_name: str) -> str:
        """Create a professional-mode response from base response"""
        if not base_response:
            return self.get_default_professional_response(intent_name)
        
        # Make response more professional and clinical
        professional_response = base_response
        
        # Add professional prefixes based on intent
        if intent_name in ['greet', 'excitement']:
            professional_response = f"Thank you for reaching out. {professional_response}"
        elif intent_name in ['mood_unhappy', 'depressed', 'stress']:
            professional_response = f"I understand you're experiencing some challenges. {professional_response}"
        elif intent_name in ['gratitude', 'positive_response']:
            professional_response = f"It's great to hear about your positive experience. {professional_response}"
        elif intent_name in ['goodbye']:
            professional_response = f"Thank you for our conversation. {professional_response}"
        
        return professional_response
    
    def get_default_friend_response(self, intent_name: str) -> str:
        """Get default friend response for intent"""
        defaults = {
            'greet': "Hi there! How are you doing today?",
            'mood_unhappy': "I'm sorry you're feeling down. What's going on?",
            'depressed': "I'm here for you. Can you tell me more about what you're experiencing?",
            'stress': "That sounds really stressful. How can I help you work through this?",
            'gratitude': "That's wonderful to hear! I'm so happy for you!",
            'goodbye': "Take care! I'm always here if you need to talk."
        }
        return defaults.get(intent_name, "I'm here to listen and help. What's on your mind?")
    
    def get_default_professional_response(self, intent_name: str) -> str:
        """Get default professional response for intent"""
        defaults = {
            'greet': "Hello. I'm here to provide support. How can I help you today?",
            'mood_unhappy': "I understand you're experiencing some difficulties. Can you tell me more about your current situation?",
            'depressed': "Depression can be challenging to navigate. It's important to address these feelings. What support systems do you have in place?",
            'stress': "Stress can significantly impact your well-being. What coping strategies have you tried so far?",
            'gratitude': "It's wonderful that you're experiencing positive emotions. What factors do you think contribute to this?",
            'goodbye': "Thank you for sharing with me today. Remember that professional help is available if needed."
        }
        return defaults.get(intent_name, "I'm here to provide support and guidance. What would you like to discuss?")
    
    def parse_all_yaml_files(self, data_dir: str = 'data') -> List[Dict[str, str]]:
        """Parse all YAML files in the data directory"""
        try:
            nlu_file = os.path.join(data_dir, 'nlu.yml')
            domain_file = os.path.join(data_dir, 'domain.yml')
            stories_file = os.path.join(data_dir, 'stories.yml')
            
            # Parse each file
            nlu_data = self.parse_nlu_file(nlu_file) if os.path.exists(nlu_file) else {}
            domain_data = self.parse_domain_file(domain_file) if os.path.exists(domain_file) else {}
            stories_data = self.parse_stories_file(stories_file) if os.path.exists(stories_file) else {}
            
            # Create training pairs
            training_pairs = self.create_training_pairs_from_yaml(nlu_data, domain_data, stories_data)
            
            return training_pairs
            
        except Exception as e:
            logger.error(f"Error parsing YAML files: {e}")
            return []
    
    def save_yaml_training_data(self, training_pairs: List[Dict[str, str]], output_file: str = 'yaml_training_data.csv'):
        """Save YAML training data to CSV format"""
        try:
            import pandas as pd
            
            # Convert to DataFrame
            df_data = []
            for pair in training_pairs:
                df_data.append({
                    'User Input': pair['input'],
                    'Friend Mode Response': pair['friend_response'],
                    'Professional Mode Response': pair['professional_response'],
                    'Intent': pair.get('intent', ''),
                    'Source': 'YAML'
                })
            
            df = pd.DataFrame(df_data)
            df.to_csv(output_file, index=False)
            
            logger.info(f"Saved {len(training_pairs)} YAML training pairs to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving YAML training data: {e}")
            return False

def main():
    """Main function to test YAML parsing"""
    parser = YAMLDatasetParser()
    
    # Parse all YAML files
    training_pairs = parser.parse_all_yaml_files()
    
    if training_pairs:
        print(f"Successfully parsed {len(training_pairs)} training pairs from YAML files")
        
        # Save to CSV
        parser.save_yaml_training_data(training_pairs)
        
        # Show sample data
        print("\nSample training pairs:")
        for i, pair in enumerate(training_pairs[:3]):
            print(f"\n{i+1}. Input: {pair['input']}")
            print(f"   Friend: {pair['friend_response']}")
            print(f"   Professional: {pair['professional_response']}")
    else:
        print("No training pairs found in YAML files")

if __name__ == "__main__":
    main()
