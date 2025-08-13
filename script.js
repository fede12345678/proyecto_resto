// Simulación de usuarios en memoria (no persistente)
let usuarios = {
    'admin': {nombre: 'Administrador', dni: '00000000', password: 'admin123', rol: 'admin'},
    'usuario1': {nombre: 'Usuario Uno', dni: '11111111', password: 'user123', rol: 'usuario'},
    'usuario2': {nombre: 'Usuario Dos', dni: '22222222', password: 'user456', rol: 'usuario'}
};


const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const mensaje = document.getElementById('mensaje');
const mensajeRegistro = document.getElementById('mensajeRegistro');
const goToRegister = document.getElementById('goToRegister');
const volverLogin = document.getElementById('volverLogin');
const loginScreen = document.querySelector('.container');
const registerScreen = document.getElementById('registerScreen');

// Mostrar pantalla de registro
goToRegister.addEventListener('click', function() {
    loginScreen.style.display = 'none';
    registerScreen.style.display = 'block';
    mensaje.textContent = '';
});

// Volver al login
volverLogin.addEventListener('click', function() {
    registerScreen.style.display = 'none';
    loginScreen.style.display = 'block';
    mensajeRegistro.textContent = '';
});

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const user = document.getElementById('loginUser').value;
    const pass = document.getElementById('loginPass').value;
    if (usuarios[user] && usuarios[user].password === pass) {
        mensaje.style.color = '#008000';
        let nombre = usuarios[user].nombre || user;
        if (nombre.includes(' ')) {
            nombre = nombre.split(' ')[0];
        }
        mensaje.textContent = `Bienvenido, ${nombre}!`;
    } else {
        mensaje.style.color = '#d8000c';
        mensaje.textContent = 'Usuario o contraseña incorrectos.';
    }
    loginForm.reset();
});

registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const dni = document.getElementById('dni').value;
    const user = document.getElementById('newUser').value;
    const pass = document.getElementById('newPass').value;
    const rol = document.getElementById('rol').value;
    if (usuarios[user]) {
        mensajeRegistro.style.color = '#d8000c';
        mensajeRegistro.textContent = 'Ese usuario ya existe. Intente con otro nombre.';
    } else {
        usuarios[user] = {nombre, dni, password: pass, rol};
        mensajeRegistro.style.color = '#008000';
        mensajeRegistro.textContent = `Usuario '${user}' creado exitosamente con rol '${rol}'.`;
        registerForm.reset();
    }
});
