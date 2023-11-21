let tblSal;
let param_id = "";
let input_daterange;  

let salida = {
    list: function (all) {
        let parameters = {
            'action': 'searchdata',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblSal = $('#data_list').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: '/erp/salida/list/',
                //url: window.location.pathname,
                type: 'POST',
                data: parameters,
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
                search: "<button class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
                searchPlaceholder: "Buscar",
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
            order: false,
            //paging: false,
            ordering: false,
            //info: false,
            //searching: false,            
            columns: [
                {
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": ''
                },
                {"data": "codigo"},
                {"data": "tipo_salida.denominacion"},
                {"data": "origen"},
                {"data": "destino"}, 
                {"data": "fecha"},
                {"data": "total"},
                {"data": "estado"},
                {"data": "id"},
            ],
            columnDefs: [
                  {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                  },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.estado == 'RECHAZADO'){
                            return '<i class="fa fa-times c-red" style="font-size: 13px;"><tool-tip role="tooltip"> Rechazado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        } 
                        else if(row.estado == 'APROBADO'){
                            return '<i class="fa fa-check c-green" style="font-size: 13px;"><tool-tip role="tooltip"> Aprobado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        }
                        else if(row.estado == 'POR APROBAR'){
                            return '<i class="fa fa-clock c-purple" style="font-size: 13px;"></i><tool-tip role="tooltip"> Por Aprobar</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>'; 
                        }
                        else if(row.estado == 'RETORNADO'){
                            return '<i class="fa fa-sync c-blue" style="font-size: 13px;"></i><tool-tip role="tooltip"> Retornada</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>'; 
                        } 
                        return '<i class="fa fa-pen c-yellow" style="font-size: 13px;"><tool-tip role="tooltip"> En Creación</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>'; 
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    // width: "14%",
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.estado !== 'EN CREACIÓN'){                            
                            let buttons = '<a href="/erp/salida/detail/' + row.id + '/" class="btn btn-success btn-xs" data-toggle="tooltip" title="Consultar Detalle"><i class="fas fa-search"></i></a> ';
                            buttons += '<a href="/erp/salida/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs" data-toggle="tooltip" title="PDF"><i class="fas fa-file-pdf"></i></a> ';
                            return buttons;
                        }else{
                            let buttons = '<a href="/erp/salida/update/' + row.id + '/" class="btn btn-warning btn-xs" data-toggle="tooltip" title="Editar"><i class="fas fa-edit" style="color: #ffffff;"></i></a> ';
                            buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs" data-toggle="tooltip" title="Eliminar"><i class="fas fa-trash-alt"></i></a> ';
                            buttons += '<a href="/erp/salida/detail/' + row.id + '/" class="btn btn-success btn-xs" data-toggle="tooltip" title="Consultar Detalle"><i class="fas fa-search"></i></a> ';
                            return buttons;
                        }
                        }
                    },
                ],
                initComplete: function (settings, json) {
            }
                
        });              
    },
    //Bienes Muebles
    formatRowHtml: function (data) {
        let html = '<table class="table">';
        html += '<thead class="thead-dark2 text-uppercase">';
        html += '<tr><th scope="col">Producto</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<th scope="col">Precio</th>';
        html += '<th scope="col">Ubicación Fisica</th>';
        html += '<th scope="col">Codigo de Bien</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(data, function (key, value) {
            html+='<tr>'
            html+='<td>'+value.product+'</td>'
            html+='<td>'+value.category+'</td>'
            html+='<td>'+value.price+' Bs</td>'
            html+='<td>'+value.codubica+'</td>'
            html+='<td>'+value.codbien+'</td>'
            html+='</tr>';
        });
        html += '</tbody>';
        return html;
    },
    //Materiales de Consumo
    formatRowHtml2: function (data) {
        let html = '<table class="table">';
        html += '<thead class="thead-dark2 text-uppercase">';
        html += '<tr><th scope="col">Producto</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<th scope="col">Cantidad</th>';
        html += '<th scope="col">Precio</th>';
        html += '<th scope="col">Número de lote</th>';
        html += '<th scope="col">Fecha de Vencimiento</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(data, function (key, value) {
            html+='<tr>'
            html+='<td>'+value.products+'</td>'
            html+='<td>'+value.categoria+'</td>'
            html+='<td>'+value.cantidad+'</td>'
            html+='<td>'+value.precio+' Bs</td>'
            html+='<td>'+value.lote+'</td>'
            html+='<td>'+value.fecha_venc+'</td>'
            html+='</tr>';
        });
        html += '</tbody>';
        return html;
    }
};

$(function () {
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        salida.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        salida.list(true);
    });
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = tblSal.cell($(this).parents('td, li')).index();
        const data = tblSal.row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);       
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación',`¿Estas seguro de eliminar la Distribución ${data.codigo}?`, parameters, function () {
            tblSal.row(tr.row).remove().draw();
        });
      });
      $('#data_list tbody').on('click', 'a[rel="detail"]', function() {
        const tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        if (data.det > 0){
            parameters.append('action', 'detail_bm');
        } else if (data.tipo_salida.bienes == 'MTC'){
            parameters.append('action', 'detail_mc');
        }
        parameters.append('id', data.id);
        $.ajax({
          url: window.location.pathname,
          type: 'POST',
          data: parameters,
          dataType: 'json',
          processData: false,
          contentType: false,
          success: function(response) {
            if (data.det > 0){
                response.forEach((resp)=>{
                    $('#concept').text(data.tipo_salida.denominacion);
                    $('#date').text(data.fecha);
                    $('#user').text(resp.user);
                    $('#status').text(data.estado);
                    $('#almacen').text(data.origen);
                    $('#resp_almacen').text(resp.resp_almacen);
                    $('#destino').text(data.destino);
                    $('#resp_destino').text(resp.resp_destino);
                    $('#comprob').text(resp.comprob);
                    $('#nro_comprob').text(resp.nro_comprob);
                    $('#obs').text(resp.observ);
                    $('#subtotal').text(resp.subtotal);
                    $('#iva').text(resp.iva + '%');
                    $('#total').text(data.total);
                })
                $('#tblDetalleProd').DataTable({
                    responsive: false,
                    autoWidth: false,
                    destroy: true,
                    data: response,
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
                        search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
                        searchPlaceholder: "Buscar",
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
                    
                        {"data": "product"},
                        {"data": "categoria"},
                        {"data": "precio"},
                        {"data": "codbien", className: "text-left"},
                        {"data": "codubica", className: "text-left"},
                    ],
                    columnDefs: [
                        {
                            targets: [-3],
                            class: 'text-left',
                            render: function (data, type, row) {
                                return parseFloat(data).toFixed(2) + ' Bs.';
                            }
                        },                    
                    ],
                    initComplete: function (settings, json) {
                    }
                    
                });
                $('#detail_bm').find('span').html('Consulta Detalle de la Distribución:  ' + data.codigo);
                $('#detail_bm').find('i').removeClass().addClass('fas fa-search');
                $('#modal_detail_bm').modal('show');
            }else{
                response.forEach((resp)=>{
                    $('#concept_mc').text(data.tipo_salida.denominacion);
                    $('#date_mc').text(data.fecha);
                    $('#user_mc').text(resp.user);
                    $('#status_mc').text(data.estado);
                    $('#almacen_mc').text(data.origen);
                    $('#resp_almacen_mc').text(resp.resp_almacen);
                    $('#destino_mc').text(data.destino);
                    $('#resp_destino_mc').text(resp.resp_destino);
                    $('#comprob_mc').text(resp.comprob);
                    $('#nro_comprob_mc').text(resp.nro_comprob);
                    $('#obs_mc').text(resp.observ);
                })
                $('#tblDetalleMc').DataTable({
                    responsive: false,
                    autoWidth: false,
                    data: response,
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
                        search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
                        searchPlaceholder: "Buscar",
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
                        {"data": "products"},
                        {"data": "categoria"},
                        {"data": "precio", className: "text-center"},
                        {"data": "cantidad", className: "text-center"},
                        {"data": "lote", className: "text-center"},
                        {"data": "fecha_venc", className: "text-center"},
                    ],
                    initComplete: function (settings, json) {
                    }
                });
                $('#detail_mc').find('span').html('Consulta Detalle de la Distribución:  ' + data.codigo);
                $('#detail_mc').find('i').removeClass().addClass('fas fa-search');
                $('#modal_detail_mc').modal('show');
               }            
          },
          error: function(error) {
          }
      });
    }) 
    .on('click', 'td.details-control', function () {
        let tr = $(this).closest('tr');
        let row =  tblSal.row(tr);
        let id=row.data().id;
        let tipo_salida=row.data().det;
        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            let parameters = new FormData();
            if (tipo_salida > 0){
                parameters.append('action', 'detail_bm');
                parameters.append('id', id);
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: parameters,
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                }).done(function (data) {
                   // console.log(data);
                    if (!data.hasOwnProperty('error')) {
                        row.child(salida.formatRowHtml(data)).show();
                        tr.addClass('shown');
                        //callback(data);
                        return false;
                    }
                    message_error(data.error);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {
                });
            }else{
                parameters.append('action', 'detail_mc');
                parameters.append('id', id);
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: parameters,
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                }).done(function (data) {
                   // console.log(data);
                    if (!data.hasOwnProperty('error')) {
                        row.child(salida.formatRowHtml2(data)).show();
                        tr.addClass('shown');
                        //callback(data);
                        return false;
                    }
                    message_error(data.error);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {
                });
            }             
        }        
    });
    salida.list(false);
});
    
    

