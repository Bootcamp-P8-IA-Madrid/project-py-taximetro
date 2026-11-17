#Constantes 
#Paso 3 

TARIFA_PARADO = 0.02
TARIFA_MOVIMIENTO = 0.05

#Paso 1 - Ayuda

AYUDA = """Taxímetro digital
i iniciar carrera (empieza PARADO)
p el taxi está parado
m el taxi está en movimiento
f finalizar la carrera y ver el total
a ver esta ayuda 
s salir"""

#Función auxiliar de tarifas
#Paso 3 Las tarifas

def tarifa(estado):
    if estado == "parado":
        return TARIFA_PARADO
    elif estado == "movimiento":
        return TARIFA_MOVIMIENTO

#Paso 2 - Bucle de órdenes
# Función principal 

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

#Arranque
if __name__ == "__main__":
    main()