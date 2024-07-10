from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import subprocess
import numpy as py
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from random import sample
from controller.controllerGasto import *
#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 
#El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
import os 
from os import remove #Modulo  para remover archivo
from os import path #Modulo para obtener la ruta o directorio
import controller.database as db
from datetime import datetime
template_dir =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'controller', 'templates')

from controller.config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)


application = app

msg  =''
tipo =''

#CONVERSIÓN DE FORMATO DE PESOS
def int_a_pesos(monto_entero):
    return "${:,.2f}".format(monto_entero)

def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

#Funcion que recorre todos los archivos almacenados en la carpeta (archivos)  
def listaArchivos():
    urlFiles = 'static/archivos'
    return (os.listdir(urlFiles))


csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Routes to Render Something
@app.route('/homee', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def homee():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM turno")
    myresult = cursor.fetchall()
    #Convertir a Diccionario
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for recrod in myresult:
        insertObject.append(dict(zip(columnName, recrod)))
    cursor.close()
    return render_template("index.html", data=insertObject)


#RUTA PARA AGREGAR TURNO
@app.route('/add_turnos', methods=['POST'])
@login_required
@csrf.exempt
def add_turnos():
    fecha_in = request.form['FechaIn']
    fecha_out = request.form['FechaOut']
    turno = request.form['Turno']
    if turno and fecha_in and fecha_out:
        cursor = db.connection.cursor()
        sql = "INSERT INTO turno (turno_cod, fecha_in, fecha_out) VALUES (%s, %s, %s)"
        data = (turno, fecha_in, fecha_out)
        cursor.execute(sql, data)
        db.connection.commit()
    return redirect(url_for('homee'))


#RUTA PARA BUSQUEDA DE ARQUEO 
@app.route('/search_arqueos', methods=['GET'])
@login_required
@csrf.exempt
def search_arqueos():
    turno = request.args.get('Turno')
    cur = db.connection.cursor()
    query = "SELECT * FROM arqueos WHERE turno_cod = %s"
    cur.execute(query, (turno,))
    filtered_data = cur.fetchall()
    cur.close()
    return render_template('index.html', data_arqueo=filtered_data)

# RUTA PARA EDITAR ARQUEO
@app.route('/edit_arqueos/<string:id>', methods=['POST'])
@login_required
@csrf.exempt
def edit_arqueos(id):
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    if empleado and recibido and entregado and entregadoM and observacion:
        cursor = db.connection.cursor()
        sql = "UPDATE arqueos SET empleado =%s, base_recibida =%s, base_entregada =%s, entrega_caja_m =%s, observacion =%s WHERE Id =%s"
        data_arqueo = (empleado, recibido, entregado, entregadoM, observacion, id)
        cursor.execute(sql, data_arqueo)
        db.connection.commit()
    return redirect(url_for('homee'))

#RUTA PARA ELIMINAR ARQUEO
@app.route('/delete_arqueos/<string:id>')
@login_required
@csrf.exempt
def delete_arqueos(id):
    cursor = db.connection.cursor()
    sql = "DELETE FROM arqueos WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('homee'))

#RUTA PARA AGREGAR VENTA
@app.route('/add_ventas', methods=['POST'])
@login_required
@csrf.exempt
def add_ventas():
    turno = request.form['Turno']
    concepto = request.form['Concepto']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['Otros']
    if turno and concepto and efectivo and datafono and otros:
        cursor = db.connection.cursor()
        sql = "INSERT INTO ventas (turno_cod, concepto, efectivo, datafono, otros) VALUES (%s, %s, %s, %s, %s)"
        data_ventas = (turno, concepto, efectivo, datafono, otros)
        cursor.execute(sql, data_ventas)
        db.connection.commit()
    return redirect(url_for('homee'))

#RUTA PARA AGREGAR VENTA TIENDA
@app.route('/add_ventas_tienda', methods=['POST'])
@login_required
@csrf.exempt
def add_ventas_tienda():
    producto_id = request.form['Producto']
    cantidad = request.form['Cantidad']
    total = request.form['Total']
    if producto_id and cantidad and total:
        cursor = db.connection.cursor()
        sql = "INSERT INTO ventas_mecato (producto_id, cantidad, total) VALUES (%s, %s, %s)"
        data_ventas_tienda = (producto_id, cantidad, total)
        cursor.execute(sql, data_ventas_tienda)
        db.connection.commit()
    return redirect(url_for('tienda'))

#RUTA PARA AGREGAR GASTO
@app.route('/add_gastos', methods=['POST'])
@login_required
@csrf.exempt
def add_gastos():
    turno = request.form['Turno']
    responsable = request.form['Responsable']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    if turno and responsable and beneficiario and concepto and valor:
        cursor = db.connection.cursor()
        sql = "INSERT INTO gastos (turno_cod, responsable, beneficiario, concepto, valor_pagado) VALUES (%s, %s, %s, %s, %s)"
        data_gastos = (turno, responsable, beneficiario, concepto, valor)
        cursor.execute(sql, data_gastos)
        db.connection.commit()
    return redirect(url_for('homee'))

#RUTA PARA BUSQUEDA DE GASTOS 
@app.route('/search_gastos', methods=['GET'])
@login_required
@csrf.exempt
def search_gastos():
    turno_gasto = request.args.get('Turno')
    cur = db.connection.cursor()
    query = "SELECT * FROM gastos WHERE turno_cod = %s"
    cur.execute(query, (turno_gasto,))
    filtered_data = cur.fetchall()
    cur2 = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur2.execute(query, (turno_gasto,))
    filtered_data2 = cur2.fetchall()
    cur.close()
    cur2.close()
    suma_valor_gasto = 0
    suma_total_gasto = 0
    for fila in filtered_data2:
        # Suponiendo que la columna que deseas sumar se llama 'valor'
        suma_valor_gasto += int(fila['valor_pagado'])
        suma_total_gasto = int_a_pesos(suma_valor_gasto)
    return render_template('index.html', data_gastos=filtered_data, suma_total_gasto=suma_total_gasto)

#RUTA PARA BUSQUEDA DE VENTAS 
@app.route('/search_ventas', methods=['GET'])
@login_required
@csrf.exempt
def search_ventas():
    turno = request.args.get('Turno')
    
    # Búsqueda de gastos
    cur_gastos = db.connection.cursor()
    query_gastos = "SELECT * FROM gastos WHERE turno_cod = %s"
    cur_gastos.execute(query_gastos, (turno,))
    filtered_gastos = cur_gastos.fetchall()
    
    cur_gastos_dict = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur_gastos_dict.execute(query_gastos, (turno,))
    filtered_gastos_dict = cur_gastos_dict.fetchall()
    
    suma_valor_gasto = sum(int(fila['valor_pagado']) for fila in filtered_gastos_dict)
    suma_total_gasto = int_a_pesos(suma_valor_gasto)
    
    cur_gastos.close()
    cur_gastos_dict.close()
    
    # Búsqueda de ventas
    cur_ventas = db.connection.cursor()
    query_ventas = "SELECT * FROM ventas WHERE turno_cod = %s"
    cur_ventas.execute(query_ventas, (turno,))
    filtered_ventas = cur_ventas.fetchall()
    
    cur_ventas_dict = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur_ventas_dict.execute(query_ventas, (turno,))
    filtered_ventas_dict = cur_ventas_dict.fetchall()
    
    suma_valor_efectivo = sum(int(fila['efectivo']) for fila in filtered_ventas_dict)
    suma_valor_datafono = sum(int(fila['datafono']) for fila in filtered_ventas_dict)
    suma_valor_otros = sum(int(fila['otros']) for fila in filtered_ventas_dict)
    
    suma_total_venta = suma_valor_efectivo + suma_valor_datafono + suma_valor_otros
    suma_total_venta_pesos = int_a_pesos(suma_total_venta)
    
    cur_ventas.close()
    cur_ventas_dict.close()
    
    return render_template('index.html', data_gastos=filtered_gastos, suma_total_gasto=suma_total_gasto,
                           data_ventas=filtered_ventas, suma_total_efectivo=int_a_pesos(suma_valor_efectivo),
                           suma_total_datafono=int_a_pesos(suma_valor_datafono),
                           suma_total_otros=int_a_pesos(suma_valor_otros),
                           suma_total_venta=suma_total_venta_pesos)

#RUTA PARA AGREGAR ARQUEOS
@app.route('/add_arqueos', methods=['GET','POST'])
@login_required
@csrf.exempt
def add_arqueos():
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    valor_recibido=request.form['suma_total_venta']
    valor_gastado=request.form['suma_total_gasto']
    total_venta = valor_recibido.replace('$', '').replace(',', '')
    total_gasto = valor_gastado.replace('$', '').replace(',', '')
    total_arqueo = float(total_venta) + float(recibido) - float(total_gasto) # Convertir a float si es necesario
    total_fin_arqueo = float(entregado)+float(entregadoM)
    # Verificar que entregadoM sea igual a suma_total_arqueo
    if turno and empleado and recibido and entregado and entregadoM and total_arqueo == total_fin_arqueo:
        cursor = db.connection.cursor()
        sql = "INSERT INTO arqueos (turno_cod, empleado, base_recibida, base_entregada, entrega_caja_m, observacion) VALUES (%s, %s, %s, %s, %s, %s)"
        data_arqueo = (turno, empleado, recibido, entregado, entregadoM, observacion)
        cursor.execute(sql, data_arqueo)
        db.connection.commit()
        return redirect(url_for('homee'))
    else:
        flash('El valor de Entrega no coincide con el valor total del arqueo', 'error')
        return redirect(url_for('homee'))  # Puedes crear una función para mostrar el formulario de nuevo



#Ruta Para Eliminar
@app.route('/delete/<string:id>')
@login_required
@csrf.exempt
def delete(id):
    cursor = db.connection.cursor()
    sql = "DELETE FROM arqueo WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('homee'))

#Ruta para Eliminar en tabla de Gastos
@app.route('/delete_gastos/<string:id>')
@login_required
@csrf.exempt
def delete_gastos(id):
    cursor = db.connection.cursor()
    sql = "DELETE FROM gastos WHERE id=%s"
    data_gastos = (id,)
    cursor.execute(sql, data_gastos)
    db.connection.commit()
    return redirect(url_for('homee'))

#Ruta Para Editar
@app.route('/edit/<string:id>', methods=['POST'])
@login_required
@csrf.exempt
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
        cursor = db.connection.cursor()
        sql = "UPDATE arqueo SET turno_cod =%s, empleado =%s, base_recibida =%s, efectivo =%s, datafono =%s, otros =%s, gastos =%s, base_entregada =%s, entrega_caja_m =%s WHERE Id =%s"
        data = (turno, empleado, recibido, efectivo, datafono, otros, gastos, entregado, entregadoM, id)
        cursor.execute(sql, data)
        db.connection.commit()
    return redirect(url_for('homee'))

# RUTA PARA EDITAR GASTOS
@app.route('/edit_gastos/<string:id>', methods=['POST'])
@login_required
@csrf.exempt
def edit_gastos(id):
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    if turno and empleado and beneficiario and concepto and valor:
        cursor = db.connection.cursor()
        sql = "UPDATE gastos SET turno_cod =%s, responsable =%s, beneficiario =%s, concepto =%s, valor_pagado =%s WHERE Id =%s"
        data_gastos = (turno, empleado, beneficiario, concepto, valor, id)
        cursor.execute(sql, data_gastos)
        db.connection.commit()
    return redirect(url_for('homee'))




#Creando mi decorador para el home, el cual retornara la Lista de Gastos
@app.route('/evidencia', methods=['GET','POST'])
@login_required
def inicio():
    return render_template('layout2.html', miData = listaGastos())


#RUTAS
@app.route('/registrar-Gasto', methods=['GET','POST'])
@login_required
def addGasto():
    return render_template('acciones/add.html')


 
#Registrando nuevo gasto
@app.route('/gasto', methods=['POST'])
@login_required
@csrf.exempt
def formAddGasto():
    if request.method == 'POST':
        turno               = request.form['turno']
        concepto            = request.form['concepto']
        valor               = request.form['valor']
        beneficiario        = request.form['beneficiario']
        responsable         = request.form['responsable']
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrarGasto(turno, concepto, valor, beneficiario, responsable, nuevoNombreFile)
            if(resultData ==1):
                return render_template('layout2.html', miData = listaGastos(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('layout2.html', miData = listaGastos(), msg='El Registro fue un éxito', tipo=1)
                #return render_template('layout2.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('layout2.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-gasto/<string:id>', methods=['GET','POST'])
@login_required
@csrf.exempt
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateGasto(id)
        if resultData:
            return render_template('acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('layout2.html', miData = listaGastos(), msg='No existe el gasto', tipo= 1)
    else:
        return render_template('layout2.html', miData = listaGastos(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-del-gasto/<int:idGasto>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def viewDetalleGasto(idGasto):
    msg =''
    if request.method == 'GET':
        resultData = detallesdelGasto(idGasto) #Funcion que almacena los detalles del gasto
        
        if resultData:
            return render_template('acciones/view.html', infoGasto = resultData, msg='Detalles del Gasto', tipo=1)
        else:
            return render_template('acciones/layout2.html', msg='No existe el registro', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-gasto/<string:idGasto>', methods=['POST'])
@login_required
@csrf.exempt
def  formActualizarGasto(idGasto):
    if request.method == 'POST':
        turno           = request.form['turno']
        concepto        = request.form['concepto']
        valor           = request.form['valor']
        beneficiario    = request.form['beneficiario']
        responsable     = request.form['responsable']
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarGasto(turno, concepto, valor, beneficiario, responsable, fotoForm, idGasto)
        else:
            fotoGasto  ='sin_foto.jpg'
            resultData = recibeActualizarGasto(turno, concepto, valor, beneficiario, responsable, fotoGasto, idGasto)

        if(resultData ==1):
            return render_template('layout2.html', miData = listaGastos(), msg='Datos actualizados', tipo=1)
        else:
            msg ='Actualización correcta del registro'
            return render_template('layout2.html', miData = listaGastos(), msg='Datos actualizados', tipo=1)
            #return render_template('layout2.html', miData = listaGastos(), msg='No se pudo actualizar', tipo=1)


#Eliminar Gasto
@app.route('/borrar-gasto', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def formViewBorrarGasto():
    if request.method == 'POST':
        idGasto         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarGasto(idGasto, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarGasto(id='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM gastos WHERE id=%s', (id,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/fotos_gastos', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar

def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/fotos_gastos', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

#RUTA PARA INVENTARIO 
@app.route('/tienda', methods=['GET'])
@login_required
@csrf.exempt
def tienda():
    codigo = request.args.get('Código')
    cur = db.connection.cursor()
    query = "SELECT * FROM inventario WHERE id = %s"
    cur.execute(query, (codigo,))
    filtered_data = cur.fetchall()
    cur.close()
    return render_template('tienda.html', data_inventario=filtered_data)

#RUTA PARA EDITAR INVENTARIO 
@app.route('/edit_inventario', methods=['POST'])
@login_required
@csrf.exempt
def edit_inventario():
    producto_id = request.form['Codigo']
    nombre = request.form['Nombre']
    cantidad = request.form['Cantidad']
    
    if producto_id and nombre and cantidad:
        cursor = db.connection.cursor()
        sql = "UPDATE inventario SET cantidad = %s WHERE id = %s"
        data = (cantidad, producto_id)  # Asegúrate de pasar los parámetros en el orden correcto
        cursor.execute(sql, data)
        db.connection.commit()
        cursor.close()  # Cierra el cursor después de usarlo
    
    return redirect(url_for('tienda'))

# Función genérica para actualizar la cantidad
def actualizar_cantidad(id_producto, nuevo_valor, operacion):
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT cantidad FROM inventario WHERE id = %s", (id_producto,))
        resultado = cursor.fetchone()

        if resultado:
            cantidad_actual = resultado[0]
            if operacion == 'entrada':
                cantidad_nueva = cantidad_actual + nuevo_valor
            elif operacion == 'salida':
                cantidad_nueva = cantidad_actual - nuevo_valor
            else:
                return jsonify({"mensaje": "Operación no válida"}), 400

            cursor.execute("UPDATE inventario SET cantidad = %s WHERE id = %s", (cantidad_nueva, id_producto))
            db.connection.commit()

            return jsonify({"mensaje": f"Cantidad actualizada a {cantidad_nueva}"}), 200
        else:
            return jsonify({"mensaje": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"mensaje": f"Error de conexión a la base de datos: {e}"}), 500
    finally:
        cursor.close()

# Ruta para la entrada de cantidad de productos al inventario
@app.route('/entrada', methods=['POST'])
@login_required
@csrf.exempt
def entrada_cantidad():
    try:
        id_producto = request.json.get('id')
        nuevo_valor = request.json.get('nuevo_valor')

        if not id_producto or not nuevo_valor:
            return jsonify({"mensaje": "Faltan datos requeridos"}), 400

        return actualizar_cantidad(id_producto, nuevo_valor, 'entrada')

    except Exception as e:
        return jsonify({"mensaje": f"Error al procesar la entrada: {e}"}), 500

# Ruta para la salida de cantidad de productos al inventario
@app.route('/salida', methods=['POST'])
@login_required
@csrf.exempt
def salida_cantidad():
    try:
        id_producto = request.json.get('id')
        nuevo_valor = request.json.get('nuevo_valor')

        if not id_producto or not nuevo_valor:
            return jsonify({"mensaje": "Faltan datos requeridos"}), 400

        return actualizar_cantidad(id_producto, nuevo_valor, 'salida')

    except Exception as e:
        return jsonify({"mensaje": f"Error al procesar la salida: {e}"}), 500


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host='127.0.0.1', debug=True)
