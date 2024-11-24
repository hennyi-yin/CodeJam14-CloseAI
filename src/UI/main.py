import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtGui import QFont,QColor

class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatBot with Bot Emoji")
        self.setGeometry(100, 100, 1400, 1000)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Set Gradient Background for Main Window
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #6a11cb, stop: 1 #2575fc
                );
            }
            """
        )

        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Arial", 12))
        self.chat_area.setStyleSheet(
            """
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.8);
                border: 5px solid #ffffff;  /* Thicker border */
                border-radius: 10px;
                padding: 10px;
                color: #333333;
            }
            """
        )
        self.main_layout.addWidget(self.chat_area)

        # Input Layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        # Input Box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.setStyleSheet(
            """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #ffffff;
                border-radius: 10px;
                padding: 8px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #6a11cb;
            }
            """
        )
        self.input_layout.addWidget(self.input_box)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #6a11cb, stop: 1 #2575fc
                );
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 8px 15px;
                margin-left: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2575fc, stop: 1 #6a11cb
                );
            }
            QPushButton:pressed {
                background: #4a00e0;
            }
            """
        )
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        # Add Input Layout to Main Layout
        self.main_layout.addLayout(self.input_layout)

    def send_message(self):
        """
        Handles sending of messages from the user.
        """
        user_message = self.input_box.text().strip()
        if user_message:  # If input is not empty
            # Display user message
            self.append_message("You", user_message, QColor("#0078d7"))

            # Clear input
            self.input_box.clear()

            # Generate chatbot response
            bot_response = self.get_bot_response(user_message)
            self.append_message("🤖", bot_response, QColor("#333333"))

    def append_message(self, sender, message, color):
        """
        Appends a styled message to the chat area.
        """
        message_html = f"""
        <div style="text-align: right; margin: 10px 0;">
            <span style="font-weight: bold; color: {color.name()};">{sender}:</span>
            <span style="color: #000000;"> {message}</span>
        </div>
        """
        self.chat_area.append(message_html)

    def get_bot_response(self, message):
        """
        Replace this method with actual chatbot logic or API integration.
        """
        if "hello" in message.lower():
            return "Hi there! How can I assist you today?"
        elif "bye" in message.lower():
            return "Goodbye! Have a great day!"
        else:
            return "I'm here to help. Please ask me something!"

# Main Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use a modern style
    window = ChatBotUI()
    window.show()
    sys.exit(app.exec_())
