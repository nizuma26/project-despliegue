let data_list;
$(function () {
    data_list = $('#data_list').DataTable({
        responsive: false,
        autoWidth: false,
        destroy: true,
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
            search: "<button class='btn btn-sm'><i class='fa fa-search'></i></button>",
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
            {"data": "image"},
            {"data": "full_name"},
            {"data": "username"},
            {"data": "is_active"},
            {"data": "date_joined", className: "text-center"},
            {"data": "groups"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-8],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="' + row.id + '" name="user" value="' + row.id + '"><span class="checkmark"></span></label>';
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" class="img-fluid mx-auto d-block elevation-1 img-border" style="width: 27px; height: 27px; border-radius:  0.45rem;">';
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if(row.is_active){return '<a><tool-tip role="tooltip"> Activo</tool-tip><i class="fa fa-check c-blue" style="font-size: 13px;"><span style="display:none;">'+'activo'+'</span></i></a>'
                    }else{return '<a><tool-tip role="tooltip"> Inactivo</tool-tip><i class="fa fa-times c-red" style="font-size: 13px;"><span style="display:none;">'+'inactivo'+'</span></i></a>'}         
                    }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    let html = '';
                    if (row.is_superuser){
                        return '<span class="badge badge-info badge-pill f-11">'+ 'SuperUsuario' +'</span>'
                    }
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-primary badge-pill f-11">' + value.name + '</span> ';
                    });
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {   
                    let buttons = '<a href="/user/update/' + row.id + '/" class="btn btn-warning btn-xs"><tool-tip role="tooltip"> Editar</tool-tip><i class="fas fa-edit"></i></a> ';
                    if (row.is_active) { buttons += '<a rel="inactivar" class="btn btn-orange btn-xs"><tool-tip role="tooltip"> inactivar Registro</tool-tip><i class="fas fa-unlink"></i></a> ';                        
                    }else { buttons += '<a rel="activar" class="btn btn-info btn-xs"><tool-tip role="tooltip"> activar Registro</tool-tip><i class="fas fa-check-circle"></i></a> ';};   
                    buttons += '<a rel="detail" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Información del Usuario</tool-tip><i class="fas fa-search"></i></a> ';
                    buttons += '<a rel="access" class="btn custom-btn-primary btn-xs"><tool-tip role="tooltip"> Accesos del Usuario</tool-tip><i class="fas fa-shield-alt"></i></a> ';
                    buttons += '<a rel="delete" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;                   
                    
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    $('#data_list tbody').on('click', 'a[rel="detail"]', function() {
		const tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
		const data = $("#data_list").DataTable().row(tr.row).data();
		$("#detalle_user").modal('show');
        $('#detail_user').find('span').html('Información del Usuario');
        $('#detail_user').find('i').removeClass().addClass('fas fa-info-circle');
		$('#image').html('<img src="'+ data.image +'" style="width: 90px; height: 90px;" class="img-circle shadow-sm" alt="User Image">');
		$('#username').text(data.username);
		$('#first_name').text(data.first_name);
		$('#last_name').text(data.last_name);	
		$('#dni').text(data.dni);	
		$('#email').text(data.email);
        if(data.is_active){
            $('#active').text('Activo');
        }else{
            $('#active').text('Inactivo');
        }
		$('#fecha').text(data.date_joined);	
		$('#sesion').text(data.last_login);	
        let groups = {
            get_groups: function () 
            {
                let group = [];        
                $.each(data.groups, function (key, value) {
                    group.push(value.name);
                });			
                return group;
            },            
        }
        $('#grupo').text(groups.get_groups());

        let permisos = '';
        for (let i = 0; i < data.user_permissions.length; i++) {
            permisos += '<span class="badge badge-secondary justify-content input-flat" style="font-size: 13px;">' + data.user_permissions[i].name + '</span> ';
        }
        if (data.is_superuser){
            $('#perm').text('Todos');
        }else{
            $('#perm').html(permisos);
        }        
        let perms = $('#tblPermsUser').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_detail',
                    'id': data.id
                },
                dataSrc: ""
            },
            language: {
                decimal: "",
                sLengthMenu: "Mostrar _MENU_ registros",
                emptyTable: "No hay información",
                infoEmpty: "Mostrando 0 a 0 de 0 Entradas",
                info: "Total de Permisos _TOTAL_",
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
            info: true,
            columns: [
                {"data": "id", className:"text-center"},
                {"data": "name"},
            ],            
            initComplete: function (settings, json) {
        
            }
        });

	});
    $('#data_list tbody').on('click', 'a[rel="access"]', function() {
		const tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
		const data = $("#data_list").DataTable().row(tr.row).data();
        $("#access_users").modal('show');
        $('#access_user').find('span').html('Accesos del Usuario');
        $('#access_user').find('i').removeClass().addClass('fas fa-shield-alt');
        $('#tblAccessUsers').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_access',
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
                search: "<button class='btn ml-5 btn-sm'><i class='fa fa-search'></i></button>",
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
               
                {"data": "date_joined"},
                {"data": "time_joined"},
                {"data": "ip_address"},
                {"data": "browser", className: "text-left"},
                {"data": "device"},
                {"data": "type"},
            ],
            order: [[0, "desc"], [1, "desc"]],
            columnDefs: [                
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type == 'success'){
                            return '<span class="badge badge-success-border badge-pill" style="font-size: 11px;">'+ 'Exitoso' +'</span> ';
                        }
                        return '<span class="badge badge-danger-border badge-pill" style="font-size: 11px;">'+ 'Fallido' +'</span> ';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });

        

	});
    
    $('#data_list tbody').on('click', 'a[rel="delete"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-edit');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
       
        const url = "/user/delete/"+data.id+"/";
        submit_with_ajax(url, 'Notificación', '¿Estas seguro de eliminar al usuario ' + '<b style="color: #304ffe;">' + data.username + '</b>?', parameters, function () {
            sweet_info( 'El Registro Ha Sido Eliminado Con Exito');
            data_list.row(tr.row).remove().draw();
        });
      });

      $('#data_list tbody').on('click', 'a[rel="activar"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-check-circle');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'activar');
        parameters.append('id', data.id);       
        const url = window.location.pathname;
        submit_with_ajax(url, 'activar Usuario', '¿Estas seguro de activar al usuario ' + '<b style="color: #304ffe;">' + data.username + '</b>?', parameters, function () {
            sweet_info( 'El Registro Ha Sido Activado Con Exito');
            data_list.ajax.reload();
        });
      });

      $('#data_list tbody').on('click', 'a[rel="inactivar"]', function () {
        $('.modal-title').find('i').removeClass().addClass('fas fa-check-circle');
        const tr = $("#data_list").DataTable().cell($(this).parents('td, li')).index();
        const data = $("#data_list").DataTable().row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'inactivar');
        parameters.append('id', data.id);       
        const url = window.location.pathname;
        submit_with_ajax(url, 'inactivar Usuario', '¿Estas seguro de inactivar al usuario ' + '<b style="color: #304ffe;">' + data.username + '</b>?', parameters, function () {
            sweet_info( 'El Registro Ha Sido Inactivado Con Exito');
            data_list.ajax.reload();
        });
      });
      showDropdown('dropdown-content','dropdown-button');
});