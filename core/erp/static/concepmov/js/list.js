let dttConcepMov;
let current_data = {}
let changes = []
$(function () {
    dttConcepMov = $('#data_list').DataTable({
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
            { "data": "codigo" },
            { "data": "denominacion" },
            { "data": "estado.name" },
            { "data": "tipo_conc.name" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estado.id == 'ACT') return '<span class="badge rounded-pill badge-success" style="font-size: 10px;">' + data + '</span>'
                    if (row.estado.id == 'INA') return '<span class="badge rounded-pill badge-danger" style="font-size: 10px;">' + data + '</span>'

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
        $('#titleConcept').find('span').html('Creando Concepto de Movimiento');
        $('#titleConcept').find('i').removeClass().addClass('fas fa-plus');
        $('#idCod').focus();
        $('#myModalConcepMov').modal('show');
    });
    $("#myModalConcepMov").on('shown.bs.modal', function () {
        const concept = $('select[name="tipo_conc"]').val()
        if (concept == 'SA') {
            $("#salida_bienes").collapse('show');
        } else {
            $('select[name="salida_bienes"]').val(null)
        }
        const inputs = document.querySelectorAll('#myModalConcepMov .txt_field input, #myModalConcepMov .txt_field select');
        inputs.forEach(input => {
            if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => {
                if (input.value.trim() !== '') {
                    input.classList.add('input-has-text');
                } else { input.classList.remove('input-has-text'); }
            });
        });
    });
    $('#myModalConcepMov').on('hidden.bs.modal', function (e) {
        $('#frmConcepMov').trigger('reset');
        const inputs = document.querySelectorAll('#myModalConcepMov .txt_field input, #myModalConcepMov .txt_field select');
        inputs.forEach(input => input.classList.remove('input-has-text'));
        $("#salida_bienes").collapse('hide');
        $('select[name="salida_bienes"]').val(null)
    })
});
$('select[name="tipo_conc"]').on('change', function () {
    let codigo = $(this).val();
    if (codigo === 'SA') {
        $("#salida_bienes").collapse('show');
    } else {
        $("#salida_bienes").collapse('hide');
        $('select[name="salida_bienes"]').val(null)
    }
});
$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    $('.modal-title').find('span').html('Edición del Concepto:  ' + '<b style="color: #ffffff;">' + data.codigo + '</b>');
    $('input[name="action"]').val('edit');
    $('input[name="id"]').val(data.id);
    $('input[name="codigo"]').val(data.codigo);
    $('input[name="denominacion"]').val(data.denominacion);
    $('#idestado').val(data.estado.id);
    $('#idtipo_conc').val(data.tipo_conc.id);
    $('#idsalida_bienes').val(data.tipo_bienes.id);
    $('#myModalConcepMov').modal('show');
    current_data = data;
});
$('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = window.location.pathname
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el Concepto?  ' + '<b style="color: #304ffe;">' + data.denominacion + '</b>', parameters, function () {
        dttConcepMov.ajax.reload();
    });
});
//PARA VERIFICAR SI LOS DATOS DEL REGISTRO SE HAN MODIFICADO O SIGUEN IGUAL
function audit_data() {
    let compare_data = [
        { field: 'Código', value_ant: current_data.codigo, value_act: $('input[name="codigo"]').val()},
        { field: 'Denominación', value_ant: current_data.denominacion, value_act: $('input[name="denominacion"]').val()},
        { field: 'Estado', value_ant: current_data.estado.name, value_act: $('select[name="estado"] option:selected').text()},
        { field: 'Tipo de concepto', value_ant: current_data.tipo_conc.name, value_act: $('select[name="tipo_conc"] option:selected').text()},
        { field: 'Bienes que despacha', value_ant: current_data.tipo_bienes.id, value_act: $('select[name="salida_bienes"]').val()},
    ]
    compare_data.forEach((data) => {
        if (data.value_ant != data.value_act) {
            changes.push(data);
        }
    });
}
$('#frmConcepMov').on('submit', function (e) {
    e.preventDefault();
    const myForm = document.getElementById('frmConcepMov');
    let parameters = new FormData(myForm);
    const url = window.location.pathname;;
    let titulo = "";
    let text = "";
    if ($('input[name="action"]').val() == 'add') {
        titulo = "¿Estas seguro de crear el Concepto?";
        text = 'creado';
    } else {
        changes = [];
        audit_data();
        text = 'modificado';
        titulo = "¿Estas seguro de actualizar el Concepto?";
    }
    submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
        $('#myModalConcepMov').modal('hide');
        sweet_info(`El registro se ha ${text} con exito`);
        dttConcepMov.ajax.reload();
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
            // callback(data);
            return false;
        }                       
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {                        
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
  }