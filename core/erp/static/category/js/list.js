let data_list;
let current_data = {};
let changes = [];
$(function () {
  data_list = $("#data_list").DataTable({
    responsive: false,
    autoWidth: false,
    destroy: true,
    deferRender: true,
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
      search:
        "<button type='button' class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
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
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        action: "searchdata",
      },
      dataSrc: "",
    },
    columns: [
      { data: "id" },
      { data: "id", className: 'text-center' },
      { data: "nombre" },
      { data: "id" },
    ],
    columnDefs: [
      {
        targets: [-4],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          return (
            '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' +
            row.id + '" name="product" value="' + row.id + '"><span class="checkmark"></span></label>'
          );
        },
      },
      {
        targets: [-3],
        class: "text-center",
        orderable: true,
        render: function (data, type, row) {
          return data;
        },
      },
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          var buttons =
            '<a rel="edit" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
          buttons += '<a rel="delete" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        },
      },
    ],
    initComplete: function (settings, json) { },
  });
  $('select[name="action"]').on('change', function () {
    if ($('select[name="action"]').val() == 'NULL') {
      return false;
    }
    else if (arrayObject.length == 0) {
      $('select[name="action"]').val('NULL');
      return info()
    }
    else if ($('select[name="action"]').val() == "INACTIVE") {
      var parameters = new FormData();
      parameters.append('action', 'inactive_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de inactivar los registros seleccionados?', parameters, function () {
        sweet_info('Los registros seleccionados han sido inactivados con exito');
        data_list.ajax.reload();
        $('select[name="action"]').val('NULL');
        $(checkAll).prop('checked', false);
        arrayObject = [];
      });
    } else if ($('select[name="action"]').val() == "ACTIVE") {
      var parameters = new FormData();
      parameters.append('action', 'active_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de activar los registros seleccionados?', parameters, function () {
        sweet_info('Los registros seleccionados han sido activados con exito');
        data_list.ajax.reload();
        $('select[name="action"]').val('NULL');
        $(checkAll).prop('checked', false)
        arrayObject = [];
      });
    } else if ($('select[name="action"]').val() == "DELETE") {
      var parameters = new FormData();
      parameters.append('action', 'delete_multiple');
      parameters.append('id', JSON.stringify(arrayObject));
      const url = window.location.pathname;
      submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar los registros seleccionados?', parameters, function () {
        sweet_info('Los registros seleccionados han sido eliminados con exito');
        data_list.ajax.reload();
        $('select[name="action"]').val('NULL');
        $(checkAll).prop('checked', false)
        arrayObject = [];
      });
    }
  });
  $(".btnAdd").on("click", function () {
    $('input[name="action"]').val("add");
    $("#modaltitle3").find("span").html("Creando Nueva Categoría");
    $("#modaltitle3").find("i").removeClass().addClass("fas fa-plus");
    $("#idnombrecateg").focus();
    $("#modalCategory").modal("show");
  });
  $("#modalCategory").on("shown.bs.modal", function () {
    const inputs = document.querySelectorAll("#modalCategory .txt_field input");
    inputs.forEach((input) => {
      if (input.value.trim() !== "") {
        input.classList.add("input-has-text");
      }
      input.addEventListener("input", () => {
        if (input.value.trim() !== "") {
          input.classList.add("input-has-text");
        } else {
          input.classList.remove("input-has-text");
        }
      });
    });
  });
  $("#modalCategory").on("hidden.bs.modal", function (e) {
    $("#frmCatgorias").trigger("reset");
    const inputs = document.querySelectorAll("#modalCategory .txt_field input");
    inputs.forEach((input) => input.classList.remove("input-has-text"));
  });
});
$("#data_list tbody").on("click", 'a[rel="edit"]', function () {
  let tr = $("#data_list").DataTable().cell($(this).parents("td, li")).index();
  let data = $("#data_list").DataTable().row(tr.row).data();
  $(".modal-title").find("i").removeClass().addClass("fas fa-edit");
  $(".modal-title").find("span").html("Edición de una categoría");
  param_id = data.id;
  $('input[name="action"]').val("edit");
  $('input[name="id"]').val(data.id);
  $('input[name="nombre"]').val(data.nombre);
  $("#modalCategory").modal("show");
  current_data = data
});
$("#data_list tbody").on("click", 'a[rel="delete"]', function () {
  let tr = $("#data_list").DataTable().cell($(this).parents("td, li")).index();
  let data = $("#data_list").DataTable().row(tr.row).data();
  let parameters = new FormData();
  parameters.append("action", "delete");
  parameters.append("id", data.id);
  url = window.location.pathname;
  submit_with_ajax(url, "Notificación", "¿Estas seguro de eliminar la categoria?  " + '<b style="color: #304ffe;">' + data.nombre + "</b>", parameters, function () {
    sweet_info("El Registro Ha Sido Eliminado Con Exito");
    data_list.row(tr.row).remove().draw();
  }
  );
});
//PARA VERIFICAR SI LOS DATOS DEL REGISTRO SE HAN MODIFICADO O SIGUEN IGUAL
function audit_data() {
  const value = $('input[name="nombre"]').val();
  if (current_data.nombre != value) {
    changes.push({ field: 'Nombre', value_ant: current_data.nombre, value_act: value });
  }
}
$("#frmCatgorias").on("submit", function (e) {
  e.preventDefault();
  let myForm = document.getElementById("frmCatgorias");
  let parameters = new FormData(myForm);
  const url = window.location.pathname;
  let titulo = "";
  let text = "";
  if ($('input[name="action"]').val() == "add") {
    titulo = "¿Estas seguro de crear la categoria?";
    text = "creado";
  } else {
    changes = [];
    audit_data();
    titulo = "¿Estas seguro de actualizar la categoria?";
    text = "modificado";
  }
  submit_with_ajax(url, "Estimado usuario(a)", titulo, parameters, function (response) {
    $("#modalCategory").modal("hide");
    sweet_info("El registro ha sido " + text + " con exito");
    data_list.ajax.reload();
    if (changes.length > 0) {
      field_save()
    }
  }
  );
});
function field_save() {
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
