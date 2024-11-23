import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

# Placeholder for the RAG logic
def query_rag_system(user_query):
    # Replace with the actual RAG logic
    return f"Fancy simulated response for query: {user_query}"

class FancyRAGApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RAG Application - Fancy Dracula Theme")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("icon.png"))  # Add a fancy icon here

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("🚗 Fancy RAG Car Query System")
        title_label.setFont(QFont("Roboto", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input Section
        input_layout = QVBoxLayout()
        self.input_label = QLabel("Enter your query:")
        self.input_label.setFont(QFont("Roboto", 12))
        input_layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your query here...")
        input_layout.addWidget(self.input_field)

        layout.addLayout(input_layout)

        # Output Section
        output_layout = QVBoxLayout()
        self.output_label = QLabel("Response:")
        self.output_label.setFont(QFont("Roboto", 12))
        output_layout.addWidget(self.output_label)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        output_layout.addWidget(self.output_field)

        layout.addLayout(output_layout)

        # Button Section
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.handle_query)
        self.submit_button.setFixedHeight(40)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Footer
        footer_label = QLabel("Made with ❤️ using PyQt5 and Dracula Theme")
        footer_label.setFont(QFont("Roboto", 10))
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)

        # Apply Layout
        central_widget.setLayout(layout)

    def handle_query(self):
        user_query = self.input_field.text()
        if user_query.strip():
            response = query_rag_system(user_query)
            self.output_field.setText(response)
        else:
            self.output_field.setText("Please enter a query.")

def main():
    app = QApplication(sys.argv)

    # Load the Fancy Dracula Theme
    with open("src\\UI\\fancy_dracula.qss", "r") as stylesheet:
        app.setStyleSheet(stylesheet.read())

    window = FancyRAGApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
