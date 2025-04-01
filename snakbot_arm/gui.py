#test code, does not work


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from arm_code import coffee, popcorn

class OrderGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create an instance of the external functions class
        self.robot = RobotArm()
        
        # Set up the GUI
        self.setWindowTitle("Order Robot Control")
        self.setGeometry(100, 100, 300, 200)
        
        # Create a layout
        layout = QVBoxLayout()
        
        # Add a label
        self.label = QLabel("Press a button to control the robot")
        layout.addWidget(self.label)
        
        # Create buttons
        self.button1 = QPushButton("Move Forward")
        self.button1.clicked.connect(self.on_forward_clicked)
        layout.addWidget(self.button1)
        
        self.button2 = QPushButton("Move Backward")
        self.button2.clicked.connect(self.on_backward_clicked)
        layout.addWidget(self.button2)
        
        # Set the layout
        self.setLayout(layout)
        
    def on_forward_clicked(self):
        self.label.setText("Moving Forward...")
        # Call the function from the other Python file
        coffee()
        self.label.setText("Moved Forward")
        
    def on_backward_clicked(self):
        self.label.setText("Moving Backward...")
        # Call the function from the other Python file
        popcorn()
        self.label.setText("Moved Backward")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderGUI()
    window.show()
    sys.exit(app.exec_())




# class OrderGUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.bot = RobotArm()
#         # Initialize ROS node and publisher
        
#     def initUI(self):
#         self.setWindowTitle("Imagine RIT Robot Barista")
#         self.setStyleSheet("background-color: white;")
        
#         self.title = QLabel("Order Your Drink or Snack", self)
#         self.title.setFont(QFont("Arial", 16, QFont.Bold))
#         self.title.setAlignment(Qt.AlignCenter)
#         self.title.setStyleSheet("color: black;")
        
#         self.image_label = QLabel(self)
#         pixmap = QPixmap("robot_icon.png")
#         self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
#         self.image_label.setAlignment(Qt.AlignCenter)
        
#         self.popcorn_btn = QPushButton("Popcorn", self)
#         self.popcorn_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
#         self.popcorn_btn.clicked.connect(lambda: self.place_order("Popcorn"))
        
#         self.coffee_btn = QPushButton("Coffee", self)
#         self.coffee_btn.setStyleSheet("background-color: orange; color: black; font-size: 18px; padding: 10px;")
#         self.coffee_btn.clicked.connect(lambda: self.place_order("Coffee"))
        
#         self.status_label = QLabel("Waiting for order...", self)
#         self.status_label.setFont(QFont("Arial", 14))
#         self.status_label.setAlignment(Qt.AlignCenter)
#         self.status_label.setStyleSheet("color: black;")
        
#         layout = QVBoxLayout()
#         layout.addWidget(self.title)
#         layout.addWidget(self.image_label)
#         layout.addWidget(self.popcorn_btn)
#         layout.addWidget(self.coffee_btn)
#         layout.addWidget(self.status_label)
#         self.setLayout(layout)
        
#     def place_order(self, item):
#         self.status_label.setText(f"{item} ordered! Preparing...")
#         # Publish the order to ROS
#         self.order_publisher.publish(item)
#         rospy.loginfo(f"Published order: {item}")
        
#         # Execute the appropriate robot function
#         if item == "Coffee":
#             self.bot.coffee()
#         elif item == "Popcorn":
#             self.bot.popcorn()
            
#         self.status_label.setText(f"{item} is ready!")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = OrderGUI()
#     window.showFullScreen()
#     sys.exit(app.exec_())