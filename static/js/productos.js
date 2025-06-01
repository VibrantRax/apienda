document.addEventListener("DOMContentLoaded", () => {
    fetch('/product')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("productos-container");
            data.forEach(productos => {
                // Solo mostrar juegos activos
                if (productos.ProductoStatus !== "A") return;

                // Convertimos el nombre del videojuego a formato de imagen
                const nombreImagen = productos.ProductoNombre
                    .toLowerCase()
                    .replace(/\s+/g, '_')   // Espacios por guiones bajos
                    .replace(/[^\w_]/g, ''); // Elimina caracteres no válidos

                const imagenSrc = `/static/img/productos/${nombreImagen}.jpg`;

                const card = document.createElement("div");
                card.className = "col-md-3 d-flex justify-content-center mb-4";
                card.innerHTML = `
                    <div class="card h-100" style="width: 18rem;">
                        <img src="${imagenSrc}" class="card-img-top imagen-ajustada" alt="${productos.ProductoNombre}" onerror="this.onerror=null;this.src='/static/img/default.jpg';">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${productos.ProductoNombre}</h5>
                            <p class="card-text">${productos.ProductoDescripcion}</p>
                            <p class="card-text precio"><strong>$${productos.ProductoPrecio}</strong></p>
                            <a href="/ver_producto/${productos.ProductoID}" class="btn btn-success mt-auto">Ver</a>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error("Error al obtener los juegos:", error);
        });
});