let detailSupport;
let tblSearchProducts;
let select_search_products;

let solicSupp = {
    detail: {
        codigo: "",
        tipo_solic: "",
        prioridad: "",
        fecha: "",
        unidad: "",
        estado: "",
        descrip: "",
        tipo_prod: "",
        productos: []
    },

    get_ids: function () 
    {
        let ids = [];       
        $.each(this.detail.productos, function (key, value) {
            ids.push(value.codbien.id);
        });
        return ids;
    },
    add: function (item) {
        this.detail.productos.push(item);
        this.list();
    },
    list: function () 
    {
        detailSupport = $('#tblSolicSupp').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.detail.productos,
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
                search: "Buscar:",
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
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "imagen"},
                {"data": "categ"},
                {"data": "diagnostico"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    orderable: false,
                    render: function(data, type, row){
                        return '<a rel="deleteProd" class="btn btn-xs btn-danger"><i class="fas fa-trash-alt"></i></a>'
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },      
                {
                    targets: [-1],
                    class: "text-left",
                    orderable: false,
                    render: function(data, type, row){
                        return '<input type="text" class="form-control form-control-sm input-flat" name="diagnostico" style="font-size: 11px; padding-left:4px; padding-right:4px; height: 24px;" autocomplete="off" placeholder="Ingrese un breve diagnóstico" value="' + row.diagnostico + '">'
                    }
                }
            ],
            initComplete: function (settings, json) {
    
            }
        });
    },    
};
function formatSearch(repo) {    
    if (repo.loading) {
        return repo.text;
    }
    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }    
    let option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>NOMBRE:</b> ' + repo.nombre +' / '+ repo.descripcion+ '<br>' +
        '<b>CATEGORÍA:</b>' + repo.categorias.nombre  +'<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');
    return option;
}
$(function(){
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('select[name="tipo_solic"]').on('change', function() {
        const tipo_solic = $(this).val();
        //alert(codigo);
        if (tipo_solic === 'REP') {
            $("#tipo_prod").collapse('show');            
            $("#detail").collapse('show');     
        }else{
            $("#tipo_prod").collapse('hide');
            $("#detail").collapse('hide');
        }        
    });
    $('.btnRemoveAll').on('click', function () {
        if (solicSupp.detail.productos.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            solicSupp.detail.productos = [];
            solicSupp.list();
        }, function () {

        });
    });
    $('#tblSolicSupp tbody').on('click', 'a[rel="deleteProd"]', function () {
        let tr = detailSupport.cell($(this).closest('td, li')).index();
        alert_action('Notificación', '¿Estas seguro de remover el producto de tu detalle?',
            function () {                
                solicSupp.detail.productos.splice(tr.row, 1);
                solicSupp.list();
            }, function () {

        });   
    }).on('change keyup', 'input[name="diagnostico"]', function () {
        let diagnostico = $(this).val();
        let tr = detailSupport.cell($(this).closest('td, li')).index();
        solicSupp.detail.productos[tr.row].diagnostico = diagnostico;            
    });
  
    $('input[name="search"]').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(solicSupp.get_ids()), //lo convierto a string para mandarlo a mi vista
                    'term': $('select[name="search"]').val(),
                    'idunidad': $('#idunidad').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "full_name"},
                {"data": "imagen"},                
                {"data": "codbien.codbien"},
                {"data": "codubica.nombre", className: "text-left"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
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
        $('#tlSolic_prod').find('span').html('Catalogo de Productos');
        $('#tlSolic_prod').find('i').removeClass().addClass('fas fa-search');
        $('#myModalSearchProducts').modal('show');
    });
    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            let product = tblSearchProducts.row(tr.row).data();
            product.id = product.prod;
            product.full_name = product.full_name;
            product.imagen = product.imagen;
            product.categ = product.categ;
            product.diagnostico = "";
    
            solicSupp.add(product)
            tblSearchProducts.row($(this).parents('tr')).remove().draw();

    });
    //Envio de datos del formulario
    $('#solicSupport').on('submit', function(e){
        e.preventDefault();
        let text = "";
        if  ($('input[name="action"]').val() == 'add'){
            text = "Creada";
        }else{
            text = "Modificada";
        }   
        if ($('select[name="tipo_solic"]').val() === 'REP') {
            if (solicSupp.detail.productos.length === 0) {
                message_error('Debe al menos tener un item en su detalle');
                return false;
            }
        }
        solicSupp.detail.codigo = $('input[name="codigo"]').val();
        solicSupp.detail.tipo_solic = $('select[name="tipo_solic"]').val();
        solicSupp.detail.prioridad = $('select[name="prioridad"]').val();
        solicSupp.detail.fecha = $('input[name="fecha"]').val();
        solicSupp.detail.unidad = $('select[name="unidad"]').val();
        solicSupp.detail.estado = $('select[name="estado"]').val();
        solicSupp.detail.descrip = $('textarea[name="descrip"]').val();
        solicSupp.detail.tipo_prod = $('select[name="tipo_prod"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('solicitud', JSON.stringify(solicSupp.detail));
        submit_with_ajax(window.location.pathname, 'Notificación', 'Estas seguro de realizar la siguiente acción?', parameters, function(response){
            sweet_info( 'La Solicitud Ha Sido '+text+' Con Exito');
                setTimeout(() => {
                    location.href = '/solicitudes/soporte/list/';
                }, 1200);                 
        });           
    });
    solicSupp.list();
});




