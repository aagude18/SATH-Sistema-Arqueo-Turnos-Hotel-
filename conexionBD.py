
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydbe = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="",
        database = "evidencias"
        )
    if mydbe:
        print ("Conexion exitosa a BD")
        return mydbe
    else:
        print("Error en la conexion a BD")
    

    
    
    