# Render Template es para redireccionar las rutas a los template HTML
from flask import Flask, render_template, request, redirect, url_for, jsonify
from random import sample
from controller.controllerGasto import *
#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 
#El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
import os 
from os import remove #Modulo  para remover archivo
from os import path #Modulo para obtener la ruta o directorio
import src.database as db
from datetime import datetime
template_dir =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__) # Inicia flask y lo almacena en una variable

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

# Routes to Render Something
@app.route('/', methods=['GET', 'POST'])
def home():
    cursor = db.mydb.cursor()
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
def add_turnos():
    fecha_in = request.form['FechaIn']
    fecha_out = request.form['FechaOut']
    turno = request.form['Turno']
    if turno and fecha_in and fecha_out:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO turno (turno_cod, fecha_in, fecha_out) VALUES (%s, %s, %s)"
        data = (turno, fecha_in, fecha_out)
        cursor.execute(sql, data)
        db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA AGREGAR ARQUEOS
@app.route('/add_arqueos', methods=['POST'])
def add_arqueos():
    turno = request.form['Turno']
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    if turno and empleado and recibido and entregado and entregadoM:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO arqueos (turno_cod, empleado, base_recibida, base_entregada, entrega_caja_m, observacion) VALUES (%s, %s, %s, %s, %s, %s)"
        data_arqueo = (turno, empleado, recibido, entregado, entregadoM, observacion)
        cursor.execute(sql, data_arqueo)
        db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA BUSQUEDA DE ARQUEO 
@app.route('/search_arqueos', methods=['GET'])
def search_arqueos():
    turno = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT * FROM arqueos WHERE turno_cod = %s"
    cur.execute(query, (turno,))
    filtered_data = cur.fetchall()
    cur.close()
    return render_template('index.html', data_arqueo=filtered_data)

# RUTA PARA EDITAR ARQUEO
@app.route('/edit_arqueos/<string:id>', methods=['POST'])
def edit_arqueos(id):
    empleado = request.form['Empleado']
    recibido = request.form['Recibido']
    entregado = request.form['Entregado']
    entregadoM = request.form['EntregadoM']
    observacion = request.form['Observacion']
    if empleado and recibido and entregado and entregadoM and observacion:
        cursor = db.mydb.cursor()
        sql = "UPDATE arqueos SET empleado =%s, base_recibida =%s, base_entregada =%s, entrega_caja_m =%s, observacion =%s WHERE Id =%s"
        data_arqueo = (empleado, recibido, entregado, entregadoM, observacion, id)
        cursor.execute(sql, data_arqueo)
        db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA ELIMINAR ARQUEO
@app.route('/delete_arqueos/<string:id>')
def delete_arqueos(id):
    cursor = db.mydb.cursor()
    sql = "DELETE FROM arqueos WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA AGREGAR VENTA
@app.route('/add_ventas', methods=['POST'])
def add_ventas():
    turno = request.form['Turno']
    concepto = request.form['Concepto']
    efectivo = request.form['Efectivo']
    datafono = request.form['Datafono']
    otros = request.form['Otros']
    if turno and concepto and efectivo and datafono and otros:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO ventas (turno_cod, concepto, efectivo, datafono, otros) VALUES (%s, %s, %s, %s, %s)"
        data_ventas = (turno, concepto, efectivo, datafono, otros)
        cursor.execute(sql, data_ventas)
        db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA AGREGAR GASTO
@app.route('/add_gastos', methods=['POST'])
def add_gastos():
    turno = request.form['Turno']
    responsable = request.form['Responsable']
    beneficiario = request.form['Beneficiario']
    concepto = request.form['Concepto']
    valor = request.form['Valor']
    if turno and responsable and beneficiario and concepto and valor:
        cursor = db.mydb.cursor()
        sql = "INSERT INTO gastos (turno_cod, responsable, beneficiario, concepto, valor_pagado) VALUES (%s, %s, %s, %s, %s)"
        data_gastos = (turno, responsable, beneficiario, concepto, valor)
        cursor.execute(sql, data_gastos)
        db.mydb.commit()
    return redirect(url_for('home'))

#RUTA PARA BUSQUEDA DE GASTOS 
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

#RUTA PARA BUSQUEDA DE VENTAS 
@app.route('/search_ventas', methods=['GET'])
def search_ventas():
    turno_venta = request.args.get('Turno')
    cur = db.mydb.cursor()
    query = "SELECT * FROM ventas WHERE turno_cod = %s"
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

# RUTA PARA EDITAR GASTOS
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

@app.route('/guardar-foto', methods=['GET', 'POST'])
def registarArchivo():
        if request.method == 'POST':
            if(request.files['archivo']):
                #Script para archivo
                file     = request.files['archivo']
                basepath = path.dirname (__file__) #La ruta donde se encuentra el archivo actual
                filename = secure_filename(file.filename) #Nombre original del archivo
                
                #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
                extension           = path.splitext(filename)[1]
                nuevoNombreFile     = stringAleatorio() + extension
                 
                upload_path = path.join (basepath, 'static/archivos', nuevoNombreFile) 
                file.save(upload_path)
        return render_template('index.html', list_Photos = listaArchivos())

@app.route('/<string:nombreFoto>', methods=['GET','POST'])
def EliminarFoto(nombreFoto=''):
    if request.method == 'GET':
        #print(nombreFoto) #Nombre del archivo subido
        basepath = path.dirname (__file__) #C:\xampp\htdocs\elmininar-archivos-con-Python-y-Flask\app
        url_File = path.join (basepath, 'static/archivos', nombreFoto)
        #print(url_File)
        
        #verifcando si existe el archivo, con la funcion (path.exists) antes de de llamar remove 
        # para eliminarlo, con el fin de evitar un error si no existe.
        if path.exists(url_File):
            remove(url_File) #Borrar foto desde la carpeta
            #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    return render_template('index.html', list_Photos = listaArchivos())
        
    
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'


#Creando mi decorador para el home, el cual retornara la Lista de Gastos
@app.route('/evidencia', methods=['GET','POST'])
def inicio():
    return render_template('layout2.html', miData = listaGastos())


#RUTAS
@app.route('/registrar-Gasto', methods=['GET','POST'])
def addGasto():
    return render_template('acciones/add.html')


 
#Registrando nuevo gasto
@app.route('/gasto', methods=['POST'])
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

       
  
  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    


# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
