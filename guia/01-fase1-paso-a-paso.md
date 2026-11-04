# Fase 1 del taxímetro, paso a paso

La fase 1 del enunciado (US-01 a US-04) en nueve pasos. Si te falta base, haz antes `00-antes-de-empezar.md`.
Lo que se corrige en cada fase está en la checklist de `04-si-ya-sabes.md`; si ya programas, empieza por ahí.

Orientativo: pasos 1 a 4 el primer día, 5 a 7 el segundo, 8 y 9 el tercero. Entrega hacia el 10/11.

## Tu repositorio

1. Si hiciste la guía 00, ya tienes tu fork clonado y abierto en VS Code: sigue en el punto 2. Si no, en
   GitHub haz **fork** de este repositorio, clónalo (`git clone <url de tu fork>`) y abre en VS Code la
   carpeta que se crea. Esa es la carpeta del proyecto: todo lo que hagas va ahí, junto al `README.md` del
   enunciado. La terminal tiene que estar en ella (`pwd`).
2. Crea en ella un fichero `.gitignore` con estas dos líneas. Git no subirá lo que coincida con ellas: la
   carpeta que Python crea al importar y tus ficheros de prueba.

   ```
   __pycache__/
   prueba_*.py
   ```
3. Abre `taximetro.py`: es el único fichero de código de la fase 1. Sustituye su contenido de ejemplo por
   tu código.

## Cómo funciona cada paso

- Cada paso dice qué debe hacer el programa al acabar, los nombres que tienes que usar y unas pistas.
  El código lo escribes tú.
- **Pruébalo**: ejecuta `python taximetro.py`, escribe las órdenes que se indican y compara con la salida.
  Cuando hay esperas, los importes dependen de lo que tardes en escribir.
- **Si falla**: los errores más habituales de ese paso y su causa.
- Al acabar cada paso, sube tus cambios a tu fork:

  ```
  git add .
  git commit -m "type: your descriptive message"
  git push
  ```

  El mensaje lo escribes tú, en inglés y en formato Conventional Commits (`feat:`, `fix:`, `docs:`...), y
  describe lo que has hecho en ese paso.

## La idea: calcular por tramos

El conductor escribe una letra y pulsa Intro: `i` inicia, `p` parado, `m` en movimiento, `f` finaliza y
muestra el total, `a` ayuda, `s` sale. Tarifas: 0,02 €/s parado y 0,05 €/s en movimiento.

Una carrera es una sucesión de **tramos**. El importe es la suma de `segundos × tarifa` de cada tramo:

```
inicio        cambio a marcha         cambio a parado        fin
  |---- parado 10 s ----|---- marcha 10 s ----|-- parado 5 s --|
        10 × 0.02 = 0.20      10 × 0.05 = 0.50     5 × 0.02 = 0.10   → 0.80 €
```

Basta con guardar **el estado**, **cuándo empezó el tramo** y **lo acumulado**. Al pulsar `p`, `m` o `f` se
«cierra el tramo»: se suma lo que vale y se apunta el nuevo instante.

---

## Paso 1 · Mostrar la ayuda

**Al acabar:** `python taximetro.py` muestra la ayuda con las seis órdenes y termina.

**Nombre:** la constante `AYUDA`, con el texto de la ayuda. Mantén las seis letras: el resto de la guía las usa.

**Pistas:**
- El texto exacto está en «Pruébalo»: cópialo de ahí.
- Un texto de varias líneas se escribe entre tres comillas `"""`. Los saltos de línea de dentro se respetan,
  también el que va justo después de abrir y el de antes de cerrar:

  ```py
  MENU = """
  Lunes: lentejas
  Martes: paella
  """
  ```
- Primero guardas el texto en la constante y después lo imprimes.

**Pruébalo:**

```

Taxímetro digital
  i  iniciar carrera (empieza PARADO)
  p  el taxi está parado
  m  el taxi está en movimiento
  f  finalizar la carrera y ver el total
  a  ver esta ayuda
  s  salir

```

**Si falla:**
- `NameError: name 'AYUDA' is not defined` → el nombre del `print` no coincide, o el `print` está antes de
  la definición.
- `SyntaxError: unterminated triple-quoted string literal` → faltan las tres comillas de cierre.
- `can't open file ... No such file or directory` → la terminal no está en la carpeta del fichero (`pwd`).

---

## Paso 2 · Un bucle de órdenes

**Al acabar:** el programa muestra la ayuda y pide órdenes sin parar. `a` vuelve a mostrar la ayuda, `s` se
despide y termina, y cualquier otra cosa da un aviso. `S` o ` s` (con espacio) valen igual que `s`.

**Nombre:** la función `main()`, que hace todo el trabajo. `AYUDA` se queda arriba, fuera de la función.

Esta es la forma que tendrá el fichero hasta el final. Las dos últimas líneas significan «si ejecutas este
fichero, arranca `main()`». Cópialas tal cual; en el paso 3 verás para qué sirven.

```py
AYUDA = """..."""

def main():
    ...

if __name__ == "__main__":
    main()
```

**Pistas:**
- El bucle que lee órdenes lo practicaste en el apartado 6 de la guía 00. El `> ` es el texto del `input`.
- Para cada orden, una rama de `if` / `elif`; lo que no reconoces, al `else`.
- Ahora la ayuda la imprime `main()` al empezar: quita el `print` suelto del paso 1.
- Para limpiar lo que escribe el conductor, los textos tienen `.strip()` (quita espacios de los lados) y
  `.lower()` (pasa a minúsculas). Se pueden encadenar:

  ```py
  print("  Hola ".strip().lower())    # hola
  ```

**Pruébalo** con `x`, `a`, `S`:

```
> x
Orden desconocida. Escribe 'a' para ver la ayuda.
> a
(la ayuda otra vez)
> S
Hasta luego.
```

**Si falla:**
- `SyntaxError: expected ':'` → faltan los dos puntos al final del `while`, `if`, `elif`, `else` o `def`.
- `IndentationError: expected an indented block` → la línea de debajo no tiene 4 espacios más.
- `s` no sale → falta el `break` o el `.lower()`. Sal con **Ctrl+C**.
- No sale nada → faltan las dos líneas finales.
- La ayuda sale dos veces al arrancar → sigue ahí el `print(AYUDA)` suelto del paso 1.

---

## Paso 3 · Las tarifas

**Al acabar:** hay una función que, dado un estado, devuelve lo que cuesta cada segundo en ese estado.

**Nombres:** las constantes `TARIFA_PARADO` (0.02 €/s) y `TARIFA_MOVIMIENTO` (0.05 €/s), y la función
`tarifa(estado)`, donde `estado` es `"parado"` o `"movimiento"`.

**Pistas:**
- Constantes arriba, encima de `AYUDA` (solo los `import` van antes). Funciones auxiliares entre `AYUDA` y `main`.
- La función no imprime nada: devuelve un valor. Repasa el apartado 7 de la guía 00.
- Usa las constantes dentro de la función, no los números: si un día cambia la tarifa, se cambia en un sitio.

**Pruébalo** con un fichero aparte, `prueba_tarifa.py`, en la misma carpeta:

```python
from taximetro import tarifa

print(tarifa("parado"))
print(tarifa("movimiento"))
```

`python prueba_tarifa.py` debe dar:

```
0.02
0.05
```

No arranca el taxímetro: el `if __name__ == "__main__":` impide que `main()` se ejecute al importar.

**Si falla:**
- `NameError: name 'movimiento' is not defined` → faltan las comillas en `"movimiento"`.
- `ModuleNotFoundError: No module named 'taximetro'` → la prueba no está en la misma carpeta.
- Sale `None` → a la función le falta el `return`.
- Aparece la ayuda y pide `> ` → `main()` está suelto al final, sin el `if __name__`.

---

## Paso 4 · Iniciar una carrera

**Al acabar:** con `i` empieza una carrera, parada y con importe cero. De momento se imprime la carrera
para comprobarla.

**Nombres:** la variable `carrera`. Sin carrera vale `None`. Con carrera es un diccionario con tres claves:
`"estado"` (`"parado"` o `"movimiento"`), `"desde"` (el instante en que empezó el tramo actual, leído con
`time.monotonic()`) e `"importe"` (lo acumulado, un `float`).

**Pistas:**
- `carrera` se crea dentro de `main()`, antes del bucle: al arrancar no hay carrera.
- Para usar `time.monotonic()` hace falta `import time` en la primera línea del fichero (apartado 10 de la 00).
- La rama de `i` crea el diccionario, avisa e imprime `carrera` (ese último `print` es temporal: lo quitas
  en el paso 5).
- Las ramas siguen siendo una sola cadena: un `if` al principio y `elif` en el resto.

**Pruébalo** con `i`, `s`:

```
> i
Carrera iniciada. El taxi está PARADO.
{'estado': 'parado', 'desde': 2839.054257017, 'importe': 0.0}
> s
Hasta luego.
```

El número de `desde` será otro.

**Si falla:**
- `NameError: name 'time' is not defined` → falta `import time`.
- `SyntaxError: invalid syntax` en el diccionario → falta una coma entre parejas.
- `SyntaxError: cannot assign to literal here...` → has puesto `=` donde van los dos puntos `"clave": valor`.
- `'desde': <built-in function monotonic>` → `time.monotonic` sin paréntesis.

---

## Paso 5 · `cerrar_tramo`

**Al acabar:** una función cobra el tramo que termina ahora: suma su valor al importe y deja apuntado que el
tramo siguiente empieza en este instante.

**Nombre:** `cerrar_tramo(carrera)`. Recibe el diccionario y lo cambia; no devuelve nada.

Primero con números. El tramo empezó en `100.0`, el estado es `"parado"`, el importe es `0.30` y ahora el
reloj marca `110.0`:

| Pregunta | Cálculo | Resultado |
|---|---|---|
| Segundos del tramo | 110.0 − 100.0 | 10.0 |
| Tarifa | `tarifa("parado")` | 0.02 |
| Valor del tramo | 10.0 × 0.02 | 0.20 |
| Nuevo importe | 0.30 + 0.20 | 0.50 |
| Nuevo `desde` | ahora | 110.0 |

**Pistas:**
- Cada fila sale de algo que ya está en el diccionario o en tu función `tarifa`. ¿De dónde sale cada número?
- «Ahora» es una lectura de `time.monotonic()`. Léelo una sola vez y úsalo para la resta y para el nuevo
  `desde`: si lo lees dos veces, se pierde el trocito de tiempo que pasa entre una lectura y otra.
- Ponla entre `tarifa` y `main`, y quita el `print(carrera)` del paso 4.

**Pruébalo** con `prueba_tramo.py`:

```python
import time
from taximetro import cerrar_tramo

carrera = {"estado": "parado", "desde": time.monotonic(), "importe": 0.0}
time.sleep(2)              # esperamos 2 segundos de verdad
cerrar_tramo(carrera)
print(f"{carrera['importe']:.2f}")   # 2 s × 0.02 = 0.04

carrera["estado"] = "movimiento"
time.sleep(2)
cerrar_tramo(carrera)
print(f"{carrera['importe']:.2f}")   # 0.04 + 2 s × 0.05 = 0.14
```

Tarda 4 segundos y debe dar `0.04` y `0.14`.

**Si falla:**
- `0.04` y `0.24` → no actualizas `"desde"`: el segundo tramo cuenta desde el principio.
- `0.04` y `0.10` → has puesto `=` en vez de `+=`: el importe se pisa en vez de acumularse.
- `TypeError: unsupported operand type(s) for -: 'builtin_function_or_method' and 'float'` (o al revés) →
  `time.monotonic` sin paréntesis, aquí o en el paso 4.
- `KeyError: 'Desde'` → las claves van en minúsculas: `"estado"`, `"desde"`, `"importe"`.

---

## Paso 6 · Cambiar entre parado y movimiento

**Al acabar:** con una carrera en curso, `p` y `m` cambian el estado y muestran lo que se lleva cobrado.

**Pistas:**
- Piensa en el orden. El tramo que termina, ¿con qué tarifa se cobra: la del estado de antes o la del nuevo?
  Eso te dice si `cerrar_tramo` va antes o después de cambiar `"estado"`.
- Puedes hacer una rama para cada letra o una para las dos. Para la segunda opción, `in` pregunta si un valor
  es uno de varios:

  ```py
  color = "verde"
  print(color in ("rojo", "verde"))    # True
  print(color in ("azul", "negro"))    # False
  ```
- El estado sale en mayúsculas en el mensaje: `"parado".upper()` da `"PARADO"`.
- Dentro de una f-string, escribe la clave de un diccionario con comillas simples. Con dobles, las versiones
  de Python anteriores a la 3.12 creen que se cierra la cadena: `f"Hola, {persona['nombre']}"`.

**Pruébalo** con `i`, espera 2 s, `m`, espera 2 s, `p`, `s`:

```
> i
Carrera iniciada. El taxi está PARADO.
> m
Estado: MOVIMIENTO. Llevas 0.04 €.
> p
Estado: PARADO. Llevas 0.14 €.
> s
Hasta luego.
```

Si escribes `p` sin carrera, el programa cae: se arregla en el paso 8.

**Si falla:**
- `Estado: <built-in method upper ...>` → `upper` sin paréntesis.
- Siempre `Llevas 0.00 €` → no llamas a `cerrar_tramo` antes del `print`.
- El importe sube de más → has cambiado el estado antes de cerrar el tramo.

---

## Paso 7 · Finalizar y mostrar el total

**Al acabar:** `f` cobra el último tramo, muestra el total con dos decimales y deja el taxímetro listo para
otra carrera sin cerrar el programa (US-04).

**Pistas:**
- El último tramo también hay que cobrarlo, igual que en el paso 6.
- Después de cobrar, ¿qué tiene que valer `carrera` para que `i` pueda empezar otra? Mira cómo empieza `main()`.
- El bucle no se corta: aquí no hay `break`.

**Pruébalo** con `i`, 2 s, `m`, 2 s, `f`, `i`, 2 s, `f`, `s`:

```
> i
Carrera iniciada. El taxi está PARADO.
> m
Estado: MOVIMIENTO. Llevas 0.04 €.
> f
Carrera finalizada. Total a cobrar: 0.14 €
> i
Carrera iniciada. El taxi está PARADO.
> f
Carrera finalizada. Total a cobrar: 0.04 €
> s
Hasta luego.
```

**Si falla:**
- `TypeError: 'NoneType' object is not subscriptable` → vacías `carrera` antes de imprimir el total; tiene que
  ser lo último de la rama.

---

## Paso 8 · Casos raros

**Al acabar:** el programa nunca cae. En estos cinco casos avisa, no cambia nada y vuelve a pedir orden:

| Si el conductor... | Mensaje |
|---|---|
| pulsa `i` con una carrera en curso | Ya hay una carrera en curso. Finalízala con 'f'. |
| pulsa `p` o `m` sin carrera | Primero inicia una carrera con 'i'. |
| pulsa `p` estando parado (o `m` en movimiento) | El taxi ya está en estado 'parado'. |
| pulsa `f` sin carrera | No hay ninguna carrera en curso. |
| pulsa `s` con carrera en curso | Hay una carrera en curso. Finalízala con 'f' antes de salir. |

**Pistas:**
- Los cinco se resuelven igual: al principio de la rama, comprobar, avisar y `continue` (vuelve al `input`;
  apartado 6 de la 00).
- «¿Hay carrera?» y «¿no hay carrera?» se preguntan con `None`, como en el apartado 9 de la 00.
- Para el tercer caso, compara el estado que pide la letra con el de la carrera. ¿Antes o después de cerrar
  el tramo?
- En el tercer caso el mensaje dice el estado (`'parado'` o `'movimiento'`), no la letra.

**Pruébalo** con `i`, `i`, `p`, `s`, espera 1 s, `m`, `f`, `f`, `m`, `s`:

```
> i
Carrera iniciada. El taxi está PARADO.
> i
Ya hay una carrera en curso. Finalízala con 'f'.
> p
El taxi ya está en estado 'parado'.
> s
Hay una carrera en curso. Finalízala con 'f' antes de salir.
> m
Estado: MOVIMIENTO. Llevas 0.02 €.
> f
Carrera finalizada. Total a cobrar: 0.02 €
> f
No hay ninguna carrera en curso.
> m
Primero inicia una carrera con 'i'.
> s
Hasta luego.
```

**Si falla:**
- `SyntaxError: 'continue' not properly in loop` → el `continue` está fuera del `while`.
- `TypeError: 'NoneType' object is not subscriptable` al pulsar `p` sin carrera → miras `carrera["estado"]`
  antes de comprobar si hay carrera.
- `i` dos veces sigue creando carrera → la comprobación va **antes** de crear el diccionario.
- El segundo `f` vuelve a cobrar en vez de avisar → no vacías `carrera` en la rama de `f` (paso 7).
- El aviso de mismo estado sale siempre → comparas después de cambiar el estado. Si no sale nunca, comparas
  la letra (`"p"`) con el estado (`"parado"`).

---

## Paso 9 · README y tablero

El `README.md` que trae tu fork es el enunciado. Guárdalo con otro nombre y escribe el tuyo:

```
git mv README.md ENUNCIADO.md
```

Tu `README.md` nuevo debe decir qué es, cómo se arranca, cómo se usa y qué decisiones técnicas tomaste.
Un esqueleto para empezar; lo que va entre paréntesis y los `...` los escribes tú:

```markdown
# Taxímetro digital

Prototipo de taxímetro por terminal para TaxiTech Solutions. Fase 1: MVP (US-01 a US-04).

## Cómo arrancarlo

Necesitas Python 3.10 o superior. En la carpeta del proyecto:

    python taximetro.py

## Cómo se usa

Al arrancar aparece la ayuda. Escribe una letra y pulsa Intro:

| Orden | Qué hace |
|---|---|
| i | iniciar carrera (empieza parado) |
| ... | ... |

(Las tarifas y cómo se calcula el importe por tramos, con tus palabras.)

## Decisiones

(Una línea por decisión y su porqué. Por ejemplo: ¿por qué un solo fichero? ¿Por qué
`time.monotonic()` y no `time.time()`?)
```

El tablero (se ve en clase el 10/11; créalo ya con lo que aquí se dice): un GitHub Project con columnas **Fase 1 · Fase 2 · Fase 3 · Fase 4 · Hecho**
y una tarjeta por historia (US-01 a US-09) en la columna de su fase. US-01 a US-04 deben acabar en «Hecho».
Si no ves la pestaña Projects: Settings → General → Features → Projects.

**Pruébalo:** en GitHub se ve el README en la portada, `taximetro.py` está subido y el tablero tiene las
cuatro historias en «Hecho». La entrega es el enlace a tu repositorio, el enlace al tablero y la demo en
directo del taxímetro.

---

## Retos extra (opcionales)

1. **Duración.** Al finalizar, muestra también cuánto ha durado (`Duración: 25 s`). Pista: guarda `"inicio"`
   en el diccionario.
2. **Confirmar la salida.** Con `s` y carrera abierta, pregunta «¿Seguro? Se perderá la carrera (s/n)».
3. **Tarifa nocturna.** Entre las 22:00 y las 6:00, tarifas un 20 % más caras. Pista:
   `time.localtime().tm_hour`. Decide si se mira al iniciar o en cada tramo, y explícalo en el README.

## Palabras que vas a oír

- **MVP**: la versión más pequeña que ya sirve; la fase 1.
- **Historia de usuario**: una necesidad escrita desde quien usa el programa («como taxista, quiero...»).
