let detailSolicitud;
let bienesDeposito;
let bienesUso;
let flag;
let typeBienes = '';

const actions = $('input[name="action"]').val();

let solicitud = {
    data: {
        tipo_solicitud: "",
        concepto: "",
        prioridad: "",
        fecha: "",
        unidad_origen: "",
        unidad_destino: "",
        estado: "",
        descripcion: "",
        productos: []
    },
    get_ids_inv: function () 
    {
        let ids = [];       
        $.each(this.data.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    get_ids_products: function () 
    {
        let ids = [];       
        $.each(this.data.productos, function (key, value) {
            ids.push(value.prod_id);
        });
        return ids;
    },

    add: function (item) {
        this.data.productos.push(item);
        this.list();
    },
    columns: function () {
        let type = $('select[name="tipo_solicitud"]').val();
        if (flag === false){
            detailSolicitud.columns(4).visible(false);
            detailSolicitud.columns(3).visible(true);
        }else{           
            detailSolicitud.columns(4).visible(true);
            detailSolicitud.columns(3).visible(false);
        }
    },
    get_detail_data: () => {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'detail_data',
            },
            dataType: "json",
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                console.log(data)
                    solicitud.data.productos = data.items
                    solicitud.list()                   

            }
            //message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    },
    
    list: function () {
        detailSolicitud = $('#tblSolicitud').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.data.productos,            
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            columns: [
                {"data": "prod_id"},
                {"data": "full_name"},
                {"data": "categoria"},
                {"data": "cantidad"},
                {"data": "codigo_bien", visible: false, className: 'text-center'},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    orderable: false,
                    render: function(data, type, row){
                        return '<a rel="deleteProd" role="button" class="c-gray-light"><i class="fas fa-trash f-15 hover_red"></i></a>'
                    }
                },                     
                {
                    targets: [-2],
                    class: "text-center",
                    orderable: false,
                    render: function(data, type, row){
                        return '<input type="text" required class="form-control form-control-sm input-flat" name="cantidad" style="font-size: 11px; padding-left:4px; padding-right:4px; height: 25px;" autocomplete="off" placeholder="Ingrese una cantidad" value="' + row.cantidad + '">'
                    }
                }
            ],
            initComplete: function (settings, json) {

            }
        });
    },
};
const concept = (type, concept) => {
    let options = '';
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_concept',
            'type': type
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            $.each(data, function (key, value) {
                
                options += `<option value="${value.id}"> ${value.text} </option>`;
            });
            concept.html(options)
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        //select_products.html(options);
    });
}
const formatRepo = (repo) => {
    if (repo.loading) {
        return repo.text;
    }
    else if (!Number.isInteger(repo.id)) {
        return repo.text;
    }
    const option = document.createElement('div');
    option.innerHTML = `<div class="wrapper container">
        <div class="row">
            <div class="col-lg-1">
            <img src="${repo.imagen}" class="img-fluid img-thumbnail d-block mx-auto rounded">
            </div>
            <div class="col-lg-11 text-left shadow-sm f-11">
                <p><b>CÓDIGO:</b> <span class="badge badge-primary" style="font-size: 9px;">${repo.codigo}</span></p>
                <p style="margin-top: -9px;"><b>NOMBRE:</b> ${repo.full_name} <b class="ml-2">MARCA:</b> ${repo.marca}</p>
                <p style="margin-top: -9px;"><b>CATEGORÍA:</b> ${repo.categoria} <b class="ml-2">MODELO:</b> ${repo.modelo}</p>
            </div>
        </div>
    </div>`
    return option;
}
$(function(){
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#fecha_solicitud').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });
    if(actions === 'edit') {
        solicitud.get_detail_data()
    }
    showDropdown('dropdown-content','dropdown-button');    
    $('select[name="tipo_solicitud"]').on('change', function() {
        let value = $(this).val()
        let concepto = $('select[name="concepto"]');
        let type = ''
        console.log(value)
        if (value === '') {
            concepto.html('<option value="">------------</option>');
            return false;
        }
        else if (value === 'DIST'){
            type = 'SA';
            flag = false
            solicitud.data.productos = [];
            solicitud.list();
            $("#detail").collapse('show');
            solicitud.columns();
        }else if (value === 'DES_DEPOSITO'){
            type = 'DS';
            flag = false
            solicitud.data.productos = [];
            solicitud.list();
            $("#detail").collapse('show');
            solicitud.columns();
        }else if (value === 'DES_USO'){
            type = 'DS';
            flag = true;
            solicitud.data.productos = [];
            solicitud.list();
            $("#detail").collapse('show');
            solicitud.columns();
        }        
        else if (value === 'TRAS'){
            type = 'TR';
            flag = true;
            solicitud.data.productos = [];
            solicitud.list();
            $("#detail").collapse('show');
            solicitud.columns();
        }
        concept(type, concepto);
    });
    
    $('select[name="concepto"]').on('change', function() {
        if ($('select[name="tipo_solicitud"]').val() === 'DIST'){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'type_concept',
                    'id': $(this).val()
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    if (data.type === 'BMS') {
                        typeBienes = '02'
                    } else if (data.type === 'MTC'){
                        typeBienes = '04'
                    }
                    solicitud.data.productos = [];
                    solicitud.list()
                    console.log(data)
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                //select_products.html(options);
            });
        }
        
    });
    
    $('.btnRemoveAll').on('click', function () {
        if (solicitud.data.productos.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de remover todos los productos de tu detalle?', function () {
            solicitud.data.productos = [];
            solicitud.list();
        }, function () {

        });
    });
    $('#tblSolicitud tbody').on('click', 'a[rel="deleteProd"]', function () {
        const tr = detailSolicitud.cell($(this).closest('td, li')).index();
        alert_action('Notificación', '¿Estas seguro de remover el producto de tu detalle?',
            function () {                 
                solicitud.data.productos.splice(tr.row, 1);
                solicitud.list();
                solicitud.columns();
            }, function () {

        });   
    }).on('change', 'input[name="cantidad"]', function () {
        let cant = parseInt($(this).val());
        const tr = detailSolicitud.cell($(this).closest('td, li')).index();
        solicitud.data.productos[tr.row].cantidad = cant;
    });
    $('input[name="search"]').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.searchProducts').on('click', function () {
        if (flag === false){
            bienesDeposito = $('#tblBienesDeposito').DataTable({
                responsive: false,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_bienes_deposito',
                        'ids': JSON.stringify(solicitud.get_ids_products()),
                        'term': $('select[name="search"]').val(),
                        'type_bienes': typeBienes,
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
                    {"data": "imagen"},                
                    {"data": "full_name"},
                    {"data": "categoria"},
                    {"data": "id"},
                ],
                columnDefs: [
                    {
                        targets: [-4],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<img src="' + data + '" class="img-fluid d-block mx-auto img-thumbnail" style="width: 33px; height: 33px;">';
                        }
                    },              
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            let buttons = '<a rel="add" class="btn btn-primary btn-xs btn-rounded"><i class="fas fa-plus"></i></a> ';
                            return buttons;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });
            $('#title_bienes_deposito').find('span').html('Búsqueda de Productos');
            $('#title_bienes_deposito').find('i').removeClass().addClass('fas fa-search');
            $('#bienesDeposito').modal('show');
        }else{
            bienesUso = $('#tblBienesUso').DataTable({
                responsive: false,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_bienes_uso',
                        'ids': JSON.stringify(solicitud.get_ids_inv()),
                        'unidad_origen': $('#id_origen').val(),
                        'depart': $('#id_depart').val(),
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
                    {"data": "imagen"},                
                    {"data": "full_name"},
                    {"data": "categoria"},
                    {"data": "codigo_bien"},
                    {"data": "departamento"},
                    {"data": "id"},
                ],
                columnDefs: [
                    {
                        targets: [-6],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<img src="' + data + '" class="img-fluid d-block mx-auto img-thumbnail" style="width: 33px; height: 33px;">';
                        }
                    },              
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            let buttons = '<a rel="add" class="btn btn-primary btn-xs btn-rounded"><i class="fas fa-plus"></i></a> ';
                            return buttons;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });
            $('#title_bienes_uso').find('span').html('Búsqueda de Productos');
            $('#title_bienes_uso').find('i').removeClass().addClass('fas fa-search');
            $('#bienesUso').modal('show');
        }
        
    });
    $('#tblBienesDeposito tbody').on('click', 'a[rel="add"]', function () {
            const tr = bienesDeposito.cell($(this).closest('td, li')).index();
            const product = bienesDeposito.row(tr.row).data();
            product.cantidad = 1;
            product.codigo_bien = 'S/N';
            product.id = null;
            solicitud.add(product)
            bienesDeposito.row($(this).parents('tr')).remove().draw();
            solicitud.columns();
    });
    $('#tblBienesUso tbody').on('click', 'a[rel="add"]', function () {
        const tr = bienesUso.cell($(this).closest('td, li')).index();
        const product = bienesUso.row(tr.row).data();
        product.codigo_bien = product.codigo_bien;
        product.cantidad = 1;
        solicitud.add(product)
        bienesUso.row($(this).parents('tr')).remove().draw();
        solicitud.columns();
    });
    //busqueda del select2 de procuctos
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'autocomplete_bienes_deposito',
                    ids: JSON.stringify(solicitud.get_ids_products()),
                    type_bienes: typeBienes,
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        console.log(data);
        // if (!Number.isInteger(data.id)) {
        //     return false;
        // }
        data.cantidad = 1;
        data.codigo_bien = 'S/N';
        data.id = null
        solicitud.add(data);
        $(this).val('').trigger('change.select2');
    });
    //Envio de datos del formulario
    $('#form_solicitud').on('submit', function(e){
        e.preventDefault();
        let text = "";
        if  ($('input[name="action"]').val() == 'add'){
            text = "creado";
        }else{
            text = "modificado";
        }   
        if (solicitud.data.productos.length === 0) {
            message_error('Debe al menos tener un producto en su detalle');
            return false;
        }
        solicitud.data.tipo_solicitud = $('select[name="tipo_solicitud"]').val();
        solicitud.data.concepto = $('select[name="concepto"]').val();
        solicitud.data.prioridad = $('select[name="prioridad"]').val();
        solicitud.data.fecha = $('input[name="fecha"]').val();
        solicitud.data.unidad_origen = $('select[name="unidad_origen"]').val();
        solicitud.data.unidad_destino = $('select[name="unidad_destino"]').val();
        solicitud.data.estado = $('select[name="estado"]').val();
        solicitud.data.descripcion = $('textarea[name="descripcion"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('solicitud', JSON.stringify(solicitud.data));
        const href = '/solicitudes/solicitud/list/'        
        submit_with_ajax(window.location.pathname, 'Notificación', 'Estas seguro de realizar la siguiente acción?', parameters, function(response){
            //sweet_save("El registro ha sido " + text + " con exito", 3000, href);
            if (response.status === 'EN ESPERA'){
                notifySocket.send(
                    JSON.stringify({
                        type: response.type,
                        title: response.title,
                        message: response.message,
                        image: response.image,
                        url: response.url,
                        user_id: response.user_id,
                        permissions: response.permissions
                    })
                );
            }
            location.href = href;  
        });
    });
    if(actions === 'edit') {
        let type = $('select[name="tipo_solicitud"]').val();
        if (type === 'TRAS' || type === 'DES_USO'){
            flag = true;
        }else{
            flag = false;
        }
        $('#detail').collapse('show')
        solicitud.columns();
    }
    solicitud.list();
});

