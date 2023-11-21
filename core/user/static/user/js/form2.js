$(function () {
    $('#formprofile').on('submit', function (e) {
     e.preventDefault();
     //var parameters = new FormData();
     //url: '{% url 'erp:product_create' %}',
     //url = "product/update/"+datos.id+"",
     //let myForm = document.querySelector('formproduc');
     let myForm = document.getElementById('formprofile');
     let parameters = new FormData(myForm);
     //let parameters = new FormData(myForm);
     //var parameters = new FormData(form);
     let url="";
     let titulo="";
     
     let param_id= $('input[name="id"]').val();
     if  ($('input[name="action"]').val() == 'edit'){
         url =  '/user/profile/';
         titulo="¿Estas seguro de editar los datos del usuario?";
     }
    // var url = "/product/add/";
     submit_with_ajax(url, 'Estimado(a) Usuario  ', titulo, parameters, function (response) {
         location.href = '/inicio/';
       // $('#productos').data.reload();
      //  tblClient.ajax.reload();
     
     });
   });   
 
});

