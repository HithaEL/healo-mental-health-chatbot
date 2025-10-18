# Healo AI Training and Testing System

This document explains how to use the separate training and testing scripts for the Healo Mental Health Chatbot.

## Overview

The Healo AI system now includes separate Python files for:
- **Training** (`train_model.py`) - Trains the AI model using the dataset
- **Testing** (`test_model.py`) - Tests the trained model and provides evaluation metrics
- **API Server** (`api_server.py`) - Serves the trained model via REST API
- **Complete Manager** (`run_healo.py`) - Manages the entire process

## Files Structure

```
Psykh-A-Mental-Health-Chatbot-main/
├── train_model.py              # Model training script
├── test_model.py               # Model testing script
├── trained_ai_backend.py       # Trained model backend
├── api_server.py               # Flask API server
├── run_healo.py                # Complete management script
├── requirements_training.txt   # Training dependencies
├── models/                     # Trained model files
│   ├── tfidf_vectorizer.pkl
│   ├── tfidf_matrix.pkl
│   ├── training_data.pkl
│   └── training_metadata.json
└── data/                       # Dataset files
    ├── mental_health_responses.csv
    ├── training_dataset.csv
    └── testing_dataset.csv
```

## Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements_training.txt
   ```

2. **Ensure Data Files Exist:**
   - `mental_health_responses.csv` - Main dataset
   - `data/training_dataset.csv` - Training split
   - `data/testing_dataset.csv` - Testing split

## Usage

### Option 1: Complete Setup (Recommended)

Run the complete setup which handles everything automatically:

```bash
python run_healo.py --mode complete
```

This will:
1. Check dependencies
2. Verify data files
3. Train the model (if needed)
4. Test the model
5. Start the API server

### Option 2: Individual Components

#### Training Only
```bash
python run_healo.py --mode train
```
or
```bash
python train_model.py
```

#### Testing Only
```bash
python run_healo.py --mode test
```
or
```bash
python test_model.py
```

#### Server Only
```bash
python run_healo.py --mode server
```
or
```bash
python api_server.py
```

## Training Process

The `train_model.py` script:

1. **Loads Dataset:** Reads `mental_health_responses.csv`
2. **Preprocesses Data:** Cleans and prepares text data
3. **Splits Data:** Creates 80/20 train/test split
4. **Trains Model:** Uses TF-IDF vectorization with enhanced parameters
5. **Saves Model:** Stores trained components in `models/` directory
6. **Evaluates:** Provides basic accuracy metrics

### Training Parameters

- **TF-IDF Features:** 2000 max features
- **N-gram Range:** (1, 3) for better context
- **Sublinear TF:** Enabled for better scaling
- **Stop Words:** English stop words removed
- **Test Split:** 20% of data for testing

## Testing Process

The `test_model.py` script:

1. **Loads Model:** Reads trained components from `models/`
2. **Quality Testing:** Tests response quality and accuracy
3. **Threshold Analysis:** Tests different similarity thresholds
4. **Mode Consistency:** Compares friend vs professional modes
5. **Interactive Testing:** Allows manual testing
6. **Generates Report:** Creates detailed `test_report.json`

### Test Metrics

- **Success Rate:** Percentage of successful responses
- **Fallback Rate:** Percentage of fallback responses used
- **Response Length:** Average response character count
- **Mode Accuracy:** Accuracy for different response modes
- **Threshold Optimization:** Best similarity threshold

## Model Architecture

### TrainedMentalHealthAI Class

The `trained_ai_backend.py` provides:

- **Pre-trained Model Loading:** Loads saved TF-IDF components
- **Response Generation:** Uses cosine similarity for best matches
- **Mood Analysis:** Keyword-based mood detection
- **Fallback Responses:** Graceful handling of unknown inputs
- **Mode Support:** Friend and professional response modes

### Key Features

- **Similarity Thresholding:** Configurable similarity thresholds
- **Mode Consistency:** Ensures responses match requested mode
- **Fallback System:** Robust handling of edge cases
- **Conversation History:** Tracks user interactions
- **Model Metadata:** Provides training information

## API Endpoints

The trained model is served via REST API:

- `POST /api/chat` - Main chat endpoint
- `POST /api/mood` - Mood analysis
- `GET /api/suggestions` - Mood-based suggestions
- `POST /api/conversation` - Save conversation
- `GET /api/health` - Health check with model info

## Performance Optimization

### Training Optimizations

- **Efficient Vectorization:** TF-IDF with optimized parameters
- **Memory Management:** Handles large datasets efficiently
- **Parallel Processing:** Uses scikit-learn's parallel capabilities
- **Data Validation:** Robust error handling during training

### Runtime Optimizations

- **Pre-loaded Models:** Models loaded once at startup
- **Caching:** Similarity calculations cached
- **Fallback Responses:** Quick fallback for unknown inputs
- **Memory Efficient:** Limited conversation history storage

## Troubleshooting

### Common Issues

1. **Missing Dependencies:**
   ```bash
   pip install -r requirements_training.txt
   ```

2. **Missing Data Files:**
   - Ensure `mental_health_responses.csv` exists
   - Run training to create train/test splits

3. **Model Loading Errors:**
   - Check `models/` directory exists
   - Verify all model files are present
   - Re-train if necessary

4. **Memory Issues:**
   - Reduce `max_features` in vectorizer
   - Use smaller dataset
   - Increase system memory

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Custom Training Parameters

Modify `train_model.py`:
```python
self.vectorizer = TfidfVectorizer(
    max_features=3000,  # Increase features
    ngram_range=(1, 4), # Increase n-gram range
    sublinear_tf=True,
    min_df=2,           # Add minimum document frequency
    max_df=0.95         # Add maximum document frequency
)
```

### Custom Testing

Modify `test_model.py` to add custom test cases:
```python
def custom_test_cases(self):
    test_cases = [
        "I feel really anxious about my job interview",
        "I've been having trouble sleeping lately",
        "I feel overwhelmed by all my responsibilities"
    ]
    # Add your custom testing logic
```

## Monitoring and Maintenance

### Regular Tasks

1. **Retrain Model:** When adding new data
2. **Test Performance:** Regular accuracy testing
3. **Update Dependencies:** Keep packages updated
4. **Monitor Logs:** Check for errors and warnings

### Model Updates

To update the model with new data:
1. Add new data to `mental_health_responses.csv`
2. Run training: `python train_model.py`
3. Test new model: `python test_model.py`
4. Restart API server

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Ensure data files are properly formatted
4. Check model files are complete

## License

This training and testing system is part of the Healo Mental Health Chatbot project.
