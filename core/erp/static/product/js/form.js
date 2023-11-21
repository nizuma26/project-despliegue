let produc_catalago =
{
    items:
    {
        codigo: '',
        nombre: '',
        descripcion: '',
        componentes: '',
        unida_medida: '',
        tipo_item: '',
        activo: '',
        lote: '',
        serie: '',
        categorias: '',
        marca: '',
        modelo: '',
        moneda: '',
        grupobien: '',
        subgrupobien: '',
        imagen: '',
        usuario: '',
        pagaimpuesto: '',
        inventariable: ''
    },

};

$(function () {
$('#formproduc').on('submit', function (e) {
    console.log($("#idcategoria :selected").text());
    console.log($('select[name="categorias"] option:selected').text());
    e.preventDefault();    
    produc_catalago.items.codigo= $('input[name="codigo"]').val();
    produc_catalago.items.nombre= $('input[name="nombre"]').val().toUpperCase();;
    produc_catalago.items.descripcion= $('textarea[name="descripcion"]').val();
    produc_catalago.items.componentes= $('textarea[name="componentes"]').val();
    produc_catalago.items.unida_medida= $('select[name="unida_medida"]').val();
    produc_catalago.items.activo= $('#idactivo').prop("checked")
    produc_catalago.items.pagaimpuesto= $('#idpagaimpuesto').prop("checked")
    produc_catalago.items.lote= $('#idlote').prop("checked")
    produc_catalago.items.serie= $('#idserie').prop("checked")
    produc_catalago.items.inventariable= $('#idinv').prop("checked")    
    produc_catalago.items.categorias= {id: $('select[name="categorias"]').val(), name: $("#idcategoria :selected").text()}
    produc_catalago.items.marca= {id: $('select[name="marca"]').val(), name: $("#idmarca :selected").text()}
    produc_catalago.items.modelo= {id: $('select[name="modelo"]').val(), name: $("#idmodelo :selected").text()}
    produc_catalago.items.moneda= {id: $('select[name="moneda"]').val(), name: $("#idmoneda :selected").text()}
    produc_catalago.items.grupobien= {id: $('select[name="grupobien"]').val(), name: $("#idgrupo :selected").text()}
    produc_catalago.items.subgrupobien= {id: $('select[name="subgrupobien"]').val(),name: $("#idsubgrupo :selected").text()}
    let filename;
    let valor = $('input[name="imagen"]').val();
    console.log(valor);
    if ($('input[name="imagen"]').val() == "") {
        filename = $imagenPrevisualizacion.src.replace(/.*(\/|\\)/, "");
        produc_catalago.items.imagen = "producto/" + filename;
      } else {
        filename = $('input[name="imagen"]').val().replace(/.*(\/|\\)/, "");
        produc_catalago.items.imagen = "producto/" + filename;
      }
   if  ($('input[name="imagen"]').val() == ''){
       // produc_catalago.items.imagen= $imagenPrevisualizacion.src;
        filename = $imagenPrevisualizacion.src.replace(/.*(\/|\\)/, '');
        produc_catalago.items.imagen= "producto/" + filename;
    }else{
        filename = $('input[name="imagen"]').val().replace(/.*(\/|\\)/, '');
        produc_catalago.items.imagen= "producto/" + filename;
    }

    let parameters = new FormData();
    parameters.append('action', $('input[name="actionprod"]').val());
    parameters.append('produc_catalago', JSON.stringify(produc_catalago.items));

    let url="";
    let titulo="";
    let text = "";
    let href = "/erp/product/list/";

    if  ($('input[name="actionprod"]').val() == 'add'){
        url =  '/erp/product/add/';
        titulo="¿Estas seguro de crear el producto?";
        text = "creado";
    }else{
        url = window.location.pathname;
        titulo="¿Estas seguro de actualizar los datos del producto?";
        text = "modificado"
    }
    submit_with_ajax(url, 'Estimado(a) Usuario  ', titulo, parameters, function (response) {
        sweet_save('El producto ha sido ' + text + ' con exito', 2500, href);
    });
});


    $('.btnAddCategoria').on('click', function () {
        $('input[name="action"]').val('add');
        $('#modaltitle3').find('span').html('Creando Nueva Categoría');
        $('#modaltitle3').find('i').removeClass().addClass('fas fa-plus');
        $('#idnombrecateg').focus();
        $('#modalCategory').modal('show');
        });   
        $('#modalCategory').on('hidden.bs.modal', function (e) {
            $('#frmCatgorias').trigger('reset');           
        })
        $('#frmCatgorias').on('submit', function (e) {
            e.preventDefault();
            let myForm = document.getElementById('frmCatgorias');
            let parameters = new FormData(myForm);                 
            let url =  '/erp/product/add/';
            let titulo="¿Estas seguro de crear la categoria?";            
            parameters.append('action', 'create_Categoria');
            submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
                let newOption = new Option(response.nombre, response.id, false, true);
                   $('select[name="categorias"]').append(newOption).trigger('change');
                   sweet_info( 'La Categoría Se Ha Creado Con Éxito'); 
                   $('#modalCategory').modal('hide');
                });
        });
        /////Marcas de producto/////////////////////////////////////////////////////  
       $('.btnAddMarca').on('click', function () {
            $('input[name="action"]').val('add');
            $('#titlemarca').find('span').html('Creación de una Marca');
            $('#titlemarca').find('i').removeClass().addClass('fas fa-plus');
            $('#idmarca').focus();
            $('#myModalMarcas').modal('show');
        });  
        $('#myModalMarcas').on('hidden.bs.modal', function (e) {
            $('#frmMarcas').trigger('reset');          
        })
        $('#frmMarcas').on('submit', function (e) {
            e.preventDefault();
            let myForm = document.getElementById('frmMarcas');
            let parameters = new FormData(myForm);
            
            let url="";
            let titulo="";
            if  ($('input[name="action"]').val() == 'add'){
                url =  '/erp/product/add/';
                titulo="¿Estas seguro de crear la Marca?";
            }else{
                url = "/erp/product/update/"+param_id+"/";
                titulo="¿Estas seguro de actualizar la Marca?";
            }
            parameters.append('action', 'create_Marca');
        
            submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
                let newOption = new Option(response.marca, response.id, false, true);
                $('select[name="marca"]').append(newOption).trigger('change');
                $('#myModalMarcas').modal('hide');
                sweet_info( 'La Marca Se Ha Creado Con Éxito'); 
                });
            }); 
        ////Modelos de producto/////////////////////////////////////////////////////
        $('.btnAddModelo').on('click', function () {
            $('input[name="action"]').val('add');
            $('#titlemodelo').find('span').html('Creación de un Modelo');
            $('#titlemodelo').find('i').removeClass().addClass('fas fa-plus');
            $('#idmodelo').focus();
            $('#myModalModelos').modal('show');
        });
        $('#myModalModelos').on('hidden.bs.modal', function (e) {
            $('#idmarcas').val("").trigger('change.select2');
            $('#frmModelos').trigger('reset');           
        })    
        $('#frmModelos').on('submit', function (e) {
            e.preventDefault();
            let myForm = document.getElementById('frmModelos');
            let parameters = new FormData(myForm);
            
            let url="";
            let titulo="";
            if  ($('input[name="action"]').val() == 'add'){
                url =  '/erp/product/add/';
                titulo="¿Estas seguro de crear el Modelo?";
            }else{
                url = "/erp/product/update/"+param_id+"/";
                titulo="¿Estas seguro de actualizar el Modelo?";
            }
            parameters.append('action', 'create_Modelo');
        
            submit_with_ajax(url, 'Estimado usuario(a)', titulo, parameters, function (response) {
                let newOption = new Option(response.modelo, response.id, false, true);
                $('select[name="modelo"]').append(newOption).trigger('change');
                $('#myModalModelos').modal('hide');  
                sweet_info( 'El Modelo Se Ha Creado Con Éxito'); 
                });
            });
});

