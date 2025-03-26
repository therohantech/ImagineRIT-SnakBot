import random
import numpy as np
from transformers import pipeline

class AIInteractionManager:
    def __init__(self):
        # Load pre-trained conversational AI
        self.conversational_ai = pipeline('conversational')
        
        # Predefined interaction scripts
        self.welcome_messages = [
            "Welcome to SnackBot! How can I assist you today?",
            "Hello! Ready to explore our delicious snack options?",
            "Greetings! I'm here to make your snack experience amazing."
        ]
        
        self.technical_explanations = {
            'popcorn': "Our robotic system precisely controls popcorn kernels...",
            'coffee': "We use advanced temperature and pressure control...",
            'robotics': "Each robotic arm is calibrated for millimeter-precise movements..."
        }
    
    def generate_welcome_message(self):
        """
        Generate personalized welcome message
        """
        return random.choice(self.welcome_messages)
    
    def provide_technical_explanation(self, topic):
        """
        Generate technical explanation about system
        """
        return self.technical_explanations.get(topic, "Let me tell you about our amazing technology!")
    
    def process_user_query(self, user_input):
        """
        Process and respond to user queries
        """
        # Use conversational AI to generate response
        response = self.conversational_ai(user_input)
        return response
    
    def detect_intent(self, user_input):
        """
        Detect user's intent from input
        """
        intents = {
            'order': ['order', 'get', 'want'],
            'info': ['how', 'why', 'explain'],
            'greeting': ['hi', 'hello', 'hey']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return intent
        
        return 'unknown'
