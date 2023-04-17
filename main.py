
import network
import socket
import time
import urequests
from machine import Pin
import uasyncio as asyncio
import rp2
rp2.country('GR') # Set your country if you can't connect to your WiFi
led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

ssid = 'WIFI' # Put your WifI SSID
password = 'password' # Put your WiFi password

html = """<!DOCTYPE html>
 <html>
 <head> <title>Hello</title> </head>
 <body> <center><h1>OK</h1></center>
 </body>
 </html>
 """

import struct
def pack_mac(split_mac_address):
    # given a split MAC address return it packed for sending/receiving

    packed = struct.pack(b'!BBBBBB',
                         int(split_mac_address[0], 16),
                         int(split_mac_address[1], 16),
                         int(split_mac_address[2], 16),
                         int(split_mac_address[3], 16),
                         int(split_mac_address[4], 16),
                         int(split_mac_address[5], 16))
    return packed

def make_packet(mac_address):
    # given a mac address return a wol magic packet

    wol_header = b'\xff' * 6
    parts = mac_address.split(':')

    if len(parts) != 6:
        return None

    return wol_header + pack_mac(parts) * 16

wlan = network.WLAN(network.STA_IF)

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def connect_to_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print(wlan.ifconfig())
    
    
async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    request = str(request_line)
    wake_up = request.find('/wakeup')
    if wake_up == 6:
        print("wake up")
        s.sendto(make_packet('XX:XX:XX:XX:XX:XX'), ('192.168.1.255', 9)) # Put your targer computer MAC address 
        
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(html)
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")
    
    async def main():
    print('Connecting to Network...')
    connect_to_network()
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    onboard.on()
    while True:
        await asyncio.sleep(10)  # Sleep for 10 second to avoid busy loop    
        
        
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()


