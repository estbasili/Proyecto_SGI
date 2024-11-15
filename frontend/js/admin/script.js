// Funciones para la seccion administrador

//-- fecha y hora ----------------------------------------------------
function actualizarFecha() {
  const fecha = new Date();
  const opciones = { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
  const fechaFormateada = fecha.toLocaleDateString('es-ES', opciones);   

  document.getElementById('fecha').textContent = fechaFormateada;
}

actualizarFecha(); // Llama a la función al cargar la página
setInterval(actualizarFecha, 1000); // Actualiza cada segundo

//-- Direccion de la api ----------------------------------------------

const urlAPI = "http://127.0.0.1:5001";


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

/*// Función para generar formularios dinámicos (anda)
function generateForm(fields, formId, submitCallback, submitText, submitClass) {
  const form = `
    <div class="card-body">
      <form id="${formId}" onsubmit="event.preventDefault(); ${submitCallback}();">
        ${fields.map(field => `
          <div class="input-group mb-3">
              <input type="text" id="${field.nombre}" name="${field.nombre}" required class="form-control" placeholder="${field.placeholder}" value="" >
              <div class="input-group-append">
                  <div class="input-group-text">
                      <span class="fas fa-align-left"></span>
                  </div>
              </div>
          </div>
        `).join('')}
        <hr>
        <div class="row">
            <div class="col-12">
                <button type="submit" class="btn ${submitClass} btn-block">${submitText}</button>
            </div>
        </div>
      </form>
    </div>`;
  document.getElementById("showSelect").innerHTML = form;
}*/
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
          'Content-Type': 'application/json'
      },
      body: data ? JSON.stringify(data) : null
  };
  
  try {
      const response = await fetch(`${urlAPI}${endpoint}`, options);
      
      // Manejar error 404 de forma específica
      if (response.status === 404) {
          throw new Error("Producto no encontrado");
      }  
      // Manejo respuesta no exitosa
      if (!response.ok) {
          throw new Error("Error en la solicitud: ${response.status}");
      }
      // Manejo si el codigo de estado es 204 (sin contenido)
      if(response.status === 204) {
        return{};
      }
      
      // si hay contenido en la rspuesta, devuelvo JSON
      return await response.json();
      
  } catch (error) {
      console.error(`Error en ${method} ${endpoint}:`, error);
      alert(`Error al procesar la solicitud: ${error.message}`);
  }
}



////////////////////////////////////////////////////////////-- Gestor de Productos -----------------------------------------------


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
            { nombre: "categoria", placeholder: "Categoría" },
            { nombre: "usuario", placeholder: "ID Usuario" } 
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
  const id_usuario = parseInt(document.getElementById("usuario").value);
  
  if (isNaN(precio) || isNaN(stock) || isNaN(id_usuario)) {
      alert("Por favor, revisa los campos numéricos.");
      return;
  }

  if (!nombre || !descripcion || !categoriaNombre) {
      alert("Por favor, completa todos los campos.");
      return;
  }

  try {
    // Consultar las categorías existentes
    const categorias = await apiRequest("/categorias", 'GET');

    if (!categorias || categorias.length === 0) {
        console.error("No se encontraron categorías en la respuesta de la API.");
        alert("No se encontraron categorías disponibles.");
        return;
    }
    
    // Imprimir las categorías obtenidas para verificar
    console.log("Categorías obtenidas:", categorias);

    // Buscar la categoría con el nombre ingresado
    const categoria = categorias.find(c => c.nombre && c.nombre.toLowerCase() === categoriaNombre.toLowerCase());

    if (!categoria) {
        alert(`La categoría "${categoriaNombre}" no existe en el sistema.`);
        return;
    }

    // Crear el objeto nuevoProducto con el id_categoria correcto
    const nuevoProducto = {
        nombre: nombre,
        descripcion: descripcion,
        precio: precio,
        stock: stock,
        id_categoria: categoria.id_categoria,  // Usar id_categoria de la API
        id_usuario: id_usuario
    };

    if (nuevoProducto.id_categoria === undefined) {
        console.error("Error: id_categoria sigue siendo undefined después de la búsqueda.");
        alert("Error interno: el ID de la categoría no se obtuvo correctamente.");
        return;
    }

    console.log("Datos a enviar:", nuevoProducto);

    // Enviar los datos a la API
    const data = await apiRequest("/productos", 'POST', nuevoProducto);
    if (data) {
        alert("Producto agregado correctamente");
    }

  } catch (error) {
    console.error("Error en el proceso de adición de producto:", error);
    alert("Hubo un problema al verificar las categorías o al agregar el producto.");
  }

  showAgregarProducto();
}

// Función para Eliminar Producto ( envia el id falta el delete en el back)
function showQuitarProducto() {
  showHeader("Gestor de Productos", "Eliminar Producto");
  clearContent();
  generateForm(
      [{ nombre: "idProduct", placeholder: "ID del producto a eliminar" }],
      "deleteProduct",
      "deleteProduct",
      "Eliminar",
      "btn-danger"
  );
}

async function deleteProduct() {
  const codigo = document.getElementById("idProduct").value.trim();  // Obtener el ID del producto
  

  // Verificar si el producto existe antes de intentar eliminarlo
  try {
      const producto = await apiRequest(`/productos/${codigo}`, 'GET');  // Consultar si el producto existe
      if (!producto) {
          alert(`No se encontró un producto con el ID ${codigo}.`);
          return;  // Detener si el producto no existe
      }
      console.log(codigo); 
      // Si el producto existe, realizar la eliminación
      const data = await apiRequest(`/productos/${codigo}`, 'DELETE');
      if (data) {
         alert("Producto eliminado correctamente");
         showQuitarProducto();
         
      }

  } catch (error) {
      console.error(error);
      alert("Hubo un problema al eliminar el producto.");
  }
}

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
      alert("Por favor, ingresa el código del producto.");
      return;
  }

  try {
      // Solicitar los datos del producto a la API
      const producto = await apiRequest(`/productos/${codigo}`, 'GET');

      if (producto) {
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
      }
  } catch (error) {
      if (error.message === 'Producto no encontrado') {
          alert("El producto con el código especificado no existe.");
      } else {
          console.error("Error al buscar el producto:", error);
          alert("Hubo un problema al buscar el producto.");
      }
  }
}

// Función para obtener las categorías desde la API
async function getCategorias() {
  // Obtener categorías desde la API
  const categorias = await apiRequest('/categorias', 'GET');
  return categorias.map(categoria => ({
    value: categoria.id_categoria,
    text: categoria.nombre
  }));
}
/*
// Función para generar el formulario de actualización
function generateSelectField(field) {
  return `
    <div class="input-group mb-3">
      <select id="${field.nombre}" name="${field.nombre}" class="form-control">
        <option value="">${field.placeholder}</option>
        ${field.opciones.map(opcion => `
          <option value="${opcion.value}" ${field.value === opcion.value ? 'selected' : ''}>
            ${opcion.text}
          </option>
        `).join('')}
      </select>
    </div>
  `;
}
*/
// Función para actualizar el producto
async function updateProduct() {
  const codigo = document.getElementById("codigo").value.trim();

  // Verificar si el ID del producto existe
  if (!codigo) {
      alert("Por favor, ingresa el código del producto.");
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
      id_usuario: 10 //////////////////////////////////// // Este valor debe corresponder al ID del usuario autenticado o elejir de una lista desplegable
  };

  // Verificar si los campos numéricos son válidos
  if (isNaN(productoActualizado.precio) || isNaN(productoActualizado.stock) || isNaN(productoActualizado.id_categoria) || isNaN(productoActualizado.id_usuario)) {
      alert("Por favor, revisa los campos numéricos.");
      return;
  }

  // Verificar si los campos requeridos están completos
  if (!productoActualizado.nombre || !productoActualizado.descripcion || !productoActualizado.id_categoria || !productoActualizado.id_usuario) {
      alert("Por favor, completa todos los campos.");
      return;
  }

  // Ver el contenido de productoActualizado en la consola para depurar
  // console.log("Contenido de productoActualizado:", productoActualizado.precio);

  try {
      // Enviar los datos a la API para actualizar el producto
      const data = await apiRequest(`/productos/${codigo}`, 'PUT', productoActualizado);
      if (data) {
          alert("Producto actualizado correctamente");
      }
  } catch (error) {
      console.error("Error al actualizar el producto:", error);
      alert("Hubo un problema al actualizar el producto.");
  }
}
// fin funcion atualizar producto


///////////////////////////////////////////////////////////////////-- Gestor Categoria ---------------------------------------------------


// Agregar nueva categoria (anda)
// Mostrar el formulario y cargar categorías existentes
async function showNuevaCategoria() {
  showHeader("Gestor de Categoría", "Agregar Categoría");
  clearContent();
  
  // Obtener las categorías y generar el formulario
  const categorias = await apiRequest("/categorias", "GET");
  generateForm(
      [{ nombre: "nuevaCategoria", placeholder: "Ingrese nueva Categoría" }],
      "addCategory",
      "addCategory",
      "Ingresar",
      "btn-success"
  );
  
  // Almacenar las categorías en un atributo de dataset para la validación
  document.getElementById("addCategory").dataset.categorias = JSON.stringify(categorias || []);
}

// Función para agregar categoría, solo si no existe previamente
async function addCategory() {
  const inputElement = document.getElementById("nuevaCategoria");
  const nuevaCategoriaNombre = inputElement.value.trim();
  const categoriasExistentes = JSON.parse(document.getElementById("addCategory").dataset.categorias);

  // Verificar si la categoría ya existe en la lista cargada
  if (categoriasExistentes.some(cat => cat.nombre.toLowerCase() === nuevaCategoriaNombre.toLowerCase())) {
      alert("La categoría ya existe.");
      inputElement.value = "";  // Limpiar el campo de entrada
      return;
  }

  // Hacer la solicitud POST para agregar la categoría
  const data = await apiRequest("/categorias", 'POST', { nombre: nuevaCategoriaNombre });
  if (data) {
      alert("Categoría agregada correctamente");
      inputElement.value = "";  // Limpiar el campo de entrada después de agregar
      showNuevaCategoria();  // Recargar el formulario y categorías
  }
}
// fin agregra categoria

// Asociacion de categoria a producto (anda)
// Función para mostrar el formulario de asociación de categoría a producto
async function showAsociarCategoriaProducto() {
  try {
      showHeader("Asociar Categoría a Producto", "Seleccione el producto y la categoría");
      clearContent();

      // Obtener productos y categorías de la API
      const [productos, categorias] = await Promise.all([
          apiRequest("/productos", "GET"),
          apiRequest("/categorias", "GET")
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
      alert(error.message);
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
      const producto = await apiRequest(`/productos/${productoId}`, "GET");

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
      const data = await apiRequest(`/productos/${productoId}`, "PUT", nuevaCategoriaProducto);

      if (data) {
          alert("Producto actualizado correctamente.");
          document.getElementById("associateForm").reset(); // Limpia el formulario después de asociar
      } else {
          throw new Error("Error al actualizar el producto.");
      }
  } catch (error) {
      alert(error.message);
  }
}
// fin de Asociacion


///////////////////////////////////////////////////////////////////-- Gestor Stock -------------------------------------------------------

// Función principal para mostrar el formulario de actualización de stock (revisar problema si no se encuentra el codigo)
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
    alert("Por favor, ingresa el código del producto.");
    return;
  }

  try {
    // Solicitar los datos del producto a la API
    const producto = await apiRequest(`/productos/${codigo}`, 'GET');

    if (!producto) {
      alert("Producto no encontrado.");
      return;
    }

    // Almacena los datos del producto
    productoActual = { ...producto, precio: parseFloat(producto.precio) };
    mostrarFormularioActualizarStock(productoActual);

  } catch (error) {
    console.error("Error al buscar el producto:", error);

    // Verificar si el error es un 404
    if (error.response && error.response.status === 404) {
      alert("Producto no encontrado.");
    } else {
      alert("Hubo un problema al buscar el producto.");
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
    alert("Por favor, ingresa una cantidad de stock válida.");
    return;
  }

  productoActual.stock = stock; // Actualizar el stock en el objeto completo del producto

  try {
    const data = await apiRequest(`/productos/${productoActual.id_producto}`, 'PUT', productoActual);
    if (data) {
      alert("Stock actualizado correctamente");
      showActualizarStock();
    }
  } catch (error) {
    console.error("Error en PUT /productos:", error);
    alert("Hubo un problema al actualizar el producto.");
  }
}
// fin de gestir actualizacion stock

// Notificaciones de producto bajo stock y si genera una lista de los productos bajo stock (anda)
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
      const productos = await apiRequest("/productos");

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
    }
  }

  // Función para renderizar productos de bajo stock en el menú de notificaciones
  function renderLowStockMenuItems(productos, limit) {
    const stockItemsContainer = document.getElementById("low-stock-items");
    stockItemsContainer.innerHTML = ""; // Limpia el contenido previo

    if (productos.length === 0) {
      stockItemsContainer.innerHTML = "<p class='dropdown-item text-muted'>No hay productos con stock mínimo.</p>";
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
      document.getElementById("stock-badge").textContent = productos.length;
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



//////////////////////////////////////////////////////////////-- Gestor de proveedores ------------------------------------------------
 
// Función para Agregar Proveedor (anda falta validar campo telefono para que sea un numero que luego se combierta en str)
async function showAgregarProveedor() {
  showHeader("Gestor de Proveedores", "Agregar Proveedor y Asociar productos");
  clearContent();
  const usuarios = await getUsuarios(); // Obtener los usuarios para el campo select

  generateForm(
      [
          { nombre: "nombre", placeholder: "Nombre de proveedor" },
          { nombre: "email", placeholder: "Email" },
          { nombre: "telefono", placeholder: "Teléfono" },
          { nombre: "usuario", placeholder: "Usuario", tipo: "select", opciones: usuarios }, // Campo select para usuario
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
      id_usuario: parseInt(document.getElementById("usuario").value, 10)
  };

  if (isNaN(nuevoProveedor.id_usuario)) {
    alert("Por favor, selecciona un usuario válido.");
    return;
  }

  const data = await apiRequest("/proveedores", 'POST', nuevoProveedor);
  if (data) {
      alert("Proveedor agregado correctamente");
      console.log(data[0].id_proveedor);
        // Ahora que el proveedor ha sido creado, mostrar la tabla para asociar productos
      await showAsociarProductos(data[0].id_proveedor); // Mostrar productos para asociar
  }
}

// muestra la table para selleccionar los productoa asociados al proveedor
async function showAsociarProductos(idProveedor) {
  clearContent();
  const productos = await apiRequest("/productos", 'GET');  // Obtener productos disponibles
  
  // Selecciona el contenedor con id="showSelect"
  const container = document.getElementById("showSelect");

  // Limpia el contenido previo en el contenedor
  container.innerHTML = "";

  // Crear una tabla con DataTables
  const table = document.createElement("table");
  table.setAttribute("id", "productosTable");
  table.classList.add("display", "table", "table-striped", "table-bordered");  // Clases para estilo Bootstrap

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
    alert("Por favor, selecciona al menos un producto.");
    return;
  }

  // Enviar los productos seleccionados a la API para asociarlos con el proveedor
  const data = await apiRequest(`/proveedores/${idProveedor}/productos/varios`, 'POST', { productos: selectedProductos });

  if (data) {
    alert("Productos asociados al proveedor correctamente");
  } else {
    alert("Hubo un error al asociar los productos al proveedor.");
  }
}
// fin para Agregar proveeedor



//Función para consultar los provedores asociados a productos especificos 

function showConsultarProveedor() {
    showHeader("Gestor de Proveedores", "Consultar Proveedor");
    clearContent();
    const table = `
      <div class="card-body table-responsive p-0" style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>idProveedor</th>
              <th>Nombre</th>
              <th>Telefono</th>
              <th>email</th>
              <th>idUsuario</th>
              
            </tr>
          </thead>
          <tbody id="tableBody_products"></tbody>
        </table>
      </div>`;
    
    document.getElementById("showSelect").innerHTML = table;
    fetchProveedor();
}

async function fetchProveedor() {
    const data = await apiRequest("/proveedores");
    if (data && Array.isArray(data.proveedores)) {
        const proveedors = data.provedores;
        const content = proveedors.map(proveedor => `
          <tr>
            <td>${proveedor[0]}</td>
            <td>${proveedor[1]}</td>
            <td>${proveedor[2]}</td>
            <td>${proveedor[3]}</td>
            <td>${proveedor[4]}</td>
            
          </tr>
        `).join("");
        document.getElementById("tableBody_products").innerHTML = content;
    }
}



  
////////////////////////////////////////////////////////////////-- Gestor de compras ---------------------------------------------------
////////// hacer  

function generarFormOrdenCompra(){
  const form = `
    <div class="card-body">
      <form id="form_orden_compra" onsubmit="event.preventDefault();">
        <div class="row">
          <div class="col-12">
            <!-- Label para el select -->
            <label for="proveedor">Seleccionar Proveedor:</label>
            <select id="proveedores" name="proveedor" class="form-control">
              <option value="">Cargando proveedores...</option> <!-- Opción por defecto mientras carga -->
            </select>
          </div>
          <div class="col-12">
            <!-- Botón de submit -->
            <button type="submit" class="btn btn-primary btn-block">Enviar</button>
          </div>
        </div>
      </form>
    </div>`;
  document.getElementById("showSelect").innerHTML = form;

  // Llamamos a la función para cargar los proveedores después de generar el formulario
  loadProveedoresSelect();
}

function loadProveedoresSelect(){
  // Función para cargar los proveedores desde la API
  fetch('http://127.0.0.1:5001/listarProveedores')
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
        console.log('Proveedor seleccionado ID:', selectedId);
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

  // Función para Listar Productos  con limite de stock (anda)
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
      <div class="card-body table-responsive p-0" style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>Id</th>
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
    fetchProducts(initialStockThreshold);
  }
  // Función que se llama al hacer clic en el botón "Aplicar"
  function establecerStock() {
    const stockThreshold = parseInt(document.getElementById("stockThresholdInput").value, 10);
    fetchProducts(stockThreshold);
  }
  // Peticion a la API
  async function fetchProducts(stockThreshold) {
    const data = await apiRequest("/productos");
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




 /////////////////////////////////////   

/*
// ! Validación de formulario de login--- en revision
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('#loginForm');
  if (loginForm) {
      loginForm.addEventListener('submit', function(event) {
          const email = document.querySelector('#email').value;
          const password = document.querySelector('#password').value;
          
          if (!email || !password) {
              event.preventDefault();
              alert('Por favor complete todos los campos.');
          }
      });
  }
});
*/
