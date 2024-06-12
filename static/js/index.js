$(document).ready(function(){
    $('#search_ventas').submit(function(e){
        e.preventDefault(); // Evita envio por defecto del formulario

        $.ajax({
            url: '/search_ventas',
            method: 'GET',
            data: { Turno: $('#turnoInput').val() },
            success: function(response) {
                // Actualización de los resultados
                $('#ventasresult').html(response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});

$(document).ready(function(){
    $('#search_arqueos').submit(function(e){
        e.preventDefault(); // Evita envio por defecto del formulario

        $.ajax({
            url: '/search_arqueos',
            method: 'GET',
            data: { Turno: $('#turno_arqueo').val() },
            success: function(response) {
                // Actualización de los resultados
                $('#arqueoresult').html(response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});

$(document).ready(function() {
    $('#add_turnos').submit(function(e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        $.ajax({
            url: '/add_turnos',
            method: 'POST',
            data: {
                FechaIn: $('#fecha_ingreso').val(),
                FechaOut: $('#fecha_salida').val(),
                Turno: $('#CodigoDelTurno').val()
            },
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Turno creado exitosamente',
                    text: response.message
                });
                // Limpiar los campos del formulario
                $('#add_turnos')[0].reset();
            },
            error: function(response) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al crear el turno',
                    text: response.responseJSON.message
                });
            }
        });
    });
});
