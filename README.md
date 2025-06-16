# Documentación del Proyecto R2D2 ESP32 MicroPython

## Requisitos
- ESP32 con MicroPython
- Servomotor 360° (cabeza)
- Parlante conectado al pin 25
- (Opcional) Archivos de sonido WAV simples

## Archivos
- main.py: Código principal, WiFi, servidor web, integración de servo y sonido
- servo.py: Control del servomotor 360°
- sound.py: Reproducción de sonidos simples (beep)
- www/index.html: Página web de control

## Uso
1. Copia todos los archivos al ESP32 (usa Thonny, ampy, rshell, etc).
2. Reinicia el ESP32.
3. Conéctate a la red WiFi "R2D2-ESP32" (clave: micropython).
4. Abre en tu navegador: http://192.168.4.1
5. Usa los botones para controlar la cabeza y reproducir sonidos.

## Notas
- Para sonidos complejos, se requiere un DAC o librerías avanzadas.
- Ajusta los pines según tu hardware.
- Puedes agregar más sonidos y botones editando `sound.py` y `index.html`.
