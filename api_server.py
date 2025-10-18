#!/usr/bin/env python3
"""
Flask API Server for Healo Mental Health Chatbot
Provides REST API endpoints for the AI backend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from improved_ai_backend import ImprovedMentalHealthAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize improved AI backend
ai_backend = ImprovedMentalHealthAI()

@app.route('/')
def serve_index():
    """Serve the main index page"""
    return send_from_directory('.', 'index.html')

@app.route('/chatbot.html')
def serve_chatbot():
    """Serve the chatbot page"""
    return send_from_directory('.', 'chatbot.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        mode = data.get('mode', 'friend')
        conversation_history = data.get('conversation_history', [])
        
        if not user_input:
            return jsonify({
                'error': 'Message cannot be empty',
                'response': 'Please enter a message to continue our conversation.'
            }), 400
        
        # Generate response using AI backend
        response = ai_backend.generate_response(user_input, mode)
        mood = ai_backend.analyze_mood(user_input)
        suggestions = ai_backend.get_suggestions(mood)
        
        # Get contextual happiness suggestions
        happiness_suggestions = ai_backend.get_happiness_suggestions(user_input, conversation_history)
        
        return jsonify({
            'response': response,
            'mood': mood,
            'suggestions': suggestions[:3],  # Return top 3 suggestions
            'happiness_suggestions': happiness_suggestions[:3],  # Return top 3 happiness suggestions
            'mode': mode
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': "I'm sorry, I'm having trouble processing that right now. Could you please try again?"
        }), 500

@app.route('/api/mood', methods=['POST'])
def analyze_mood():
    """Analyze mood from text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        mood = ai_backend.analyze_mood(text)
        suggestions = ai_backend.get_suggestions(mood)
        
        return jsonify({
            'mood': mood,
            'suggestions': suggestions[:3]
        })
        
    except Exception as e:
        print(f"Error in mood analysis: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggestions for a specific mood"""
    try:
        mood = request.args.get('mood', 'neutral')
        suggestions = ai_backend.get_suggestions(mood)
        
        return jsonify({
            'mood': mood,
            'suggestions': suggestions
        })
        
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_info = ai_backend.get_model_info()
    return jsonify({
        'status': 'healthy',
        'message': 'Healo AI Backend is running',
        'model_info': model_info
    })

@app.route('/api/conversation', methods=['POST'])
def save_conversation():
    """Save conversation history"""
    try:
        data = request.get_json()
        conversation = data.get('conversation', [])
        
        if not conversation:
            return jsonify({'error': 'Conversation data is required'}), 400
        
        # Save conversation
        ai_backend.save_conversation(conversation)
        
        return jsonify({
            'message': 'Conversation saved successfully',
            'saved_entries': len(conversation)
        })
        
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/happiness-suggestions', methods=['POST'])
def get_happiness_suggestions():
    """Get contextual happiness suggestions"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])
        
        if not user_input:
            return jsonify({'error': 'Message is required'}), 400
        
        suggestions = ai_backend.get_happiness_suggestions(user_input, conversation_history)
        
        return jsonify({
            'happiness_suggestions': suggestions,
            'message': 'Happiness suggestions generated successfully'
        })
        
    except Exception as e:
        print(f"Error getting happiness suggestions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/happiness-boost', methods=['GET'])
def get_quick_happiness_boost():
    """Get a quick happiness boost suggestion"""
    try:
        boost = ai_backend.get_quick_happiness_boost()
        
        return jsonify({
            'happiness_boost': boost,
            'message': 'Quick happiness boost suggestion generated'
        })
        
    except Exception as e:
        print(f"Error getting happiness boost: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/happiness-habits', methods=['GET'])
def get_happiness_habits():
    """Get suggested happiness-building habits"""
    try:
        habits = ai_backend.get_happiness_habits()
        
        return jsonify({
            'happiness_habits': habits,
            'message': 'Happiness habits suggestions generated'
        })
        
    except Exception as e:
        print(f"Error getting happiness habits: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/happiness-plan', methods=['POST'])
def generate_happiness_plan():
    """Generate a personalized happiness plan"""
    try:
        data = request.get_json()
        user_goals = data.get('goals', [])
        
        plan = ai_backend.generate_happiness_plan(user_goals)
        
        return jsonify({
            'happiness_plan': plan,
            'message': 'Personalized happiness plan generated'
        })
        
    except Exception as e:
        print(f"Error generating happiness plan: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Healo AI Backend Server...")
    print("=" * 50)
    print("Available endpoints:")
    print("- GET  /                    : Main page")
    print("- GET  /chatbot.html        : Chatbot interface")
    print("- POST /api/chat            : Chat with AI")
    print("- POST /api/mood            : Analyze mood")
    print("- GET  /api/suggestions     : Get mood-based suggestions")
    print("- POST /api/conversation    : Save conversation")
    print("- GET  /api/health          : Health check")
    print("- POST /api/happiness-suggestions : Get contextual happiness suggestions")
    print("- GET  /api/happiness-boost : Get quick happiness boost")
    print("- GET  /api/happiness-habits : Get happiness-building habits")
    print("- POST /api/happiness-plan  : Generate personalized happiness plan")
    print("=" * 50)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
