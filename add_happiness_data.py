#!/usr/bin/env python3
"""
Script to add happiness-focused training data to the mental health responses CSV
"""

import pandas as pd
import csv

def add_happiness_data():
    """Add comprehensive happiness and positive suggestion data"""
    
    # Read existing data
    try:
        df = pd.read_csv('mental_health_responses.csv')
        print(f"Loaded existing data: {len(df)} rows")
    except FileNotFoundError:
        print("Creating new CSV file...")
        df = pd.DataFrame(columns=['User Input', 'Friend Mode Response', 'Professional Mode Response'])
    
    # Happiness-focused training data
    happiness_data = [
        # General happiness and positivity
        ["I want to be happier", "I love that you're focusing on your happiness! What brings you joy? Maybe we can explore activities that make you smile, like spending time with loved ones, pursuing hobbies, or practicing gratitude. What makes you feel most alive?", "Focusing on happiness is a wonderful goal. Research shows that practicing gratitude, engaging in meaningful activities, and maintaining social connections can boost well-being. What aspects of your life currently bring you the most satisfaction?"],
        
        ["I feel sad and want to feel better", "I'm sorry you're feeling sad. Let's work on lifting your spirits together! Try doing something you love, like listening to your favorite music, going for a walk in nature, or calling a friend. Sometimes even small acts of self-care can make a big difference. What usually helps you feel better?", "Feeling sad is a natural emotion, and wanting to feel better shows self-awareness. Consider activities that have brought you joy in the past, practice self-compassion, and remember that it's okay to seek professional support. What coping strategies have worked for you before?"],
        
        ["I need motivation to be happy", "You've got this! Sometimes we need a little push to find our happiness. Try starting your day with something positive - maybe a morning walk, listening to uplifting music, or writing down three things you're grateful for. Small steps lead to big changes! What's one small thing that could make you smile today?", "Motivation for happiness often comes from taking action. Start with small, achievable goals that align with your values. Consider creating a daily routine that includes activities you enjoy, practicing mindfulness, or setting aside time for self-care. What would make you feel most fulfilled right now?"],
        
        ["I want to find joy in life", "Finding joy is such a beautiful journey! Joy can be found in the simplest things - a warm cup of coffee, a beautiful sunset, or a good laugh with friends. Try keeping a joy journal where you write down moments that make you smile. What little things in your day bring you the most happiness?", "Discovering joy in life is about being present and mindful of positive experiences. Consider exploring new hobbies, spending time in nature, or volunteering for causes you care about. Joy often comes from connection and purpose. What activities or experiences have made you feel most alive recently?"],
        
        ["I feel stuck and want to be more positive", "Feeling stuck can be frustrating, but you're already taking a positive step by wanting to change! Try shifting your perspective - what if you saw this as an opportunity to grow? Start with small positive changes like practicing gratitude or doing one thing that makes you happy each day. What would feeling unstuck look like for you?", "Feeling stuck is common, and wanting to be more positive shows great self-awareness. Consider reframing challenges as opportunities for growth. Practice positive self-talk, set small achievable goals, and celebrate your progress. Sometimes a change in routine or environment can help. What small step could you take today to move forward?"],
        
        # Specific happiness activities and suggestions
        ["What can I do to be happier?", "There are so many wonderful ways to boost your happiness! Try spending time in nature, practicing gratitude by writing down three good things each day, connecting with friends or family, doing something creative, or helping others. Exercise and good sleep also make a huge difference! What sounds most appealing to you right now?", "Happiness can be cultivated through various evidence-based practices. Consider regular exercise, maintaining social connections, practicing mindfulness or meditation, pursuing meaningful activities, and ensuring adequate sleep. Setting and working toward personal goals can also enhance well-being. What area would you like to focus on first?"],
        
        ["I want to feel more positive about life", "I love your positive mindset! Try starting each day with a positive affirmation, like 'Today I choose to see the good in life.' Practice gratitude by noticing the small beautiful moments around you. Surround yourself with positive people and content. What's one positive thing that happened to you recently?", "Cultivating a positive outlook is a skill that can be developed. Practice reframing negative thoughts, focus on your strengths and accomplishments, and engage in activities that bring you satisfaction. Consider limiting exposure to negative news or social media. What positive aspects of your life would you like to focus on more?"],
        
        ["I need help staying positive", "Staying positive is a practice, and you're doing great by asking for help! Try the 'three good things' exercise - each evening, write down three positive things that happened. Practice self-compassion when things get tough. Remember, it's okay to have difficult days - what matters is how you bounce back. What helps you feel most positive?", "Maintaining positivity requires consistent practice and self-awareness. Develop a toolkit of positive coping strategies, practice mindfulness to stay present, and challenge negative thought patterns. Remember that being positive doesn't mean ignoring problems, but rather approaching them with hope and resilience. What strategies have helped you stay positive in the past?"],
        
        ["How can I be happier at work?", "Work happiness is so important since we spend so much time there! Try building positive relationships with colleagues, taking breaks to recharge, finding meaning in your tasks, or setting small achievable goals. Maybe decorate your workspace with things that make you smile. What aspects of your work do you actually enjoy?", "Work satisfaction significantly impacts overall well-being. Consider finding purpose in your role, building positive workplace relationships, setting boundaries between work and personal time, and seeking opportunities for growth or learning. If possible, discuss workload or role adjustments with your supervisor. What changes could make your work more fulfilling?"],
        
        ["I want to be happier in my relationships", "Relationships are such an important source of happiness! Try expressing appreciation for your loved ones, spending quality time together, practicing active listening, and showing empathy. Sometimes small gestures of kindness can make a big difference. What do you appreciate most about the people in your life?", "Healthy relationships are key to happiness and well-being. Focus on effective communication, showing appreciation, spending quality time together, and supporting each other's growth. Consider couples or family therapy if needed. What aspects of your relationships would you like to strengthen?"],
        
        # Gratitude and appreciation
        ["I want to practice gratitude", "Gratitude is such a powerful happiness booster! Try keeping a gratitude journal where you write down three things you're thankful for each day. You could also practice gratitude meditation or simply take a moment each day to appreciate something beautiful around you. What are you grateful for right now?", "Practicing gratitude has been shown to significantly improve well-being and life satisfaction. Consider daily gratitude journaling, expressing appreciation to others, or mindfulness practices that focus on positive aspects of life. Even small moments of appreciation can have a big impact. What would you like to be more grateful for?"],
        
        ["I want to appreciate the good things in life", "That's such a wonderful intention! Try the 'rose, thorn, bud' exercise - each day, identify one good thing (rose), one challenge (thorn), and one thing you're looking forward to (bud). Practice mindfulness to really notice and savor the good moments. What's something beautiful you noticed today?", "Appreciating life's positive aspects is a skill that enhances happiness and resilience. Practice mindful awareness of positive experiences, keep a gratitude journal, and make time to savor enjoyable moments. Consider volunteering or helping others to gain perspective on your blessings. What positive aspects of your life would you like to appreciate more?"],
        
        # Self-care and wellness
        ["I want to take better care of myself", "Self-care is so important for happiness! Start with the basics - good sleep, nutritious food, regular exercise, and time for relaxation. Don't forget emotional self-care too, like setting boundaries, practicing self-compassion, and doing things you enjoy. What area of self-care would you like to focus on first?", "Self-care is essential for mental and physical well-being. Develop a holistic approach including physical health (exercise, nutrition, sleep), emotional wellness (stress management, self-compassion), and social connections. Remember that self-care isn't selfish - it's necessary for your overall health. What self-care practices would be most beneficial for you right now?"],
        
        ["I need to find balance in my life", "Finding balance is such an important part of happiness! Try creating a schedule that includes time for work, relationships, hobbies, and rest. Remember that balance looks different for everyone - it's about what works for you. What areas of your life feel most out of balance right now?", "Life balance is crucial for sustained happiness and well-being. Consider your priorities and values, then create a schedule that reflects them. This might include work, relationships, personal growth, health, and leisure. Remember that balance is dynamic and may need adjustment over time. What aspects of your life would you like to rebalance?"],
        
        ["I want to reduce stress and be happier", "Stress can really impact our happiness! Try deep breathing exercises, regular physical activity, spending time in nature, or practicing mindfulness. Don't forget to set boundaries and say no when you need to. What's your favorite way to relax and unwind?", "Managing stress is key to maintaining happiness and well-being. Consider stress-reduction techniques like meditation, exercise, time management, and relaxation practices. Identify your stress triggers and develop healthy coping strategies. Professional support can also be helpful for chronic stress. What stress management techniques have worked for you in the past?"],
        
        # Goal setting and motivation
        ["I want to set goals to be happier", "Setting happiness goals is such a great idea! Try making them specific and achievable - like 'I will spend 30 minutes in nature three times this week' or 'I will call a friend every Sunday.' Start small and celebrate your progress. What would make you feel most accomplished and happy?", "Goal-setting for happiness can be very effective when done thoughtfully. Make your goals SMART (Specific, Measurable, Achievable, Relevant, Time-bound) and focus on activities that align with your values and bring you joy. Consider both short-term and long-term goals. What happiness goals would be most meaningful for you?"],
        
        ["I need motivation to pursue my dreams", "Pursuing your dreams is such an exciting journey! Break your big dreams into smaller, manageable steps. Visualize your success and remind yourself why your dreams matter to you. Surround yourself with supportive people who believe in you. What's one small step you could take toward your dream today?", "Pursuing meaningful goals and dreams can significantly contribute to happiness and life satisfaction. Break large goals into smaller, actionable steps, create a timeline, and identify potential obstacles and solutions. Consider finding a mentor or support group. What resources or support do you need to move forward with your dreams?"],
        
        ["I want to find my purpose in life", "Finding your purpose is such a meaningful journey! Think about what makes you feel most alive and fulfilled. Consider your values, passions, and the impact you want to have on the world. Sometimes purpose evolves over time, so be open to exploration. What activities or causes make you feel most passionate?", "Discovering life purpose is a key component of happiness and well-being. Reflect on your values, interests, and strengths. Consider how you want to contribute to others or the world. Purpose often involves using your unique gifts to serve something larger than yourself. What would give your life the most meaning?"],
        
        # Social connections and relationships
        ["I want to make more friends", "Making friends is such a wonderful way to increase happiness! Try joining clubs or groups related to your interests, volunteering, or taking classes. Be open and authentic when meeting new people. Remember that quality friendships take time to develop. What activities do you enjoy that might help you meet like-minded people?", "Building meaningful friendships is important for happiness and well-being. Consider joining groups, clubs, or activities that align with your interests. Practice active listening and be genuinely interested in others. Remember that friendships develop gradually through shared experiences. What social activities would you like to explore?"],
        
        ["I want to strengthen my relationships", "Strengthening relationships is such a beautiful way to increase happiness! Try spending quality time together, expressing appreciation, practicing active listening, and being supportive during difficult times. Small gestures of kindness can make a big difference. What relationships would you like to focus on most?", "Strong relationships are fundamental to happiness and well-being. Focus on effective communication, showing appreciation, spending quality time together, and being supportive. Consider relationship counseling if needed. What specific aspects of your relationships would you like to improve?"],
        
        # Mindfulness and present moment
        ["I want to be more mindful and present", "Mindfulness is such a powerful tool for happiness! Try starting with just 5 minutes of meditation each day, or practice mindful breathing. Pay attention to your senses - what do you see, hear, smell, taste, and touch right now? What's one thing you can do today to be more present?", "Mindfulness practices can significantly enhance happiness and well-being. Start with short meditation sessions, practice mindful breathing, or engage in activities with full attention. Mindfulness helps you appreciate the present moment and reduce stress. What mindfulness practice would you like to try first?"],
        
        ["I want to enjoy the present moment more", "Living in the present is such a gift! Try the 5-4-3-2-1 grounding technique - notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste. Practice gratitude for the small moments. What's something beautiful you can appreciate right now?", "Enjoying the present moment is key to happiness and life satisfaction. Practice mindfulness techniques, engage your senses, and focus on what you can control right now. Let go of worries about the past or future. What present moment experience would you like to savor more?"],
        
        # Overcoming challenges with positivity
        ["I want to overcome challenges with a positive attitude", "Having a positive attitude during challenges is such a strength! Try reframing problems as opportunities for growth, focusing on what you can control, and celebrating small wins along the way. Remember that challenges often make us stronger. What's one challenge you've overcome that you're proud of?", "Maintaining a positive attitude during challenges is a valuable skill that enhances resilience and well-being. Practice reframing negative thoughts, focus on solutions rather than problems, and draw on your past successes. Consider what you can learn from difficult experiences. What strategies help you stay positive during tough times?"],
        
        ["I want to turn negative thoughts into positive ones", "Transforming negative thoughts is such a powerful skill! Try the 'thought challenging' technique - ask yourself if your negative thought is really true, helpful, or necessary. Replace it with a more balanced or positive perspective. What's one negative thought you'd like to reframe today?", "Cognitive restructuring is an effective technique for improving mood and well-being. Challenge negative thoughts by examining evidence, considering alternative perspectives, and replacing them with more balanced thoughts. Practice self-compassion and remember that thoughts are not facts. What negative thought pattern would you like to work on changing?"],
        
        # Celebration and joy
        ["I want to celebrate my achievements more", "Celebrating achievements is so important for happiness! Take time to acknowledge your wins, both big and small. Share your successes with others, treat yourself to something special, or write down what you're proud of. What achievement would you like to celebrate today?", "Celebrating achievements is crucial for maintaining motivation and happiness. Acknowledge your progress, share successes with supportive people, and create meaningful rewards for yourself. This reinforces positive behavior and builds confidence. What accomplishments would you like to recognize and celebrate?"],
        
        ["I want to find joy in everyday moments", "Finding joy in everyday moments is such a beautiful practice! Try noticing the small things - a good cup of coffee, a beautiful sky, or a kind gesture from someone. Practice gratitude for these moments. What's one small thing that brought you joy today?", "Cultivating joy in daily life enhances overall happiness and well-being. Practice mindful awareness of positive moments, keep a joy journal, and engage in activities that bring you pleasure. Remember that joy can be found in the simplest experiences. What everyday activities bring you the most joy?"],
        
        # Future happiness and hope
        ["I want to feel hopeful about the future", "Feeling hopeful about the future is such a wonderful mindset! Try focusing on what you can control and influence, setting small achievable goals, and surrounding yourself with positive influences. Remember that the future is full of possibilities. What are you most excited about for the future?", "Maintaining hope for the future is important for mental health and well-being. Focus on what you can control, set realistic goals, and practice optimism. Consider how past challenges have led to growth. What future possibilities excite you most?"],
        
        ["I want to create a happier future for myself", "Creating a happier future is such an empowering goal! Start by identifying what happiness means to you, then take small steps each day toward that vision. Remember that you have the power to shape your future through your choices today. What would your happiest future look like?", "Building a happier future requires intentional planning and action. Define what happiness means to you, set goals that align with your values, and take consistent steps toward them. Consider what changes you can make today to create the future you want. What aspects of your future happiness are most important to you?"]
    ]
    
    # Convert to DataFrame
    new_df = pd.DataFrame(happiness_data, columns=['User Input', 'Friend Mode Response', 'Professional Mode Response'])
    
    # Combine with existing data
    combined_df = pd.concat([df, new_df], ignore_index=True)
    
    # Remove duplicates based on User Input
    combined_df = combined_df.drop_duplicates(subset=['User Input'], keep='last')
    
    # Save to CSV
    combined_df.to_csv('mental_health_responses.csv', index=False)
    
    print(f"Added {len(happiness_data)} new happiness-focused entries")
    print(f"Total entries now: {len(combined_df)}")
    print("Happiness data added successfully!")

if __name__ == "__main__":
    add_happiness_data()
