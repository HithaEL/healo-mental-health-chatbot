#!/usr/bin/env python3
"""
Add Robust Training Data for Accuracy Improvement
This script safely adds training data while handling CSV parsing issues
"""

import csv
import os
import random

CSV_FILE = 'data/Mental Health Chatbot Dataset - Friend mode and Professional mode Responses.csv'

# Advanced training data with better quality and diversity
advanced_data = [
    # Complex emotional states and nuanced responses
    {"User Input": "I feel like I'm drowning in responsibilities but also guilty for not doing enough.", "Friend Mode Response": "Oh wow, that's such a heavy feeling - being overwhelmed AND guilty at the same time. That's like emotional whiplash! What's making you feel like you're not doing enough?", "Professional Mode Response": "Experiencing both overwhelm and guilt simultaneously can be particularly challenging. This combination often indicates high self-expectations. Can you identify which responsibilities feel most pressing right now?"},
    
    {"User Input": "I'm happy about my promotion but terrified I'll mess it up.", "Friend Mode Response": "Dude, imposter syndrome hitting you right when you should be celebrating! That's so unfair. What makes you think you'll mess it up? You got promoted for a reason!", "Professional Mode Response": "Mixed emotions about success are common, especially with imposter syndrome. The fear of failure can overshadow achievement. What specific aspects of the new role concern you most?"},
    
    {"User Input": "I feel numb most days but then suddenly everything hits me at once.", "Friend Mode Response": "That emotional rollercoaster is exhausting! Like you're walking around in a fog and then BAM - all the feels hit you like a truck. What usually triggers those sudden emotional waves?", "Professional Mode Response": "Emotional numbness alternating with intense feelings can indicate emotional dysregulation. This pattern often suggests the need for emotional processing strategies. Have you noticed any patterns in what triggers these intense episodes?"},
    
    {"User Input": "I'm constantly worried about what others think but also feel invisible.", "Friend Mode Response": "That's such a weird contradiction, right? Like you're hyper-aware of everyone's opinions but also feel like you don't matter. That must be so confusing and exhausting. What's that like for you?", "Professional Mode Response": "The paradox of being hypervigilant about others' perceptions while feeling invisible suggests complex self-worth issues. This combination often stems from past experiences. How long have you been experiencing this pattern?"},
    
    {"User Input": "I want to be alone but I'm scared of being alone.", "Friend Mode Response": "Ugh, that's such a relatable contradiction! You crave solitude but then when you get it, it feels scary and empty. It's like your brain is playing tricks on you. What does being alone feel like for you?", "Professional Mode Response": "The conflict between wanting solitude and fearing isolation is common in anxiety and depression. This ambivalence often reflects underlying attachment or self-regulation issues. What do you think might be driving this fear of being alone?"},
    
    # Advanced coping strategies and responses
    {"User Input": "I've tried everything to feel better but nothing works.", "Friend Mode Response": "That's so frustrating when you're putting in all this effort and nothing seems to stick! It's like you're running on a hamster wheel. What have you tried so far? Maybe we can figure out why it's not clicking.", "Professional Mode Response": "Feeling like nothing works despite trying various approaches can be discouraging. Sometimes the timing or combination of strategies matters. What specific methods have you attempted, and for how long did you try each one?"},
    
    {"User Input": "I know I should be grateful but I just feel empty inside.", "Friend Mode Response": "Oh man, that 'should' word is such a trap! You can't force gratitude when you're feeling empty - that's like trying to smile when you want to cry. What's making you feel empty right now?", "Professional Mode Response": "The pressure to feel grateful while experiencing emptiness can create additional emotional burden. This disconnect between what you 'should' feel and what you actually feel is valid. What do you think might be contributing to this sense of emptiness?"},
    
    {"User Input": "I'm scared I'll never be happy again.", "Friend Mode Response": "That fear is so real and scary! It's like you're looking into this dark tunnel and can't see any light at the end. But feelings aren't permanent, even when they feel like they are. What's making you feel like happiness is gone forever?", "Professional Mode Response": "The fear of permanent unhappiness is a common symptom of depression. This 'forever' feeling is often a cognitive distortion. Have you experienced periods of happiness before, and if so, what helped you through difficult times?"},
    
    {"User Input": "I feel like I'm pretending to be okay all the time.", "Friend Mode Response": "The 'I'm fine' mask is so exhausting to wear! It's like you're performing happiness for everyone else while you're falling apart inside. That takes so much energy. Who do you feel like you have to pretend for?", "Professional Mode Response": "Constantly pretending to be okay can lead to emotional exhaustion and disconnection from authentic feelings. This 'masking' behavior often stems from fear of judgment or burdening others. What would it feel like to be more authentic about your struggles?"},
    
    {"User Input": "I'm angry at myself for not being stronger.", "Friend Mode Response": "Being angry at yourself for struggling is like kicking yourself when you're already down! You're being so hard on yourself. What does 'stronger' look like to you? Because asking for help IS strength, not weakness.", "Professional Mode Response": "Self-directed anger often masks deeper feelings of shame or inadequacy. The expectation to be 'stronger' can be unrealistic and harmful. What does strength mean to you, and where do you think these expectations come from?"},
    
    # Relationship and social dynamics
    {"User Input": "I feel like I'm always the one reaching out to friends.", "Friend Mode Response": "Ugh, that one-sided friendship energy is so draining! It's like you're the only one putting in effort and they're just... there. Have you tried talking to them about it? Maybe they don't realize how it feels.", "Professional Mode Response": "Feeling like the primary initiator in relationships can lead to resentment and emotional exhaustion. This pattern often reflects different communication styles or priorities. Have you noticed if this happens with all your relationships or specific ones?"},
    
    {"User Input": "I'm scared of being vulnerable with people I care about.", "Friend Mode Response": "Vulnerability is scary! It's like handing someone your heart and hoping they don't drop it. But the people who matter won't mind, and the people who mind don't matter. What makes it feel so risky for you?", "Professional Mode Response": "Fear of vulnerability often stems from past experiences of rejection or betrayal. This protective mechanism can prevent deep connections. What experiences have made you cautious about being open with others?"},
    
    {"User Input": "I feel like I'm too much for people to handle.", "Friend Mode Response": "That 'too much' feeling is so painful! It's like you're walking on eggshells around your own personality. But the right people will love all of you, even the messy parts. What makes you feel like you're too much?", "Professional Mode Response": "Feeling 'too much' often indicates shame about your authentic self or past experiences of rejection. This belief can lead to people-pleasing or emotional suppression. What specific aspects of yourself do you worry are 'too much'?"},
    
    {"User Input": "I don't know how to set boundaries without feeling guilty.", "Friend Mode Response": "Boundary guilt is so real! It's like you're being mean just for protecting yourself. But boundaries aren't walls - they're doors with locks that you control. What kind of boundaries are you trying to set?", "Professional Mode Response": "Guilt around boundary-setting often stems from people-pleasing patterns or fear of conflict. Healthy boundaries are essential for mental well-being. What specific situations are making you feel guilty about setting limits?"},
    
    # Work and life balance
    {"User Input": "I'm burned out but I can't afford to slow down.", "Friend Mode Response": "That's such a catch-22! You're running on empty but feel like you can't stop. It's like being stuck on a treadmill that's going too fast. What would slowing down look like for you?", "Professional Mode Response": "Burnout while feeling unable to slow down creates a dangerous cycle. This often leads to decreased productivity and increased health risks. What would need to change for you to feel safe slowing down?"},
    
    {"User Input": "I feel like I'm failing at everything important to me.", "Friend Mode Response": "That 'failing at everything' feeling is so overwhelming! It's like you're looking at your life through a funhouse mirror where everything looks distorted. What does 'important' mean to you right now?", "Professional Mode Response": "The perception of failing at everything important often indicates depression or unrealistic self-expectations. This all-or-nothing thinking can be harmful. Can you identify any areas where you're actually succeeding, even in small ways?"},
    
    {"User Input": "I'm scared I'm wasting my life but don't know what to do.", "Friend Mode Response": "That fear of wasting time is so paralyzing! It's like you're frozen because you don't want to make the wrong choice. But even 'wrong' choices teach us something. What would you do if you weren't afraid of wasting time?", "Professional Mode Response": "Fear of wasting life often stems from perfectionism or external pressure to achieve certain milestones. This anxiety can prevent action. What does a 'wasted' life look like to you, and what would a meaningful life look like?"},
    
    # Identity and self-discovery
    {"User Input": "I don't know who I am anymore.", "Friend Mode Response": "That identity crisis is so disorienting! It's like looking in the mirror and seeing a stranger. But maybe you're not lost - maybe you're just changing and growing. What feels different about yourself lately?", "Professional Mode Response": "Feeling disconnected from your identity can be a sign of major life transitions or underlying mental health concerns. This often occurs during periods of significant change. What events or changes have led to this feeling of not knowing yourself?"},
    
    {"User Input": "I feel like I'm living someone else's life.", "Friend Mode Response": "That's such a surreal feeling! Like you're watching yourself go through the motions but it's not really you. It's like you're in a movie about someone else's life. What would your authentic life look like?", "Professional Mode Response": "Feeling like you're living someone else's life often indicates a disconnect between your authentic self and your current circumstances. This can lead to depression and anxiety. What aspects of your current life feel most inauthentic?"},
    
    {"User Input": "I'm scared of making the wrong life choices.", "Friend Mode Response": "Decision paralysis is so real! It's like every choice feels like it could ruin everything. But there's no such thing as a perfect choice - just choices that lead to different experiences. What's the worst that could happen if you made a 'wrong' choice?", "Professional Mode Response": "Fear of making wrong choices often stems from perfectionism or past experiences with regret. This anxiety can prevent growth and fulfillment. What would need to be true for you to feel more confident about your decision-making?"},
    
    # Trauma and healing
    {"User Input": "I feel like my past is holding me back from being happy.", "Friend Mode Response": "That past baggage is so heavy! It's like carrying around a backpack full of rocks everywhere you go. But your past doesn't have to define your future. What from your past feels most stuck with you?", "Professional Mode Response": "Feeling held back by past experiences is common in trauma recovery. The past can influence present happiness, but healing is possible. What specific experiences from your past feel most challenging to move beyond?"},
    
    {"User Input": "I'm scared I'll never heal from what happened to me.", "Friend Mode Response": "That fear of never healing is so scary! It's like you're stuck in this dark place and can't see a way out. But healing isn't linear - it's more like a spiral where you keep coming back to things but from different angles. What does healing look like to you?", "Professional Mode Response": "The fear of never healing often indicates trauma or significant past experiences. Healing is a process that takes time and often requires professional support. What specific experiences are you working to heal from?"},
    
    {"User Input": "I feel broken and don't know if I can be fixed.", "Friend Mode Response": "You're not broken - you're human! It's like you've been through a storm and your ship is damaged, but ships can be repaired and made stronger. What makes you feel broken? Because feeling broken is often the first step to healing.", "Professional Mode Response": "Feeling 'broken' often indicates trauma, depression, or significant life challenges. This belief can be harmful to self-worth and recovery. What experiences have led you to feel this way, and what would 'being fixed' look like to you?"},
    
    # Future and uncertainty
    {"User Input": "I'm terrified of the future but also excited about it.", "Friend Mode Response": "That mix of terror and excitement is so confusing! It's like your emotions are playing tug-of-war. The future is scary because it's unknown, but also exciting for the same reason. What parts are you most excited about?", "Professional Mode Response": "Mixed feelings about the future are common, especially during transitions. This ambivalence often reflects both hope and anxiety. What specific aspects of the future excite you, and what aspects create the most fear?"},
    
    {"User Input": "I feel like I'm running out of time to figure out my life.", "Friend Mode Response": "That time pressure is so intense! It's like you're in a race against the clock to have everything figured out. But there's no deadline for life - everyone figures it out at their own pace. What makes you feel like time is running out?", "Professional Mode Response": "Feeling pressure to figure out life quickly often stems from societal expectations or internalized timelines. This urgency can create anxiety and poor decision-making. What timeline are you comparing yourself to, and where do you think this pressure comes from?"},
    
    {"User Input": "I'm scared I'll regret the choices I'm making now.", "Friend Mode Response": "Regret anxiety is so paralyzing! It's like you're trying to predict the future and avoid all possible mistakes. But you can't live a life without regrets - they're part of being human. What would you do if you knew you couldn't regret it later?", "Professional Mode Response": "Fear of future regret often indicates anxiety about decision-making or past experiences with regret. This fear can prevent you from making necessary life choices. What past regrets are influencing your current decision-making?"},
    
    # Self-care and recovery
    {"User Input": "I know I need to take care of myself but I don't know how.", "Friend Mode Response": "Self-care can feel so overwhelming when you're already struggling! It's like you need to learn a whole new language. But it doesn't have to be complicated - it's just about being kind to yourself. What does being kind to yourself look like?", "Professional Mode Response": "Not knowing how to practice self-care is common, especially when you're used to prioritizing others. Self-care is highly individual and requires experimentation. What activities or practices have brought you comfort or joy in the past?"},
    
    {"User Input": "I feel like I'm too broken to be helped.", "Friend Mode Response": "That 'too broken' feeling is so isolating! It's like you're standing outside a house with the lights on, thinking you don't belong inside. But everyone deserves help and healing, no matter how broken they feel. What makes you feel like you're beyond help?", "Professional Mode Response": "Feeling 'too broken' to be helped often indicates severe depression or trauma. This belief can prevent you from seeking necessary support. What experiences have led you to feel this way, and what would help look like if you believed you deserved it?"},
    
    {"User Input": "I'm tired of trying to get better.", "Friend Mode Response": "Recovery fatigue is so real! It's like you've been climbing this mountain forever and you're just exhausted. But you don't have to climb alone, and you can take breaks. What would taking a break from 'getting better' look like?", "Professional Mode Response": "Feeling tired of recovery efforts often indicates burnout in the healing process. This is normal and doesn't mean you're failing. What aspects of your recovery feel most exhausting right now?"},
    
    # Social anxiety and isolation
    {"User Input": "I want to connect with people but I'm scared they'll reject me.", "Friend Mode Response": "That fear of rejection is so powerful! It's like you're standing at the edge of a pool, wanting to jump in but scared of the cold water. But the right people will welcome you with open arms. What's the worst that could happen if someone rejected you?", "Professional Mode Response": "Fear of rejection often stems from past experiences or low self-worth. This fear can lead to social isolation and loneliness. What specific rejection scenarios are you most afraid of?"},
    
    {"User Input": "I feel like I don't belong anywhere.", "Friend Mode Response": "That belonging struggle is so painful! It's like you're looking for your tribe but can't find them. But your people are out there - sometimes you just have to keep looking. What kind of people do you wish you could connect with?", "Professional Mode Response": "Feeling like you don't belong anywhere often indicates social anxiety, depression, or identity issues. This can lead to isolation and low self-worth. What groups or communities have you tried to connect with, and what happened?"},
    
    {"User Input": "I'm scared of being judged for my mental health struggles.", "Friend Mode Response": "Mental health stigma is so real and scary! It's like you're carrying this secret that you're afraid will change how people see you. But the people who matter won't judge you for struggling. Who in your life do you think would be understanding?", "Professional Mode Response": "Fear of judgment about mental health is common due to societal stigma. This fear can prevent you from seeking support. What specific judgments are you most afraid of, and have you had any positive experiences sharing your struggles?"},
    
    # Purpose and meaning
    {"User Input": "I feel like my life has no purpose or meaning.", "Friend Mode Response": "That purposeless feeling is so heavy! It's like you're going through the motions but there's no 'why' behind it. But purpose isn't something you find - it's something you create. What makes you feel alive, even for a moment?", "Professional Mode Response": "Feeling a lack of purpose often indicates depression or major life transitions. Purpose can be found in many places - relationships, work, hobbies, or helping others. What activities or experiences have given you a sense of meaning in the past?"},
    
    {"User Input": "I'm scared I'll never find my passion or calling.", "Friend Mode Response": "That passion pressure is so intense! It's like everyone expects you to have this one thing that sets your soul on fire. But passion isn't always obvious - sometimes it's quiet and grows slowly. What makes you lose track of time?", "Professional Mode Response": "Fear of never finding passion often stems from pressure to have a clear life direction. Passion can develop gradually and change over time. What activities or subjects have you found yourself drawn to, even if you're not sure why?"},
    
    {"User Input": "I feel like I'm just existing, not really living.", "Friend Mode Response": "That 'just existing' feeling is so hollow! It's like you're watching life happen around you but not participating in it. But you're not just existing - you're here, you're feeling, you're reaching out. That's living. What would really living look like to you?", "Professional Mode Response": "Feeling like you're just existing often indicates depression or disconnection from life. This can be a sign that you need to reconnect with your values and interests. What would need to change for you to feel like you're truly living?"}
]

def add_robust_training_data():
    """Add training data using robust CSV handling"""
    try:
        print("Adding robust training data for accuracy improvement...")
        
        # Read existing data line by line to handle parsing issues
        existing_data = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8', errors='ignore') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i == 0:  # Skip header
                        continue
                    if len(row) >= 3:  # Only process rows with at least 3 columns
                        existing_data.append({
                            'User Input': row[0] if len(row) > 0 else '',
                            'Friend Mode Response': row[1] if len(row) > 1 else '',
                            'Professional Mode Response': row[2] if len(row) > 2 else ''
                        })
        
        print(f"Loaded existing data: {len(existing_data)} rows")
        
        # Add new advanced data
        all_data = existing_data + advanced_data
        
        # Remove duplicates based on user input
        seen_inputs = set()
        unique_data = []
        for item in all_data:
            if item['User Input'] not in seen_inputs:
                seen_inputs.add(item['User Input'])
                unique_data.append(item)
        
        # Write back to CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['User Input', 'Friend Mode Response', 'Professional Mode Response']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_data)
        
        added_count = len(unique_data) - len(existing_data)
        print(f"Added {added_count} new advanced training examples")
        print(f"Total training examples: {len(unique_data)}")
        print("Robust training data added successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error adding robust training data: {e}")
        return False

if __name__ == "__main__":
    success = add_robust_training_data()
    if success:
        print("\n[SUCCESS] Robust training data added successfully!")
    else:
        print("\n[ERROR] Failed to add robust training data!")
