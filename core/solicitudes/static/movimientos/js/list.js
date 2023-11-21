let input_daterange;
let data_list;

let solicitud_list = {
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
        data_list = $('#data_list').DataTable({
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
                {"data": "id"},
                {"data": "codigo"},
                {"data": "fecha"},
                {"data": "unidad_origen"},
                {"data": "usuario"},
                {"data": "prioridad"},
                {"data": "tipo"},
                {"data": "estado"},
                {"data": "id"},
            ],
            columnDefs: [               
                {
                    targets: [-9],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' + row.id + '" name="object" value="' + row.id + '"><span class="checkmark"></span></label>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center text-capitalize',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '';
                        if (row.estado === 'EN CREACIÓN' || row.estado === 'RETORNADO') {
                            buttons += '<a href="/solicitudes/solicitud/update/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                            buttons += '<a href="/solicitudes/solicitud/detail/' + row.id + '/" class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';                       
                            buttons += '<a rel="delete" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                            return buttons;   
                        }
                        return buttons += '<a href="/solicitudes/solicitud/detail/' + row.id + '/" target="_blank" class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';
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
        solicitud_list.list(false);
    });
    $('.btnSearchAll').on('click', function () {
        solicitud_list.list(true);
    });
    const showDropdownActions = (content, button) =>{
        const dropdownContent = document.getElementById(content)
        const dropdownButton = document.getElementById(button)
        
        dropdownButton.addEventListener('click', () =>{
            dropdownContent.classList.toggle('show-dropdown')           
        })
        document.addEventListener('click', function (event) {
            if (!dropdownContent.contains(event.target) && !dropdownButton.contains(event.target)) {
                dropdownContent.classList.remove('show-dropdown');
            }
        });
     }
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar la solicitud ' + '<b style="color: #304ffe;">' + data.codigo + '?</b>', parameters, function () {
            data_list.row(tr.row).remove().draw();
            sweet_info( 'Registro eliminado con exito');
        });
      });
    solicitud_list.list(false);
    showDropdown('dropdown-content','dropdown-button');
    showDropdownActions('dropdown-actions','dropdown-button-actions');
});