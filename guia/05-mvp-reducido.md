# MVP reducido

Versión corta del proyecto para quien tiene menos tiempo. Se presenta el jueves 19/11 igual que el resto.

Lo que hay que entregar:

- El taxímetro por terminal (US-01 a US-04). Es la fase 1 del enunciado.
- El mismo taxímetro en el navegador, con botones (US-09), hecho con Streamlit.
- Tu README y el tablero.

Lo demás del enunciado (log, tarifas en fichero, historial, tests, contraseña, clases) queda fuera.

Al final tendrás en tu repositorio `taximetro.py`, `app.py`, `requirements.txt` y tu `README.md`, además de
lo que ya traía el fork.

---

## Parte 1 · Terminal

No hay nada nuevo que explicar aquí, se hace con las guías que ya están en esta carpeta:

1. `00-antes-de-empezar.md`, si no has programado antes. Si ya sabes algo de Python, sáltatela. Si te
   atascas en algún apartado, pregunta en clase.
2. `01-fase1-paso-a-paso.md`, pasos 1 a 8. Respeta los nombres que pide (`AYUDA`, `tarifa`, `cerrar_tramo`,
   `carrera`) porque la parte 2 los usa. El paso 9 déjalo para el final (parte 3 de esta guía).

Antes de pasar a la parte 2, comprueba que la prueba del paso 8 te da la salida que pone la guía.

---

## Parte 2 · Streamlit

Streamlit es una librería de Python para hacer páginas web escribiendo solo Python. Lo que hiciste en la
terminal sigue valiendo, la app va a usar las mismas funciones.

Los pasos van como en la guía 01 (pistas, «Pruébalo», «Si falla») y al acabar cada uno subes los cambios.
Documentación: [API de Streamlit](https://docs.streamlit.io/develop/api-reference).

### Paso A · Instalar Streamlit

Streamlit hay que instalarlo, y se hace dentro de un entorno virtual: una carpeta `.venv` con un Python
propio del proyecto. En la terminal, desde la carpeta del proyecto:

```
python -m venv .venv             # o python3 -m venv .venv
source .venv/bin/activate        # Mac y Linux
.venv\Scripts\activate           # Windows
pip install streamlit
```

Hay que activarlo cada vez que abres una terminal nueva. Sabes que está activo porque la línea empieza por
`(.venv)`.

Crea también `requirements.txt` con esta línea, para que cualquiera pueda instalar lo mismo con
`pip install -r requirements.txt`:

```
streamlit>=1.48
```

Y añade `.venv/` al `.gitignore`, esa carpeta no se sube.

**Pruébalo** con `streamlit hello`. Se abre una demo en el navegador (se cierra con Ctrl+C en la terminal).
`git status` no debe enseñar `.venv/`.

**Si falla:**
- `streamlit: command not found` o `No module named 'streamlit'` → el entorno no estaba activo. Actívalo y
  repite el `pip install`.
- `ensurepip is not available` (Linux) → `sudo apt install python3-venv`, borra `.venv` y repite.
- En Windows, «la ejecución de scripts está deshabilitada» → usa «Command Prompt» en vez de PowerShell (en
  VS Code, la flecha que hay junto al `+` de la terminal).
- No se abre el navegador → copia `http://localhost:8501` de la terminal.
- Te pide un correo la primera vez → Intro sin escribir nada.

### Paso B · Un botón que recuerda

**Al acabar:** `app.py` muestra un título y un botón, y cuenta las veces que lo pulsas.

Streamlit funciona distinto a un programa de terminal:

1. Cada vez que pulsas algo, ejecuta el fichero entero de arriba abajo. `st.button("X")` vale `True` solo
   en la ejecución del clic.
2. Las variables normales se pierden entre un clic y otro. Lo que quieras conservar va en `st.session_state`.
3. No se usa `while True` ni `input`, la página se quedaría colgada.

Crea `app.py` en la carpeta del proyecto y completa lo que falta:

```python
import streamlit as st

st.title("Mi primera app")

if "clics" not in st.session_state:      # solo la primera vez
    st.session_state.clics = 0

if st.button("Púlsame"):
    ...                                  # suma 1 al contador guardado

st.write(f"Veces que me has pulsado: {st.session_state.clics}")
```

Se arranca con `streamlit run app.py`. Déjalo abierto: cuando guardas el fichero, la página te deja recargar
(«Rerun»).

**Pruébalo:** con tres clics sale «Veces que me has pulsado: 3». Si recargas con F5 vuelve a 0.

Prueba también a guardar el contador en una variable normal (`clics = 0`). Verás que no pasa de 1, por lo
que dice el punto 1.

**Si falla:**
- `st.session_state has no attribute "clics"` → lo usas antes de crearlo.
- Siempre dice 1 (o 0) → falta el `if "clics" not in ...` y lo pones a 0 en cada ejecución.
- `python app.py` da un aviso y no abre nada → se arranca con `streamlit run app.py`.

### Paso C · La carrera con botones

**Al acabar:** se puede hacer una carrera completa desde la app (iniciar, parado, en marcha, finalizar) y
empezar otra sin recargar. El cálculo lo sigue haciendo `taximetro.py`.

Borra lo que tenías en `app.py`. Ahora tiene que tener:

- Los `import`: `time`, `streamlit` y tu `cerrar_tramo` (`from taximetro import ...`, como en las pruebas de
  la guía 01).
- `st.set_page_config(page_title="Taxímetro", page_icon="🚕")` y un título.
- La carrera en `st.session_state.carrera`, con los mismos valores que en la terminal: `None` si no hay
  carrera y, si la hay, el diccionario del paso 4 de la guía 01.
- Si no hay carrera, el botón «Iniciar carrera». Cuando acabas de terminar una, encima aparece
  `Última carrera: 0.14 €`.
- Si hay carrera, el estado (`🔴 PARADO` o `🟢 EN MARCHA`), el importe (`0.04 €`), los botones «Parado» y
  «En marcha» uno al lado del otro (el del estado actual, apagado) y el botón «Finalizar carrera».

**Pistas:**
- La carrera se guarda igual que el contador del paso B, pero empieza en `None`.
- Lo que hace cada botón ya lo tienes en las ramas `i`, `p`/`m` y `f` de `main()`. Donde había
  `elif orden == ...` ahora hay `if st.button(...)`. Los `continue` y los `print` no los copies.
- Para crear o vaciar la carrera asigna a `st.session_state.carrera`, no a una variable normal.
- Después de cambiar la carrera llama a `st.rerun()` para que la página se repinte.
- Al finalizar, guarda el total en `st.session_state.ultimo` antes de vaciar la carrera. Se muestra con
  `st.success(...)`, dentro de `if "ultimo" in st.session_state:`.
- Dos botones en fila: `izq, der = st.columns(2)` y después `izq.button(...)` y `der.button(...)`.
- `st.metric("Importe", "0.04 €")` pinta un número grande con su etiqueta. El segundo valor es un texto
  (f-string con `:.2f`). El estado va en otro `st.metric`; el texto lo eliges con un `if`, porque en el
  diccionario pone `"movimiento"` y en pantalla `🟢 EN MARCHA`.
- Un botón apagado es `disabled=True`. En lugar de `True`, pon una comparación con el estado de la carrera.
- Para que ocupen todo el ancho y los de iniciar y finalizar salgan en color:
  `st.button("Iniciar carrera", type="primary", width="stretch")`.

**Pruébalo** con `streamlit run app.py`:

1. Solo aparece «Iniciar carrera». Al pulsarlo salen `🔴 PARADO`, `0.00 €` y los tres botones, con
   «Parado» apagado.
2. Espera 2 s y pulsa «En marcha»: `🟢 EN MARCHA` y `0.04 €`.
3. Espera 2 s y pulsa «Finalizar carrera»: `Última carrera: 0.14 €` y vuelve «Iniciar carrera».
4. Inicia otra. Empieza en `0.00 €`.

De momento el importe solo cambia al pulsar un botón. Eso se arregla en el paso D.

**Si falla:**
- Sale la ayuda del taxímetro en la terminal y la página no carga → en `taximetro.py` faltan las dos líneas
  finales (`if __name__ == "__main__":`).
- Cada clic empieza una carrera nueva → la carrera se crea sin el `if ... not in st.session_state`.
- Pulsas «Iniciar» y no pasa nada → guardas el diccionario en una variable normal.
- `TypeError: 'NoneType' object is not subscriptable` → usas la carrera cuando no la hay. Los botones de la
  carrera van dentro del `else`, y el total se guarda antes de vaciarla.
- `SyntaxError: 'continue' not properly in loop` → se te ha colado un `continue` de la terminal.
- El importe no cuadra al cambiar de estado → cambias el estado antes de llamar a `cerrar_tramo`.
- `StreamlitDuplicateElementId` → dos botones con el mismo texto.

### Paso D · El importe sube solo

**Al acabar:** con una carrera en curso el importe sube cada segundo sin pulsar nada, y los botones siguen
respondiendo. Botones y números se ven grandes.

Hace falta una función nueva en `taximetro.py`, `importe_actual(carrera)`, que devuelve lo que se lleva
cobrado ahora mismo: lo acumulado más el tramo que está abierto. No modifica el diccionario.

Por ejemplo, si el importe es `0.20`, el estado `"movimiento"`, el tramo empezó en `100.0` y el reloj marca
`104.0`, devuelve `0.20 + 4.0 × 0.05 = 0.40`.

En `app.py` se usa un fragmento, que es una función que Streamlit vuelve a ejecutar cada cierto tiempo sin
repintar el resto de la página. Un ejemplo con un reloj:

```python
from datetime import datetime

import streamlit as st

@st.fragment(run_every=1)          # cada segundo
def reloj():
    st.metric("Hora", datetime.now().strftime("%H:%M:%S"))

reloj()                            # se pinta donde la llamas
```

**Pistas:**
- `importe_actual` hace las mismas cuentas que `cerrar_tramo`, pero con `return` y sin guardar nada. Ponla
  entre `cerrar_tramo` y `main`, y añádela al `from taximetro import ...` de `app.py`.
- Lleva las líneas que pintan el estado y el importe a un fragmento sin parámetros. Se define arriba,
  después de crear la carrera en `session_state`, y se llama dentro del `else`.
- Dentro del fragmento lee la carrera de `st.session_state.carrera`. Si no hay carrera, `return` al
  principio (puede ejecutarse justo después de finalizar).
- El importe que se pinta ahora es el que devuelve `importe_actual`.
- Para los botones y números grandes copia esto debajo de `st.set_page_config`. Es CSS, no hace falta
  entenderlo:

  ```python
  st.markdown(
      "<style>div.stButton > button { height: 4.5rem; font-size: 1.6rem; }"
      "[data-testid='stMetricValue'] { font-size: 3rem; }</style>",
      unsafe_allow_html=True,
  )
  ```

**Pruébalo.** Primero la función, con un fichero `prueba_importe.py`:

```python
import time
from taximetro import importe_actual

carrera = {"estado": "movimiento", "desde": time.monotonic() - 4, "importe": 0.20}
print(f"{importe_actual(carrera):.2f}")   # 0.20 + 4 s × 0.05 = 0.40
print(carrera["importe"])                 # sigue en 0.2
```

Tiene que dar `0.40` y `0.2`.

Luego la app. Inicia una carrera y no toques nada: sube 2 céntimos por segundo. En marcha, 5 céntimos por
segundo. Al finalizar, el total es el último importe que viste.

Para verlo en el móvil (en la misma wifi): `streamlit run app.py --server.address 0.0.0.0` y abre en el móvil
la «Network URL» que sale en la terminal.

**Si falla:**
- La prueba da `0.40` y `0.4` → `importe_actual` está cambiando el diccionario.
- `ImportError: cannot import name 'importe_actual'` → el nombre no coincide o no has guardado `taximetro.py`.
- `NameError: name 'importe_actual' is not defined` → falta en el `from taximetro import ...`.
- El importe no sube solo → no está dentro del fragmento, o el fragmento no se llama.
- Al finalizar el total es menor que lo que veías → falta `cerrar_tramo` antes de guardar el total.

---

## Parte 3 · README, tablero y demo

El `README.md` que trae el fork es el enunciado. Renómbralo y escribe el tuyo:

```
git mv README.md ENUNCIADO.md
```

En tu README cuenta qué es el proyecto y qué historias cubre, cómo se arranca (entorno virtual,
`pip install -r requirements.txt`, `python taximetro.py` y `streamlit run app.py`), cómo se usa y cómo se
calcula el importe. Añade las decisiones que has tomado, con el motivo, y qué historias no has hecho.

El tablero es un GitHub Project con las columnas Fase 1, Fase 2, Fase 3, Fase 4 y Hecho, y una tarjeta por
historia (US-01 a US-09) en la columna de su fase. Al entregar, US-01 a US-04 y US-09 están en «Hecho». Si
no te aparece la pestaña Projects, actívala en Settings → General → Features.

Para la demo tienes unos 3 minutos. Enseña una carrera por terminal, una carrera en la app con el importe
subiendo, y el código de `cerrar_tramo` e `importe_actual`. Ensáyala antes.

## Qué se revisa

- La terminal hace lo que pide la guía 01 hasta el paso 8, casos raros incluidos.
- El importe se calcula por tramos con `time.monotonic()`.
- La app hace la carrera completa con botones y el importe sube solo.
- `app.py` usa las funciones de `taximetro.py`, no repite el cálculo.
- Hay `requirements.txt` y `.venv/` no está subido.
- README propio y tablero al día.
- Commits pequeños con Conventional Commits.

## Si te sobra tiempo

- Lista de carreras en la app: guarda en `st.session_state` el importe de cada carrera terminada y enséñalas
  con `st.table`, con el total.
- Mostrar la duración de la carrera.
- Empezar la guía `02-fase2-paso-a-paso.md` (pasos 1 a 3).
