const get_detail_data = () => {
    $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: {
            'action': 'detail_data',
        },
        dataType: "json",
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            console.log(data);
            const products = data.items;
            let table = ''
            if (data.type === 'BM'){
              table = `<thead class="wrapper container">
                    <tr>
                    <th scope="col" style="width: 37%;">PRODUCTO</th>
                    <th scope="col" style="width: 8%;">STOCK</th>
                    <th scope="col" style="width: 15%;">PRECIO</th>
                    <th scope="col" style="width: 20%;">CÓDIGO DE BIEN</th>
                    <th scope="col" style="width: 20%;">UBICACIÓN FÍSICA</th>
                    </tr>
                </thead>
                <tbody class="f-11">
                ${products.map((item) => {
                    return `<tr>
                        <td>${item.full_name}</td>
                        <td class="f-13"><span class="badge badge-secondary badge-pill">${item.stock_actual}</span></td>
                        <td>${item.precio}</td>
                        <td>${item.codbien}</td>
                        <td>${item.codubica}</td>
                    </tr>`;
                }).join('')}
                </tbody>`
            }else{
                table = `<thead class="wrapper container">
                    <tr>
                    <th scope="col" style="width: 8%;">CODIGO</th>
                    <th scope="col" style="width: 31%;">PRODUCTO</th>
                    <th scope="col" style="width: 10%;">STOCK</th>
                    <th scope="col" style="width: 14%;">PRECIO</th>
                    <th scope="col" style="width: 10%;">CANTIDAD</th>
                    <th scope="col" style="width: 8%;">SUBTOTAL</th>
                    <th scope="col" style="width: 9%;">LOTE</th>
                    <th scope="col" style="width: 9%;">FECHA_VENC</th>
                    </tr>
                </thead>
                <tbody class="f-11">
                ${products.map((item) => {
                    return `<tr>
                        <td>${item.codigo}</td>
                        <td>${item.full_name}</td>
                        <td class="f-13"><span class="badge badge-secondary badge-pill">${item.stock_actual}</span></td>
                        <td>${item.precio}</td>
                        <td>${item.cant}</td>
                        <td>${item.subtotal}</td>
                        <td>${item.nro_lote}</td>
                        <td>${item.fecha_venc}</td>
                    </tr>`;
                }).join('')}
                </tbody>`
            }
            $('#detail').html(table);
        }
        //message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

get_detail_data();