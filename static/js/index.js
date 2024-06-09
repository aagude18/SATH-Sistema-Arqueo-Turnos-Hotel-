$(document).ready(function(){
    $('#search_ventas').submit(function(e){
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        $.ajax({
            url: '/search_ventas',
            method: 'GET',
            data: { Turno: $('#turnoInput').val() },
            success: function(response) {
                // Aquí actualizas el contenedor con los datos recibidos
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
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        $.ajax({
            url: '/search_arqueos',
            method: 'GET',
            data: { Turno: $('#turno_arqueo').val() },
            success: function(response) {
                // Aquí actualizas el contenedor con los datos recibidos
                $('#arqueoresult').html(response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});

