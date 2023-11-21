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

let arrayObjectAccess = [];
const checkAllAccess = $("#checkAllAccess");

$(checkAllAccess).on("change", function () {
  if (checkAllAccess.prop("checked")) {
    console.log('ALccess');
  let rows = access.rows({ search: "applied" }).nodes();
    arrayObjectAccess = [];
    $('input[type="checkbox"]', rows).prop("checked", this.checked);
    $(".objectCheck:checked").each(function (value, key) {
      arrayObjectAccess.push(parseInt($(this).val()));
      
    });
  } else {
    arrayObjectAccess = [];
    $('#data_access tbody input[type="checkbox"]').prop("checked", false);
  }
  console.log('ALL', arrayObjectAccess);
  });

  //PARA GUARDAR LOS ID DE LOS REGISTROS EN MI ARRAY CUANDO SELECCIONO LOS CHECKBOX   
  $('#data_access tbody').on('change', 'input[type="checkbox"]', function () {
    let tr = access.cell($(this).closest('td, li')).index();
    let id = access.row(tr.row).data().id;

    if ($(this).is(':checked')) {
      arrayObjectAccess.push(id);
    } else {
      let index = arrayObjectAccess.indexOf(id);
      if (index > -1) {
        arrayObjectAccess.splice(index, 1);
      }
    }
    let allChecked = true;
    if (arrayObjectAccess.length == 0) {
      $(checkAllAccess).prop('checked', false);
      return false;
    } else {
      allChecked = true;
    }
    $(checkAllAccess).prop('checked', allChecked);
    console.log('SINGLE', arrayObjectAccess);
  });

  //PARA ESCUCHAR El CLICK EN LAS OPCIONES DE MI DROPDOWN Y ENVIAR LOS ID DE MIS REGISTROS A MI VISTA DE DJANGO
  $('.delete_access').on('click', function () {
    if (arrayObjectAccess.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObjectAccess.length > 1 ? text = 'elementos han sido eliminados con exito' : text = 'elemento ha sido eliminado con exito';
    let parameters = new FormData();
      parameters.append('action', 'delete_multiple_access');
      parameters.append('id', JSON.stringify(arrayObjectAccess));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObjectAccess.length} ${text}`);
        access.ajax.reload();
        $(checkAllAccess).prop('checked', false)
        arrayObjectAccess = [];
      });
  });