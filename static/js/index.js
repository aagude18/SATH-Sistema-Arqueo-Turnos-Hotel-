$(document).ready(function() {

    // Función para poblar el selector de empleados
    function populateEmpleadoSelect() {
        const empleados = ['Vanessa', 'Anguie', 'Lina'];
        const select = $('#Empleado');

        select.empty(); // Limpiar opciones anteriores

        empleados.forEach(empleado => {
            select.append(`<option value="${empleado}">${empleado}</option>`);
        });
    }

    // Capturar el envío del formulario de agregar turnos
    $('#add_turnos').on('submit', function(e) {
        e.preventDefault();
        const formData = $(this).serialize();

        $.ajax({
            url: '/add_turnos',
            method: 'POST',
            data: formData,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Turno agregado',
                    text: 'El turno se ha agregado exitosamente.',
                }).then(function() {
                    $('#add_turnos')[0].reset();
                });
            },
            error: function(error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema al agregar el turno. Inténtelo de nuevo.',
                });
            }
        });
    });

    // Capturar el envío del formulario de cierre de turno
    $('#formCierreTurno').on('submit', function(e) {
        e.preventDefault();
        const formData = $(this).serialize();

        $.ajax({
            url: '/add_arqueos',
            method: 'POST',
            data: formData,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Cierre de turno guardado',
                    text: 'Los detalles del cierre de turno se han guardado exitosamente.',
                }).then(function() {
                    $('#formCierreTurno')[0].reset();
                });
            },
            error: function(error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema al guardar el cierre de turno. Inténtelo de nuevo.',
                });
            }
        });
    });

    // Capturar el envío del formulario de ventas
    $('#formVentas').on('submit', function(e) {
        e.preventDefault();
        const formData = $(this).serialize();

        $.ajax({
            url: '/add_ventas',
            method: 'POST',
            data: formData,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Venta guardada',
                    text: 'Los detalles de la venta se han guardado exitosamente.',
                }).then(function() {
                    $('#formVentas')[0].reset();
                });
            },
            error: function(error) {
                let messajerror="Hubo un problema al guardar el gasto, por favor verifique e inténtelo de nuevo";
                if(error.responseJSON && error.responseJSON.error){
                    messajerror=error.responseJSON.error;
                }
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: messajerror,
                });
            }
        });
    });

    // Capturar el envío del formulario de gastos
    $('#formGastos').on('submit', function(e) {
        e.preventDefault();

        // Crear objeto FormData
        var formData = new FormData(this);

        // Enviar datos mediante AJAX
        $.ajax({
            url: '/add_gastos',
            method: 'POST',
            data: formData,
            processData: false,  // No procesar los datos (FormData se encarga)
            contentType: false,  // No configurar el tipo de contenido
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Gasto guardado',
                    text: 'Los detalles del gasto se han guardado exitosamente.',
                }).then(function() {
                    $('#formGastos')[0].reset();  // Limpiar el formulario después de éxito
                });
            },
            error: function(error) {
                let mensajeerror = "Hubo un problema al guardar el gasto, por favor verifique e inténtelo de nuevo";
                if (error.responseJSON && error.responseJSON.error) {
                    mensajeerror = error.responseJSON.error;
                }
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: mensajeerror,
                });
            }
        });
    });

    // Capturar el envío del formulario de búsqueda
    $('#search_form').on('submit', function(e) {
        e.preventDefault();
        const turno = $('#search_turno').val();

        if (!turno) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Por favor, ingrese un turno.',
            });
            return;
        }

        $.ajax({
            url: '/search_all',
            method: 'GET',
            data: { Turno: turno },
            success: function(response) {
                let resultados_html = '';

                // Tabla de Arqueos
                resultados_html += '<h4>Arqueos</h4><table class="table table-striped"><thead><tr><th>Fecha Inicio</th><th>Fecha Fin</th><th>Empleado</th><th>Base Recibida</th><th>Base Entregada</th><th>Entrega Admin</th><th>Observaciones</th></tr></thead><tbody>';
                response.arqueos.forEach(arqueo => {
                    resultados_html += `<tr>
                        <td>${arqueo.fecha_in}</td>
                        <td>${arqueo.fecha_out}</td>
                        <td>${arqueo.empleado}</td>
                        <td>${arqueo.base_recibida}</td>
                        <td>${arqueo.base_entregada}</td>
                        <td>${arqueo.entrega_caja_m}</td>
                        <td>${arqueo.observacion}</td>
                    </tr>`;
                });
                resultados_html += '</tbody></table>';

                // Tabla de Ventas
                resultados_html += '<h4>Ventas</h4><table class="table table-striped"><thead><tr><th>Turno</th><th>Concepto</th><th>Efectivo</th><th>Datafono</th><th>Otros Medios</th></tr></thead><tbody>';
                response.ventas.forEach(venta => {
                    resultados_html += `<tr>
                        <td>${venta.turno_cod}</td>
                        <td>${venta.concepto}</td>
                        <td>${venta.efectivo}</td>
                        <td>${venta.datafono}</td>
                        <td>${venta.otros}</td>
                    </tr>`;
                });
                resultados_html += '</tbody></table>';

                // Tabla de Gastos
                resultados_html += '<h4>Gastos</h4><table class="table table-striped"><thead><tr><th>Turno</th><th>Responsable</th><th>Beneficiario</th><th>Concepto</th><th>Valor</th><th>Evidencia</th></tr></thead><tbody>';
                response.gastos.forEach(gasto => {
                    // Construir la URL completa de la evidencia
                    const evidenciaUrl = `/static/archivos/${gasto.evidencia}`;

                    resultados_html += `<tr>
                        <td>${gasto.turno_cod}</td>
                        <td>${gasto.responsable}</td>
                        <td>${gasto.beneficiario}</td>
                        <td>${gasto.concepto}</td>
                        <td>${gasto.valor_pagado}</td>
                        <td><a href="${evidenciaUrl}" target="_blank">Ver Evidencia</a></td>
                    </tr>`;
                });
                resultados_html += '</tbody></table>';

                $('#resultados').html(resultados_html);
            },
            error: function(error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema al realizar la búsqueda. Inténtelo de nuevo.',
                });
            }
        });
    });
});
