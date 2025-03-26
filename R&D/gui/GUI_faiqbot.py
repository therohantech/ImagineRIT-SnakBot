# Character AI Config
token = "ae52b470beb8be2cc0e5b34dd6a7332157b391ab"
character_id = "FS54dIDelfofnZPprHP5hSyMcLwogfH2uo8UTEHeD0E"



from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import asyncio
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError



detected_users = set()  # Track detected users

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

        # Start chatbot session
        asyncio.run(self.init_chatbot())

        self.current_user = None  # Track the current ordering user
        self.user_orders = {}  # Track number of orders per user

    async def init_chatbot(self):
        self.client = await get_client(token=token)
        self.chat, greeting_message = await self.client.chat.create_chat(character_id)
        self.chat_display.append(f"FaiqBot: {greeting_message.get_primary_candidate().text}")

    def initUI(self):
        self.setWindowTitle("Imagine RIT Robot Barista")
        self.setGeometry(0, 0, 1920, 1080)  # Fullscreen for 16:9
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #222831, stop:1 #393E46);")
        
        # Title Label
        self.title = QLabel("Order Your Drink or Snack", self)
        self.title.setFont(QFont("Arial", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #EEEEEE; padding: 20px;")
        
        # Vector Graphics - Logo or Icon
        self.image_label = QLabel(self)
        pixmap = QPixmap("robot_icon.png")  # Ensure file exists
        self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Order Status
        self.status_label = QLabel("Waiting for order...", self)
        self.status_label.setFont(QFont("Arial", 22))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00ADB5; padding: 15px;")
        
        # Chat Display
        self.chat_display = QTextEdit(self)
        self.chat_display.setFont(QFont("Arial", 18))
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background: rgba(255, 255, 255, 0.1); color: #EEEEEE; border-radius: 15px; padding: 10px;")
        
        # Buttons
        self.popcorn_button = QPushButton("🍿 Order Popcorn", self)
        self.popcorn_button.setFont(QFont("Arial", 20))
        self.popcorn_button.setStyleSheet("background: #00ADB5; color: white; border-radius: 15px; padding: 15px;")
        self.popcorn_button.clicked.connect(lambda: self.place_order("Popcorn"))
        
        self.coffee_button = QPushButton("☕ Order Coffee", self)
        self.coffee_button.setFont(QFont("Arial", 20))
        self.coffee_button.setStyleSheet("background: #00ADB5; color: white; border-radius: 15px; padding: 15px;")
        self.coffee_button.clicked.connect(lambda: self.place_order("Coffee"))
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.image_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.popcorn_button)
        layout.addWidget(self.coffee_button)
        
        self.setLayout(layout)
    
    def detect_user(self, user_id):
        """Detects a user and ensures they can't spam orders."""
        if user_id not in detected_users:
            detected_users.add(user_id)
            self.current_user = user_id
            self.user_orders[user_id] = 0
            return True
        return False
    
    def process_voice_order(self, text):
        if self.current_user is None:
            user_id = "user_123"  # Placeholder (replace with real detection)
            if not self.detect_user(user_id):
                self.status_label.setText("Order already placed. Please wait...")
                return
        
        asyncio.run(self.send_chat_message(text))
    
    async def send_chat_message(self, text):
        self.chat_display.append(f"You: {text}")
        
        answer = await self.client.chat.send_message(character_id, self.chat.chat_id, text, streaming=False)
        response_text = answer.get_primary_candidate().text
        
        self.chat_display.append(f"FaiqBot: {response_text}")
    
        if "popcorn" in response_text.lower():
            self.place_order("Popcorn")
        elif "coffee" in response_text.lower():
            self.place_order("Coffee")
    
    def place_order(self, item):
        if self.current_user is None:
            return
        
        if self.user_orders[self.current_user] >= 2:
            self.status_label.setText("Maximum of 2 items per user. Please wait...")
            return
        
        self.user_orders[self.current_user] += 1
        self.status_label.setText(f"{item} ordered! Preparing...")
        self.order_publisher.publish(item)
        rospy.loginfo(f"Published order: {item}")
        
        if self.user_orders[self.current_user] == 2:
            self.status_label.setText("Order limit reached. Processing...")
            detected_users.discard(self.current_user)  # Reset user after ordering
            self.current_user = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderGUI()
    window.showFullScreen()  # Ensure fullscreen mode
    sys.exit(app.exec_())
