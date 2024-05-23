from flask import Flask, render_template # Render Template es para redireccionar las rutas a los template HTML
import os
import src.database as db
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

# Routes to Render Something
@app.route('/')
def home():
    cursor = db.mydb.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir a Diccionario
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for recrod in myresult:
        insertObject.append(dict(zip(columnName, recrod)))
    cursor.close()
    return render_template("index.html", data=insertObject)

@app.route('/enlaces', strict_slashes=False)
def enlaces():
    return render_template("enlaces.html")

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
