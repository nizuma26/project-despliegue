//Bienes Muebles
let tblSalProducts;
let tblSearchProducts;
//Materiales de Consumo
let tblSalSuminist;
let tblSearchSuminist;

let request_url = '';
let request = '/erp/salida/add/'
let text = '';
let action = '';
let codigo = '';
const actions = $('input[name="action"]').val();
const url_location = $('input[name="url"]').val();

let conta = 0;
let datos_cantprod = []
let tr = ""
let productos = ""
let cantprod = 0.00

function productReserved() {
    const Toast = Swal.mixin({
      toast: true,
      position: 'top',
      customClass: {
        popup: 'colored-toast'
      },
      showClass: {
        popup: 'fade_down_animation'
      },
      showConfirmButton: false,
      timer: 3600,
    })
    Toast.fire({
      icon: 'info',
      title: 'El producto ya esta reservado'
    })
  }

let salidas =
{
    items:
    {
        cod_salida: '',
        origen: '',
        respon_origen: '',
        destino: '',
        respon_destino: '',
        tipo_salida: '',
        tipo_comprob: '',
        num_comprob: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        fecha_salida: '',
        observ: '',
        estado: '',
        produc_sal: [],
        produc_sal2: []
    },
    get_ids: function () {
        let ids = [];
        $.each(this.items.produc_sal2, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    get_idsCodbien: function () {
        let idcodbien = [];
        $.each(this.items.produc_sal, function (key, value) {
            idcodbien.push(value.codbien.id);
        });
        return idcodbien;
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
                if (data.type === 'BM'){
                    salidas.items.produc_sal = data.items                    
                    $("#dist_bienes_muebles").collapse('show');
                    //$("#dist_bienes_muebles").removeClass('collapse');
                    salidas.list()
                }else{
                    salidas.items.produc_sal2 = data.items
                    $("#dist_suministros").collapse('show');
                    //$("#dist_suministros").removeClass('collapse');
                    salidas.list2()                   
                    
                }
            }
            //message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    },    
    calcular_guia_sal: function () {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.produc_sal, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = 1 * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    calcular_guia_sal2: function () {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.produc_sal2, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.precio);
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
        this.items.produc_sal.push(item);
        this.list();
    },
    add2: function (item) {
        this.items.produc_sal2.push(item);
        this.list2();
    },
    list: function () {
        this.calcular_guia_sal();        
        tblSalProducts = $('#tblSalProducts').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.produc_sal,
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
                { "data": "id" },
                { "data": "full_name" },
                { "data": "stock_actual" },
                { "data": "precio" },
                { "data": "subtotal" },
                { "data": "codbien.id" },
                { "data": "codubica.id" },
                { "data": "fila" }

            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="deletprodsal" class="btn btn-danger btn-xs btn-rounded" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-7],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>' + data + '</span>';;
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        // return parseFloat(data).toFixed(2);
                        return '<span class="badge badge-primary badge-pill" style="font-size: 10px;">' + data + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" required class="form-control input-flat" name="codbien" id="' + row.codbien.id + '" style="font-size: 11px; height: 22px;" autocomplete="off" placeholder="Buscar codigo..." value="' + row.codbien.codbien + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" required class="form-control input-flat" style="font-size: 11px; height: 22px;" placeholder="Buscar ubicación..." maxlength="50" name="codubica" id="' + row.codubica.id + '" value="' + row.codubica.nombre + '">';
                        // return '<select class="form-control select2" name="searchCodubica"></select>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center hidden-xs',
                    orderable: false,
                    visible: false,
                    render: function (data, type, row) {
                        return parseFloat(data);
                        // return '<select class="form-control select2" name="searchCodubica"></select>';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
            },
            initComplete: function (settings, json) {

            }
        });
        if (codigo === '51') {
            tblSalProducts.columns(6).visible(false)
        }      
    },
    list2: function () {
        this.calcular_guia_sal2();
        tblSalSuminist = $('#tblSalSuministros').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.produc_sal2,
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
                { "data": "id" },
                { "data": "codigo", className: "text-center" },
                { "data": "full_name", className: "text-left" },
                { "data": "stock_actual" },
                { "data": "precio", className: "text-center" },
                { "data": "cant" },
                { "data": "subtotal" },
                { "data": "nro_lote" },
                { "data": "fecha_venc" },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="deleteprod2" class="btn btn-danger btn-xs btn-rounded" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-primary badge-pill" style="font-size: 10px;">' + data + '</span>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-flat" name="cant2" style="font-size: 11px; height: 24px;" autocomplete="off" value="' + row.cant + '">';
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
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.lote) {
                            return '<input type="text" class="form-control form-control-sm input-flat" name="nro_lote" style="text-align: center; font-size: 11px; padding-left:4px; padding-right:4px; height: 24px;" autocomplete="off" placeholder="Ingrese lote" value="' + row.nro_lote + '">';
                        } else {
                            return '<input type="text" disabled=true class="form-control form-control-sm input-flat" name="nro_lote" style="text-align: center; font-size: 11px; padding-left:4px; padding-right:4px; height: 24px;" autocomplete="off" value="' + row.nro_lote + '">';
                        }
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.lote) {
                            return '<input type="date"  name="fecha_venc" id="fecha_venc" style="font-size: 11px; height: 24px;" class="form-control form-control-sm input-flat f_venc" format="YYYY-MM-DD" autocomplete="off" value="' + row.fecha_venc + '">';
                        } else {
                            return '<input type="date" disabled=true  name="fecha_venc" style="font-size: 11px; height: 24px;" class="form-control form-control-sm input-flat" format="YYYY-MM-DD" autocomplete="off" value="' + row.fecha_venc + '">';
                        }
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                let stock = 0;
                if (data.reserved > 0 ){
                    stock = data.stock_actual - data.reserved;
                }else{
                    stock = data.stock_actual;
                }
                $(row).find('input[name="cant2"]').TouchSpin({
                    min: 1,
                    max: stock,
                    buttonup_class: 'btn btn-secondary btn-xs btn-flat',
                    buttondown_class: 'btn btn-secondary btn-xs btn-flat'
                });
            },
            initComplete: function (settings, json) {
            }
        });
    },
};
//Para los Bienes Muebles
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }
    const option = document.createElement('div');
    option.innerHTML = `<div class="wrapper container">
        <div class="row">
            <div class="col-lg-1">
            <img src="${repo.imagen}" class="img-fluid img-thumbnail d-block mx-auto rounded">
            </div>
            <div class="col-lg-11 text-left shadow-sm">                
                <p><b>NOMBRE:</b> ${repo.full_name}</p>
                <p style="margin-top: -8px;"><b>STOCK:</b> ${repo.stock}</p>               
                <p style="margin-top: -8px;"><b>PRECIO:</b> <span class="badge badge-warning" style="font-size: 9px;">${repo.precio}</span></p>
            </div>
        </div>
    </div>`
    return option;
}
//Para los bienes de consumo
function formatRepo2(repo2) {
    if (repo2.loading) {
        return repo2.text;
    }
    if (!Number.isInteger(repo2.id)) {
        return repo2.text;
    }
    let option2 = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo2.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo2.full_name + '<br>' +
        '<b>Stock:</b> ' + repo2.stock_actual + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">' + repo2.precio + ' Bs.</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');
    return option2;
}

$(function () {
    const bienes_muebles = (value) => {
        $("#dist_bienes_muebles").collapse('show');
        $("#dist_suministros").collapse('hide');
        tblSalProducts.columns(6).visible(true)
        if (value){
            setTimeout(() => {
                salidas.items.produc_sal2 = [];
                salidas.list2();
            }, 900);
        }        
    }

    const materiales_consumo = (value) => {
        $("#dist_suministros").collapse('show');
        $("#dist_bienes_muebles").collapse('hide');
        if (value){
            setTimeout(() => {
                $.each(datos_cantprod, function (key, value) {
                    value.cantprod = value.cantprod - value.cantprod;
                });
                salidas.items.produc_sal = [];
                salidas.list();
            }, 900);
        }        
    }

    const ambos = () => {
        $("#dist_suministros").collapse('hide');
        //salidas.items.produc_sal = [];
        $("#dist_bienes_muebles").collapse('hide');
        //salidas.items.produc_sal2 = [];
        $('#myModalBienes').modal('show');
        $('#title_bienes').find('span').html('Bienes a Distribuir');
        $('.modal-title').find('i').removeClass().addClass('fas fa-shipping-fast');
    }

    const convert_request = () => {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'convert_request',
            },
            dataType: "json",
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                codigo = data.header.code
                $('select[name="tipo_salida"]').val(data.header.tipo_salida).select2({
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
                $('input[name="respon_origen"]').val(data.header.representante_origen);

                $('select[name="origen"]').val(1).prop("disabled", true);
                if (data.header.tipo_bienes === 'MTC'){
                    const search_mtc = document.querySelector('.content_search_mtc')
                    search_mtc.remove();
                    materiales_consumo(false);
                    salidas.items.produc_sal2 = data.detail
                    salidas.list2()
                    let cells = tblSalSuminist.column(5).nodes();

                    // Recorre todas las celdas y deshabilita los inputs
                    cells.each(function() {
                        let input = $(this).find('input');
                        input.prop('disabled', true);
                    });
                }else{
                    const search_bsm = document.querySelector('.content_search_bsm')
                    search_bsm.remove();
                    bienes_muebles(false);
                    let detail = data.detail;
                    salidas.items.produc_sal = detail
                    salidas.list()
                }
                //$('select[name="tipo_salida"]').select2()
                //$('select[name="tipo_comprob"]').val('FAC')
            }
            //message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    }

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
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
        request_url = '/erp/salida/add/'
        action = 'add';
        text = 'creado'
        convert_request()
    }    
    $('#fecha_salida').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('.btnAddUbicaF').on('click', function () {
        $('input[name="action"]').val('add');
        $('#titledepart').find('span').html('Creación de un Departamento');
        $('#titledepart').find('i').removeClass().addClass('fas fa-plus');
        $("#iddepartamento").focus();
        $('#myModalDepart').modal('show');
    });
    $('#myModalDepart').on('hidden.bs.modal', function (e) {
        $('#frmDepart').trigger('reset');
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
        let myForm = document.getElementById('frmConcepMov');
        let parameters = new FormData(myForm);
        parameters.append('action', 'create_concepto');
        submit_with_ajax(request, 'Notificación',
            '¿Estas seguro de crear el siguiente Concepto?', parameters, function (response) {
                console.log(response);
                let newOption = new Option(response.denominacion, response.id, false, true);
                //  $('#proveedor').append(newOption).trigger('change');
                // $('#proveedor').selectmenu("refresh", true);
                $('select[name="tipo_salida"]').append(newOption).trigger('change');
                //$('select[name="categorias"]').append(newOption).trigger('change');
                $('#myModalConcepMov').modal('hide');
            });
        salidas.list();
    });
    $('select[name="tipo_salida"]').on('change', function() {
        $.ajax({
            url: request,
            type: 'POST',
            data: {
                'action': 'type_bienes',
                'id': $(this).val()
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                console.log(data)
                if (data.salida_bienes === 'BMS') {
                    bienes_muebles(true)
                }
                else if (data.salida_bienes === 'MTC') {
                    materiales_consumo(true)
                }
                else if (data.salida_bienes === 'AMB') {
                    ambos()
                }
                codigo = data.codigo;
            }
            //message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_products.html(options);
        });
    });
    // $('select[name="tipo_salida"]').select2({
    //     theme: "bootstrap4",
    //     language: 'es',
    //     allowClear: true,
    //     ajax: {
    //         delay: 250,
    //         type: 'POST',
    //         url: request_url,
    //         data: function (params) {
    //             let queryParameters = {
    //                 term: params.term,
    //                 action: 'search_concepto'
    //             }
    //             return queryParameters;
    //         },
    //         processResults: function (data) {
    //             return {
    //                 results: data,
    //             };
    //         },
    //     },
    //     placeholder: 'Ingrese una descripción',
    //     minimumInputLength: 1,
    // }).on('select2:select', function (e) {
    //     let data = e.params.data;
    //     if (data.salida_bienes === 'BMS') {
    //         bienes_muebles()
    //     }
    //     else if (data.salida_bienes === 'MTC') {
    //         materiales_consumo()
    //     }
    //     else if (data.salida_bienes === 'AMB') {
    //         ambos()
    //     }
    // });
    $('.accept').on('click', function () {
        let select_val = $('select[name="bienes"]').val();
        if (select_val === 'BM') {
            $("#dist_bienes_muebles").collapse('show');
            bienes_muebles(true)
            if (codigo === '51'){
                tblSalProducts.columns(6).visible(false);
            }

        } else {
            materiales_consumo(true)
            $("#dist_suministros").collapse('show');
        }
        $('#myModalBienes').modal('hide');
    });
    $('#myModalBienes').on('hidden.bs.modal', function (e) {
        $('#frmBienes').trigger('reset');        
    })
    $('.btnRemoveAll').on('click', function () {
        if (salidas.items.produc_sal.length === 0) return false;
        let fila = $(this).parent();
        let productos = tblSalProducts.row(tr.row).data();
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            $.each(datos_cantprod, function (key, value) {
                value.cantprod = value.cantprod - value.cantprod;
            });
            salidas.items.produc_sal = [];
            salidas.list();
        }, function () {
        });
    });
    $('.btnRemoveAll2').on('click', function () {
        if (salidas.items.produc_sal2.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            salidas.items.produc_sal2 = [];
            salidas.list2();
        }, function () {
        });
    });

    $('select[name="origen"]').on('change', function () {
        let id = $(this).val();
        salidas.items.produc_sal = [];
        salidas.items.produc_sal = [];
        salidas.list();
        salidas.list2();
        if (id === ''){
            $('input[name="respon_origen"]').val('');
            return false;
        }
        if (codigo === '51') {
            tblSalProducts.columns(6).visible(false)
        }
        else{
            tblSalProducts.columns(6).visible(true)
        }
        // if (id === '') {
        //     $('input[name="respon_origen"]').val('');
        //     return false;
        // }
        $.ajax({
            url: request,
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
    $('select[name="destino"]').on('change', function () {
        let id = $(this).val();
        let options = '<option value="">-----------</option>';
        if (id === '') {
            $('input[name="respon_destino"]').val('');
            return false;
        }
        $.ajax({
            url: request,
            type: 'POST',
            data: {
                'action': 'search_responorigen',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                $('input[name="respon_destino"]').val(data[0].nombrejefe);
                return true;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_products.html(options);
        });
    });
    $('.btnAddDestino').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de una Unidad');
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
        submit_with_ajax(request, 'Notificación',
            '¿Estas seguro de crear la siguiente Unidad?', parameters, function (response) {
                let newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="destino"]').append(newOption).trigger('change');
                $('#myModalUnidad').modal('hide');
            });
    });

    $('#frmDepart').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_departamento');
        submit_with_ajax(request, 'Notificación',
            '¿Estas seguro de crear el Departamento?', parameters, function (response) {
                $('#myModalDepart').modal('hide');
            });
    });

    $('#tblSalProducts tbody').on('click', 'a[rel="deletprodsal"]', function () {
        let tr = tblSalProducts.cell($(this).closest('td, li')).index();
        let fila = $(this).parent();
        let productos = tblSalProducts.row(tr.row).data();
        alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
            function () {
                $.each(datos_cantprod, function (key, value) {
                    if (value.id == productos.id) {
                        value.cantprod = value.cantprod - 1;
                    }
                });
                salidas.items.produc_sal.splice(tr.row, 1);
                salidas.list();
            }, function () {
    });
    }).on('change', 'input[name="cant"]', function () {
        let cant = parseInt($(this).val());
        let tr = tblSalProducts.cell($(this).closest('td, li')).index();
        salidas.items.produc_sal[tr.row].cant = cant;
        salidas.calcular_guia_sal();
        $('td:eq(4)', tblSalProducts.row(tr.row).node()).html(salidas.items.produc_sal[tr.row].subtotal.toFixed(2));

    }).on('keydown.autocomplete', 'input[name="codubica"]', function () {
        $(this).autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: request_url,
                    type: 'POST',
                    data: {
                        'action': 'busca_ubicacionfisica',
                        'term': request.term
                    },
                    dataType: 'json',
                }).done(function (data) {
                    response(data);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                }).always(function (data) {
                });
            },
            delay: 200,
            minLength: 2,
            select: function (event, ui) {
                let tr = tblSalProducts.cell($(this).closest('td, li')).index();
                salidas.items.produc_sal[tr.row].codubica.id = ui.item.id;
                salidas.items.produc_sal[tr.row].codubica.nombre = ui.item.nombre;
                salidas.list();
            }
        });
    });

    $('#tblSalProducts tbody').on('keydown.autocomplete', 'input[name="codbien"]', function () {
        console.log(salidas.get_idsCodbien())
        if ($(this).attr('id') != 0) {
            let tr = tblSalProducts.cell($(this).closest('td, li')).index();
            salidas.items.produc_sal[tr.row].codbien.id = 0;
            salidas.items.produc_sal[tr.row].codbien.codbien = '';
            salidas.list();
        } else {
            $(this).autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: request_url,
                        type: 'POST',
                        data: {
                            'action': 'busca_codbien',
                            'term': request.term,
                            'idsCodbien': JSON.stringify(salidas.get_idsCodbien())
                        },
                        dataType: 'json',
                    }).done(function (data) {
                        response(data);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                    }).always(function (data) {
                    });
                },
                delay: 200,
                minLength: 1,
                select: function (event, ui) {
                    let tr = tblSalProducts.cell($(this).closest('td, li')).index();
                    salidas.items.produc_sal[tr.row].codbien.id = ui.item.id;
                    salidas.items.produc_sal[tr.row].codbien.codbien = ui.item.codbien;
                    salidas.list();
                }
            });
        }
    });
    //Bienes de Consumo
    $('#tblSalSuministros tbody').on('click', 'a[rel="deleteprod2"]', function () {
        let tr = tblSalSuminist.cell($(this).closest('td, li')).index();
        alert_action('Notificación', '¿Estas seguro de remover el producto de tu detalle?',
            function () {
                salidas.items.produc_sal2.splice(tr.row, 1);
                salidas.list2();
            }, function () {

            });
    }).on('change', 'input[name="cant2"]', function () {
        let cant = parseInt($(this).val());
        let tr = tblSalSuminist.cell($(this).closest('td, li')).index();
        if ($(this).val() < 1) {
            message_error('La cantidad debe ser mayor a 0');
            return false;
        }
        if ($(this).val() == "") {
            message_error('La cantidad del producto no puede quedar vacia');
            return false;
        }

        salidas.items.produc_sal2[tr.row].cant = cant;
        salidas.calcular_guia_sal2();
        $('td:eq(6)', tblSalSuminist.row(tr.row).node()).html(salidas.items.produc_sal2[tr.row].subtotal.toFixed(2));

    }).on('change keyup', 'input[name="fecha_venc"]', function () {
        let fecha_venc = $(this).val();
        let tr = tblSalSuminist.cell($(this).closest('td, li')).index();
        salidas.items.produc_sal2[tr.row].fecha_venc = fecha_venc;

    }).on('change keyup', 'input[name="nro_lote"]', function () {
        let nro_lote = $(this).val();
        console.log(nro_lote);
        let tr = tblSalSuminist.cell($(this).closest('td, li')).index();
        salidas.items.produc_sal2[tr.row].nro_lote = nro_lote;
    })

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('input[name="search"]').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducSal').on('click', function () {
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
            order: false,
            ordering: false,
            ajax: {
                url: request,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'datos_cantprod': JSON.stringify(datos_cantprod),
                    'term': $('select[name="search"]').val(),
                    'idorigen': $('#idorigen').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "categoria" },
                { "data": "imagen" },
                { "data": "precio" },
                { "data": "stock" },
                { "data": "reserved"},
                { "data": "id" },
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto img-thumbnail" style="width: 30px; height: 30px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-success badge-pill" style="font-size: 11px;">' + parseInt(data) + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary badge-pill" style="font-size: 11px;">' + parseInt(data) + '</span>';
                    }
                },
                {
                    targets: [-4],
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

    $('.btnSearchSuminist').on('click', function () {
        tblSearchSuminist = $('#tblSearchSuminist').DataTable({
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
            order: false,
            ordering: false,
            ajax: {
                url: request,
                type: 'POST',
                data: {
                    'action': 'search_suministros',
                    'term': $('select[name="search"]').val(),
                    'ids': JSON.stringify(salidas.get_ids()),
                    'idorigen2': $('#idorigen').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "imagen" },
                { "data": "precio" },
                { "data": "stock_actual" },
                { "data": "reserved"},
                { "data": "id" },
            ],
            columnDefs: [
                {
                    targets: [-5],
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
                        return '<span class="badge badge-success">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-4],
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
                        let buttons = '<a rel="add2" class="btn btn-info btn-xs btn-rounded"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });

        $('#myModalSearchSuminist').modal('show');
    });
    
    //PARA RESTAR MIS STOCK EN TIEMPO REAL
    const subtract = (productos) => {
        let item = {}
        let flag_subtract=false;

        datos_cantprod.map((value)=>{
            if (value.id == productos.id) {
                value.cantprod += 1;
                flag_subtract=true;
             }
        })
        if (flag_subtract==false){
            item['id'] = productos.id;
            item['cantprod'] = 1.00;
            datos_cantprod.push(item)
        }
    }    

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        const tr = tblSearchProducts.cell($(this).closest('td, li')).index();
        let fila = $(this).parent();
        let stockcelda = fila.siblings("td:eq(4)").text();
        let reserved = fila.siblings("td:eq(5)").text();
        if (stockcelda === reserved){
            productReserved();
            return false;
        }
        console.log('STOCK: ', stockcelda, 'APARTADOS: ', reserved);
        productos = tblSearchProducts.row(tr.row).data();
        let product = {};
        let item = {}

        product['id'] = productos.id;
        product['full_name'] = productos.full_name;
        product['precio'] = productos.precio;
        product['subtotal'] = 0.00;
        product['codbien'] = { 'id': 0, 'codbien': '' };
        product['codubica'] = { 'id': 0, 'nombre': '' };
        product['stock_actual'] = stockcelda - 1;
        product['cant'] = 1;
        product['fila'] = conta;
        conta++;
        $('td:eq(4)', tblSearchProducts.row(tr.row).node()).find('span').html(product['stock_actual'])

        subtract(productos)
        salidas.add(product);

        if (product.stock_actual == 0) {
            tblSearchProducts.row(tr.row).remove().draw();
        }

    });

    $('#tblSearchSuminist tbody').on('click', 'a[rel="add2"]', function () {
        let tr = tblSearchSuminist.cell($(this).closest('td, li')).index();
        let product = tblSearchSuminist.row(tr.row).data();
        let fila = $(this).parent();
        let stockcelda = fila.siblings("td:eq(3)").text();
        let reserved = fila.siblings("td:eq(4)").text();
        
        if (stockcelda === reserved){
            productReserved();
            return false;
        }
        product.cant = 1;
        product.id = product.id;
        product.precio = product.precio;
        product.codigo = product.codigo;
        product.full_name = product.full_name;
        product.reserved = product.reserved;
        product.subtotal = 0.00;
        
        if (product.lote) {
            product.nro_lote = "";
            product.fecha_venc = "";
        } else {
            product.nro_lote = "Sin lote";
            product.fecha_venc = null;
        }
        console.log('STOCK: ', stockcelda, 'APARTADOS: ', reserved);
        salidas.add2(product);
        console.log('PRODUCT: ', salidas.items.produc_sal2);
        tblSearchSuminist.row($(this).parents('tr')).remove().draw();
    });
    //BUSQUEDA DE BIENES MUEBLES CON SELECT2
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: request,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(salidas.get_ids()),
                    datos_cantprod: JSON.stringify(datos_cantprod),
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
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.id = data.id;
        data.codigo = data.codigo;
        data.full_name = data.full_name;
        data.cant = 1.00;
        data.subtotal = 0.00;
        data.codbien = { 'id': 0, 'codbien': '' };
        data.codubica = { 'id': 0, 'nombre': '' };
        data.stock_actual = data.stock - 1
        data.fila = conta
        conta++;

        let es_igual = false;
        $.each(datos_cantprod, function (key, value) {
            if (value.id == data.id) {
                value.cantprod = value.cantprod + 1;
                es_igual = true;
            }
        });
        if (es_igual == false) {
            let item = {};
            item['id'] = data.id;
            item['cantprod'] = 1.00;
            item['fila'] = conta;
            datos_cantprod.push(item)
        }
        console.log(datos_cantprod);

        salidas.add(data);


        $(this).val('').trigger('change.select2');
    });
    //BUSQUEDA DE MATERIALES DE CONSUMO CON SELECT2
    $('select[name="search2"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: request,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete_suminist',
                    ids: JSON.stringify(salidas.get_ids()),
                    idorigen2: $('#idorigen').val()

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
        templateResult: formatRepo2,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        console.log(e.params);
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.id = data.id;
        data.codigo = data.codigo;
        data.full_name = data.full_name;
        data.cant = 1.00;
        data.subtotal = 0.00;

        if (data.lote) {
            data.nro_lote = "";
            data.fecha_venc = "";
        } else {
            data.nro_lote = "Sin lote";
            data.fecha_venc = null;
        }
        // data.codbienn = {'id': 0, 'codbien': ''};
        // data.codubican = {'id': 0, 'nombredepar': ''};
        salidas.add2(data);
        console.log(data);
        $(this).val('').trigger('change.select2');
    });

    // event submit
    $('#frmSalidaprod').on('submit', function (e) {
        e.preventDefault();
        if (salidas.items.produc_sal.length === 0 && salidas.items.produc_sal2.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;        
        }
        salidas.items.cod_salida = $('input[name="cod_salida"]').val();
        salidas.items.origen = $('select[name="origen"]').val();
        salidas.items.respon_origen = $('input[name="respon_origen"]').val();
        salidas.items.destino = $('select[name="destino"]').val();
        salidas.items.respon_destino = $('input[name="respon_origen"]').val();
        salidas.items.tipo_salida = $('select[name="tipo_salida"]').val();
        salidas.items.tipo_comprob = $('select[name="tipo_comprob"]').val();
        salidas.items.num_comprob = $('input[name="num_comprob"]').val();
        salidas.items.iva = $('#idiva').val();
        salidas.items.fecha_salida = $('input[name="fecha_salida"]').val();
        salidas.items.observ = $('textarea[name="observ"]').val();
        salidas.items.estado = $('select[name="estado"]').val();

        let parameters = new FormData();
        const list = '/erp/salida/list/'
        parameters.append('action', action);
        parameters.append('code', codigo);
        parameters.append('salidas', JSON.stringify(salidas.items)); //los convierto a string para enviarlos a mi vista

        submit_with_ajax(request_url, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            if (response.status === 'POR APROBAR'){
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
            sweet_save("El registro ha sido " + text + " con exito", 3000, list);
        });
    });
    salidas.list();
    salidas.list2();
});