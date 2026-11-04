# Repaso de Python para la fase 1

Lo que usa la fase 1 del taxímetro, en diez apartados. Cada uno recuerda una idea y propone un mini reto
para resolver con tu propio código. Si algo no te suena, vuelve a tus apuntes.

---

## Cómo trabajar

En GitHub haz **fork** de este repositorio, clónalo (`git clone <url de tu fork>`) y abre en VS Code la
carpeta que se crea. Dentro, crea una carpeta `ejercicios` para los retos, separados del código del
taxímetro. Abre la terminal («Terminal → Nueva terminal») y entra en ella con `cd ejercicios`.

Cada reto es un fichero `.py` nuevo que ejecutas con `python nombre.py` (o `python3 nombre.py` si el primero
no se reconoce). La carpeta `ejercicios/` también se sube a tu fork; el ejemplo está en la guía 01.

---

## 1. Ejecutar un fichero .py

El taxímetro vivirá en `taximetro.py` y se arrancará con `python taximetro.py`. Si sale `can't open file`,
la terminal no está en la carpeta del fichero: compruébalo con `pwd`.

**Reto:** crea `hola.py`, que escriba tu nombre, y ejecútalo.

## 2. print e input

`input("> ")` enseña `> `, espera a que escribas y pulses Intro, y devuelve lo escrito. Así leerá el
taxímetro las órdenes del conductor.

**Reto:** un programa que te pregunte tu nombre y te salude usándolo.

## 3. Variables y tipos

En la fase 1 usarás `str` (texto: `"parado"`) y `float` (decimales con punto: `0.02`). `input()` siempre
devuelve texto: `"3"` no es `3`. Los valores que no cambian van en MAYÚSCULAS: `PRECIO_CAFE = 1.20`.

**Reto:** pide el precio de un café, conviértelo con `float()` y muestra lo que cuestan tres. Usa `type()`
para ver el tipo antes y después de convertir. Si con 1.20 sale 3.5999…, el apartado 4 lo arregla.

## 4. f-strings y `:.2f`

Una f-string mete variables entre llaves: `f"Hola, {nombre}"`. Los decimales se guardan de forma
aproximada, así que el dinero se muestra con dos:

```py
print(f"Total: {importe:.2f} €")
```

**Reto:** calcula `0.1 + 0.2` y muéstralo sin formato y con `:.2f`. Con formato debe salir `0.30`, no
`0.30000000000000004`.

## 5. if / elif / else

`==` compara; `=` guarda. Cada condición acaba en `:` y su bloque lleva 4 espacios delante. Cada orden
del taxímetro será una rama de `if` / `elif` / `else`.

**Reto:** pide una letra: con `c` responde «Un café», con `t` «Un té» y con cualquier otra cosa «No lo
tenemos». Prueba con `C` mayúscula y arréglalo con `.lower()`.

## 6. while True, break y continue

`while True` repite sin fin; `break` sale del bucle; `continue` salta a la vuelta siguiente sin ejecutar lo
que queda debajo. El taxímetro pedirá órdenes así hasta la `s`. Si un programa no para, pulsa Ctrl+C.

**Reto:** pide palabras sin parar y repite cada una. Con `fin` se despide y termina. Una línea vacía no se
repite: vuelve a preguntar directamente.

## 7. Funciones con parámetros y return

`def` crea una función; recibe datos (parámetros) y `return` devuelve el resultado. En el taxímetro, una
función calculará las tarifas sin imprimir nada. Si al usarla sale `None`, falta el `return`.

**Reto:** escribe `precio_entrada(edad)`, que devuelve 4.0 para menores de 12 años y 7.5 para el resto.
Pruébala con dos edades.

## 8. Diccionarios

Un diccionario agrupa datos con etiquetas (claves). Se lee y se cambia con corchetes, y `+=` suma a lo que
había:

```py
pedido = {"plato": "tortilla", "precio": 6.0}
pedido["precio"] += 1.5
```

Una clave que no existe da `KeyError`. La carrera en curso será un diccionario.

**Reto:** crea un diccionario para un libro con título y páginas. Cambia el título, suma 50 páginas e
imprime el diccionario entero.

## 9. None

`None` significa «todavía no hay nada». En un `if` cuenta como falso: `if not pedido:` pregunta «¿no hay
pedido?». En el taxímetro, `carrera` valdrá `None` cuando no haya carrera.

**Reto:** empieza con `pedido = None` y avisa de que no hay pedido. Después guarda en `pedido` un
diccionario con un plato y, con otro `if`, muestra ese plato.

## 10. import time y time.monotonic()

`time.monotonic()` es un cronómetro: el número suelto no significa nada; la resta de dos lecturas da los
segundos pasados. Así sabrá el taxímetro cuánto dura cada tramo.

```py
import time
antes = time.monotonic()
```

Sin paréntesis no da error, pero no obtienes un número.

**Reto:** mide cuánto tardas en escribir tu nombre en un `input` y muéstralo con dos decimales.

---

## Autocomprobación

1. ¿Qué diferencia hay entre `orden = "s"` y `orden == "s"`? (apartado 5)
2. ¿En qué se diferencian `continue` y `break`? (apartado 6)
3. Tu función devuelve `None`. ¿Qué le falta? (apartado 7)
4. ¿Cómo sumas 0.3 a la clave `"precio"` de un diccionario? (apartado 8)
5. `time.monotonic()` da `1523.8`. ¿Qué hora es? (apartado 10)

---

Cuando acabes, vuelve a la carpeta del proyecto con `cd ..` y sigue con `01-fase1-paso-a-paso.md`.
