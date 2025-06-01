$(document).ready(function () {
    // Cargar productos y categorías al inicio
    loadVideojuegos();
    loadPlataforma();
    loadGenero();

    function loadPlataforma() {
        $.get('/platform', function (data) {
            const PlataformaSelect = $('#PlataformaId');
            PlataformaSelect.empty();
            PlataformaSelect.append('<option value="">Selecciona una Plataforma</option>');
            data.forEach(function (plataforma) {
                PlataformaSelect.append(`<option value="${plataforma.PlataformaID}">${plataforma.PlataformaDescripcion}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar las plataformas:', xhr.responseText);
        });
    }

    function loadGenero() {
        $.get('/gender', function (data) {
            const GeneroSelect = $('#GeneroId');
            GeneroSelect.empty();
            GeneroSelect.append('<option value="">Selecciona un Género</option>');
            data.forEach(function (genero) {
                GeneroSelect.append(`<option value="${genero.GeneroID}">${genero.GeneroDescripcion}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los géneros:', xhr.responseText);
        });
    }

    function loadVideojuegos() {
        $.get('/games', function (data) {
            $('#VideojuegoTableBody').empty();
            data.forEach(function (videojuego) {
                const nombreImagen = videojuego.VideojuegoNombre
                    .toLowerCase()
                    .replace(/\s+/g, '_')
                    .replace(/[^\w_]/g, '');

                const imagenSrc = `/static/img/juegos/${nombreImagen}.jpg`;

                $('#VideojuegoTableBody').append(`
                    <tr>
                        <td>${videojuego.VideojuegoID}</td>
                        <td>${videojuego.VideojuegoNombre}</td>
                        <td>${videojuego.VideojuegoDescripcion}</td>
                        <td>${videojuego.PlataformaDescripcion}</td>
                        <td>${videojuego.GeneroDescripcion}</td>
                        <td>$ ${videojuego.VideojuegoPrecio}</td>
                        <td>${videojuego.VideojuegoLanzamiento}</td>
                        <td>${videojuego.VideojuegoStock}</td>
                        <td>${videojuego.VideojuegoFechMod}</td>
                        <td><img src="${imagenSrc}" alt="Imagen" width="50"></td>
                        <td>
                            <button class='btn btn-warning' onclick='editVideojuego(${videojuego.VideojuegoID})'>
                                <ion-icon name="create"></ion-icon>
                            </button>
                            <button class='btn btn-danger' onclick='deleteVideojuego(${videojuego.VideojuegoID})'>
                                <ion-icon name="trash"></ion-icon>
                            </button>
                        </td>
                    </tr>`);
            });
            $('#VideojuegoTable').removeClass('d-none');
        });
    }

    // Mostrar formulario para agregar producto
    $('#btnAddVideojuego').on('click', function () {
        resetForm();
        $('#formContainer').removeClass('d-none');
    });

    // Guardar producto (crear o actualizar) con FormData para incluir imagen
    $('#VideojuegoForm').on('submit', function (e) {
        e.preventDefault();

        const VideojuegoID = $('#VideojuegoId').val();


        // Crear FormData desde el formulario
        const formData = new FormData(this);

        // Nombre procesado para imagen
        const nombreVideojuegoProcesado = $('#VideojuegoNombre').val()
            .toLowerCase()
            .replace(/\s+/g, '_')
            .replace(/[^\w_]/g, '');
        formData.append('VideojuegoNombreProcesado', nombreVideojuegoProcesado);

        $.ajax({
            url: VideojuegoID ? `/games/${VideojuegoID}` : '/games',
            type: VideojuegoID ? 'PUT' : 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                loadVideojuegos();
                resetForm();
            },
            error: function (xhr, status, error) {
                console.error('Error al guardar el videojuego:', status, error);
                alert('Error al guardar el videojuego.');
            }
        });
    });

    // Editar producto: cargar datos en formulario
    window.editVideojuego = function (id) {
        $.get(`/games/${id}`, function (data) {
            if (data && data.VideojuegoID) {
                $('#VideojuegoId').val(data.VideojuegoID);
                $('#VideojuegoNombre').val(data.VideojuegoNombre);
                $('#VideojuegoDescripcion').val(data.VideojuegoDescripcion);
                $('#PlataformaId').val(data.PlataformaID);
                $('#GeneroId').val(data.GeneroID);
                $('#VideojuegoPrecio').val(data.VideojuegoPrecio);

                // Convertir fecha al formato "YYYY-MM-DD"
                const fecha = new Date(data.VideojuegoLanzamiento).toISOString().split('T')[0];
                $('#VideojuegoLanzamiento').val(fecha);

                $('#VideojuegoStock').val(data.VideojuegoStock);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Videojuego no encontrado.');
            }
        }).fail(function (xhr) {
            console.error('Error al obtener el videojuego:', xhr.responseText);
            alert('Error al cargar los datos del videojuego.');
        });
    };

    // Eliminar producto con confirmación
    window.deleteVideojuego = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este videojuego?')) {
            $.ajax({
                url: `/games/${id}`,
                type: 'DELETE',
                success: function () {
                    loadVideojuegos();
                },
                error: function (xhr) {
                    console.error('Error al eliminar el videojuego:', xhr.responseText);
                    alert('Error al eliminar el videojuego.');
                }
            });
        }
    };

    // Cancelar y limpiar formulario
    $('#btnCancel').on('click', resetForm);

    function resetForm() {
        $('#VideojuegoId').val('');
        $('#VideojuegoNombre').val('');
        $('#VideojuegoDescripcion').val('');
        $('#PlataformaId').val('');
        $('#GeneroId').val('');
        $('#VideojuegoPrecio').val('');
        $('#VideojuegoLanzamiento').val('');
        $('#VideojuegoStock').val('');
        $('#VideojuegoFoto').val('');
        $('#formContainer').addClass('d-none');
    }
});
