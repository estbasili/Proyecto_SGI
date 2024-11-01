// static/js/script.js

// Validación de formulario de login
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


// Función para mostrar encabezados
function showHeader(nameSection, nameSubSection) {
    document.getElementById("section").textContent = nameSection;
    document.getElementById("subSection").textContent = nameSubSection;
  }
  
  // Función para limpiar el contenido de showSelect
  function showOut() {
    const elementoAEliminar = document.getElementById("showSelect");
    if (elementoAEliminar) {
        elementoAEliminar.innerHTML = "";
    }
  }
  
  // Función para generar formularios dinámicamente
  function formulario(campos, idFormulario,method, botonTexto, botonClase) {
    let form = `<div class="card-body">
        <form id="${idFormulario}" action="" method="${method}">`;
  
    campos.forEach(campo => {
        form += `<div class="input-group mb-3">
            <input type="text" name="${campo.nombre}" required class="form-control" placeholder="${campo.placeholder}" value="">
            <div class="input-group-append">
                <div class="input-group-text">
                    <span class="fas fa-align-left"></span>
                </div>
            </div>
        </div>`;
    });
  
    form += `
        <hr>
        <div class="row">
            <div class="col-12">
                <button type="submit" class="btn ${botonClase} btn-block">${botonTexto}</button>
            </div>
        </div>
        </form>
    </div>`;
  
    document.getElementById("showSelect").innerHTML = form;
  }
  
  // Función para mostrar pantalla "Agregar Producto"
  function showAgregarProducto() {
    showHeader("Gestor de Productos", "Agregar Producto");
    showOut();
    formulario(
        [
            { nombre: "Codigo", placeholder: "codigo" },
            { nombre: "producto", placeholder: "producto" },
            { nombre: "descripción", placeholder: "descripción"},
            { nombre: "precio", placeholder: "precio" },
            { nombre: "stock", placeholder: "stock" },
            { nombre: "provedor", placeholder: "provedor"},
            { nombre: "categoria", placeholder: "categoria"}
        ],
        "addProduct",
        "POST",
        "Ingresar",
        "btn-success"
    );
  }
  
  // Función para mostrar pantalla "Quitar Producto"
  function showQuitarProducto() {
    showHeader("Gestor de Productos", "Quitar Producto");
    showOut();
    formulario(
        [
            { nombre: "codigo", placeholder: "codigo"},
            { nombre: "producto", placeholder: "producto"}
        ],
        "quitProduct",
        "DELETE",
        "Quitar",
        "btn-danger"
    );
  }
  
  // Función para mostrar pantalla "Actualizar Producto"
  function showActualizarProducto() {
    showHeader("Gestor de Productos", "Actualizar Producto");
    showOut();
    formulario(
        [
            { nombre: "Codigo", placeholder: "codigo"},
            { nombre: "producto", placeholder: "producto"},
            { nombre: "descripción", placeholder: "descripción"},
            { nombre: "precio", placeholder: "precio"},
            { nombre: "stock", placeholder: "stock"},
            { nombre: "provedor", placeholder: "provedor"},
            { nombre: "categoria", placeholder: "categoria"}
        ],
        "updateProduct",
        "PUT",
        "Actualizar",
        "btn-warning"
    );
  }
  
      
  function showListarProducto(){
      showHeader("Gestor de Productos"," Lista Productos");
      showOut();
      let table = ` <!-- Table -->
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
                            <th>Provedor</th>
                          </tr>
                        </thead>
                        <tbody id="tableBody_products"></tbody>
                      </table>
                    </div>
                    <!--/ Table-->`;  
      
      showSelect.innerHTML= table;
      
      /*const listProducts = async()=>{
        try{
          const response = await fetch("http://127.0.0.1:5001/productos")
          const products= await response.json();
          let content = ``; //  en esta variable se guarda el contenido que se va a escribir en la tabla
          products.forEach((product,index) => {
            content+= `<tr>
                          <td>${product.id}</td>
                          <td>${product.nombre}</td>
                          <td>${product.descripcion}</td>
                          <td>${product.precio}</td> 
                          <td>${product.stock}</td>
                          <td>${product.categoria}</td> 
                          <td>${product.provedor}</td> 
                       </tr>`; 
                      });
          tableBody_products.innerHTML = content;
        
        }
        catch(ex) {
          alert(ex);
        }
      };*/

      const listProducts = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5001/productos");
            const data = await response.json();
    
            // Asegúrate de que `data.productos` es un arreglo
            let products = Array.isArray(data.productos) ? data.productos : [];
    
            // Genera el contenido de la tabla utilizando los índices de cada subarreglo
            let content = ""; 
            products.forEach((product) => {
                content += `<tr>
                              <td>${product[0]}</td>
                              <td>${product[1]}</td>
                              <td>${product[2]}</td>
                              <td>${product[3]}</td>
                              <td>${product[4]}</td>
                              <td>${product[5]}</td>
                              <td>${product[6]}</td>
                            </tr>`;
            });
    
            tableBody_products.innerHTML = content;
        } catch (ex) {
            console.error("Error al listar los productos:", ex);
            alert("Error al obtener la lista de productos. Por favor, intenta de nuevo.");
        }
      };  
      
    listProducts();
  
  }
  
  //----- Pantallas Gestor Categoria
  
  function showNuevaCategoria(){
      showHeader("Gestor de Categoria","Agregar Categoria");
      showOut();
      formulario(
        [
            { nombre: "nuevaCategoria", placeholder: "Nueva Categoria" },
        ],
        "addCategory",
        "POST",
        "Ingresar",
        "btn-success"
    );
      
    // seguir codigo
  }
  
  //---------Pantalla Gestor Stock
  function showActualizarStock(){
    showHeader("Gestor de Stock","Actualizar Stock");
    showOut();
    
    
    // seguir codigo
  
  }
  function showListarStock(){
    showHeader("Gestor de Stock"," Lista Stock");
    showOut();
  
    // seguir codigo
  
  }
  
  //-------- Pantalla Gestor de provedores
  function showAgregarProvedor(){
      showHeader("Gestor de Provedores","Agregar Provedor");
      showOut();
      
    // seguir codigo
  }
  
  function showConsultarProvedor(){
    showHeader("Gestor de Provedor","Lista Provedor");
    showOut();
  
    // seguir codigo
  
  }
  
  //----- Pantalla gestor de compras
  
  function showAgregarCompra(item){
      showHeader("Gestor de Compras","Agregar Compra");
      showOut();
      
    // seguir codigo
  }
  
  function showConsultarCompra(){
    showHeader("Gestor de Compras","Consultar Compra");
    showOut();
  
    // seguir codigo
  
  }
  
  //--------- Pantalla de Gestionar usuario
  
  function gestionarUsuario(){
      showHeader("Gestor de Usuario","Agregar Usuario");
      showOut();
  }

