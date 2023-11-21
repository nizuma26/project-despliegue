//SELECCIONAR TODOS MIS REGISTROS
function info(){
    Swal.fire({
        title: 'Notificación!',
        text: 'Debe seleccionar al menos un elemento de la lista para realizar esta acción',
        icon: 'info',
        timer: 4000,
        timerProgressBar: true,
        confirmButtonText: '<i class="fa fa-thumbs-up"></i> OK!',
        confirmButtonColor: '#289aff',
    });
}

let arrayObject = [];
const checkAll = $("#checkAll");
const checkboxes = $('#data_list tbody input[type="checkbox"]');

$(checkAll).on("change", function () {
    if ($("#checkAll").prop("checked")) {
      let rows = data_list.rows({ search: "applied" }).nodes();
      arrayObject = [];
      $('input[type="checkbox"]', rows).prop("checked", this.checked);
      $(".objectCheck:checked").each(function (value, key) {
        arrayObject.push(parseInt($(this).val()));
      });
    } else {
      arrayObject = [];
      $('#data_list tbody input[type="checkbox"]').prop("checked", false);
    }
    console.log('ALL', arrayObject);
  });

  //PARA GUARDAR LOS ID DE LOS REGISTROS EN MI ARRAY CUANDO SELECCIONO LOS CHECKBOX   
  $('#data_list tbody').on('change', 'input[type="checkbox"]', function () {
    let tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
    let id = $("#data_list").DataTable().row(tr.row).data().id;

    if ($(this).is(':checked')) {
      arrayObject.push(id);
    } else {
      let index = arrayObject.indexOf(id);
      if (index > -1) {
        arrayObject.splice(index, 1);
      }
    }
    let allChecked = true;
    if (arrayObject.length == 0) {
      $(checkAll).prop('checked', false);
      return false;
    } else {
      allChecked = true;
    }
    $(checkAll).prop('checked', allChecked);
    console.log('SINGLE', arrayObject);
  });

  //PARA ESCUCHAR EL CAMBIO EN MI SELECT ACTION Y ENVIAR LOS ID DE MIS REGISTROS A MI VISTA DE DJANGO
  $('.disabled').on('click', function () {
    if (arrayObject.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObject.length > 1 ? text = 'elementos han sido inactivados con exito' : text = 'elemento ha sido inactivado con exito';
    let parameters = new FormData();
      parameters.append('action', 'inactive_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;

      submit_with_ajax(url, 'Notificación', '¿Estas seguro de inactivar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObject.length} ${text}`);
        data_list.ajax.reload();        
        $(checkAll).prop('checked', false);
        arrayObject = [];
      });            
  });
  $('.is_active').on('click', function () {
    if (arrayObject.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObject.length > 1 ? text = 'elementos han sido activados con exito' : text = 'elemento ha sido activado con exito'; 
    let parameters = new FormData();
      parameters.append('action', 'active_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de activar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObject.length} ${text}`);
        data_list.ajax.reload();
        $(checkAll).prop('checked', false)
        arrayObject = [];
      }); 
  });
  $('.delete').on('click', function () {
    if (arrayObject.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObject.length > 1 ? text = 'elementos han sido eliminados con exito' : text = 'elemento ha sido eliminado con exito';
    let parameters = new FormData();
      parameters.append('action', 'delete_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObject.length} ${text}`);
        data_list.ajax.reload();
        $(checkAll).prop('checked', false)
        arrayObject = [];
      });
  });
  $('.complete').on('click', function () {
    if (arrayObject.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObject.length > 1 ? text = 'solicitudes han sido eliminados con exito' : text = 'elemento ha sido eliminado con exito';
    let parameters = new FormData();
      parameters.append('action', 'delete_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObject.length} ${text}`);
        data_list.ajax.reload();
        $(checkAll).prop('checked', false)
        arrayObject = [];
      });
  });