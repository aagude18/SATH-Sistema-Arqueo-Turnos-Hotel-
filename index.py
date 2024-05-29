from flask import Flask, render_template, request, redirect, url_for# Render Template es para redireccionar las rutas a los template HTML
import os
import src.database as db
from datetime import datetime
template_dir =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__) # Inicia flask y lo almacena en una variable

#CONVERSIÓN DE FORMATO DE FECHA 
def convertir_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return None

#CONVERSIÓN DE FORMATO DE PESOS
def int_a_pesos(monto_entero):
    return "${:,.2f}".format(monto_entero)

# Routes to Render Something
@app.route('/')
def home():
    cursor = db.mydb.cursor()
    cursor.execute("SELECT * FROM arqueo")
    myresult = cursor.fetchall()
    #Convertir a Diccionario
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for recrod in myresult:
        insertObject.append(dict(zip(columnName, recrod)))
    cursor.close()
    return render_template("index.html", data=insertObject)

#Ruta para la busqueda de Arqueo 
@app.route('/search_turno', methods=['GET'])
def search_turno():
    turno_code = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT Id, turno_cod, empleado, base_recibida, efectivo, datafono, otros, gastos, base_entregada, entrega_caja_m FROM arqueo WHERE turno_cod = %s"
    cur.execute(query, (turno_code,))
    filtered_data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=filtered_data)

#Ruta para la busqueda de Gastos 
@app.route('/search_gastos', methods=['GET'])
def search_gastos():
    turno_gasto = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT * FROM gastos WHERE turno_cod = %s"
    cur.execute(query, (turno_gasto,))
    filtered_data = cur.fetchall()
    cur2 = db.mydb.cursor(dictionary=True)
    cur2.execute(query, (turno_gasto,))
    filtered_data2 = cur2.fetchall()
    cur.close()
    cur2.close()
    suma_valor = 0
    suma_total = 0
    for fila in filtered_data2:
        # Suponiendo que la columna que deseas sumar se llama 'valor'
        suma_valor += int(fila['valor_pagado'])
        suma_total = int_a_pesos(suma_valor)
    return render_template('index.html', data_gastos=filtered_data, suma_total=suma_total)

#Ruta para la busqueda de Ventas 
@app.route('/search_ventas', methods=['GET'])
def search_ventas():
    turno_venta = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT * FROM habitaciones WHERE turno_cod = %s"
    cur.execute(query, (turno_venta,))
    filtered_data = cur.fetchall()
    cur2 = db.mydb.cursor(dictionary=True)
    cur2.execute(query, (turno_venta,))
    filtered_data2 = cur2.fetchall()
    cur.close()
    cur2.close()
    suma_valor_efectivo = 0
    suma_total_efectivo = 0
    suma_valor_datafono = 0
    suma_total_datafono = 0
    suma_valor_otros = 0
    suma_total_otros = 0
    for fila in filtered_data2:
        # Suponiendo que la columna que deseas sumar se llama 'valor'
        suma_valor_efectivo += int(fila['efectivo'])
        suma_total_efectivo = int_a_pesos(suma_valor_efectivo)
        suma_valor_datafono += int(fila['datafono'])
        suma_total_datafono = int_a_pesos(suma_valor_datafono)
        suma_valor_otros += int(fila['otros'])
        suma_total_otros = int_a_pesos(suma_valor_otros)
    return render_template('index.html', data_ventas=filtered_data, suma_total_efectivo=suma_total_efectivo, suma_total_datafono=suma_total_datafono, suma_total_otros=suma_total_otros)



# Ruta para guardar Usuarios en La BD
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['Username']
    name = request.form['Name']
    password = request.form['Password']
    if username and name and password:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO users (Username, Firstname, Passw) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.mydb.commit()
    return redirect(url_for('home'))

#Ruta Para Eliminar
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.mydb.cursor()
    sql = "DELETE FROM arqueo WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.mydb.commit()
    return redirect(url_for('home'))

#Ruta para Eliminar en tabla de Gastos
@app.route('/delete_gastos/<string:id>')
def delete_gastos(id):
    cursor = db.mydb.cursor()
    sql = "DELETE FROM gastos WHERE id=%s"
    data_gastos = (id,)
    cursor.execute(sql, data_gastos)
    db.mydb.commit()
    return redirect(url_for('home'))

#Ruta Para Editar
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
        cursor = db.mydb.cursor()
        sql = "UPDATE arqueo SET turno_cod =%s, empleado =%s, base_recibida =%s, efectivo =%s, datafono =%s, otros =%s, gastos =%s, base_entregada =%s, entrega_caja_m =%s WHERE Id =%s"
        data = (turno, empleado, recibido, efectivo, datafono, otros, gastos, entregado, entregadoM, id)
        cursor.execute(sql, data)
        db.mydb.commit()
    return redirect(url_for('home'))

# Ruta para Editar Gastos
@app.route('/edit_gastos/<string:id>', methods=['POST'])
def edit_gastos(id):
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    if turno and empleado and beneficiario and concepto and valor:
        cursor = db.mydb.cursor()
        sql = "UPDATE gastos SET turno_cod =%s, responsable =%s, beneficiario =%s, concepto =%s, valor_pagado =%s WHERE Id =%s"
        data_gastos = (turno, empleado, beneficiario, concepto, valor, id)
        cursor.execute(sql, data_gastos)
        db.mydb.commit()
    return redirect(url_for('home'))


@app.route('/enlaces', strict_slashes=False)
def enlaces():
    return render_template("enlaces.html")

@app.route('/homee', strict_slashes=False)
def homee():
    return render_template("homee.html")

#Nuevas Rutas
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
        # Convertir las fechas al formato YYYY-MM-DD
        fecha_inicio_convertida = convertir_fecha(fecha_inicio)
        fecha_fin_convertida = convertir_fecha(fecha_fin)
        if fecha_inicio_convertida is None or fecha_fin_convertida is None:
            return "Error en la conversión de fechas", 400
        cursor = db.mydb.cursor()
        sql = "INSERT INTO arqueo (fecha_in, fecha_out, turno_cod, empleado, base_recibida, efectivo, datafono, otros, base_entregada, entrega_caja_m, gastos, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (fecha_inicio_convertida, fecha_fin_convertida, turno, empleado, recibido, efectivo, datafono, otros, entregado, entregadoM, gastos, observacion,)
        cursor.execute(sql, data)
        db.mydb.commit()
    return redirect(url_for('home'))

#Ruta para los Gastos 
@app.route('/user3', methods=['POST'])
def addUser3():
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    if turno and empleado and beneficiario and concepto and valor:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO gastos (turno_cod, responsable, beneficiario, concepto, valor_pagado) VALUES (%s, %s, %s, %s, %s)"
        data_gastos = (turno, empleado, beneficiario, concepto, valor)
        cursor.execute(sql, data_gastos)
        db.mydb.commit()
    return redirect(url_for('home'))

#Ruta para los Ventas 
@app.route('/ventas', methods=['POST'])
def ventas():
    turno = request.form['Turno']
    habitacion = request.form['Habitacion']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['Otros']
    if turno and habitacion and efectivo and datafono and otros:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO habitaciones (turno_cod, hab, efectivo, datafono, otros) VALUES (%s, %s, %s, %s, %s)"
        data_ventas = (turno, habitacion, efectivo, datafono, otros)
        cursor.execute(sql, data_ventas)
        db.mydb.commit()
    return redirect(url_for('home'))

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
