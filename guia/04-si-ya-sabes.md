# Si ya sabes programar: lo que tiene que cumplir cada fase y retos extra

Esta página resume **qué tiene que cumplir tu entrega** en cada fase (es lo que se corrige, a todo el mundo) y propone
**retos extra** para cuando acabes antes. Las guías `01` a `03` siguen ahí para cuando te atasques en algo
concreto.

- El diseño descrito (un fichero en las fases 1 y 2; paquete `taximetro/` en la 3) no es la única forma de
  hacerlo, pero es con la que se corrige. Si te apartas, explícalo en el README y cumple igual la lista.
- Los retos extra se hacen **después** de tener la fase entregable, no en vez de.

---

## Fase 1 · MVP por terminal (3 a 10/11)

### Checklist

- [ ] Arranca con `python taximetro.py`, imprime la ayuda y entra en un bucle de órdenes (`i`, `p`, `m`, `f`, `a`, `s`).
- [ ] El importe se calcula **por tramos**: al cambiar de estado se cierra el tramo (`segundos × tarifa`) y se anota el instante. Nada de `sleep` en bucle ni de recalcular desde el inicio.
- [ ] `time.monotonic()` para medir, no `time.time()`.
- [ ] Tarifas 0.02 €/s parado y 0.05 €/s en movimiento, definidas una sola vez.
- [ ] Al finalizar: total con dos decimales y lista para otra carrera sin salir (US-04).
- [ ] Casos raros cubiertos sin traceback: iniciar con carrera en curso, cambiar al estado actual, finalizar o cambiar sin carrera, salir con carrera abierta.
- [ ] README con cómo ejecutarlo (el del enunciado, renómbralo a `ENUNCIADO.md`); tablero con US-01 a US-04 en «Hecho».

### Retos extra

- **Importe en vivo por terminal.** Enseña el importe subiendo mientras el programa espera una orden. Pista: `input()` bloquea; necesitas un hilo (`threading.Thread`) que imprima cada segundo con `\r` y un `threading.Event` para pararlo. Cuidado con mezclar impresiones de dos hilos.
- **Umbral de velocidad.** El enunciado dice «parado o velocidad < 20 km/h». Añade una orden `v <km/h>` que decida el estado a partir de la velocidad. El cálculo por tramos no cambia; solo quién decide el estado.
- **Tarifa mínima y bajada de bandera.** Un importe mínimo por carrera (p. ej. 2,50 €) y un fijo inicial. Piensa dónde va cada cosa para que el cálculo por tramos no cambie.

---

## Fase 2 · Observabilidad y persistencia (10 a 13/11)

### Checklist

- [ ] `logging` a fichero (`taximetro.log`) con fecha, nivel y mensaje: arranque, carrera iniciada, cambio de estado, carrera guardada, cierre; `WARNING` en órdenes desconocidas. `print` para el taxista, `logging` para el técnico.
- [ ] Tarifas en `config.json`; si falta o está mal formado, aviso en el log y tarifas por defecto. Cambiar el JSON y reiniciar cambia el cobro **sin tocar código**.
- [ ] `historial.csv` con cabecera `fecha,hora,duracion_s,importe`, escrito con el módulo `csv`, en modo append, cabecera solo si el fichero es nuevo.
- [ ] Orden `h`: carreras de hoy y total del día, leídas con `csv.DictReader`.
- [ ] El cálculo vive en una función pura `importe_tramo(segundos, estado, tarifas)` (sin reloj, sin ficheros; `ValueError` con segundos negativos).
- [ ] Tests con pytest en un entorno virtual: al menos tres de `importe_tramo` (10 s parado, 10 s en movimiento, segundos negativos) más uno propio; `pytest.approx` para decimales. `python -m pytest` en verde.
- [ ] `.gitignore` con `taximetro.log`, `historial.csv`, `.venv/`, `.pytest_cache/`, `__pycache__/`.
- [ ] README actualizado; tablero con US-05 a US-07 en «Hecho».

### Retos extra

- **Tarifa nocturna.** Entre las 22:00 y las 6:00 las tarifas suben un 20 %. `importe_tramo` sigue siendo pura (recibe la hora o un factor, no mira el reloj), y los tests cubren el cambio de tramo en la frontera de las 22:00. Pista: un tramo que empieza a las 21:59:30 y acaba a las 22:00:30 tiene dos partes.
- **Varias ciudades en `config.json`.** `{"ciudades": {"madrid": {...}, "barcelona": {...}}, "por_defecto": "madrid"}` y una orden de arranque `python taximetro.py --ciudad barcelona` (módulo `argparse`). Los valores por defecto siguen funcionando si falta todo.
- **Rotación del log.** `logging.handlers.RotatingFileHandler` para que `taximetro.log` no crezca sin límite (p. ej. 1 MB, 3 copias). Explica en el README por qué importa en un taxi que lleva meses encendido.
- **Tests de las funciones de fichero.** `guardar_carrera` y `carreras_de_hoy` con `tmp_path`: cabecera una sola vez tras dos guardados; filtro por fecha (escribe una fila de ayer a mano y comprueba que no sale). Y uno que compruebe que `cargar_tarifas` ignora claves extra del JSON.
- **Historial por fecha.** `h 2026-11-10` lista las carreras de ese día; `h` a secas, las de hoy. Validación de la fecha con `datetime.strptime` y mensaje claro si está mal.

---

## Fase 3 · Arquitectura y Streamlit (16 a 18/11; la app puede empezar el 11)

### Checklist

- [ ] Paquete `taximetro/` con un módulo por responsabilidad: `registro` (log), `tarifas` (`Tarifas` + `cargar`), `historial` (`Historial`), `carrera` (`Carrera`, `Resumen`, `CarreraError`), `auth`. `taximetro.py` pasa a llamarse `cli.py` (un fichero y una carpeta `taximetro` no pueden convivir). `cli.py` y `app.py` fuera del paquete, **sin lógica propia**: `grep -n "monotonic\|por_estado\|csv.writer\|DictReader\|pbkdf2\|json.loads" cli.py app.py` no devuelve nada.
- [ ] `Carrera`: `iniciar(estado="parado")`, `cambiar_estado(nuevo)`, `importe_actual()`, `duracion()`, `finalizar() -> Resumen`, propiedad `en_curso`; operaciones imposibles lanzan `CarreraError` (no imprimen). Encadena carreras con la misma instancia.
- [ ] `Resumen` y `Tarifas` son `@dataclass(frozen=True)`; método `tarifas.por_estado(estado)`; `cargar` devuelve `Tarifas()` si el JSON falla.
- [ ] `Historial(ruta)` con `guardar(resumen)`, `leer()`, `de_hoy()`, `total(filas)` estático.
- [ ] Reloj inyectable: `Carrera(tarifas, reloj=time.monotonic)` y tests con un reloj falso (paso 5 de la guía 03): **ningún `sleep` en los tests**.
- [ ] `registro.configurar()` con su propio `FileHandler` sobre el logger `"taximetro"` (no `basicConfig`: solo funciona si nadie ha configurado el log antes, y con Streamlit no lo controlas).
- [ ] `auth.py`: `crear_contrasena`, `hay_contrasena`, `verificar`; PBKDF2-HMAC-SHA256 con sal aleatoria (`os.urandom` o `secrets`) y comparación con `hmac.compare_digest`; `python -m taximetro.auth` crea `credenciales.json`; la contraseña no aparece en el fichero (hay un test que lo afirma). Fichero en `.gitignore`.
- [ ] `app.py`: `st.set_page_config` primero; acceso con `st.form` + `st.stop()` que deja `session_state.autenticado`; `Carrera` en `st.session_state`; contador en `st.fragment(..., run_every=1)` (nunca `while`/`sleep`/`st.rerun` en bucle); botones grandes (CSS), el del estado actual deshabilitado; «Finalizar» guarda en `Historial` y en `session_state.ultimo`; historial de hoy en un `st.expander`; botón «Salir» que limpia `session_state`.
- [ ] Tests en `tests/`, 14 en verde con `python -m pytest` (9 de `Carrera`, 3 de tarifas/historial, 2 de auth; los de los pasos 4, 5 y 6 de la guía 03 se pueden copiar). `requirements.txt`. README con estructura, arranque y **decisiones técnicas justificadas**. Tablero con una columna por fase, US-08 y US-09 en «Hecho».

### Retos extra

- **Tests de la app con `AppTest`.** Streamlit trae `streamlit.testing.v1.AppTest` para ejecutar `app.py` sin navegador: escribir la contraseña, pulsar botones y leer las métricas. Un ejemplo para `tests/test_app.py`, pensado para una app que cumple la checklist (ajusta los textos a los de la tuya):

  ```python
  from pathlib import Path

  from streamlit.testing.v1 import AppTest

  from taximetro import auth

  APP = Path(__file__).resolve().parent.parent / "app.py"


  def test_la_app_pide_contrasena_y_arranca_una_carrera(tmp_path, monkeypatch):
      monkeypatch.chdir(tmp_path)                 # historial y credenciales en una carpeta temporal
      auth.crear_contrasena("taxi1234")
      at = AppTest.from_file(str(APP)).run()
      at.text_input[0].input("taxi1234")
      at.button[0].click().run()
      assert at.session_state.autenticado
      at.button[0].click().run()                  # Iniciar carrera
      assert at.metric[0].value == "🔴 PARADO"
      assert not at.exception
  ```

  Reto: añadir el cambio a «En marcha» (busca el botón por `label`) y el «Finalizar» comprobando que `historial.csv` aparece en `tmp_path`.

- **Type hints en todo el paquete** (`def iniciar(self, estado: str = "parado") -> None`, `Callable[[], float]` para el reloj, `list[dict[str, str]]` para las filas del historial) y pasarlo por `mypy` o `pyright` sin errores. Añade el comando al README.
- **Exportar el historial a Excel.** Orden `x` en el CLI y botón en la app que generen `historial.xlsx` con `openpyxl` (cabecera en negrita, columna de importe con formato `0.00 €`, una fila de total). Que viva en `Historial.exportar(ruta)`, no en las interfaces.
- **Tarifa nocturna y varias ciudades, ahora con clases.** Si los hiciste en la fase 2, pásalos al diseño nuevo: `Tarifas` con un método `vigentes(cuando: datetime)` o una clase `Tarificador` que `Carrera` reciba inyectada, igual que el reloj. Los tests no deben depender de la hora real (inyecta también el `datetime`).
- **Estado del taxi persistente.** Si la app se cierra con una carrera abierta, al volver a abrirla la carrera sigue (guarda el estado en un JSON al cambiar y recupéralo al arrancar). Piensa qué reloj usas para que el tiempo cerrado también cuente: `monotonic` no sirve entre procesos.
- **Varias instancias / varios taxis.** `Carrera` por matrícula en `session_state` y un selector arriba; `historial.csv` con columna `taxi`. Es el paso previo natural a la base de datos de la fase 4.
- **Empaquetado.** Un `pyproject.toml` que permita `pip install -e .` y una entrada de consola `taximetro` que lance `cli.main()`. Y un `Dockerfile` que arranque la app: te adelantas a la fase 4.
- **Calidad.** `ruff` (lint + formato) y un `pre-commit` que lo ejecute; un workflow de GitHub Actions que corra `python -m pytest` en cada push. Que el badge verde esté en el README el día de la demo.

---

## Qué se mira al corregir, sea cual sea tu nivel

1. Que funcione lo que pide cada historia, probándolo en la demo, no leyendo el código.
2. Que el cálculo viva en **un solo sitio** y las interfaces no lo repitan.
3. Que los tests existan, pasen y no esperen (sin `sleep`).
4. Que no haya secretos ni datos en el repositorio (`credenciales.json`, log, CSV, `.venv`).
5. Que el README explique cómo arrancar y **por qué** se decidió cada cosa.
6. Que sepas explicar en la defensa cualquier línea de tu código y por qué la escribiste así.
7. Commits pequeños en formato Conventional Commits; tablero al día.
