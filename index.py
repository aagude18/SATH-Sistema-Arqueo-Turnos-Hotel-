from flask import Flask, render_template, request, redirect, url_for# Render Template es para redireccionar las rutas a los template HTML
import os
import src.database as db
from datetime import datetime
template_dir =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__) # Inicia flask y lo almacena en una variable

# Creating simple Routes 
#@app.route('/test')
#def test():
#    return "Home Page"

#@app.route('/test/about/')
#def about_test():
#    return "About Page"

def convertir_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return None

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

#Ruta para la busqueda 
@app.route('/search_turno', methods=['GET'])
def search_turno():
    turno_code = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT Id, turno_cod, empleado, base_recibida, efectivo, datafono, otros, gastos, base_entregada, entrega_caja_m FROM arqueo WHERE turno_cod = %s"
    cur.execute(query, (turno_code,))
    filtered_data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=filtered_data)

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


#Ruta Para Eliminar
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

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
