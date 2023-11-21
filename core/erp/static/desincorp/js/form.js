let tblDesincProducts;
let tblSearchProducts;
let desincorp =
{
    items:
    {
        cod_desinc: '',
        origen: '',
        respon_origen:'',
        tipo_desinc: '',
        fecha_desinc: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        observ: '',
        estado: '',
        soportedocum: '',
        produc_desinc: []
    },

    get_idsCodbien: function ()
    {
        let idcodbien = [];
        $.each(this.items.produc_desinc, function (key, value) {
            idcodbien.push(value.codbien.id);
        });
        return idcodbien;
    },

    add: function (item) {
        this.items.produc_desinc.push(item);
        this.list();
    },

    list: function ()
    {
        tblDesincProducts = $('#tblDesincProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.produc_desinc,
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
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            columns: [
                {"data": "id"},
                {"data": "full_name", className: "text-left"},
                {"data": "categoria"},
                {"data": "codbien"},
                {"data": "codubica"},

            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="deletproddesinc" class="btn btn-danger btn-rounded btn-xs" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data.name;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data.name;
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
            },
            initComplete: function (settings, json) {

            }
        });
    },
};


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
                    '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                    '<div class="row">' +
                        '<div class="col-lg-6">' +
                            '<p style="margin-bottom: 0;">' +'<b>Nombre:</b> ' + repo.full_name + '</p>' +
                            '<b>PVP:</b> <span class="badge badge-warning">' + repo.precio + ' Bs.</span>' +
                        '</div>' +
                        '<div class="col-lg-6">' +
                            '<div class="row">' +
                                 '<div class="col-lg-6">' +
                                      '<b>Ubicación Origen: </b> ' + '<input type="text" class="form-control form-control-sm" readonly=true name="codubica" id="' + repo.codubica.id + '" style="font-size: 10px; height: 20px;" autocomplete="off" value="' + repo.codubica.nombre + '">' + 
                                 '</div>' +
                                  '<div class="col-lg-6">' +
                                     '<b>Código Bien: </b> ' + '<input type="text" class="form-control form-control-sm" readonly=true name="codbien" id="' + repo.codbien.id + '" style="font-size: 10px; height: 20px;" autocomplete="off" value="' + repo.codbien.codbien + '">' + 
                                 '</div>' +

                             '</div>' +                                                 
                        '</div>' +
                     '</div>' +
                '</div>' +
            '</div>' +
        '</div>');

    return option;
}
$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    showDropdown('dropdown-content','dropdown-button');
    $('select[name="origen"]').on('change', function () {
        let id = $(this).val();
        if (id != '') {
            desincorp.items.produc_desinc = [];
            desincorp.list();
        }
        if (id == ''){
            desincorp.items.produc_desinc = [];
            desincorp.list();
        }
        if (id === '') {
            $('input[name="respon_origen"]').val('');
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_responorigen',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
               
                $('input[name="respon_origen"]').val(data[0].nombrejefe);
                
                return true;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

      $('.btnAddUbicaF').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de un Departamento');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $("#idnombre").focus();
        $('#myModalDepartamento').modal('show');

    });

    $('#myModalDepartamento').on('hidden.bs.modal', function (e) {
        $('#frmDepartamento').trigger('reset');
    })

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
            desincorp.list();
    });

    $('.btnRemoveAll').on('click', function () {
        if (desincorp.items.produc_desinc.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            desincorp.items.produc_desinc = [];
            desincorp.list();
        }, function () {

        });
    });

    $('#tblDesincProducts tbody').on('click', 'a[rel="deletproddesinc"]', function () {
            let tr = tblDesincProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    desincorp.items.produc_desinc.splice(tr.row, 1);
                    desincorp.list();
                }, function () {

                });
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
                search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
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
            order: false,
            ordering: false,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'idsCodbien': JSON.stringify(desincorp.get_idsCodbien()),
                    'term': $('select[name="search"]').val(),
                    'idorigen': $('#idorigen').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "imagen"},
                {"data": "full_name"},
                {"data": "categoria"},
                {"data": "codbien.id"},
                {"data": "codubica.id", className: "text-left"},
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
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>' + row.codbien.codbien + '<span>' ;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>' + row.codubica.nombre + '<span>' ;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a rel="add" class="btn btn-primary btn-rounded btn-xs"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            let product = tblSearchProducts.row(tr.row).data();
            product.id = product.prod;
            product.full_name = product.full_name;
            product.categoria = product.categoria;
            product.codbien = {id: product.codbien.id, name: product.codbien.codbien}
            product.codubica = {id: product.codubica.id, name: product.codubica.nombre}
            
            desincorp.add(product);
            console.log(desincorp.items)
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });
    // event submit
    $('#frmDesincprod').on('submit', function (e) {
        e.preventDefault();
        let text = "";
        if (desincorp.items.produc_desinc.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }
        if  ($('input[name="action"]').val() == 'add'){
            text = "creado";
        }else{
            text = "modificado";
        }
        desincorp.items.cod_desinc = $('input[name="cod_desinc"]').val();
        desincorp.items.origen = $('select[name="origen"]').val();
        desincorp.items.respon_origen = $('input[name="respon_origen"]').val();
        desincorp.items.tipo_desinc = $('select[name="tipo_desinc"]').val();
        desincorp.items.fecha_desinc = $('input[name="fecha_desinc"]').val();
        desincorp.items.observ = $('textarea[name="observ"]').val();
        desincorp.items.estado = $('select[name="estado"]').val();
    //     let filename
    //    if  ($('input[name="soportedocum"]').val() == ''){
    //        // produc_catalago.items.imagen= $imagenPrevisualizacion.src;
    //       //  filename = $idsoportetraslado.src.replace(/.*(\/|\\)/, '');
    //         desincorp.items.soportedocum= "documsoporte/desincorporacionEquipo/" + filename;
    //     }else{
    //         filename = $('input[name="soportedocum"]').val().replace(/.*(\/|\\)/, '');
    //         desincorp.items.soportedocum= "documsoporte/desincorporacionEquipo/" + filename;
    //     }
        const href = "/erp/desinc/list/";
        console.log(desincorp.items.produc_desinc)
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('desincorp', JSON.stringify(desincorp.items)); //los convierto a string para enviarlos a mi vista
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {        
            sweet_save("El registro ha sido " + text + " con exito", 3000, href);        
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
                    idsCodbien: JSON.stringify(desincorp.get_idsCodbien()),
                    idorigen: $('#idorigen').val()

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
        data.id = data.prod;
        data.full_name = data.full_name;
        data.categoria = data.categoria;
        data.codbien ={'id': data.codbien.id, 'name': data.codbien.codbien};
        data.codubica = {'id': data.codubica.id, 'name': data.codubica.nombre};
        desincorp.add(data);
            $(this).val('').trigger('change.select2');
    });
     desincorp.list();

});