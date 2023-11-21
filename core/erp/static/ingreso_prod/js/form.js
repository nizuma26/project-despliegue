let tblProducts;
let tblSearchProducts;
let current_data = {};
let changes = [];

let ingresos =
{
    items:
    {
        cod_ingreso: '',
        almacen: '',
        respon_almac: '',
        tipo_ingreso: '',
        proveedor: '',
        tipo_comprob: '',
        num_comprob: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        fecha_ingreso: '',
        usuario: '',
        observ: '',
        estado: '',
        productos: [],
        seriales: [],
        lotes: []
    },
    get_ids: function () {
        let ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    data_header: function () {
        let previous_data_header = {
            data: {
                tipo_comprob: $("#id_comprob :selected").text(),
                num_comprob: $('input[name="num_comprob"]').val(),
                subtotal: $('input[name="subtotal"]').val(),
                iva: $('input[name="iva"]').val(),
                total: $('input[name="total"]').val(),
                fecha_ingreso: $('input[name="fecha_ingreso"]').val(),
                observ: $('textarea[name="observ"]').val(),
                tipo_ingreso: $("#idtipo_incorp :selected").text(),
                proveedor: $("#idproveedor :selected").text(),
                estado: $("#estatusIng :selected").text(),
            }
        }
        current_data = previous_data_header;
    },
    audit_data_header: function () {
        let compare_data = [
            { field: 'Tipo de incorporación', value_ant: current_data.data.tipo_ingreso, value_act: $("#idtipo_incorp :selected").text()},
            { field: 'Tipo de comprobante', value_ant: current_data.data.tipo_comprob, value_act: $("#id_comprob :selected").text()},
            { field: 'Nº de comprobante', value_ant: current_data.data.num_comprob, value_act: $('input[name="num_comprob"]').val()},
            { field: 'Fecha', value_ant: current_data.data.fecha_ingreso, value_act: $('input[name="fecha_ingreso"]').val()},
            { field: 'Proveedor', value_ant: current_data.data.proveedor, value_act: $("#idproveedor :selected").text()},
            { field: 'Observación', value_ant: current_data.data.observ, value_act: $('textarea[name="observ"]').val()},
            { field: 'Estado', value_ant: current_data.data.estado, value_act: $("#estatusIng :selected").text()},
            { field: 'Subtotal', value_ant: current_data.data.subtotal, value_act: $('input[name="subtotal"]').val()},
            { field: 'Iva', value_ant: current_data.data.iva, value_act: $('#idiva').val()},
            { field: 'Total', value_ant: current_data.data.total, value_act: $('input[name="total"]').val()},
        ]
        compare_data.forEach((data) => {
            if (data.value_ant != data.value_act) {
                changes.push(data);
            }
        });
    },
    calcula_guia_ingreso: function () {
        let subtotalIVA = 0.00;
        let subtotal = 0.00;
        let total = 0.00;
        let costoiva = 0.00;

        $.each(this.items.productos, function (pos, dict) {
            dict.pos = pos;
            costoiva = parseFloat(dict.precio) * parseFloat(dict.iva);
            dict.subtotal = (parseFloat(dict.precio) + costoiva) * dict.cant;
            subtotal += dict.subtotal;
            subtotalIVA = subtotalIVA + costoiva;
        });

        total = subtotal;
        subtotal = subtotal - subtotalIVA
        $('input[name="subtotal"]').val(subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(subtotalIVA.toFixed(2));
        $('input[name="total"]').val(total.toFixed(2));
    },

    add: function (item) {
        this.items.productos.push(item);
        this.list();
    },

    list: function () {
        this.calcula_guia_ingreso();
        tblProducts = $('#tblProducts').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.productos,
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
                { "data": "id" },
                { "data": "codigo" },
                { "data": "full_name", className: "text-left" },
                { "data": "precio" },
                { "data": "cant" },
                { "data": "iva" },
                { "data": "subtotal" },
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
                        if (row.impuesto) {
                            return '<input type="text" class="form-control form-control-sm input-flat" name="iva" style="text-align: center; font-size: 11px; padding-left:4px; padding-right:4px; height: 24px;" autocomplete="off" value="' + row.iva + '">';
                        } else {
                            return '<input type="text" disabled=true class="form-control form-control-sm input-flat" name="iva" style="text-align: center; font-size: 11px; padding-left:4px; padding-right:4px; height: 24px;" autocomplete="off" value="' + row.iva + '">';
                        }

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-flat" style="font-size: 11px; height: 24px;" name="cant" autocomplete="off" id="cantidad" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-flat" name="precio" style="font-size: 11px; height: 24px;" autocomplete="off" value="' + row.precio + '">';
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

//esta funcion me permite dar un mejor formato a los select2
function formatRepo(repo) {
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
            <div class="col-lg-11 text-left shadow-sm">                
                <p><b>CÓDIGO:</b> <span class="badge badge-primary" style="font-size: 9px;">${repo.codigo}</span></p>
                <p style="margin-top: -8px;"><b>NOMBRE:</b> ${repo.full_name}</p>
                <p style="margin-top: -8px;"><b>CATEGORÍA:</b> ${repo.categoria}</p>               
            </div>
        </div>
    </div>`
    return option;
}
$(function () {
    showDropdown('dropdown-content','dropdown-button');
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#fecha_ingreso').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });
    $('#f_venc').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('select[name="almacen"]').on('change', function () {
        let id = $(this).val();
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

    $('.btnAddProvee').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de un Proveedor');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $('#empresa').focus();
        $('#myModalProveedor').modal('show');
    });
    $("#myModalProveedor").on('shown.bs.modal', function () {
        const inputs = document.querySelectorAll('#myModalProveedor .txt_field input, #myModalProveedor .txt_field select, #myModalProveedor .txt_field textarea');
        inputs.forEach(input => {
            if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => {
                if (input.value.trim() !== '') {
                    input.classList.add('input-has-text');
                } else { input.classList.remove('input-has-text'); }
            });
        });
    });

    $('#myModalProveedor').on('hidden.bs.modal', function (e) {
        $('#frmProvee').trigger('reset');
        const inputs = document.querySelectorAll('#myModalProveedor .txt_field input, #myModalProveedor .txt_field select, #myModalProveedor .txt_field textarea');
        inputs.forEach(input => input.classList.remove('input-has-text')
        );
    });

    $('#frmProvee').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_proveedor');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente Proveedor?', parameters, function (response) {
                let newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="proveedor"]').append(newOption).trigger('change');
                $('#myModalProveedor').modal('hide');
            });
    });

    $('.btnAddConcep').on('click', function () {
        $('input[name="action"]').val('add');
        $('.modal-title').find('span').html('Creación de un Concepto');
        $('.modal-title').find('i').removeClass().addClass('fas fa-plus');
        $('#codigo').focus();
        $('#myModalConcepMov').modal('show');
    });
    $("#myModalConcepMov").on('shown.bs.modal', function () {
        const inputs = document.querySelectorAll('#myModalConcepMov .txt_field input, #myModalConcepMov .txt_field select');
        inputs.forEach(input => {
            if (input.value.trim() !== '') { input.classList.add('input-has-text'); }
            input.addEventListener('input', () => {
                if (input.value.trim() !== '') {
                    input.classList.add('input-has-text');
                } else { input.classList.remove('input-has-text'); }
            });
        });
    });
    $('#myModalConcepMov').on('hidden.bs.modal', function (e) {
        $('#frmConcepMov').trigger('reset');
        const inputs = document.querySelectorAll('#myModalConcepMov .txt_field input, #myModalConcepMov .txt_field select');
        inputs.forEach(input => input.classList.remove('input-has-text'));
    })

    $('#frmConcepMov').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_concepto');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear el siguiente Concepto?', parameters, function (response) {
                let newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="tipo_ingreso"]').append(newOption).trigger('change');
                $('#myModalConcepMov').modal('hide');
            });
    });

    $('.btnRemoveAll').on('click', function () {
        if (ingresos.items.productos.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            ingresos.items.productos = [];
            ingresos.list();
        }, function () {

        });
    });

    // function seriales(cant, code, name, category, id) {
    //     $('#code').html(code);
    //     $('#name').html(name);
    //     $('#category').html(category);
    //     $('#cant').html(cant);        
    //     let inputs = '';
    //     for (let i = 0; i < cant; i++) {
    //         inputs += '<tr>'
    //         inputs+='<td>'+'<input type="text"  class="form-control border-0 input-flat" style="font-size:12px; height: 28px;" name="serial-'+i+'" placeholder="Ingrese el serial">'+'</td>'            
    //         inputs+='</tr>';
    //     }       
    //     return inputs;
    // }
    // function btnSerial(idProd){
    //     $('.btnSerial').on('click', function (){                             
    //         $('#tbl_serials input').each(function(){   
    //             let seriales={};              
    //             let value = $(this).val();
    //             seriales['prod_id']=idProd;
    //             seriales['serial']=value;
    //             ingresos.items.seriales.push(seriales);
    //         });
    //         $('#myModalSerial').modal('hide');                
    //         console.log(ingresos.items.seriales);
    //     });  
    // }
    // function btnSerial(id){            
    // function btnSerial(idProd) {
    //     $('.btnSerial').on('click', function () {
    //       let serials = [];
    //       $('#tbl_serials input').each(function () {
    //         let value = $(this).val();
    //         serials.push(value);
    //       });
    //       let ingreso = {
    //         prod_id: idProd,
    //         seriales: serials
    //       };
    //       ingresos.items.seriales.push(ingreso);

    //       $('#myModalSerial').modal('hide');
    //       console.log(ingresos.items.seriales);
    //     });
    //   }
    // }


    // function serial(cant, code, name, category) {
    //     $('#code').html(code);
    //     $('#name').html(name);
    //     $('#category').html(category);
    //     $('#cant').html(cant);
    //     let html = '<table class="table table-sm table-bordered" style="width:100%;" id="tblSerial">';
    //     html += '<thead style="background-color: #699ac9; color: #fff;">';
    //     html += '<tr class="text-center" style="color: #fff">'
    //         if (cant==1){
    //             html += '<th class="thw" scope="col">INGRESE EL SERIAL</th>';
    //         }else{
    //             html += '<th class="thw" scope="col">INGRESE LOS SERIALES</th>';
    //         }
    //     html += '<tr>'        
    //     html += '</thead>';
    //     html += '<tbody>';
    //     for (let i = 1; i <= cant; i++) {
    //         html+='<tr>'
    //         html+='<td>'+'<input type="text" class="form-control border-0 input-flat" style="font-size:12px; height: 28px;" name="serial-'+i+'" placeholder="Ingrese el serial">'+'</td>'            
    //         html+='</tr>';
    //     }
    //     html += '</tbody>';  
    //     html += '</table>';  
    //     return html;

    // }   

    //FUNCIÓN QUE GENERA LOS INPUTS DE MANERA DINAMICA EN EL TABLE     

    function seriales(cant, code, name, category, idProd) {
        $('#code').html(code);
        $('#name').html(name);
        $('#category').html(category);
        $('#cant').html(cant);
        $('#btnAssign').html('<button type="button" class="btn btn-primary btn-block input-flat btn-sm btnSerial" data-id="' + idProd + '">Guardar</button>');
        let inputs = '';
        for (let i = 0; i < cant; i++) {
            inputs += '<tr>'
            inputs += '<td>' + '<input type="text" class="form-control border-0 input-flat" style="font-size:12px; height: 28px;" name="serial-' + i + '" placeholder="Ingrese el serial">' + '</td>'
            inputs += '</tr>';

        }
        $('.btnSerial').on('click', function () {
            let inputs_value = $('#tbl_serials input[type="text"]');
            for (let i = 0; i < inputs_value.length; i++) {
                let input = $(inputs_value[i]);
                let value = input.val();
                if (value === '') {
                    message_error('Todos los campos son obligatorios');
                    return false;
                }
            }
            let id = $(this).data('id');
            addSerial(id);
            $('#myModalSerial').modal('hide');
        });
        return inputs;
    }
    //FUNCIÓN QUE AGREGA LOS DATOS AL ARRAY
    function addSerial(idProd) {
        $('#tbl_serials input').each(function () {
            let value = $(this).val();
            ingresos.items.seriales.push({ prod_id: idProd, serial: value });
        });
        console.log(ingresos.items.seriales);
    }
    //FUNCIÓN QUE GENERA EL BOTÓN Y ENVIA LOS DATOS A LA FUNCIÓN addLotes
    function lotes(code, name, category, idProd) {
        $('#codeProd').html(code);
        $('#nameProd').html(name);
        $('#categoryProd').html(category);
        $('#btnLotes').html('<button type="button" class="btn btn-primary btn-bord btnLotes" data-id="' + idProd + '">Asignar Lote</button>');
        $('.btnLotes').on('click', function () {
            let listLotes = []
            let dataLote = {}
            let id_prod = $(this).data('id');
            let lote = $('#id_nro').val();
            let fecha_venc = $('#fecha_venc').val();
            dataLote['lote'] = lote;
            dataLote['fecha_venc'] = fecha_venc;
            listLotes.push(dataLote);
            console.log(fecha_venc);
            addLotes(id_prod, listLotes);
            $('#myModalLotes').modal('hide');
        });
    }
    $('#myModalLotes').on('hidden.bs.modal', function (e) {
        $('#frmLotes').trigger('reset');
    })
    function addLotes(idProd, lotes) {
        lotes.forEach(lote => {
            ingresos.items.lotes.push({ prod_id: idProd, nro_lote: lote.lote, fecha: lote.fecha_venc });
        });
        console.log(ingresos.items.lotes);
    }

    //   function addSerial(idProd) {
    //     let seriales = [];
    //     $('#tbl_serials input').each(function () {
    //       let value = $(this).val();
    //       seriales.push(value);
    //     });      
    //     let ingreso = {
    //       prod_id: idProd,
    //       seriales: seriales
    //     };
    //     let index = serial.detail.findIndex(item => item.prod_id === idProd);
    //     if (index === -1) {
    //         serial.detail.push(ingreso);
    //     } else {
    //         serial.detail[index] = ingreso;
    //     }      
    //     $('#myModalSerial').modal('hide');
    //     console.log(serial.detail);
    //   }

    $('#tblProducts tbody').on('click', 'a[rel="deleteprod"]', function () {
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
            function () {
                ingresos.items.productos.splice(tr.row, 1);
                ingresos.list();
            }, function () {
        });
    }).on('change', 'input[name="cant"]', function () {
        if ($(this).val() == '') {
            message_error('La Cantidad no puede quedar vacia');
            return false;
        }
        if ($(this).val() < 1) {
            message_error('La Cantidad debe ser mayor a 0');
            return false;
        }
        let cant = parseInt($(this).val());
        console.log(cant);
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        ingresos.items.productos[tr.row].cant = cant;
        let prod = ingresos.items.productos[tr.row];
        let code = prod.codigo;
        let id = prod.id;
        let name = prod.full_name;
        let category = prod.categoria;
        ingresos.calcula_guia_ingreso();
        $('td:eq(6)', tblProducts.row(tr.row).node()).html(ingresos.items.productos[tr.row].subtotal.toFixed(2));
        if (prod.serie) {
            $("#myModalSerial").modal('show');
            $('#serials').html(seriales(cant, code, name, category, id));
        }
        if (prod.lote) {
            $("#myModalLotes").modal('show');
            lotes(code, name, category, id)
        }

    }).on('change', 'input[name="precio"]', function () {

        if ($(this).val() == '') {
            message_error('El Precio no puede quedar vacio');
            return false;
        }
        if ($(this).val() < 0.01) {
            message_error('El Precio debe ser mayor a 0');
            return false;
        }
        let precio = parseFloat($(this).val());
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        ingresos.items.productos[tr.row].precio = precio;
        ingresos.calcula_guia_ingreso();
        $('td:eq(6)', tblProducts.row(tr.row).node()).html(ingresos.items.productos[tr.row].subtotal.toFixed(2));
    }).on('change', 'input[name="iva"]', function () {
        let iva = parseFloat($(this).val());
        console.log(iva);
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        ingresos.items.productos[tr.row].iva = iva;
        ingresos.calcula_guia_ingreso();
        $('td:eq(6)', tblProducts.row(tr.row).node()).html(ingresos.items.productos[tr.row].subtotal.toFixed(2));

    }).on('change keyup', 'input[name="fecha_venc"]', function () {
        let fecha_venc = $(this).val();
        console.log(fecha_venc);
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        ingresos.items.productos[tr.row].fecha_venc = fecha_venc;

    }).on('change keyup', 'input[name="nro_lote"]', function () {
        let nro_lote = $(this).val();
        console.log(nro_lote);
        let tr = tblProducts.cell($(this).closest('td, li')).index();
        ingresos.items.productos[tr.row].nro_lote = nro_lote;

    })

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('input[name="search"]').on('click', function () {
        $('input[name="search"]').val('').focus();
    });
    $('.searchProducts').on('click', function () {
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
                    'ids': JSON.stringify(ingresos.get_ids()),
                    'term': $('select[name="search"]').val(),
                    'idalmacen': $('#idalmacen').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "categoria" },
                { "data": "imagen" },
                { "data": "impuesto" },
                { "data": "serie" },
                { "data": "lote" },
                { "data": "id", className: 'text-center' },
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid img-thumbnail d-block mx-auto" style="width: 36px; height: 36px;">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.impuesto) {
                            return '<i class="fa fa-check c-blue" style="font-size: 14px;"></i>';
                        }
                        return '<i class="fa fa-times c-red" style="font-size: 14px;"></i>';

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.serie) {
                            return '<i class="fa fa-check c-blue" style="font-size: 14px;"></i>';
                        }
                        return '<i class="fa fa-times c-red" tyle="font-size: 14px;"></i>';

                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.lote) {
                            return '<i class="fa fa-check c-blue" style="font-size: 14px;"></i>';
                        }
                        return '<i class="fa fa-times c-red" tyle="font-size: 14px;"></i>';

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
        $('#modaltitleproduc').find('span').html('Catalogo de Productos');
        $('#modaltitleproduc').find('i').removeClass().addClass('fas fa-search');
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
        let product = tblSearchProducts.row(tr.row).data();
        product.cant = 1;
        product.precio = 0.01;
        product.subtotal = 0.00;
        if (product.impuesto) {
            product.iva = $('#idiva').val();
        }
        else {
            product.iva = 0.00;
        }
        ingresos.add(product);
        tblSearchProducts.row(tr.row).remove().draw();
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
                    ids: JSON.stringify(ingresos.get_ids()),
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
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.precio = 0.00;
        data.subtotal = 0.00;

        if (data.impuesto) {
            data.iva = $('#idiva').val();
        } else {
            data.iva = 0.00;
        }

        if (data.lote) {
            data.nro_lote = "";
            data.fecha_venc = "";
        } else {
            data.nro_lote = "Sin lote";
            data.fecha_venc = null;
        }
        ingresos.add(data);
        $(this).val('').trigger('change.select2');
    });

    // event submit
    $('#frmIngresoprod').on('submit', function (e) {
        e.preventDefault();
        let text = "";
        const href = "/erp/ingreso/list/";
        if (ingresos.items.productos.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }
        if ($('input[name="total"]').val() === '0.00') {
            message_error('Total Ingresos Vacio, debes colocar montos reales en precio y cantidad');
            return false;
        }
        if ($('input[name="precio"]').val() === '0.00') {
            message_error('Debe colocar un precio');
            return false;
        }
        if ($('input[name="action"]').val() == 'add') {
            text = "creado";
        } else {
            changes = [];
            ingresos.audit_data_header();
            text = "modificado";
        }
        ingresos.items.cod_ingreso = $('input[name="cod_ingreso"]').val();
        ingresos.items.almacen = $('select[name="almacen"]').val();
        ingresos.items.respon_almac = $('input[name="respon_almac"]').val();
        ingresos.items.tipo_ingreso = $('select[name="tipo_ingreso"]').val();
        ingresos.items.proveedor = $('select[name="proveedor"]').val();
        ingresos.items.tipo_comprob = $('select[name="tipo_comprob"]').val();
        ingresos.items.num_comprob = $('input[name="num_comprob"]').val();
        ingresos.items.fecha_ingreso = $('input[name="fecha_ingreso"]').val();
        ingresos.items.subtotal = $('input[name="subtotal"]').val();
        ingresos.items.iva = $('#idiva').val();
        ingresos.items.total = $('input[name="total"]').val();
        ingresos.items.observ = $('textarea[name="observ"]').val();
        ingresos.items.estado = $('select[name="estado"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('ingresos', JSON.stringify(ingresos.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            console.log(response)
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
            if (changes.length > 0){
                field_save()
            }
            sweet_save("El registro ha sido " + text + " con exito", 3000, href);
        });
    });
    function field_save(){
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'fields_save',
                'changes': JSON.stringify(changes),
            },
            dataType: "json",
        }).done(function (data) {                      
            if (!data.hasOwnProperty('error')) {
                return false;
            }                       
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {                        
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
    
        });
      }
    ingresos.list();
});