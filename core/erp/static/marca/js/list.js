let dttMarca;
let current_data = {};
$(function () {
    dttMarca = $('#data_list').DataTable({
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
            {"data": "marca"},
            {"data": "id"},
        ],
        order: [[0, "desc"]],
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
        $('#titlemarca').find('span').html('Creación de una Marca');
        $('#titlemarca').find('i').removeClass().addClass('fas fa-plus');
        $('#idmarca').focus();
        $('#myModalMarcas').modal('show');
    });
    $("#myModalMarcas").on('shown.bs.modal', function(){
        const inputs = document.querySelectorAll('#myModalMarcas .txt_field input');
        inputs.forEach(input => { if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => { if (input.value.trim() !== '') { input.classList.add('input-has-text');
            } else { input.classList.remove('input-has-text'); }
            });
        });
    });
    
    $('#myModalMarcas').on('hidden.bs.modal', function (e) {
        $('#frmMarcas').trigger('reset');
        const inputs = document.querySelectorAll('#myModalMarcas .txt_field input');
         inputs.forEach(input => input.classList.remove('input-has-text'));
    })
   
});
$('#frmMarcas').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('frmMarcas');
    let parameters = new FormData(myForm);
    const url= window.location.pathname;
    let titulo="";
    let text="";
    if  ($('input[name="action"]').val() == 'add'){
        titulo="¿Estas seguro de crear la marca?";
        text = 'creado'
    }else{
        titulo="¿Estas seguro de actualizar la marca?";
        text='modificado'
        parameters.append('current_data', JSON.stringify(current_data));
    }
    submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
            $('#myModalMarcas').modal('hide'); 
            sweet_info(`Registro ${text} con exito`); 
            dttMarca.ajax.reload();
        });
});

    $('#data_list tbody').on('click', 'a[rel="edit"]', function () {
        let tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        let data = $("#data_list").DataTable().row(tr.row).data();
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
      $('.modal-title').find('span').html('Edición de una Marca');
      $('input[name="action"]').val('edit');
      $('input[name="id"]').val(data.id);
      $('input[name="marca"]').val(data.marca);
        current_data = data;
      $('#myModalMarcas').modal('show');
    });
  $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
    let tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    let data = $("#data_list").DataTable().row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = window.location.pathname;
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar la marca?  ' + '<b style="color: #304ffe;">' + data.marca + '</b>', parameters, function () {
        sweet_info('Registro eliminado con exito'); 
        dttMarca.row(tr.row).remove().draw();
    });
  });
