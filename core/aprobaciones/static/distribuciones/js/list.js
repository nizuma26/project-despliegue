let dttestado;
let input_daterange;

let salida_aprob = {
    list: function(all){
        let parameters = {
            'action': 'searchdata',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        dttestado = $('#data_list').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
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
            //paging: false,
            ordering: false,
            //info: false,
            //searching: false,    
            columns: [
                {"data": "codigo", className: "text-center"},
                {"data": "tipo_salida"},
                {"data": "origen"},
                {"data": "destino"}, 
                {"data": "usuario"},
                {"data": "fecha"},
                {"data": "estado"},
                {"data": "id"},
            ],
            columnDefs: [      
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<i class="fa fa-clock c-purple" style="font-size: 13px;"><tool-tip role="tooltip"> Por Aprobar</tool-tip></i><span style="display:none;">'+row.estado+'</span></i>';               
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    // width: "14%",
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/erp/salida/detail/' + row.id + '/" target="_blank" class="btn btn-success btn-xs" data-toggle="tooltip" title="Consultar Detalle"><i class="fas fa-search"></i></a> ';
                        buttons += '<a href="/erp/salida/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a rel="status_change" class="btn btn-primary btn-xs"><i class="fas fa-check-square"></i></a>';
                        return buttons;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });
    },
}
$(function () { 
    input_daterange = $('input[name="date_range"]');
    input_daterange.daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });
    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        salida_aprob.list(false);
    });
    $('.btnSearchAll').on('click', function () {
        salida_aprob.list(true);
    });       
    $('#data_list tbody').on('click', 'a[rel="status_change"]', function () {
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        $('#manage_state_title').find('i').removeClass().addClass('fas fa-pen');
        $('#manage_state_title').find('span').html(`Cambiar Estado: ${data.codigo}`);
        $('#modalManageState').modal('show')        
        $('input[name="id"]').val(data.id);
    });
    showDropdown('dropdown-content','dropdown-button');
    salida_aprob.list(false);
});