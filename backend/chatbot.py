import random
import re
from datetime import datetime

class BushraChatbot:
    """A warm and empathetic chatbot to help users with mental health support."""

    def __init__(self):
        self.greetings = [
            "Hello, I'm Bushra. How can I help you today?",
            "Hi there! I'm Bushra, your mental wellness companion. What's on your mind?",
            "Welcome! I'm here to listen and support you. How are you feeling today?"
        ]
        
        self.farewells = [
            "Take care and remember, you are not alone.",
            "Goodbye for now. Stay strong, and I'll always be here if you need me.",
            "Thank you for sharing with me. Wishing you peace and strength."
        ]
        
        self.responses = {
            "sad": [
                "I'm sorry you're feeling sad. Can you share what's troubling you?",
                "Sadness can be overwhelming. Take your time and let it out. I'm here to listen.",
                "You're doing your best, even if it feels hard right now."
            ],
            "anxious": [
                "Anxiety can be tough. Let's focus on breathing: Inhale... exhale... Can you try that with me?",
                "It's okay to feel anxious. What's making you feel this way?",
                "Remember, you’re not alone in this. One step at a time, we’ll get through it."
            ],
            "angry": [
                "Anger can be intense. It's okay to feel this way. Do you want to talk about it?",
                "I’m here to help you process your anger. Let’s take a deep breath together.",
                "Sometimes expressing anger helps. What's on your mind?"
            ],
            "happy": [
                "That’s wonderful! Tell me more about what’s making you happy.",
                "Happiness looks good on you. What’s been going well for you?",
                "I’m glad to hear that! Let’s celebrate this moment together."
            ],
            "fearful": [
                "Fear can feel overwhelming. Can you tell me what’s causing it?",
                "You are safe here with me. Let’s talk about what’s making you feel this way.",
                "It’s brave to face your fears. Let’s work through them together."
            ],
            "mixed": [
                "It sounds like you’re feeling a mix of emotions. Let’s take it one step at a time.",
                "Having mixed feelings can be confusing. Share more with me, and we’ll sort through it.",
                "It’s okay to feel complex emotions. You’re navigating them as best as you can."
            ],
            "neutral": [
                "I’m here to support you. What’s on your mind today?",
                "Sometimes sharing helps, even when you’re not sure how you feel. Let’s talk.",
                "I’m listening. Feel free to share anything you’d like."
            ]
        }
    
    def get_greeting(self):
        """Return a random greeting message."""
        return random.choice(self.greetings)
    
    def get_farewell(self):
        """Return a random farewell message."""
        return random.choice(self.farewells)
    
    def detect_emotion(self, user_message):
        """
        Detect the emotion from a user's message using keyword-based logic.
        
        Parameters:
            user_message (str): The user's input message.
            
        Returns:
            tuple: (emotion, confidence)
        """
        emotions = {
            "sad": ["sad", "unhappy", "down", "depressed", "crying"],
            "anxious": ["anxious", "worried", "nervous", "stress", "overwhelmed"],
            "angry": ["angry", "mad", "furious", "irritated", "annoyed"],
            "happy": ["happy", "joyful", "excited", "great", "awesome"],
            "fearful": ["scared", "afraid", "fear", "terrified", "panic"]
        }
        
        detected_emotions = []
        user_message = user_message.lower()
        
        # Check for emotion keywords
        for emotion, keywords in emotions.items():
            if any(word in user_message for word in keywords):
                detected_emotions.append(emotion)
        
        # Determine the confidence level (mock logic)
        confidence = 0.85 + (0.05 * len(detected_emotions)) if detected_emotions else 0.75
        
        # Handle mixed emotions
        if len(detected_emotions) > 1:
            return "mixed", confidence
        elif detected_emotions:
            return detected_emotions[0], confidence
        else:
            return "neutral", confidence
    
    def generate_response(self, emotion, user_message):
        """
        Generate a response based on the detected emotion.
        
        Parameters:
            emotion (str): The detected emotion.
            user_message (str): The user's input message.
            
        Returns:
            str: The chatbot's response.
        """
        if emotion not in self.responses:
            emotion = "neutral"  # Default to neutral if emotion is not recognized
        
        response = random.choice(self.responses[emotion])
        return response
    
    

    pass

    def process_message(self, user_message):
        """
        Process the user's message and return a response.
        
        Parameters:
            user_message (str): The user's input message.
            
        Returns:
            dict: A dictionary containing the chatbot's response, detected emotion, and confidence.
        """
        emotion, confidence = self.detect_emotion(user_message)
        response = self.generate_response(emotion, user_message)
        return {
            "response": response,
            "emotion": emotion,
            "confidence": confidence,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
