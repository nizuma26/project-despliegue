const state = document.querySelector('.status')
const status_change_btn = document.querySelector('.status_change')

$('.status_change').on('click', function () {    
    $('#manage_state_title').find('i').removeClass().addClass('fas fa-pen');
    $('#manage_state_title').find('span').html('Cambiar Estado');
    $('#modalManageState').modal('show')
});
// const get_detail_data = () => {
//     $.ajax({
//         url: '/erp/salida/add/',
//         type: "POST",
//         data: {
//             'action': 'request_data',
//         },
//         dataType: "json",
//     }).done(function (data) {
        
//         //message_error(data.error);
//     }).fail(function (jqXHR, textStatus, errorThrown) {
//         alert(textStatus + ': ' + errorThrown);
//     }).always(function (data) {

//     });
// }

// $('.transform').on('click', function () {
    
// });

$('#manage_state').on('submit', function (e) {
    e.preventDefault();
    let myForm = document.getElementById('manage_state');
    let parameters = new FormData(myForm);
    console.log(this.getAttribute('data-url'))
    const url = this.getAttribute('data-url');
    const estado = $('select[name="estado"]').val();
    const title = "¿Estas seguro de actualizar el Estado?";
    if (url === '/aprobaciones/solicitud/movimiento/'){
        parameters.append('type', type_request);
        if (estado === 'APROBADO' && type_request === 'EN_DEPOSITO'){
            parameters.append('cantidad_aprobada', JSON.stringify(cantidad_aprobada.productos));
        } else if (estado === 'APROBADO' && type_request === 'EN_USO'){
            parameters.append('aprobados', JSON.stringify(aprobados.productos));
        }       
    }
    parameters.append('action', 'manage_state');
    parameters.append('id', $('input[name="id"]').val());
    parameters.append('new_status', $('select[name="estado"]').val());
    parameters.append('motive', $('textarea[name="motive"]').val());
    submit_with_ajax(url, 'Estimado usuario(a)', title, parameters, function (response) {           
        $('#modalManageState').modal('hide');
        $('textarea[name="motive"]').val('')
        sweet_info('Estado modificado con exito');
        if (state && status_change_btn){
            state.textContent = response.state;
            status_change_btn.remove();
        }
        notifySocket.send(
            JSON.stringify({
                type: response.type,
                title: response.title,
                message: response.message,
                url: response.url,
                image: 'notificaciones/info.png',
                user_id: response.user_id,
                permissions: '',
            })
        );
    });
});    