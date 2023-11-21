let dttDepart;
let current_data = {}
$(function () {
    dttDepart = $('#data_list').DataTable({
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
            {"data": "id"},
            {"data": "nombre"},
            {"data": "id"},
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
        $('#titledepart').find('span').html('Creación de un Departamento');
        $('#titledepart').find('i').removeClass().addClass('fas fa-plus');        
        $('#iddepartamento').focus();
        $('#myModalDepart').modal('show');
    });
    
    $('#myModalDepart').on('hidden.bs.modal', function (e) {
        $('#frmDepart').trigger('reset');
        const inputs = document.querySelectorAll('#myModalDepart .txt_field input');
         inputs.forEach(input => input.classList.remove('input-has-text'));
    })
    $("#myModalDepart").on('shown.bs.modal', function(){
        const inputs = document.querySelectorAll('#myModalDepart .txt_field input');
        inputs.forEach(input => { if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => { if (input.value.trim() !== '') { input.classList.add('input-has-text');
            } else { input.classList.remove('input-has-text'); }
            });
        });
    });
   
});
$('#frmDepart').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmDepart');
    let parameters = new FormData(myForm);
    let titulo="";
    let text="";
    if  ($('input[name="action"]').val() == 'add'){
        titulo="¿Estas seguro de crear el departamento?";
        text = 'creado'
    }else{
        titulo="¿Estas seguro de actualizar los datos del departamento?";
        text = 'modificado'
        parameters.append('current_data', JSON.stringify(current_data));
    }
    submit_with_ajax(window.location.pathname, 'Estimado usuario(a)', titulo, parameters, function (response) {
            $('#myModalDepart').modal('hide');
            sweet_info(`El departamento se ha ${text} con exito`);
            dttDepart.ajax.reload();
        });

});
$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
      $('.modal-title').find('span').html('Edición de un departamento');
      param_id=data.id;
      $('input[name="action"]').val('edit');
      $('input[name="id"]').val(data.id);
      $('input[name="nombre"]').val(data.nombre);
        current_data = data;
      $('#myModalDepart').modal('show');
  });
  $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el departamento?  ' + '<b style="color: #304ffe;">' + data.nombre + '</b>', parameters, function () {
        sweet_info('Registro eliminado con exito'); 
        dttDepart.row(tr.row).remove().draw();
    });
  });
