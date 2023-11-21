let input_daterange_act;
let activity;
let activity_users = {
    list: function (all) {
        let parameters = {
            'action': 'search_data_activity',
            'start_date_act': input_daterange_act.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date_act': input_daterange_act.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date_act'] = '';
            parameters['end_date_act'] = '';
        }
        activity = $('#data_activity').DataTable({
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
            columns: [
                { "data": "id", className: "text-center", width: '3%'},
                { "data": "id", className: "text-center", width: '6%'},
                { "data": "user", width: '11%'},
                { "data": "date_joined", width: '16%' },
                { "data": "action", width: '9%' },
                { "data": "modules", className: "text-capitalize", width: '12%' },
                { "data": "object_id", className: "text-center", width: '9%' },
                { "data": "object_repr", width: '26%' },
                { "data": "id", width: '8%' }
            ],
            order: [[1, "desc"], [3, "desc"]],
            columnDefs: [
                {
                    targets: [-9],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' + row.id + '"value="' + row.id + '"><span class="checkmark"></span></label>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        if (row.action == 'Creado') {
                            return '<i class="fas fa-plus c-blue" style="font-size: 11px;"><tool-tip role="tooltip"> Creado</tool-tip></i>';
                        } else if (row.action == 'Modificado') {
                            return '<i class="fas fa-pen c-yellow" style="font-size: 11px;"><tool-tip role="tooltip"> Modificado</tool-tip> </i>';
                        }
                        return '<i class="fas fa-times c-red" style="font-size: 11px;"><tool-tip role="tooltip"> Eliminado</tool-tip></i>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.action == 'Modificado') {
                            button = '<a rel="delete" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a> ';
                            button += '<a rel="detail" class="btn custom-btn-primary btn-xs"><tool-tip role="tooltip"> Ver  modificaciones</tool-tip><i class="fas fa-eye f-11"></i></a> ';
                            return button
                        }
                        return '<a rel="delete" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a> ';

                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
    },
};

$(function () {
    const showDropdownHistorical = (content, button) =>{
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
    input_daterange_act = $('input[name="date_range_activity"]');
    input_daterange_act.daterangepicker({
        language: 'auto',
        startDate: new Date(),
        locale: {
            format: 'YYYY-MM-DD',
        }
    });
    $('.drp-buttons').hide();
    $('.btnActSearch').on('click', function () {
        activity_users.list(false);
    });
    $('.btnActSearchAll').on('click', function () {
        activity_users.list(true);
    });
    $('#data_activity tbody').on('click', 'a[rel="detail"]', function () {
        const tr = $("#data_activity").DataTable().cell($(this).closest('td, li')).index();
        const data = $("#data_activity").DataTable().row(tr.row).data();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'detail',
                'id': data.id
            },
            success: function (response) {
                let html = '<table class="table table-sm table-hover">';
                html += '<thead>';
                html += '<tr><th scope="col" style="width: 20%;">CAMPO</th>';
                html += '<th scope="col" style="width: 40%;">VALOR ANTERIOR</th>';
                html += '<th scope="col" style="width: 40%;">VALOR ACTUAL</th></tr>';
                html += '</thead>';
                html += '<tbody style="font-size: 14px;">';
                if (response != '') {
                    $.each(response, function (key, value) {
                        html += '<tr>'
                        html += '<td>' + value.field + ':</td>'
                        html += '<td>' + value.previous_value + '</td>'
                        html += '<td>' + value.current_value + '</td>'
                        html += '</tr>';
                    });
                } else {
                    html += '<tr>'
                    html += '<td class="text-center" colspan="9">' + 'Sin modificaciones' + '</td>'
                    html += '</tr>';
                }
                html += '</tbody>';
                html += '</table>';
                $('#table_fields').html(html);
            },
            error: function (error) {
            }
        });
        $("#audit_fields").modal('show');
        $('#audit_field').find('span').html('Campos Modificados: ');
        $('#audit_field').find('i').removeClass().addClass('fas fa-pen');
    });
    function detail(response) {
        let html = '<table class="table table-sm">';
        html += '<thead>';
        html += '<tr><th scope="col">CAMPO</th>';
        html += '<th scope="col">VALOR ANTERIOR</th>';
        html += '<th scope="col">VALOR ACTUAL</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(response, function (key, value) {
            html += '<tr>'
            html += '<td>' + value.field + '</td>'
            html += '<td>' + value.previous_value + '</td>'
            html += '<td>' + value.current_value + '</td>'
            html += '</tr>';
        });
        html += '</tbody>';
        html += '</table>';
        console.log(html);
        return html;
    }
    function deleteObject(tr) {
        activity.row(tr.row).remove().draw();
    }
    $('#data_activity tbody').on('click', 'a[rel="delete"]', function () {
        const tr = activity.cell($(this).parents('td, li')).index();
        const data = activity.row(tr.row).data();
        const parameters = new FormData();
        parameters.append('action', 'delete_log_audit');
        parameters.append('id_log', data.id);
        const url = window.location.pathname;
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el registro Nº ' + '<b style="color: #304ffe;">' + data.id + '</b>?', parameters, function () {
            sweet_info('Registro eliminado con exito');
            deleteObject(tr);
        });
    });
    showDropdown('dropdown-content-act', 'dropdown-button-act');
    showDropdownHistorical('dropdown_content_hostorical','dropdown_button_historical');
    activity_users.list(false);
});


