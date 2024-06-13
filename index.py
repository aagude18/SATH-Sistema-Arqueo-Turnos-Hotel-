from flask import Flask, render_template, request,jsonify, redirect, url_for# Render Template es para redireccionar las rutas a los template HTML
import os
from src.database import mydb
from datetime import datetime
template_dir =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__) # Inicia flask y lo almacena en una variable

#CONVERSIÓN DE FORMATO DE PESOS
def int_a_pesos(monto_entero):
    return "${:,.2f}".format(monto_entero)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

# Ruta para agregar turno
@app.route('/add_turnos', methods=['POST'])
def add_turnos():
    fecha_in = request.form['FechaIn']
    fecha_out = request.form['FechaOut']
    turno = request.form['Turno']

    if turno and fecha_in and fecha_out:
        try:
            cursor = mydb.cursor()
            sql = "INSERT INTO turno (turno_cod, fecha_in, fecha_out) VALUES (%s, %s, %s)"
            data = (turno, fecha_in, fecha_out)
            cursor.execute(sql, data)
            mydb.commit()
            cursor.close()
            return jsonify({'message': 'Turno creado exitosamente'}), 200
        except Exception as e:
            return jsonify({'message': 'Error al crear el turno', 'error': str(e)}), 500
        


# Ruta para agregar arqueos
@app.route('/add_arqueos', methods=['POST'])
def add_arqueos():
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    
    if turno and empleado and recibido and entregado and entregadoM:
        cursor = mydb.cursor()
        sql = "INSERT INTO arqueos (turno_cod, empleado, base_recibida, base_entregada, entrega_caja_m, observacion) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (turno, empleado, recibido, entregado, entregadoM, observacion)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('dashboard'))

    
#Ruta para buscar todo
@app.route('/search_all', methods=['GET'])
def search_all():
    turno = request.args.get('Turno')
    
    # Buscar arqueos
    cursor_turno = mydb.cursor(dictionary=True)
    query_turno = "SELECT * FROM turno WHERE turno_cod = %s"
    cursor_turno.execute(query_turno, (turno,))
    turno_data = cursor_turno.fetchall()
    cursor_turno.close()
    
    # Buscar arqueos
    cursor_arqueos = mydb.cursor(dictionary=True)
    query_arqueos = "SELECT * FROM arqueos WHERE turno_cod = %s"
    cursor_arqueos.execute(query_arqueos, (turno,))
    arqueos_data = cursor_arqueos.fetchall()
    cursor_arqueos.close()
    
    # Buscar ventas
    cursor_ventas = mydb.cursor(dictionary=True)
    query_ventas = "SELECT * FROM ventas WHERE turno_cod = %s"
    cursor_ventas.execute(query_ventas, (turno,))
    ventas_data = cursor_ventas.fetchall()
    cursor_ventas.close()

    # Buscar gastos
    cursor_gastos = mydb.cursor(dictionary=True)
    query_gastos = "SELECT * FROM gastos WHERE turno_cod = %s"
    cursor_gastos.execute(query_gastos, (turno,))
    gastos_data = cursor_gastos.fetchall()
    cursor_gastos.close()

    return jsonify({
        'arqueos': arqueos_data,
        'ventas': ventas_data,
        'gastos': gastos_data,
        'turno':turno_data
    })




# Ruta para eliminar arqueo
@app.route('/delete_arqueos/<string:id>')
def delete_arqueos(id):
    cursor = mydb.cursor()
    sql = "DELETE FROM arqueos WHERE id = %s"
    cursor.execute(sql, (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('dashboard'))

# Ruta para agregar venta
@app.route('/add_ventas', methods=['POST'])
def add_ventas():
    turno = request.form['Turno']
    concepto = request.form['Concepto']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['Otros']
    
    if turno and concepto and efectivo and datafono and otros:
        cursor = mydb.cursor()
        sql = "INSERT INTO ventas (turno_cod, concepto, efectivo, datafono, otros) VALUES (%s, %s, %s, %s, %s)"
        data = (turno, concepto, efectivo, datafono, otros)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('dashboard'))

# Ruta para agregar gasto
@app.route('/add_gastos', methods=['POST'])
def add_gastos():
    turno = request.form['Turno']
    responsable = request.form['Responsable']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    
    if turno and responsable and beneficiario and concepto and valor:
        cursor = mydb.cursor()
        sql = "INSERT INTO gastos (turno_cod, responsable, beneficiario, concepto, valor_pagado) VALUES (%s, %s, %s, %s, %s)"
        data = (turno, responsable, beneficiario, concepto, valor)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('home'))




# Ruta para agregar usuario
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['Username']
    name = request.form['Name']
    password = request.form['Password']
    
    if username and name and password:
        cursor = mydb.cursor()
        sql = "INSERT INTO users (Username, Firstname, Passw) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('home'))

# Ruta para eliminar usuario
@app.route('/delete/<string:id>')
def delete(id):
    cursor = mydb.cursor()
    sql = "DELETE FROM arqueo WHERE id = %s"
    cursor.execute(sql, (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('dashboard'))

# Ruta para eliminar gasto
@app.route('/delete_gastos/<string:id>')
def delete_gastos(id):
    cursor = mydb.cursor()
    sql = "DELETE FROM gastos WHERE id = %s"
    cursor.execute(sql, (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('dashboard'))

# Ruta para editar arqueo
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['OtrosMedios']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    gastos = request.form['Gastos']

    if empleado and recibido and efectivo and datafono and otros and entregado and entregadoM and gastos:
        cursor = mydb.cursor()
        sql = "UPDATE arqueo SET turno_cod = %s, empleado = %s, base_recibida = %s, efectivo = %s, datafono = %s, otros = %s, gastos = %s, base_entregada = %s, entrega_caja_m = %s WHERE Id = %s"
        data = (turno, empleado, recibido, efectivo, datafono, otros, gastos, entregado, entregadoM, id)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('home'))

# Ruta para editar gasto
@app.route('/edit_gastos/<string:id>', methods=['POST'])
def edit_gastos(id):
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    
    if turno and empleado and beneficiario and concepto and valor:
        cursor = mydb.cursor()
        sql = "UPDATE gastos SET turno_cod = %s, responsable = %s, beneficiario = %s, concepto = %s, valor_pagado = %s WHERE Id = %s"
        data = (turno, empleado, beneficiario, concepto, valor, id)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('home'))

@app.route('/enlaces', strict_slashes=False)
def enlaces():
    return render_template("enlaces.html")

@app.route('/homee', strict_slashes=False)
def homee():
    return render_template("homee.html")

# Ruta para agregar usuario con más campos
@app.route('/user2', methods=['POST'])
def addUser2():
    fecha_inicio = request.form['FechaIn']
    fecha_fin = request.form['FechaOut']
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['OtrosMedios']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    gastos = request.form['Gastos']
    observacion = request.form['Observacion']
    
    if fecha_inicio and fecha_fin and turno and empleado and recibido and efectivo and datafono and otros and entregado and entregadoM and gastos:
        cursor = mydb.cursor()
        sql = "INSERT INTO arqueo (fecha_in, fecha_out, turno_cod, empleado, base_recibida, efectivo, datafono, otros, base_entregada, entrega_caja_m, gastos, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (fecha_inicio, fecha_fin, turno, empleado, recibido, efectivo, datafono, otros, entregado, entregadoM, gastos, observacion)
        cursor.execute(sql, data)
        mydb.commit()
        cursor.close()
    return redirect(url_for('home'))

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)