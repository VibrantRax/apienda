$(document).ready(function () {
    // Cargar categorías y opciones del select al inicio
    loadCategorias();

    function loadCategorias() {
        $.get('/category', function (data) {
            $('#CategoriasTableBody').empty(); // Limpia la tabla
            data.forEach(function (categoria) {
                $('#CategoriasTableBody').append(`
                    <tr>
                        <td>${categoria.CategoriaID}</td>
                        <td>${categoria.CategoriaDescripcion}</td>
                        <td>${categoria.CategoriaFechMod}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editCategoria(${categoria.CategoriaID})'>
                                <ion-icon name="create"></ion-icon>
                            </button>
                            <button class='btn btn-danger' onclick='deleteCategoria(${categoria.CategoriaID})'>
                                <ion-icon name="trash"></ion-icon>
                            </button>
                        </td>
                    </tr>`);
            });
            $('#CategoriasTable').removeClass('d-none');

        });
    }

    // Mostrar el formulario al hacer clic en "Agregar Categoria"
    $('#btnAddCategoria').on('click', function () {
        resetForm();
        $('#formContainer').removeClass('d-none');
    });

    // Guardar categoría (crear o actualizar)
    $('#CategoriaForm').on('submit', function (e) {
        e.preventDefault();

        const CategoriaID = $('#CategoriaId').val();
        const CategoriaData = {
            CategoriaDescripcion: $('#CategoriaNombre').val(), // corregido
        };


        if (CategoriaID) {
            // Actualizar categoría
            $.ajax({
                url: `/category/${CategoriaID}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(CategoriaData),
                success: function () {
                    loadCategorias();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al actualizar la categoría:', xhr.responseText);
                    alert('Error al actualizar la categoría.');
                }
            });
        } else {
            // Crear nueva categoría
            $.ajax({
                url: '/category',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(CategoriaData),
                success: function () {
                    loadCategorias();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear la categoría:', xhr.responseText);
                    alert('Error al crear la categoría.');
                }
            });
        }
    });

    // Editar categoría
    window.editCategoria = function (id) {
        $.get(`/category/${id}`, function (data) {
            if (data && data.CategoriaID) {
                $('#CategoriaId').val(data.CategoriaID);
                $('#CategoriaNombre').val(data.CategoriaDescripcion);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Categoría no encontrada.');
            }
        }).fail(function (xhr) {
            console.error('Error al obtener la categoría:', xhr.responseText);
            alert('Error al cargar los datos de la categoría.');
        });
    };


    // Eliminar categoría
    window.deleteCategoria = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta categoría?')) {
            $.ajax({
                url: `/category/${id}`,
                type: 'DELETE',
                success: function () {
                    loadCategorias();
                },
                error: function (xhr) {
                    console.error('Error al eliminar la categoría:', xhr.responseText);
                    alert('Error al eliminar la categoría.');
                }
            });
        }
    };

    // Cancelar y limpiar formulario
    $('#btnCancel').on('click', resetForm);

    function resetForm() {
        $('#CategoriaId').val('');
        $('#CategoriaNombre').val('');
        $('#formContainer').addClass('d-none');
    }

});
