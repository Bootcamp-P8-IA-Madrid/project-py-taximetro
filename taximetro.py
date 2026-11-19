import json
import logging
from pathlib import Path
import time

# Rutas seguras para que siempre encuentre los archivos
CARPETA = Path(__file__).parent
CONFIG = CARPETA / "config.json"
LOG = CARPETA / "taximetro.log"

# Tarifas de respaldo si el JSON falla o se borra
TARIFAS_POR_DEFECTO = {
    "tarifa_parado": 0.02,
    "tarifa_movimiento": 0.05,
}

#Logger con el nombre del enunciado
log = logging.getLogger("taximetro")


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

def tarifa(estado, tarifas):
    if estado == "parado":
        return tarifas["tarifa_parado"]
    elif estado == "movimiento":
        return tarifas["tarifa_movimiento"]
    return 0.0

#Paso 5 - Cerrar tramo

def cerrar_tramo(carrera, tarifas):
    ahora = time.monotonic()
    segundos = ahora - carrera["desde"]
    precio_segundo = tarifa(carrera["estado"], tarifas)
    coste_tramo = segundos * precio_segundo

    carrera["importe"] += coste_tramo
    carrera["desde"] = ahora

def configurar_log():
    logging.basicConfig(
        filename=LOG,
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s"
    )

def cargar_tarifas(ruta=CONFIG):
    try:
        contenido = ruta.read_text(encoding="utf-8")
        datos = json.loads(contenido)
        tarifas = {
            "tarifa_parado": float(datos["tarifa_parado"]),
            "tarifa_movimiento": float(datos["tarifa_movimiento"]),
        }
        log.info("Tarifas cargadas de %s: %s", ruta, tarifas)
        return tarifas
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        log.warning("No se pudo leer %s (%s); uso tarifas por defecto", ruta, error)
        return dict(TARIFAS_POR_DEFECTO)  


#Paso 2 - Bucle de órdenes
# Función principal 

#configurar_log(): Aplica las reglas del archivo.

def main():
    configurar_log()
    log.info("Arranque del taxímetro")
    tarifas = cargar_tarifas()

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
            log.info("Carrera iniciada")
            print("carrera iniciada.")

        elif orden == "p":
            if carrera is None:
                print("Primero inicia una carrera con 'i'.")
                continue

            if carrera["estado"] == "parado":
                print("El taxi ya está en estado 'parado'.")
                continue 

            cerrar_tramo(carrera, tarifas)
            carrera["estado"] = "parado"
            log.info("Cambio de estado a %s (%.2f € acumulados)", "parado", carrera["importe"])
            print(f"Taxi en {carrera['estado'].upper()}. Llevas {carrera['importe']: .2f} €.")

        elif orden == "m":
            if carrera is None:
                print("Primero inicia una carrera con 'i'.")
                continue

            if carrera["estado"] == "movimiento":
                print("El taxi ya está en estado 'movimiento'.")
                continue

            cerrar_tramo(carrera, tarifas)
            carrera["estado"] = "movimiento"
            log.info("Cambio de estado a %s (%.2f € acumulados)", "movimiento", carrera["importe"])
            print(f"Taxi en {carrera['estado'].upper()}. Llevas {carrera['importe']:.2f} €.")

        elif orden =="f":
            if carrera is None:
                print("No hay ninguna carrera en curso.")
                continue

            cerrar_tramo(carrera, tarifas)
            log.info("carrera finalizada: %.2f €", carrera["importe"])
            print(f"Carrera finalizada. Total a pagar: {carrera['importe']:.2f} €.")
            carrera = None

        elif orden == "a":
            print(AYUDA)

        elif orden == "s":
            if carrera is not None:
                print("Hay una carrera en curso. Finalízala con 'f' antes de salir.")
                continue

            log.info("Cierre del taxímetro")
            print("Hasta luego.")
            break
        else: 
            log.warning("Orden desconocida: %r", orden)
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")


#Arranque
if __name__ == "__main__":
    main()