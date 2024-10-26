function encabezado(nameSection,nameSubSection){
    let section = document.getElementById("section");
    section.textContent= nameSection;
    let subsection = document.getElementById("subSection");
    subsection.textContent= nameSubSection;

}

// ------ Pantallas Producto
function showAgregarProducto(){
      encabezado("Gestor de Productos","Agregar Producto");
      
    // seguir codigo
}
function showQuitarProducto(){
    encabezado("Gestor de Productos","Quitar Producto");
    
    // seguir codigo

}
function showActualizarProducto(){
    encabezado("Gestor de Productos","Actualizar Producto");
    
    // seguir codigo

}
function showListarProducto(){
    encabezado("Gestor de Productos"," Lista Productos");

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
    
    const listProducts = async()=>{
      try{
        const response = await fetch("https://6715928633bc2bfe40ba9bc2.mockapi.io/Productos/Productos")
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
    };
    
  listProducts();


}

//----- Pantallas Gestor Categorioa

function showNuevaCategoria(){
    encabezado("Gestor de Categoria","Agregar Categoria");
    
  // seguir codigo
}

//---------Pantalla Gestor Stock
function showActualizarStock(){
  encabezado("Gestor de Stock","Actualizar Stock");
  
  // seguir codigo

}
function showListarStock(){
  encabezado("Gestor de Stock"," Lista Stock");

  // seguir codigo

}

//-------- Pantalla Gestor de provedores
function showAgregarProvedor(){
    encabezado("Gestor de Provedores","Agregar Provedor");
    
  // seguir codigo
}

function showConsultarProvedor(){
  encabezado("Gestor de Provedor","Lista Provedor");

  // seguir codigo

}

//----- Pantalla gestor de compras

function showAgregarCompra(item){
    encabezado("Gestor de Compras","Agregar Compra");
    
  // seguir codigo
}

function showConsultarCompra(){
  encabezado("Gestor de Compras","Consultar Compra");

  // seguir codigo

}

//--------- Pantalla de Gestionar usuario

function gestionarUsuario(){
    encabezado("Gestor de Usuario","Agregar Usuario");
}