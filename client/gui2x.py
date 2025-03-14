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

        # Create labels, sliders, and textboxes for each GPIO channel
        self.gpio_labels = []
        self.gpio_sliders = []
        self.gpio_textboxes = []

        for i in range(4):  # Four channels: GPIO1-1, GPIO1-2, GPIO2-1, GPIO2-2
            label = QLabel(f"GPIO{i+1}: 0 (0x0)", self)
            layout.addWidget(label)
            self.gpio_labels.append(label)
            
            slider = QSlider(Qt.Horizontal, self)
            slider.setRange(0, 0x7FFFFFFF)  # Max 2147483647
            slider.valueChanged.connect(lambda value, idx=i: self.update_label(value, idx))
            layout.addWidget(slider)
            self.gpio_sliders.append(slider)

            textbox = QLineEdit(self)
            textbox.setText("0")
            textbox.returnPressed.connect(lambda idx=i: self.set_slider(idx))
            layout.addWidget(textbox)
            self.gpio_textboxes.append(textbox)

        # Send button
        self.send_button = QPushButton("Send GPIO Values", self)
        self.send_button.clicked.connect(self.send_values)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle("GPIO Client")
        self.show()

    def update_label(self, value, index):
        """Update label when slider changes."""
        self.gpio_labels[index].setText(f"GPIO{index+1}: {value} (0x{value:X})")
        self.gpio_textboxes[index].setText(str(value))

    def set_slider(self, index):
        """Update slider position when textbox value changes."""
        try:
            value = int(self.gpio_textboxes[index].text())
            self.gpio_sliders[index].setValue(value)
        except ValueError:
            pass  # Ignore invalid input

    def send_values(self):
        """Send GPIO values to the server when button is pressed."""
        values = [self.gpio_sliders[i].value() for i in range(4)]
        gpio_values = ", ".join(f"0x{val:08X}" for val in values)
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

