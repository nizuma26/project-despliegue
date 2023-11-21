let dttStock;
let products = {
    values: []
};

let stock = {
    list: function () {
        let parameters = {
            'action': 'searchdata',
            'almacen': $('select[name="almacenes"]').val(),    
        };
        dttStock = $('#data_stock').DataTable({
            responsive: false,
            autoWidth: true,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
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
            columns: [
                {"data": "id_prod"},
                {"data": "prod"},
                {"data": "categorias"},
                {"data": "precio"},
                {"data": "stock"},
                {"data": "stock_min"},
                {"data": "stock_max"},
            ],    
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2)+ ' Bs.';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if(row.stock > row.stock_min){
                            return '<span class="badge badge-success badge-pill" style="font-size: 10px;">'+data+'</span>'
                        }else if(row.stock == 0){
                            return '<span class="badge badge-danger badge-pill" style="font-size: 10px;"><tool-tip role="tooltip"> Sin Stock</tool-tip>'+data+'</span>'
                        }
                        return '<span class="badge badge-warning badge-pill" style="font-size: 10px;"><tool-tip role="tooltip"> Por debajo del minimo</tool-tip>'+data+'</span>'
                    }
                }, 
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control" style="font-size: 11px; height: 24px;" name="stock_min" autocomplete="off" value="' + row.stock_min + '">';

                    }
                }, 
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control" style="font-size: 11px; height: 24px;" name="stock_max" autocomplete="off" value="' + row.stock_max + '">';
                    }
                },              
                ],
                rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                    $(row).find('input[name="stock_min"]').TouchSpin({                                                  
                        min: 0,
                        max: 1000000,
                        buttonup_class: 'btn btnTouchspinUp btn-xs btn-flat',
                        buttondown_class: 'btn btnTouchspinDown btn-xs btn-flat'                               
                    });
                    $(row).find('input[name="stock_max"]').TouchSpin({                                                  
                        min: 0,
                        max: 1000000,
                        buttonup_class: 'btn btnTouchspinUp btn-xs btn-flat',
                        buttondown_class: 'btn btnTouchspinDown btn-xs btn-flat'                               
                    });           
                    
                },       
                initComplete: function (settings, json) {
                
            }
        });
        
    },
    
};
$(function () { 
    $('#data_stock').on('change', 'input[name="stock_min"], input[name="stock_max"]', function() {
        let tr = dttStock.cell($(this).closest('td, li')).index();
        let id = dttStock.row(tr.row).data();
        let fila = $(this).closest('tr'); // Obtener la fila actual
        let idProd = fila.find('td:eq(0)').text(); // Obtener el ID del producto
        let stockMin = fila.find('input[name="stock_min"]').val(); // Obtener el valor de stock_min
        let stockMax = fila.find('input[name="stock_max"]').val(); // Obtener el valor de stock_max
        products.values[idProd] = {id:id.id, stockMin: stockMin, stockMax: stockMax };
      });

    $('select[name="almacenes"]').on('change', function () {        
        stock.list(true);
        products.values = [];
    });

    stock.list(false);    
        $('#formStock').on('submit', function (e) {
         e.preventDefault();         
         let myForm = document.getElementById('formStock');
         let parameters = new FormData(myForm);        
         parameters.append('value', JSON.stringify(products));                
         parameters.append('almacen', $('select[name="almacenes"]').val());        
         parameters.append('param_id', $('input[name="id"]').val());        
             
         let url="";
         let titulo="";         
         let param_id= $('input[name="id"]').val();
         if  ($('input[name="action"]').val() == 'edit'){
             url =  '/erp/stock/list/';
             titulo="¿Estas seguro de realizar la siguiente acción?";             
         }         
         submit_with_ajax(url, 'Estimado(a) Usuario  ', titulo, parameters, function (response) {                 
            dttStock.ajax.reload();  
            Swal.fire({
				title: 'Notificación',                           
				text: 'SE GUARDARON LOS CAMBIOS EXITOSAMENTE',
				icon: 'success',	
                timer: 2700,			
                timerProgressBar: true,
                confirmButtonText: '<i class="fa fa-thumbs-up"></i> OK!',
                confirmButtonColor: '#289aff',
			})
            products.values = [];  
         });
    });        
});