document.addEventListener("DOMContentLoaded", () => {
    fetch('/gamescard')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("juegos-container");
            data.forEach(videojuego => {
                // Convertimos el nombre del videojuego a formato de imagen
                const nombreImagen = videojuego.VideojuegoNombre
                    .toLowerCase()
                    .replace(/\s+/g, '_')   // Espacios por guiones bajos
                    .replace(/[^\w_]/g, ''); // Elimina caracteres no válidos


                const imagenSrc = `/static/img/juegos/${nombreImagen}.jpg`;

                const card = document.createElement("div");
                card.className = "col-md-4 d-flex justify-content-center mb-4";
                card.innerHTML = `
                    <div class="card h-100" style="width: 18rem;">
                        <img src="${imagenSrc}" class="card-img-top imagen-ajustada" alt="${videojuego.VideojuegoNombre}" onerror="this.onerror=null;this.src='/static/img/default.jpg';">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${videojuego.VideojuegoNombre}</h5>
                            <p class="card-text">${videojuego.VideojuegoDescripcion}</p>
                            <a href="/ver_juego/${videojuego.VideojuegoID}" class="btn btn-success mt-auto">Ver</a>
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
