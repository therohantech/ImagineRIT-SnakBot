import sys
import rospy
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from std_msgs.msg import String
from robot_arm import RobotArm

class OrderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_ros()
        self.bot = RobotArm()
        
    def init_ros(self):
        if not rospy.core.is_initialized():
            rospy.init_node('order_gui', anonymous=True)
        self.order_publisher = rospy.Publisher('/robot_order', String, queue_size=10)

    def initUI(self):
        self.setWindowTitle("Imagine RIT Robot Barista")
        self.setStyleSheet("background-color: white;")

        self.title = QLabel("Order Your Drink or Snack", self)
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black;")

        self.image_label = QLabel(self)
        pixmap = QPixmap("robot_icon.png")
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)

        self.popcorn_btn = QPushButton("Popcorn", self)
        self.popcorn_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
        self.popcorn_btn.clicked.connect(lambda: self.place_order("Popcorn"))

        self.coffee_btn = QPushButton("Coffee", self)
        self.coffee_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
        self.coffee_btn.clicked.connect(lambda: self.place_order("Coffee"))

        self.status_label = QLabel("Waiting for order...", self)
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.image_label)
        layout.addWidget(self.popcorn_btn)
        layout.addWidget(self.coffee_btn)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def place_order(self, item):
        self.status_label.setText(f"{item} ordered! Preparing...")
        self.order_publisher.publish(item)
        rospy.loginfo(f"Published order: {item}")
        if item == "Coffee":
            self.bot.coffee()
        elif item == "Popcorn":
            self.bot.popcorn()
        self.status_label.setText(f"{item} is ready!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderGUI()
    window.showFullScreen()
    sys.exit(app.exec_())