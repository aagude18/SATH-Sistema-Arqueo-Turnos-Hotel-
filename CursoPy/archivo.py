def main():
    menu = {
        "BAJA TACO": 4.00,
        "BURRITO": 7.50,
        "BOWL": 8.50,
        "NACHOS": 11.00,
        "QUESADILLA": 8.50,
        "SUPER QUESADILLA": 9.50,
        "TACO": 3.00,
        "TORTILLA SALAD": 8.00
    }
    order_total = 0.0
    while True:
        try:
            item = input("Ingrese un artículo de su pedido: ")
        except EOFError:
            break
        item = item.upper()
        if item in menu:
            order_total += menu[item] 
            print(f"${menu[item]:.2f}")
        elif item == "SALIR":
            print(f"El total de su pedido es: ${order_total:.2f}")
            break
        else:
            print("Artículo Inválido")
if __name__=="__main__":
    main()