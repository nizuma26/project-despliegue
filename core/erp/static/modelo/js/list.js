let dttModelo;
let current_data = {}
let modelos = {
    list: function () {
        dttModelo = $('#data_list').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdata'
                },
                dataSrc: "",
            },
            language: {
                decimal: "",
                sLengthMenu: "Mostrar _MENU_ registros",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 a 0 de 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                searchPlaceholder: "Buscar",
                search: "<button type='button' class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                    first: "Primero",
                    last: "Ultimo",
                    next: "<span class='fa fa-angle-double-right'></span>",
                    previous: "<span class='fa fa-angle-double-left'></span>",
                },
                buttons: {
                    copy: "Copiar",
                    print: "Imprimir",
                },
            },
            columns: [
                { "data": "id" },
                { "data": "modelo" },
                { "data": "marcas.marca" },
                { "data": "id" },
            ],
            order: [[0, "desc"]],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a rel="edit" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        })
    }
};
$(function () {
    modelos.list(); 
    $('select[name="marcas"]').select2({
        dropdownParent: $('#myModalModelos .modal-body'),
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_marcas'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data,
                };            
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,

    })
        $('.btnAdd').on('click', function () {
            $('input[name="action"]').val('add');
            $('#titlemodelo').find('span').html('Creación de un Modelo');
            $('#titlemodelo').find('i').removeClass().addClass('fas fa-plus');
            $('#idmodelo').focus();
            $('#myModalModelos').modal('show');
        })        

        $('#myModalModelos').on('hidden.bs.modal', function (e) {
            $('#frmModelos').trigger('reset');          
        })

    });
    $('#frmModelos').on('submit', function (e) {
        e.preventDefault();
        let myForm = document.getElementById('frmModelos');
        let parameters = new FormData(myForm);
        const url = window.location.pathname;
        let titulo = "";
        let text = "";
        if ($('input[name="action"]').val() == 'add') {            
            titulo = "¿Estas seguro de crear el modelo?";
            text = 'creado'
        } else {
            titulo = "¿Estas seguro de actualizar el modelo?";
            text = 'modificado'
            parameters.append('current_data', JSON.stringify(current_data));
        }
        submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
            $('#myModalModelos').modal('hide');
            sweet_info(`Registro ${text} con exito`);
            dttModelo.ajax.reload();
        });
    });
    $('#data_list tbody').on('click', 'a[rel="edit"]', function () {
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        $('.modal-title').find('span').html('Edición de un Modelo');
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="marca_id"]').val(data.marcas.id);
        $('input[name="modelo"]').val(data.modelo);
        $('#idmarcas').val(data.marcas.id).trigger('change.select2');
        console.log(data);
        current_data = data;
        $('#myModalModelos').modal('show');
    });
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el modelo?  ' + '<b style="color: #304ffe;">' + data.modelo + '</b>', parameters, function () {
            sweet_info('Registro eliminado con exito'); 
            dttModelo.row(tr.row).remove().draw();
        })
});

