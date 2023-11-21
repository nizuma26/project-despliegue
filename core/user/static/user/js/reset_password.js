$(function () {
    $('#formpass').on('submit', function (e) {
     e.preventDefault();
     let myForm = document.getElementById('formpass');
     let parameters = new FormData(myForm);
     let titulo="";
     
     let param_id= $('input[name="id"]').val();
     if  ($('input[name="action"]').val() == 'edit'){        
         titulo="¿Estas seguro de cambiar la contraseña?";
     }    
     
    // var url = "/product/add/";
     submit_with_ajax(window.location.pathname, 'Estimado(a) Usuario  ', titulo, parameters, function (response) {
         location.href = "/inicio/";
         
         
       // $('#productos').data.reload();
      //  tblClient.ajax.reload();
     
     });

     
   });  
 
});