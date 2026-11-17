AYUDA = """Taxímetro digital
i iniciar carrera (empieza PARADO)
p el taxi está parado
m el taxi está en movimiento
f finalizar la carrera y ver el total
a ver esta ayuda 
s salir"""
print (AYUDA)

def main():
    print(AYUDA)

    while True:
        orden = input("> ").strip().lower()

        if orden == "a":
            print(AYUDA)
        elif orden == "s":
            print("Hasta luego.")
            break
        else: 
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")

if __name__ == "__main__":
    main()
