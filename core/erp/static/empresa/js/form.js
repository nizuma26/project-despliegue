$(function () {
    $('#formempresa').on('submit', function (e) {
     e.preventDefault();
     //var parameters = new FormData();
     //url: '{% url 'erp:product_create' %}',
     //url = "product/update/"+datos.id+"",
     //let myForm = document.querySelector('formproduc');
     let myForm = document.getElementById('formempresa');
     let parameters = new FormData(myForm);
     //let parameters = new FormData(myForm);
     //var parameters = new FormData(form);
     let url="";
     let titulo="";
     
     let param_id= $('input[name="id"]').val();
     if  ($('input[name="action"]').val() == 'edit'){
         url =  '/erp/empresa/update/';
         titulo="¿Estas seguro de editar los datos de la institución?";
     }
    // var url = "/product/add/";
     submit_with_ajax(url, 'Estimado(a) Usuario  ', titulo, parameters, function (response) {
         location.href = '/erp/empresa/list/';     
     });    
   }); 
   $("input[name='iva']").TouchSpin({
    min: 0.01,
    max: 100,
    step: 0.01,
    decimals: 2,
    boostat: 5,
    maxboostedstep: 10,
    postfix: '%'
  })  
 
});

