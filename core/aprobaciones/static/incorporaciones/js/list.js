let tblIngreso;
let input_daterange;

let incorp_aprob = {
    list: function (all) {
        var parameters = {
            'action': 'searchdata',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblIngreso = $('#data_list').DataTable({
            responsive: false,
            scrollX: false,
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

            columns: [
                { "data": "cod_ingreso" },
                { "data": "almacen" },
                { "data": "usuario" },
                { "data": "tipo_ingreso" },
                { "data": "num_comprob" },
                { "data": "fecha_ingreso" },
                { "data": "total" },
                { "data": "estado" },
                { "data": "id" },
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' Bs.';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {                        
                        return '<i class="fa fa-clock c-purple" style="font-size: 13px;"><tool-tip role="tooltip"> Por Aprobrar</tool-tip><span class="d-none">'+row.estado.name+'</span></i>'; 
                    }

                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/erp/ingreso/detail/' + row.id + '/" target="_blank" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Consultar Detalle</tool-tip><i class="fas fa-search"></i></a> ';
                        buttons += '<a href="/erp/ingreso/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a rel="status_change" class="btn btn-primary btn-xs"><i class="fas fa-check-square"></i></a>';
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
        incorp_aprob.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        incorp_aprob.list(true);
    });
    $('#data_list tbody').on('click', 'a[rel="status_change"]', function () {
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        $('#manage_state_title').find('i').removeClass().addClass('fas fa-pen');
        $('#manage_state_title').find('span').html(`Cambiar Estado: ${data.cod_ingreso}`);
        $('#modalManageState').modal('show')        
        $('input[name="id"]').val(data.id);
    });
    showDropdown('dropdown-content','dropdown-button');
    incorp_aprob.list(false);
});