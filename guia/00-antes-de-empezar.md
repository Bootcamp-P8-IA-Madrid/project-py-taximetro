# Lo mínimo de Python que necesitas para la fase 1

Aquí está solo lo que usa la fase 1 del taxímetro. Cada apartado tiene una explicación corta, un
ejemplo y un ejercicio de 5 minutos con el resultado que debe salir. Hazlos en orden antes de empezar
`01-fase1-paso-a-paso.md`, y vuelve aquí cuando algo no te suene.

---

## Cómo trabajar

Empieza ya en tu proyecto: en GitHub haz **fork** de este repositorio, clónalo (`git clone <url de tu fork>`)
y abre en VS Code la carpeta que se crea. Dentro, crea una carpeta `ejercicios`: aquí van los ejercicios de
esta guía, separados del código del taxímetro. Abre la terminal («Terminal → Nueva terminal») y entra en
ella con `cd ejercicios`.

Cada ejercicio es un fichero `.py` nuevo: lo escribes, lo guardas (Ctrl+S) y lo ejecutas con
`python nombre.py`. Si te dice «command not found» o «no se reconoce», usa `python3 nombre.py`.

Al acabar, guárdalos en Git y súbelos a tu fork: la carpeta `ejercicios/` también se sube. En la guía 01
tienes el ejemplo de cómo hacerlo.

---

## 1. Ejecutar un fichero .py

Un programa en Python es un fichero de texto con extensión `.py`. Python lo lee de arriba abajo. El
taxímetro entero vivirá en `taximetro.py` y se arrancará con `python taximetro.py`.

### Ejercicio (5 min)

Crea `hola.py`:

```python
print("Taxímetro digital")
```

Ejecuta `python hola.py`.

**Resultado esperado**

```
Taxímetro digital
```

Si sale `can't open file` o `No such file or directory`, la terminal no está en la carpeta del fichero.
Escribe `pwd` para ver dónde estás (también en PowerShell).

---

## 2. print e input

`print(...)` escribe en pantalla lo que le pongas entre paréntesis. `input(...)` muestra ese texto como
pregunta, espera a que el usuario escriba algo y pulse Intro, y devuelve lo escrito. En el taxímetro el
conductor verá `> ` y escribirá una letra: eso es `input("> ")`.

### Ejercicio (5 min)

Crea `pregunta.py`:

```python
print("Taxímetro digital")
orden = input("> ")
print("Has escrito:", orden)
```

Ejecútalo, escribe `i` y pulsa Intro.

**Resultado esperado**

```
Taxímetro digital
> i
Has escrito: i
```

`print` con dos cosas separadas por coma las escribe con un espacio en medio.

---

## 3. Variables y tipos (str, float)

Una variable es un nombre que guarda un valor; se crea con `=`. En la fase 1 usarás dos tipos: `str`
(texto, entre comillas: `"parado"`, `"i"`) y `float` (número con decimales, con punto: `0.02`, `12.5`).
`"3"` y `3` no son lo mismo: el primero es texto y con texto no se calcula dinero. `input()` siempre
devuelve texto.

```py
estado = "parado"
TARIFA_PARADO = 0.02     # en MAYÚSCULAS: es una constante, un valor que no cambia
```

### Ejercicio (5 min)

Crea `tipos.py`:

```python
estado = "parado"
tarifa = 0.02
segundos = 10

print(estado)
print(tarifa * segundos)
print(type(estado))
print(type(tarifa))
```

**Resultado esperado**

```
parado
0.2
<class 'str'>
<class 'float'>
```

`type(x)` te dice de qué tipo es un valor.

---

## 4. f-strings y `:.2f`

Una f-string mezcla texto y variables: una `f` delante de las comillas y las variables entre llaves
`{}`. Con dinero hay un problema: `0.1 + 0.2` da `0.30000000000000004`, porque los decimales se guardan
de forma aproximada. Para enseñar dos decimales se añade `:.2f` dentro de las llaves. El requisito
«importe en euros con dos decimales» es `f"Total a cobrar: {importe:.2f} €"`.

```py
nombre = "Ana"
print(f"Hola, {nombre}")          # Hola, Ana

total = 0.1 + 0.2
print(f"Total: {total:.2f} €")    # Total: 0.30 €
```

### Ejercicio (5 min)

Crea `formato.py`:

```python
importe = 10 * 0.02 + 10 * 0.05 + 5 * 0.02

print(importe)
print(f"Total a cobrar: {importe:.2f} €")
print(f"Total a cobrar: {importe} €")
```

**Resultado esperado**

```
0.7999999999999999
Total a cobrar: 0.80 €
Total a cobrar: 0.7999999999999999 €
```

Si ves llaves en pantalla (`Total: {importe:.2f}`), te falta la `f` delante de las comillas.

---

## 5. if / elif / else

Hacen una cosa u otra según una condición. `==` compara; un solo `=` guarda en una variable. Cada
condición acaba en dos puntos `:` y lo que va dentro lleva 4 espacios delante (indentación): así sabe
Python qué líneas pertenecen a cada rama. El bucle principal del taxímetro es una cadena de
`if orden == "i"` / `elif orden == "p"` / ... / `else`.

```py
orden = "i"

if orden == "i":
    print("Iniciar")
elif orden == "s":
    print("Salir")
else:
    print("No conozco esa orden")
```

### Ejercicio (5 min)

Crea `decidir.py`:

```python
orden = input("> ")

if orden == "i":
    print("Carrera iniciada.")
elif orden == "f":
    print("Carrera finalizada.")
else:
    print("Orden desconocida. Escribe 'a' para ver la ayuda.")
```

Ejecútalo tres veces, escribiendo `i`, `f` y `x`.

**Resultado esperado**

```
> i
Carrera iniciada.
```
```
> f
Carrera finalizada.
```
```
> x
Orden desconocida. Escribe 'a' para ver la ayuda.
```

Con `I` mayúscula dirá «Orden desconocida»: `"I"` y `"i"` son textos distintos. En el taxímetro lo
resolverás con `.lower()`, que pasa el texto a minúsculas.

---

## 6. while True, break y continue

`while True:` repite el bloque para siempre, hasta que dentro aparece un `break`, que lo corta.
`continue` no sale del bucle: salta al principio de la siguiente vuelta sin ejecutar lo que queda debajo.
El taxímetro es un `while True` que lee órdenes sin parar; solo la orden `s` hace `break`. Si tu
programa se queda en bucle y no sale, pulsa Ctrl+C.

```py
while True:
    orden = input("> ")
    if orden == "s":
        break            # sale del bucle
    print("Sigo aquí")
print("Fin")
```

### Ejercicio (5 min)

Crea `bucle.py`:

```python
while True:
    orden = input("> ")
    if orden == "s":
        print("Hasta luego.")
        break
    if orden == "":
        continue
    print("Has escrito:", orden)
```

Ejecútalo y escribe, por este orden: `i`, Intro sin nada, `p`, `s`.

**Resultado esperado**

```
> i
Has escrito: i
> 
> p
Has escrito: p
> s
Hasta luego.
```

Con la línea vacía no dice «Has escrito»: el `continue` ha vuelto al principio.

---

## 7. Funciones con parámetros y return

Una función es un trozo de código con nombre que puedes usar las veces que quieras. Se define con
`def`, recibe datos (parámetros) y devuelve un resultado con `return`. Se llama escribiendo su nombre
con paréntesis y los datos dentro. En el taxímetro harás una función parecida para las tarifas.

```py
def doble(numero):          # «numero» es el parámetro
    return numero * 2       # lo que devuelve

print(doble(4))             # 8
resultado = doble(10)       # también se puede guardar
```

### Ejercicio (5 min)

Crea `funciones.py`:

```python
PRECIO_NINO = 4.0
PRECIO_ADULTO = 7.5

def precio(edad):
    if edad < 12:
        return PRECIO_NINO
    else:
        return PRECIO_ADULTO

def total(entradas, edad):
    return entradas * precio(edad)

print(precio(8))
print(precio(30))
print(total(4, 30))
```

**Resultado esperado**

```
4.0
7.5
30.0
```

`total` llama a `precio` por dentro. Si llamas a una función sin el dato que espera, Python avisa:
`TypeError: precio() missing 1 required positional argument: 'edad'`.

---

## 8. Diccionarios: crear, leer, modificar

Un diccionario guarda varios datos juntos, cada uno con su etiqueta (la clave). Se crea con llaves
`{}` y parejas `"clave": valor`; se lee y se modifica con corchetes `[]`. `+=` suma al valor que había.
Una clave que no existe da `KeyError`, y `"estado"` y `"Estado"` son claves distintas. La carrera en
curso del taxímetro será un diccionario con `estado`, `desde` (cuándo empezó el tramo actual) e
`importe` (lo acumulado).

```py
carrera = {"estado": "parado", "importe": 0.0}     # crear
print(carrera["estado"])                           # leer     → parado
carrera["estado"] = "movimiento"                   # modificar
carrera["importe"] += 0.5                          # sumar al valor que había
```

### Ejercicio (5 min)

Crea `ficha.py`:

```python
carrera = {"estado": "parado", "importe": 0.0}

print(carrera["estado"])
carrera["estado"] = "movimiento"
carrera["importe"] += 0.5
carrera["importe"] += 0.25
print(carrera["estado"])
print(carrera["importe"])
print(carrera)
```

**Resultado esperado**

```
parado
movimiento
0.75
{'estado': 'movimiento', 'importe': 0.75}
```

---

## 9. None

`None` significa «nada, todavía no hay». Se escribe con N mayúscula y sin comillas. En un `if` cuenta
como falso, así que `if not carrera:` pregunta «¿no hay carrera?». En el taxímetro, `carrera` vale
`None` cuando no hay carrera, pasa a ser un diccionario al iniciar y vuelve a `None` al finalizar.

```py
carrera = None          # no hay carrera

if not carrera:         # ¿no hay carrera?
    print("Primero inicia una carrera.")
if carrera:             # ¿hay carrera?
    print("Hay una carrera en curso.")
```

### Ejercicio (5 min)

Crea `nada.py`:

```python
carrera = None
print(carrera)

if not carrera:
    print("No hay carrera.")

carrera = {"estado": "parado", "importe": 0.0}

if carrera:
    print("Hay carrera.")

carrera = None
print(carrera is None)
```

**Resultado esperado**

```
None
No hay carrera.
Hay carrera.
True
```

Si lees una casilla de `None` como si fuera un diccionario, Python avisa:
`TypeError: 'NoneType' object is not subscriptable`.

---

## 10. import time y time.monotonic()

Los módulos son herramientas que ya trae Python; se cargan con `import` al principio del fichero.
`time.monotonic()` devuelve los segundos de un reloj que solo avanza. El número en sí no significa nada:
lo útil es restar dos lecturas para saber cuántos segundos han pasado. No se usa `time.time()` porque
la hora del ordenador puede cambiar en mitad de una carrera. `time.sleep(2)` espera 2 segundos; solo lo
usarás en pruebas.

En el taxímetro, al iniciar la carrera se apunta `time.monotonic()` en `carrera["desde"]`. Al cambiar
de estado se vuelve a leer, se restan y esos segundos se multiplican por la tarifa.

```py
import time

antes = time.monotonic()
# ... pasa el tiempo ...
despues = time.monotonic()
segundos = despues - antes
```

### Ejercicio (5 min)

Crea `reloj.py`:

```python
import time

antes = time.monotonic()
time.sleep(2)
despues = time.monotonic()

segundos = despues - antes
print(f"Han pasado {segundos:.2f} segundos")
print(f"A 0.02 €/s son {segundos * 0.02:.2f} €")
```

**Resultado esperado** (tarda 2 segundos en aparecer)

```
Han pasado 2.00 segundos
A 0.02 €/s son 0.04 €
```

Puede salir `2.00` o `2.01`. Si escribes `time.monotonic` sin paréntesis no da error, pero en vez del
número devuelve `<built-in function monotonic>`.

---

## ¿Estoy listo?

Piensa la respuesta antes de abrir cada una. Si fallas dos o más, repasa ese apartado y vuelve a hacer
su ejercicio.

<details>
<summary><strong>1.</strong> ¿Qué escribe en pantalla <code>print(f"Total: {0.5:.2f} €")</code>?</summary>

`Total: 0.50 €`. Las llaves con `:.2f` ponen dos decimales. Sin la `f` delante de las comillas saldría
`Total: {0.5:.2f} €` tal cual. (Apartado 4)
</details>

<details>
<summary><strong>2.</strong> ¿Cuál es la diferencia entre <code>orden = "s"</code> y <code>orden == "s"</code>?</summary>

El primero guarda el texto `"s"` en la variable `orden`. El segundo pregunta si `orden` vale `"s"` y
devuelve verdadero o falso; es el que va en un `if`. (Apartado 5)
</details>

<details>
<summary><strong>3.</strong> En un <code>while True</code>, ¿qué hace <code>break</code> y qué hace <code>continue</code>?</summary>

`break` sale del bucle del todo (el programa sigue después del bucle). `continue` salta a la siguiente
vuelta sin ejecutar lo que queda debajo. (Apartado 6)
</details>

<details>
<summary><strong>4.</strong> Si <code>carrera = {"estado": "parado", "importe": 0.0}</code>, ¿cómo pasas el estado a <code>"movimiento"</code> y cómo sumas 0.3 al importe?</summary>

`carrera["estado"] = "movimiento"` y `carrera["importe"] += 0.3`. Corchetes, clave entre comillas, y `+=`
para añadir a lo que había. (Apartado 8)
</details>

<details>
<summary><strong>5.</strong> ¿Qué devuelve <code>precio(30)</code> en el ejercicio del apartado 7, y qué pasa si llamas <code>precio()</code> sin nada?</summary>

Devuelve `7.5`. Sin nada, Python para con
`TypeError: precio() missing 1 required positional argument: 'edad'`: la función esperaba un dato y no se
lo has dado. (Apartado 7)
</details>

<details>
<summary><strong>6.</strong> Lees <code>time.monotonic()</code> y te da <code>1523.8</code>. ¿Qué hora es?</summary>

No se sabe, y no importa. `monotonic` no da la hora: es un cronómetro que solo avanza. Solo sirve para
restar dos lecturas y saber cuántos segundos han pasado entre ellas. (Apartado 10)
</details>

---

Con los ejercicios funcionando tienes todo lo que necesita la fase 1. Vuelve a la carpeta del proyecto con
`cd ..` y sigue con `01-fase1-paso-a-paso.md`.
