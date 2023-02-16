from machine import Pin, I2C, Timer
import time
import utime
import socket
import network
import bme280
from secrets import secrets
import gc

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

timeInit = time.time()

ssid = secrets['ssid']
pw = secrets['pw']

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pw)

# Gets file
def get_request_file(request_file_name):
    with open(request_file_name, 'rb') as file:
        file_requested = file.read()
    return file_requested

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open a socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        request = cl.recv(1024)
        request = str(request)


        try:
            # Split request down to the file name
            request = request.split()[1]

        except IndexError:
            pass
        # Add 1 to visitors.txt
        with open('visitors.txt') as f:
            visitors = int(f.read())

        with open('visitors.txt', 'w') as f:
            f.write(str(visitors + 1))
            
        print(request)

        if '.html' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
        elif '.css' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n'
        elif '.js' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\n\r\n'
        elif '.svg' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: image/svg+xml\r\n\r\n'
        elif '.png' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
        elif '.jpg' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\n\r\n'
        elif '.ico' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\n\r\n'
        elif request == '/altitude':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            pressure_int = bme.values[1]
            pressure_int = pressure_int[:-3]
            response = "{:.2f}".format(44330 * (1 - (float(pressure_int)/1013.25)**(1/5.255) ) * 3.281) + 'ft'
            cl.send(file_header)
            cl.send(response)
        elif request == '/pressure':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = str(bme.values[1])
            cl.send(file_header)
            cl.send(response)
        elif request == '/temperature':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            temp = str(bme.values[0])
            temp = temp[:-1]
            fahrenheit = (float(temp) * 1.8) + 32
            response = str(fahrenheit) + "°F"
            cl.send(file_header)
            cl.send(response)
        elif request == '/temperature_celsius':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            temp = str(bme.values[0])
            temp = temp[:-1]
            response = str(temp) + "°C"
            cl.send(file_header)
            cl.send(response)
        elif request == '/humidity':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = str(bme.values[2])
            cl.send(file_header)
            cl.send(response)
        elif request == '/visitors':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = str(visitors)
            cl.send(file_header)
            cl.send(response)
        elif request == '/memory_usage':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            used_mem = gc.mem_alloc()
            free_mem = gc.mem_free()
            ram_usage = used_mem / 264000 * 100
            free_mem_kb = free_mem // 1024
            used_mem_kb = used_mem // 1024
            response = str('{:.0f}'.format(ram_usage)) + "% (" + str('{:.0f}'.format(used_mem_kb)) + " KB)"
            cl.send(file_header)
            cl.send(response)
        elif request == '/uptime':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            timeDiff = time.time()-timeInit
            (minutes, seconds) = divmod(timeDiff, 60)
            (hours, minutes) = divmod(minutes, 60)
            (days,hours) = divmod(hours, 24)
            uptime = str(days)+" days, "+f"{hours} hours, {minutes} minutes, {seconds} seconds"
            response = str(uptime)
            cl.send(file_header)
            cl.send(response)
        elif request == '/':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = get_request_file('index.html')
            cl.sendall(response)
        elif request == '':
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = get_request_file('index.html')
            cl.sendall(response)
        # If file not found, throw a 404 exception
        else:
            file_header = 'HTTP/1.1 404 Not Found\r\nContent-type: text/html\r\n\r\n'
            response = "404 Not Found"
            cl.send(file_header)
            cl.sendall(response)

        response = get_request_file(request)
        print('file header = ', file_header)


        cl.send(file_header)
        cl.sendall(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
