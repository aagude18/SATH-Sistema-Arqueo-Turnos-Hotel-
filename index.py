from flask import Flask, render_template, request, redirect, jsonify, url_for
from random import sample
from werkzeug.utils import secure_filename
import os
from src.database import mydb_connection

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la carpeta de carga de archivos estáticos y extensiones permitidas
app.config['UPLOAD_FOLDER'] = 'static/archivos/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Función para generar una cadena aleatoria
def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud = 20
    secuencia = string_aleatorio.upper()
    resultado_aleatorio = sample(secuencia, longitud)
    return "".join(resultado_aleatorio)

# Función para verificar la extensión de un archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



# Ruta para eliminar un archivo
@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    filename = request.json.get('filename')
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'message': 'Archivo eliminado exitosamente.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Función para listar archivos en la carpeta estática
def listaArchivos():
    urlFiles = 'static/archivos'
    return os.listdir(urlFiles)

# Función para convertir un monto entero a formato de pesos
def int_a_pesos(monto_entero):
    return "${:,.2f}".format(monto_entero)

# Ruta de inicio
@app.route('/')
def home():
    return render_template("login.html")

# Ruta del dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

# Ruta para agregar turnos
@app.route('/add_turnos', methods=['POST'])
def add_turnos():
    fecha_in = request.form['FechaIn']
    fecha_out = request.form['FechaOut']
    turno = request.form['Turno']

    if turno and fecha_in and fecha_out:
        try:
            connection = mydb_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO turno (turno_cod, fecha_in, fecha_out) VALUES (%s, %s, %s)"
            data = (turno, fecha_in, fecha_out)
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Turno creado exitosamente'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error al crear el turno', 'error': str(e)}), 500
        
        
@app.route('/add_arqueos', methods=['POST'])
def add_arqueos():
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    
    if turno and empleado and recibido and entregado and entregadoM:
        mydb=mydb_connection()
        cursor = mydb.cursor()
        sql = "INSERT INTO arqueos (turno_cod, empleado, base_recibida, base_entregada, entrega_caja_m, observacion) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (turno, empleado, recibido, entregado, entregadoM, observacion)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('dashboard'))


# Ruta para buscar todos los datos
@app.route('/search_all', methods=['GET'])
def search_all():
    turno = request.args.get('Turno')
    
    mydb = mydb_connection()
    cursor_turno = mydb.cursor(dictionary=True)
    query_turno = "SELECT * FROM turno WHERE turno_cod = %s"
    cursor_turno.execute(query_turno, (turno,))
    turno_data = cursor_turno.fetchall()
    cursor_turno.close()
    
    cursor_arqueos = mydb.cursor(dictionary=True)
    query_arqueos = "SELECT * FROM arqueos WHERE turno_cod = %s"
    cursor_arqueos.execute(query_arqueos, (turno,))
    arqueos_data = cursor_arqueos.fetchall()
    cursor_arqueos.close()
    
    cursor_ventas = mydb.cursor(dictionary=True)
    query_ventas = "SELECT * FROM ventas WHERE turno_cod = %s"
    cursor_ventas.execute(query_ventas, (turno,))
    ventas_data = cursor_ventas.fetchall()
    cursor_ventas.close()

    cursor_gastos = mydb.cursor(dictionary=True)
    query_gastos = "SELECT * FROM gastos WHERE turno_cod = %s"
    cursor_gastos.execute(query_gastos, (turno,))
    gastos_data = cursor_gastos.fetchall()
    cursor_gastos.close()

    return jsonify({
        'arqueos': arqueos_data,
        'ventas': ventas_data,
        'gastos': gastos_data,
        'turno': turno_data
    })

# Ruta para eliminar arqueos por ID
@app.route('/delete_arqueos/<string:id>')
def delete_arqueos(id):
    mydb = mydb_connection()
    cursor = mydb.cursor()
    sql = "DELETE FROM arqueos WHERE id = %s"
    cursor.execute(sql, (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('dashboard'))

# Ruta para agregar ventas
@app.route('/add_ventas', methods=['POST'])
def add_ventas():
    turno = request.form['Turno']
    concepto = request.form['Concepto']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['Otros']
    mydb = mydb_connection()
    
    if turno and concepto and efectivo and datafono and otros:
        cursor = mydb.cursor()
        
        arqueoexist = "SELECT COUNT(*) FROM arqueos WHERE turno_cod = %s"
        cursor.execute(arqueoexist, (turno,))
        verificacion = cursor.fetchone()
        
        if verificacion[0] > 0:
            cursor.close()
            return jsonify({'error': 'No se pueden crear más ventas en este turno.'}), 400
        else:
            sql = "INSERT INTO ventas (turno_cod, concepto, efectivo, datafono, otros) VALUES (%s, %s, %s, %s, %s)"
            data = (turno, concepto, efectivo, datafono, otros)
            cursor.execute(sql, data)
            mydb.commit()
            cursor.close()
            return redirect(url_for('dashboard'))
    else:
        return jsonify({'error': 'Datos incompletos.'}), 400
    
    
@app.route('/add_gastos', methods=['POST'])
def add_gastos():
    turno = request.form['Turno']
    responsable = request.form['Responsable']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    mydb = mydb_connection()
    cursor = mydb.cursor()
    
    
    arqueoexist = "SELECT COUNT(*) FROM arqueos WHERE turno_cod = %s"
    cursor.execute(arqueoexist, (turno,))
    verificacion = cursor.fetchone()
        
    if verificacion[0] > 0:
        cursor.close()
        return jsonify({'error': 'No se pueden crear más gastos en este turno.'}), 400
    else:
        # Verificar que se haya subido un archivo de evidencia
        if 'Evidencia' not in request.files:
            return jsonify({'error': 'No se proporcionó evidencia del gasto.'}), 400
        
        file = request.files['Evidencia']
        
        # Verificar que el archivo tenga un nombre y una extensión permitida
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Archivo no permitido o no seleccionado.'}), 400
        
        # Generar un nombre único para el archivo
        filename = secure_filename(file.filename)
        filename = f"{stringAleatorio()}_{filename}"
        
        # Guardar el archivo en la carpeta de carga estática
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Conectar a la base de datos y guardar los datos del gasto
        
        
        if turno and responsable and beneficiario and concepto and valor:
            try:
                sql = "INSERT INTO gastos (turno_cod, responsable, beneficiario, concepto, valor_pagado, evidencia) VALUES (%s, %s, %s, %s, %s, %s)"
                data = (turno, responsable, beneficiario, concepto, valor, filename)
                cursor.execute(sql, data)
                mydb.commit()
                cursor.close()
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(e)
                return jsonify({'error': 'Error al insertar en la base de datos.', 'exception': str(e)}), 500
        else:
            return jsonify({'error': 'Datos incompletos.'}), 400
    



if __name__ == '__main__':
    app.run(debug=True, port=5000)
