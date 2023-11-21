let dttMonedas;
let current_data = {}
let changes = []
$(function () {
    dttMonedas = $('#data_list').DataTable({
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
            search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
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
            { "data": "codigo" },
            { "data": "simbolo" },
            { "data": "moneda" },
            { "data": "pais" },
            { "data": "tasa_cambio" },
            { "data": "status" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.status == true) return '<a><i class="fa fa-check" style="color:green"><span style="display:none;">' + 'activo' + '</span></i></a>'
                    if (row.status == false) return '<a><i class="fa fa-times" style="color:red"><span style="display:none;">' + 'inactivo' + '</span></i></a>'
                }
            },
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
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('#titlemoneda').find('span').html('Creando Nueva Moneda');
        $('#titlemoneda').find('i').removeClass().addClass('fas fa-plus');
        $('#idcod').focus();
        $('#myModalMoneda').modal('show');
    });

    $('#myModalMoneda').on('hidden.bs.modal', function (e) {
        $('#frmMoneda').trigger('reset');
    })

});
function audit_data(){
    let compare_data = [
        {field: 'Codigo', value_ant: current_data.codigo, value_act: $('input[name="codigo"]').val()},
        {field: 'Pais', value_ant: current_data.pais, value_act: $('input[name="pais"]').val()},
        {field: 'Nombre', value_ant: current_data.moneda, value_act: $('input[name="moneda"]').val()},
        {field: 'Simbolo', value_ant: current_data.simbolo, value_act: $('input[name="simbolo"]').val()},
        {field: 'Tasa_cambio', value_ant: current_data.tasa_cambio, value_act: $('input[name="tasa_cambio"]').val()},
        {field: 'Estado', value_ant: current_data.status, value_act: $('#idstatus').prop("checked")},
    ]
    compare_data.forEach((data) => {
        if (data.value_ant != data.value_act){
            changes.push(data);
        }
    });        
}
$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    $('.modal-title').find('span').html('Edición de la Moneda:  ' + '<b style="color: #ffffff;">' + data.codigo + '</b>');
    $('input[name="action"]').val('edit');
    $('input[name="id"]').val(data.id);
    $('input[name="codigo"]').val(data.codigo);
    $('input[name="moneda"]').val(data.moneda);
    $('input[name="simbolo"]').val(data.simbolo);
    $('input[name="pais"]').val(data.pais);
    $('input[name="tasa_cambio"]').val(data.tasa_cambio);
    if (data.status == true) {
        //$("#idactivo").val(1).change();
        $("#idstatus").prop('checked', 1);
    } else {
        //$("#idactivo").val(0).change();
        $("#idstatus").prop('checked', 0);
    }
    console.log(data)
    current_data = data;
    $('#myModalMoneda').modal('show');
});
$('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);

    const url = window.location.pathname;
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el Almacen?  ' + '<b style="color: #304ffe;">' + data.codbien + '</b>', parameters, function () {
        dttMonedas.row(tr.row).remove().draw();
    });
});

$('#frmMoneda').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmMoneda');
    let parameters = new FormData(myForm);
    let text = "";
    let update = false
    const url = window.location.pathname;
    let titulo = "";
    if ($('input[name="action"]').val() == 'add') {
        titulo = "¿Estas seguro de crear la moneda?";
        text = 'creado'
    } else {
        changes = [];
        audit_data();
        titulo = "¿Estas seguro de actualizar la moneda?";
        text = 'modificado'
        update = true
    }
    console.log(changes);
    submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
        $('#myModalMoneda').modal('hide');
        sweet_info(`El registro se ha ${text} con exito`);
        dttMonedas.ajax.reload();
        if (update){
            field_save()
        }
    });
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

