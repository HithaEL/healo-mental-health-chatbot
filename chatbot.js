// AI Mental Health Chatbot with BERT-like functionality
class MentalHealthChatbot {
    constructor() {
        this.currentMode = 'friend';
        this.conversationHistory = [];
        this.isTyping = false;
        this.apiBaseUrl = 'http://localhost:5000/api';

        this.initializeElements();
        this.initializeEventListeners();
        this.checkApiHealth();
    }

    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.suggestionButtons = document.getElementById('suggestionButtons');
    }

    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('API Health Check:', data);
        } catch (error) {
            console.error('API not available, using fallback responses:', error);
        }
    }

    parseCSV(csvText) {
        const lines = csvText.split('\n');
        const dataset = [];

        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line) {
                const columns = this.parseCSVLine(line);
                if (columns.length >= 3) {
                    dataset.push({
                        input: columns[0].replace(/"/g, ''),
                        friendResponse: columns[1].replace(/"/g, ''),
                        professionalResponse: columns[2].replace(/"/g, '')
                    });
                }
            }
        }

        return dataset;
    }

    parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];

            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }

        result.push(current);
        return result;
    }

    getFallbackDataset() {
        return [{
                input: "I feel anxious",
                friendResponse: "I totally get that feeling! Anxiety can be really overwhelming. What's making you feel anxious right now?",
                professionalResponse: "Anxiety is a common experience. Can you tell me more about what specific situations or thoughts are triggering these feelings?"
            },
            {
                input: "I'm stressed about work",
                friendResponse: "Work stress is the worst! It can really take a toll on you. Have you tried any relaxation techniques?",
                professionalResponse: "Work-related stress is very common. It might help to identify specific stressors and develop coping strategies. What aspects of work are most challenging?"
            },
            {
                input: "I feel depressed",
                friendResponse: "I'm really sorry you're going through this. Depression is tough, but you're not alone. How long have you been feeling this way?",
                professionalResponse: "Depression can significantly impact daily functioning. It's important to seek professional help if these feelings persist. Have you noticed changes in sleep, appetite, or energy levels?"
            },
            {
                input: "I can't sleep",
                friendResponse: "Ugh, insomnia is the worst! I've been there. What's keeping you up at night?",
                professionalResponse: "Sleep disturbances can affect both physical and mental health. Establishing a consistent bedtime routine and avoiding screens before bed can help. How long has this been going on?"
            },
            {
                input: "I'm having relationship problems",
                friendResponse: "Relationship issues can be really tough to navigate. What's going on? Sometimes talking it out helps.",
                professionalResponse: "Relationship challenges can be emotionally taxing. Open communication and understanding each other's perspectives are key. What specific issues are you facing?"
            }
        ];
    }

    async initializeModel() {
        try {
            // Load Universal Sentence Encoder as a BERT alternative
            this.model = await use.load();
            console.log('Model loaded successfully');
        } catch (error) {
            console.error('Error loading model:', error);
            this.model = null;
        }
    }

    initializeEventListeners() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Enter key press
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.sendBtn.disabled = true;

        // Add to conversation history
        this.conversationHistory.push({
            role: 'user',
            content: message
        });

        // Show typing indicator
        this.showTypingIndicator();

        // Generate response
        try {
            const response = await this.generateResponse(message);
            this.hideTypingIndicator();
            this.addMessage(response, 'bot');
            this.conversationHistory.push({
                role: 'bot',
                content: response
            });
        } catch (error) {
            console.error('Error generating response:', error);
            this.hideTypingIndicator();
            this.addMessage("I'm sorry, I'm having trouble processing that right now. Could you please try again?", 'bot');
        }

        this.sendBtn.disabled = false;
        this.scrollToBottom();
    }

    sendSuggestion(text) {
        this.chatInput.value = text;
        this.sendMessage();
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="bx bx-user"></i>' : '<i class="bx bx-heart"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
    }

    async generateResponse(userInput) {
        try {
            // Try to use API backend first
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userInput,
                    mode: this.currentMode
                })
            });

            if (response.ok) {
                const data = await response.json();
                return data.response;
            } else {
                throw new Error('API request failed');
            }
        } catch (error) {
            console.error('API request failed, using fallback:', error);
            return this.getFallbackResponse(userInput);
        }
    }

    async findBestMatch(userInput) {
        if (!this.model || !this.dataset) {
            return this.findBestMatchFallback(userInput);
        }

        try {
            // Encode user input
            const userEmbedding = await this.model.embed([userInput]);

            let bestMatch = null;
            let bestSimilarity = -1;

            // Compare with dataset entries in batches
            const batchSize = 50;
            for (let i = 0; i < this.dataset.length; i += batchSize) {
                const batch = this.dataset.slice(i, i + batchSize);
                const batchInputs = batch.map(item => item.input);
                const batchEmbeddings = await this.model.embed(batchInputs);

                // Calculate cosine similarity
                const similarities = this.calculateCosineSimilarity(
                    userEmbedding,
                    batchEmbeddings
                );

                const maxSimilarity = Math.max(...similarities);
                const maxIndex = similarities.indexOf(maxSimilarity);

                if (maxSimilarity > bestSimilarity) {
                    bestSimilarity = maxSimilarity;
                    bestMatch = batch[maxIndex];
                }
            }

            // Only return if similarity is above threshold
            return bestSimilarity > 0.3 ? bestMatch : null;

        } catch (error) {
            console.error('Error in semantic matching:', error);
            return this.findBestMatchFallback(userInput);
        }
    }

    calculateCosineSimilarity(embedding1, embedding2) {
        const similarities = [];

        for (let i = 0; i < embedding2.shape[0]; i++) {
            const dotProduct = tf.sum(tf.mul(embedding1, embedding2.slice([i, 0], [1, -1])));
            const norm1 = tf.norm(embedding1);
            const norm2 = tf.norm(embedding2.slice([i, 0], [1, -1]));
            const similarity = tf.div(dotProduct, tf.mul(norm1, norm2));
            similarities.push(similarity.dataSync()[0]);
        }

        return similarities;
    }

    findBestMatchFallback(userInput) {
        const input = userInput.toLowerCase();

        // Simple keyword matching
        const keywords = {
            'anxious': ['anxious', 'anxiety', 'worried', 'nervous', 'panic'],
            'depressed': ['depressed', 'depression', 'sad', 'down', 'hopeless'],
            'stressed': ['stressed', 'stress', 'overwhelmed', 'pressure'],
            'sleep': ['sleep', 'insomnia', 'tired', 'exhausted'],
            'relationship': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'marriage'],
            'work': ['work', 'job', 'career', 'boss', 'colleague'],
            'family': ['family', 'parent', 'mother', 'father', 'sibling']
        };

        let bestCategory = null;
        let maxMatches = 0;

        for (const [category, words] of Object.entries(keywords)) {
            const matches = words.filter(word => input.includes(word)).length;
            if (matches > maxMatches) {
                maxMatches = matches;
                bestCategory = category;
            }
        }

        if (bestCategory) {
            return this.dataset.find(item =>
                item.input.toLowerCase().includes(bestCategory) ||
                item.friendResponse.toLowerCase().includes(bestCategory) ||
                item.professionalResponse.toLowerCase().includes(bestCategory)
            );
        }

        return null;
    }

    generateContextualResponse(userInput) {
        const mood = this.analyzeMood(userInput);
        const responses = {
            anxious: {
                friend: "I can hear that you're feeling anxious. That's totally valid! What's on your mind that's making you feel this way?",
                professional: "Anxiety can be challenging to manage. It might help to practice deep breathing or grounding techniques. What specific thoughts or situations are contributing to your anxiety?"
            },
            depressed: {
                friend: "I'm really sorry you're going through a tough time. Depression can feel isolating, but you're not alone. How long have you been feeling this way?",
                professional: "Depression can significantly impact your daily life. It's important to consider professional help if these feelings persist. Have you noticed changes in your sleep, appetite, or interest in activities?"
            },
            stressed: {
                friend: "Stress can really take a toll on you! What's been stressing you out lately? Sometimes talking about it helps.",
                professional: "Chronic stress can affect both physical and mental health. Identifying stress triggers and developing coping strategies is important. What areas of your life are causing the most stress?"
            },
            neutral: {
                friend: "Thanks for sharing that with me. I'm here to listen and help however I can. What else is on your mind?",
                professional: "I appreciate you opening up. It's important to express your feelings and concerns. Is there anything specific you'd like to discuss or work through?"
            }
        };

        return responses[mood][this.currentMode];
    }

    getFallbackResponse(userInput) {
        const responses = {
            friend: [
                "I'm here for you! Can you tell me more about what's going on?",
                "That sounds really tough. I'm listening - what else is on your mind?",
                "I understand this is difficult for you. How can I best support you right now?",
                "You're not alone in this. What would help you feel better today?"
            ],
            professional: [
                "I appreciate you sharing that with me. Can you help me understand more about your current situation?",
                "It takes courage to talk about these feelings. What specific challenges are you facing?",
                "I'm here to help you work through this. What would you like to focus on today?",
                "Thank you for being open with me. How can I best assist you in this moment?"
            ]
        };

        const modeResponses = responses[this.currentMode];
        return modeResponses[Math.floor(Math.random() * modeResponses.length)];
    }


    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new MentalHealthChatbot();
});

// Global functions for HTML onclick events
function sendMessage() {
    if (window.chatbot) {
        window.chatbot.sendMessage();
    }
}

function sendSuggestion(text) {
    if (window.chatbot) {
        window.chatbot.sendSuggestion(text);
    }
}