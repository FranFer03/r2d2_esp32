# main.py
# Programa principal para R2D2 ESP32 MicroPython
import network
import socket
import os
from servo import Servo360
from sound import beep

# Configuración WiFi (modo cliente STA)
SSID = 'WiFi-Arnet-w6ex-2.4G'  # <-- Cambia esto por el nombre de tu red WiFi
PASSWORD = 'ge5jbhgax6'  # <-- Cambia esto por tu contraseña

sta = network.WLAN(network.STA_IF)
sta.active(True)
if not sta.isconnected():
    print('Conectando a la red WiFi...')
    sta.connect(SSID, PASSWORD)
    while not sta.isconnected():
        pass
print('Conectado! IP:', sta.ifconfig()[0])

# Inicializa servo en pin 18 (ajusta según tu hardware)
servo = Servo360(pin=18)

# Servidor web básico
def web_page():
    with open('www/index.html', 'r') as f:
        return f.read()

def handle_request(request):
    if '/servo/left' in request:
        servo.left()
    elif '/servo/right' in request:
        servo.right()
    elif '/servo/stop' in request:
        servo.stop()
    elif '/sound/beep1' in request:
        beep(freq=1000, duration=200)
    elif '/sound/beep2' in request:
        beep(freq=1500, duration=300)

def send_file(conn, filepath, content_type):
    try:
        with open(filepath, 'rb') as f:
            conn.send('HTTP/1.1 200 OK\r\nContent-type: {}\r\n\r\n'.format(content_type))
            while True:
                data = f.read(512)
                if not data:
                    break
                conn.send(data)
    except Exception as e:
        conn.send('HTTP/1.1 404 NOT FOUND\r\nContent-type: text/plain\r\n\r\nArchivo no encontrado.')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print('WiFi AP:', SSID)
print('IP:', sta.ifconfig()[0])

while True:
    conn, addr = s.accept()
    try:
        request = conn.recv(1024).decode()
        print('Request:', request)
        # Obtiene la ruta solicitada
        path = '/' if 'GET /' not in request else request.split('GET ')[1].split(' ')[0]
        if path == '/' or path.startswith('/index.html'):
            send_file(conn, 'www/index.html', 'text/html')
        elif path.startswith('/image/cabeza.png'):
            send_file(conn, 'www/image/cabeza.png', 'image/png')
        elif path.startswith('/image/perfil.png'):
            send_file(conn, 'www/image/perfil.png', 'image/png')
        elif '/servo/left' in path:
            servo.left()
            conn.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
        elif '/servo/right' in path:
            servo.right()
            conn.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
        elif '/servo/stop' in path:
            servo.stop()
            conn.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
        elif '/sound/beep1' in path:
            beep(freq=1000, duration=200)
            conn.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
        elif '/sound/beep2' in path:
            beep(freq=1500, duration=300)
            conn.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
        else:
            conn.send('HTTP/1.1 404 NOT FOUND\r\nContent-type: text/plain\r\n\r\nRecurso no encontrado.')
    except Exception as e:
        print('Error:', e)
    finally:
        conn.close()
