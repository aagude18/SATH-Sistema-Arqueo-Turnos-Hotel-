    function convertSelection() {
        const selectElement = document.getElementById('selectElement');
        const inputElement = document.getElementById('inputElement');
        inputElement.value = selectElement.value;
    }

    $(document).ready(function() {
        // Manejar envío del formulario de turnos
        $('#add_turnos').on('submit', function(e) {
            e.preventDefault(); // Prevenir el envío del formulario

            const formData = $(this).serialize(); // Serializar los datos del formulario

            $.ajax({
                url: '/add_turnos',
                method: 'POST',
                data: formData,
                success: function(response) {
                    // Mostrar alerta de éxito con SweetAlert
                    Swal.fire({
                        icon: 'success',
                        title: 'Turno agregado',
                        text: 'El turno se ha agregado exitosamente.',
                    });

                    // Limpiar el formulario
                    $('#add_turnos')[0].reset();
                },
                error: function(error) {
                    // Mostrar alerta de error con SweetAlert
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Hubo un problema al agregar el turno. Inténtelo de nuevo.',
                    });
                }
            });
        });

        // Manejar envío del formulario de arqueo
        $('#add_arqueo').on('submit', function(e) {
            e.preventDefault(); // Prevenir el envío del formulario
            
            const formData = $(this).serialize(); // Serializar los datos del formulario
            
            $.ajax({
                url: '/add_arqueos',
                method: 'POST',
                data: formData,
                success: function(response) {
                    // Mostrar alerta de éxito con SweetAlert
                    Swal.fire({
                        icon: 'success',
                        title: 'Arqueo agregado',
                        text: 'El arqueo se ha agregado exitosamente.',
                    });

                    // Limpiar el formulario
                    $('#add_arqueo')[0].reset();
                }
            });
        });

        // Manejar envío del formulario de búsqueda
        $('#search_form').on('submit', function(e) {
            e.preventDefault();
            const turno = $('#search_turno').val();

            $.ajax({
                url: '/search_all',
                method: 'GET',
                data: { Turno: turno },
                success: function(response) {
                    let resultados_html = '';

                    // Arqueos
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

                    // Ventas
                    resultados_html += '<h4>Ventas</h4><table class="table table-striped"><thead><tr><th>Turno</th><th>Concepto</th><th>Efectivo</th><th>Datafono</th><th>Otros Medios</th></tr></thead><tbody>';
                    response.ventas.forEach(venta => {
                        resultados_html += `<tr>
                            <td>${venta.turno}</td>
                            <td>${venta.concepto}</td>
                            <td>${venta.efectivo}</td>
                            <td>${venta.datafono}</td>
                            <td>${venta.otros_medios}</td>
                        </tr>`;
                    });
                    resultados_html += '</tbody></table>';

                    // Gastos
                    resultados_html += '<h4>Gastos</h4><table class="table table-striped"><thead><tr><th>Turno</th><th>Responsable</th><th>Beneficiario</th><th>Concepto</th><th>Valor</th></tr></thead><tbody>';
                    response.gastos.forEach(gasto => {
                        resultados_html += `<tr>
                            <td>${gasto.turno}</td>
                            <td>${gasto.responsable}</td>
                            <td>${gasto.beneficiario}</td>
                            <td>${gasto.concepto}</td>
                            <td>${gasto.valor}</td>
                        </tr>`;
                    });
                    resultados_html += '</tbody></table>';

                    $('#resultados').html(resultados_html);
                },
                error: function(error){
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Hubo un problema al agregar el arqueo. Inténtelo de nuevo.',
                    });
                }
            });
        });
    });

