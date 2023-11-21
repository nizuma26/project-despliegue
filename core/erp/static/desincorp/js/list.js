let tblDesinc;
let input_daterange;
let param_id = "";

let desincorp = {
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
        tblDesinc = $('#data_list').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: '/erp/desinc/list/',
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
            order: false,
            ordering: false,
            columns: [
                {
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": ''
                },
                {"data": "cod_desinc"},
                {"data": "tipo_desinc"},
                {"data": "origen"},            
                {"data": "fecha_desinc"},
                {"data": "estado"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.estado == 'REC'){
                            return '<i class="fa fa-times c-red" style="font-size: 13px;"><tool-tip role="tooltip"> Rechazado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        } 
                        else if(row.estado == 'APR'){
                            return '<i class="fa fa-check c-blue" style="font-size: 13px;"><tool-tip role="tooltip"> Aprobado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        }
                        else if(row.estado == 'PAP'){
                            return '<i class="fa fa-clock c-purple" style="font-size: 13px;"></i><tool-tip role="tooltip"> Por Aprobar</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>'; 
                        } 
                        return '<i class="fa fa-pen c-yellow" style="font-size: 13px;"><tool-tip role="tooltip"> En Creación</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                    } 
                },
                {            
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.estado == 'APR' || row.estado == 'PAP'){
                            let buttons = '<a rel="detail" class="btn btn-success btn-xs" data-toggle="tooltip" title="Consultar Detalle"><i class="fas fa-search"></i></a> ';
                            buttons += '<a href="/erp/desinc/factura/pdf/' + row.id + '/" target="_blank"class="btn btn-info btn-xs" data-toggle="tooltip" title="PDF"><i class="fas fa-file-pdf"></i></a> ';                    
                            return buttons;
    
                        }else{
                            let buttons = '<a href="/erp/desinc/update/' + row.id + '/" class="btn btn-warning btn-xs" data-toggle="tooltip" title="Editar"><i class="fas fa-edit" style="color: #ffffff;"></i></a> ';
                            buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt" data-toggle="tooltip" title="Eliminar"></i></a> ';
                            buttons += '<a rel="detail" class="btn btn-success btn-xs"><i class="fas fa-search" data-toggle="tooltip" title="Consultar Detalle"></i></a> ';
                            return buttons;
                        }
                    
                        }
                    },
            ],
            initComplete: function (settings, json) {
            }
        });        

    },
    formatRowHtml: function (data) {
        let html = '<table class="table text-uppercase">';
        html += '<thead class="thead-dark2">';
        html += '<tr><th scope="col">Producto</th>';
        html += '<th scope="col">Categoria</th>';
        html += '<th scope="col">Ubicación Física</th>';
        html += '<th scope="col">Cod. Bien</th></t>';
        html += '</thead>';
        html += '<tbody>';
        $.each(data, function (key, value) {
            html+='<tr>'
            html+='<td>'+value.products+'</td>'
            html+='<td>'+value.category+'</td>'
            html+='<td>'+value.depart+'</td>'
            html+='<td>'+value.codbien+'</td>'
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
        desincorp.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        desincorp.list(true);
    });

      $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = tblDesinc.cell($(this).parents('td, li')).index();
        const data = tblDesinc.row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar la desincorporación?  ' + '<b style="color: #304ffe;">' + data.cod_desinc + '</b>', parameters, function () {
            sweet_info('Registro eliminado con exito'); 
            tblDesinc.row(tr.row).remove().draw();
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
            response.forEach((resp)=>{
                $('#concept').text(data.tipo_desinc);
                $('#date').text(data.fecha_desinc);
                $('#user').text(resp.user);
                $('#status').text(data.estado);
                $('#unidad').text(data.origen);
                $('#resp_origen').text(resp.resp_origen);
                $('#obs').text(resp.observ);
            })            
            $('#tblDetalleProdDesinc').DataTable({
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
                    {"data": "products"},
                    {"data": "category"},
                    {"data": "codbien"},
                    {"data": "depart"},
                ],                
                initComplete: function (settings, json) {

                }
            });
            $('#desinc_title').find('span').html('Detalle de la Desincorporación:  ' + data.cod_desinc);
            $('#desinc_detail').modal('show');
          },
          error: function(error) {
          }
        });
      
    }).on('click', 'td.details-control', function () {
            let tr = $(this).closest('tr');
            let row =  tblDesinc.row(tr);
            let id=row.data().id;
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                let parameters = new FormData();
                 parameters.append('action', 'detail');
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
                         row.child(desincorp.formatRowHtml(data)).show();
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
         });
        showDropdown('dropdown-content','dropdown-button');
        desincorp.list(false);

});
