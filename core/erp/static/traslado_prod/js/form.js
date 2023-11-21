let tblTrasProducts;
let tblSearchProducts;

let request_url = '';
let text = '';
let action = '';
const actions = $('input[name="action"]').val();
const url_location = $('input[name="url"]').val();

let traslados = {
    items: {

        cod_traslado: '',
        origen: '',
        respon_origen:'',
        destino: '',
        respon_destino:'',
        tipo_traslado: '',
        fecha_traslado: '',
        observ: '',
        estado: '',
        soportedocum: '',
        salida: '',
        produc_tras: []
    },   
    get_ids: function ()
    {
        let ids = [];       
        $.each(this.items.produc_tras, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    get_idsCodbien: function ()
    {
        let idcodbien = [];       
        $.each(this.items.produc_tras, function (key, value) {
            idcodbien.push(value.codbien.id);
        });
        return idcodbien;
    },    
    calcular_guia_tras: function () {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.produc_tras, function (pos, dict) {
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
        this.items.produc_tras.push(item);
        this.list();
    },

    list: function ()
    {
        this.calcular_guia_tras();
        tblTrasProducts = $('#tblTrasProducts').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,            
            data: this.items.produc_tras,
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
                {"data": "full_name", className: "text-left"},
                {"data": "categ"},
                {"data": "codbien.id"},
                {"data": "codubica.id"},               
                {"data": "ubica_destino.id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="deletprodsal" class="btn btn-danger btn-xs w-100 h-100" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },                
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm input-flat" readonly=true name="codbien" id="' + row.codbien.id + '" style="font-size: 11px; height: 25px;" autocomplete="off" value="' + row.codbien.codbien + '">';                        
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm input-flat" readonly=true style="font-size: 11px; height: 25px;" placeholder="Ingrese la Ubicación" maxlength="50" name="codubica" id="' + row.codubica.id + '" value="' + row.codubica.nombre + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" required class="form-control form-control-sm input-flat" style="font-size: 11px; height: 25px;" placeholder="Ingrese la Ubicación" maxlength="50" name="ubica_destino" id="' + row.ubica_destino.id + '" value="' + row.ubica_destino.nombre + '">';
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

function formatcodbien(repo) {

      let option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-sm-2 text-lef">' +
        '<p style="margin-bottom: 0;">' +
        '<i class="far fa-hand-point-right">  </i>' + repo.codbien + '<br>' +
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
    
    const convert_request = () => {
        $.ajax({
            url: url_location,
            type: "POST",
            data: {
                'action': 'convert_request',
            },
            dataType: "json",
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                console.log(data)
                $('select[name="tipo_traslado"]').val(data.header.tipo_traslado).select2({
                    theme: "bootstrap4",
                    language: 'es',
                    disabled: true
                })
                $('select[name="destino"]').val(data.header.destino).select2({
                    theme: "bootstrap4",
                    language: 'es',
                    disabled: true
                })
                $('input[name="respon_destino"]').val(data.header.representante_destino);
                // $('input[name="respon_origen"]').val(data.header.representante_origen);

                // $('select[name="origen"]').val(1).prop("disabled", true);
                traslados.items.produc_tras = data.detail;
                traslados.list()
                //$('select[name="tipo_salida"]').select2()
                //$('select[name="tipo_comprob"]').val('FAC')
                console.log('FUNCIONO: ', 'asdsa')
            }
            //message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    }
    if (actions === 'add'){
        request_url = url_location;
        text = 'creado';
        action = 'add';
        //salidas
    } else if(actions === 'edit') {
        request_url = url_location;
        salidas.get_detail_data()
        action = 'edit';
        text = 'modificado'
    } else {
        request_url = '/erp/traslado/add/'
        action = 'add';
        convert_request()
    }   
      $('select[name="origen"]').on('change', function () {
        let id = $(this).val();
        if (id != '') {
            traslados.items.produc_tras = [];
            traslados.list();
        }
        if (id == ''){
            traslados.items.produc_tras = [];
            traslados.list();
        }
        //alert(id)
        let options = '<option value="">-----------</option>';
        if (id === '') {
            $('input[name="respon_origen"]').val('');
            return false;
        }
        $.ajax({
            url: request_url,
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
            //select_products.html(options);
        });
    });

     //Para extraer datos del responsable del Destino del traslado
     $('select[name="destino"]').on('change', function () {
        let id = $(this).val();
        //alert(id)
        let options = '<option value="">-----------</option>';
        if (id === '') {
            $('input[name="respon_destino"]').val('');
            return false;
        }
        $.ajax({
            url: request_url,
            type: 'POST',
            data: {
                'action': 'search_responorigen',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
               
                $('input[name="respon_destino"]').val(data[0].nombrejefe);
                
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_products.html(options);
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
               $('select[name="tipo_traslado"]').append(newOption).trigger('change');
               $('#myModalConcepMov').modal('hide');               
            });
            traslados.list();
    });

    $('.btnRemoveAll').on('click', function () {
        if (traslados.items.produc_tras.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            traslados.items.produc_tras = [];
            traslados.list();
        }, function () {

        });
    });
    $('select[name="destino"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: request_url,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_destino'
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

    });

    $('.btnAddDestino').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de Unidad');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $('#empresa').focus();
        $('#myModalUnidad').modal('show');
    });

    $('#myModalUnidad').on('hidden.bs.modal', function (e) {
        $('#frmUnidad').trigger('reset');
    })

    $('#frmUnidad').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_unidad');
        submit_with_ajax(request_url, 'Notificación',
            '¿Estas seguro de crear la siguiente Unidad?', parameters, function (response) {
                let newOption = new Option(response.full_name, response.id, false, true);               
               $('select[name="destino"]').append(newOption).trigger('change');
               $('#myModalUnidad').modal('hide');
            });
    });

    $('#frmDepartamento').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_departamento');
        submit_with_ajax(request_url, 'Notificación',
            '¿Estas seguro de crear el Departamento?', parameters, function (response) {               
               $('#myModalDepartamento').modal('hide');
            });
    });

    // event cant
    $('#tblTrasProducts tbody').on('click', 'a[rel="deletprodsal"]', function () {
            let tr = tblTrasProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {                   
                    traslados.items.produc_tras.splice(tr.row, 1);
                    traslados.list();
                }, function () {

        });
        }).on('keydown.autocomplete', 'input[name="ubica_destino"]', function () {            
           $(this).autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: request_url,
                        type: 'POST',
                        data: {
                            'action': 'search_depart',
                            'term': request.term
                        },
                        dataType: 'json',
                    }).done(function (data) {
                        response(data);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {
                    });
                },
                delay: 350,
                minLength: 1,                
                select: function (event, ui) {
                    let tr = tblTrasProducts.cell($(this).closest('td, li')).index();
                    traslados.items.produc_tras[tr.row].ubica_destino.id = ui.item.id;
                    traslados.items.produc_tras[tr.row].ubica_destino.nombre = ui.item.nombre;
                    traslados.list();
                }
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
            ordering: false,            
            ajax: {
                url: request_url,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'idsCodbien': JSON.stringify(traslados.get_idsCodbien()),
                    'term': $('select[name="search"]').val(),
                    'idorigen': $('#idorigen').val()
                },                
                dataSrc: ""
            },
            columns: [
                {"data": "full_name"},
                {"data": "imagen"},
                {"data": "codbien.id"},
                {"data": "codubica.id", className: "text-left"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },                
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>' + row.codbien.codbien + '</span>';                    
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span>' + row.codubica.nombre + '</span>';
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
            product.categ = product.categ;
            product.codbien = {'id': product.codbien.id, 'codbien': product.codbien.codbien};
            product.codubica = {'id': product.codubica.id, 'nombre': product.codubica.nombre};
            product.ubica_destino = {'id': 0, 'nombre': ''};
            traslados.items.salida= product.salida;
            traslados.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    $('#frmTrasladoprod').on('submit', function (e) {
        e.preventDefault();
        if (traslados.items.produc_tras.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }
        traslados.items.cod_traslado = $('input[name="cod_traslado"]').val();
        traslados.items.origen = $('select[name="origen"]').val();
        traslados.items.respon_origen = $('input[name="respon_origen"]').val();
        traslados.items.destino = $('select[name="destino"]').val();
        traslados.items.respon_destino = $('input[name="respon_destino"]').val();
        traslados.items.tipo_traslado = $('select[name="tipo_traslado"]').val();
        traslados.items.fecha_traslado = $('input[name="fecha_traslado"]').val();
        traslados.items.observ = $('textarea[name="observ"]').val();
        traslados.items.estado = $('select[name="estado"]').val();

        let filename
       if  ($('input[name="soportedocum"]').val() == ''){
           // produc_catalago.items.imagen= $imagenPrevisualizacion.src;
          //  filename = $idsoportetraslado.src.replace(/.*(\/|\\)/, '');
            traslados.items.soportedocum= "documsoporte/trasladoEquipo/" + filename;
        }else{
            filename = $('input[name="soportedocum"]').val().replace(/.*(\/|\\)/, '');
            traslados.items.soportedocum= "documsoporte/trasladoEquipo/" + filename;
        }
        const href = "/erp/traslado/list/";
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('traslados', JSON.stringify(traslados.items)); //los convierto a string para enviarlos a mi vista
        console.log(traslados);
        submit_with_ajax(request_url, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
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
            url: request_url,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    idsCodbien: JSON.stringify(traslados.get_idsCodbien()),
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
        data.precio = data.precio;
        data.subtotal =  0.00;
        data.codbien ={'id': data.codbien.id, 'codbien': data.codbien.codbien};
        data.codubica = {'id': data.codubica.id, 'nombre': data.codubica.nombre};
        data.ubica_destino =  {'id': 0, 'nombre': ''};
        traslados.add(data);
            $(this).val('').trigger('change.select2');
    });
    traslados.list();
});