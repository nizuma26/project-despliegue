let tblIncorp;
let param_id = "";
let input_daterange;
let incorp = {
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
        tblIncorp = $('#data_list').DataTable({
            responsive: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: '/erp/ingreso/list/',
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
            columns: [
                {
                    "className": 'details-control',
                    "orderable": true,
                    "data": null,
                    "defaultContent": ''
                },
                {"data": "cod_ingreso", className: "text-center"},
                {"data": "almacen"},
                {"data": "tipo_ingreso"},
                {"data": "fecha_ingreso"},
                {"data": "subtotal"}, 
                {"data": "total"},
                {"data": "estado"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2)+ ' Bs.';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        if(row.estado == 'RECHAZADO'){
                            return '<i class="fa fa-times c-red" style="font-size: 13px;"><tool-tip role="tooltip"> Rechazado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        } 
                        else if(row.estado == 'APROBADO'){
                            return '<i class="fa fa-check c-blue" style="font-size: 13px;"><tool-tip role="tooltip"> Aprobado</tool-tip><span style="display:none;">'+row.estado.name+'</span></i>';
                        }
                        else if(row.estado == 'POR APROBAR'){
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
                        if(row.estado !== 'EN CREACIÓN'){                            
                            let buttons = '<a href="/erp/ingreso/detail/' + row.id + '/" target="_blank" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Consultar Detalle</tool-tip><i class="fas fa-search"></i></a> ';
                            buttons += '<a href="/erp/ingreso/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><tool-tip role="tooltip"> Ver PDF</tool-tip><i class="fas fa-file-pdf"></i></a> ';
                            return buttons;

                        }else{
                            let buttons = '<a href="/erp/ingreso/update/' + row.id + '/"  class="btn  btn-warning btn-xs"><tool-tip role="tooltip"> Editar</tool-tip><i class="fas fa-edit" style="color: #ffffff;"></i></a> ';
                            buttons += '<a href="/erp/ingreso/detail/' + row.id + '/" target="_blank" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Consultar Detalle</tool-tip><i class="fas fa-search"></i></a> ';
                            buttons += '<a rel="delete" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a> ';
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
        let html = '<table class="table table-sm">';
        html += '<thead class="thead-dark2">';
        html += '<tr><th scope="col">PRODUCTO</th>';
        html += '<th scope="col">CATEGORÍA</th>';
        html += '<th scope="col">PRECIO</th>';
        html += '<th scope="col">CANTIDAD</th>';
        html += '<th scope="col">SUBTOTAL</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(data, function (key, value) {
            html+='<tr>'
            html+='<td>'+value.product+'</td>'
            html+='<td>'+value.category+'</td>'
            html+='<td>'+value.price+' Bs.</td>'
            html+='<td>'+value.cant+'</td>'
            html+='<td>'+value.subtotal+' Bs.</td>'
            html+='</tr>';
        });
        html += '</tbody>';
        html += '</table>';
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
        incorp.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        incorp.list(true);
    });
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        let tr = tblIncorp.cell($(this).parents('td, li')).index();
        let data = tblIncorp.row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id); 
        url = "/erp/ingreso/delete/"+data.id+"/";
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el Ingreso?  ' + '<b style="color: #304ffe;">' + data.cod_ingreso + '</b>', parameters, function () {
            tblIncorp.ajax.reload();
        });
      });

    $('#data_list tbody').on('click', 'a[rel="VerDetIngre"]', function () {
            let tr =  $("#data_list").DataTable().cell($(this).closest('td, li')).index();
            let data =  $("#data_list").DataTable().row(tr.row).data();
            $('#tipo_incorp').text(data.tipo_ingreso);
            $('#fecha').text(data.fecha_ingreso);
            $('#usuario').text(data.usuario);
            $('#t_comprob').text(data.tipo_comprob);
            $('#nro_comprob').text(data.num_comprob);
            $('#almacen').text(data.almacen);
            $('#jefe').text(data.respon_almac);
            $('#prov').text(data.proveedor);
            $('#status').text(data.estado);
            $('#obs').text(data.observ);

            $('#tblDetalleProd').DataTable({
                responsive: false,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_detalle_prod',
                        'id': data.id
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
                columns: [
                   
                    {"data": "product"},
                    {"data": "category"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "subtotal"}
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2) + ' Bs.';
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });
            $('#incorp_title').find('span').html('Detalle de la Incorporación:  ' + data.cod_ingreso);
            $('#myModalDetProd').modal('show');
        })
        .on('click', 'td.details-control', function () {
            let tr = $(this).closest('tr');
            let row =  tblIncorp.row(tr);
            let id=row.data().id;
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                let parameters = new FormData();
                 parameters.append('action', 'search_detalle_prod');
                 parameters.append('id', id);
                 $.ajax({
                     url: window.location.pathname,
                     type: 'POST',
                     data: parameters,
                     dataType: 'json',
                     processData: false,
                     contentType: false,
                 }).done(function (data) {
                     if (!data.hasOwnProperty('error')) {
                         row.child(incorp.formatRowHtml(data)).show();
                         tr.addClass('shown');
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
    incorp.list(false);
});
