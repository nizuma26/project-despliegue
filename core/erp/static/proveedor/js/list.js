let dttProveedor;
let current_data = {};
let changes = [];
let proveedor = {
    list: function () {
        dttProveedor = $('#data_list').DataTable({
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
                dataSrc: ""
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
                { "data": "full_name" },
                { "data": "documento" },
                { "data": "email" },
                { "data": "tlf" },
                { "data": "id" },
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a rel="edit" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="delete" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
    }
}
$(function () {
    proveedor.list()
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de un Proveedor');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $('#empresa').focus();
        $('#myModalProveedor').modal('show');
    });

    $('#myModalProveedor').on('hidden.bs.modal', function (e) {
        $('#frmProvee').trigger('reset');
        const inputs = document.querySelectorAll('#myModalProveedor .txt_field input, #myModalProveedor .txt_field select, #myModalProveedor .txt_field textarea');
        inputs.forEach(input => input.classList.remove('input-has-text')
        );
    });
});

$("#myModalProveedor").on('shown.bs.modal', function () {
    const inputs = document.querySelectorAll('#myModalProveedor .txt_field input, #myModalProveedor .txt_field select, #myModalProveedor .txt_field textarea');
    inputs.forEach(input => {
        if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
        input.addEventListener('input', () => {
            if (input.value.trim() !== '') {
                input.classList.add('input-has-text');
            } else { input.classList.remove('input-has-text'); }
        });
    });
});
function audit_data(){
    let compare_data = [
        {field: 'Nombre', value_ant: current_data.empresa, value_act: $('input[name="empresa"]').val()},
        {field: 'Documento', value_ant: current_data.documento, value_act: $('input[name="documento"]').val()},
        {field: 'Email', value_ant: current_data.email, value_act: $('input[name="email"]').val()},
        {field: 'Ramo/Área comercial', value_ant: current_data.ramo, value_act: $('input[name="ramo"]').val()},
        {field: 'Representante', value_ant: current_data.represen, value_act: $('input[name="represen"]').val()},
        {field: 'Cedúla', value_ant: current_data.ced_repre, value_act: $('input[name="ced_repre"]').val()},
        {field: 'Teléfono', value_ant: current_data.tlf, value_act: $('input[name="tlf"]').val()},
        {field: 'Tipo de documento', value_ant: current_data.tipo_docu.name, value_act: $('select[name="tipo_docu"] option:selected').text()},
        {field: 'Dirección', value_ant: current_data.direccion, value_act: $('textarea[name="direccion"]').val()},
    ]
    compare_data.forEach((data) => {
        if (data.value_ant != data.value_act){
            changes.push(data)
        }
    });
    //console.log(changes);
}
$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    $('.modal-title').find('span').html('Edición del Proveedor:  ' + data.empresa);
    $('input[name="action"]').val('edit');
    $('input[name="id"]').val(data.id);
    $('input[name="empresa"]').val(data.empresa);
    $('select[name="tipo_docu"]').val(data.tipo_docu.id);
    $('input[name="documento"]').val(data.documento);
    $('input[name="ramo"]').val(data.ramo);
    $('input[name="tlf"]').val(data.tlf);
    $('input[name="ced_repre"]').val(data.ced_repre);
    $('input[name="represen"]').val(data.represen);
    $('input[name="email"]').val(data.email);
    $('textarea[name="direccion"]').val(data.direccion);
    current_data = data;
    $('#myModalProveedor').modal('show');
    //console.log(current_data);
});
$('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = window.location.pathname;
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar al proveedor?  ' + '<b style="color: #304ffe;">' + data.empresa + '</b>', parameters, function () {
        dttProveedor.row(tr.row).remove().draw();
    });
});

$('#frmProvee').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmProvee');
    let parameters = new FormData(myForm);
    const url = window.location.pathname;
    let titulo = "";
    let text = "";
    let update = false
    if ($('input[name="action"]').val() == 'add') {
        titulo = "¿Estas seguro de crear el proveedor?";
        text = 'creado';
    } else {
        changes = [];
        audit_data();
        titulo = "¿Estas seguro de actualizar los datos del proveedor?";
        text = 'modificado';
        update = true;
    }
    submit_with_ajax(url, 'Estimado(a) Usuario  ', titulo, parameters, function () {
        $('#myModalProveedor').modal('hide');
        sweet_info(`El registro se ha ${text} con exito`);
        dttProveedor.ajax.reload();
        if (update){
            field_save()
        }
    });
    function field_save(){
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'fields_save',
                'changes': JSON.stringify(changes),
            },
            dataType: "json",
        }).done(function (data) {                      
            if (!data.hasOwnProperty('error')) {
                return false;
            }                       
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {                        
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
      }
});
