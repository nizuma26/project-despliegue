//Creo una variable para eliminar el compflicto de libreria con el simbolo dolar y Jquery
let $ = jQuery.noConflict();
function message_error(obj) {
    let html = '';
	if (typeof(obj) === 'object') {
		$.each(obj, function(key, value) {
			html += value
		})
	} else {
		html = obj
	}
    Swal.fire({
        title: 'Error!',
        iconColor: '#f27474',
        timer: 3900,
        timerProgressBar: true,
        html: html,
        confirmButtonText: '<i class="fa fa-thumbs-up"></i> OK!',
        confirmButtonColor: '#289aff',
        icon: 'error',         
    });
}

const testss = '#f27474'

function sweet_info(title){
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
        timer: 2900,
        timerProgressBar: true,        
      })
      Toast.fire({
        icon: 'success',
        title: title
      })
}
// Swal.fire({
//     title: 'Custom animation with Animate.css',
//     showClass: {
//       popup: 'animate__animated animate__fadeInDown'
//     },
//     hideClass: {
//       popup: 'animate__animated animate__fadeOutUp'
//     }
//   })
function sweet_save(title, timer, url){
    Swal.fire({
        title: 'Genial!',
        text: title,
        icon: 'success',
        timer: timer,
        timerProgressBar: true,
        confirmButtonText: '<i class="fa fa-thumbs-up"></i> OK!',
        confirmButtonColor: '#289aff',
        willClose: () => {
            location.href = url;
        }
    }).then((result) => {

    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'modern',
        title: title,
        icon: 'fa fa-info-circle',
        content: content,
        type: 'blue',
        columnClass: 'small',
        typeAnimated: false,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'custom-btn-primary',
                action: function () { 
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {                      
                        if (!data.hasOwnProperty('error')) {                            
                            callback(data);
                            return false;
                        }                       
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {                        
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                action: function () {

                }
            },
        }
    })
}

function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'modern',
        title: title,
        icon: 'fa fa-info-circle',
        type: 'blue',
        content: content,
        columnClass: 'small',
        typeAnimated: false,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'custom-btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                action: function () {
                    cancel();
                }
            },
        }
    })
}

//Solo texto
function Solo_Texto(e) {
    let code;
    if (!e) var e = window.event;
    if (e.keyCode) code = e.keyCode;
    else if (e.which) code = e.which;
    let character = String.fromCharCode(code);
    let AllowRegex  = /^[\ba-zA-Z\s]$/;
    if (AllowRegex.test(character)) return true;     
    return false; 
  }

//Solo numeros
function Solo_Numero(e){
    let keynum = window.event ? window.event.keyCode : e.which;
    if ((keynum == 8) || (keynum == 46))
    return true;
    return /\d/.test(String.fromCharCode(keynum));
}


//Solo numeros sin puntos 
function Solo_Numero_ci(e){
    let keynum = window.event ? window.event.keyCode : e.which;
    if ((keynum == 8))
    return true;
    return /\d/.test(String.fromCharCode(keynum));
}

// solo numeros y letras sin caracteres especiales
function Texto_Numeros(e) {
    let code;
    if (!e) var e = window.event;
    if (e.keyCode) code = e.keyCode;
    else if (e.which) code = e.which;
    let character = String.fromCharCode(code);
    let AllowRegex  = /^[A-Za-z0-9\s\.,-]+$/g;
    if (AllowRegex.test(character)) return true;     
    return false; 
}
const showDropdown = (content, button) =>{
    const dropdownContent = document.getElementById(content)
    const dropdownButton = document.getElementById(button)
    
    dropdownButton.addEventListener('click', () =>{
        dropdownContent.classList.toggle('show-dropdown')        
    })
    document.addEventListener('click', function (event) {
        if (!dropdownContent.contains(event.target) && !dropdownButton.contains(event.target)) {
            dropdownContent.classList.remove('show-dropdown');
          }
      });
 }
 
// const dropdown= document.getElementById('dropdownID');
//   let dropdownActive = false;

//   $('#btn-dropdown').click(() => {
//       if (dropdownActive == false) {
//           dropdown.classList.add("active");
//           dropdownActive = true;
//       } else if (dropdownActive == true) {
//           dropdown.classList.remove("active");
//           dropdownActive = false;
//       }
//   });
  