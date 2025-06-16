import socket
import uasyncio as asyncio

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
