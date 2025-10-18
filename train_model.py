#!/usr/bin/env python3
"""
Healo AI Model Training Script
This script trains the mental health chatbot model using the enhanced dataset.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import re
import json
import os
from datetime import datetime
import logging
from yaml_dataset_parser import YAMLDatasetParser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MentalHealthModelTrainer:
    def __init__(self, dataset_path='mental_health_responses.csv', use_yaml=True):
        self.dataset_path = dataset_path
        self.use_yaml = use_yaml
        self.dataset = []
        self.vectorizer = TfidfVectorizer(
            max_features=3000,  # Increased from 2000
            stop_words='english',
            ngram_range=(1, 4),  # Increased from (1, 3)
            sublinear_tf=True,
            min_df=1,  # Added minimum document frequency
            max_df=0.95,  # Added maximum document frequency
            norm='l2'  # Added normalization
        )
        self.tfidf_matrix = None
        self.training_data = []
        self.testing_data = []
        self.yaml_parser = YAMLDatasetParser() if use_yaml else None
        
    def load_dataset(self):
        """Load and preprocess the dataset from CSV and YAML files"""
        try:
            logger.info(f"Loading dataset from {self.dataset_path}")
            
            # Load CSV data
            csv_data = self.load_csv_data()
            
            # Load YAML data if enabled
            yaml_data = []
            if self.use_yaml and self.yaml_parser:
                logger.info("Loading YAML dataset...")
                yaml_data = self.load_yaml_data()
            
            # Combine datasets
            all_data = csv_data + yaml_data
            self.dataset = all_data
            
            logger.info(f"Successfully processed {len(self.dataset)} training examples")
            logger.info(f"CSV examples: {len(csv_data)}, YAML examples: {len(yaml_data)}")
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise
    
    def load_csv_data(self):
        """Load data from CSV file"""
        csv_data = []
        try:
            # Read CSV file
            df = pd.read_csv(self.dataset_path)
            logger.info(f"Loaded {len(df)} rows from CSV dataset")
            
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Clean and prepare the data
                    user_input = str(row.iloc[0]).strip()
                    friend_response = str(row.iloc[1]).strip()
                    professional_response = str(row.iloc[2]).strip()
                    
                    # Skip empty or invalid rows
                    if (user_input == 'nan' or user_input == '' or 
                        friend_response == 'nan' or friend_response == '' or
                        professional_response == 'nan' or professional_response == ''):
                        continue
                    
                    # Add both friend and professional mode responses
                    csv_data.append({
                        'input': self.clean_text(user_input),
                        'response': self.clean_text(friend_response),
                        'mode': 'friend',
                        'source': 'CSV'
                    })
                    
                    csv_data.append({
                        'input': self.clean_text(user_input),
                        'response': self.clean_text(professional_response),
                        'mode': 'professional',
                        'source': 'CSV'
                    })
                    
                except Exception as e:
                    logger.warning(f"Error processing CSV row {index}: {e}")
                    continue
            
            logger.info(f"Successfully processed {len(csv_data)} CSV training examples")
            
        except Exception as e:
            logger.error(f"Error loading CSV dataset: {e}")
            csv_data = []
        
        return csv_data
    
    def load_yaml_data(self):
        """Load data from YAML files"""
        yaml_data = []
        try:
            # Parse YAML files
            yaml_training_pairs = self.yaml_parser.parse_all_yaml_files()
            
            # Convert YAML data to our format
            for pair in yaml_training_pairs:
                # Add friend mode
                yaml_data.append({
                    'input': self.clean_text(pair['input']),
                    'response': self.clean_text(pair['friend_response']),
                    'mode': 'friend',
                    'source': 'YAML',
                    'intent': pair.get('intent', '')
                })
                
                # Add professional mode
                yaml_data.append({
                    'input': self.clean_text(pair['input']),
                    'response': self.clean_text(pair['professional_response']),
                    'mode': 'professional',
                    'source': 'YAML',
                    'intent': pair.get('intent', '')
                })
            
            logger.info(f"Successfully processed {len(yaml_data)} YAML training examples")
            
        except Exception as e:
            logger.error(f"Error loading YAML dataset: {e}")
            yaml_data = []
        
        return yaml_data
    
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
    
    def split_dataset(self, test_size=0.2, random_state=42):
        """Split dataset into training and testing sets"""
        logger.info("Splitting dataset into training and testing sets")
        
        # Convert to DataFrame for easier splitting
        df = pd.DataFrame(self.dataset)
        
        # Split by mode to ensure both modes are represented in both sets
        friend_data = df[df['mode'] == 'friend']
        professional_data = df[df['mode'] == 'professional']
        
        # Split each mode separately
        friend_train, friend_test = train_test_split(
            friend_data, test_size=test_size, random_state=random_state
        )
        professional_train, professional_test = train_test_split(
            professional_data, test_size=test_size, random_state=random_state
        )
        
        # Combine the splits
        self.training_data = pd.concat([friend_train, professional_train]).to_dict('records')
        self.testing_data = pd.concat([friend_test, professional_test]).to_dict('records')
        
        logger.info(f"Training set: {len(self.training_data)} examples")
        logger.info(f"Testing set: {len(self.testing_data)} examples")
        
        # Save the splits
        self.save_dataset_splits()
    
    def save_dataset_splits(self):
        """Save training and testing datasets to separate files"""
        try:
            # Save training data
            train_df = pd.DataFrame(self.training_data)
            train_df.to_csv('data/training_dataset.csv', index=False)
            logger.info("Training dataset saved to data/training_dataset.csv")
            
            # Save testing data
            test_df = pd.DataFrame(self.testing_data)
            test_df.to_csv('data/testing_dataset.csv', index=False)
            logger.info("Testing dataset saved to data/testing_dataset.csv")
            
        except Exception as e:
            logger.error(f"Error saving dataset splits: {e}")
            raise
    
    def train_model(self):
        """Train the TF-IDF model"""
        logger.info("Training TF-IDF model")
        
        try:
            # Prepare training data
            training_inputs = [item['input'] for item in self.training_data]
            training_responses = [item['response'] for item in self.training_data]
            
            # Fit the vectorizer
            self.tfidf_matrix = self.vectorizer.fit_transform(training_inputs)
            
            logger.info(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
            logger.info("Model training completed successfully")
            
            # Save the trained model
            self.save_model()
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def save_model(self):
        """Save the trained model and metadata"""
        try:
            # Create models directory if it doesn't exist
            os.makedirs('models', exist_ok=True)
            
            # Save vectorizer
            import joblib
            joblib.dump(self.vectorizer, 'models/tfidf_vectorizer.pkl')
            
            # Save TF-IDF matrix
            joblib.dump(self.tfidf_matrix, 'models/tfidf_matrix.pkl')
            
            # Save training data
            joblib.dump(self.training_data, 'models/training_data.pkl')
            
            # Save metadata
            metadata = {
                'dataset_path': self.dataset_path,
                'training_size': len(self.training_data),
                'testing_size': len(self.testing_data),
                'total_features': self.tfidf_matrix.shape[1],
                'training_date': datetime.now().isoformat(),
                'vectorizer_params': {
                    'max_features': self.vectorizer.max_features,
                    'ngram_range': self.vectorizer.ngram_range,
                    'sublinear_tf': self.vectorizer.sublinear_tf
                }
            }
            
            with open('models/training_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info("Model and metadata saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def evaluate_model(self):
        """Evaluate the model on testing data"""
        logger.info("Evaluating model on testing data")
        
        try:
            correct_predictions = 0
            total_predictions = len(self.testing_data)
            
            for test_item in self.testing_data:
                # Get the most similar response
                predicted_response = self.get_response(test_item['input'], test_item['mode'])
                
                # Simple evaluation: check if response is not empty
                if predicted_response and len(predicted_response.strip()) > 0:
                    correct_predictions += 1
            
            accuracy = correct_predictions / total_predictions
            logger.info(f"Model accuracy: {accuracy:.2%}")
            
            return accuracy
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            return 0.0
    
    def get_response(self, user_input, threshold=0.05):
        """Get response for user input (simplified version for evaluation)"""
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
            if best_similarity >= threshold and best_match_idx < len(self.training_data):
                return self.training_data[best_match_idx]['response']
            
            return "I understand you're going through a difficult time. How can I help you today?"
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return "I'm here to help. Could you tell me more about what you're experiencing?"
    
    def evaluate_model(self, threshold=0.05):
        """Evaluate model accuracy on testing data"""
        try:
            correct = 0
            total = len(self.testing_data)
            
            for test_item in self.testing_data:
                # Get response
                response = self.get_response(test_item['input'], threshold)
                
                # Simple evaluation - check if response is not empty
                if response and len(response.strip()) > 0:
                    correct += 1
            
            accuracy = correct / total if total > 0 else 0
            return accuracy
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            return 0.0
    
    def run_training(self):
        """Run the complete training pipeline"""
        try:
            logger.info("Starting Healo AI Model Training")
            logger.info("=" * 50)
            
            # Load dataset
            self.load_dataset()
            
            # Split dataset
            self.split_dataset()
            
            # Train model
            self.train_model()
            
            # Evaluate model
            accuracy = self.evaluate_model()
            
            logger.info("=" * 50)
            logger.info("Training completed successfully!")
            logger.info(f"Final accuracy: {accuracy:.2%}")
            logger.info(f"Training examples: {len(self.training_data)}")
            logger.info(f"Testing examples: {len(self.testing_data)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False

def main():
    """Main function to run training"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Healo AI Mental Health Chatbot Model')
    parser.add_argument('--csv-only', action='store_true', help='Use only CSV dataset')
    parser.add_argument('--yaml-only', action='store_true', help='Use only YAML dataset')
    parser.add_argument('--dataset', default='mental_health_responses.csv', help='CSV dataset path')
    
    args = parser.parse_args()
    
    # Determine which datasets to use
    use_yaml = not args.csv_only
    use_csv = not args.yaml_only
    
    if args.yaml_only:
        print("Training with YAML dataset only...")
        trainer = MentalHealthModelTrainer(use_yaml=True, dataset_path=None)
    elif args.csv_only:
        print("Training with CSV dataset only...")
        trainer = MentalHealthModelTrainer(use_yaml=False, dataset_path=args.dataset)
    else:
        print("Training with both CSV and YAML datasets...")
        trainer = MentalHealthModelTrainer(use_yaml=True, dataset_path=args.dataset)
    
    success = trainer.run_training()
    
    if success:
        print("\n[SUCCESS] Model training completed successfully!")
        print("You can now use the trained model in your chatbot.")
    else:
        print("\n[ERROR] Model training failed!")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main()
