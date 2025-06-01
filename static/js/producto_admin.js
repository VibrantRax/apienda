$(document).ready(function () {
    // Cargar productos y categorías al inicio
    loadProducto();
    loadCategoria();

    function loadCategoria() {
        $.get('/category', function(data){
            const categoriaSelect = $('#CategoriaId');
            categoriaSelect.empty();
            categoriaSelect.append('<option value="">Selecciona una categoria</option>');
            data.forEach(function (categoria){
                categoriaSelect.append(`<option value="${categoria.CategoriaID}">${categoria.CategoriaDescripcion}</option>`);
            });
        }).fail(function (xhr){
            console.error('Error al cargar las categorias:', xhr.responseText);
        });
    }

    function loadProducto() {
        $.get('/product', function (data) {
            $('#ProductoTableBody').empty();
            data.forEach(function (producto) {
                const nombreImagen = producto.ProductoNombre
                    .toLowerCase()
                    .replace(/\s+/g, '_')
                    .replace(/[^\w_]/g, '');

                const imagenSrc = `/static/img/productos/${nombreImagen}.jpg`;

                $('#ProductoTableBody').append(`
                    <tr>
                        <td>${producto.ProductoID}</td>
                        <td>${producto.ProductoNombre}</td>
                        <td>${producto.ProductoDescripcion}</td>
                        <td>${producto.CategoriaDescripcion}</td>
                        <td>$ ${producto.ProductoPrecio}</td>
                        <td>${producto.ProductoStock}</td>
                        <td>${producto.ProductoFechMod}</td>
                        <td><img src="${imagenSrc}" alt="Imagen" width="50"></td>
                        <td>
                            <button class='btn btn-warning' onclick='editProducto(${producto.ProductoID})'>
                                <ion-icon name="create"></ion-icon>
                            </button>
                            <button class='btn btn-danger' onclick='deleteProducto(${producto.ProductoID})'>
                                <ion-icon name="trash"></ion-icon>
                            </button>
                        </td>
                    </tr>`);
            });
            $('#ProductoTable').removeClass('d-none');
        });
    }

    // Mostrar formulario para agregar producto
    $('#btnAddProducto').on('click', function () {
        resetForm();
        $('#formContainer').removeClass('d-none');
    });

    // Guardar producto (crear o actualizar) con FormData para incluir imagen
    $('#ProductoForm').on('submit', function (e) {
        e.preventDefault();

        const ProductoID = $('#ProductoId').val();

        // Crear FormData desde el formulario (incluye inputs y archivo)
        const formData = new FormData(this);

        // Ejemplo: agregar campo procesado (opcional)
        const nombreProductoProcesado = $('#ProductoNombre').val()
            .toLowerCase()
            .replace(/\s+/g, '_')
            .replace(/[^\w_]/g, '');
        formData.append('ProductoNombreProcesado', nombreProductoProcesado);

        $.ajax({
            url: ProductoID ? `/product/${ProductoID}` : '/product',
            type: ProductoID ? 'PUT' : 'POST',
            data: formData,
            processData: false,  // Importante para FormData
            contentType: false,  // Importante para FormData
            success: function () {
                loadProducto();
                resetForm();
            },
            error: function (xhr, status, error) {
                console.error('Error al guardar el producto:', status, error);
                alert('Error al guardar el producto.');
            }
        });
    });

    // Editar producto: cargar datos en formulario
    window.editProducto = function (id) {
        $.get(`/product/${id}`, function (data) {
            if (data && data.ProductoID) {
                $('#ProductoId').val(data.ProductoID);
                $('#ProductoNombre').val(data.ProductoNombre);
                $('#ProductoDescripcion').val(data.ProductoDescripcion);
                $('#CategoriaId').val(data.CategoriaID);
                $('#ProductoPrecio').val(data.ProductoPrecio);
                $('#ProductoStock').val(data.ProductoStock);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Producto no encontrado.');
            }
        }).fail(function (xhr) {
            console.error('Error al obtener el producto:', xhr.responseText);
            alert('Error al cargar los datos del producto.');
        });
    };

    // Eliminar producto con confirmación
    window.deleteProducto = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
            $.ajax({
                url: `/product/${id}`,
                type: 'DELETE',
                success: function () {
                    loadProducto();
                },
                error: function (xhr) {
                    console.error('Error al eliminar el producto:', xhr.responseText);
                    alert('Error al eliminar el producto.');
                }
            });
        }
    };

    // Cancelar y limpiar formulario
    $('#btnCancel').on('click', resetForm);

    function resetForm() {
        $('#ProductoId').val('');
        $('#ProductoNombre').val('');
        $('#ProductoDescripcion').val('');
        $('#CategoriaId').val('');
        $('#ProductoPrecio').val('');
        $('#ProductoStock').val('');
        $('#ProductoFoto').val(''); // limpiar input file
        $('#formContainer').addClass('d-none');
    }
});
