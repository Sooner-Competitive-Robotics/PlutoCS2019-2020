import sys, serial, json, socket
host_ip, server_port = "192.168.1.52", 9999

ser = serial.Serial(timeout = 1) # Set serial timeout to 1 second
ser.baudrate = 38400
ser.port = "/dev/ttyUSB0" # TODO: use try/catch to find the port Arduino is connected to automatically
ser.open()

dataRead = "Client start".encode()

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    # Try loop to prevent horrible issues should errors get thrown
    try:
        # Send data to UDP Server
        udp_client.sendto(dataRead, (host_ip, server_port))
        # Read data from the UDP server
        received = udp_client.recv(1024)
        # Print data received from server
        print(received.decode())
        
        # Send data read from server to Arduino
        ser.write(received)
        # Read from Arduino
        dataRead = ser.readline()
    finally:
        pass
        
''' Weird stuff; maybe delete if not necessary        
<<<<<<< HEAD
        pass
=======
        tcp_client.close()
>>>>>>> 428bad6c7cd443bb16b1b3f259b79229b9ae4161
