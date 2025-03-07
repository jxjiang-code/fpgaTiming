#!/usr/local/share/pynq-venv/bin/python
import socket
from pynq.lib import AxiGPIO
from pynq import Overlay

# Load bitstream
ol = Overlay('/home/xilinx/overlay/2022.1/TimingDesign_wrapper.bit')
gpio = AxiGPIO(ol.ip_dict["axi_gpio_0"])

# Start TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5005))  # Listen on port 5005
server_socket.listen(1)

print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected to {addr}")

try:
    while True:
        data = conn.recv(1024)  # Receive up to 1024 bytes
        if not data:  # Check if client disconnected
            print("Client disconnected, waiting for new connection...")
            conn, addr = server_socket.accept()  # Accept a new connection
            print(f"Connected to {addr}")
            continue  # Go back to waiting for data

        # Convert received data from hex to int
        try:
            value1, value2 = map(lambda x: int(x, 16), data.decode().split(","))
            print(f"Received values: {hex(value1)}, {hex(value2)}")

            gpio.channel1.write(value1, 0xFFFFFFFF)
            gpio.channel2.write(value2, 0xFFFFFFFF)
            print(f"GPIO set to {value1:#010x}, {value2:#010x}")
        except ValueError:
            print("Invalid data format received.")

except KeyboardInterrupt:
    print("\nServer shutting down...")
    conn.close()
    server_socket.close()
