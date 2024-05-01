from flask import Flask, render_template # Render Template es para redireccionar las rutas a los template HTML

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
    return render_template("home.html")

@app.route('/enlaces', strict_slashes=False)
def enlaces():
    return render_template("enlaces.html")

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
