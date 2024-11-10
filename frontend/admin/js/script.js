// Funciones para la seccion administrador


//-- Direccion de la api ----------------------------------------------

const urlAPI = "http://127.0.0.1:5001";


/////////////////////////////////////////////////////////-- Funciones compartidas entre opciones ------------------------------

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
  // Obtener valores de los campos del formulario
  const nombre = document.getElementById("producto").value.trim();
  const descripcion = document.getElementById("descripcion").value.trim();
  const precio = parseFloat(document.getElementById("precio").value);
  const stock = parseInt(document.getElementById("stock").value);
  const categoriaNombre = document.getElementById("categoria").value.trim(); // Obtener el nombre de la categoría
  const id_usuario = parseInt(document.getElementById("usuario").value);
  
  // Verificar que los campos numéricos sean válidos
  if (isNaN(precio) || isNaN(stock) || isNaN(id_usuario)) {
      alert("Por favor, revisa los campos numéricos.");
      return;
  }

  // Verificar que los campos de texto no estén vacíos
  if (!nombre || !descripcion || !categoriaNombre) {
      alert("Por favor, completa todos los campos.");
      return;
  }

  // Consultar las categorías existentes para obtener el id basado en el nombre
  try {
    const categorias = await apiRequest("/categorias", 'GET');
    
    // Buscar la categoría con el nombre ingresado
    const categoria = categorias.find(c => c.nombre.toLowerCase() === categoriaNombre.toLowerCase());

    if (!categoria) {
        alert(`La categoría "${categoriaNombre}" no existe.`);
        return;
    }

    // Crear el objeto nuevoProducto con los datos del formulario, usando el id_categoria obtenido
    const nuevoProducto = {
        nombre: nombre,
        descripcion: descripcion,
        precio: precio,
        stock: stock,
        id_categoria: categoria.id,  // Usar el id de la categoría encontrada
        id_usuario: id_usuario
    };

    // Consultar los productos existentes
    const productosExistentes = await apiRequest("/productos", 'GET');
    
    // Verificar si el producto ya existe en la lista de productos
    const productoExistente = productosExistentes.find(producto => producto.nombre.toLowerCase() === nombre.toLowerCase());
    if (productoExistente) {
        alert(`El producto "${nombre}" ya está en la lista.`);
        showAgregarProducto();
        return;  // Detener la ejecución si el producto ya existe
    }

    // Enviar los datos a la API
    const data = await apiRequest("/productos", 'POST', nuevoProducto);
    if (data) {
        alert("Producto agregado correctamente");
        
    }

  } catch (error) {
    console.error(error);
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

      // Si el producto existe, realizar la eliminación
      const data = await apiRequest(`/productos/${codigo}`, 'DELETE');
      if (data) {
         alert("Producto eliminado correctamente");
         console.log(data);
         showQuitarProducto();
         
      }

  } catch (error) {
      console.error(error);
      alert("Hubo un problema al eliminar el producto.");
  }
}


// Función para Actualizar Producto
function showActualizarProducto() {
  showHeader("Gestor de Productos", "Actualizar Producto");
  clearContent();
  generateForm(
      [
          { nombre: "codigo", placeholder: "Código", tipo: "number" },  // Código del producto
          { nombre: "producto", placeholder: "Producto", tipo: "text" },
          { nombre: "descripcion", placeholder: "Descripción", tipo: "text" },
          { nombre: "precio", placeholder: "Precio", tipo: "number" },
          { nombre: "stock", placeholder: "Stock", tipo: "number" },
          { nombre: "proveedor", placeholder: "Proveedor", tipo: "text" },
          { nombre: "categoria", placeholder: "Categoría", tipo: "text" }
      ],
      "updateProduct",  
      "updateProduct",
      "Actualizar",
      "btn-warning"
  );
}

async function updateProduct() {
  const codigo = document.getElementById("codigo").value.trim();  // Obtener código del producto
  const productoActualizado = {
      nombre: document.getElementById("producto").value.trim(),
      descripcion: document.getElementById("descripcion").value.trim(),
      precio: parseFloat(document.getElementById("precio").value),
      stock: parseInt(document.getElementById("stock").value),
      proveedor: document.getElementById("proveedor").value.trim(),
      categoria: document.getElementById("categoria").value.trim()
  };
  
  // Validación de campos
  if (isNaN(productoActualizado.precio) || isNaN(productoActualizado.stock)) {
      alert("Por favor, revisa los campos numéricos.");
      return;
  }

  if (!codigo || !productoActualizado.nombre || !productoActualizado.descripcion || !productoActualizado.proveedor || !productoActualizado.categoria) {
      alert("Por favor, completa todos los campos.");
      return;
  }

  try {
      // Enviar los datos a la API para actualizar el producto
      const data = await apiRequest(`/productos/${codigo}`, 'PUT', productoActualizado);
      if (data) {
          alert("Producto actualizado correctamente");
          // Aquí podrías agregar código para redirigir a la lista de productos o limpiar el formulario
          // showListarProducto(); // Descomenta si quieres listar productos después de actualizar
      }
  } catch (error) {
      console.error("Error al actualizar el producto:", error);
      alert("Hubo un problema al actualizar el producto.");
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
        alert("Categoria agregado correctamente");
        
    }
}

function showAsociarProducto(){
  showHeader("Gestor de Categoria","Asociar Producto");
  clearContent();
  generateForm(
    [
        { nombre: "proCategoria", placeholder: "Producto a asociar" },
        { nombre: "catProducto", placeholder: "Categoria" },
    ],
    "addProdCategoria",
    "addProductoCategoria",
    "Asociar",
    "btn-success"
  );
}

async function addProductoCategoria() {

}
  

//-- Gestor Stock -------------------------------------------------------

  function showActualizarStock(){
    showHeader("Gestor de Stock","Actualizar Stock");
    clearContent();
    
    
    // seguir codigo
  
  }
 
//////////////////////////////////////////////////////////////-- Gestor de provedores ------------------------------------------------
    
// Función para Agregar Proveedor
function showAgregarProveedor() {
  showHeader("Gestor de Proveedores", "Agregar Proveedor");
  clearContent();
  generateForm(
      [
          { nombre: "nombre", placeholder: "Nombre de proveedor" },
          { nombre: "direccion", placeholder: "Direccion" },
          { nombre: "email", placeholder: "email" },
          { nombre: "telefono", placeholder: "Telefono" },
          { nombre: "productos", placeholder: "Productos que provee (produto 1, producto 2,...)" }
      ],
      "addProveedor",
      "addProveedor",
      "Ingresar",
      "btn-success"
  );
}

async function addProveedor() {
  const nuevoProveedor = {
      code: document.getElementById("nombre").value,
      product: document.getElementById("direccion").value,
      description: document.getElementById("email").value,
      price: document.getElementById("telefono").value,
      stock: document.getElementById("productos").value
     
  };
  
  const data = await apiRequest("/proveedor", 'POST', nuevoProveedor);
  if (data) {
      alert("Proveedor agregado correctamente");
      
  }
}
//Función para Listar Proveedores----( para prueba)

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
  
  function showAgregarCompra(item){
      showHeader("Gestor de Compras","Agregar Compra");
      clearContent();
      
    // seguir codigo
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
  



  // Función para Listar Compras
  /*
  function showHCompras() {
    showHeader("Gestor de Reportes", "Historial de Compras");
    clearContent();
    const table = `
      <div class="card-body table-responsive p-0" style="height: 300px;">
        <table id="dataTable_products" class="table table-head-fixed text-nowrap">
          <thead>
            <tr>
              <th>Producto Solicitado</th>
              <th>Cantidad</th>
              <th>Fecha pedido</th>
              <th>Fecha recepcion</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody id="tableBody_products"></tbody>
        </table>
      </div>`;
  
    document.getElementById("showSelect").innerHTML = table;
    //fetchHCompras();
  }

  async function fetchHCompras() {
    const data = await apiRequest("/compras ");
    if (data && Array.isArray(data.compras)) {
        const shopping = data.compras;
        const content = shopping.map(buys => `
          <tr>
            <td>${buys[0]}</td>
            <td>${buys[1]}</td>
            <td>${buys[2]}</td>
            <td>${buys[3]}</td>
            <td>${buys[4]}</td>
          </tr>
        `).join("");
        document.getElementById("tableBody_products").innerHTML = content;
    }
  }
  */
  






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

