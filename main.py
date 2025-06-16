# nuevo_main.py
# Reproductor MP3 con interfaz web usando ESP32, MicroPython y VS1053
import network # type: ignore
import socket
import os
import time
import uasyncio as asyncio # type: ignore
from machine import SPI, Pin # type: ignore
from sounds import VS1053
import sdcard # type: ignore
from env import *

# Configuración WiFi
SSID = NAME_WIFI
PASSWORD = PASSWORD_WIFI

# Pines para VS1053
spi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
reset = Pin(32, Pin.OUT, value=1)
xcs = Pin(33, Pin.OUT, value=1)
sdcs = Pin(25, Pin.OUT, value=1)
xdcs = Pin(26, Pin.OUT, value=1)
dreq = Pin(27, Pin.IN)

# Montar tarjeta SD
try:
    sd = sdcard.SDCard(spi, sdcs)
    os.mount(sd, '/fc')
    print("Tarjeta SD montada correctamente en /fc")
except Exception as e:
    print(f"Error montando tarjeta SD: {e}")
    print("Verifique que la tarjeta SD esté insertada y formateada en FAT32")

# Inicializar VS1053
try:
    player = VS1053(spi, reset, dreq, xdcs, xcs)
    print("VS1053 inicializado correctamente")
    # Configurar volumen inicial
    player.volume(-10, -10)  # Volumen moderado (-10dB)
    print("Volumen configurado")
except Exception as e:
    print(f"Error inicializando VS1053: {e}")
    # Reintentar con configuración diferente
    try:
        # Resetear todo
        reset.value(0)
        time.sleep_ms(100)
        reset.value(1)
        time.sleep_ms(100)
        player = VS1053(spi, reset, dreq, xdcs, xcs)
        player.volume(-10, -10)
        print("VS1053 inicializado en segundo intento")
    except Exception as e2:
        print(f"Error crítico inicializando VS1053: {e2}")
        raise

# Función de diagnóstico
async def test_system():
    """Función para probar el sistema de audio"""
    try:
        print("=== DIAGNÓSTICO DEL SISTEMA ===")
        print(f"Versión VS1053: {player.version()}")
        print(f"Modo actual: {hex(player.mode())}")
        
        # Verificar archivos de audio
        print("\n=== ARCHIVOS DE AUDIO DISPONIBLES ===")
        try:
            files = os.listdir('/fc')
            audio_files = [f for f in files if f.endswith('.mp3')]
            print(f"Archivos MP3 encontrados: {audio_files}")
            
            if not audio_files:
                print("¡ADVERTENCIA! No se encontraron archivos MP3 en la tarjeta SD")
            
            # Verificar tamaño de archivos
            for file in audio_files:
                try:
                    stat = os.stat(f'/fc/{file}')
                    print(f"  {file}: {stat[6]} bytes")
                except:
                    print(f"  {file}: Error al leer información")
                    
        except Exception as e:
            print(f"Error accediendo a la tarjeta SD: {e}")
        
        # Prueba de sonido sine
        print("\n=== PRUEBA DE SONIDO SINE ===")
        print("Ejecutando prueba de sonido sine por 2 segundos...")
        await player.sine_test(2)
        print("Prueba sine completada")
        
        print("=== DIAGNÓSTICO COMPLETADO ===\n")
        
    except Exception as e:
        print(f"Error en diagnóstico: {e}")

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
            await player.play(f)
    except Exception as e:
        print(f'Error reproduciendo sonido {filename}: {e}')

async def handle_request(request, conn):
    try:
        request_line = request.split('\r\n')[0]
        path = request_line.split(' ')[1]
        print(f"Solicitud recibida: {path}")

        if path == '/' or path == '/index.html':
            html = await web_page()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)
            return

        # Ruta de diagnóstico
        if path == '/diagnostico':
            await test_system()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nDiagnostico ejecutado - ver consola')
            return

        # Ruta de prueba sine
        if path == '/test-sine':
            print("Ejecutando prueba sine...")
            await player.sine_test(3)
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nPrueba sine completada')
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

        # Comandos de audio
        if path.startswith('/A'):
            nombre = path[1:] + ".mp3"
            print(f"Intentando reproducir: {nombre}")
            await play_sound(nombre)
            conn.send('HTTP/1.1 204 No Content\r\n\r\n')
            return

        conn.send('HTTP/1.1 404 Not Found\r\n\r\n')
        
    except Exception as e:
        print(f'Error manejando solicitud: {e}')
        try:
            conn.send('HTTP/1.1 500 Internal Server Error\r\n\r\n')
        except:
            pass

async def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    print('Servidor web esperando conexiones...')
    
    while True:
        try:
            conn, addr = s.accept()
            print('Conexión desde:', addr)
            request = conn.recv(1024).decode('utf-8')
            await handle_request(request, conn)
            conn.close()
        except Exception as e:
            print(f'Error en servidor: {e}')
            try:
                conn.close()
            except:
                pass

async def main():
    ip = await connect_to_wifi()
    print(f'Servidor disponible en: http://{ip}')
    
    # Ejecutar diagnóstico del sistema
    await test_system()
    
    await asyncio.sleep(1)
    await server()

# Ejecutar
asyncio.run(main())
