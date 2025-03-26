from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import ollama

class VoiceListener(QThread):
    recognized_text = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        
        while True:
            with mic as source:
                try:
                    print("Listening for orders...")
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio).lower()
                    print(f"Recognized: {text}")
                    self.recognized_text.emit(text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError:
                    print("Speech recognition service unavailable")

class OrderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        rospy.init_node('order_gui', anonymous=True)
        self.order_publisher = rospy.Publisher('/robot_order', String, queue_size=10)

        # Start voice recognition thread
        self.voice_listener = VoiceListener()
        self.voice_listener.recognized_text.connect(self.process_voice_order)
        self.voice_listener.start()

    def initUI(self):
        self.setWindowTitle("Imagine RIT Robot Barista")
        self.setGeometry(0, 0, 1920, 1080)  # Fullscreen for 16:9
        self.setStyleSheet("background-color: white;")
        
        # Title Label
        self.title = QLabel("Order Your Drink or Snack", self)
        self.title.setFont(QFont("Arial", 24, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black;")
        
        # Vector Graphics - Logo or Icon
        self.image_label = QLabel(self)
        pixmap = QPixmap("robot_icon.png")  # Ensure file exists
        self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Order Status
        self.status_label = QLabel("Waiting for order...", self)
        self.status_label.setFont(QFont("Arial", 20))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: black;")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.image_label)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def process_voice_order(self, text):
        response = ollama.chat(model='mistral', messages=[
            {"role": "user", "content": text}
        ])
        ai_response = response['message']['content'].lower()
        
        if "popcorn" in ai_response:
            self.place_order("Popcorn")
        elif "coffee" in ai_response:
            self.place_order("Coffee")
        else:
            self.status_label.setText("Unrecognized order. Please try again.")

    def place_order(self, item):
        self.status_label.setText(f"{item} ordered! Preparing...")
        self.order_publisher.publish(item)
        rospy.loginfo(f"Published order: {item}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderGUI()
    window.showFullScreen()  # Ensure fullscreen mode
    sys.exit(app.exec_())
