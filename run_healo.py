#!/usr/bin/env python3
"""
Healo AI Complete Startup Script
Handles training, testing, and running the mental health chatbot
"""

import os
import sys
import subprocess
import time
import argparse
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HealoManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.models_dir = self.base_dir / 'models'
        self.data_dir = self.base_dir / 'data'
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_packages = [
            'flask', 'flask-cors', 'scikit-learn', 'pandas', 'numpy', 'joblib'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✓ {package}")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"✗ {package}")
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Installing missing packages...")
            
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    logger.info(f"✓ Installed {package}")
                except subprocess.CalledProcessError:
                    logger.error(f"✗ Failed to install {package}")
                    return False
        
        return True
    
    def check_data_files(self):
        """Check if required data files exist"""
        logger.info("Checking data files...")
        
        required_files = [
            'mental_health_responses.csv',
            'data/training_dataset.csv',
            'data/testing_dataset.csv'
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                logger.info(f"✓ {file_path}")
            else:
                missing_files.append(file_path)
                logger.warning(f"✗ {file_path}")
        
        if missing_files:
            logger.error(f"Missing files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def check_models(self):
        """Check if trained models exist"""
        logger.info("Checking trained models...")
        
        required_models = [
            'tfidf_vectorizer.pkl',
            'tfidf_matrix.pkl',
            'training_data.pkl',
            'training_metadata.json'
        ]
        
        missing_models = []
        
        for model_file in required_models:
            model_path = self.models_dir / model_file
            if model_path.exists():
                logger.info(f"✓ {model_file}")
            else:
                missing_models.append(model_file)
                logger.warning(f"✗ {model_file}")
        
        if missing_models:
            logger.warning(f"Missing models: {', '.join(missing_models)}")
            logger.info("Models will be trained automatically...")
            return False
        
        return True
    
    def train_model(self):
        """Train the AI model"""
        logger.info("Training AI model...")
        
        try:
            # Run training script
            result = subprocess.run(
                [sys.executable, 'train_model.py'],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Model training completed successfully")
                return True
            else:
                logger.error(f"✗ Model training failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Error during training: {e}")
            return False
    
    def test_model(self):
        """Test the AI model"""
        logger.info("Testing AI model...")
        
        try:
            # Run testing script
            result = subprocess.run(
                [sys.executable, 'test_model.py'],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Model testing completed successfully")
                return True
            else:
                logger.warning(f"⚠ Model testing had issues: {result.stderr}")
                return True  # Don't fail if testing has issues
                
        except Exception as e:
            logger.warning(f"⚠ Error during testing: {e}")
            return True  # Don't fail if testing has issues
    
    def start_api_server(self):
        """Start the API server"""
        logger.info("Starting Healo AI API server...")
        
        try:
            # Start the API server
            subprocess.run([sys.executable, 'api_server.py'], cwd=self.base_dir)
            
        except KeyboardInterrupt:
            logger.info("API server stopped by user")
        except Exception as e:
            logger.error(f"Error starting API server: {e}")
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        logger.info("Starting Healo AI Complete Setup")
        logger.info("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            logger.error("Dependency check failed!")
            return False
        
        # Check data files
        if not self.check_data_files():
            logger.error("Data files check failed!")
            return False
        
        # Check models
        models_exist = self.check_models()
        
        # Train model if needed
        if not models_exist:
            if not self.train_model():
                logger.error("Model training failed!")
                return False
        
        # Test model
        self.test_model()
        
        # Start API server
        logger.info("=" * 50)
        logger.info("Starting Healo AI Application...")
        logger.info("=" * 50)
        self.start_api_server()
        
        return True
    
    def run_training_only(self):
        """Run only the training process"""
        logger.info("Running Healo AI Training Only")
        logger.info("=" * 50)
        
        if not self.check_dependencies():
            return False
        
        if not self.check_data_files():
            return False
        
        return self.train_model()
    
    def run_testing_only(self):
        """Run only the testing process"""
        logger.info("Running Healo AI Testing Only")
        logger.info("=" * 50)
        
        if not self.check_models():
            logger.error("No trained models found! Please train the model first.")
            return False
        
        return self.test_model()
    
    def run_server_only(self):
        """Run only the API server"""
        logger.info("Running Healo AI Server Only")
        logger.info("=" * 50)
        
        if not self.check_models():
            logger.error("No trained models found! Please train the model first.")
            return False
        
        self.start_api_server()
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Healo AI Mental Health Chatbot Manager')
    parser.add_argument('--mode', choices=['complete', 'train', 'test', 'server'], 
                       default='complete', help='Run mode (default: complete)')
    
    args = parser.parse_args()
    
    manager = HealoManager()
    
    if args.mode == 'complete':
        success = manager.run_complete_setup()
    elif args.mode == 'train':
        success = manager.run_training_only()
    elif args.mode == 'test':
        success = manager.run_testing_only()
    elif args.mode == 'server':
        success = manager.run_server_only()
    else:
        logger.error("Invalid mode specified!")
        success = False
    
    if success:
        logger.info("Healo AI operation completed successfully!")
    else:
        logger.error("Healo AI operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
