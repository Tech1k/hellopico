from machine import Pin, I2C, Timer
import time
import utime
import usocket as socket
import network
import bme280
from secrets import secrets
import gc

gc.collect()

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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(100)

print('listening on', addr)


# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        #cl.settimeout(3.0)
        request = cl.recv(1024)
        request = str(request)
        cl.settimeout(None)

        print(request)


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

        # Altitude
        altitude = bme.values[1]
        altitude = altitude[:-3]
        altitude = "{:.2f}".format(44330 * (1 - (float(altitude)/1013.25)**(1/5.255) ) * 3.281) + 'ft'


        # Pressure
        pressure = str(bme.values[1])


        # Humidity
        humidity = str(bme.values[2])


        # Memory Usage
        used_mem = gc.mem_alloc()
        free_mem = gc.mem_free()
        ram_usage = used_mem / 264000 * 100
        free_mem_kb = free_mem // 1024
        used_mem_kb = used_mem // 1024
        memory_usage = str('{:.0f}'.format(ram_usage)) + "% (" + str('{:.0f}'.format(used_mem_kb)) + " KB)"


        # Uptime
        timeDiff = time.time()-timeInit
        (minutes, seconds) = divmod(timeDiff, 60)
        (hours, minutes) = divmod(minutes, 60)
        (days,hours) = divmod(hours, 24)
        uptime = str(days)+" days, "+f"{hours} hours, {minutes} minutes, {seconds} seconds"
        response = str(uptime)

        # Temperature
        temp = str(bme.values[0])
        temp = temp[:-1]
        fahrenheit = "{:.2f}".format((float(temp) * 1.8) + 32)
        temperature = str(fahrenheit) + "°F"


        # Temperature Celsius
        temp = str(bme.values[0])
        temp = temp[:-1]
        temperature_celsius = str(temp) + "°C"


        def web_page():
            html = """
        <html lang='en'>
            <head>
                <meta charset='UTF-8'/>
                <meta name='viewport' content='width=device-width, initial-scale=1'/>
                <link rel='stylesheet' href='https://pro.fontawesome.com/releases/v5.10.0/css/all.css' crossorigin='anonymous'/>
                <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet' crossorigin='anonymous'>
                <link href='https://fonts.googleapis.com/css2?family=Cabin+Condensed:wght@600;700&display=swap' rel='stylesheet'/>
                <title>HelloPico - Hosted on a Pico W</title>
                <meta name='description' content='HelloPico is a website that is hosted on a Pico W to demonstrate what you can do with it.'/>
                <link rel='shortcut icon' href='/favicon.png'/>
                <meta name='keywords' content='pico, pico w, development, coding, programming'/>
                <meta name='author' content='Kristian Kramer'/>
                <meta name='theme-color' content='#2686e6'/>
                <link rel='canonical' href='https://hellopico.net'/>
                <meta name='robots' content='index, follow'/>
                <link rel='stylesheet' href='/styles.css'/>
                <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js' crossorigin='anonymous'></script> 

                <meta name='twitter:card' content='summary_large_image' />
                <meta name='twitter:title' content='HelloPico' />
                <meta name='twitter:description' content='HelloPico is a website that is hosted on a Pico W to demonstrate what you can do with it.' />
                <meta name='twitter:image' content='https://hellopico.net/favicon.png' />
                <meta name='twitter:site' content='@kristianjkramer' />
                <meta name='twitter:creator' content='@kristianjkramer' />

                <meta property='og:image' content='https://hellopico.net/favicon.png'/>
                <meta property='og:image:width' content='512'/>
                <meta property='og:image:height' content='512'/>
                <meta property='og:description' content='HelloPico is a website that is hosted on a Pico W to demonstrate what you can do with it.'/>
                <meta property='og:title' content='HelloPico'/>
                <meta property='og:site_name' content='HelloPico'/>
                <meta property='og:url' content='https://hellopico.net/'/>
            </head>
            <body>
                <div class='HMP'>
                    <div class='HMP-title m-0 fw-bold'>HelloPico</div>
                    <div class='program m-0'>Hosted on a Raspberry Pi Pico W</div>
                    <br/> <br/> 
                    <blockquote class='box'>
                        <p class='lead'> This website is hosted on a Pico W to demonstrate what you can do with it!<br/> Checkout the <a href='https://github.com/Tech1k/hellopico' target='_blank'>GitHub repo</a> for the code and feel free to contribute! </p>
                    </blockquote>
                    <section class='stats_section'>
                        <div class='container'>
                            <div class='row'>
                                <center>
                                    <div class='col-lg-8 col-lg-offset-2'>
                                        <h2 class='section-heading'><i class='fas fa-analytics'></i> Statistics</h2>
                                        <div class='grid_container'>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='fas fa-hourglass stat_icon'></i> Uptime</div>
                                                    <div class='stat_content' id='uptime'>""" + uptime + """</div>
                                                </div>
                                            </div>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='fas fa-memory stat_icon'></i> Memory Usage</div>
                                                    <div class='stat_content' id='memory_usage'>""" + memory_usage + """</div>
                                                </div>
                                            </div>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='fas fa-users stat_icon'></i> Visitors</div>
                                                    <div class='stat_content' id='visitors'>""" + str(visitors) + """</div>
                                                </div>
                                            </div>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='far fa-thermometer-half stat_icon'></i> Temperature (±2°F)</div>
                                                    <div class='stat_content' id='temperature'>""" + temperature + """</div>
                                                    <div class='stat_content' style='font-size: 16px; margin-top: -10px;' id='temperature_celsius'>""" + temperature_celsius + """</div>
                                                </div>
                                            </div>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='fas fa-mountains stat_icon'></i> Altitude (±1 hPa or 3.3 ft)</div>
                                                    <div class='stat_content' id='altitude'>""" + altitude + """</div>
                                                    <div class='stat_content' style='font-size: 16px; margin-top: -10px;' id='pressure'>""" + pressure + """</div>
                                                </div>
                                            </div>
                                            <div class='stat_card'>
                                                <div class='stat_container'>
                                                    <div class='stat_title'><i class='fas fa-humidity stat_icon'></i> Humidity (±3%)</div>
                                                    <div class='stat_content' id='humidity'>""" + humidity + """</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </center>
                            </div>
                        </div>
                    </section>
                </div>
                <br/> 
                <center>
                    <p class='is-size-6' style='font-size: 24px; font-weight: 700; margin-bottom: 5px;'><i class='icon far fa-images'></i> Photos</p>
                    <div id='carouselExampleCaptions' class='carousel slide' data-bs-ride='carousel' style='max-width: 512px; border-radius: 0.5rem; overflow: hidden; box-shadow: 0 0.2rem 0.5rem rgba(0, 0, 0, 0.05);'>
                        <img src='https://raw.githubusercontent.com/Tech1k/hellopico/master/pico-webserver.jpg' class='d-block w-100' alt='Pico W Webserver' style='max-width: 512px; height: 280px;'> 
                        <div class='carousel-caption d-none d-md-block'>
                            <p style='font-size: 16px; color: white;'>The Pico W that is hosting this website, taken on 2/16/2023.</p>
                        </div>
                    </div>
                    <br/> 
                    <p class='is-size-6' style='font-size: 24px; font-weight: 700; margin-bottom: 5px;'><i class='icon far fa-newspaper'></i> Updates</p>
                    <div style='height: 256px; max-width: 512px; overflow-x: hidden; overflow-y: auto;' class='updates_container'>
                        <div class='updates_content' align='left'> <strong>2/16/2023 - </strong> HelloPico has launched, this is a little project of mine which is a fork of my <a href='https://helloesp.com'>HelloESP project</a> to show what can be done with a Raspberry Pi Pico W!</div>
                    </div>
                </center>
                <br/>
                <footer id='contact' class='contact-section'>
                    <div class='contact-section-header'>
                        <p class='h5'>Made with <i class='fas fa-heart'></i> by <a href='https://kk.dev' target='_blank' class='author_link'>Kristian</a></p>
                    </div>
                    <div class='contact-links border-top'> <a href='https://kk.dev' target='_blank' class='btn contact-details'><i class='fas fa-globe'></i> kk.dev</a> <a href='https://kk.dev/donate' target='_blank' class='btn contact-details'><i class='fas fa-heart'></i> Donate</a> <a href='https://github.com/Tech1k' target='_blank' class='btn contact-details'><i class='fab fa-github'></i> GitHub</a> <a href='https://twitter.com/KristianJKramer' target='_blank' class='btn contact-details'><i class='fab fa-twitter'></i> Twitter</a> <a href='https://github.com/Tech1k/hellopico' class='btn contact-details'><i class='fas fa-code'></i> Contribute</a> </div>
                </footer>
            </body>
        </html>
        """
            return html

        if request == '/index.html':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/html\n')
            cl.send('Connection: close\n\n')
            response = web_page()
            cl.sendall(response)
            cl.close()
        elif request == '/styles.css':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/css\n')
            cl.send('Connection: close\n\n')
            response = get_request_file('styles.css')
            cl.sendall(response)
            cl.close()
        elif request == '/favicon.png':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: image/png\n')
            cl.send('Connection: close\n\n')
            response = get_request_file('favicon.png')
            cl.sendall(response)
            cl.close()
        elif request == '/favicon.ico':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: image/x-icon\n')
            cl.send('Connection: close\n\n')
            response = get_request_file('favicon.ico')
            cl.sendall(response)
            cl.close()
        elif request == '/':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/html\n')
            cl.send('Connection: close\n\n')
            response = web_page()
            cl.sendall(response)
            cl.close()
        elif request == '':
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/html\n')
            cl.send('Connection: close\n\n')
            response = web_page()
            cl.sendall(response)
            cl.close()
        # If file not found, throw a 404 exception
        else:
            cl.send('HHTTP/1.1 404 Not Found')
            cl.send('Content-Type: text/html\n')
            response = "404 Not Found"
            cl.sendall(response)

    except OSError as e:
        cl.close()
        print('connection closed')
