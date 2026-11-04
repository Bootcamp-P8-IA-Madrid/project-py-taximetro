# Fase 3 del taxímetro, paso a paso

Historias US-08 (contraseña segura) y US-09 (interfaz para tablet), más el encargo de que cada componente tenga
una responsabilidad clara. Partes del `taximetro.py` de la fase 2. Lo que se corrige está en la checklist de la fase 3 de `04-si-ya-sabes.md`.

Al terminar, el proyecto queda así:

```
tu-proyecto/
  taximetro/              el paquete: la lógica, sin pantalla
    __init__.py
    registro.py           configurar el log
    tarifas.py            Tarifas + cargar(ruta)
    historial.py          Historial: guardar / leer / de_hoy / total
    carrera.py            Carrera, Resumen, CarreraError
    auth.py               contraseña con hash y sal
  tests/                  los tests
  cli.py                  la terminal, usando el paquete
  app.py                  la interfaz Streamlit, usando el MISMO paquete
  config.json  requirements.txt  README.md  .gitignore
```

`ENUNCIADO.md`, `guia/`, `assets/` y `.github/` no se tocan.

| Cuándo | Qué | Necesita |
|---|---|---|
| 11 a 13/11 (en paralelo con la fase 2) | Paso 0, y 7.1 y 7.2 (Streamlit básico, sin el paquete) | Clase de Streamlit (11/11) |
| 16/11 | Pasos 1, 2 y 6 (paquete, módulos, contraseña) | Python II (12/11): módulos |
| 17/11 | Pasos 3, 4 y 5 (clases y tests de la carrera) | POO (17/11) |
| 18/11 | Paso 7 completo, 8 y 9 (app, entrega) | Todo lo anterior |

## Cómo funciona cada paso

- Los nombres y lo que devuelve cada cosa son obligatorios: los usan los tests y la otra interfaz.
- Casi todo ya lo tienes en tu fase 2: **mueve, no reescribas**. Tras cada movimiento, ejecuta el programa **y** los
  tests.
- Trabajas siempre desde la raíz del proyecto, con el entorno virtual activado. Desde ahí lanzas `python cli.py`,
  `python -m pytest` y `streamlit run app.py`. Para probar una clase suelta, abre `python`.
- Al acabar cada paso, sube tus cambios a Git como en la fase 1.

---

## Paso 0 · Instalar Streamlit — Obligatorio

Con el entorno de la fase 2 activado (si aún no lo tienes, créalo como en la guía 02), `pip install streamlit`. Crea en la raíz `requirements.txt` (otra persona
instala lo mismo con `pip install -r requirements.txt`):

```
streamlit>=1.48
pytest>=8
```

**Pruébalo** con `streamlit hello`: se abre la demo en el navegador. Ciérrala con Ctrl+C.

**Si falla:**
- `streamlit: command not found` o `No module named 'streamlit'` → el entorno no estaba activo. Actívalo y repite.
- No se abre el navegador → copia `http://localhost:8501` de la terminal.

---

## Paso 1 · Por qué separar — Obligatorio (15 minutos)

Apunta de qué se ocupa cada función de tu `taximetro.py`: calcular, la configuración, el historial, el log, el
reloj, la pantalla… ¿Cuál se ocupa de todo?

Es `main`. Para la app con botones tendrías que copiarla entera, y la carrera no se puede probar sin esperar porque
está pegada a `input()` y al reloj. La salida: **un módulo por responsabilidad** y dos pantallas que solo los
llaman.

---

## Paso 2 · El paquete, módulo a módulo — Obligatorio

Un **paquete** es una carpeta con un `__init__.py` (puede estar vacío); cada `.py` de dentro es un **módulo**. Desde
fuera se importa así: `from taximetro.tarifas import cargar`. Aquí las funciones se mueven tal cual, **sin
clases**. Repaso: [módulos y paquetes](https://docs.python.org/es/3/tutorial/modules.html).

**2.1 `taximetro.py` pasa a ser `cli.py`.** No pueden convivir un fichero `taximetro.py` y una carpeta `taximetro/`:

```bash
git mv taximetro.py cli.py
```

`python -m pytest` da ahora `ModuleNotFoundError: No module named 'taximetro'`. De momento, que el test importe
`importe_tramo` de `cli`. En verde.

**2.2 El log, a `registro.py`.**

```bash
mkdir taximetro
touch taximetro/__init__.py        # Windows: type nul > taximetro\__init__.py
```

`taximetro/registro.py` tiene una función, `configurar(ruta="taximetro.log")`, que sustituye a `configurar_log`.
Sin `basicConfig`: solo funciona si nadie ha configurado el log antes, y con Streamlit no lo controlas. En su
lugar, sobre el logger `"taximetro"`:

- si ya tiene manejadores (`.handlers`), no hace nada: así no se duplican las líneas;
- si no, le añade (`addHandler`) un `logging.FileHandler(ruta, encoding="utf-8")` con un `logging.Formatter` de
  formato `"%(asctime)s %(levelname)s %(name)s: %(message)s"`, y pone el nivel `logging.INFO` (`setLevel`).

Otro tema:

```python
import logging

log = logging.getLogger("juego")
if not log.handlers:                          # solo si aún no tiene manejador
    manejador = logging.FileHandler("juego.log", encoding="utf-8")
    manejador.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    log.addHandler(manejador)
    log.setLevel(logging.INFO)

logging.getLogger("juego.nivel1").info("hola")   # un hijo de "juego"
```

En `juego.log` sale `INFO juego.nivel1: hola`: lo que escribe un logger hijo va al fichero del padre.

Cada módulo usará un logger hijo, `logging.getLogger("taximetro.tarifas")`, `"taximetro.historial"`…, y todos
escriben en ese fichero. Documentación: [logging](https://docs.python.org/es/3/howto/logging.html).

En `cli.py`, borra `configurar_log` y `LOG` y llama a `registro.configurar()`.

**Pruébalo:** una carrera. En `taximetro.log`, las líneas nuevas llevan el nombre del logger:

```
2026-11-16 10:12:33,733 INFO taximetro: Arranque del taxímetro
```

**2.3 Las tarifas, a `tarifas.py`.** Mueve `TARIFAS_POR_DEFECTO` y `cargar_tarifas`, que pasa a llamarse
`cargar(ruta="config.json")` (ruta relativa: a partir de ahora lanzas siempre desde la raíz, también
`streamlit run`). ¿Qué imports necesita el módulo? En
`cli.py`, borra lo movido y `CONFIG`, y usa `cargar("config.json")`.

**Pruébalo:** en el log, `INFO taximetro.tarifas: Tarifas cargadas de config.json: {...}`.

**2.4 El historial, a `historial.py`.** Igual con `guardar_carrera` y `carreras_de_hoy` (ruta por defecto
`"historial.csv"`). **Pruébalo:** una carrera y `h`.

**2.5 El cálculo, a `carrera.py`; los tests, a `tests/`.** `importe_tramo` y `cerrar_tramo` van a
`taximetro/carrera.py`; `cli.py` importa `cerrar_tramo` de `taximetro.carrera`. En `cli.py` quedan imports, `log`, `AYUDA` y `main()`: borra `CARPETA` y los imports sin
uso.

```bash
mkdir tests
git mv test_taximetro.py tests/
```

El test importa ahora de `taximetro.carrera`.

**Pruébalo:** una carrera completa (`i`, `m`, `p`, `f`, `h`, `s`) y `python -m pytest`:

```
tests/test_taximetro.py .....                                            [100%]
============================== 5 passed in 0.01s ===============================
```

(O `4 passed` sin el opcional de la fase 2.)

**Si falla:**
- `ModuleNotFoundError: No module named 'taximetro'` con `pytest` a secas → usa `python -m pytest`. Con
  `python cli.py` → no estás en la raíz o falta `taximetro/__init__.py`.
- `ImportError: cannot import name 'cargar'` → la función se sigue llamando `cargar_tarifas`.
- `NameError: name 'HISTORIAL' is not defined` (u otro nombre) → algo movido se sigue usando en otro sitio.
  Impórtalo o pon el valor (`"historial.csv"`).
- `NameError: name 'json' is not defined` (o `csv`, `Path`, `time`) → cada módulo importa lo que usa.
- Las líneas del log salen dos veces → `configurar` añade el manejador aunque ya tenga uno.

---

## Paso 3 · La clase `Carrera` — Obligatorio (tras la clase de POO del 17/11)

Una **clase** junta datos (**atributos**, en `self`) y las funciones que los manejan (**métodos**). Otro tema:

```python
class LimiteError(Exception):
    """Error con nombre propio: basta con heredar de Exception."""

class Tarjeta:
    def __init__(self, limite):      # se ejecuta al crear: Tarjeta(100)
        self.limite = limite
        self._gastado = 0.0          # guion bajo: «interno, no lo toques desde fuera»

    @property
    def agotada(self):               # se usa sin paréntesis: t.agotada
        return self._gastado >= self.limite

    def pagar(self, euros):
        if self._gastado + euros > self.limite:
            raise LimiteError(f"Faltan {self._gastado + euros - self.limite:.2f} €")
        self._gastado += euros

t = Tarjeta(100)
t.pagar(30)
print(t.agotada)     # False
t.pagar(80)          # LimiteError: Faltan 10.00 €
```

`self` es el propio objeto: primer parámetro de todo método. Documentación:
[clases](https://docs.python.org/es/3/tutorial/classes.html).

**Qué tiene que haber en `carrera.py`** (`importe_tramo` se queda de momento): la excepción `CarreraError` y la
clase `Carrera`. `Carrera(tarifas)` empieza sin carrera en curso.

| Método o atributo | Qué hace | Devuelve o lanza |
|---|---|---|
| `estado` | `None` sin carrera; si no, `"parado"` o `"movimiento"` | — |
| `inicio` | fecha y hora de inicio (`datetime`) | — |
| `en_curso` (propiedad) | ¿hay carrera? | `bool` |
| `iniciar(estado="parado")` | la orden `i` | `CarreraError("Ya hay una carrera en curso")`; `CarreraError("Estado desconocido: ...")` |
| `cambiar_estado(nuevo)` | `p`/`m`: cierra el tramo y cambia; al mismo estado, no hace nada | `CarreraError("No hay ninguna carrera en curso")`; `CarreraError("Estado desconocido: ...")` |
| `importe_actual()` | lo cobrado hasta ahora, **sin** cerrar el tramo | `float` (0.0 sin carrera) |
| `duracion()` | segundos desde el inicio | `float` (0.0 sin carrera) |
| `finalizar()` | `f`: cierra el tramo y deja el objeto listo para otra carrera | `{"inicio", "duracion", "importe"}` con el importe redondeado a céntimos (`round(…, 2)`); `CarreraError("No hay ninguna carrera en curso")` |

La clase no imprime: **lanza** `CarreraError`, y quien la usa decide cómo enseñarlo. Sí escribe en el log, con el
logger `"taximetro.carrera"`: los mismos eventos que en la fase 2 (inicio, cambio de estado, fin).

Pistas:
- Cada clave de tu diccionario `carrera` será un atributo. `__init__` los crea todos.
- `cerrar_tramo(carrera, tarifas)` pasa a ser un método interno. ¿Dónde tiene ahora las tarifas?
- `importe_actual` hace la cuenta de cerrar el tramo, pero sin guardar nada. ¿Qué pasaría si lo cerrara?
- Borra la función suelta `cerrar_tramo`.

**`cli.py`**: `main()` crea una `Carrera(cargar("config.json"))` y cada orden llama a un método; ni cuentas, ni
`time`, ni diccionario. El «Llevas» de `p` y `m` sale de `importe_actual()`. Los avisos del paso 8 de la fase 1
desaparecen: el cuerpo del bucle va en un `try` cuyo `except CarreraError as error` imprime `No se puede: {error}.`.
Solo `s` con una carrera abierta sigue necesitando su comprobación (`en_curso`): salir no es un método de `Carrera`.

**Pruébalo.** La clase sola, en `python`:

```python
>>> from taximetro.carrera import Carrera
>>> c = Carrera({"tarifa_parado": 0.02, "tarifa_movimiento": 0.05})
>>> c.en_curso
False
>>> c.iniciar()
>>> c.estado
'parado'
>>> c.cambiar_estado("movimiento")
>>> c.finalizar()
{'inicio': datetime.datetime(2026, 11, 17, 10, 56, 7, 370054), 'duracion': 8.300123456, 'importe': 0.3}
>>> c.finalizar()
Traceback (most recent call last):
  ...
taximetro.carrera.CarreraError: No hay ninguna carrera en curso
```

Luego `python cli.py` con los casos raros:

```
> f
No se puede: No hay ninguna carrera en curso.
> i
Carrera iniciada. El taxi está PARADO.
> i
No se puede: Ya hay una carrera en curso.
> m
Estado: MOVIMIENTO. Llevas 0.04 €.
> m
Estado: MOVIMIENTO. Llevas 0.09 €.
> f
Carrera finalizada. Total a cobrar: 0.21 €
```

**Si falla:**
- `TypeError: ... takes 1 positional argument but 2 were given` → falta `self` en algún método.
- `AttributeError: 'Carrera' object has no attribute '...'` → `__init__` no lo creó, o está escrito distinto.
- `TypeError: 'bool' object is not callable` → `c.en_curso()`: una propiedad va sin paréntesis.
- El programa cae con `CarreraError` → esa línea está fuera del `try`.
- El importe sale siempre `0.00` → el tramo no se suma, o `iniciar` no anota cuándo empieza.
- Mirar el importe lo cambia (`m` dos veces cobra de más) → `importe_actual` modifica algún atributo.

---

## Paso 4 · `Resumen`, `Tarifas` e `Historial` — Obligatorio

Una **dataclass** es una clase para guardar datos: declaras los campos y Python escribe el `__init__`, el `==` y
cómo se imprime. Con `frozen=True` no se puede modificar. Puede tener métodos. Otro tema:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Libro:
    titulo: str            # «nombre: tipo»: así sabe qué campos hay
    paginas: int = 100     # con valor por defecto

    def es_largo(self):
        return self.paginas > 300

b = Libro("Niebla", 250)   # Libro(titulo='Niebla', paginas=250)
b == Libro("Niebla", 250)  # True
b.paginas = 1              # dataclasses.FrozenInstanceError
```

Documentación: [dataclasses](https://docs.python.org/es/3/library/dataclasses.html).

**4.1 `Resumen`**, en `carrera.py`: dataclass congelada con `inicio`, `duracion` e `importe`, en ese orden.
`finalizar` lo devuelve en vez del diccionario, y `cli.py` lee `resumen.importe`, `resumen.inicio`…, con punto
(también en la llamada que guarda en el historial).

**4.2 `Tarifas`**, en `tarifas.py`, en lugar de `TARIFAS_POR_DEFECTO`:

| Nombre | Qué es o hace | Devuelve |
|---|---|---|
| `Tarifas(parado=0.02, movimiento=0.05)` | dataclass congelada, campos en ese orden (€/s) | — |
| `tarifas.por_estado(estado)` | método: la tarifa de ese estado | `float` |
| `cargar(ruta="config.json")` | lee el JSON como antes | un `Tarifas`; `Tarifas()` si falla |

El JSON no cambia: sigue con `tarifa_parado` y `tarifa_movimiento`. Los campos de `Tarifas` se llaman `parado` y
`movimiento`.

`importe_tramo` sobra: bórrala y que `Carrera` use `por_estado`. `Carrera(tarifas=None)` usa `Tarifas()` si no le
pasan nada. Dentro del paquete, un módulo importa a otro con un punto («del mismo paquete»):

```python
from .tarifas import Tarifas
```

Borra `tests/test_taximetro.py`: probaba `importe_tramo`.

**4.3 `Historial`**, en `historial.py`. Tus dos funciones comparten la ruta: eso es una clase con un atributo.

| Método | Qué hace | Devuelve |
|---|---|---|
| `Historial(ruta="historial.csv")` | guarda la ruta | — |
| `guardar(resumen)` | añade la fila de un `Resumen` (mismo CSV que en la fase 2) | nada |
| `leer()` | todas las filas, como diccionarios | lista (vacía sin fichero) |
| `de_hoy()` | las de hoy | lista |
| `total(filas)` | suma sus importes | `float` |

`total` no usa `self`: ponle `@staticmethod` encima y quita `self`. ¿Puede `de_hoy` aprovechar `leer`? En
`cli.py`, un `Historial("historial.csv")` junto a la carrera, para `f` y `h`.

**4.4 Tests.** Copia en `tests/test_tarifas_historial.py`:

```python
import json
from datetime import datetime

from taximetro.carrera import Resumen
from taximetro.historial import Historial
from taximetro.tarifas import Tarifas, cargar

def test_historial_guarda_y_lee(tmp_path):
    historial = Historial(tmp_path / "h.csv")
    historial.guardar(Resumen(datetime.now(), 12.4, 1.5))
    historial.guardar(Resumen(datetime.now(), 30, 2.25))
    filas = historial.de_hoy()
    assert [f["importe"] for f in filas] == ["1.50", "2.25"]
    assert historial.total(filas) == 3.75

def test_tarifas_desde_json(tmp_path):
    ruta = tmp_path / "config.json"
    ruta.write_text(json.dumps({"tarifa_parado": 0.03, "tarifa_movimiento": 0.08}))
    assert cargar(ruta) == Tarifas(0.03, 0.08)

def test_tarifas_por_defecto_si_falta(tmp_path):
    assert cargar(tmp_path / "nada.json") == Tarifas()
```

`tmp_path` es una carpeta temporal y vacía que pytest crea para cada test.

**Pruébalo** en `python`:

```python
>>> from taximetro.tarifas import Tarifas
>>> t = Tarifas()
>>> t
Tarifas(parado=0.02, movimiento=0.05)
>>> t.por_estado("movimiento")
0.05
>>> t.parado = 1
dataclasses.FrozenInstanceError: cannot assign to field 'parado'
```

Después una carrera y `h` en `python cli.py`, y los tests: `3 passed` (5 si ya hiciste el paso 6).

**Si falla:**
- `AttributeError: 'dict' object has no attribute ...` → `finalizar` o `cargar` siguen devolviendo un diccionario.
- `TypeError: 'Resumen' object is not subscriptable` (o `'Tarifas'`) → quedan corchetes; con objetos, punto.
- `TypeError: Historial.guardar() takes 2 positional arguments but 4 were given` → ahora recibe el `Resumen`.
- `ImportError: cannot import name 'importe_tramo'` → queda el test viejo o un import que la nombra.
- `test_tarifas_desde_json` da `Tarifas(parado=0.08, movimiento=0.03)` → campos en otro orden.
- `TypeError: Historial.total() takes 1 positional argument but 2 were given` → falta `@staticmethod`.

---

## Paso 5 · Reloj inyectable y tests de `Carrera` — Obligatorio

Probar una carrera de 25 segundos en un milisegundo. Si `Carrera` guarda **una función que da la hora**, en el
programa es `time.monotonic` y en los tests un reloj falso que avanza cuando el test dice. Pasarle a un objeto «de
quién depende» es **inyección de dependencias** (clase de patrones del 16/11).

Lo que tiene que cumplir: `Carrera(tarifas=None, reloj=time.monotonic)` y **ningún** `time.monotonic()` en el resto
de la clase. Una función se guarda **sin paréntesis** y se llama después:

```python
import random
tirar = random.random      # guardas la función
tirar()                    # la llamas
```

Copia en `tests/test_carrera.py`. `__call__` hace que `RelojFalso` se pueda **llamar como una función**; las
funciones con `@pytest.fixture` preparan un objeto nuevo para cada test que lo pida como parámetro.

```python
import pytest

from taximetro.carrera import Carrera, CarreraError
from taximetro.tarifas import Tarifas

class RelojFalso:
    """Reloj que solo avanza cuando el test lo dice: así no hay que esperar."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def avanzar(self, segundos):
        self.t += segundos

@pytest.fixture
def reloj():
    return RelojFalso()

@pytest.fixture
def carrera(reloj):
    return Carrera(Tarifas(parado=0.02, movimiento=0.05), reloj=reloj)

def test_parado_10_segundos(carrera, reloj):
    carrera.iniciar()
    reloj.avanzar(10)
    assert carrera.finalizar().importe == pytest.approx(0.20)

def test_movimiento_10_segundos(carrera, reloj):
    carrera.iniciar("movimiento")
    reloj.avanzar(10)
    assert carrera.finalizar().importe == pytest.approx(0.50)

def test_carrera_mixta(carrera, reloj):
    carrera.iniciar()
    reloj.avanzar(10)                        # 10 s parado   = 0.20
    carrera.cambiar_estado("movimiento")
    reloj.avanzar(10)                        # 10 s en marcha = 0.50
    carrera.cambiar_estado("parado")
    reloj.avanzar(5)                         # 5 s parado    = 0.10
    resumen = carrera.finalizar()
    assert resumen.importe == pytest.approx(0.80)
    assert resumen.duracion == 25

def test_importe_actual_sin_finalizar(carrera, reloj):
    carrera.iniciar("movimiento")
    reloj.avanzar(4)
    assert carrera.importe_actual() == pytest.approx(0.20)
    assert carrera.en_curso

def test_mismo_estado_no_cambia_nada(carrera, reloj):
    carrera.iniciar()
    reloj.avanzar(3)
    carrera.cambiar_estado("parado")
    reloj.avanzar(3)
    assert carrera.finalizar().importe == pytest.approx(0.12)

def test_no_se_puede_iniciar_dos_veces(carrera):
    carrera.iniciar()
    with pytest.raises(CarreraError):
        carrera.iniciar()

def test_no_se_puede_finalizar_sin_iniciar(carrera):
    with pytest.raises(CarreraError):
        carrera.finalizar()

def test_estado_desconocido(carrera):
    carrera.iniciar()
    with pytest.raises(CarreraError):
        carrera.cambiar_estado("volando")

def test_tras_finalizar_se_puede_encadenar(carrera, reloj):
    carrera.iniciar()
    reloj.avanzar(10)
    carrera.finalizar()
    carrera.iniciar("movimiento")
    reloj.avanzar(2)
    assert carrera.finalizar().importe == pytest.approx(0.10)
```

**Pruébalo:** `python -m pytest` → `12 passed` (14 si ya hiciste el paso 6). `python cli.py` sigue con el reloj de verdad.

**Si falla:**
- `TypeError: 'float' object is not callable` → `reloj=time.monotonic()`, con paréntesis.
- `duracion == 25` falla, o sale una duración enorme → queda algún `time.monotonic()` en la clase.
- `fixture 'carrera' not found` → falta un `@pytest.fixture` al copiar.

---

## Paso 6 · Contraseña con hash y sal — Obligatorio (US-08)

La contraseña no se guarda: se guarda su **hash**, una ristra calculada a partir de ella que no se puede deshacer.
Para comprobar, se calcula el hash de lo escrito y se compara con el guardado.

- **Sal**: bytes aleatorios, distintos para cada contraseña, que se mezclan con ella antes del hash. Se guarda junto
  al hash; no es secreta, pero inutiliza las tablas de hashes conocidos.
- **PBKDF2** repite el hash muchas veces (aquí, 200 000) para que probar millones de contraseñas cueste.
- **`hmac.compare_digest`** compara en tiempo constante: nadie deduce nada midiendo cuánto tarda.

Otro tema, un PIN de móvil:

```python
import hashlib, hmac, os

sal = os.urandom(16)                                                    # 16 bytes aleatorios
huella = hashlib.pbkdf2_hmac("sha256", "1234".encode(), sal, 200_000)   # bytes
texto = sal.hex()                       # bytes → texto (para un JSON)
bytes.fromhex(texto) == sal             # True: texto → bytes

intento = hashlib.pbkdf2_hmac("sha256", "1243".encode(), sal, 200_000)
hmac.compare_digest(intento, huella)    # False
```

Documentación: [hashlib.pbkdf2_hmac](https://docs.python.org/es/3/library/hashlib.html#hashlib.pbkdf2_hmac),
[hmac.compare_digest](https://docs.python.org/es/3/library/hmac.html#hmac.compare_digest),
[getpass](https://docs.python.org/es/3/library/getpass.html) (pide texto sin enseñarlo).

**6.1 `taximetro/auth.py`:**

| Función | Qué hace | Devuelve o lanza |
|---|---|---|
| `crear_contrasena(contrasena, ruta="credenciales.json")` | sal nueva y hash; guarda los dos en hexadecimal en un JSON `{"sal": ..., "hash": ...}` | nada; `ValueError` con menos de 4 caracteres |
| `hay_contrasena(ruta="credenciales.json")` | ¿existe el fichero? | `bool` |
| `verificar(contrasena, ruta="credenciales.json")` | hash de lo escrito con la sal **guardada**, comparado con el hash guardado | `bool`; `False` si el fichero falta o está mal |

Al final del módulo, un `if __name__ == "__main__":` que pide la contraseña dos veces con `getpass.getpass`; si no
coinciden, `raise SystemExit("No coinciden.")`; si coinciden, la guarda y escribe
`Contraseña guardada en credenciales.json`. Si `crear_contrasena` lanza `ValueError` (demasiado corta), atrápalo y
`raise SystemExit(error)`. Se lanza con `python -m taximetro.auth`.

Pistas: ¿una función interna para el hash, que usen las dos? Para leer el JSON sin caer, mira tu `cargar`.

**6.2 `cli.py`**: si hay contraseña y la escrita (con `getpass`) no es buena,
`raise SystemExit("Contraseña incorrecta.")`.

**6.3** `credenciales.json` al `.gitignore`: ni el hash se sube. En `git status` no debe aparecer.

**6.4 Tests.** Copia en `tests/test_auth.py`. El primero es la prueba de US-08:

```python
from taximetro import auth

def test_contrasena_no_se_guarda_en_claro(tmp_path):
    ruta = tmp_path / "cred.json"
    auth.crear_contrasena("taxi1234", ruta)
    assert "taxi1234" not in ruta.read_text()
    assert auth.verificar("taxi1234", ruta)
    assert not auth.verificar("otra", ruta)

def test_sin_fichero_de_credenciales(tmp_path):
    assert not auth.verificar("x", tmp_path / "no.json")
```

**Pruébalo:** `python -m taximetro.auth`, y `cat credenciales.json`:

```
{"sal": "4614eaf91e73f5f69897779598e2661a", "hash": "a59876527a95eecc92239652a810b0cd4bc91e919ad8f389dce41b900e41a08d"}
```

Tu sal y tu hash serán otros; tu contraseña no está. `python cli.py` con una mala dice `Contraseña incorrecta.`;
con la buena, el menú. Tests: `14 passed` (7 si aún no has hecho el paso 4).

**Si falla:**
- `TypeError: Object of type bytes is not JSON serializable` → al JSON, texto: `.hex()`.
- `TypeError: a bytes-like object is required, not 'str'` → `pbkdf2_hmac` quiere bytes: `.encode()` para la
  contraseña, `bytes.fromhex(...)` para la sal leída.
- `verificar` siempre da `False` → usas una sal nueva en vez de la guardada, o comparas texto con bytes.
- `test_sin_fichero_de_credenciales` cae con `FileNotFoundError` → la lectura está fuera del `try`.
- `EOFError` al pedir la contraseña → el editor no admite entrada oculta. Usa una terminal normal.

---

## Paso 7 · La app Streamlit, en cinco tramos — Obligatorio (US-09)

Botones grandes, estado e importe a la vista, el importe subiendo solo y los botones respondiendo mientras sube.
Tres cosas de Streamlit distintas de un programa normal:

1. **Ejecuta el fichero entero, de arriba abajo, cada vez que pulsas algo.** `st.button("X")` es `True` solo en la
   ejecución del clic.
2. **Las variables normales se pierden entre clics.** Lo que debe sobrevivir va en `st.session_state`.
3. **Nada de `while True` ni `time.sleep`**: bloquean la página.

Arranca `streamlit run app.py` y déjalo: al guardar, se recarga. Documentación:
[API de Streamlit](https://docs.streamlit.io/develop/api-reference).

**7.1 Un botón.** `app.py` con `st.title`, `st.write` y un `st.button` que, al pulsarlo, escribe «Me has pulsado».
**Pruébalo:** pulsa y sale; recarga y desaparece.

**7.2 Recordar entre clics.** Un contador de clics con una variable normal siempre dice 1: ¿por qué? Con
`session_state`:

```python
import streamlit as st

if "clics" not in st.session_state:      # solo la primera vez
    st.session_state.clics = 0

if st.button("Púlsame"):
    ...                                  # suma 1 al contador guardado

st.write(f"Me has pulsado {st.session_state.clics} veces.")
```

**Pruébalo:** tres clics, «3 veces». Ese «si no está, créalo» es el de la carrera.

**7.3 Los botones de la carrera.** Sustituye `app.py`. Tiene que haber:

- `st.set_page_config(page_title="Taxímetro", page_icon="🚕")` como **primera** orden `st.`, y
  `registro.configurar()`.
- Una `Carrera` creada **una vez**, en `st.session_state.carrera`. El `Historial` puede crearse en cada ejecución:
  no guarda nada en memoria.
- Sin carrera: botón «Iniciar carrera».
- Con carrera: estado (`🔴 PARADO` / `🟢 EN MARCHA`) e importe (`0.37 €`) con `st.metric`; «Parado» y «En marcha»
  en fila, con el del estado actual apagado; y «Finalizar carrera», que guarda en el historial.
- Tras cambiar la carrera, `st.rerun()`: repinta al momento con el estado nuevo.

Pistas: `izq, der = st.columns(2)` y luego `izq.button(...)`. `disabled=` recibe `True` o `False` (por ejemplo,
comparando con `carrera.estado`). `st.metric("Estado", ...)`.

**La app no calcula nada**: llama a `Carrera` e `Historial`, como el CLI. Botones a todo el ancho: `width="stretch"`
en [st.button](https://docs.streamlit.io/develop/api-reference/widgets/st.button).

**Pruébalo:** Iniciar → En marcha → el importe sube **solo al pulsar algo** (lo arregla 7.4) → Finalizar → vuelve
«Iniciar carrera» y hay una fila más en `historial.csv`.

**7.4 El contador en tiempo real.** Un **fragmento** es una función que Streamlit vuelve a ejecutar sola cada cierto
tiempo, **sin** el resto de la página. Otro tema:

```python
from datetime import datetime

import streamlit as st

@st.fragment(run_every=1)          # cada segundo
def reloj():
    st.metric("Hora", datetime.now().strftime("%H:%M:%S"))

reloj()                            # se pinta donde la llamas
```

Pasa las métricas de la carrera a un fragmento y añade la duración (`st.caption`). Documentación:
[st.fragment](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment).

Botones y números grandes para la tablet (es CSS, el lenguaje de estilos de la web), tras `registro.configurar()`:

```python
st.markdown(
    "<style>div.stButton > button { height: 4.5rem; font-size: 1.6rem; }"
    "[data-testid='stMetricValue'] { font-size: 3rem; }</style>",
    unsafe_allow_html=True,
)
```

**Pruébalo:** el importe sube cada segundo **sin tocar nada**, y Parado responde al instante.

**7.5 Acceso, última carrera, historial y salir.**

- **Acceso**, antes de la carrera. Sin contraseña creada: `st.error` que diga cómo crearla
  (`python -m taximetro.auth`) y nada más. Con contraseña y sin haber entrado: caja
  `st.text_input(..., type="password")` y `st.form_submit_button("Entrar")`, los dos dentro de un
  [st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form). Buena:
  `st.session_state.autenticado = True` y `st.rerun()`. Mala: «Contraseña incorrecta». Mientras no hayas entrado,
  [st.stop()](https://docs.streamlit.io/develop/api-reference/execution-flow/st.stop) corta el script ahí.
- **Última carrera.** «Finalizar» guarda también el resumen en `st.session_state.ultimo`. Sin carrera, antes de
  Iniciar: `Última carrera: 0.80 € (25 s)` con `st.success`.
- **Historial de hoy**, al final, en un `st.expander` desplegado solo sin carrera (parámetro `expanded=`): tabla con hora, duración e importe
  (`st.table` acepta una lista de diccionarios) y total del día.
- **Salir**: botón que olvida carrera y acceso (`st.session_state.clear()`) y vuelve a ejecutar.

**Pruébalo:**

1. Sin `credenciales.json` (renómbralo un momento): mensaje rojo y nada más.
2. Contraseña mala: «Contraseña incorrecta». Buena: «Iniciar carrera» y el historial desplegado.
3. Iniciar → En marcha → sube solo → Parado → Finalizar → «Última carrera» y una fila más en el historial.
4. Otra carrera seguida, sin recargar.
5. En `taximetro.log`, los eventos de la app con `taximetro.carrera`, `taximetro.auth`…
6. Desde el móvil o la tablet en la misma red: `streamlit run app.py --server.address 0.0.0.0` y
   `http://IP-de-tu-ordenador:8501`.

**Si falla:**
- `st.session_state has no attribute "carrera"` → la usas antes de crearla: el fichero va de arriba abajo.
- Cada clic empieza una carrera nueva, o pide contraseña otra vez → `Carrera` o `autenticado` no están en
  `session_state`, o se crean sin el «si no está».
- El importe no sube solo → el contador no está en un fragmento con `run_every`, o no lo llamas.
- La página se queda en «RUNNING» → hay un `while True` o un `time.sleep`.
- `set_page_config() can only be called once` o «must be the first Streamlit command» → `st.set_page_config` va
  la primera.
- `StreamlitDuplicateElementId` → dos botones con el mismo texto: cambia uno o dale `key=`.
- `Missing Submit Button` → el `st.form` necesita un `st.form_submit_button` dentro.
- El log de la app no se escribe → `registro.configurar()` usa `basicConfig`.
- No aparece la última carrera → el `st.rerun()` va antes de guardarla en `session_state`.

---

## Paso 8 · `cli.py` y `app.py` comparten el paquete — Obligatorio (10 minutos)

1. No debe salir nada:

   ```bash
   grep -n "monotonic\|por_estado\|csv.writer\|DictReader\|pbkdf2\|json.loads" cli.py app.py
   ```

   (PowerShell: `Select-String -Pattern "monotonic|por_estado|csv.writer|DictReader|pbkdf2|json.loads" cli.py, app.py`.)
   Si sale algo, se va al módulo que le toca.
2. Los dos importan lo mismo del paquete (`Carrera`, `Historial`, `cargar`, `auth`, `registro`).
3. Una carrera en cada interfaz acaba en el mismo `historial.csv` y el mismo `taximetro.log`.
4. `"tarifa_movimiento": 0.50` en `config.json`: las dos cobran distinto sin tocar código. Vuelve a 0.05.
5. Piensa cómo explicarías qué cambia si mañana el cliente quiere una app de móvil, y qué no.

---

## Paso 9 · Entrega — Obligatorio

**9.1** `git status`: no salen el log, el CSV, `credenciales.json` ni `.venv/`. Si sale alguno, añádelo al
`.gitignore`.

**9.2** Sección `## Fase 3` del README, con tus palabras: **estructura** (el árbol del principio, una línea por
fichero), **cómo arrancar** (entorno, `pip install -r requirements.txt`, `python -m taximetro.auth`, `streamlit run
app.py` o `python cli.py`, `python -m pytest`) y **decisiones técnicas**, que el enunciado pide justificar: una
línea por decisión y su porqué. ¿Por qué un módulo por responsabilidad? ¿Por qué un hash y no la contraseña? ¿Dónde
vive la carrera en Streamlit y cómo sube el contador sin bloquear?

**9.3** Tablero: US-08 y US-09 a «Hecho».

**9.4** Ensayo de la demo (3 minutos):

1. `python -m pytest` en verde.
2. `cat credenciales.json`: «aquí no está la contraseña».
3. `streamlit run app.py`: entrar, carrera con cambio de estado, finalizar, historial.
4. `python cli.py`: la misma carrera por terminal, mismo paquete.
5. `taximetro/` en el editor: un fichero por responsabilidad.

Lo que se corrige está en `04-si-ya-sabes.md`, sección Fase 3. La
fase 4 (base de datos, API, despliegue) es el proyecto siguiente y parte de esto: una lógica que no sabe nada de la
interfaz.
