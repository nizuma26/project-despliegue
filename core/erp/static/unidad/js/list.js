let dttUnidad;
let current_data = {}
let changes = []
let unidad = {
    list: function () {
        dttUnidad = $('#data_list').DataTable({
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
              {"data": "full_name"},
              {"data": "nombrejefe"},
              {"data": "email"},
              {"data": "tlf"},
              {"data": "tipo_unidad.name"},
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
      }
}

$(function () {
    unidad.list();
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de una Unidad');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $("#idcodigo").focus();
        $('#myModalUnidad').modal('show');
    });
    $("#myModalUnidad").on('shown.bs.modal', function(){
        const inputs = document.querySelectorAll('#myModalUnidad .txt_field input, #myModalUnidad .txt_field select, #myModalUnidad .txt_field textarea');
         inputs.forEach(input => { if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => { if (input.value.trim() !== '') { input.classList.add('input-has-text');
            } else { input.classList.remove('input-has-text');  }
            });
        });
    });
    $('#myModalUnidad').on('hidden.bs.modal', function (e) {
        $('#frmUnidad').trigger('reset');
        const inputs = document.querySelectorAll('#myModalUnidad .txt_field input, #myModalUnidad .txt_field select, #myModalUnidad .txt_field textarea');
         inputs.forEach(input => input.classList.remove('input-has-text'));
        
    })
    function audit_data(){
        let compare_data = [
            {field: 'Nombre', value_ant: current_data.nombre, value_act: $('input[name="nombre"]').val()},
            {field: 'RIF', value_ant: current_data.rif, value_act: $('input[name="rif"]').val()},
            {field: 'Responsable', value_ant: current_data.nombrejefe, value_act: $('input[name="nombrejefe"]').val()},
            {field: 'Cédula', value_ant: current_data.ced_resp, value_act: $('input[name="ced_resp"]').val()},
            {field: 'Email', value_ant: current_data.email, value_act: $('input[name="email"]').val()},
            {field: 'Teléfono', value_ant: current_data.tlf, value_act: $('input[name="tlf"]').val()},
            {field: 'Tipo de unidad', value_ant: current_data.tipo_unidad.name, value_act: $('select[name="tipo_unidad"] option:selected').text()},
            {field: 'Dirección', value_ant: current_data.direccion, value_act: $('textarea[name="direccion"]').val()},
        ]
        compare_data.forEach((data) => {
            if (data.value_ant != data.value_act){
                changes.push(data);
            }
        });        
    }
    $('#data_list tbody').on('click', 'a[rel="edit"]', function () {        
            $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
          const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
          const data = $("#data_list").DataTable().row(tr.row).data();
          $('.modal-title').find('span').html('Edición de una Unidad');
          $('input[name="nombre"]').val(data.nombre);
           $('textarea[name="direccion"]').val(data.direccion);
          $('input[name="action"]').val('edit');
          $('input[name="id"]').val(data.id);
          $('input[name="rif"]').val(data.rif);
          $('input[name="ced_resp"]').val(data.ced_resp);
          $('input[name="nombrejefe"]').val(data.nombrejefe);
          $('input[name="email"]').val(data.email);
          $('input[name="tlf"]').val(data.tlf);
          $('select[name="tipo_unidad"]').val(data.tipo_unidad.id);
          if (data.solic_almacen == true) {
            //$("#idactivo").val(1).change();
            $("#id_almacen").prop('checked', 1);
            } else {
            //$("#idactivo").val(0).change();
            $("#id_almacen").prop('checked', 0);
        }
          current_data = data;
          $('#myModalUnidad').modal('show');
    });
      $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar la unidad' + '<b style="color: #304ffe;">' + data.nombre + '?</b>', parameters, function () {
            sweet_info('Registro eliminado con exito'); 
            dttUnidad.row(tr.row).remove().draw();
        });
      });     

      $('#frmUnidad').on('submit', function (e) {
        e.preventDefault();
        let myForm = document.getElementById('frmUnidad');
        let parameters = new FormData(myForm);
        const url=window.location.pathname;
        let title="";
        let text = "";
        let update = false
        if  ($('input[name="action"]').val() == 'add'){
            title="¿Estas seguro de crear la unidad?";
            text = 'creado';
        }else{
            changes = [];
            audit_data();
            title="¿Estas seguro de actualizar la unidad?";
            text = 'modificado';
            update = true
        }
        submit_with_ajax(url, 'Estimado(a) Usuario  ', title, parameters, function () {        
            $('#myModalUnidad').modal('hide');
           sweet_info(`El registro se ha ${text} con exito`);
           dttUnidad.ajax.reload();
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
                // callback(data);
                return false;
            }                       
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {                        
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
      }
});

