let input_daterange;
let access = "";

let access_users = {
    list: function (all) {
        let parameters = {
            'action': 'search_data_access',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        access = $('#data_access').DataTable({
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
                {"data": "id", className: "text-center"},
                {"data": "id", className: "text-center"},
                {"data": "user"},
                {"data": "date_joined"},
                {"data": "time_joined"},
                {"data": "ip_address"},
                {"data": "browser"},
                {"data": "device"},
                {"data": "type", className: "text-center"},
                {"data": "id"},
            ],
            order: [[2, "desc"], [3, "desc"]],
            columnDefs: [     
                {
                    targets: [-10],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' + row.id + '"value="' + row.id + '"><span class="checkmark"></span></label>';
                    }
                },           
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.type == 'success'){
                            return '<span class="badge badge-success badge-pill" style="font-size: 11px;">'+ 'Exitoso' +'</span> ';
                        }
                        return '<span class="badge badge-danger badge-pill" style="font-size: 11px;">'+ 'Fallido' +'</span> ';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
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
    const showDropdownAccess = (content, button) =>{
        const dropdownContent = document.getElementById(content),
              dropdownButton = document.getElementById(button)
        
        dropdownButton.addEventListener('click', () =>{
            dropdownContent.classList.toggle('show-dropdown')            
        })
        document.addEventListener('click', function (event) {
            if (!dropdownContent.contains(event.target) && !dropdownButton.contains(event.target)) {
                dropdownContent.classList.remove('show-dropdown');
            }
        });
     }
    
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
        access_users.list(false);
        //$('#dropdown-content').classList.remove("show-dropdown")
    });
    $('.btnSearchAll').on('click', function () {
        access_users.list(true);
    });
    function deleteObject(tr) {
        access.row(tr.row).remove().draw();
    }
    $('#data_access tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $('#data_access').DataTable().cell($(this).parents('td, li')).index();
        const data = $('#data_access').DataTable().row(tr.row).data();
        const parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
       
        const url = "/security/access/users/delete/"+data.id+"/";
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar el registro Nº ' + '<b style="color: #304ffe;">' + data.id + '</b>?', parameters, function () {
            sweet_info('Registro eliminado con exito');
            deleteObject(tr);
        });
      });
      showDropdown('dropdown-content','dropdown-button');
      showDropdownAccess('dropdown_content_access','dropdown_button_access');
    access_users.list(false);
});
