#!/Users/jxjiang/miniconda3/envs/xray_py10/bin/python
import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class GPIOClient(QWidget):
    def __init__(self):
        super().__init__()
        self.server_ip = "164.54.170.53"  # Change to your board's IP
        self.port = 5005

        # Open the socket connection once
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_ip, self.port))
            print("Connected to server.")
        except Exception as e:
            print("Connection failed:", e)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label and slider for GPIO1
        self.label1 = QLabel("GPIO1: 0 (0x0)", self)
        layout.addWidget(self.label1)
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setRange(0, 0x7FFFFFFF)  # Max 2147483647
        self.slider1.valueChanged.connect(self.update_label1)
        layout.addWidget(self.slider1)

        # Textbox for GPIO1
        self.textbox1 = QLineEdit(self)
        self.textbox1.setText("0")
        self.textbox1.returnPressed.connect(self.set_slider1)
        layout.addWidget(self.textbox1)

        # Label and slider for GPIO2
        self.label2 = QLabel("GPIO2: 0 (0x0)", self)
        layout.addWidget(self.label2)
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(0, 0x7FFFFFFF)
        self.slider2.valueChanged.connect(self.update_label2)
        layout.addWidget(self.slider2)

        # Textbox for GPIO2
        self.textbox2 = QLineEdit(self)
        self.textbox2.setText("0")
        self.textbox2.returnPressed.connect(self.set_slider2)
        layout.addWidget(self.textbox2)

        # Send button
        self.send_button = QPushButton("Send GPIO Values", self)
        self.send_button.clicked.connect(self.send_values)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle("GPIO Client")
        self.show()

    def update_label1(self, value):
        """Update label when slider changes."""
        self.label1.setText(f"GPIO1: {value} (0x{value:X})")
        self.textbox1.setText(str(value))

    def update_label2(self, value):
        """Update label when slider changes."""
        self.label2.setText(f"GPIO2: {value} (0x{value:X})")
        self.textbox2.setText(str(value))

    def set_slider1(self):
        """Update slider position when textbox value changes."""
        try:
            value = int(self.textbox1.text())
            self.slider1.setValue(value)
        except ValueError:
            pass  # Ignore invalid input

    def set_slider2(self):
        """Update slider position when textbox value changes."""
        try:
            value = int(self.textbox2.text())
            self.slider2.setValue(value)
        except ValueError:
            pass  # Ignore invalid input

    def send_values(self):
        """Send GPIO values to the server when button is pressed."""
        value1 = self.slider1.value()
        value2 = self.slider2.value()
        gpio_values = f"0x{value1:08X}, 0x{value2:08X}"
        try:
            self.client.send(gpio_values.encode())
            print("Sent:", gpio_values)
        except Exception as e:
            print("Error sending data:", e)

    def closeEvent(self, event):
        """Close socket when GUI is closed."""
        print("Closing connection...")
        self.client.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GPIOClient()
    sys.exit(app.exec_())

