//-- Url 

//import { handleResponse } from '../common/common.js';

const urlAPI = "http://127.0.0.1:5001";

//-- funcionalidades del front Login-register

document.getElementById("btn_registrarse").addEventListener("click",register);
document.getElementById("btn_iniciar-sesion").addEventListener("click", iniciarSesion);
window.addEventListener("resize", anchoPage);

//Declarando variables
var formulario_login = document.querySelector(".formulario_login");
var formulario_register = document.querySelector(".formulario_register");
var contenedor_login_register = document.querySelector(".contenedor_login-register");
var caja_trasera_login = document.querySelector(".caja_trasera-login");
var caja_trasera_register = document.querySelector(".caja_trasera-register");

function updateStyles(element, styles) {
    if (!element) return;
    Object.assign(element.style, styles);
}

function anchoPage() {
    if (window.innerWidth > 850) {
        updateStyles(caja_trasera_register, { display: "block", opacity: "" });
        updateStyles(caja_trasera_login, { display: "block", opacity: "" });
    } else {
        updateStyles(caja_trasera_register, { display: "block", opacity: "1" });
        updateStyles(caja_trasera_login, { display: "none" });
        updateStyles(formulario_login, { display: "block" });
        updateStyles(contenedor_login_register, { left: "0px" });
        updateStyles(formulario_register, { display: "none" });
    }
}

function iniciarSesion() {
    if (window.innerWidth > 850) {
        updateStyles(formulario_login, { display: "block" });
        updateStyles(contenedor_login_register, { left: "10px" });
        updateStyles(formulario_register, { display: "none" });
        updateStyles(caja_trasera_register, { opacity: "1" });
        updateStyles(caja_trasera_login, { opacity: "0" });
    } else {
        updateStyles(formulario_login, { display: "block" });
        updateStyles(contenedor_login_register, { left: "0px" });
        updateStyles(formulario_register, { display: "none" });
        updateStyles(caja_trasera_register, { display: "block" });
        updateStyles(caja_trasera_login, { display: "none" });
    }

    document.addEventListener("DOMContentLoaded", () => {
        // Limpiar cualquier dato de sesión previo
        localStorage.removeItem("token");
        localStorage.removeItem("email");
        localStorage.removeItem("id");
    });
}

function register() {
    if (window.innerWidth > 850) {
        updateStyles(formulario_register, { display: "block" });
        updateStyles(contenedor_login_register, { left: "410px" });
        updateStyles(formulario_login, { display: "none" });
        updateStyles(caja_trasera_register, { opacity: "0" });
        updateStyles(caja_trasera_login, { opacity: "1" });
    } else {
        updateStyles(formulario_register, { display: "block" });
        updateStyles(contenedor_login_register, { left: "0px" });
        updateStyles(formulario_login, { display: "none" });
        updateStyles(caja_trasera_register, { display: "none" });
        updateStyles(caja_trasera_login, { display: "block", opacity: "1" });
    }

}

// Ejecuta anchoPage inicialmente y al cambiar el tamaño de la ventana
anchoPage();
window.addEventListener("resize", anchoPage);




//--  logica de Carlos */


//-- funcion si el usuario esta registrado y decide logearse

function userLogin(){ 
    // Obtener los valores ingresados en el formulario
    const email = document.getElementById("email_login").value;
    const password = document.getElementById("password_login").value;

    // Elemento para mostrar mensajes al usuario
    const messageElement = document.getElementById("message_login");
    messageElement.classList.remove('error', 'success');

     
    // Validación de campos
    if (!email || !password) {
        messageElement.innerHTML = "Por favor, complete ambos campos.";
        messageElement.classList.add('error');
        return;
    }

    // Mostrar un mensaje de carga
    messageElement.innerHTML = "Iniciando sesión...";
      

    // Configuración de la solicitud
    const credentials = btoa(`${email}:${password}`);
    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Basic ${credentials}`
        }
    };
    console.log(credentials)
    // Realizar la solicitud de inicio de sesión
    fetch(urlAPI + '/login', requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            if (response.token) {
                // Almacenar los datos de sesión en localStorage
                
                localStorage.setItem("token", response.token);
                localStorage.setItem("email", response.email);
                localStorage.setItem("id", response.id_usuario);

                // Redirigir al usuario al dashboard
                window.location.href = "index.html";
            } else {
                // Mensaje en caso de que no se obtenga un token
                messageElement.innerHTML = response.message || "Error al iniciar sesión.";
                messageElement.classList.add('error');
            }
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                messageElement.innerHTML = "No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.";
            } else {
                messageElement.innerHTML = error.message || "Error al iniciar sesión";
            }
            messageElement.classList.add('error');
            messageElement.classList.add('error');
        })
        .finally(() => {
           
            
      });
}

// -- funcion para registrarse
function userRegister(){
    
       // Obtener los valores ingresados en el formulario
   const nombre = document.getElementById('nombre_register').value;
   const email = document.getElementById('email_register').value;
   const contraseña = document.getElementById('password_register').value;
   const id_rol = 1 /////////////////////////////////////////////////////////////////cambiar por el id_rol que tengan en la tabla  yo tengo 4,5,6

    // Elemento para mostrar mensajes al usuario
    const messageElement = document.getElementById("message_register");
    messageElement.classList.remove('error', 'success');

    // Validación de campos
    if (!nombre || !contraseña || !email) {
        messageElement.innerHTML = "Por favor, complete los campos.";
        messageElement.classList.add('error');

        return;
    }

    // Mostrar un mensaje de carga
    messageElement.innerHTML = "Registrando su cuenta...";

    // Configuración de la solicitud
    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nombre, email, contraseña, id_rol })
    };
    console.log(requestOptions)
    // Realizar la solicitud de creación de usuario
    fetch(urlAPI + '/register', requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // El usuario se creó correctamente, si es necesario se usa el 
            // objeto response para ejecutar más acciones
            console.log(response)
            messageElement.innerHTML = "Usuario creado correctamente";
            messageElement.classList.add('success');   
                     
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                messageElement.innerHTML = "No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.";
            } else {
                messageElement.innerHTML = error.message || "Error al crear el usuario";
            }
            messageElement.classList.add('error');
            messageElement.classList.add('error');
        })
        .finally(() => {
            
                 
        });
      
       
}