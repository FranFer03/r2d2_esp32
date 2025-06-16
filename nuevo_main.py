# nuevo_main.py
# Reproductor MP3 con interfaz web usando ESP32, MicroPython y VS1053
import network
import socket
import os
import uasyncio as asyncio
from machine import SPI, Pin
from servo import Servo360
from sounds import VS1053
import sdcard

# Configuración WiFi
SSID = 'WiFi-Arnet-w6ex-2.4G'
PASSWORD = 'ge5jbhgax6'

# Pines para VS1053
spi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
reset = Pin(32, Pin.OUT, value=1)
xcs = Pin(33, Pin.OUT, value=1)
sdcs = Pin(25, Pin.OUT, value=1)
xdcs = Pin(26, Pin.OUT, value=1)
dreq = Pin(27, Pin.IN)

# Montar tarjeta SD
sd = sdcard.SDCard(spi, sdcs)
os.mount(sd, '/fc')

# Inicializar VS1053
player = VS1053(spi, reset, dreq, xdcs, xcs, sdcs, '/fc')

# Inicializar servo
servo = Servo360(pin=15)

async def connect_to_wifi():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print('Conectando a la red WiFi...')
        sta.connect(SSID, PASSWORD)
        while not sta.isconnected():
            await asyncio.sleep(1)
    print('Conectado! IP:', sta.ifconfig()[0])
    return sta.ifconfig()[0]

async def web_page():
    try:
        with open('www/index.html', 'r') as f:
            return f.read()
    except:
        return "<html><body><h1>Error: archivo index.html no encontrado.</h1></body></html>"

async def send_file(conn, filepath, content_type):
    try:
        with open(filepath, 'rb') as f:
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n'.format(content_type))
            while True:
                data = f.read(512)
                if not data:
                    break
                conn.send(data)
    except Exception as e:
        print('Error enviando archivo:', e)

async def play_sound(filename):
    filepath = '/fc/' + filename
    try:
        os.stat(filepath)
        print(f'Reproduciendo: {filename}')
        with open(filepath, 'rb') as f:
            player.play_file(f)
            await asyncio.sleep(0.1)
    except Exception as e:
        print('Error reproduciendo sonido:', e)

async def handle_request(request, conn):
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]

    if path == '/' or path == '/index.html':
        html = await web_page()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)
        return

    # Archivos estáticos
    if path.startswith('/image/'):
        filepath = 'www' + path
        try:
            os.stat(filepath)
            content_type = 'image/png' if filepath.endswith('.png') else 'application/octet-stream'
            await send_file(conn, filepath, content_type)
        except OSError:
            conn.send('HTTP/1.1 404 Not Found\r\n\r\n')
        return

    # Comandos
    if path.startswith('/A'):
        nombre = path[1:] + ".mp3"
        await play_sound(nombre)
        conn.send('HTTP/1.1 204 No Content\r\n\r\n')
        return

    if path.startswith('/servo/left'):
        servo.left()
        conn.send('HTTP/1.1 204 No Content\r\n\r\n')
        return

    if path.startswith('/servo/right'):
        servo.right()
        conn.send('HTTP/1.1 204 No Content\r\n\r\n')
        return

    if path.startswith('/servo/stop'):
        servo.stop()
        conn.send('HTTP/1.1 204 No Content\r\n\r\n')
        return

    conn.send('HTTP/1.1 404 Not Found\r\n\r\n')

async def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Servidor web esperando conexiones...')
    while True:
        conn, addr = s.accept()
        print('Conexión desde:', addr)
        request = conn.recv(1024).decode('utf-8')
        await handle_request(request, conn)
        conn.close()

async def main():
    ip = await connect_to_wifi()
    print(f'Servidor disponible en: http://{ip}')
    await asyncio.sleep(1)
    await server()

# Ejecutar
asyncio.run(main())
