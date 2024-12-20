// Funciones para la seccion administrador
//-- Direccion de la api ----------------------------------------------

const urlAPI = "http://127.0.0.1:5001";

//-- Manejo de la fecha y hora ----------------------------------------------------

function actualizarFecha() {
  const fecha = new Date();
  const opciones = { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
  const fechaFormateada = fecha.toLocaleDateString('es-ES', opciones);   
  document.getElementById('fecha').textContent = fechaFormateada;
}

actualizarFecha(); // Llama a la función al cargar la página
setInterval(actualizarFecha, 1000); // Actualiza cada segundo

//-- Manejo del Usuario que inicio sesion ------------------------------------------

// Recuperar los datos del usuario logeado
const token = localStorage.getItem("token");
const email = localStorage.getItem("email");
const id_usuario_sesion = parseInt(localStorage.getItem("id"),10);

// Mostrar los datos en la consola para verificarlos 
// //console.log("Token:", token);
// //console.log("Email:", email);
// //console.log("ID", id_usuario_sesion);

// Agrega el email al contenido al <h4>
const userInfoElement = document.getElementById("user-info");
userInfoElement.textContent = email;

// Función para cerrar sesión
function logout() {
  // Validar si hay una sesión activa
  if (!localStorage.getItem("token")) {
   // Redirigir al login si no hay token
    window.location.href = "login_register.html";
  }
  localStorage.removeItem("token");
  localStorage.removeItem("email");
  localStorage.removeItem("id");
  window.location.href = "login-register.html"; // Redirigir al login/registro
}


//-- Funciones compartidas entre opciones ------------------------------


// Función genérica para mostrar encabezados (anda)
function showHeader(nameSection, nameSubSection) {
  document.getElementById("section").textContent = nameSection;
  document.getElementById("subSection").textContent = nameSubSection;
}

// Función para limpiar el contenido de showSelect (anda)
function clearContent() {
  document.getElementById("showSelect").innerHTML = "";
}

// Modificación de generateForm para manejar campos tipo select
function generateForm(fields, formId, submitCallback, submitText, submitClass) {
  const formFields = fields.map(field => {
    if (field.tipo === 'select') {
      return generateSelectField(field);  // Generar select
    } else {
      return generateInputField(field);  // Generar input
    }
  }).join('');

  const form = `
    <div class="card-body">
      <form id="${formId}" onsubmit="event.preventDefault(); ${submitCallback}();">
        ${formFields}
        <hr>
        <div class="row">
          <div class="col-12">
            <button type="submit" class="btn ${submitClass} btn-block">${submitText}</button>
          </div>
        </div>
      </form>
    </div>
  `;

  document.getElementById("showSelect").innerHTML = form;
}

// Función principal optimizada para generar el formulario
function generateUpdateForm(fields, formId, submitCallback, submitText, submitClass) {
  const formFields = fields.map(field => {
    if (field.tipo === 'select') {
      return generateSelectField(field);  // Generar select
    } else {
      return generateInputField(field);  // Generar input
    }
  }).join('');

  const form = `
    <div class="card-body">
      <form id="${formId}" onsubmit="event.preventDefault(); ${submitCallback}();">
        ${formFields}
        <hr>
        <div class="row">
          <div class="col-12">
            <button type="submit" class="btn ${submitClass} btn-block">${submitText}</button>
          </div>
        </div>
      </form>
    </div>
  `;

  document.getElementById("showSelect").innerHTML = form;
}
// Función para generar los campos editables
function generateInputField(field) {
  // Aplica el atributo readonly si field.readonly es verdadero
  const isReadonly = field.readonly ? 'readonly' : '';
  return `
    <div class="input-group mb-3">
      <input 
        type="${field.tipo}" 
        id="${field.nombre}" 
        name="${field.nombre}" 
        ${isReadonly} 
        class="form-control" 
        placeholder="${field.placeholder}" 
        value="${field.value || ''}" 
        step="${field.step || ''}">
      <div class="input-group-append">
        <div class="input-group-text">
          <span class="fas fa-align-left"></span>
        </div>
      </div>
    </div>
  `;
}

// Generar el campo select basado en opciones 
function generateSelectField(field) {
  const optionsHTML = field.opciones.map(option => 
    `<option value="${option.value}">${option.text}</option>`
  ).join('');

  return `
    <div class="input-group mb-3">
      <select id="${field.nombre}" name="${field.nombre}" class="form-control">
        <option value="">Seleccione ${field.placeholder}</option>
        ${optionsHTML}
      </select>
    </div>
  `;
}

// Función genérica para hacer peticiones a la API (anda)
async function apiRequest(endpoint, method = 'GET', data = null) {
  const options = {
      method,
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Incluir el token en el encabezado Authorization
      },
      body: data ? JSON.stringify(data) : null
  };
  
  try {
      const response = await fetch(`${urlAPI}${endpoint}`, options);
      //console.log(`${urlAPI}${endpoint}`);
     
      // Manejo respuesta no exitosa
      if (!response.ok) {
          throw new Error(`Error en la solicitud: ${response.status}`);
      }
      
      if (response.status === 204 || response.status === 404) {
         return []; // Retorna un array vacío si no hay productos
      }
      
      // Si hay contenido en la respuesta, devuelvo JSON
      return await response.json();
      
  } catch (error) {
      console.error(`Error en ${method} ${endpoint}:`, error);
      //alert(`Error al procesar la solicitud: ${error.message}`);
  }
}

// Funcion manejadora de mensajes para UI
function showAlert(title, text, icon = 'info', confirmButtonText = 'OK') {
  Swal.fire({
    title: title,                  // Título del mensaje
    text: text,                    // Texto del mensaje
    icon: icon,                    // Tipo de ícono ('success', 'error', 'warning', 'info', 'question')
    confirmButtonText: confirmButtonText // Texto del botón
  });
}




// -- Gestor de Productos ( anda 25/11)----------------------------------------------------


// Función para Agregar Producto (anda)
function showAgregarProducto() {
    showHeader("Gestor de Productos", "Agregar Producto");
    clearContent();
    generateForm(
        [
            { nombre: "producto", placeholder: "Producto" },
            { nombre: "descripcion", placeholder: "Descripción" },
            { nombre: "precio", placeholder: "Precio" },
            { nombre: "stock", placeholder: "Stock" },
            { nombre: "categoria", placeholder: "Categoría" }
            
        ],
        "addProduct",
        "addProduct",
        "Ingresar",
        "btn-success"
    );
}
async function addProduct() {
  const nombre = document.getElementById("producto").value.trim();
  const descripcion = document.getElementById("descripcion").value.trim();
  const precio = parseFloat(document.getElementById("precio").value);
  const stock = parseInt(document.getElementById("stock").value);
  const categoriaNombre = document.getElementById("categoria").value.trim();
  
  
  if (isNaN(precio) || isNaN(stock) || isNaN(id_usuario_sesion)) {
      showAlert('Por favor', 'Completa todos los campos', 'info');
      return;
  }

  if (!nombre || !descripcion || !categoriaNombre) {
      showAlert('Por favor', 'Revisa los campos', 'info');
      return;
  }

  try {
    // Consultar las categorías existentes
    const categorias = await apiRequest(`/usuarios/${id_usuario_sesion}/categorias`, 'GET');
    
    if (!Array.isArray(categorias))
    {
      console.error("La respuesta de categorías no es un arreglo:", categorias);
      showAlert('Ups!', 'No se encontraron Categorías, por favor crea una', 'info');
      return;
    }
    if (!categorias || categorias.length === 0) {
        console.error("No se encontraron categorías en la respuesta de la API.");
        showAlert('Ups!', 'No se encontraron categorías disponibles', 'info');
        return;
    }
    
    // Imprimir las categorías obtenidas para verificar
    ////console.log("Categorías obtenidas:", categorias);

    // Buscar la categoría con el nombre ingresado
    const categoria = categorias.find(c => c.nombre && c.nombre.toLowerCase() === categoriaNombre.toLowerCase());

    if (!categoria) {
        showAlert('Ups!', `La categoría "${categoriaNombre}" no existe en el sistema`, 'info');
        return;
    }

    // Crear el objeto nuevoProducto con el id_categoria correcto
    const nuevoProducto = {
        nombre: nombre,
        descripcion: descripcion,
        precio: precio,
        stock: stock,
        id_categoria: categoria.id_categoria,  // Usar id_categoria de la API
        id_usuario: id_usuario_sesion
    };

    if (nuevoProducto.id_categoria === undefined) {
        console.error("Error: id_categoria sigue siendo undefined después de la búsqueda.");
        showAlert('Error!', 'El ID de la categoría no se obtuvo correctamente', 'error');
        return;
    }

    //console.log("Datos a enviar:", nuevoProducto);

    // Enviar los datos a la API
    const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos`, 'POST', nuevoProducto);
    if (data) {
        showAlert('Bien!', 'Producto guardado correctamente', 'success');
        showAgregarProducto();
   }

  } catch (error) {
    console.error("Error en el proceso de adición de producto:", error);
    showAlert('Error!', 'Hubo un problema al verificar las categorías o al agregar el producto.', 'error');
    
  }

  showAgregarProducto();
}
// fin funcion Agregar Producto

// Función para Eliminar Producto (anda)
function showQuitarProducto() {
  showHeader("Gestor de Productos", "Eliminar Producto");
  clearContent();
  generateForm(
      [{ nombre: "idProduct", placeholder: "Código del producto a eliminar" }],
      "deleteProduct",
      "deleteProduct",
      "Eliminar",
      "btn-danger"
  );
}
async function deleteProduct() {
  const codigo = document.getElementById("idProduct").value.trim();  // Obtener el ID del producto

   // Valida que el código no esté vacío
    if (!codigo) {
        showAlert('Por favor', 'Ingresa un código de producto', 'warning');
        return;
    }

  // Verificar si el producto existe antes de intentar eliminarlo
  try {
      const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'GET');  // Consultar si el producto existe
      //console.log (producto);
      if (producto.length === 0) {
          showAlert('Advertencia', `No se encontró un producto con ese código ${codigo}.`, 'warning');
          return;  // Detener si el producto no existe
      }

      // Si el producto existe, realizar la eliminación
      const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'DELETE');
      if (data) {
          showAlert('Bien!', 'Producto eliminado correctamente.', 'success');
          showQuitarProducto(); // Actualizar la interfaz
      }

  } catch (error) {
    console.error("Error en el proceso de eliminación:", error);
    showAlert('Error', 'Hubo un problema al eliminar el producto', 'error');
          
  }
}
// fin Eliminar

// Función para Actualizar Producto (anda)
function showActualizarProducto() {
  showHeader("Gestor de Productos", "Actualizar Producto");
  clearContent();

  // Crear formulario para ingresar el ID del producto a buscar
  generateForm(
      [
          { nombre: "codigo", placeholder: "Código del producto", tipo: "number" }
      ],
      "buscarProducto",  
      "buscarProducto",
      "Buscar",
      "btn-primary"
  );
}
// Función para buscar el producto por su código
async function buscarProducto() {
  const codigo = document.getElementById("codigo").value.trim();

  if (!codigo) {
      showAlert('Por favor', 'Ingresa el id del producto', 'warning');
      return;
  }

  try {
      // Solicitar los datos del producto a la API
      const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'GET');
      //console.log(producto);

       // Verificar si la respuesta es un array vacío
       if (Array.isArray(producto) && producto.length === 0) {
        showAlert('Ups!', 'Producto no encontrado', 'warning');
        return;  // Detener la ejecución si no se encuentra el producto
    }
          clearContent();
          showHeader("Gestor de Productos", "Actualizar Producto");

          // Generar el formulario para la actualización con los valores recibidos
          generateUpdateForm(
              [
                  { nombre: "codigo", placeholder: "Código", tipo: "number", value: producto.id_producto, readonly: true },
                  { nombre: "producto", placeholder: "Producto", tipo: "text", value: producto.nombre },
                  { nombre: "descripcion", placeholder: "Descripción", tipo: "text", value: producto.descripcion },
                  { nombre: "precio", placeholder: "Precio", tipo: "number", value: producto.precio, step: "any" },
                  { nombre: "stock", placeholder: "Stock", tipo: "number", value: producto.stock },
                  { nombre: "categoria", placeholder: "Categoría", tipo: "select", value: producto.id_categoria, opciones: await getCategorias() }
              ],
              "updateProduct",
              "updateProduct",
              "Actualizar",
              "btn-warning"
          );
      
  } catch (error) {
      if (error.message === 'Producto no encontrado') {
          showAlert('Ups', 'El producto con el id especificado no existe', 'warning');
          
      } else {
          console.error("Error al buscar el producto:", error);
          showAlert('Error', 'Hubo un Problema al buscar el producto', 'error');
      }
  }
}
// Función para obtener las categorías desde la API
async function getCategorias() {
  // Obtener categorías desde la API
  const categorias = await apiRequest(`/usuarios/${id_usuario_sesion}/categorias`, 'GET');
  return categorias.map(categoria => ({
    value: categoria.id_categoria,
    text: categoria.nombre
  }));
}
// Función para actualizar el producto
async function updateProduct() {
  const codigo = document.getElementById("codigo").value.trim();

  // Verificar si el ID del producto existe
  if (!codigo) {
      showAlert('Por favor', 'Ingrese el código del producto', 'warning');
      return;
  }

  // Obtener los valores del formulario
  const productoActualizado = {
      nombre: document.getElementById("producto") ? document.getElementById("producto").value.trim() : '',
      descripcion: document.getElementById("descripcion") ? document.getElementById("descripcion").value.trim() : '',
      // Asegura de que el precio sea un número flotante con 2 decimales
      precio: parseFloat(document.getElementById("precio").value.trim().replace(",", ".")), // Reemplazar coma por punto y convertir a float
      stock: parseInt(document.getElementById("stock") ? document.getElementById("stock").value : NaN),
      id_categoria: parseInt(document.getElementById("categoria") ? document.getElementById("categoria").value : NaN),
      id_usuario: id_usuario_sesion // Este valor debe corresponder al ID del usuario autenticado 
  };

  // Verificar si los campos numéricos son válidos
  if (isNaN(productoActualizado.precio) || isNaN(productoActualizado.stock) || isNaN(productoActualizado.id_categoria) || isNaN(productoActualizado.id_usuario)) {
      showAlert('Por favor', 'Revisa los campos', 'warning');  
      return;
  }

  // Verificar si los campos requeridos están completos
  if (!productoActualizado.nombre || !productoActualizado.descripcion || !productoActualizado.id_categoria || !productoActualizado.id_usuario) {
      showAlert('Por favor', 'Revisa todos los campos', 'warning'); 
      return;
  }

  // Ver el contenido de productoActualizado en la consola para depurar
  // //console.log("Contenido de productoActualizado:", productoActualizado.precio);

  try {
      // Enviar los datos a la API para actualizar el producto
      const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'PUT', productoActualizado);
      if (data) {
          showAlert('Bien!', 'Producto actualizado!', 'success'); 
          showActualizarProducto();
       }
  } catch (error) {
      console.error("Error al actualizar el producto:", error);
      showAlert('Error', 'Hubo un problema al actualizar el producto ', 'error'); 
 }
}
// fin funcion atualizar producto


///////////////////////////////////////////////////////////////////-- Gestor Categoria (Anda 25/11)---------------------------------------------------


// Agregar nueva categoria (anda 25/11)
function showNuevaCategoria() {
  showHeader("Gestor de Categoría", "Agregar Categoría");
  clearContent();
  
  // Obtener las categorías y generar el formulario
 // const categorias = await apiRequest(`/usuarios/${id_usuario_sesion}/categorias`, "GET");
  generateForm(
      [{ nombre: "nuevaCategoria", placeholder: "Ingrese nueva Categoría" }],
      "addCategory",
      "addCategory",
      "Ingresar",
      "btn-success"
  );
  
}
// Función para agregar categoría
async function addCategory() {
  const inputElement = document.getElementById("nuevaCategoria");
  const nuevaCategoriaNombre = inputElement.value.trim();

  // Valida que el campo no esté vacío
  if (!nuevaCategoriaNombre) {
    showAlert('Por favor', 'Completa la categoría', 'info');
    return;
  }

  try{
       const response = await apiRequest(`/usuarios/${id_usuario_sesion}/categorias`, 'POST', { nombre: nuevaCategoriaNombre });
       if (response.message === "La categoría ya existe") {
        showAlert('Ups!',`La categoría "${nuevaCategoriaNombre}" ya existe`, 'info');
        
        } else {
            showAlert('Bien!','La categoría fue agregada.', 'success');
            inputElement.value = ""; // Limpiar el campo de entrada
            showNuevaCategoria();   // Recargar el formulario y categorías
        }
      } catch (error) {
                console.error("Error al agregar categoría:", error);
                showAlert('Error!','Hubo un problema al agregar la categoría. Intenta nuevamente.', 'error');
               
      }
}
// fin agregra categoria

// Asociacion de categoria a producto (anda25/11)
// Función para mostrar el formulario de asociación de categoría a producto
async function showAsociarCategoriaProducto() {
  try {
      showHeader("Asociar Categoría a Producto", "Seleccione el producto y la categoría");
      clearContent();

      // Obtener productos y categorías de la API
      const [productos, categorias] = await Promise.all([
          apiRequest(`/usuarios/${id_usuario_sesion}/productos`, "GET"),
          apiRequest(`/usuarios/${id_usuario_sesion}/categorias`, "GET")
      ]);

      if (!productos || !categorias) {
          throw new Error("Error al cargar productos o categorías.");
      }

      // Generar el formulario de asociación
      const form = `
          <div class="card-body">
              <form id="associateForm" onsubmit="event.preventDefault(); asociarCategoriaProducto();">
                  ${createDropdown("productoSelect", "Seleccione un producto:", productos, "id_producto", "nombre", "descripcion")}
                  ${createDropdown("categoriaSelect", "Seleccione una categoría:", categorias, "id_categoria", "nombre")}
                  <button type="submit" class="btn btn-success btn-block">Asociar</button>
              </form>
          </div>`;

      document.getElementById("showSelect").innerHTML = form;
  } catch (error) {
      showAlert('Error!',`${error.message}`, 'error');
     
  }
}
// Función auxiliar para generar dropdowns
function createDropdown(id, label, items, valueKey, labelKey, descriptionKey) {
  return `
      <div class="form-group">
          <label for="${id}">${label}</label>
          <select id="${id}" class="form-control">
              ${items.map(item => `<option value="${item[valueKey]}">${item[labelKey]}${descriptionKey ? " - " + item[descriptionKey] : ""}</option>`).join('')}
          </select>
      </div>`;
}
// Función para asociar la categoría al producto seleccionado
async function asociarCategoriaProducto() {
  try {
      const productoId = document.getElementById("productoSelect").value;
      const categoriaId = document.getElementById("categoriaSelect").value;

      // Obtener los detalles del producto seleccionado
      const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${productoId}`, "GET");

      if (!producto) {
          throw new Error("Producto no encontrado.");
      }

      // Crear el objeto con los datos del producto y la nueva categoría
      const nuevaCategoriaProducto = {
          nombre: producto.nombre,
          descripcion: producto.descripcion,
          precio: parseFloat(producto.precio), // Asegurarse de que el precio es un número flotante
          stock: producto.stock,
          id_categoria: parseInt(categoriaId, 10),  // Asegurarse de que id_categoria sea un número entero
          id_usuario: producto.id_usuario  // ID de usuario del producto
      };

      // Llamar a apiRequest para realizar la actualización
      
      const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${productoId}`, "PUT", nuevaCategoriaProducto);

      if (data) {
          showAlert('Bien!', 'Producto asociado correctamente', 'success');
          document.getElementById("associateForm").reset(); // Limpia el formulario después de asociar
      } else {
          throw new Error("Error al actualizar el producto.");
      }
  } catch (error) {
      showAlert('Error!', `${error.message}`, 'error');
      
  }
}
// fin de Asociacion


///////////////////////////////////////////////////////////////////-- Gestor Stock (anda 25/11) -------------------------------------------------------
//funcion para actualizar stock de un producto (anda 25/11)

// Función principal para mostrar el formulario de actualización de stock ()
function showActualizarStock() {
  showHeader("Gestor de Stock", "Actualizar Stock de Producto");
  clearContent();

  // Crear formulario para ingresar el ID del producto a buscar
  generateForm(
    [{ nombre: "codigo", placeholder: "Código del producto", tipo: "number" }],
    "buscarProducto",  
    "buscarProducto1",
    "Buscar",
    "btn-primary"
  );
}
// Función para buscar el producto y mostrar solo el campo de stock
async function buscarProducto1() {
  const codigo = document.getElementById("codigo").value.trim();

  if (!codigo) {
    showAlert('Por favor', 'Ingrese el código del Producto', 'info');
    return;
  }

  try {
    // Solicitar los datos del producto a la API
    const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'GET');
    //console.log(producto);

       // Verificar si la respuesta es un array vacío
       if (Array.isArray(producto) && producto.length === 0) {
        showAlert('Ups!', 'Producto no encontrado', 'warning');
        return;  // Detener la ejecución si no se encuentra el producto
    }


    // Almacena los datos del producto
    productoActual = { ...producto, precio: parseFloat(producto.precio) };
    mostrarFormularioActualizarStock(productoActual);

  } catch (error) {
    console.error("Error al buscar el producto:", error);

    // Verificar si el error es un 404
    if (error.response && error.response.status === 404) {
      showAlert('Ups!', 'Producto no encontrado', 'warning');
      
    } else {
      showAlert('Error!', 'Hubo un problema al buscar el producto', 'error');
      
    }
  }
}
// Función para mostrar el formulario de actualización de stock
function mostrarFormularioActualizarStock(producto) {
  clearContent();
  showHeader("Gestor de Stock", "Actualizar Stock");

  generateUpdateForm(
    [
      { nombre: "codigo", placeholder: "Código", tipo: "number", value: producto.id_producto, readonly: true },
      { nombre: "producto", placeholder: "Producto", tipo: "text", value: producto.nombre, readonly: true },
      { nombre: "stock", placeholder: "Cantidad en Stock", tipo: "number", value: producto.stock }
    ],
    "updateStock",
    "updateStock",
    "Actualizar Stock",
    "btn-warning"
  );
}
// Función para actualizar el stock, enviando todos los datos del producto
async function updateStock() {
  const stock = parseInt(document.getElementById("stock").value.trim());

  if (isNaN(stock)) {
    showAlert('Por favor', 'Ingresa una cantidad de stock válida', 'info');
    return;
  }

  productoActual.stock = stock; // Actualizar el stock en el objeto completo del producto
  try {
    const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${productoActual.id_producto}`, 'PUT', productoActual);
    if (data) {
      showAlert('Bien!', 'Stock actualizado', 'success');
      showActualizarStock();
    }
  } catch (error) {
    console.error("Error en PUT /productos:", error);
    showAlert('Error!', 'Hubo un problema al actualizar el producto', 'error');
    
  }
}
// fin de gestir actualizacion stock

// Notificaciones de producto bajo stock y si genera una lista de los productos bajo stock (anda 25/11)
document.addEventListener("DOMContentLoaded", function () {
  loadLowStockProducts(4); // Carga productos de bajo stock en el menú con un límite de 4

  // Establece un intervalo de una hora para actualizar
  setInterval(() => {
    loadLowStockProducts(4);
  }, 3600000);

  // Función general para cargar productos de bajo stock con un límite opcional
  async function loadLowStockProducts(limit = null, renderTable = false) {
    try {
      // Realizar solicitud a la API usando apiRequest
      const productos = await apiRequest(`/usuarios/${id_usuario_sesion}/productos`);
      
    
      // Filtrar productos con stock bajo
      const productosBajoStock = productos.filter(producto => producto.stock <= 30); //  límite de stock según sea necesario

      // Renderizar productos dependiendo de la opción renderTable
      if (renderTable) {
        renderLowStockTable(productosBajoStock); // Renderiza todos los productos en una tabla
      } else {
        renderLowStockMenuItems(productosBajoStock, limit); // Renderiza los productos en el menú
      }
    } catch (error) {
      console.error("Error al cargar productos con stock mínimo:", error);
      showAlert('Error!', 'Hubo un problema al cargar productos con stock mínimo', 'error');
    }
  }

  // Función para renderizar productos de bajo stock en el menú de notificaciones
  function renderLowStockMenuItems(productos, limit) {
    const stockItemsContainer = document.getElementById("low-stock-items");
    const stockBadge = document.getElementById("stock-badge");
    stockItemsContainer.innerHTML = ""; // Limpia el contenido previo

    if (productos.length === 0) {
      stockItemsContainer.innerHTML = "<p class='dropdown-item text-muted'>No hay productos con stock mínimo.</p>";
      // Ocultar el badge de notificaciones
      stockBadge.style.display = "none";
    } else {
      const productosMostrados = limit ? productos.slice(0, limit) : productos;
      productosMostrados.forEach((producto) => {
        const itemHTML = `
          <a href=# class="dropdown-item">
            <i class="fas fa-box mr-2"></i> ${producto.nombre}
            <span class="float-right text-muted text-sm">Stock: ${producto.stock}</span>
          </a>
          <div class="dropdown-divider"></div>
        `;
        stockItemsContainer.insertAdjacentHTML("beforeend", itemHTML);
      });

      // Actualiza el contador de productos en stock mínimo
      //document.getElementById("stock-badge").textContent = productos.length;
      stockBadge.textContent = productos.length;
      stockBadge.style.display = "inline-block"; // Asegurar que sea visible
    }
  }

  // Función para renderizar la tabla completa de productos de bajo stock con DataTables
  function renderLowStockTable(productos) {
    const showSelect = document.getElementById("showSelect");
    showSelect.innerHTML = `
      <div class="card-body table-responsive p-0" style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Categoría</th>
            </tr>
          </thead>
          <tbody>
            ${productos.map(producto => `
              <tr>
                <td>${producto.nombre}</td>
                <td>${producto.descripcion}</td>
                <td>${producto.precio}</td>
                <td>${producto.stock}</td>
                <td>${producto.categoria_nombre}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>`;

    // Inicializar DataTables en la tabla recién creada
    $('#dataTable_products').DataTable({
      paging: false,        // Desactiva la paginación
      info: false,          // Oculta el texto de "showing X to Y of Z entries"
      searching: false,     // Opcional: desactiva la barra de búsqueda si no la necesitas
      lengthChange: false   // Oculta el selector de "entries per page"
    });
  }

  // Cargar productos al abrir el menú de notificaciones
  document.querySelector(".nav-item.dropdown > a").addEventListener("click", () => loadLowStockProducts(4));

  // Mostrar todos los productos de bajo stock en la tabla al hacer clic en "See All Notifications"
  document.getElementById("see-all-notifications").addEventListener("click", (event) => {
    event.preventDefault(); // Evita el comportamiento por defecto del enlace
    showHeader("Gestor de Stock","Productos con bajo stock");
    clearContent();
    loadLowStockProducts(null, true); // Carga todos los productos de bajo stock sin límite y los renderiza en la tabla
  });
});
// fin de agrega notificaciones de producto bajo stock 



//////////////////////////////////////////////////////////////-- Gestor de proveedores (anda 25/11)------------------------------------------------
 
// Función para Agregar Proveedor (anda25/11)
function showAgregarProveedor() {
  showHeader("Gestor de Proveedores", "Agregar Proveedor y Asociar productos");
  clearContent();
  generateForm(
      [
          { nombre: "nombre", placeholder: "Nombre de proveedor" },
          { nombre: "email", placeholder: "Email" },
          { nombre: "telefono", placeholder: "Teléfono" },
     ],
      "addProveedor",
      "addProveedor",
      "Ingresar",
      "btn-success"
  );
}
// Función para obtener las categorías desde la API
async function getUsuarios() {
  // Obtener categorías desde la API
  const usuarios = await apiRequest('/usuarios', 'GET');
  return usuarios.map(usuario => ({
    value: usuario.id_usuario,
    text: usuario.nombre
  }));
}
async function addProveedor() {
  const nuevoProveedor = {
      nombre: document.getElementById("nombre").value,
      email: document.getElementById("email").value,
      telefono: document.getElementById("telefono").value,
      id_usuario: id_usuario_sesion
  };

  // Verificar si el nombre está vacío
   if (!nuevoProveedor.nombre || !nuevoProveedor.email || !nuevoProveedor.telefono) {
      showAlert('Por favor!', 'completa todos los campos', 'info');  
    
      return;  // Detener la ejecución si el nombre está vacío
   }

  const data = await apiRequest(`/usuarios/${id_usuario_sesion}/proveedores`, 'POST', nuevoProveedor);
  if (data) {
      // Verificar que el arreglo no esté vacío
      if (data.length > 0) {
          // Obtener el último elemento del array
           const ultimoProveedor = data[data.length - 1];
          // Extraer el id_proveedor del último objeto
            const idProveedor = ultimoProveedor.id_proveedor;
            showAlert('Bien!', 'Proveedor agregado correctamente', 'success');  
            //console.log(idProveedor);
        // Ahora que el proveedor ha sido creado, mostrar la tabla para asociar productos
            await showAsociarProductos(idProveedor); // Mostrar productos para asociar
            
        } 
  }
}
// muestra la table para selleccionar los productoa asociados al proveedor
async function showAsociarProductos(idProveedor) {
  clearContent();
  
  const productos = await apiRequest(`/usuarios/${id_usuario_sesion}/productos`, 'GET');  // Obtener productos disponibles
  
  // Selecciona el contenedor con id="showSelect"
  const container = document.getElementById("showSelect");

  // Limpia el contenido previo en el contenedor
  container.innerHTML = "";

  // Crear una tabla con DataTables
  const table = document.createElement("table");
  table.setAttribute("id", "productosTable");
  table.classList.add("display", "table", "table-striped", "table-bordered","table-blur");  // Clases para estilo Bootstrap

  // Crear el encabezado de la tabla
  table.innerHTML = `
    <thead>
      <tr>
        <th><input type="checkbox" id="selectAll"></th>
        <th>Nombre del Producto</th>
        <th>Descripción</th>
        <th>Stock</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;
  container.appendChild(table);

  // Insertar productos en las filas de la tabla
  const tbody = table.querySelector("tbody");
  productos.forEach(producto => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input type="checkbox" class="producto-checkbox" value="${producto.id_producto}"></td>
      <td>${producto.nombre}</td>
      <td>${producto.descripcion}</td>
      <td>${producto.stock}</td>
    `;
    tbody.appendChild(row);
  });

  // Botón para asociar productos
  const button = document.createElement("button");
  button.textContent = "Asociar Productos";
  button.type = "button";
  button.classList.add("btn", "btn-success", "mt-3");
  button.onclick = () => asociarProductosAlProveedor(idProveedor);
  container.appendChild(button);

  $(document).ready(function() {
    $('#productosTable').DataTable({
       paging: true,
       searching: true,
       info: true,
       responsive: true,
       language: {
          search: "Buscar ",
          lengthMenu: "Mostrar _MENU_ registros por página",
          zeroRecords: "No se encontraron resultados",
          info: "Mostrando página _PAGE_ de _PAGES_",
          infoEmpty: "No hay registros disponibles",
          infoFiltered: "(filtrado de _MAX_ registros totales)",
          paginate: {
             first: "Primero",
             last: "Último",
             next: "Siguiente",
             previous: "Anterior"
          }
       },
       dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
       pagingType: "simple_numbers",
       
    
    });
 });
 

  // Event listener para seleccionar o deseleccionar todos los checkboxes
  document.getElementById("selectAll").addEventListener("change", function() {
    const checkboxes = document.querySelectorAll(".producto-checkbox");
    checkboxes.forEach(checkbox => {
      checkbox.checked = this.checked;
    });
  });
}
// Función para asociar los productos seleccionados a un proveedor
async function asociarProductosAlProveedor(idProveedor) {
  const selectedProductos = Array.from(document.querySelectorAll('.producto-checkbox:checked'))
                                  .map(checkbox => parseInt(checkbox.value, 10));

  if (selectedProductos.length === 0) {
    showAlert('Por favor!', 'Selecciona al menos un producto', 'info');  
    return;
  }

  // Enviar los productos seleccionados a la API para asociarlos con el proveedor
  
  const data = await apiRequest(`/usuarios/${id_usuario_sesion}/proveedores/${idProveedor}/productos/varios`, 'POST', { productos: selectedProductos });

  if (data) {
    showAlert('Bien!', 'Productos asociados correctamente', 'success');  
    
  } else {
    showAlert('Error!', 'Hubo un error al asociar los productos al proveedor', 'error');  
    
  }
}
// fin para Agregar proveeedor


// Función para editar proveedor
async function getProvedores(){
  
  const data = await apiRequest(`/usuarios/${id_usuario_sesion}/listarProveedores`, 'GET');
  return data;
}

function tabla_listado_proveedores(data) {
  // Obtener el contenedor donde se mostrará la tabla
  const content = document.getElementById("showSelect");
  content.innerHTML = ""; // Limpiar contenido previo

  // Crear la tabla
  const table = document.createElement("table");
  table.className = "table table-striped table-bordered"; // Clases de Bootstrap para estilo

  // Crear el encabezado de la tabla
  const thead = document.createElement("thead");
  thead.innerHTML = `
    <tr>
      <th>ID Proveedor</th>
      <th>Nombre</th>
      <th>Acción</th>
    </tr>
  `;
  table.appendChild(thead);

  // Crear el cuerpo de la tabla
  const tbody = document.createElement("tbody");
  data.forEach(proveedor => {
    const row = document.createElement("tr");

    // Columna ID
    const idCol = document.createElement("td");
    idCol.textContent = proveedor.id_proveedor;
    row.appendChild(idCol);

    // Columna Nombre
    const nameCol = document.createElement("td");
    nameCol.textContent = proveedor.nombre;
    row.appendChild(nameCol);

    // Columna Acción
    const actionCol = document.createElement("td");
    const editButton = document.createElement("button");
    editButton.className = "btn btn-primary btn-sm";
    editButton.textContent = "Editar";
    editButton.onclick = () => editarProveedor(proveedor.id_proveedor); // Asocia función de editar
    actionCol.appendChild(editButton);
    row.appendChild(actionCol);

    tbody.appendChild(row);
  });
  table.appendChild(tbody);

  // Añadir la tabla al contenedor
  content.appendChild(table);
  
}

async function editarProveedor(id_proveedor) {
  const content = document.getElementById("showSelect");
  content.innerHTML = ""; // Limpiar contenido previo
  showAsociarProductos(id_proveedor);
}

async function showEditarProveedor() {
  showHeader("Gestor de Proveedores", "Editar Proveedor");
  clearContent();
  // Obtener los proveedores y mostrar la tabla
  const data = await getProvedores();
  tabla_listado_proveedores(data);
}
// fin funcion para editar proveedor



//Función para consultar los provedores asociados a productos especificos  (anda 25/11)
function showConsultarProveedor() {
  showHeader("Gestor de Proveedores", "Proveedores asociados al producto");
  clearContent();
  // Crear formulario para ingresar el ID del producto a buscar
  generateForm(
    [
      { nombre: "codigo", placeholder: "Código del producto", tipo: "number" }
    ],
    "buscarProducto",  
    "buscarProducto3",
    "Buscar",
     "btn-primary"
  );
  
}
// Función para buscar el producto por su código
async function buscarProducto3() {
  const codigo = document.getElementById("codigo").value.trim();
  
  if (!codigo) {
    showAlert('Por favor!', 'Ingrese el código del producto', 'info');
    return;
  }
  
  // Solicitar los datos del producto a la API
  const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'GET');
  //console.log(producto);

     // Verificar si la respuesta es un array vacío
     if (Array.isArray(producto) && producto.length === 0) {
      alert("Producto no encontrado");
      return;  // Detener la ejecución si no se encuentra el producto
  }
      clearContent();
      showHeader("Gestor de Proveedores", " Proveedores asociados al producto");

     const div = `
                  <div class="card-body bg-dark rounded p-3 shadow-sm">
                    <h4>Producto</h4>
                    <p>Código: ${producto.id_producto}</p>
                    <p>Nombre: ${producto.nombre}</p>
                  <div class="card-body bg-dark  p-1 text-center">
                    <h4>Proveedores</h4>
                  </div>
                  </div>
                 
                 `;

      document.getElementById("showSelect").innerHTML = div; 
      proveedoresAsociados(producto.id_producto);  
    
} 
 async function proveedoresAsociados(id_producto) {
      const data = await apiRequest(`/usuarios/${id_usuario_sesion}/proveedores/${id_producto}`, 'GET');
      if (data && Array.isArray(data)) {
        // Generar la tabla
        const table = `
          <div class="card-body table-responsive p-0 table-blur  style="height: 300px;">
            <table id="dataTable_products" class="table table-head-fixed text-nowrap">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                </tr>
              </thead>
              <tbody id="tableBody_products">
                <!-- Las filas se generarán aquí dinámicamente -->
              </tbody>
            </table>
          </div>`;
        
        // Obtener el segundo hijo div de "showSelect"
        const firstChildDiv = document.querySelector("#showSelect > div");
       
  
           // Insertar la tabla después del primer hijo div
           firstChildDiv.insertAdjacentHTML('afterend', table);
  
          // Generar las filas para cada proveedor
          const rows = data.map(proveedor => `
            <tr>
              <td>${proveedor.id_proveedor}</td>
              <td>${proveedor.nombre_proveedor}</td>
            </tr>
          `).join(""); // Unir todas las filas en un solo string
          // Insertar las filas en el cuerpo de la tabla
          document.getElementById("tableBody_products").innerHTML = rows;
      } else {
        // Manejar el caso en que no hay proveedores
        showAlert('Ups!', 'No se encontraron Proveedores asociados', 'warning');
      }
   
}

// fin funcion consulta proveedore de un producto
/*
// Función para buscar el producto por su código
async function buscarProducto3() {
const codigo = document.getElementById("codigo").value.trim();

if (!codigo) {
  alert("Por favor, ingresa el código del producto.");
  return;
}

// Solicitar los datos del producto a la API
const producto = await apiRequest(`/usuarios/${id_usuario_sesion}/productos/${codigo}`, 'GET');
console.log(producto);

   // Verificar si la respuesta es un array vacío
   if (Array.isArray(producto) && producto.length === 0) {
    alert("Producto no encontrado");
    return;  // Detener la ejecución si no se encuentra el producto
}
    clearContent();
    showHeader("Gestor de Proveedores", " Proveedores asociados al producto");

   const div = `
                <div class="card-body bg-dark rounded p-3 shadow-sm">
                  <h4>Producto</h4>
                  <p>Código: ${producto.id_producto}</p>
                  <p>Nombre: ${producto.nombre}</p>
                <div class="card-body bg-dark  p-1 text-center">
                  <h4>Proveedores</h4>
                </div>
                </div>
               
               `;

    document.getElementById("showSelect").innerHTML = div; 
    proveedoresAsociados(producto.id_producto);  
  
} 
async function proveedoresAsociados(id_producto) {
    const data = await apiRequest(`/usuarios/${id_usuario_sesion}/proveedores/${id_producto}`, 'GET');
    if (data && Array.isArray(data)) {
      // Generar la tabla
      const table = `
        <div class="card-body table-responsive p-0 table-blur  style="height: 300px;">
          <table id="dataTable_products" class="table table-head-fixed text-nowrap">
            <thead>
              <tr>
                <th>Id del Proveedor</th>
                <th>Nombre</th>
              </tr>
            </thead>
            <tbody id="tableBody_products">
              <!-- Las filas se generarán aquí dinámicamente -->
            </tbody>
          </table>
        </div>`;
      
      // Obtener el segundo hijo div de "showSelect"
      const firstChildDiv = document.querySelector("#showSelect > div");
     

         // Insertar la tabla después del primer hijo div
         firstChildDiv.insertAdjacentHTML('afterend', table);

        // Generar las filas para cada proveedor
        const rows = data.map(proveedor => `
          <tr>
            <td>${proveedor.id_proveedor}</td>
            <td>${proveedor.nombre_proveedor}</td>
          </tr>
        `).join(""); // Unir todas las filas en un solo string
        // Insertar las filas en el cuerpo de la tabla
        document.getElementById("tableBody_products").innerHTML = rows;
    } else {
      // Manejar el caso en que no hay proveedores
      console.warn("No se encontraron proveedores asociados.");
    }
 
}
// fin funcion Consultar proveedres de un producto 
*/
 
////////////////////////////////////////////////////////////////-- Gestor de compras ---------------------------------------------------
  

function generarFormOrdenCompra(){
  const form = `
    <div class="card-body">
      <form id="form_orden_compra" onsubmit="enviarOrdenCompra(event);">
        <div class="row">
          <div class="col-12">
            <!-- Label para el select -->
            <label for="proveedor">Seleccionar Proveedor:</label>
            <select id="proveedores" name="proveedor" class="form-control">
              <option value="">Cargando proveedores...</option>
            </select>
            <input type="hidden" id="proveedor_seleccionado" />
            <br>
          </div>

          <!-- Fecha de Pedido -->
          <div class="col-6">
            <label for="fecha_pedido">Fecha de Pedido:</label>
            <input type="date" id="fecha_pedido" name="fecha_pedido" class="form-control" required>
          </div>

          <!-- Fecha de Recepción -->
          <div class="col-6">
            <label for="fecha_recepcion">Fecha de Recepción:</label>
            <input type="date" id="fecha_recepcion" name="fecha_recepcion" class="form-control">
          </div>

          <!-- Estado -->
          <div class="col-12">
            <label for="estado">Estado:</label>
            <select id="estado" name="estado" class="form-control" required>
                <option value="">Cargando estados...</option>
            </select>
          </div>

          <div class="col-12">
            <!-- Contenedor para las filas de productos -->
            <label>Productos:</label>
            <div id="productos-container">
              <!-- Aquí se insertarán las filas dinámicamente -->
            </div>
            <!-- Botón para agregar más filas -->
            <button type="button" id="add-product-row" class="btn btn-success btn-sm">+ Agregar Producto</button>
          </div>
          <div class="col-12 mt-4">
            <!-- Botón de submit -->
            <button type="submit" class="btn btn-primary btn-block">Enviar</button>
          </div>
        </div>
      </form>
    </div>`;
  
  document.getElementById("showSelect").innerHTML = form;

  // Cargar proveedores y configurar el formulario
  loadProveedoresSelect();
  loadState();
  setFechaPedido();
  cargarMultipleInput();
}

async function loadState() {
  const estadoSelect = document.getElementById('estado');

  try {
      // Llamada a la API utilizando apiRequest
      const data = await apiRequest('/estados', 'GET');////////////////////////////////////////////////
      //console.log(data);
      // Limpiar las opciones anteriores del select
      estadoSelect.innerHTML = '';

      ////////////////////////////////////////////////////////////////////////////////////////////////
      if (data.message == "Error al recuperar los estados desde la base de datos."){
        alert("no hay estados");
        return;
      }
      ///////////////////////////////////////////////////////////////////////////////////////////////
      
      // Agregar nuevas opciones al select
      data.forEach(estado => {
          const option = document.createElement('option');
          option.value = estado.id_estado;
          option.textContent = estado.descripcion;
          estadoSelect.appendChild(option);
      });
  } catch (error) {
      // Manejo de errores
      console.error("Error al cargar los estados:", error);
      estadoSelect.innerHTML = '<option value="">Error al cargar estados</option>';
  }
}


function setFechaPedido() {
  const fechaPedidoInput = document.getElementById("fecha_pedido");

  // Obtener la fecha actual
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0'); // Meses empiezan desde 0
  const dd = String(today.getDate()).padStart(2, '0');

  const formattedDate = `${yyyy}-${mm}-${dd}`;
  fechaPedidoInput.value = formattedDate;
}

function capturarProductos() {
  const ordenCompra = {
    fecha_pedido: document.getElementById("fecha_pedido").value,
    fecha_recepcion: document.getElementById("fecha_recepcion").value,
    estado: parseInt(document.getElementById("estado").value, 10),  // Convierte a int
    id_proveedor: parseInt(document.getElementById("proveedor_seleccionado").value, 10),  // Convierte a int
    id_usuario: id_usuario_sesion,  // Se asume que 'id_usuario_sesion' está definido correctamente
    productos: []  // Lista para almacenar productos, puede llenarse dinámicamente
  };

  const productRows = document.querySelectorAll("#productos-container .product-row");

  productRows.forEach(row => {
    const productoId = row.querySelector(".producto-select").value;
    const cantidad = row.querySelector("input[name='cantidad[]']").value;

    if (productoId && cantidad) {
      ordenCompra.productos.push({
        id_producto: productoId,
        cantidad: parseInt(cantidad, 10) // Convertir cantidad a entero
      });
    }
  });

  //console.log(ordenCompra); // Para verificar el resultado en la consola
  return ordenCompra;
}


async function guardarOrdenCompra(ordenCompra) {
      //console.log("Datos enviados a la API:", ordenCompra); // Log de los datos enviados

      // Realizar la solicitud a la API
      const data = await apiRequest(`/usuarios/${id_usuario_sesion}/ordenes`, 'POST', ordenCompra);

      if(!data.error){
        //console.log(data);
        showAlert('Bien!', `${data.message}`, 'success');
      }else{
        showAlert('Error!',`${data.message}`,'error');
      }
      
} 

function enviarOrdenCompra(event) {
  event.preventDefault(); // Prevenir la acción por defecto del formulario

  // Validar campos obligatorios
  const proveedorId = document.getElementById("proveedor_seleccionado").value;
  const fecha_pedido = document.getElementById("fecha_pedido").value;
  const fecha_recepcion = document.getElementById("fecha_recepcion").value;
  const estado = parseInt(document.getElementById("estado").value, 10);  // Convertimos a int
  const proveedor = document.getElementById('proveedor_seleccionado').value;

  if (!proveedorId || !fecha_pedido || !fecha_recepcion || isNaN(estado) || !proveedor) {
    alert("Por favor, complete todos los campos obligatorios.");
    return;
  }
  // Capturar productos
  const ordenCompra = capturarProductos();

  if (ordenCompra.length === 0) {
    alert("Debe agregar al menos un producto.");
    return;
  }

  guardarOrdenCompra(ordenCompra); // Llamar a la función para guardar la orden
}

function loadProductos(selectElement,idProveedor) {
    fetch(`http://127.0.0.1:5001/usuarios/${id_usuario_sesion}/proveedores/${idProveedor}/productos`,
      {
      method: 'GET', // Por defecto, el método GET ya está configurado, pero lo incluyo para mayor claridad
      headers: {
          'Authorization': `Bearer ${token}`, // Incluir el token en el encabezado Authorization
          'Content-Type': 'application/json' // Tipo de contenido
      }
    })
    .then(response => response.json())
    .then(data => {
      //console.log(data);
      // Limpiar el select antes de llenarlo
      selectElement.innerHTML = '';

      // Opción por defecto
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.textContent = 'Selecciona un producto';
      selectElement.appendChild(defaultOption);

      // Agregar las opciones de productos
      data.forEach(producto => {
        const option = document.createElement('option');
        option.value = producto.idProducto; // ID del producto
        option.textContent = producto.nombre_producto; // Nombre del producto
        selectElement.appendChild(option);
      });
    })
    .catch(error => {
      console.error('Error al cargar los productos:', error);
      selectElement.innerHTML = '<option value="">Error al cargar productos</option>';
    });
}

function cargarMultipleInput() {
  const productosContainer = document.getElementById("productos-container");
  const addProductRowButton = document.getElementById("add-product-row");
  const proveedorSelect = document.getElementById('proveedor_seleccionado');

  // Evento para agregar nuevas filas
  addProductRowButton.addEventListener("click", () => {
    // Validar si hay un proveedor seleccionado
    if (!proveedorSelect.value || proveedorSelect.value === "") {
      alert("Por favor, selecciona un proveedor antes de agregar productos.");
      return; // Salir de la función si no hay proveedor seleccionado
    }

    // Crear nueva fila
    const newRow = document.createElement("div");
    newRow.classList.add("row", "mb-3", "align-items-center", "product-row");

    newRow.innerHTML = `
      <div class="col-md-8">
        <select name="producto[]" class="form-control producto-select">
          <option value="">Cargando productos...</option>
        </select>
      </div>
      <div class="col-md-3">
        <input type="number" name="cantidad[]" class="form-control" placeholder="Cantidad" min="1" />
      </div>
      <div class="col-md-1">
        <button type="button" class="btn btn-danger btn-sm remove-row">-</button>
      </div>
    `;

    productosContainer.appendChild(newRow);

    // Seleccionar el nuevo select de productos
    const newSelect = newRow.querySelector(".producto-select");

    // Cargar productos en el nuevo select
    loadProductos(newSelect,proveedorSelect.value);

    // Evento para eliminar una fila
    newRow.querySelector(".remove-row").addEventListener("click", () => {
      newRow.remove();
    });
  });

  // Evento inicial para eliminar la fila existente
  productosContainer.addEventListener("click", (event) => {
    if (event.target.classList.contains("remove-row")) {
      event.target.closest(".product-row").remove();
    }
  });
}

function loadProveedoresSelect(){
  // Función para cargar los proveedores desde la API
  
  fetch(`http://127.0.0.1:5001/usuarios/${id_usuario_sesion}/proveedores`,
    {
      method: 'GET', // Por defecto, el método GET ya está configurado, pero lo incluyo para mayor claridad
      headers: {
          'Authorization': `Bearer ${token}`, // Incluir el token en el encabezado Authorization
          'Content-Type': 'application/json' // Tipo de contenido
      }
    }
  )
    .then(response => response.json())  // Convertir la respuesta en JSON
    .then(data => {
      const selectElement = document.getElementById('proveedores');
      
      // Limpiar la opción predeterminada mientras se cargan los proveedores
      selectElement.innerHTML = '';

      // Crear la opción predeterminada
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.textContent = 'Selecciona un proveedor';
      selectElement.appendChild(defaultOption);

      // Recorrer los proveedores y agregar opciones al select
      data.forEach(proveedor => {
        const option = document.createElement('option');
        option.id = proveedor.id_proveedor;  // Usamos el id_proveedor como id
        option.value = proveedor.id_proveedor;  // El primer valor es el ID del proveedor
        option.textContent = proveedor.nombre;  // El segundo valor es el nombre del proveedor
        selectElement.appendChild(option);  // Agregar la opción al select
      });

      // Agregar el evento change para obtener el ID del proveedor seleccionado
      selectElement.addEventListener('change', function() {
        const selectedId = selectElement.value; // El valor del select es el ID del proveedor
        //console.log('Proveedor seleccionado ID:', selectedId);
        document.getElementById('proveedor_seleccionado').value = selectedId;
        // Aquí puedes usar el ID seleccionado, como enviarlo a un servidor o hacer algo más
      });
    })
    .catch(error => {
      console.error('Error al cargar los proveedores:', error);
      // Manejo de error: en caso de que no se carguen los proveedores
      const selectElement = document.getElementById('proveedores');
      selectElement.innerHTML = '';
      const errorOption = document.createElement('option');
      errorOption.value = '';
      errorOption.textContent = 'Error al cargar los proveedores';
      selectElement.appendChild(errorOption);
    });
}
// Esta función se llamará al mostrar el formulario para agregar una compra
function showAgregarCompra(item){
  showHeader("Gestor de Compras","Agregar Compra");
  clearContent();
  generarFormOrdenCompra(); // Llama a la función para generar el formulario y cargar proveedores
}

  
  /////////////////////////////////////////////////////////////-- Gestor de Reportes -------------------------------------------------

  // Función para Listar Productos  con limite de stock (anda 25/11)
function showProdBS() {
    showHeader("Gestor de Reportes", "Lista de Productos Bajo Stock");
    clearContent();
    
    // Crear un campo de entrada y un botón para el límite de stock
    const controls = `
      <div class="card-body">
        <label for="stockThresholdInput">Límite de Stock:</label>
        <input type="number" id="stockThresholdInput" value="100" min="1" style="width: 60px;"> 
        <button onclick="establecerStock()"  class="btn btn-success">Aplicar</button>
      </div>
    `;
  
    const table = `
      <div class="card-body table-responsive p-0 table-blur  style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Descripcion</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Categoria</th>
            </tr>
          </thead>
          <tbody id="tableBody_products"></tbody>
        </table>
      </div>`;
    
    document.getElementById("showSelect").innerHTML = controls + table;
  
    // Límite de stock inicial
    const initialStockThreshold = parseInt(document.getElementById("stockThresholdInput").value, 10);
    Products(initialStockThreshold);
}
  // Función que se llama al hacer clic en el botón "Aplicar"
function establecerStock() {
    const stockThreshold = parseInt(document.getElementById("stockThresholdInput").value, 10);
    Products(stockThreshold);
}
  // Peticion a la API
async function Products(stockThreshold) {
    const data = await apiRequest(`/usuarios/${id_usuario_sesion}/productos`);
    if (data && Array.isArray(data)) {
      // Filtrar productos con stock por debajo del límite
      const lowStockProducts = data.filter(product => product.stock < stockThreshold);
      const content = lowStockProducts.map(product => `
        <tr>
          <td>${product.id_producto}</td>
          <td>${product.nombre}</td>
          <td>${product.descripcion}</td>
          <td>${product.precio}</td>
          <td>${product.stock}</td>
          <td>${product.categoria_nombre}</td>
        </tr>
      `).join("");
      document.getElementById("tableBody_products").innerHTML = content;
    }
}
  // fin de listar productos con limite de stock



  // Funcion para el historial de orden de compra (anda 26/11 )
function showHCompras() {
    showHeader("Gestor de Reportes", "Historial de Compras");
    clearContent();

    // Crear estructura inicial de la tabla
    const table = `
     
        <div class="card-body table-responsive p-0 table-blur style="height: 100%; width: 100%;" >
            <table id="dataTable_compras" class="table table-head-fixed text-nowrap">
                <thead>
                    <tr>
                        <th>ID Orden</th>
                        <th>Fecha Pedido</th>
                        <th>Fecha Recepción</th>
                        <th>Estado</th>
                        <th>Proveedor</th>
                        <th>Detalles</th>
                    </tr>
                </thead>
                <tbody id="tableBody_orders"></tbody>
            </table>
        </div>
    `;

    // Insertar la tabla en el contenedor
    document.getElementById("showSelect").innerHTML = table;

    // Cargar los datos
    compras();
}
// Petición a la API
async function compras() {
    const data = await apiRequest(`/usuarios/${id_usuario_sesion}/ordenes`);
    
    console.log(data);
    if (data == null){
      showAlert('Ups!', 'no hay ordenes','info');
      return;
    }
    
    
    if (data && Array.isArray(data)) {
        // Generar contenido de la tabla
        const content = data.map(orden => `
            <tr>
                <td>${orden.id_orden}</td>
                <td>${orden.fecha_pedido}</td>
                <td>${orden.fecha_recepcion ? orden.fecha_recepcion : "Sin recepción"}</td>
                <td>${orden.estado_descri}</td>
                <td>${orden.nombre_proveedor}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="detalleProductos(${orden.id_orden})">
                        Ver Detalle
                    </button>
                </td>
            </tr>
        `).join("");

        // Insertar contenido en la tabla
        document.getElementById("tableBody_orders").innerHTML = content;

        // Inicializar DataTable para la tabla generada
        $('#dataTable_compras').DataTable({
            paging: true,
            searching: true,
            info: false,
            responsive: true,
            language: {
                search: "Buscar: ",
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "No se encontraron resultados",
                infoEmpty: "No hay registros disponibles",
                infoFiltered: "(filtrado de _MAX_ registros totales)",
                paginate: {
                    first: "Primero",
                    last: "Último",
                    next: "Siguiente",
                    previous: "Anterior"
                }
            }
        });
    }
}
// Función para manejar el botón de detalle
async function detalleProductos(idOrden) {
    clearContent();
    showHeader("Gestor de Reportes", "Detalle de contenido");

   const div = `
                <div class="card-body bg-dark rounded p-3 shadow-sm">
                  <h4>Detalle de Orden</h4>
                  <p>Código: ${idOrden}</p>
                <div class="card-body bg-dark  p-1 text-center">
                  <h4>Productos</h4>
                </div>
                </div>
               
               `;

    document.getElementById("showSelect").innerHTML = div; 
    productosAsociados(idOrden);  
}
async function productosAsociados(idOrden) {
  const data = await apiRequest(`/usuarios/${id_usuario_sesion}/ordenes/${idOrden}`, 'GET');
  
  if (data && Array.isArray(data)) {
    // Generar la tabla
    const table = `
      <div class="card-body table-responsive p-0 table-blur  style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>Código del Producto</th>
              <th>Nombre</th>
              <th>Cantidad</th>
            </tr>
          </thead>
          <tbody id="tableBody_products">
            <!-- Las filas se generarán aquí dinámicamente -->
          </tbody>
        </table>
      </div>`;
    
    // Obtener el segundo hijo div de "showSelect"
    const firstChildDiv = document.querySelector("#showSelect > div");
   
       // Insertar la tabla después del primer hijo div
       firstChildDiv.insertAdjacentHTML('afterend', table);

      // Generar las filas para cada producto
      const rows = data.map(producto => `
        <tr>
          <td>${producto.id_producto}</td>
          <td>${producto.nombre}</td>
          <td>${producto.cantidad}</td>
        </tr>
      `).join(""); // Unir todas las filas en un solo string
      // Insertar las filas en el cuerpo de la tabla
      document.getElementById("tableBody_products").innerHTML = rows;
  } else {
    // Manejar el caso en que no hay proveedores
    showAlert('Ups!', 'No se encontraron Proveedores asociados', 'warning');
    console.warn("No se encontraron proveedores asociados.");
  }
}
// fin para listar detalle de compra




/// funcion para listar inventario actual (anda 25/11)
function showInventarioActual(){
  showHeader("Gestor de Reportes", "Historial Actual");
  clearContent();
  
  const table = `
    <div class="card-body table-responsive p-0 table-blur style="height: 100%; width: 100%;" ">
    <!-- Tabla -->
    <table id="dataTable_products" class="table table-head-fixed text-nowrap">
      <thead>
        <tr>
          <th>Código del Producto</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Stock</th>
          <th>Proveedor</th>
       </tr>
      </thead>
      <tbody id="tableBody_products"></tbody>
      <tfoot>
        <tr>
        <th></th> <!-- Vacío para la columna ID -->
        <th></th> <!-- Vacío para la columna Nombre -->
        <th></th> <!-- Vacío para la columna Descripción -->
        <th>Total de stock: 0</th> <!-- Mostrar total aquí -->
        <th></th> <!-- Vacío para la columna Proveedor -->
      </tr>
      </tfoot>
    </table>
  </div>`;
  
  document.getElementById("showSelect").innerHTML =  table;

  listar(id_usuario_sesion);
}
// funcion para listar el inventario actual 
async function listar(id_usuario_sesion) {
  
  const data = await apiRequest(`/productos/${id_usuario_sesion}/usuario`);
  //console.log(data)
  
  if (data && Array.isArray(data)) {
    // Agrupar los proveedores por producto
    const productosAgrupados = {};
    data.forEach(producto => {
      if (!productosAgrupados[producto.id_producto]) {
        productosAgrupados[producto.id_producto] = {
          id_producto: producto.id_producto,
          producto_nombre: producto.producto_nombre,
          descripcion: producto.descripcion,
          stock: producto.stock,
          proveedores: []
        };
      }
      productosAgrupados[producto.id_producto].proveedores.push(producto.proveedor_nombre);
    });

    // Generar filas para la tabla con los datos agrupados
    const rows = Object.values(productosAgrupados).map(producto => `
      <tr>
        <td>${producto.id_producto}</td>
        <td>${producto.producto_nombre}</td>
        <td>${producto.descripcion}</td>
        <td>${producto.stock}</td>
        <td>${producto.proveedores.join(", ")}</td>
      </tr>
    `).join("");

    // Insertar filas en el cuerpo de la tabla
    document.getElementById("tableBody_products").innerHTML = rows;

    // Inicializar DataTable
    $('#dataTable_products').DataTable({
      destroy: true, // Reinicia la tabla si ya existe
      paging: true,
      searching: true,
      info: false,
      responsive: true,
      footerCallback: function (row, data, start, end, display) {
        // Calcular la sumatoria del stock visible en la tabla
        const api = this.api();
        const sumatoria = api
          .column(3, { search: 'applied' }) // Columna de "Stock"
          .data()
          .reduce((total, stock) => total + parseFloat(stock || 0), 0);

        // Insertar la sumatoria en el pie de la tabla
        $(api.column(3).footer()).html(`Total de stock: ${sumatoria}`);
      },
      language: {
        search: "Filtrar producto:",
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "No se encontraron productos",
        infoEmpty: "No hay registros disponibles",
        infoFiltered: "(filtrado de _MAX_ registros totales)",
        paginate: {
          first: "Primero",
          last: "Último",
          next: "Siguiente",
          previous: "Anterior"
        }
      }
    });
  } else {
    document.getElementById("tableBody_products").innerHTML = `
      <tr>
        <td colspan="4">No se encontraron productos.</td>
      </tr>`;
  }
}
//fin para listar Inventario actual


 /////////////////////////////////////   


