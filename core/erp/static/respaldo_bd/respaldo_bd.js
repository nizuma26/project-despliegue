// BOTONES DE ABRIR Y CERRAR EL MODAL

function abrir_modal_verificacion() {
	$("#ModalConfirmacion").modal("show");
	$("#password1").focus();
	$("#password1").val('');
	$("#password2").val('');
}

function cerrar_modal_verificacion() {
	$("#ModalConfirmacion").modal("hide");
	$("#password1").val('');
	$("#password2").val('');
}

// BOTONES PARA ABRIR EL MODAL DEL FORMULARIO DE RESTABLECIMIENTO
function abrir_modal_upload() {
	$("#ModalConfirmacion_upload").modal("show");
	$("#password_1").focus();
	$("#password_1").val('');
	$("#password_2").val('');
	$("#upload_file").val('');
}

function cerrar_modal_upload() {
	$("#ModalConfirmacion_upload").modal("hide");
	$("#password_1").val('');
	$("#password_2").val('');
	$("#upload_file").val('');
}

// ENVIO DEL FORMULARIO CON AJAX
$('#form_verificacion').on('submit', function(e) {
	e.preventDefault();
	if ($("#password1").val() !== $("#password2").val()) {
		message_error('Las contraseñas no coinciden, intenta nuevamente');
		$("#password1").val('');
		$("#password2").val('');
		$("#password1").focus();
	} else {
		let parameters = new FormData(this);
		parameters.append('action', 'validate_export_data');
		//$('#spinner_download_bd').html('<div class="spinner" id="spinner"></div>');
		submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar esta accion?', parameters, function() {
			//$('#spinner_download_bd').fadeIn(1000).html('');
			$("#ModalConfirmacion").modal('hide');
			sweet_info( 'AUTENTICACIÓN EXITOSA, DESCARGANDO BASE DE DATOS');		
		});
	}
});

// SUBIR LA BASE DE DATOS
$('#form_verificacion_upload').on('submit', function(e) {
	e.preventDefault();
	if ($("#upload_file").val() == null || $("#upload_file").val() == '') {
		message_error('Se debe seleccionar el archivo de la base de datos');
	}else{
		let parameters = new FormData(this);
		parameters.append('action', 'validate_import_data');
		$('#spinner_load_bd').html('<div class="spinner" id="spinner"></div>');
		submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar esta accion?', parameters, function(response) {
			$('#spinner_load_bd').fadeIn(1000).html('');
			$("#ModalConfirmacion").modal('hide');
			sweet_info( 'LA BASE DE DATOS HA SIDO RESTAURADA');
			setTimeout(() => {
				window.location.replace('/inicio/');
			}, 1400);
		
		});
	}

});