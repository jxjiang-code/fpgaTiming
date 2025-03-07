#!/Users/jxjiang/miniconda3/envs/xray_py10/bin/python
import socket

server_ip = "164.54.170.53"  # Change to your board's IP
port = 5005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))

# Send GPIO values
gpio_values = "0x0EE6B280, 0x0B2D05E0"
client.send(gpio_values.encode())

client.close()
