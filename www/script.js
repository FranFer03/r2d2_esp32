// R2D2 ESP32 Control JavaScript - Optimizado para rendimiento

// --- Configuración Inicial ---
const r2d2Container = document.getElementById('r2d2-container');

// --- Fondo de Estrellas Optimizado ---
const starfield = document.querySelector('.starfield');
const numStars = 50; // Reducido de 100 a 50 para mejor rendimiento

function createStars() {
    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.classList.add('s' + (Math.floor(Math.random() * 3) + 1));
        
        star.style.top = Math.random() * 100 + '%';
        star.style.left = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 5 + 's'; 
        starfield.appendChild(star);
    }
}

// --- Funciones de Control Optimizadas ---
function moveHead(direction) {
    console.log(`Comando cabeza: /servo/${direction}`);
    fetch('/servo/' + direction).catch(err => console.error('Error ESP32:', err));
    
    r2d2Container.classList.add('shake');
    setTimeout(() => r2d2Container.classList.remove('shake'), 200);
}

function playSound(soundId) {
    console.log(`Reproduciendo sonido: ${soundId}`);
    fetch(`/${soundId}`)
        .then(response => {
            if (response.ok) {
                console.log(`Sonido ${soundId} enviado correctamente`);
            } else {
                console.error(`Error enviando sonido ${soundId}:`, response.status);
            }
        })
        .catch(err => console.error('Error de conexión:', err));
    
    r2d2Container.classList.add('shake');
    setTimeout(() => r2d2Container.classList.remove('shake'), 500);
}

function playRandomSound() {
    console.log('Reproduciendo sonido aleatorio...');
    fetch('/random_sound')
        .then(response => {
            if (response.ok) {
                console.log('Sonido aleatorio enviado correctamente');
            } else {
                console.error('Error enviando sonido aleatorio:', response.status);
            }
        })
        .catch(err => console.error('Error de conexión:', err));

    r2d2Container.classList.add('shake');
    setTimeout(() => r2d2Container.classList.remove('shake'), 500);
}

function runDiagnostic() {
    console.log('Ejecutando diagnóstico del sistema...');
    fetch('/diagnostico')
        .then(response => {
            if (response.ok) {
                alert('Diagnóstico ejecutado. Revisa la consola del ESP32 para ver los resultados.');
            } else {
                alert('Error ejecutando diagnóstico. Código: ' + response.status);
            }
        })
        .catch(err => {
            console.error('Error ejecutando diagnóstico:', err);
            alert('Error de conexión durante el diagnóstico.');
        });
}

function testSine() {
    console.log('Ejecutando prueba de sonido sine...');
    fetch('/test-sine')
        .then(response => {
            if (response.ok) {
                alert('Prueba sine ejecutada. Deberías escuchar un tono durante 3 segundos.');
            } else {
                alert('Error ejecutando prueba sine. Código: ' + response.status);
            }
        })
        .catch(err => {
            console.error('Error ejecutando prueba sine:', err);
            alert('Error de conexión durante la prueba sine.');
        });
}

// --- Inicialización Optimizada ---
document.addEventListener('DOMContentLoaded', () => {
    createStars(); 

    // Animación de "encendido" de R2D2
    setTimeout(() => {
        r2d2Container.classList.add('shake');
        setTimeout(() => r2d2Container.classList.remove('shake'), 500);
    }, 200);
});
