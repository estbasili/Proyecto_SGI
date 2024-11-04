// Funciones para la seccion administrador


//-- Direccion de la api ----------------------------------------------

const urlAPI = "http://127.0.0.1:5001";


//-- Funciones compartidas entre opciones ------------------------------

// Función genérica para mostrar encabezados
function showHeader(nameSection, nameSubSection) {
  document.getElementById("section").textContent = nameSection;
  document.getElementById("subSection").textContent = nameSubSection;
}

// Función para limpiar el contenido de showSelect
function clearContent() {
  document.getElementById("showSelect").innerHTML = "";
}

// Función para generar formularios dinámicos
function generateForm(fields, formId, submitCallback, submitText, submitClass) {
  const form = `
    <div class="card-body">
      <form id="${formId}" onsubmit="event.preventDefault(); ${submitCallback}();">
        ${fields.map(field => `
          <div class="input-group mb-3">
              <input type="text" id="${field.nombre}" name="${field.nombre}" required class="form-control" placeholder="${field.placeholder}" value="">
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
}

// Función genérica para hacer peticiones a la API
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
      if (!response.ok) throw new Error("Error en la solicitud");
      return await response.json();
  } catch (error) {
      console.error(`Error en ${method} ${endpoint}:`, error);
      alert(`Error al procesar la solicitud: ${error.message}`);
  }
}


//-- Gestor de Productos -----------------------------------------------


// Función para Agregar Producto
function showAgregarProducto() {
    showHeader("Gestor de Productos", "Agregar Producto");
    clearContent();
    generateForm(
        [
            { nombre: "codigo", placeholder: "Código" },
            { nombre: "producto", placeholder: "Producto" },
            { nombre: "descripcion", placeholder: "Descripción" },
            { nombre: "precio", placeholder: "Precio" },
            { nombre: "stock", placeholder: "Stock" },
            { nombre: "proveedor", placeholder: "Proveedor" },
            { nombre: "categoria", placeholder: "Categoría" }
        ],
        "addProduct",
        "addProduct",
        "Ingresar",
        "btn-success"
    );
}

async function addProduct() {
    const nuevoProducto = {
        code: document.getElementById("codigo").value,
        product: document.getElementById("producto").value,
        description: document.getElementById("descripcion").value,
        price: document.getElementById("precio").value,
        stock: document.getElementById("stock").value,
        supplier: document.getElementById("proveedor").value,
        category: document.getElementById("categoria").value
    };
    
    const data = await apiRequest("/producto", 'POST', nuevoProducto);
    if (data) {
        alert("Producto agregado correctamente");
        showListarProducto();
    }
}

// Función para Eliminar Producto
function showQuitarProducto() {
    showHeader("Gestor de Productos", "Eliminar Producto");
    clearContent();
    generateForm(
        [{ nombre: "codigo", placeholder: "Código del producto a eliminar" }],
        "deleteProduct",
        "deleteProduct",
        "Eliminar",
        "btn-danger"
    );
}

async function deleteProduct() {
    const codigo = document.getElementById("codigo").value;
    const data = await apiRequest(`/producto/${codigo}`, 'DELETE');
    if (data) alert("Producto eliminado correctamente");
}

// Función para Actualizar Producto
function showActualizarProducto() {
    showHeader("Gestor de Productos", "Actualizar Producto");
    clearContent();
    generateForm(
        [
            { nombre: "codigo", placeholder: "Código" },
            { nombre: "producto", placeholder: "Producto" },
            { nombre: "descripcion", placeholder: "Descripción" },
            { nombre: "precio", placeholder: "Precio" },
            { nombre: "stock", placeholder: "Stock" },
            { nombre: "proveedor", placeholder: "Proveedor" },
            { nombre: "categoria", placeholder: "Categoría" }
        ],
        "updateProduct",
        "updateProduct",
        "Actualizar",
        "btn-warning"
    );
}

async function updateProduct() {
    const codigo = document.getElementById("codigo").value;
    const productoActualizado = {
        product: document.getElementById("producto").value,
        description: document.getElementById("descripcion").value,
        price: document.getElementById("precio").value,
        stock: document.getElementById("stock").value,
        supplier: document.getElementById("proveedor").value,
        category: document.getElementById("categoria").value
    };
    
    const data = await apiRequest(`/producto/${codigo}`, 'PUT', productoActualizado);
    if (data) {
        alert("Producto actualizado correctamente");
        showListarProducto();
    }
}

// Función para Listar Productos
function showListarProducto() {
    showHeader("Gestor de Productos", "Lista de Productos");
    clearContent();
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
              <th>Proveedor</th>
            </tr>
          </thead>
          <tbody id="tableBody_products"></tbody>
        </table>
      </div>`;
    
    document.getElementById("showSelect").innerHTML = table;
    fetchProducts();
}

async function fetchProducts() {
    const data = await apiRequest("/productos");
    if (data && Array.isArray(data.productos)) {
        const products = data.productos;
        const content = products.map(product => `
          <tr>
            <td>${product[0]}</td>
            <td>${product[1]}</td>
            <td>${product[2]}</td>
            <td>${product[3]}</td>
            <td>${product[4]}</td>
            <td>${product[5]}</td>
            <td>${product[6]}</td>
          </tr>
        `).join("");
        document.getElementById("tableBody_products").innerHTML = content;
    }
}


//-- Gestor Categoria ---------------------------------------------------

function showNuevaCategoria(){
      showHeader("Gestor de Categoria","Agregar Categoria");
      clearContent();
      generateForm(
        [
            { nombre: "nuevaCategoria", placeholder: "Ingrese nueva Categoría" },
        ],
        "addCategory",
        "addCategory",
        "Ingresar",
        "btn-success"
    );
}

async function addCategory() {
    const nuevaCategoria = {
        category: document.getElementById("nuevaCategoria").value
    };
    
    const data = await apiRequest("/categoria", 'POST', nuevaCategoria);
    if (data) {
        alert("Producto agregado correctamente");
        showListarProducto();
    }
}
  

//-- Gestor Stock -------------------------------------------------------

  function showActualizarStock(){
    showHeader("Gestor de Stock","Actualizar Stock");
    clearContent();
    
    
    // seguir codigo
  
  }
  function showListarStock(){
    showHeader("Gestor de Stock"," Lista Stock");
    clearContent();
  
    // seguir codigo
  
  }
  
//-- Gestor de provedores ------------------------------------------------
  function showAgregarProveedor(){
      showHeader("Gestor de Proveedores","Agregar Proveedor");
      clearContent();
      
    // seguir codigo
  }
  
  function showConsultarProveedor(){
    showHeader("Gestor de Proveedores","Lista Proveedor");
    clearContent();
  
    // seguir codigo
  
  }
  
//-- Gestor de compras ---------------------------------------------------
  
  function showAgregarCompra(item){
      showHeader("Gestor de Compras","Agregar Compra");
      clearContent();
      
    // seguir codigo
  }
  
  function showConsultarCompra(){
    showHeader("Gestor de Compras","Consultar Compra");
    clearContent();
  
    // seguir codigo
  
  }
  
//-- Gestor usuario ------------------------------------------------------
  
  function gestionarUsuario(){
      showHeader("Gestor de Usuario","Agregar Usuario");
      clearContent();
  }



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

