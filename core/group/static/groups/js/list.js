let dttGroup;
$(function () {
    dttGroup = $('#data_list').DataTable({
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
            {"data": "name"},                               
            {"data": "permissions.length"},                               
            {"data": "id"},                
        ],
        columnDefs: [  
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {                    
                    return '<span class="badge badge-primary badge-pill" style="font-size: 10px;">'+ data +'</span>';
                }
            },              
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/group/update/'+ row.id +'/" class="btn btn-warning btn-xs btnEdit"><tool-tip role="tooltip"> Editar</tool-tip><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="detail" class="btn btn-success btn-xs"><tool-tip role="tooltip"> Información del Rol</tool-tip><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/group/delete/'+ row.id +'/" class="btn btn-danger btn-xs"><tool-tip role="tooltip"> Eliminar</tool-tip><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],                  
        initComplete: function (settings, json) {

        }
        
    });  
    $('#data_list tbody').on('click', 'a[rel="detail"]', function() {
		let tr = $("#data_list").DataTable().cell($(this).closest('td, li')).index();
		let data = $("#data_list").DataTable().row(tr.row).data();
		$("#myModal").modal('show');
        $('#titleGroup').find('i').removeClass().addClass('fas fa-info-circle');
		$('#ids').text(data.id);
		$('#name').text(data.name);
         
        // function permsView(data) {
        //     console.log(data);
        //     let html =
        //       '<table class="table table-bordered table-sm" id="ppp">' +
        //       '<thead style="background-color: #0088cc;">' +
        //       '<tr><th scope="col">PERMISOS VIEW</th><th scope="col">PERMISOS ADD</th><th scope="col">PERMISOS CHANGE</th><th scope="col">PERMISOS DELETE</th></tr>' +
        //       '</thead>' +
        //       '<tbody style="font-size: 15px;">';
          
        //     let viewPerms = '';
        //     let addPerms = '';
        //     let changePerms = '';
        //     let deletePerms = '';
          
        //     if (data && data.permissions) { // Validating that data contains permissions
        //       $.each(data.permissions, function (key, value) {
        //         if (value.name.trim() !== '') { // Filtering out blank permission names
        //           let permName = '<td>' + value.name + '</td>';
        //           let codename = value.codename.split('_')[0];
        //           switch (codename) {
        //             case 'view':
        //               viewPerms += '<tr>' + permName + '<td></td><td></td><td></td></tr>';
        //               break;
        //             case 'add':
        //               addPerms += '<tr><td></td>' + permName + '<td></td><td></td></tr>';
        //               break;
        //             case 'change':
        //               changePerms += '<tr><td></td><td></td>' + permName + '<td></td></tr>';
        //               break;
        //             case 'delete':
        //               deletePerms += '<tr><td></td><td></td><td></td>' + permName + '</tr>';
        //               break;
        //             default:
        //               console.log('Unknown type of permission:', codename);
        //               break;
        //           }
        //         } else {
        //           console.log('Blank permission name found. Skipping...');
        //         }
        //       });
        //     } else {
        //       console.log('Invalid data object. No permissions found.');
        //     }
        //     html += viewPerms + addPerms + changePerms + deletePerms;
        //     html += '</tbody></table>';
        //     return html;
        //   }
        // html += '<>';
        
        function permsView(data) {          
            //console.log(data.permissions.name);
            const array_module = [];
            const array = data.permissions;
            array.forEach((data) => {                
                array_module.push({content: data.content});
            });
            const uniqueArray = [...new Set(array_module.map(item => JSON.stringify(item)))].map(item => JSON.parse(item));
            let html = '<div class="scroll-h">';
            html += '<table class="table max-cont table-hover table-sm" id="tblPerms">';
            html += '<thead>';
            html += '<tr>';
            html += '<th scope="col">MODULOS</th>';          
            html += '<th scope="col">VER</th>';          
            html += '<th scope="col">AGREGAR</th>'; 
            html += '<th scope="col">MODIFICAR</th>'; 
            html += '<th scope="col">ELIMINAR</th>'; 
            html += '</tr>';
            html += '</thead>';
            html += '<tbody style="font-size: 14px;">';        
            //let module = data.content_type;
            let module = uniqueArray
            let perms = data.permissions;
            let perms_view = data.permissions.filter(function(perm) { return perm.codename.includes("view"); });
            let perms_add = data.permissions.filter(function(perm) { return perm.codename.includes("add"); });
            let perms_change = data.permissions.filter(function(perm) { return perm.codename.includes("change"); });
            let perms_delete = data.permissions.filter(function(perm) { return perm.codename.includes("delete"); });
            let num_rows = Math.max(module.length, perms_view.length, perms_add.length, perms_change.length, perms_delete.length);
            console.log(perms_view);
            console.log(perms_add);
            console.log(perms_change);
            $('#perms_view').html(perms_view.length);
            $('#perms_add').html(perms_add.length);
            $('#perms_change').html(perms_change.length);
            $('#perms_delete').html(perms_delete.length);
            $('#total_perms').html(data.permissions.length);
            for (let i = 0; i < num_rows; i++) {
                html+='<tr>'
                if (i < module.length) {
                    html+='<td>'+module[i].content+'</td>';
                }
                if (i < perms_view.length) {
                    html+='<td>'+ perms_view[i].name +'</td>';
                } else {
                    html+='<td><span>'+'Sin Asignar'+'</span></td>';
                }
                if (i < perms_add.length) {
                    html+='<td>'+ perms_add[i].name +'</td>';
                } else {
                    html+='<td><span>'+'Sin Asignar'+'</span></td>';
                }
                if (i < perms_change.length) {
                    html+='<td>'+ perms_change[i].name +'</td>';
                } else {
                    html+='<td><span>'+'Sin Asignar'+'</span></td>';
                }
                if (i < perms_delete.length) {
                    html+='<td>'+ perms_delete[i].name +'</td>';
                } else {
                    html+='<td><span>'+'Sin Asignar'+'</span></td>';
                    //html+='<td><i class="fas fa-times"><span style="display:none;">'+'No'+'</span></i></td>';
                }
                html+='</tr>';
            }                         
            html += '</tbody>';
            html += '</table>';
            html += '</div>';

            return html;
        }
        // function permsView(data) {            
        //     console.log(data);
        //     let html = '<table class="table table-bordered table-sm" id="tblPerms">';
        //     html += '<thead style="background-color: #0088cc;">';
        //     html += '<tr>';          
        //     html += '<th scope="col">PERMISOS</th>';          
        //     html += '<th scope="col">PERMISOS</th>';          
        //     html += '</tr>';          
        //     html += '</thead>';
        //     html += '<tbody style="font-size: 15px;">';        
        //     $.each(data.permissions, function (key, value) {                              
        //         html+='<tr>'
        //         switch (value.codename.split('_')[0]) { // Splitting the codename to get the type of permission
        //             case 'view':
        //                 html +='<td>' + value.name + '</td></tr>';
        //                 break;
        //             case 'add':
        //                 html += '<td>' + value.name + '</td></tr>';
        //                 break;
        //             case 'change':
        //                 html += '<td>' + value.name + '</td></tr>';
        //                 break;
        //             case 'delete':
        //                 html += '<td>' + value.name + '</td></tr>';
        //                 break;
        //         }
        //     });
                                  
        //     html += '</tbody>';
        //     return html;
        // }
        $('#perms').html(permsView(data));

            
        // let perms_add = data.permissions_add;
        //   function mostrarPermisosAdd(perms_add) {
        //     const name_add = perms_add.map(p => p.name); 
        //     return name_add.join('<li style="list-style-type: none"> </li>'); 
        //   }

        $('#tblPerms').DataTable({
            responsive: false,
            autoWidth: false,
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
            initComplete: function (settings, json) {
            }
        });     
	});
 
});