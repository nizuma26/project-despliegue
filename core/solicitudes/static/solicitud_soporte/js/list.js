let input_daterange;
let solicSupport;

let solicList = {
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
        solicSupport = $('#data_list').DataTable({
            responsive: false,
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
                search: "<button type='button' class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
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
                {"data": "id", className: "text-center"},
                {"data": "codigo"},
                {"data": "unidad.nombre"},
                {"data": "usuario.full_name"},
                {"data": "prioridad.name"},
                {"data": "tipo_solic.name"},
                {"data": "estado.name"},
                {"data": "fecha"},
                {"data": "id"},
            ],
            columnDefs: [               
                
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/solicitudes/soporte/update/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="detail" class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';                       
                        buttons += '<a rel="delete" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                        return buttons;   
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
    
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
        solicList.list(false);
    });
    $('.btnSearchAll').on('click', function () {
        solicList.list(true);
    });
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);       
        url = window.location.pathname
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar la solicitud ' + '<b style="color: #304ffe;">' + data.id + '</b>?', parameters, function () {
            sweet_info( 'La solicitud Ha Sido Eliminada Con Exito');
            console.log(data.id)
            solicSupport.ajax.reload();
        });
      });

    solicList.list(false);
});