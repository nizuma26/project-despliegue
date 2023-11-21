let data_list = ""; 
//let prod_data = []


let product = {
  list: function () {
    data_list = $('#data_list').DataTable({
      responsive: false,
      autoWidth: false,
      destroy: true,
      //data: data,
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
          search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
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
      ordering: true,
      columns: [
          {"data": "id"},
          {"data": "imagen"},
          {"data": "codigo"},
          {"data": "nombre"},
          {"data": "categoria"},
          {"data": "marca"},
          {"data": "modelo"},
          {"data": "activo"},
          {"data": "id"},
      ],
      
      columnDefs: [
          {
            targets: [-9],
            searchable: false,
            orderable: false,
            className: 'text-center',
            render: function (data, type, row) {
                return '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' + row.id + '" name="product" value="' + row.id + '"><span class="checkmark"></span></label>';
            }
          },

            {
              targets: [-8],
              class: 'text-center',
              orderable: false,
              render: function (data, type, row) {
                  return '<img src="'+data+'" class="img-fluid img-thumbnail d-block mx-auto" style="width: 33px; height: 33px;">';
              }
            },        
            {
              targets: [-2],
              class: 'text-center',
              //orderable: true,
              render: function (data, type, row) {
                  if(row.activo){return '<a><tool-tip role="tooltip"> Activo</tool-tip><i class="fa fa-check c-blue" style="font-size: 13px;"><span style="display:none;">'+'activo'+'</span></i></a>'
                  }else{return '<a><tool-tip role="tooltip"> Inactivo</tool-tip><i class="fa fa-times c-red" style="font-size: 13px;"><span style="display:none;">'+'inactivo'+'</span></i></a>'}
              }
          },
          {
              targets: [-1],
              class: 'text-center',
              orderable: false,
              render: function (data, type, row) {
                  let buttons = '<a href="/erp/product/update/'+ row.id +'/" class="btn btn-warning btn-xs btnEdit"><tool-tip role="tooltip"> Editar</tool-tip><i class="fas fa-pen"></i></a> ';
                  if(row.activo){ buttons += '<a rel="inactivar" class="btn btn-orange btn-xs inactive"><tool-tip role="tooltip"> Inactivar Registro</tool-tip><i class="fas fa-unlink"></i></a> ';                        
                  }else{ buttons += '<a rel="activar" class="btn btn-info btn-xs btn_active"><tool-tip role="tooltip"> Activar Registro</tool-tip><i class="fas fa-check-circle"></i></a> '};   
                  buttons += '<a rel="detail" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Información del Producto</tool-tip><i class="fas fa-search"></i></a> ';
                  buttons += '<a rel="historical" class="btn btn-secondary btn-xs"><tool-tip role="tooltip"> Histórico</tool-tip><i class="fas fa-file-medical"></i></a> ';
                  buttons += '<a rel="delete" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a> ';
                  return buttons;
                  }
              },
          ],
          initComplete: function (settings, json) {
          }
      });    
  }
};

$(function () {
  //search_data()
  product.list();
  function detail(response){
    $("#detalle_prod").modal('show');
    $('#detail_prod').find('span').html('Información del Producto: ');
    $('#detail_prod').find('i').removeClass().addClass('fas fa-info-circle');
    $.each(response, function (key, value) {
      $('#image').html('<img src="'+ value.imagen +'" style="width: 120px; height: 110px;" class="img-fluid" alt="User Image">');
      $('#codigo').html('<span class="title-custom">' + value.codigo + '</span>');
      $('#first_name').text(value.nombre);
      $('#last_name').text(value.categoria);	
      $('#dni').text(value.marca);	
      $('#email').text(value.modelo);
      $('#fecha').text(value.grupo);
      $('#sesion').text(value.subgrupo);
      $('#medida').text(value.unidad_medida);
      $('#moneda').text(value.moneda);
      $('#desc').text(value.descripcion);     
      if(value.activo){
          $('#active').html('<i class="fas fa-check"></i>');
      }else{
          $('#active').html('<i class="fas fa-times"></i>');
      }
      if(value.pagaimpuesto){
        $('#imp').html('<i class="fas fa-check"></i>');
      }else{
          $('#imp').html('<i class="fas fa-times"></i>');
      }
      if(value.inventariable){
        $('#inv').html('<i class="fas fa-check"></i>');
      }else{
          $('#inv').html('<i class="fas fa-times"></i>');
      } 
      if(value.lote){
        $('#lote').html('<i class="fas fa-check"></i>');
      }else{
          $('#lote').html('<i class="fas fa-times"></i>');
      } 
      if(value.serie){
        $('#serie').html('<i class="fas fa-check"></i>');
      }else{
          $('#serie').html('<i class="fas fa-times"></i>');
      }
  });
  }
   $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
    var tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    var data = $("#data_list").DataTable().row(tr.row).data();
    var parameters = new FormData();
    parameters.append('action', 'delete');
    parameters.append('id', data.id);
    const url = "/erp/product/delete/"+data.id+"/";
    submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el producto?  ' + '<b style="color: #1e88e5;">' + data.codigo + ' / ' + data.nombre  + '</b>', parameters, function () {
      sweet_info( 'Registro eliminado con exito');
      data_list.row(tr.row).remove().draw();
    });
  });
  $('#data_list tbody').on('click', 'a[rel="detail"]', function() {
    const tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
    const data = $("#data_list").DataTable().row(tr.row).data();
    $.ajax({
      url: window.location.pathname,
      type: 'POST',
      data: {
          'action': 'detail',
          'id': data.id
      },        
      success: function(response) {
          detail(response);
          
          $('#elemento').html(response);
      },
      error: function(error) {
      }
  });
});
$('#data_list tbody').on('click', 'a[rel="historical"]', function () {
  const tr =$("#data_list").DataTable().cell($(this).closest('td, li')).index();
  const data = $("#data_list").DataTable().row(tr.row).data();
  $.ajax({
      url: window.location.pathname,
      type: 'POST',
      data: {
          'action': 'historical',
          'id': data.id
      },
      success: function (response) {
          let html = '<table class="table max-cont table-sm table-hover" width="100%">';
          html += '<thead>';
          html += '<tr><th scope="col" style="width: 20%;">FECHA</th>';
          html += '<th scope="col" style="width: 40%;">USUARIO</th>';
          html += '<th scope="col" style="width: 20%;">ACCIÓN</th>';
          html += '<th scope="col" style="width: 20%;">DISPOSITIVO</th></tr>';
          html += '</thead>';
          html += '<tbody style="font-size: 14px;">';
              $.each(response, function (key, value) {
                  html += '<tr>'
                  html += '<td>' + value.date_joined + '</td>'
                  html += '<td>' + value.user + '</td>'
                  html += '<td>' + value.action + '</td>'
                  html += '<td>' + value.device + '</td>'
                  html += '</tr>';
              });
          html += '</tbody>';
          html += '</table>';
          $('#table_historical').html(html);
      },
      
      error: function (error) {
      }
  });
  $("#historical").modal('show');
  $('#historical_title').find('span').html(`Histórico: <span style="font-size: 15px;">${data.codigo} - ${data.nombre}</span>`);
  $('#historical_title').find('i').removeClass().addClass('fas fa-clipboard-list');
});  
  $('#data_list tbody').on('click', '.btn_active', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-check-circle');
    var tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
    var data = $("#data_list").DataTable().row(tr.row).data();
    var parameters = new FormData();
    parameters.append('action', 'activar');
    parameters.append('id', data.id);       
    const url = window.location.pathname;
    submit_with_ajax(url, 'Activar Producto', '¿Estas seguro de activar el producto ' + '<b style="color: #1e88e5;">' + data.nombre + '</b>?', parameters, function () {
      sweet_info( 'El Registro ha sido activado con exito');
      $('td:eq(7)', data_list.row(tr.row).node()).find('i').removeClass().addClass('fas fa-check c-blue');
      $('td:eq(8)', data_list.row(tr.row).node()).find('a.btn-info').removeClass().addClass('btn btn-xs btn-orange  inactive');
      $('td:eq(8)', data_list.row(tr.row).node()).find('i.fa-check-circle').removeClass().addClass('fas fa-unlink');
      //data_list.ajax.reload();
    });
  });
  $('#data_list tbody').on('click', '.inactive', function () {
    $('.modal-title').find('i').removeClass().addClass('fas fa-check-circle');
    const tr = data_list.cell($(this).parents('td, li')).index();
    const data = data_list.row(tr.row).data();
    let parameters = new FormData();
    parameters.append('action', 'inactivar');
    parameters.append('id', data.id);       
    const url = window.location.pathname;
    submit_with_ajax(url, 'Inactivar Producto', '¿Estas seguro de inactivar el producto ' + '<b style="color: #1e88e5;">' + data.nombre + '</b>?', parameters, function () {
      sweet_info( 'El Registro ha sido inactivado con exito');
      $('td:eq(7)', data_list.row(tr.row).node()).find('i').removeClass().addClass('fas fa-times c-red');
      $('td:eq(8)', data_list.row(tr.row).node()).find('a.btn-orange').removeClass().addClass('btn btn-xs btn-info btn_active');
      $('td:eq(8)', data_list.row(tr.row).node()).find('i.fa-unlink').removeClass().addClass('fas fa-check-circle');
     //data_list.ajax.reload();
    });
           
  });
  showDropdown('dropdown-content','dropdown-button');
});
