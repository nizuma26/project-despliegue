let dttAlmacen;
let current_data = {}
let changes = []
$(function () {
    dttAlmacen = $('#data_list').DataTable({
        responsive: true,
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
            search: "<button class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
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
            { "data": "codigo" },
            { "data": "nombre" },
            { "data": "responsable" },
            { "data": "cedula" },
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
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('#title_almacen').find('span').html('Creación de un Almacen');
        $('#title_almacen').find('i').removeClass().addClass('fas fa-plus');
        $('#idAlmacen').focus();
        $('#myModalAlmacen').modal('show');
    });
    
    $('#myModalAlmacen').on('hidden.bs.modal', function (e) {
        $('#frmAlmacen').trigger('reset');
        const inputs = document.querySelectorAll('#myModalAlmacen .txt_field input, #myModalAlmacen .txt_field select');
        inputs.forEach(input => input.classList.remove('input-has-text'));
    });
    $("#myModalAlmacen").on('shown.bs.modal', function () {
        const inputs = document.querySelectorAll('#myModalAlmacen .txt_field input, #myModalAlmacen .txt_field select');
        inputs.forEach(input => {
            if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => {
                if (input.value.trim() !== '') {
                    input.classList.add('input-has-text');
                } else { input.classList.remove('input-has-text'); }
            });
        });
    });
});
//PARA VERIFICAR SI LOS DATOS DEL REGISTRO SE HAN MODIFICADO O SIGUEN IGUAL
const audit_data = () => {
    let compare_data = [
        { field: 'Código', value_ant: current_data.codigo, value_act: $('input[name="codigo"]').val()},
        { field: 'Nombre', value_ant: current_data.nombre, value_act: $('input[name="nombre"]').val()},
        { field: 'Responsable', value_ant: current_data.responsable, value_act: $('input[name="responsable"]').val()},
        { field: 'Cédula', value_ant: current_data.cedula, value_act: $('input[name="cedula"]').val()},
        { field: 'Unidad', value_ant: current_data.unidad, value_act: $('select[name="unidad"]').val()},
    ]
    compare_data.forEach((data) => {
        if (data.value_ant != data.value_act) {
            changes.push(data);
        }
    });
}

$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    $('.modal-title').find('span').html('Edición del Almacen:  ' + '<b style="color: #ffffff;">' + data.codigo + '</b>');
    $('input[name="action"]').val('edit');
    $('input[name="id"]').val(data.id);
    $('input[name="codigo"]').val(data.codigo);
    $('input[name="nombre"]').val(data.nombre);
    $('#idunidad').val(data.unidad).trigger('change.select2');
    $('input[name="cedula"]').val(data.cedula);
    $('input[name="responsable"]').val(data.responsable);
    current_data = data;
    $('#myModalAlmacen').modal('show');
});
$('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = window.location.pathname;
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el Almacen?  ' + '<b style="color: #304ffe;">' + data.nombre + '</b>', parameters, function () {
        sweet_info('Registro eliminado con exito');
        dttAlmacen.row(tr.row).remove().draw();
    });
});
$('#frmAlmacen').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmAlmacen');
    let parameters = new FormData(myForm);
    const url = window.location.pathname;
    let text = "";
    let titulo = "";
    if ($('input[name="action"]').val() == 'add') {
        titulo = "¿Estas seguro de crear el Almacen?";
        text = 'creado'
    } else {
        changes = [];
        audit_data();
        titulo = "¿Estas seguro de actualizar el Almacen?";
        text = 'modificado'
    }
    submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
        $('#myModalAlmacen').modal('hide');
        sweet_info(`El registro se ha ${text} con exito`);
        dttAlmacen.ajax.reload();
        if (changes.length > 0){
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

