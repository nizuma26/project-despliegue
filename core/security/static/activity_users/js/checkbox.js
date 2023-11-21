//SELECCIONAR TODOS MIS REGISTROS
let arrayObjectHistorical = [];
const checkAllHistorical = $("#checkAllHistorical");

$(checkAllHistorical).on("change", function () {
  if (checkAllHistorical.prop("checked")) {
    let rows = activity.rows({ search: "applied" }).nodes();
    arrayObjectHistorical = [];
    $('input[type="checkbox"]', rows).prop("checked", this.checked);
    $(".objectCheck:checked").each(function (value, key) {
      arrayObjectHistorical.push(parseInt($(this).val()));
      
    });
  } else {
    arrayObjectHistorical = [];
    $('#data_activity tbody input[type="checkbox"]').prop("checked", false);
  }
  console.log('ALL', arrayObjectHistorical);
  });

  //PARA GUARDAR LOS ID DE LOS REGISTROS EN MI ARRAY CUANDO SELECCIONO LOS CHECKBOX   
  $('#data_activity tbody').on('change', 'input[type="checkbox"]', function () {
    let tr = activity.cell($(this).closest('td, li')).index();
    let id = activity.row(tr.row).data().id;

    if ($(this).is(':checked')) {
      arrayObjectHistorical.push(id);
    } else {
      let index = arrayObjectHistorical.indexOf(id);
      if (index > -1) {
        arrayObjectHistorical.splice(index, 1);
      }
    }
    let allChecked = true;
    if (arrayObjectHistorical.length == 0) {
      $(checkAllHistorical).prop('checked', false);
      return false;
    } else {
      allChecked = true;
    }
    $(checkAllHistorical).prop('checked', allChecked);
    console.log('SINGLE', arrayObjectHistorical);
  });

  //PARA ESCUCHAR El CLICK EN LAS OPCIONES DE MI DROPDOWN Y ENVIAR LOS ID DE MIS REGISTROS A MI VISTA DE DJANGO
  $('.delete_historical').on('click', function () {
    if (arrayObjectHistorical.length == 0) {      
      return info()
    }   
    let text = '';
    arrayObjectHistorical.length > 1 ? text = 'elementos han sido eliminados con exito' : text = 'elemento ha sido eliminado con exito';
    let parameters = new FormData();
      parameters.append('action', 'delete_multiple_historical');
      parameters.append('id', JSON.stringify(arrayObjectHistorical));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar los elementos seleccionados?', parameters, function () {
        sweet_info(`${arrayObjectHistorical.length} ${text}`);
        activity.ajax.reload();
        $(checkAllHistorical).prop('checked', false)
        arrayObjectHistorical = [];
      });
  });