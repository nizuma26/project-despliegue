let data_list;
let type_request = '';

let cantidad_aprobada = {
    productos: []
}
let aprobados = {
    productos: []
}
const get_detail_data = () => {
    $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: {
            'action': 'detail_data',
        },
        dataType: "json",
    }).done(function (response) {
        let table = ''
        if (!response.hasOwnProperty('error')) {            
            const products = response.items;
            type_request = response.type;
            if (response.status === 'EN ESPERA' && response.type === 'EN_DEPOSITO'){
                products.map((item) =>{
                    if (item.cantidad > item.stock_actual){
                        item.cantidad_aprobada = item.stock_actual
                    } else{
                        item.cantidad_aprobada = item.cantidad
                    }
                    cantidad_aprobada.productos.push(item);
                })
            }else if (response.status === 'EN ESPERA' && response.type === 'EN_USO') {
                products.map((item) =>{
                    aprobados.productos.push(item.codigo_bien_id);
                })
            }
            
            if (response.type === 'EN_DEPOSITO'){
                table = `
                <tr>
                    <th scope="col" style="width: 38%;">PRODUCTO</th>
                    <th scope="col" style="width: 19%;">CATEGORIA</th>
                    <th scope="col" style="width: 17%;">CANTIDAD SOLICITADA</th>
                    <th scope="col" style="width: 12%;">STOCK ACTUAL</th>
                    <th scope="col" style="width: 14%;">CANTIDAD APROBADA</th>
                </tr>`
                $('#thead_detail').html(table);
                data_list = $('#detail').DataTable({
                    data: response.items,            
                    order: false,
                    paging: false,
                    ordering: false,
                    info: false,
                    searching: false,
                    columns: [
                        {"data": "full_name"},
                        {"data": "categoria"},
                        {"data": "cantidad", className: 'text-center'},
                        {"data": "stock_actual", className: 'text-center'},
                        {"data": "prod_id"},                        
                    ],
                    columnDefs: [                        
                        {
                            targets: [-1],
                            class: "text-center",
                            orderable: false,
                            render: function(data, type, row){
                                if (response.status == 'EN ESPERA' && response.perm){
                                    if (row.cantidad > row.stock_actual){
                                        return `<input type="text" class="form-control input-flat" name="cant" style="font-size: 11px; height: 24px;" autocomplete="off" value="${row.stock_actual}">`
                                    }
                                    return `<input type="text" class="form-control input-flat" name="cant" style="font-size: 11px; height: 24px;" autocomplete="off" value="${row.cantidad}">`
                                }else if (response.status == 'EN ESPERA' && response.perm === false){
                                    return '<span>0</span>'
                                }
                                return `<span>${row.cantidad_aprobada}</span>`

                            }
                        }
                    ],
                    rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                        $(row).find('input[name="cant"]').TouchSpin({
                            min: 0,
                            max: data.stock_actual,
                            buttonup_class: 'btn btn-secondary btn-xs btn-flat',
                            buttondown_class: 'btn btn-secondary btn-xs btn-flat'
                        });
                    },
                    initComplete: function (settings, json) {
            
                    }
                });
                // table = `<thead class="wrapper container">
                //     <tr>
                //         <th scope="col" style="width: 40%;">PRODUCTO</th>
                //         <th scope="col" style="width: 20%;">CATEGORIA</th>
                //         <th scope="col" style="width: 20%;">CANTIDAD</th>
                //         <th scope="col" style="width: 20%;">CANTIDAD APROBADA</th>
                //     </tr>
                // </thead>
                // <tbody class="f-11">
                // ${products.map((item) => {
                //     return `<tr>
                //         <td>${item.full_name}</td>
                //         <td>${item.categoria}</td>
                //         <td>${item.cantidad}</td>
                //         <td><input type="text" class="form-control input-flat" name="cant" style="font-size: 11px; height: 24px;" autocomplete="off" value="${item.cantidad}"></td>
                //     </tr>`;
                // }).join('')}
                // </tbody>`
            }else{
                table = `
                <tr>
                    <th scope="col" style="width: 45%;">PRODUCTO</th>
                    <th scope="col" style="width: 20%;">CATEGORIA</th>
                    <th scope="col" style="width: 25%;">CÓDIGO DE BIEN</th>
                    <th scope="col" style="width: 10%;">APROBADOS</th>
                </tr>`
                $('#thead_detail').html(table);
                data_list = $('#detail').DataTable({
                    data: response.items,            
                    order: false,
                    paging: false,
                    ordering: false,
                    info: false,
                    searching: false,
                    columns: [
                        {"data": "full_name"},
                        {"data": "categoria"},
                        {"data": "codigo_bien"},
                        {"data": "codigo_bien_id"},                        
                    ],
                    columnDefs: [                             
                        {
                            targets: [-1],
                            class: "text-center",
                            orderable: false,
                            render: function(data, type, row){
                                if (response.status === 'EN ESPERA' && response.perm){
                                    return `<label class="checkbox-container"><input class="objectCheck" type="checkbox" data-id="${row.prod_id}" name="product" value="${row.codigo_bien_id}" checked><span class="checkmark"></span></label>`
                                }
                                else if (response.status === 'EN ESPERA' && response.perm === false) {
                                    return `<span><tool-tip role="tooltip"> En espera</tool-tip><i class="fas fa-clock text-secondary"></i></span>`
                                }
                                else if (row.aprobado) {
                                    return `<span><tool-tip role="tooltip"> Aprobado</tool-tip><i class="fas fa-check text-secondary"></i></span>`
                                } else{
                                    return `<span><tool-tip role="tooltip"> Rechazado</tool-tip><i class="fas fa-times text-secondary"></i></span>`
                                }
                            }
                        }
                    ],
                    initComplete: function (settings, json) {
            
                    }
                });            
        }
        }
        //message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
    
    console.log(cantidad_aprobada)
}
$(function () {
    $('#detail tbody').on('change', 'input[name="cant"]', function () {
        let cant = parseInt($(this).val());
        const tr = data_list.cell($(this).closest('td, li')).index();
        cantidad_aprobada.productos[tr.row].cantidad_aprobada = cant;
        console.log(cantidad_aprobada.productos[tr.row])
    });
    $('#detail tbody').on('change', 'input[type="checkbox"]', function () {
        let tr = $("#detail").DataTable().cell($(this).closest('td, li')).index();
        let id = $("#detail").DataTable().row(tr.row).data().codigo_bien_id;
        console.log(id)
    
        if ($(this).is(':checked')) {
          aprobados.productos.push(id);
        } else {
          let index = aprobados.productos.indexOf(id);
          if (index > -1) {
            aprobados.productos.splice(index, 1);
          }
        }       
      });

});
get_detail_data();





