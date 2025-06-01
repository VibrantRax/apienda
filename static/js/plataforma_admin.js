$(document).ready(function () {
    // Cargar Plataformas
    loadPlataforma();

    function loadPlataforma() {
        $.get('/platform', function (data) {
            $('#GPlataformaTableBody').empty(); // Limpia la tabla
            data.forEach(function (plataforma) {
                $('#PlataformaTableBody').append(`
                    <tr>
                        <td>${plataforma.PlataformaID}</td>
                        <td>${plataforma.PlataformaDescripcion}</td>
                        <td>${plataforma.PlataformaFechMod}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editPlataforma(${plataforma.PlataformaID})'>
                                <ion-icon name="create"></ion-icon>
                            </button>
                            <button class='btn btn-danger' onclick='deletePlataforma(${plataforma.PlataformaID})'>
                                <ion-icon name="trash"></ion-icon>
                            </button>
                        </td>
                    </tr>`);
            });
            $('#PlataformaTable').removeClass('d-none');

        });
    }

    // Mostrar el formulario al hacer clic en "Agregar Plataforma"
    $('#btnAddPlataforma').on('click', function () {
        resetForm();
        $('#formContainer').removeClass('d-none');
    });

    // Guardar Plataforma (crear o actualizar)
    $('#PalaformaForm').on('submit', function (e) {
        e.preventDefault();

        const PlataformaID = $('#PlataformaId').val();
        const PlataformaData = {
            PlataformaDescripcion: $('#PlataformaNombre').val(), // corregido
        };


        if (PlataformaID) {
            // Actualizar Plataforma
            $.ajax({
                url: `/platform/${PlataformaID}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(PlataformaData),
                success: function () {
                    loadPlataforma();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al actualizar la plataforma:', xhr.responseText);
                    alert('Error al actualizar la plataforma.');
                }
            });
        } else {
            // Crear nuevo Plataforma
            $.ajax({
                url: '/platform',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(PlataformaData),
                success: function () {
                    loadPlataforma();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear la plataforma:', xhr.responseText);
                    alert('Error al crear la plataforma.');
                }
            });
        }
    });

    // Editar Plataforma
    window.editPlataforma = function (id) {
        $.get(`/platform/${id}`, function (data) {
            if (data && data.PlataformaID) {
                $('#PlataformaId').val(data.PlataformaID);
                $('#PlataformaNombre').val(data.PlataformaDescripcion);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Plataforma no encontrado.');
            }
        }).fail(function (xhr) {
            console.error('Error al obtener la plataforma:', xhr.responseText);
            alert('Error al cargar los datos de la plataforma.');
        });
    };


    // Eliminar Plataforma
    window.deletePlataforma = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este Plataforma?')) {
            $.ajax({
                url: `/platform/${id}`,
                type: 'DELETE',
                success: function () {
                    loadPlataforma();
                },
                error: function (xhr) {
                    console.error('Error al eliminar la plataforma:', xhr.responseText);
                    alert('Error al eliminar la plataforma.');
                }
            });
        }
    };

    // Cancelar y limpiar formulario
    $('#btnCancel').on('click', resetForm);

    function resetForm() {
        $('#PlataformaId').val('');
        $('#PlataformaNombre').val('');
        $('#formContainer').addClass('d-none');
    }

});
