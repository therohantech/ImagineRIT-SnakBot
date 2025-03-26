from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import rospy
from std_msgs.msg import String

class OrderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        rospy.init_node('order_gui', anonymous=True)
        self.order_publisher = rospy.Publisher('/robot_order', String, queue_size=10)

    def initUI(self):
        self.setWindowTitle("Imagine RIT Robot Barista")
        self.setStyleSheet("background-color: white;")

        # Title Label
        self.title = QLabel("Order Your Drink or Snack", self)
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black;")

        # Vector Graphics - Logo or Icon
        self.image_label = QLabel(self)
        pixmap = QPixmap("robot_icon.png")  # Ensure this file exists in the working directory
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)

        # Order Buttons
        self.popcorn_btn = QPushButton("Popcorn", self)
        self.popcorn_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
        self.popcorn_btn.clicked.connect(lambda: self.place_order("Popcorn"))

        self.coffee_btn = QPushButton("Coffee", self)
        self.coffee_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
        self.coffee_btn.clicked.connect(lambda: self.place_order("Coffee"))

        # Order Status
        self.status_label = QLabel("Waiting for order...", self)
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: black;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.image_label)
        layout.addWidget(self.popcorn_btn)
        layout.addWidget(self.coffee_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Move to second screen and show fullscreen
        self.move_to_second_screen()

    def move_to_second_screen(self):
        app = QApplication.instance()
        screens = app.screens()
        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            self.setGeometry(geometry)
            self.showFullScreen()
        else:
            self.showFullScreen()  # Defaults to primary screen if no second screen is detected

    def place_order(self, item):
        self.status_label.setText(f"{item} ordered! Preparing...")
        self.order_publisher.publish(item)
        rospy.loginfo(f"Published order: {item}")
        # This sends the order to the ROS topic '/robot_order'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderGUI()
    sys.exit(app.exec_())
