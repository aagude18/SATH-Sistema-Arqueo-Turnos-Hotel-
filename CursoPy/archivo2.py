#1. Crea una clase `Animal` con los atributos `nombre` y `edad`, y un método `hacer_sonido`.
#Clase Animal
class Animal():
    #Constructor
    def __init__ (self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    #Metodo
    def hacer_sonido (self):
        pass
#2. Crea una subclase `Perro` que hereda de `Animal`, añade el atributo `raza`, y sobreescribe el método `hacer_sonido`.
#SubClase Perro
class Perro(Animal):
    def __init__ (self, nombre, edad, raza):
        super().__init__(nombre, edad)
        self.raza = raza 
    
    def hacer_sonido(self): 
        return  "GUAUU!!"
#3.Crea una subclase `Gato` que hereda de `Animal`, añade el atributo `color`, y sobreescribe el método `hacer_sonido`.
#SubClase Gato
class Gato(Animal):
    def __init__ (self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color 
    
    def hacer_sonido(self): 
        return  "MIAUU!!"
#4. Crea instancias de `Perro` y `Gato` y haz que emitan sus sonidos.
# Creando Instancias
mi_perro = Perro("Tango", 7, "Buldog")
mi_gato = Gato("Tom", 2, "Gris")
#5. Crea una función `presentar_animal` que reciba un `Animal` y muestre su nombre, edad, y haga que el animal emita su sonido. 
# Utilízala con instancias de `Perro` y `Gato`. Observa cómo se aplica el polimorfismo.
# Definiendo Función para presentar animal
def presentar_animal(Animal):
    print("Nombre:", Animal.nombre)
    print("Edad:", Animal.edad)
    print("Sonido:", Animal.hacer_sonido())

# Función principal
def main():
    animal = input("¿Es su animal un gato o un perro?: ").capitalize()
    if animal == "Perro":
        presentar_animal(mi_perro)
        print("Raza: ", mi_perro.raza)
    elif animal == "Gato":
        presentar_animal(mi_gato)
        print("Color: ", mi_gato.color)
    else:
        print("La información suministrada no es la correcta")

if __name__=="__main__":
    main()