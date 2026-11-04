# Fase 2 del taxímetro, paso a paso

Observabilidad y persistencia: US-05, US-06 y US-07, del 10 al 13/11. Al cerrar el programa ya queda rastro
(log e historial) y las tarifas se cambian sin tocar el código. Lo que se corrige está en la checklist de la fase 2 de `04-si-ya-sabes.md`.

Partes del `taximetro.py` de la fase 1. Clases que acompañan: SCRUM y GitHub Projects (10/11) y Python II
(12/11), que es la base de los pasos 2, 3 y 6.

## Cómo funciona cada paso

Igual que en la fase 1, con dos cosas nuevas:

- **Obligatorio** es lo que se evalúa; **Opcional si te da tiempo**, un extra.
- Cada herramienta nueva trae un ejemplo sobre otro tema (un juego) y el enlace a su documentación. El
  ejemplo enseña la forma, no tu código. Si llegas al paso antes que la clase, con eso puedes empezar.

Al acabar cada paso, sube tus cambios a Git como en la fase 1.

---

## Paso 0 · Antes de tocar nada

Haz una carrera completa (`i`, `m`, `f`, `s`) para ver que funciona. En GitHub Projects, comprueba que US-01 a
US-04 están en «Hecho».

En esta fase aparecen ficheros que son datos de cada ordenador, no código. Añade estas líneas al `.gitignore`
que creaste en la fase 1:

```
taximetro.log
historial.csv
.venv/
.pytest_cache/
```

Cuando aparezcan, `git status` no debe enseñarlos.

---

## Paso 1 · Logging: que el programa deje rastro — **Obligatorio**

`print` escribe en pantalla para el taxista. El **log** escribe en un fichero para el técnico: si algo falló
ayer a las 11, abre el log y ve qué pasó. Cada línea lleva fecha, hora y nivel (`INFO` normal, `WARNING` raro,
`ERROR` fallo). Lo hace el módulo `logging`, que viene con Python.

**Al acabar el paso**, cada vez que arrancas se añaden líneas al final de `taximetro.log` (no se borra lo
anterior), con este formato y estos mensajes. Los `print` siguen igual.

| Cuándo | Nivel | Mensaje |
|---|---|---|
| Al arrancar | `INFO` | `Arranque del taxímetro` |
| Con `i`, al crear la carrera | `INFO` | `Carrera iniciada` |
| Con `p` o `m`, al cambiar de estado | `INFO` | `Cambio de estado a movimiento (0.04 € acumulados)` |
| Con `f`, al cobrar | `INFO` | `Carrera finalizada: 0.23 €` |
| Con `s`, al salir | `INFO` | `Cierre del taxímetro` |
| Con una orden que no existe | `WARNING` | `Orden desconocida: 'x'` |

**Nombres:** el «logger» (el objeto con el que escribes) se llama `log` y se crea arriba del fichero, fuera de
las funciones, con `logging.getLogger("taximetro")`. La configuración va en una función `configurar_log()`.

**Ejemplo** (otro programa):

```py
import logging

log = logging.getLogger("juego")

logging.basicConfig(filename="juego.log", level=logging.INFO, encoding="utf-8",
                    format="%(asctime)s %(levelname)s %(message)s")

log.info("Partida empezada")
log.info("Nivel %s superado con %.1f puntos", 3, 1250)
log.warning("Tecla no válida: %r", "q")
```

Deja en `juego.log`:

```
2026-11-10 09:00:01,123 INFO Partida empezada
2026-11-10 09:00:01,124 INFO Nivel 3 superado con 1250.0 puntos
2026-11-10 09:00:01,124 WARNING Tecla no válida: 'q'
```

- `basicConfig` dice dónde escribir y con qué formato. Solo cuenta la primera vez, y lo que se escribe antes
  de llamarla se pierde. ¿En qué punto de `main()` tiene que ir tu `configurar_log()`?
- `level=logging.INFO` guarda `INFO` y lo más grave. ¿Qué dejaría de verse con `logging.WARNING`?
- `logging` no usa f-strings: pones `%s` (cualquier valor), `%.2f` (dos decimales) o `%r` (entre comillas) en
  el texto y los valores detrás, separados por comas.
- Mira la tabla: ¿en qué rama del bucle va cada línea, y antes o después de qué?

Documentación: [tutorial de logging](https://docs.python.org/es/3/howto/logging.html).

**Pruébalo** con dos terminales en la carpeta del proyecto. En una, `tail -f taximetro.log` (en PowerShell:
`Get-Content taximetro.log -Wait`): enseña cada línea nueva del fichero; se para con Ctrl+C. Si dice que no
existe, arranca antes el programa. En la otra, el taxímetro con `i`, `m`, `x`, `f`, `s`:

```
2026-11-10 10:15:49,677 INFO Arranque del taxímetro
2026-11-10 10:15:52,120 INFO Carrera iniciada
2026-11-10 10:15:54,301 INFO Cambio de estado a movimiento (0.04 € acumulados)
2026-11-10 10:15:55,918 WARNING Orden desconocida: 'x'
2026-11-10 10:15:58,044 INFO Carrera finalizada: 0.23 €
2026-11-10 10:16:00,502 INFO Cierre del taxímetro
```

**Si falla:**
- No aparece `taximetro.log` → `configurar_log()` no se llama. Si falta solo la primera línea, se llama tarde:
  ¿qué se ejecuta antes que ella?
- En pantalla sale `INFO:taximetro:Carrera iniciada` → falta `filename=` en `basicConfig`.
- `NameError: name 'log' is not defined` → falta `log = logging.getLogger(...)` arriba del fichero, fuera de
  cualquier función.
- `--- Logging error ---` con `TypeError: not enough arguments for format string` (o `not all arguments
  converted`) → no coinciden los `%` con los valores. El programa sigue, pero esa línea no se escribe.
- `tail -f` no enseña nada → estás en otra carpeta. `ls` en las dos terminales.

---

## Paso 2 · Las tarifas en `config.json` — **Obligatorio**

JSON es un formato de texto para datos que casi cualquier lenguaje sabe leer; se parece a un diccionario.
Crea `config.json` junto a `taximetro.py`:

```json
{
  "tarifa_parado": 0.02,
  "tarifa_movimiento": 0.05
}
```

Comillas **dobles** siempre, sin coma tras el último valor, decimales con punto. `config.json` sí se sube a
Git: es parte del programa.

**Al acabar el paso:**
- Las constantes `TARIFA_PARADO` y `TARIFA_MOVIMIENTO` desaparecen. En su lugar, un diccionario
  `TARIFAS_POR_DEFECTO` con las mismas dos claves y valores que el JSON.
- `cargar_tarifas(ruta=CONFIG)` lee el JSON y devuelve un diccionario con las dos tarifas como `float`.
  `ruta=CONFIG` es un valor por defecto: si la llamas sin nada, `cargar_tarifas()`, usa `CONFIG`; un test
  podrá pasarle otra ruta.
- Si va bien, escribe un `INFO` en el log; si no, un `WARNING`. Si el fichero no existe, está mal escrito o le
  falta una clave, **no cae**: devuelve una copia de `TARIFAS_POR_DEFECTO`. Mensajes en «Pruébalo».
- `main()` carga las tarifas una sola vez, justo después del log de arranque. `cerrar_tramo(carrera, tarifas)`
  recibe las tarifas como segundo parámetro, y lo mismo la función que elige la tarifa del estado.
- `config.json` y `taximetro.log` se buscan junto a `taximetro.py`, aunque lances el programa desde otra
  carpeta. Constantes: `CARPETA`, `CONFIG` y `LOG`. La primera es esta línea (`__file__` es la ruta del propio
  `.py`, y `.parent`, su carpeta):

```py
CARPETA = Path(__file__).parent
```

**Ejemplo** de lectura de un JSON con `try` / `except` (otro programa):

```py
import json
from pathlib import Path

ruta = Path("ajustes_juego.json")         # Path(...) / "fichero" une rutas
try:
    ajustes = json.loads(ruta.read_text(encoding="utf-8"))   # texto del fichero → diccionario
    vidas = int(ajustes["vidas"])
except (OSError, KeyError) as error:
    print("No pude leer", ruta, "->", error)
    vidas = 3
print(vidas)
```

- Python intenta lo del `try`. Si salta uno de los errores del `except`, salta ahí en vez de caer; `as error`
  guarda el mensaje. Un error que no está en la lista sigue rompiendo el programa.
- `OSError`: no se puede leer el fichero (`FileNotFoundError` es uno de ellos). `KeyError`: falta una clave.
  `ValueError`: un JSON mal escrito o un `float("abc")`. ¿Cuáles necesitas tú?
- Escribe `python` en la terminal, crea un diccionario `d`, prueba qué devuelve `dict(d)` y si cambiar la copia
  cambia `d`. Sal con `exit()`. ¿Por qué devolver una copia?
- ¿Qué funciones usaban `TARIFA_PARADO` y `TARIFA_MOVIMIENTO`? Esas necesitan ahora las tarifas, y quien las
  llama tiene que pasárselas.

Documentación: [errores y excepciones](https://docs.python.org/es/3/tutorial/errors.html),
[json](https://docs.python.org/es/3/library/json.html), [pathlib](https://docs.python.org/es/3/library/pathlib.html).

Tus `prueba_*.py` de la fase 1 usan las funciones antiguas y ya no funcionan: bórralos. En el paso 6 los
sustituyen los tests.

**Pruébalo** en cuatro tiempos:

1. Haz una carrera y busca en el log con `grep Tarifas taximetro.log` (en PowerShell:
   `Select-String Tarifas taximetro.log`):
   ```
   ... INFO Tarifas cargadas de /home/ana/taximetro/config.json: {'tarifa_parado': 0.02, 'tarifa_movimiento': 0.05}
   ```
2. La demo de US-07: pon `"tarifa_movimiento": 0.50`, arranca **sin tocar el código**, `i`, `m`, 10 s, `f`:
   unos 5 €. Vuelve a 0.05.
3. `mv config.json config.bak`, arranca y `s`. No se cae, y en el log:
   ```
   ... WARNING No se pudo leer /home/ana/taximetro/config.json ([Errno 2] No such file or directory: ...); uso tarifas por defecto
   ```
   Déjalo como estaba (`mv config.bak config.json`).
4. Borra la última `}` del JSON, arranca y `s`: otro `WARNING`, con `Expecting ',' delimiter` o parecido.
   Arregla el fichero.

**Si falla:**
- `NameError: name 'TARIFA_PARADO' is not defined` → algún sitio usa aún las constantes. Busca `TARIFA_`:
  solo debe quedar `TARIFAS_POR_DEFECTO`.
- `TypeError: cerrar_tramo() missing 1 required positional argument: 'tarifas'` → una llamada sigue sin el
  segundo argumento. Hay dos: en `p`/`m` y en `f`.
- `FileNotFoundError` o `JSONDecodeError` y el programa cae → la lectura está fuera del `try`, o al `except`
  le falta `OSError` o `ValueError`.
- `Expecting property name enclosed in double quotes` en el log → comillas simples o coma tras el último
  valor en el JSON.
- Cambias el JSON y cobra igual → editas otro `config.json` (mira la ruta del log) o no has reiniciado: las
  tarifas se leen al arrancar.
- `NameError: name 'CONFIG' is not defined` al arrancar → `def cargar_tarifas(ruta=CONFIG)` está encima de
  `CONFIG = ...`. Las constantes van antes de las funciones.

**Opcional si te da tiempo:** que Ctrl+C mientras espera una orden salga como si hubieras escrito `s`.
Ctrl+C dentro de `input()` lanza `KeyboardInterrupt`, y Ctrl+D (Ctrl+Z en Windows) `EOFError`.

---

## Paso 3 · Guardar cada carrera en `historial.csv` — **Obligatorio**

Un CSV es un fichero de texto con una fila por línea y los valores separados por comas; la primera línea es
la **cabecera**. Lo abre cualquier hoja de cálculo.

**Al acabar el paso**, cada `f` añade una fila a `historial.csv` (junto a `taximetro.py`; constante
`HISTORIAL`). La cabecera se escribe solo cuando el fichero es nuevo:

```
fecha,hora,duracion_s,importe
2026-11-10,10:42:07,25,0.80
```

`fecha` y `hora` son las del inicio de la carrera; `duracion_s`, segundos enteros redondeados; `importe`, con
dos decimales. En el log, la línea de `f` pasa a ser `Carrera guardada: 25 s, 0.80 €`.

**Nombres:**
- `guardar_carrera(inicio, duracion, importe, ruta=HISTORIAL)`: `inicio` es la fecha y hora reales,
  `duracion` los segundos y `importe` el total.
- El diccionario de la carrera gana dos claves al crearse: `"inicio"`, con `datetime.now()`, y
  `"inicio_mono"`, con `time.monotonic()`. `datetime` da la fecha y hora reales; `monotonic` solo sirve
  para medir. ¿Por qué no te vale `"desde"` para calcular la duración?
- La duración la calculas en la rama `f`.

**Ejemplo** (otro programa):

```py
import csv
from datetime import datetime

ahora = datetime.now()
print(ahora.strftime("%d/%m/%Y"))         # 10/11/2026

with open("partidas.csv", "a", newline="", encoding="utf-8") as fichero:
    escritor = csv.writer(fichero)
    escritor.writerow(["jugador", "puntos"])
    escritor.writerow(["Ana", 1250])
```

- `with open(...) as fichero:` abre el fichero y lo cierra solo al acabar el bloque. `"a"` añade al final;
  si el fichero no existe, lo crea.
- `newline=""` es obligatorio con `csv` (sin él, en Windows salen líneas en blanco).
- El ejemplo escribe la cabecera cada vez que se ejecuta. Para evitarlo, `Path(ruta).exists()` dice si el
  fichero ya está. ¿Lo preguntas antes o después del `open`?
- `csv.writer` se encarga de las comas y las comillas: no escribas las líneas a mano con `f"{a},{b}"`.
- Los códigos de `strftime`: `%Y`, `%m`, `%d` para la fecha; `%H`, `%M`, `%S` para la hora.

Documentación: [csv](https://docs.python.org/es/3/library/csv.html),
[códigos de strftime](https://docs.python.org/es/3/library/datetime.html#strftime-and-strptime-format-codes).

**Pruébalo** con `i`, `m`, `f`, `i`, `f`, `s` y luego `cat historial.csv`:

```
fecha,hora,duracion_s,importe
2026-11-10,10:42:07,4,0.20
2026-11-10,10:42:15,2,0.04
```

Arranca otra vez y haz otra carrera: tres filas y una sola cabecera.

**Si falla:**
- La cabecera se repite en cada arranque → miras si existe después del `open`. Piensa qué hace `"a"` si el
  fichero no existe.
- El importe sale `0.2` en vez de `0.20` → `round` quita el cero del final. Escríbelo con formato `:.2f`.
- El log dice `3 s` y el CSV `4` → `%d` corta los decimales sin redondear. Usa `round(duracion)` en los dos.
- `AttributeError: 'float' object has no attribute 'strftime'` → has pasado `inicio_mono` en vez de `inicio`.
- `KeyError: 'inicio'` → al diccionario de la orden `i` le falta la clave nueva.
- Una línea en blanco entre filas (Windows) → falta `newline=""`.
- El fichero no aparece → está junto a `taximetro.py` (por `CARPETA`), no donde lanzaste el programa.

---

## Paso 4 · La orden `h`: las carreras de hoy — **Obligatorio**

**Al acabar el paso**, la ayuda tiene, entre `f` y `a`, la línea `  h  historial de carreras de hoy`, y la
orden `h` lista las carreras de hoy y el total del día:

- Cada fila: dos espacios, la hora, dos espacios, la duración alineada a la derecha en 5 caracteres y ` s`,
  dos espacios, el importe alineado a la derecha en 8 y ` €`. Al final, `  Total del día: 0.47 €`.
- Sin carreras hoy, o sin fichero: `Hoy no hay carreras registradas.`, sin caer.

**Nombres:** `carreras_de_hoy(ruta=HISTORIAL)` devuelve una **lista** con las filas de hoy, cada una un
diccionario con las claves de la cabecera (`fila["hora"]`, `fila["importe"]`...). Sin fichero, lista vacía.
La función no imprime: el `print` va en la rama `h`. ¿Por qué conviene separarlo? (Pista: fase 3.)

**Ejemplo** (otro programa):

```py
with open("partidas.csv", newline="", encoding="utf-8") as fichero:
    for fila in csv.DictReader(fichero):
        print(fila["jugador"], fila["puntos"])
```

- `csv.DictReader` usa la cabecera como claves. Todo lo que sale es **texto**, también los números: para
  sumar importes, pásalos a `float`.
- Para saber si una fila es de hoy, compara su `fecha` con la de hoy escrita en el mismo formato que al
  guardar.
- Alinear: `f"{'abc':>5}"` da `'  abc'`.

**Pruébalo** con `h`:

```
> h
  10:42:07      4 s      0.20 €
  10:42:15      2 s      0.04 €
  10:58:02      7 s      0.23 €
  Total del día: 0.47 €
```

Sin CSV (`rm historial.csv`), `h` dice «Hoy no hay carreras registradas.» y no cae.

**Si falla:**
- `h` no enseña nada con filas en el CSV → el formato de fecha al filtrar no es el mismo que al guardar.
- `TypeError: unsupported operand type(s) for +: 'int' and 'str'` → sumas importes sin `float`.
- `KeyError: 'fecha'` → el CSV tiene otra cabecera (quizá lo creaste a mano). Bórralo y deja que lo cree el
  programa.
- `FileNotFoundError` al pulsar `h` → abres el CSV sin mirar antes si existe.

---

## Paso 5 · Sacar el cálculo a `importe_tramo()` — **Obligatorio**

Para comprobar `cerrar_tramo` hay que esperar segundos de verdad, porque mira el reloj. Una función que
recibe `(10, "parado", tarifas)` y devuelve `0.20` se comprueba al instante y siempre da lo mismo: es una
**función pura**. La idea: separar el cálculo del reloj, los ficheros y la pantalla.

**Al acabar el paso:**
- `importe_tramo(segundos, estado, tarifas)` devuelve lo que cuesta un tramo: segundos por la tarifa del
  estado. No mira el reloj ni toca ficheros.
- Con segundos negativos, lanza `ValueError("Los segundos no pueden ser negativos")`: es un fallo, y mejor
  enterarse que cobrar de menos.
- Sustituye a la función de la fase 1 que elegía la tarifa, y `cerrar_tramo` la usa: así `cerrar_tramo` solo
  se ocupa del reloj y del diccionario.

Para lanzar un error tú (otro ejemplo):

```py
def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

**Pruébalo** sin arrancar el taxímetro: escribe `python` en la carpeta y luego:

```python
>>> from taximetro import importe_tramo
>>> t = {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05}
>>> importe_tramo(10, "parado", t)
0.2
>>> importe_tramo(10, "movimiento", t)
0.5
>>> importe_tramo(-1, "parado", t)
Traceback (most recent call last):
  ...
ValueError: Los segundos no pueden ser negativos
>>> exit()
```

Después, una carrera normal: debe seguir cobrando bien.

**Si falla:**
- `ImportError: cannot import name 'importe_tramo'` → nombre mal escrito, o la función está dentro de `main()`.
- `NameError: name 'tarifa' is not defined` → algún sitio llama aún a la función antigua.
- `importe_tramo(-1, ...)` devuelve `-0.02` → la comprobación no está, o va después del `return`.

---

## Paso 6 · Tests con pytest — **Obligatorio**

Pytest se da en diciembre. Aquí basta con instalarlo, copiar tres tests, leer lo que dicen y escribir uno.

Pytest no viene con Python: se instala en un **entorno virtual** (12/11), una carpeta `.venv` con un Python
solo para este proyecto. Desde la carpeta del proyecto:

```bash
python -m venv .venv             # o python3 -m venv .venv
source .venv/bin/activate        # Mac y Linux
.venv\Scripts\activate           # Windows
pip install pytest
```

Actívalo cada vez que abras una terminal: está activo si la línea empieza por `(.venv)`. Dentro, el comando
es siempre `python`. `python -m pytest --version` debe responder `pytest` y un número.

Crea `test_taximetro.py` junto a `taximetro.py`, tal cual. Estos tests dicen lo que tu `importe_tramo` tiene
que cumplir:

```py
"""Tests de la lógica de tarifas (fase 2). Ejecutar con: python -m pytest"""
import pytest

from taximetro import importe_tramo

TARIFAS = {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05}

def test_parado_10_segundos():
    assert importe_tramo(10, "parado", TARIFAS) == pytest.approx(0.20)

def test_movimiento_10_segundos():
    assert importe_tramo(10, "movimiento", TARIFAS) == pytest.approx(0.50)

def test_segundos_negativos_dan_error():
    with pytest.raises(ValueError):
        importe_tramo(-1, "parado", TARIFAS)
```

- Pytest busca ficheros y funciones que empiecen por `test_`. Cada función es un test.
- `assert algo` afirma que eso es verdad; si no, el test falla y pytest enseña qué salió.
- `pytest.approx(0.20)` es «aproximadamente 0.20»: los decimales no son exactos en el ordenador
  (`7 * 0.05` da `0.35000000000000003`).
- `with pytest.raises(ValueError):` afirma que lo de dentro lanza ese error.

**Pruébalo** con `python -m pytest`:

```
collected 3 items

test_taximetro.py ...                                                    [100%]

============================== 3 passed in 0.01s ===============================
```

Cada punto es un test que pasa (`-v` muestra los nombres). Ahora rompe uno: cambia `0.20` por `0.25` en el
primero y ejecuta otra vez. Lo importante de la salida:

```
test_taximetro.py F..
...
E         Obtained: 0.2
E         Expected: 0.25 ± 2.5e-07

test_taximetro.py:9: AssertionError
...
========================== 1 failed, 2 passed in 0.02s =========================
```

Se lee de abajo arriba: qué test, en qué línea, qué salió y qué esperabas. Vuelve a poner `0.20`.

Tu test, al final del fichero: `test_carrera_mixta_suma_tramos`, que compruebe que 10 s parado más 10 s en
movimiento suman 0.70 €. Fíjate en los dos primeros. Debe dar `4 passed`. **Opcional si te da tiempo:** otro
que compruebe que 0 segundos en movimiento valen `0`.

**Si falla:**
- `No module named pytest` o `pytest: command not found` → el entorno no está activo, o pytest se instaló
  fuera. Actívalo y usa `python -m pytest`.
- `collected 0 items` → el fichero o las funciones no empiezan por `test_`.
- `assert 0.7000000000000001 == 0.7` → falta `pytest.approx`.
- `ensurepip is not available` al crear el entorno (Ubuntu) → instala el paquete que dice el mensaje
  (`sudo apt install python3-venv` o parecido), borra `.venv` y repite.
- PowerShell: `la ejecución de scripts está deshabilitada` al activar → una vez,
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, y activa de nuevo.
- VS Code subraya `import pytest` pero los tests pasan → elige el Python de `.venv`: Ctrl+Shift+P,
  «Python: Select Interpreter».

---

## Paso 7 · README, tablero y entrega — **Obligatorio**

Añade al `README.md` una sección `## Fase 2`, con tus palabras. Lo mínimo:

- cómo se cambian las tarifas y cuándo se aplican;
- dónde se guardan las carreras y cómo se ven las de hoy;
- dónde está el log y cómo seguirlo en vivo;
- cómo se preparan y se pasan los tests (los comandos del paso 6).

En GitHub Projects, US-05, US-06 y US-07 a «Hecho».

Demo (2 minutos): `tail -f` al lado, una carrera, `h`, cambiar la tarifa en el JSON y ver que cobra distinto,
y `python -m pytest` en verde. Lo que se corrige está en la checklist de la fase 2 de `04-si-ya-sabes.md`.

---

## Para pensar antes de la fase 3

Tu fichero ya tiene unas 150 líneas y hace de todo: calcula, lee ficheros, escribe el log y pinta el menú.
¿Qué pasaría si mañana la interfaz no fuera la terminal, sino una pantalla con botones? ¿Cuánto código
podrías reutilizar sin copiarlo? Esa es la fase 3.
