"""
Sistemas Quest 🖥️ · Juego interactivo de Sistemas Informáticos.
Dos unidades: UDI 1 (arquitectura y componentes) y Tema 2 (sistemas operativos).
Ejecutar con:  streamlit run app.py
"""
import math
import random
from types import SimpleNamespace

import streamlit as st

import preguntas as U1M
import preguntas_t2 as T2M

st.set_page_config(page_title="Sistemas Quest", page_icon="🖥️", layout="centered")

# ---------------------------------------------------------------------------
# Configuración del juego
# ---------------------------------------------------------------------------
PUNTOS_CAMPO = 2       # puntos por cada apartado acertado al clasificar/ordenar
BONUS_PERFECTO = 4     # extra si aciertas todo
PUNTOS_PREGUNTA = 5    # puntos por pregunta de opción múltiple / V-F / escrita
TAM_RETO = 15          # preguntas del reto mixto

NIVELES = [
    (0, "Usuario 🙋"),
    (40, "Técnico de aula 🛠️"),
    (120, "Técnico SMR 🧑‍🔧"),
    (250, "Administrador de sistemas 🐧"),
    (400, "Root 👑"),
]

MODOS = [
    "🏠 Inicio",
    "🧩 Clasifica",
    "🧮 Entrenador de cálculos",
    "🔢 Ordena la secuencia",
    "❓ Verdadero o falso",
    "🧠 Quiz de teoría",
    "⚡ Reto mixto",
    "🧪 Laboratorio",
    "📖 Chuleta",
]


def vf_items(mod):
    return [{"enunciado": t, "opciones": ["Verdadero", "Falso"], "correcta": 0 if ok else 1,
             "explicacion": e, "barajar": False} for t, ok, e in mod.VERDADERO_FALSO]


# ---------------------------------------------------------------------------
# Estado y puntuación
# ---------------------------------------------------------------------------
def iniciar_estado():
    for clave, valor in {"puntos": 0, "racha": 0, "mejor_racha": 0, "aciertos": 0, "intentos": 0}.items():
        st.session_state.setdefault(clave, valor)


def nivel_actual():
    nombre = NIVELES[0][1]
    for minimo, titulo in NIVELES:
        if st.session_state.puntos >= minimo:
            nombre = titulo
    return nombre


def siguiente_nivel():
    for minimo, titulo in NIVELES:
        if st.session_state.puntos < minimo:
            return minimo, titulo
    return None


def registrar(aciertos, intentos, puntos, perfecto):
    s = st.session_state
    s.aciertos += aciertos
    s.intentos += intentos
    s.puntos += puntos
    if perfecto:
        s.racha += 1
        s.mejor_racha = max(s.mejor_racha, s.racha)
    else:
        s.racha = 0


def reiniciar_modo(modo):
    for clave in [k for k in st.session_state if k.startswith(f"{modo}_")]:
        del st.session_state[clave]


def preparar_cola(modo, total, limite=None):
    """Crea (una sola vez) el orden aleatorio de preguntas de un modo."""
    if f"{modo}_orden" not in st.session_state:
        orden = list(range(total))
        random.shuffle(orden)
        st.session_state[f"{modo}_orden"] = orden[:limite] if limite else orden
        st.session_state[f"{modo}_pos"] = 0
        st.session_state[f"{modo}_res"] = None
        st.session_state[f"{modo}_ok"] = 0


def avanzar(modo):
    st.session_state[f"{modo}_pos"] += 1
    st.session_state[f"{modo}_res"] = None


def pantalla_final(modo, titulo):
    orden = st.session_state[f"{modo}_orden"]
    ok = st.session_state[f"{modo}_ok"]
    total = len(orden)
    st.success(f"🏁 ¡Completado! Has acertado **{ok} de {total}** en «{titulo}».")
    if ok / total >= 0.8:
        st.balloons()
        st.write("Nota: **Sobresaliente** 🎉")
    elif ok / total >= 0.5:
        st.write("Nota: **Aprobado**, ¡pero puedes mejorarlo! 💪")
    else:
        st.write("Nota: **A repasar** la chuleta 📖 y volver a intentarlo.")
    st.button("🔁 Jugar otra vez", on_click=reiniciar_modo, args=(modo,), key=f"again_{modo}")


def como_lista(valor):
    return list(valor) if isinstance(valor, (list, tuple)) else [valor]


# ---------------------------------------------------------------------------
# Modo: clasificar casos (uno o varios desplegables)
# ---------------------------------------------------------------------------
def modo_clasificador(modo, titulo, descripcion, casos, campos):
    st.caption(f"{descripcion} {PUNTOS_CAMPO} puntos por apartado + {BONUS_PERFECTO} de bonus si aciertas todo.")
    preparar_cola(modo, len(casos))
    pos = st.session_state[f"{modo}_pos"]
    orden = st.session_state[f"{modo}_orden"]
    if pos >= len(orden):
        pantalla_final(modo, titulo)
        return

    idx = orden[pos]
    caso = casos[idx]
    st.progress(pos / len(orden), text=f"Caso {pos + 1} de {len(orden)}")
    st.subheader(caso["titulo"])
    st.info(caso["enunciado"])

    res = st.session_state[f"{modo}_res"]
    if res is None:
        if caso["pista"]:
            with st.expander("💡 Pista"):
                st.write(caso["pista"])
        with st.form(f"form_{modo}_{idx}"):
            elegido = {}
            for clave, campo in campos.items():
                elegido[clave] = st.selectbox(
                    campo["nombre"], campo["opciones"], index=None,
                    placeholder="Elige una opción…", key=f"{modo}_{idx}_{clave}",
                )
            enviar = st.form_submit_button("Comprobar ✅", type="primary")
        if enviar:
            if None in elegido.values():
                st.warning("Responde todos los apartados antes de comprobar.")
            else:
                aciertos = sum(elegido[k] in como_lista(caso["respuesta"][k]) for k in campos)
                perfecto = aciertos == len(campos)
                puntos = aciertos * PUNTOS_CAMPO + (BONUS_PERFECTO if perfecto else 0)
                registrar(aciertos, len(campos), puntos, perfecto)
                st.session_state[f"{modo}_ok"] += 1 if perfecto else 0
                st.session_state[f"{modo}_res"] = {"elegido": elegido, "aciertos": aciertos,
                                                    "puntos": puntos, "perfecto": perfecto}
                st.rerun()
    else:
        if res["perfecto"]:
            st.success(f"🎯 ¡Perfecto! {res['aciertos']}/{len(campos)} · +{res['puntos']} puntos")
        else:
            st.error(f"Has acertado {res['aciertos']}/{len(campos)} · +{res['puntos']} puntos")
        filas = []
        for clave, campo in campos.items():
            correcta = caso["respuesta"][clave]
            tu = res["elegido"][clave]
            filas.append({"Apartado": campo["nombre"], "Tu respuesta": tu,
                          "Correcta": " / ".join(como_lista(correcta)),
                          "": "✅" if tu in como_lista(correcta) else "❌"})
        st.dataframe(filas, hide_index=True)
        st.markdown(f"**Explicación:** {caso['justificacion']}")
        st.button("Siguiente caso ➡️", on_click=avanzar, args=(modo,), type="primary")


def modo_clasifica(U):
    st.header("🧩 Clasifica")
    tema = st.selectbox("Tema", list(U.mod.TEMAS_CLASIF), key=f"sel_{U.pref}_clas_tema")
    modo, casos, campos, desc = U.mod.TEMAS_CLASIF[tema]
    modo_clasificador(modo, tema, desc, casos, campos)


# ---------------------------------------------------------------------------
# Modo: ejercicios con respuesta escrita (o elegida) y generados al azar
# ---------------------------------------------------------------------------
def modo_escrito(modo, titulo, descripcion, crear, selectores=None):
    st.header(titulo)
    st.caption(descripcion)
    if selectores:
        selectores()
    if f"{modo}_items" not in st.session_state:
        items = crear()
        st.session_state[f"{modo}_items"] = items
        st.session_state[f"{modo}_orden"] = list(range(len(items)))
        st.session_state[f"{modo}_pos"] = 0
        st.session_state[f"{modo}_res"] = None
        st.session_state[f"{modo}_ok"] = 0
    items = st.session_state[f"{modo}_items"]
    pos = st.session_state[f"{modo}_pos"]
    if pos >= len(items):
        pantalla_final(modo, titulo)
        return

    item = items[pos]
    st.progress(pos / len(items), text=f"Ejercicio {pos + 1} de {len(items)}")
    st.markdown(f"### {item['enunciado']}")
    res = st.session_state[f"{modo}_res"]
    if res is None:
        if item["pista"]:
            with st.expander("💡 Pista"):
                st.write(item["pista"])
        with st.form(f"form_{modo}_{pos}"):
            if item["opciones"]:
                resp = st.radio("Tu respuesta", item["opciones"], index=None, key=f"{modo}_in_{pos}")
            else:
                resp = st.text_input("Tu respuesta", key=f"{modo}_in_{pos}", placeholder=item["placeholder"])
            enviar = st.form_submit_button("Comprobar ✅", type="primary")
        if enviar:
            if not resp or not resp.strip():
                st.warning("Escribe o elige una respuesta primero.")
            else:
                ok = U1M.comprobar(item, resp)
                registrar(1 if ok else 0, 1, PUNTOS_PREGUNTA if ok else 0, ok)
                st.session_state[f"{modo}_ok"] += 1 if ok else 0
                st.session_state[f"{modo}_res"] = {"resp": resp, "ok": ok}
                st.rerun()
    else:
        if res["ok"]:
            st.success(f"✅ ¡Correcto! +{PUNTOS_PREGUNTA} puntos")
        else:
            st.error(f"❌ Has respondido «{res['resp']}». La correcta era: **{item['canonica']}**")
        st.info(item["explicacion"])
        st.button("Siguiente ➡️", on_click=avanzar, args=(modo,), type="primary")


def modo_calculo(U):
    modo = f"{U.pref}_calc"
    mod = U.mod

    def selectores():
        c1, c2 = st.columns(2)
        c1.selectbox("Tema", list(mod.TEMAS_CALCULO), key=f"sel_{U.pref}_calc_tema",
                     on_change=reiniciar_modo, args=(modo,))
        c2.selectbox("Dificultad", mod.NIVELES_CALC, key=f"sel_{U.pref}_calc_nivel",
                     on_change=reiniciar_modo, args=(modo,))

    def crear():
        tema = st.session_state.get(f"sel_{U.pref}_calc_tema", list(mod.TEMAS_CALCULO)[0])
        nivel = st.session_state.get(f"sel_{U.pref}_calc_nivel", mod.NIVELES_CALC[-1])
        return mod.TEMAS_CALCULO[tema](nivel)

    modo_escrito(modo, "🧮 Entrenador de cálculos",
                 "Ejercicios que se generan al azar: practica todo lo que quieras.", crear, selectores)


# ---------------------------------------------------------------------------
# Modo: ordena la secuencia
# ---------------------------------------------------------------------------
def modo_ordenar(U):
    modo = f"{U.pref}_ord"
    retos = U.mod.ORDENAR
    st.header("🔢 Ordena la secuencia")
    st.caption(f"Pon cada elemento en su posición. {PUNTOS_CAMPO} puntos por posición + {BONUS_PERFECTO} de bonus si aciertas todas.")
    preparar_cola(modo, len(retos))
    pos = st.session_state[f"{modo}_pos"]
    orden = st.session_state[f"{modo}_orden"]
    if pos >= len(orden):
        pantalla_final(modo, "Ordena la secuencia")
        return

    idx = orden[pos]
    reto = retos[idx]
    pasos = reto["pasos"]
    n = len(pasos)
    barajados = list(pasos)
    random.Random(f"{modo}-{idx}").shuffle(barajados)
    st.progress(pos / len(orden), text=f"Reto {pos + 1} de {len(orden)}")
    st.subheader(reto["titulo"])
    st.info(reto["enunciado"])

    res = st.session_state[f"{modo}_res"]
    if res is None:
        with st.form(f"form_{modo}_{idx}"):
            elegido = [st.selectbox(f"Posición {i + 1}", barajados, index=None, placeholder="Elige…",
                                    key=f"{modo}_{idx}_{i}") for i in range(n)]
            enviar = st.form_submit_button("Comprobar ✅", type="primary")
        if enviar:
            if None in elegido:
                st.warning("Rellena todas las posiciones.")
            elif len(set(elegido)) < n:
                st.warning("No repitas elementos: cada uno va en una sola posición.")
            else:
                aciertos = sum(elegido[i] == pasos[i] for i in range(n))
                perfecto = aciertos == n
                puntos = aciertos * PUNTOS_CAMPO + (BONUS_PERFECTO if perfecto else 0)
                registrar(aciertos, n, puntos, perfecto)
                st.session_state[f"{modo}_ok"] += 1 if perfecto else 0
                st.session_state[f"{modo}_res"] = {"elegido": elegido, "aciertos": aciertos,
                                                    "puntos": puntos, "perfecto": perfecto}
                st.rerun()
    else:
        if res["perfecto"]:
            st.success(f"🎯 ¡Orden perfecto! {res['aciertos']}/{n} · +{res['puntos']} puntos")
        else:
            st.error(f"Has colocado bien {res['aciertos']}/{n} · +{res['puntos']} puntos")
        filas = [{"Posición": i + 1, "Tu respuesta": res["elegido"][i], "Correcto": pasos[i],
                  "": "✅" if res["elegido"][i] == pasos[i] else "❌"} for i in range(n)]
        st.dataframe(filas, hide_index=True)
        st.markdown(f"**Explicación:** {reto['explicacion']}")
        st.button("Siguiente reto ➡️", on_click=avanzar, args=(modo,), type="primary")


# ---------------------------------------------------------------------------
# Modo genérico: opción múltiple (V/F, quiz, reto mixto)
# ---------------------------------------------------------------------------
def modo_opciones(modo, titulo, items, limite=None, descripcion="", cabecera=True):
    if cabecera:
        st.header(titulo)
        if descripcion:
            st.caption(descripcion)
    if not items:
        st.info("No hay preguntas en este bloque.")
        return
    preparar_cola(modo, len(items), limite)
    pos = st.session_state[f"{modo}_pos"]
    orden = st.session_state[f"{modo}_orden"]
    if pos >= len(orden):
        pantalla_final(modo, titulo)
        return

    idx = orden[pos]
    item = items[idx]
    st.progress(pos / len(orden), text=f"Pregunta {pos + 1} de {len(orden)}")
    if item.get("bloque") and modo.endswith("_reto"):
        st.caption(f"Bloque: {item['bloque']}")
    st.markdown(f"### {item['enunciado']}")
    opciones = list(item["opciones"])
    texto_correcto = opciones[item["correcta"]]
    if item.get("barajar", True):
        random.Random(f"{modo}-{idx}").shuffle(opciones)

    res = st.session_state[f"{modo}_res"]
    if res is None:
        with st.form(f"form_{modo}_{pos}"):
            eleccion = st.radio("Tu respuesta", opciones, index=None, key=f"{modo}_radio_{pos}")
            enviar = st.form_submit_button("Comprobar ✅", type="primary")
        if enviar:
            if eleccion is None:
                st.warning("Elige una opción primero.")
            else:
                ok = eleccion == texto_correcto
                registrar(1 if ok else 0, 1, PUNTOS_PREGUNTA if ok else 0, ok)
                st.session_state[f"{modo}_ok"] += 1 if ok else 0
                st.session_state[f"{modo}_res"] = {"eleccion": eleccion, "ok": ok}
                st.rerun()
    else:
        if res["ok"]:
            st.success(f"✅ ¡Correcto! +{PUNTOS_PREGUNTA} puntos")
        else:
            st.error(f"❌ Has elegido «{res['eleccion']}». La correcta era: **{texto_correcto}**")
        st.info(item["explicacion"])
        st.button("Siguiente ➡️", on_click=avanzar, args=(modo,), type="primary")


def modo_quiz(U):
    mod = U.mod
    st.header("🧠 Quiz de teoría")
    st.caption("Elige un bloque o juega con todos a la vez.")
    ids = {"Todos los bloques": f"{U.pref}_q0", **{b: f"{U.pref}_q{i + 1}" for i, b in enumerate(mod.BLOQUES)}}
    bloque = st.selectbox("Bloque", list(ids), key=f"sel_{U.pref}_quiz_bloque")
    items = mod.QUIZ if bloque == "Todos los bloques" else [q for q in mod.QUIZ if q["bloque"] == bloque]
    modo_opciones(ids[bloque], f"Quiz · {bloque}", items, cabecera=False)


# ---------------------------------------------------------------------------
# Laboratorio UDI 1
# ---------------------------------------------------------------------------
def lab_conversor():
    c1, c2 = st.columns([2, 1])
    texto = c1.text_input("Número", value="255", key="lab_u1_num")
    base = c2.selectbox("Base de partida", [10, 2, 8, 16], key="lab_u1_base",
                        format_func=lambda b: U1M.NOMBRE_BASE[b].capitalize())
    try:
        n = int(texto.strip().replace(" ", ""), base)
        if n < 0 or n > 2 ** 32:
            raise ValueError
    except ValueError:
        st.warning(f"«{texto}» no es un número válido en base {base} (o es demasiado grande).")
        return
    st.markdown(f"**Decimal:** `{n}` · **Binario:** `{format(n, 'b')}`")
    st.markdown(f"**Octal** (grupos de 3 bits): `{U1M.agrupa(n, 8)}` → `{format(n, 'o')}`")
    st.markdown(f"**Hexadecimal** (grupos de 4 bits): `{U1M.agrupa(n, 16)}` → `{format(n, 'X')}`")


def lab_fuente():
    c1, c2 = st.columns(2)
    cpu = c1.slider("Procesador (W)", 35, 250, 125, key="lab_u1_cpu")
    gpu = c2.slider("Tarjeta gráfica (W)", 0, 600, 300, key="lab_u1_gpu")
    base = cpu + gpu + 75
    total = base * 1.3
    comerciales = [450, 550, 650, 750, 850, 1000, 1200, 1600]
    rec = next((w for w in comerciales if w >= total), None)
    st.markdown(f"**{cpu} + {gpu} + 75 = {base} W** → con un 30 % de margen: **{total:g} W**")
    st.success(f"Fuente recomendada: **{rec} W**" if rec else "Necesitas una fuente de más de 1600 W.")


def lab_paridad():
    d = st.text_input("7 bits de datos", value="1011001", max_chars=7, key="lab_u1_par")
    if len(d) == 7 and set(d) <= {"0", "1"}:
        p = str(d.count("1") % 2)
        st.markdown(f"Tiene **{d.count('1')}** unos → bit de paridad **{p}** → se envía `{d + p}`")
    else:
        st.caption("Escribe exactamente 7 bits (0 y 1).")
    r = st.text_input("Comprobar un byte recibido (8 bits)", value="10110010", max_chars=8, key="lab_u1_par2")
    if len(r) == 8 and set(r) <= {"0", "1"}:
        if r.count("1") % 2 == 0:
            st.success(f"{r.count('1')} unos (par): se da por bueno.")
        else:
            st.error(f"{r.count('1')} unos (impar): ¡hubo un error!")


def lab_ascii():
    t = st.text_input("Escribe un texto", value="CPU", max_chars=20, key="lab_u1_asc")
    filas = []
    for c in t:
        if ord(c) < 128:
            filas.append({"Carácter": c, "Decimal": ord(c), "Hex": format(ord(c), "X"), "Binario": format(ord(c), "08b")})
        else:
            by = c.encode("utf-8")
            filas.append({"Carácter": c, "Decimal": ord(c), "Hex": " ".join(format(b, "X") for b in by),
                          "Binario": f"UTF-8: {len(by)} bytes"})
    if filas:
        st.dataframe(filas, hide_index=True)
        st.caption("Fuera del ASCII (ñ, tildes, emojis) hace falta Unicode (UTF-8): de 1 a 4 bytes por carácter.")


def lab_unidades():
    c1, c2 = st.columns(2)
    v = c1.number_input("Valor", min_value=0.0, value=1.0, step=1.0, key="lab_u1_uv")
    u = c2.selectbox("Unidad", ["bytes", "KB", "MB", "GB", "TB"], index=3, key="lab_u1_uu")
    b = v * {"bytes": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}[u]
    st.markdown(f"- **bits:** {b * 8:,.0f}\n- **bytes:** {b:,.0f}\n- **KB:** {b / 1024:,.4g}\n- **MB:** {b / 1024 ** 2:,.4g}\n"
                f"- **GB:** {b / 1024 ** 3:,.4g}\n- **TB:** {b / 1024 ** 4:,.4g}")
    st.caption("De 1024 en 1024. Un fabricante cuenta de 1000 en 1000: por eso 1 TB «se queda» en unos 931 GB.")


def lab_u1():
    st.header("🧪 Laboratorio")
    st.caption("Experimenta sin puntos con las herramientas de la UDI 1.")
    h = st.radio("Herramienta", ["🔢 Conversor de bases", "🔌 Fuente de alimentación", "✅ Bit de paridad",
                                 "🔤 Tabla ASCII", "📏 Unidades"], horizontal=True, key="sel_u1_lab")
    {"🔢": lab_conversor, "🔌": lab_fuente, "✅": lab_paridad, "🔤": lab_ascii, "📏": lab_unidades}[h[0]]()


# ---------------------------------------------------------------------------
# Laboratorio Tema 2
# ---------------------------------------------------------------------------
def lab_dev():
    c1, c2, c3 = st.columns(3)
    tipo = c1.selectbox("Tipo de disco", ["SATA o USB", "NVMe"], key="lab_t2_tipo")
    d = c2.number_input("Nº de disco (1, 2, 3…)", 1, 8, 2, key="lab_t2_d")
    p = c3.number_input("Nº de partición", 1, 9, 2, key="lab_t2_p")
    if tipo == "SATA o USB":
        logica = st.checkbox("Es una partición lógica (disco MBR): se numera desde el 5", key="lab_t2_log")
        n = p + 4 if logica else p
        disco = f"/dev/sd{chr(96 + d)}"
        st.markdown(f"Disco: `{disco}` · Partición: `{disco}{n}`")
    else:
        disco = f"/dev/nvme{d - 1}n1"
        st.markdown(f"Disco: `{disco}` · Partición: `{disco}p{p}` (los NVMe cuentan desde 0)")
    st.caption(f"En Windows, ese disco se llamaría «Disco {d - 1}» (cuenta desde 0).")


def lab_frag():
    c1, c2, c3 = st.columns(3)
    h1 = c1.slider("Hueco 1 (GB)", 0.0, 2.0, 0.5, 0.1, key="lab_t2_h1")
    h2 = c2.slider("Hueco 2 (GB)", 0.0, 2.0, 0.8, 0.1, key="lab_t2_h2")
    h3 = c3.slider("Hueco 3 (GB)", 0.0, 2.0, 0.8, 0.1, key="lab_t2_h3")
    proc = st.slider("Memoria que necesita el proceso (GB)", 0.1, 4.0, 1.5, 0.1, key="lab_t2_pr")
    total, mayor = round(h1 + h2 + h3, 1), max(h1, h2, h3)
    st.markdown(f"Suman **{total:g} GB** libres; el hueco mayor es **{mayor:g} GB**.")
    if proc <= mayor:
        st.success("✅ El proceso cabe en un hueco.")
    elif proc <= total:
        st.warning("⚠️ No cabe: **fragmentación externa** (hay memoria libre, pero suelta).")
    else:
        st.error("❌ No hay memoria libre suficiente ni sumando los huecos.")


def lab_vm():
    so = st.radio("Sistema invitado", ["Windows 11", "Ubuntu"], horizontal=True, key="lab_t2_so")
    datos = {"Windows 11": ("4 GB", "2", "64 GB", "Obligatorio: EFI + TPM 2.0"),
             "Ubuntu": ("6 GB", "2", "25 GB", "Funciona también como sesión en vivo desde la ISO")}[so]
    st.dataframe([{"RAM": datos[0], "CPU": datos[1], "Disco VDI dinámico": datos[2], "Notas": datos[3]}], hide_index=True)
    st.caption("Valores de la práctica de VirtualBox. Antes, activa Intel VT-x / AMD-V en la UEFI. "
               "Red: NAT (sale a Internet) o adaptador puente (un equipo más de la red).")


def lab_tabla():
    uefi = st.checkbox("El equipo usa UEFI (no solo BIOS)", value=True, key="lab_t2_uefi")
    w11 = st.checkbox("Vas a instalar Windows 11", key="lab_t2_w11")
    grande = st.checkbox("El disco es de más de 2 TB", key="lab_t2_gr")
    motivos = []
    if w11:
        motivos.append("Windows 11 necesita UEFI con GPT.")
    if grande:
        motivos.append("MBR solo llega a 2 TB.")
    if uefi:
        motivos.append("Equipo con UEFI: lo normal es GPT (arranca desde la partición EFI).")
    if w11 or grande or uefi:
        st.success("**GPT**\n\n" + "\n".join(f"- {m}" for m in motivos))
    else:
        st.info("**MBR**: equipo antiguo que solo tiene BIOS y un disco de hasta 2 TB (4 primarias o 3 + extendida).")


def lab_t2():
    st.header("🧪 Laboratorio")
    st.caption("Experimenta sin puntos con las herramientas del Tema 2.")
    h = st.radio("Herramienta", ["💽 Nombres en Linux", "🧱 Fragmentación", "📦 Máquina virtual", "🗂️ ¿MBR o GPT?"],
                 horizontal=True, key="sel_t2_lab")
    {"💽": lab_dev, "🧱": lab_frag, "📦": lab_vm, "🗂": lab_tabla}[h[0]]()


# ---------------------------------------------------------------------------
# Inicio y unidades
# ---------------------------------------------------------------------------
def pantalla_inicio(U):
    st.title("🖥️ Sistemas Quest")
    st.subheader(U.titulo)
    st.write(U.descripcion)
    mod = U.mod
    casos = sum(len(c) for _, c, _, _ in mod.TEMAS_CLASIF.values())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Casos para clasificar", casos)
    c2.metric("Retos de orden", len(mod.ORDENAR))
    c3.metric("Verdadero/falso", len(mod.VERDADERO_FALSO))
    c4.metric("Preguntas de quiz", len(mod.QUIZ))
    st.markdown(U.temas)
    st.info("👈 Elige un modo en el menú de la izquierda para empezar. Puedes cambiar de unidad cuando quieras.")


U1 = SimpleNamespace(
    pref="u1", mod=U1M, lab=lab_u1, titulo="UDI 1 · Arquitectura y componentes de un sistema informático",
    descripcion="Numeración y conversiones, información, arquitectura, hardware por dentro, arranque, software y licencias.",
    temas="""**Temas**
- 🧱 Sistema informático: hardware, software, firmware y personas; las 5 generaciones.
- 🔢 Sistemas de numeración, suma y resta binaria, unidades, ASCII, paridad y formatos.
- 🏛️ Arquitectura Von Neumann y Harvard; unidades funcionales.
- 🔩 Hardware por dentro: placa base, zócalos, procesador, RAM, PCIe, almacenamiento, GPU, conectores y fuente.
- 🚀 El arranque: POST, BIOS/UEFI, gestor de arranque.
- 📜 Software y licencias: libre, propietario, OEM, freeware, shareware.""")
T2 = SimpleNamespace(
    pref="t2", mod=T2M, lab=lab_t2, titulo="Tema 2 · Sistemas operativos",
    descripcion="Qué es un SO, tipos, estructura, funciones, procesos, memoria, E/S, archivos, virtualización, instalación y particiones.",
    temas="""**Temas**
- 🧭 Tipos de SO (los 5 criterios) y estructura: monolítico, THE, MINIX, cliente-servidor.
- ⚙️ Funciones: procesos e hilos, memoria, E/S, archivos y seguridad.
- 📦 Virtualización: hipervisores tipo 1 y 2, contenedores, emulación.
- 💽 Instalación y particiones: MBR y GPT, EFI, nombres en Linux.
- 🚀 Gestores de arranque: Windows Boot Manager y GRUB; cómo repararlos.""")
UNIDADES = {U1.titulo: U1, T2.titulo: T2}


# ---------------------------------------------------------------------------
# Barra lateral y programa principal
# ---------------------------------------------------------------------------
def barra_lateral():
    s = st.session_state
    st.sidebar.title("🖥️ Sistemas Quest")
    unidad = st.sidebar.selectbox("Unidad", list(UNIDADES), key="unidad")
    modo = st.sidebar.radio("Elige modo de juego", MODOS, key="modo_menu")
    st.sidebar.divider()
    st.sidebar.metric("Puntos", s.puntos)
    c1, c2 = st.sidebar.columns(2)
    c1.metric("Racha 🔥", s.racha)
    c2.metric("Mejor racha", s.mejor_racha)
    precision = (s.aciertos / s.intentos * 100) if s.intentos else 0
    st.sidebar.write(f"**Nivel:** {nivel_actual()}")
    st.sidebar.write(f"**Precisión:** {precision:.0f}% ({s.aciertos}/{s.intentos})")
    prox = siguiente_nivel()
    if prox:
        minimo, titulo = prox
        st.sidebar.progress(min(s.puntos / minimo, 1.0))
        st.sidebar.caption(f"Te faltan {minimo - s.puntos} puntos para {titulo}")
    else:
        st.sidebar.caption("¡Nivel máximo alcanzado!")
    if st.sidebar.button("🗑️ Reiniciar todo"):
        st.session_state.clear()
        st.rerun()
    return UNIDADES[unidad], modo


def main():
    iniciar_estado()
    U, modo = barra_lateral()
    if modo == MODOS[0]:
        pantalla_inicio(U)
    elif modo == MODOS[1]:
        modo_clasifica(U)
    elif modo == MODOS[2]:
        modo_calculo(U)
    elif modo == MODOS[3]:
        modo_ordenar(U)
    elif modo == MODOS[4]:
        modo_opciones(f"{U.pref}_vf", "❓ Verdadero o falso", vf_items(U.mod), descripcion="Cuidado con las trampas.")
    elif modo == MODOS[5]:
        modo_quiz(U)
    elif modo == MODOS[6]:
        modo_opciones(f"{U.pref}_reto", "⚡ Reto mixto", U.mod.QUIZ + vf_items(U.mod), limite=TAM_RETO,
                      descripcion=f"{TAM_RETO} preguntas al azar de todos los bloques.")
    elif modo == MODOS[7]:
        U.lab()
    else:
        st.header("📖 Chuleta")
        st.markdown(U.mod.CHULETA)


main()
