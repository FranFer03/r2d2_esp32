import time
import socket
import uasyncio as asyncio
from machine import Pin

# Configuración del botón
button_pin = Pin(14, Pin.IN, Pin.PULL_UP)  # Pin GPIO 14 configurado como entrada con resistencia pull-up

# Función principal
def main():
    print("Presione el botón para ver el mensaje en la terminal.")

    while True:
        if not button_pin.value():  # Detecta si el botón está presionado (estado bajo)
            print("¡Botón presionado!")
            time.sleep(0.2)  # Pequeña pausa para evitar múltiples detecciones

async def handle_request(request, conn):
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]

    print(f"Botón presionado: {path}")  # Mostrar en la terminal qué botón fue presionado

    conn.send('HTTP/1.1 204 No Content\r\n\r\n')

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
    print('Servidor disponible en: http://localhost')
    await asyncio.sleep(1)
    await server()

# Ejecutar
asyncio.run(main())
