let dttCodbienes;
let current_data = {}
$(function () {
    dttCodbienes = $('#data_list').DataTable({
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
            {"data": "codbien"},
            {"data": "estado.name"},
            {"data": "id"},
        ],
        order: [[0, "desc"]],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if(row.estado.id == 'ASI')return '<span class="badge rounded-pill badge-primary" style="font-size: 10px;">'+data+'</span>'
                    else if(row.estado.id == 'SAS')return '<span class="badge rounded-pill badge-success" style="font-size: 10px;">'+data+'</span>'
                    else if(row.estado.id == 'ANU')return '<span class="badge rounded-pill badge-danger" style="font-size: 10px;">'+data+'</span>'
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
        $('#titlecodbienes').find('span').html('Creando Código de Bien Nacional');
        $('#titlecodbienes').find('i').removeClass().addClass('fas fa-plus');
        $('#idCod').focus();
        $('#myModalCodbienes').modal('show');
    });
    $("#myModalCodbienes").on('shown.bs.modal', function(){
        const inputs = document.querySelectorAll('#myModalCodbienes .txt_field input, #myModalCodbienes .txt_field select');
         inputs.forEach(input => { if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => { if (input.value.trim() !== '') { input.classList.add('input-has-text');
            } else { input.classList.remove('input-has-text');  }
            });
        });
    });
    
    $('#myModalCodbienes').on('hidden.bs.modal', function (e) {
        $('#frmCodbienes').trigger('reset');
        $('#frmCodbienes').trigger('reset');
        const inputs = document.querySelectorAll('#myModalCodbienes .txt_field input, #myModalCodbienes .txt_field select');
         inputs.forEach(input => input.classList.remove('input-has-text'));
    })
   
});
$('#frmCodbienes').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmCodbienes');
    let parameters = new FormData(myForm);
    const url = window.location.pathname;
    let titulo = "";
    let text = ""
    if  ($('input[name="action"]').val() == 'add'){
        titulo="¿Estas seguro de crear el Codigo?";
        text = "creado"
    }else{
        titulo="¿Estas seguro de actualizar el Codigo?";
        text = "modificado"
    }
    parameters.append('current_data', JSON.stringify(current_data));
    submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
            $('#myModalCodbienes').modal('hide');
            sweet_info( 'El registro ha sido '+text+' con exito'); 
            dttCodbienes.ajax.reload();
        });
});
$('#data_list tbody').on('click', 'a[rel="edit"]', function () {
        let tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        let data = $("#data_list").DataTable().row(tr.row).data();
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
      $('.modal-title').find('span').html('Edición del Codigo:  ' + '<b style="color: #b3e5fc;">' + data.codbien + '</b>');
      param_id=data.id;
      $('input[name="action"]').val('edit');
      $('input[name="id"]').val(data.id);
      $('input[name="codbien"]').val(data.codbien);      
      $('#idestado').val(data.estado.id).trigger('change.select2');
        current_data = data;
      $('#myModalCodbienes').modal('show');      
  });
  $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    let tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    let data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = window.location.pathname;
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el Registro?  ' + '<b style="color: #304ffe;">' + data.codbien + '</b>', parameters, function () {
        sweet_info("El registro ha sido eliminado con exito");
        dttCodbienes.row(tr.row).remove().draw();
    });
  });
