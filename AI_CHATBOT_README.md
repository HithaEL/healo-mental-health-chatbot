# 🤖 Healo AI Mental Health Chatbot

An advanced AI-powered mental health chatbot built with BERT-like functionality, featuring intelligent mood analysis, contextual responses, and dual conversation modes.

## ✨ Features

### 🧠 AI-Powered Intelligence
- **BERT-like Semantic Understanding**: Uses TF-IDF vectorization and cosine similarity for intelligent response matching
- **Mood Analysis**: Automatically detects user emotions (anxious, depressed, stressed, angry, happy, neutral)
- **Contextual Responses**: Generates appropriate responses based on detected mood and conversation context
- **Dual Conversation Modes**: Friend Mode (casual, supportive) and Professional Mode (clinical, structured)

### 💬 Advanced Chat Features
- **Real-time Typing Indicators**: Visual feedback during AI processing
- **Smart Suggestions**: Context-aware quick response buttons
- **Conversation History**: Maintains chat history for better context
- **Mood Tracking**: Real-time mood indicator with color-coded status
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🎯 Mental Health Focus
- **Trained on Mental Health Dataset**: 874+ training examples from real mental health conversations
- **Professional & Friend Responses**: Each input has both casual and professional response options
- **Mood-Based Suggestions**: Provides relevant coping strategies based on detected mood
- **Crisis Awareness**: Recognizes concerning language and provides appropriate resources

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)
```bash
python start_healo.py
```
This will:
- Install all required dependencies
- Start the AI backend server
- Open your browser to the chatbot interface

### Option 2: Manual Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the AI Backend**:
   ```bash
   python api_server.py
   ```

3. **Open the Chatbot**:
   - Navigate to `http://localhost:5000/chatbot.html`
   - Or start from the main page at `http://localhost:5000`

## 🏗️ Architecture

### Frontend (JavaScript)
- **chatbot.html**: Main chat interface with modern UI
- **chatbot.js**: Client-side logic with API integration
- **index.html**: Landing page with navigation to chatbot

### Backend (Python)
- **api_server.py**: Flask REST API server
- **ai_backend.py**: Core AI logic with BERT-like functionality
- **start_healo.py**: One-click startup script

### Data
- **training_dataset.csv**: 874 mental health conversation examples
- **testing_dataset.csv**: 218 test examples for validation

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Main chat endpoint |
| `/api/mood` | POST | Analyze mood from text |
| `/api/suggestions` | GET | Get mood-based suggestions |
| `/api/conversation` | POST | Save conversation history |
| `/api/health` | GET | Health check |

### Example API Usage
```javascript
// Send a message to the chatbot
const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "I feel anxious about my job interview",
        mode: "friend"  // or "professional"
    })
});

const data = await response.json();
console.log(data.response); // AI response
console.log(data.mood);     // Detected mood
console.log(data.suggestions); // Suggested actions
```

## 🧠 AI Technology

### BERT-like Semantic Matching
- **TF-IDF Vectorization**: Converts text to numerical vectors
- **Cosine Similarity**: Finds most similar training examples
- **Contextual Understanding**: Considers conversation history and mood

### Mood Detection Algorithm
```python
mood_patterns = {
    'anxious': ['anxious', 'worried', 'nervous', 'panic', 'scared'],
    'depressed': ['depressed', 'sad', 'hopeless', 'empty', 'worthless'],
    'stressed': ['stressed', 'overwhelmed', 'pressure', 'burnout'],
    'angry': ['angry', 'mad', 'furious', 'irritated', 'frustrated'],
    'happy': ['happy', 'good', 'great', 'wonderful', 'excited']
}
```

### Response Generation
1. **Semantic Matching**: Find most similar training example
2. **Mood Analysis**: Detect user's emotional state
3. **Contextual Response**: Generate appropriate response based on mode
4. **Suggestion Generation**: Provide relevant coping strategies

## 📊 Dataset Information

- **Training Data**: 874 examples (80% of total dataset)
- **Testing Data**: 218 examples (20% of total dataset)
- **Format**: User Input, Friend Mode Response, Professional Mode Response
- **Topics Covered**: Anxiety, depression, stress, relationships, work, family, sleep

### Sample Data
```
User Input: "I feel really anxious about my exams"
Friend Response: "Ugh, exams suck, don't they? But hey, you've made it this far..."
Professional Response: "Exams can be a significant source of stress. Have you been experiencing physical symptoms..."
```

## 🎨 User Interface

### Chat Interface
- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Real-time Updates**: Instant message delivery with smooth animations
- **Mode Switching**: Easy toggle between Friend and Professional modes
- **Mood Indicator**: Color-coded mood status in header
- **Suggestion Buttons**: Quick response options for common concerns

### Responsive Design
- **Mobile Optimized**: Works perfectly on phones and tablets
- **Touch Friendly**: Large buttons and easy navigation
- **Cross-browser**: Compatible with all modern browsers

## 🔒 Privacy & Security

- **Local Processing**: All AI processing happens on your local machine
- **No Data Collection**: Conversations are not stored or transmitted
- **Secure API**: Local Flask server with CORS protection
- **Mental Health Focus**: Designed with user privacy and safety in mind

## 🛠️ Customization

### Adding New Responses
Edit `ai_backend.py` to add new response patterns:
```python
def generate_contextual_response(self, user_input, mood, mode):
    responses = {
        'your_mood': {
            'friend': ['Your friend responses here'],
            'professional': ['Your professional responses here']
        }
    }
```

### Modifying Mood Detection
Update mood patterns in `ai_backend.py`:
```python
mood_patterns = {
    'your_mood': ['keyword1', 'keyword2', 'keyword3']
}
```

## 🚨 Important Notes

### Mental Health Disclaimer
This chatbot is designed for general mental health support and should not replace professional medical advice. If you're experiencing a mental health crisis, please contact:
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

### Technical Requirements
- **Python 3.7+**
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Internet Connection** (for initial model loading)
- **4GB RAM** (recommended for smooth operation)

## 🤝 Contributing

We welcome contributions to improve Healo! Areas for improvement:
- Additional training data
- New mood detection patterns
- Enhanced response generation
- UI/UX improvements
- Mobile app development

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Dataset**: Mental Health Chatbot Dataset - Friend mode and Professional mode Responses
- **AI Libraries**: scikit-learn, pandas, numpy
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript ES6+

---

**Made with 💚 for mental health awareness and support**

*Remember: It's okay to not be okay. Reach out for help when you need it.*
