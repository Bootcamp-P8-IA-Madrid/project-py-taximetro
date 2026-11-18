import time

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

#Paso 5 - Cerrar tramo

def cerrar_tramo(carrera):
    ahora = time.monotonic()
    segundos = ahora - carrera["desde"]
    precio_segundo = tarifa(carrera["estado"])
    coste_tramo = segundos * precio_segundo

    carrera["importe"] += coste_tramo
    carrera["desde"] = ahora


#Paso 2 - Bucle de órdenes
# Función principal 

def main():
    print(AYUDA)
    carrera = None 

    while True:
        orden = input("> ").strip().lower()

        if orden == "i":
            if carrera is not None:
                print("Ya hay una carrera en curso. Finalízala con 'f'.")
                continue 

            carrera = {
                "estado": "parado",
                "desde": time.monotonic(),
                "importe": 0.0
            }
            print("carrera iniciada.")

        elif orden == "p":
            if carrera is None:
                print("Primero inicia una carrera con 'i'.")
                continue

            if carrera["estado"] == "parado":
                print("El taxi ya está en estado 'parado'.")
                continue 

            cerrar_tramo(carrera)
            carrera["estado"] = "parado"
            print(f"Taxi en {carrera['estado'].upper()}. Llevas {carrera['importe']: .2f} €.")

        elif orden == "m":
            if carrera is None:
                print("Primero inicia una carrera con 'i'.")
                continue

            if carrera["estado"] == "movimiento":
                print("El taxi ya está en estado 'movimiento'.")
                continue

            cerrar_tramo(carrera)
            carrera["estado"] = "movimiento"
            print(f"Taxi en {carrera['estado'].upper()}. Llevas {carrera['importe']:.2f} €.")

        elif orden =="f":
            if carrera is None:
                print("No hay ninguna carrera en curso.")
                continue

            cerrar_tramo(carrera)
            print(f"Carrera finalizada. Total a pagar: {carrera['importe']:.2f} €.")
            carrera = None

        elif orden == "a":
            print(AYUDA)

        elif orden == "s":
            if carrera is not None:
                print("Hay una carrera en curso. Finalízala con 'f' antes de salir.")
                continue

            print("Hasta luego.")
            break
        else: 
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")


#Arranque
if __name__ == "__main__":
    main()