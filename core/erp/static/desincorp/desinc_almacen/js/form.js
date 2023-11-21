let tblDesincAlmacen;
let tblSearchProducts;
let desincorp =
{
    items:
    {
        cod_desinc: '',
        almacen: '',
        respon_almac: '',
        tipo_desinc: '',
        fecha_desinc: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        observ: '',
        estado: '',
        soportedocum: '',
        desinc_almacen: []
    },

    get_ids: function () 
    {
        let ids = [];
        $.each(this.items.desinc_almacen, function (key, value) {
            ids.push(value.productos.id);
        });
        return ids;
    },
    calcular_guia_desinc: function () {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.desinc_almacen, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = parseFloat(dict.precio);
            subtotal += dict.subtotal;
        });

        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.desinc_almacen.push(item);
        this.list();
    },
    list: function () 
    {
        this.calcular_guia_desinc();
        tblDesincAlmacen = $('#tblDesincAlmacen').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,            
            data: this.items.desinc_almacen,
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
                  next: "Siguiente",
                  previous: "Anterior",
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
                {"data": "productos.codigo"},
                {"data": "productos.nombre", className: "text-left"},
                {"data": "stock_actual"},
                {"data": "precio"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="deleteprod" class="btn btn-danger btn-xs btn-rounded" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        
                        return '<input type="text" class="form-control form-control-sm" style="font-size: 12px; height: 24px;" name="cant" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },

                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary" style="font-size: 9px;">' + (data) + '</span>';
                    }
                },               
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span>' + data + '</span>';
                    }
                },               
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {                
                $(row).find('input[name="cant"]').TouchSpin({
                    max: data.stock_actual,                               
                    min: 1,
                    buttonup_class: 'btn btnTouchspinUp btn-xs btn-flat',
                    buttondown_class: 'btn btnTouchspinDown btn-xs btn-flat'                               
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

//esta funcion me permite dar un mejor formato a los select2
function formatRepo(repo) {
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
        '<img src="' + repo.productos.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.productos.nombre + '<br>' +
        '<b>Stock:</b> ' + repo.stock_actual + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">' + repo.precio + ' Bs.</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');


    return option;
}

$(function () {    
    showDropdown('dropdown-content','dropdown-button');
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    
    $('#fecha_desinc').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('select[name="almacen"]').on('change', function () {
        let id = $(this).val();
        if (id != '') {
            desincorp.items.desinc_almacen = [];
            desincorp.list();
        }
        if (id == ''){
            desincorp.items.desinc_almacen = [];
            desincorp.list();
        }
        let options = '<option value="">-----------</option>';
        if (id === '') {
            $('input[name="respon_almac"]').val('');
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_responalmac',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
               
                $('input[name="respon_almac"]').val(data[0].responsable);
                
                return true;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.btnAddConcep').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de un Concepto');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $('#codigo').focus();
        $('#myModalConcepMov').modal('show');
    });

    $('#myModalConcepMov').on('hidden.bs.modal', function (e) {
        $('#frmConcepMov').trigger('reset');
    })

    $('#frmConcepMov').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_concepto');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear el siguiente Concepto?', parameters, function (response) {
                let newOption = new Option(response.full_name, response.id, false, true);
               $('select[name="tipo_desinc"]').append(newOption).trigger('change');
               $('#myModalConcepMov').modal('hide');               
            });
    });

    $('.btnRemoveAll').on('click', function () {
        if (desincorp.items.desinc_almacen.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            desincorp.items.desinc_almacen = [];
            desincorp.list();
        }, function () {

        });
    });
    $('#tblDesincAlmacen tbody').on('click', 'a[rel="deleteprod"]', function () {
            let tr = tblDesincAlmacen.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    desincorp.items.desinc_almacen.splice(tr.row, 1);
                    desincorp.list();
                }, function () {

                });
        }).on('change', 'input[name="cant"]', function () {
            if ($(this).val() < 1)
            {
                message_error('La cantidad debe ser mayor a 0');
                return false; 
            } 
            if ($(this).val() == '') 
            {
                message_error('La cantidad no puede quedar vacia'); 
                return false; 
            }
            let cant = parseInt($(this).val());
            let tr = tblDesincAlmacen.cell($(this).closest('td, li')).index();
            desincorp.items.desinc_almacen[tr.row].cant = cant;
            desincorp.calcular_guia_desinc();
            $('td:eq(6)', tblDesincAlmacen.row(tr.row).node()).html(desincorp.items.desinc_almacen[tr.row].subtotal.toFixed(2));
        });
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });
  
    $('input[name="search"]').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.searchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(desincorp.get_ids()), //lo convierto a string para mandarlo a mi vista
                    'term': $('select[name="search"]').val(),
                    'idalmacen': $('#idalmacen').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "productos.nombre"},
                {"data": "productos.imagen"},
                {"data": "stock_actual"},
                {"data": "precio"},
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
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-info">'+data+'</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' Bs.';
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
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
            let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            let product = tblSearchProducts.row(tr.row).data();
            product.id = product.productos.id
            product.cant = 1;
            product.precio = product.precio;
            product.subtotal = product.subtotal;
            desincorp.add(product);
            console.log(product)
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });


    // event submit
    $('#frmDesincalmacen').on('submit', function (e) {
        e.preventDefault();
        if (desincorp.items.desinc_almacen.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }        
        desincorp.items.cod_desinc = $('input[name="cod_desinc"]').val();
        desincorp.items.almacen = $('select[name="almacen"]').val();
        desincorp.items.respon_almac = $('input[name="respon_almac"]').val();
        desincorp.items.tipo_desinc = $('select[name="tipo_desinc"]').val();
        desincorp.items.fecha_desinc = $('input[name="fecha_desinc"]').val();
        desincorp.items.subtotal = $('input[name="subtotal"]').val();
        desincorp.items.total = $('input[name="total"]').val();
        desincorp.items.iva = $('#idiva').val();
        desincorp.items.observ = $('textarea[name="observ"]').val();
        desincorp.items.estado = $('select[name="estado"]').val();       
        let filename
        if  ($('input[name="soportedocum"]').val() == ''){
            desincorp.items.soportedocum= "documsoporte/desincorpEquipo/" + filename;
        }else{
            filename = $('input[name="soportedocum"]').val().replace(/.*(\/|\\)/, '');
            desincorp.items.soportedocum= "documsoporte/desincorpEquipo/" + filename;
        }
        console.log(desincorp.items.desinc_almacen)
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('desincorp', JSON.stringify(desincorp.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {                
            location.href = '/erp/desincorp/list/';
        });
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
                    action: 'search_autocomplete',
                    ids: JSON.stringify(desincorp.get_ids()),
                    idalmacen: $('#idalmacen').val()
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
        if(!Number.isInteger(data.id)){
            return false;
        }
        data.cant = 1;
        data.precio = data.precio;
        data.subtotal = data.subtotal;


        desincorp.add(data);
        $(this).val('').trigger('change.select2');
    });
     desincorp.list();
});