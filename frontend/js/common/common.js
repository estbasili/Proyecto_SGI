// Scrip base para todas las consultas provenientes de Login-register
// tambien se puede ampliar a admin/script.js (pero todavia no esta implementada esta union)


function handleResponse(response) {
    if (!response.ok) {
        // Rechaza la promesa con la información de la API
        return response.json().then(info => {
            return Promise.reject(info); 
        })
    } else {
        // Devuelve el cuerpo de la respuesta en formato JSON
        return response.json();
    }
}