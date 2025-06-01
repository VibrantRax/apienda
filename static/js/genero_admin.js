$(document).ready(function () {
    // Cargar Generos
    loadGenero();

    function loadGenero() {
        $.get('/gender', function (data) {
            $('#GenerosTableBody').empty(); // Limpia la tabla
            data.forEach(function (genero) {
                $('#GenerosTableBody').append(`
                    <tr>
                        <td>${genero.GeneroID}</td>
                        <td>${genero.GeneroDescripcion}</td>
                        <td>${genero.GeneroFechMod}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editGenero(${genero.GeneroID})'>
                                <ion-icon name="create"></ion-icon>
                            </button>
                            <button class='btn btn-danger' onclick='deleteGenero(${genero.GeneroID})'>
                                <ion-icon name="trash"></ion-icon>
                            </button>
                        </td>
                    </tr>`);
            });
            $('#GenerosTable').removeClass('d-none');

        });
    }

    // Mostrar el formulario al hacer clic en "Agregar Genero"
    $('#btnAddGenero').on('click', function () {
        resetForm();
        $('#formContainer').removeClass('d-none');
    });

    // Guardar Genero (crear o actualizar)
    $('#GeneroForm').on('submit', function (e) {
        e.preventDefault();

        const GeneroID = $('#GeneroId').val();
        const GeneroData = {
            GeneroDescripcion: $('#GeneroNombre').val(), // corregido
        };


        if (GeneroID) {
            // Actualizar Genero
            $.ajax({
                url: `/gender/${GeneroID}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(GeneroData),
                success: function () {
                    loadGenero();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al actualizar el genero:', xhr.responseText);
                    alert('Error al actualizar el genero.');
                }
            });
        } else {
            // Crear nuevo Genero
            $.ajax({
                url: '/gender',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(GeneroData),
                success: function () {
                    loadGenero();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear el genero:', xhr.responseText);
                    alert('Error al crear el genero.');
                }
            });
        }
    });

    // Editar Genero
    window.editGenero = function (id) {
        $.get(`/gender/${id}`, function (data) {
            if (data && data.GeneroID) {
                $('#GeneroId').val(data.GeneroID);
                $('#GeneroNombre').val(data.GeneroDescripcion);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Genero no encontrado.');
            }
        }).fail(function (xhr) {
            console.error('Error al obtener la Genero:', xhr.responseText);
            alert('Error al cargar los datos de la Genero.');
        });
    };


    // Eliminar Genero
    window.deleteGenero = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este Genero?')) {
            $.ajax({
                url: `/gender/${id}`,
                type: 'DELETE',
                success: function () {
                    loadGenero();
                },
                error: function (xhr) {
                    console.error('Error al eliminar el genero:', xhr.responseText);
                    alert('Error al eliminar el genero.');
                }
            });
        }
    };

    // Cancelar y limpiar formulario
    $('#btnCancel').on('click', resetForm);

    function resetForm() {
        $('#GeneroId').val('');
        $('#GeneroNombre').val('');
        $('#formContainer').addClass('d-none');
    }

});
