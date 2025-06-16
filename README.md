# 🤖 R2D2 ESP32 - Reproductor de Sonidos con Interfaz Web

![R2D2](https://img.shields.io/badge/Star%20Wars-R2D2-yellow?style=for-the-badge&logo=starwars)
![ESP32](https://img.shields.io/badge/ESP32-MicroPython-blue?style=for-the-badge&logo=espressif)
![VS1053](https://img.shields.io/badge/Audio-VS1053-green?style=for-the-badge)

Un reproductor de sonidos R2D2 controlado por ESP32 con MicroPython, usando el chip VS1053 para reproducción de audio MP3 y una interfaz web temática de Star Wars.

## 🌟 Características

- 🎵 **Reproducción de audio MP3** usando chip VS1053
- 🌐 **Interfaz web responsive** con diseño Star Wars
- 📱 **Control remoto** desde cualquier dispositivo con navegador
- 🔧 **Sistema de diagnóstico integrado** para troubleshooting
- 🎛️ **Control de volumen** programable
- 📂 **Lectura desde tarjeta SD** para archivos de audio
- ⚡ **Servidor web asíncrono** para múltiples conexiones
- 🔍 **Herramientas de debugging** incorporadas

## 📋 Requisitos de Hardware

### Componentes Principales
- **ESP32** (cualquier modelo compatible con MicroPython)
- **VS1053 Audio Codec** (módulo breakout)
- **Tarjeta microSD** (formateada en FAT32)
- **Altavoz** (8Ω, 0.5-3W recomendado)
- **Cables jumper** para conexiones

### Conexiones de Hardware

```
ESP32 Pin    →    VS1053 Pin    →    Función
─────────────────────────────────────────────
GPIO18       →    SCK           →    SPI Clock
GPIO23       →    MOSI (SI)     →    SPI Data Out
GPIO19       →    MISO (SO)     →    SPI Data In
GPIO32       →    RESET         →    Hardware Reset
GPIO33       →    XCS           →    Control Chip Select
GPIO25       →    SDCS          →    SD Card Chip Select
GPIO26       →    XDCS          →    Data Chip Select
GPIO27       →    DREQ          →    Data Request
3.3V         →    VCC           →    Alimentación
GND          →    GND           →    Tierra
```

### Diagrama de Conexión

```
                    ┌─────────────┐
                    │    ESP32    │
                    │             │
GPIO18 ────────────→│ SCK         │
GPIO23 ────────────→│ MOSI        │
GPIO19 ←────────────│ MISO        │
GPIO32 ────────────→│             │         ┌─────────────┐
GPIO33 ────────────→│             │ SPI     │   VS1053    │
GPIO25 ────────────→│             │◄───────►│   Module    │
GPIO26 ────────────→│             │         │             │
GPIO27 ←────────────│             │         │   ┌───────┐ │
                    │             │         │   │Speaker│ │
3.3V ──────────────→│ 3.3V        │         │   └───────┘ │
GND ───────────────→│ GND         │         └─────────────┘
                    └─────────────┘
```

## 💾 Requisitos de Software

### ESP32
- **MicroPython** v1.19 o superior
- **Módulos incluidos:**
  - `network` - Conectividad WiFi
  - `socket` - Servidor web
  - `uasyncio` - Programación asíncrona
  - `machine` - Control de hardware
  - `sdcard` - Manejo de tarjeta SD

### Archivos del Proyecto
```
r2d2_esp32/
├── main.py              # Programa principal
├── sounds.py            # Driver VS1053
├── env.py              # Configuración WiFi
├── www/
│   ├── index.html      # Interfaz web
│   └── image/
│       ├── cabeza.png  # Imagen R2D2 principal
│       └── perfil.png  # Imagen R2D2 esquina
├── Audios/            # Archivos MP3 (copiar a SD)
│   ├── A1.mp3
│   ├── A2.mp3
│   ├── A3.mp3
│   ├── A4.mp3
│   ├── A5.mp3
│   ├── A6.mp3
│   └── A7.mp3
└── components/
    └── micropython-vs1053/  # Driver VS1053
```

## 🚀 Instalación y Configuración

### 1. Preparar el Hardware
1. Conecta el VS1053 al ESP32 según el diagrama de conexiones
2. Inserta la tarjeta microSD en el módulo VS1053
3. Conecta el altavoz al VS1053
4. Alimenta el sistema con 3.3V

### 2. Configurar la Tarjeta SD
1. Formatea la tarjeta microSD en **FAT32**
2. Copia los archivos MP3 a la **raíz** de la tarjeta
3. Nombra los archivos exactamente como: `A1.mp3`, `A2.mp3`, `A3.mp3`, etc.

### 3. Configurar WiFi
Edita el archivo `env.py` con tus credenciales WiFi:
```python
NAME_WIFI = 'Tu_Red_WiFi'
PASSWORD_WIFI = 'Tu_Contraseña'
```

### 4. Subir Archivos al ESP32
1. Instala **Thonny** o tu IDE preferido para MicroPython
2. Sube todos los archivos Python al ESP32:
   - `main.py`
   - `sounds.py`
   - `env.py`
3. Crea la carpeta `www/` y sube:
   - `www/index.html`
   - `www/image/cabeza.png`
   - `www/image/perfil.png`

### 5. Ejecutar el Sistema
1. Conecta el ESP32 por USB y abre el monitor serie
2. Ejecuta `main.py`
3. Observa los mensajes de diagnóstico
4. Anota la dirección IP asignada

## 🎮 Uso del Sistema

### Interfaz Web
1. Abre un navegador web
2. Ve a `http://IP_DEL_ESP32`
3. Usa los botones para:
   - **Sonido A1-A7**: Reproduce sonidos R2D2
   - **DIAGNÓSTICO**: Ejecuta verificación del sistema
   - **TEST SINE**: Prueba el hardware de audio

### URLs de Control
- `http://IP_ESP32/` - Interfaz principal
- `http://IP_ESP32/A1` - Reproduce sonido A1
- `http://IP_ESP32/A2` - Reproduce sonido A2
- `http://IP_ESP32/diagnostico` - Ejecuta diagnóstico
- `http://IP_ESP32/test-sine` - Prueba de hardware

### Monitor Serie
El sistema proporciona información detallada en tiempo real:
```
=== DIAGNÓSTICO DEL SISTEMA ===
Versión VS1053: 4
Modo actual: 0x4800
Archivos MP3 encontrados: ['A1.mp3', 'A2.mp3', ...]
=== DIAGNÓSTICO COMPLETADO ===

Servidor disponible en: http://192.168.1.100
```

## 🔧 Solución de Problemas

### No se reproducen sonidos
1. **Verifica conexiones**: Revisa el diagrama de conexiones
2. **Ejecuta diagnóstico**: Usa el botón "DIAGNÓSTICO" en la interfaz web
3. **Prueba sine**: Usa "TEST SINE" para verificar hardware
4. **Revisa archivos**: Verifica que los MP3 estén en la raíz de la SD

### Error de tarjeta SD
```
Error montando tarjeta SD: [Errno 19] ENODEV
```
**Soluciones:**
- Verifica que la SD esté insertada correctamente
- Formatea la SD en FAT32
- Prueba con otra tarjeta SD

### No conecta a WiFi
**Verifica:**
- Credenciales en `env.py`
- Señal WiFi estable
- Red 2.4GHz (ESP32 no soporta 5GHz)

### VS1053 no responde
```
OSError: No VS1053 device found
```
**Soluciones:**
- Verifica alimentación 3.3V
- Revisa todas las conexiones SPI
- Verifica pin RESET conectado

## 📱 Capturas de Pantalla

### Interfaz Principal
```
┌─────────────────────────────────┐
│         R2D2 ESP32 CONTROL      │
├─────────────────────────────────┤
│  [IMG: R2D2]                   │
├─────────────────────────────────┤
│        SONIDOS R2D2            │
│  [A1] [A2] [A3] [A4]           │
│  [A5] [A6] [A7]                │
├─────────────────────────────────┤
│     DIAGNÓSTICO SISTEMA        │
│  [DIAGNÓSTICO] [TEST SINE]     │
└─────────────────────────────────┘
```

## 🛠️ Personalización

### Cambiar Volumen
```python
# En main.py, línea ~45
player.volume(-5, -5)   # Más fuerte
player.volume(-20, -20) # Más suave
```

### Agregar Más Sonidos
1. Agrega archivos `A8.mp3`, `A9.mp3`, etc. a la SD
2. Agrega botones en `www/index.html`:
```html
<button onclick="playSound('A8')">Sonido A8</button>
```

### Cambiar Red WiFi
```python
# env.py
NAME_WIFI = 'Nueva_Red'
PASSWORD_WIFI = 'Nueva_Contraseña'
```

## 📋 API de Referencia

### Funciones Principales

#### `play_sound(filename)`
Reproduce un archivo MP3 de la tarjeta SD
```python
await play_sound('A1.mp3')
```

#### `test_system()`
Ejecuta diagnóstico completo del sistema
```python
await test_system()
```

### Endpoints Web

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz principal |
| `/A1` | GET | Reproduce sonido A1 |
| `/diagnostico` | GET | Ejecuta diagnóstico |
| `/test-sine` | GET | Prueba de hardware |

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [MicroPython ESP32](https://micropython.org/download/esp32/)
- [VS1053 Datasheet](https://www.vlsi.fi/fileadmin/datasheets/vs1053.pdf)
- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)

## 👨‍💻 Autor

**Francisco** - [GitHub Profile](https://github.com/franf)

## 🙏 Agradecimientos

- **Peter Hinch** - Por el excelente driver VS1053 para MicroPython
- **Adafruit** - Por la inspiración en el diseño del driver
- **Comunidad MicroPython** - Por el soporte continuo

---

⭐ Si este proyecto te fue útil, ¡dale una estrella en GitHub!

🤖 *"Beep boop beep!"* - R2D2
