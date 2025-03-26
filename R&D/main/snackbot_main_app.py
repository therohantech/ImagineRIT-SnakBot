import sys
import numpy as np
import cv2
import pyttsx3
import speech_recognition as sr
from zed_camera_module import ZEDCameraAnalyzer
from robotic_arm_controller import RoboticArmSystem
from ai_interaction_manager import AIInteractionManager
from snack_recommendation_engine import SnackRecommendationEngine

class SnackBotSystem:
    def __init__(self):
        # Initialize core systems
        self.camera_analyzer = ZEDCameraAnalyzer()
        self.robotic_arms = RoboticArmSystem()
        self.ai_manager = AIInteractionManager()
        self.recommendation_engine = SnackRecommendationEngine()
        
        # Speech systems
        self.speech_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        # System state tracking
        self.current_visitor = None
        self.current_order = None
    
    def detect_visitor(self):
        """
        Detect and analyze approaching visitor
        """
        visitor_data = self.camera_analyzer.analyze_visitor()
        self.current_visitor = visitor_data
        
        # Generate personalized recommendation
        recommended_snack = self.recommendation_engine.get_recommendation(visitor_data)
        
        return recommended_snack
    
    def process_order(self, selected_snack):
        """
        Process visitor's snack order
        """
        # Validate order
        if not self.recommendation_engine.is_available(selected_snack):
            self.speak("Sorry, that snack is currently unavailable.")
            return False
        
        # Initiate robotic arm sequence
        order_success = self.robotic_arms.prepare_order(selected_snack)
        
        if order_success:
            self.speak(f"Your {selected_snack} is being prepared!")
            return True
        else:
            self.speak("There was an issue preparing your order.")
            return False
    
    def speak(self, message):
        """
        Text-to-speech output
        """
        self.speech_engine.say(message)
        self.speech_engine.runAndWait()
    
    def listen(self):
        """
        Speech recognition input
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
            try:
                user_input = self.recognizer.recognize_google(audio)
                return user_input
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return None
    
    def run_exhibition_mode(self):
        """
        Main exhibition interaction loop
        """
        while True:
            # Detect visitor
            recommended_snack = self.detect_visitor()
            
            # Introduce and recommend
            self.speak(f"Hello! Based on your preferences, I recommend our {recommended_snack}.")
            
            # Wait for order confirmation
            user_response = self.listen()
            
            if user_response and ('yes' in user_response.lower() or 'order' in user_response.lower()):
                order_status = self.process_order(recommended_snack)
                
                if order_status:
                    self.speak("Enjoy your snack! Is there anything else I can help you with?")
                else:
                    self.speak("I apologize for the inconvenience.")
            
            # Optional: Add exit condition or continuous loop logic

def main():
    snackbot = SnackBotSystem()
    snackbot.run_exhibition_mode()

if __name__ == "__main__":
    main()
