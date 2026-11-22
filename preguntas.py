"""
preguntas.py
Contenido y generadores de la UDI 1 · Arquitectura y componentes de un sistema informático
(SISTEMAS 6). Para añadir contenido basta con copiar un elemento de la lista correspondiente.
"""
import random
import re

HEXD = "0123456789ABCDEF"
SUB = {2: "₂", 8: "₈", 10: "₁₀", 16: "₁₆"}
NOMBRE_BASE = {2: "binario", 8: "octal", 10: "decimal", 16: "hexadecimal"}
NIVELES_CALC = ["Fácil (0-63)", "Normal (0-255)"]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def num_en(n, base):
    return {2: format(n, "b"), 8: format(n, "o"), 10: str(n), 16: format(n, "X")}[base]


def con_base(n, base):
    return f"{num_en(n, base)}{SUB[base]}"


def agrupa(n, base):
    """Bits de n agrupados de 3 (octal) o de 4 (hexadecimal) desde la derecha."""
    s = format(n, "b")
    size = {8: 3, 16: 4}.get(base)
    if not size:
        return s
    s = s.zfill(-(-len(s) // size) * size)
    return " ".join(s[i:i + size] for i in range(0, len(s), size))


def pasos_div(n, base):
    partes, cifras, x = [], [], n
    while x > 0:
        c, r = divmod(x, base)
        extra = f" ({HEXD[r]})" if base == 16 and r > 9 else ""
        partes.append(f"{x} ÷ {base} = {c} resto {r}{extra}")
        cifras.append(HEXD[r])
        x = c
    return " · ".join(partes) + f" → restos de abajo arriba: **{''.join(reversed(cifras))}**"


def pasos_pos(n, base):
    s = num_en(n, base)
    terminos = [f"{int(c, 16)}×{base ** (len(s) - 1 - i)}" for i, c in enumerate(s)]
    valores = [int(c, 16) * base ** (len(s) - 1 - i) for i, c in enumerate(s)]
    return f"{' + '.join(terminos)} = {' + '.join(map(str, valores))} = **{n}**"


def comprobar(item, texto):
    """Comprueba una respuesta escrita (o elegida) contra un ejercicio."""
    t = (texto or "").strip()
    if not t:
        return False
    tipo = item["tipo"]
    if tipo == "numero":
        base = item["base"]
        t = re.sub(r"[\s|_]", "", t.lower())
        for pref in {2: ("0b",), 8: ("0o",), 16: ("0x", "#")}.get(base, ()):
            if t.startswith(pref):
                t = t[len(pref):]
                break
        try:
            return int(t, base) == item["valor"]
        except ValueError:
            return False
    if tipo == "decimal":
        try:
            return abs(float(t.replace(",", ".").replace(" ", "")) - item["valor"]) < 1e-6
        except ValueError:
            return False
    t = t.lower().replace(" ", "")
    return t in [a.lower().replace(" ", "") for a in item["aceptadas"]]


def _item(enunciado, tipo, canonica, explicacion, pista="", valor=None, base=None,
          aceptadas=None, opciones=None, placeholder="Escribe tu respuesta…"):
    return {"enunciado": enunciado, "tipo": tipo, "canonica": canonica, "explicacion": explicacion,
            "pista": pista, "valor": valor, "base": base, "aceptadas": aceptadas or [],
            "opciones": opciones, "placeholder": placeholder}


def _c(titulo, enunciado, respuesta, justificacion, pista=""):
    return {"titulo": titulo, "enunciado": enunciado, "respuesta": respuesta,
            "justificacion": justificacion, "pista": pista}


def _q(bloque, enunciado, correcta, incorrectas, explicacion):
    """Pregunta de test. La correcta se escribe primero; el juego baraja las opciones."""
    return {"bloque": bloque, "enunciado": enunciado, "opciones": [correcta] + list(incorrectas),
            "correcta": 0, "explicacion": explicacion}


# ---------------------------------------------------------------------------
# Cambios de base
# ---------------------------------------------------------------------------
def g_dec2base(n, base):
    return _item(f"Pasa **{n}₁₀** a base {base} ({NOMBRE_BASE[base]}).", "numero", num_en(n, base),
                 pasos_div(n, base),
                 f"Divide entre {base} y lee los restos de abajo arriba." +
                 (" Si un resto es 10 o más, se escribe con letra (A-F)." if base == 16 else ""),
                 valor=n, base=base, placeholder="Escribe el resultado")


def g_base2dec(n, base):
    return _item(f"Pasa **{con_base(n, base)}** a decimal.", "numero", str(n), pasos_pos(n, base),
                 "Multiplica cada cifra por su peso (potencia de la base) y suma." +
                 (" Recuerda: A=10 … F=15." if base == 16 else ""),
                 valor=n, base=10, placeholder="Escribe el resultado")


def g_atajo(n, b1, b2):
    return _item(f"Pasa **{con_base(n, b1)}** a {NOMBRE_BASE[b2]} (usa el atajo por binario).", "numero",
                 num_en(n, b2),
                 f"{num_en(n, b1)} → {agrupa(n, b1)} → {agrupa(n, b2)} → **{num_en(n, b2)}**",
                 "1 cifra octal = 3 bits · 1 cifra hexadecimal = 4 bits.", valor=n, base=b2,
                 placeholder="Escribe el resultado")


def gen_bases(nivel, tipo="mezcla", cantidad=10):
    maximo = 63 if nivel.startswith("Fácil") else 255
    items = []
    for n in random.sample(range(2, maximo + 1), cantidad):
        t = tipo if tipo != "mezcla" else random.choice(["dec", "base", "atajo"])
        if t == "dec":
            items.append(g_dec2base(n, random.choice([2, 8, 16])))
        elif t == "base":
            items.append(g_base2dec(n, random.choice([2, 8, 16])))
        else:
            items.append(g_atajo(n, *random.choice([(2, 8), (2, 16), (8, 2), (16, 2), (8, 16), (16, 8)])))
    return items


# ---------------------------------------------------------------------------
# Suma y resta en binario
# ---------------------------------------------------------------------------
def gen_sumas(nivel, cantidad=10):
    w = 4 if nivel.startswith("Fácil") else 6
    items = []
    for i in range(cantidad):
        a, b = random.randint(1, 2 ** w - 1), random.randint(1, 2 ** w - 1)
        if i % 2:
            a, b = max(a, b), min(a, b)
            op, res = "−", a - b
            pista = "0 − 1 = 1 y pido 1 prestado a la columna de la izquierda."
        else:
            op, res = "+", a + b
            pista = "1 + 1 = 0 y me llevo 1 · 1 + 1 + 1 = 1 y me llevo 1."
        items.append(_item(f"Calcula en binario: **{format(a, f'0{w}b')} {op} {format(b, f'0{w}b')}**",
                           "numero", format(res, "b"),
                           f"Compruébalo en decimal: {a} {op} {b} = {res} → **{format(res, 'b')}**.",
                           pista, valor=res, base=2, placeholder="Escribe el resultado en binario"))
    return items


# ---------------------------------------------------------------------------
# Unidades de medida
# ---------------------------------------------------------------------------
def gen_unidades(nivel=None, cantidad=10):
    plantillas = []
    n = random.randint(2, 20)
    plantillas.append(_item(f"¿Cuántos bits hay en **{n} bytes**?", "decimal", str(n * 8),
                            f"{n} × 8 = **{n * 8}** bits.", "1 byte = 8 bits.", valor=n * 8))
    g = random.randint(2, 16)
    plantillas.append(_item(f"¿Cuántos MB son **{g} GB**?", "decimal", str(g * 1024),
                            f"{g} × 1024 = **{g * 1024}** MB.", "Cada escalón vale 1024.", valor=g * 1024))
    m = random.choice([256, 512, 768, 1024, 1536, 2048])
    plantillas.append(_item(f"¿Cuántos GB son **{m} MB**?", "decimal", f"{m / 1024:g}",
                            f"{m} ÷ 1024 = **{m / 1024:g}** GB.", "Divide entre 1024 (puede salir con decimales).",
                            valor=m / 1024))
    mb = random.randint(2, 12)
    plantillas.append(_item(f"¿Cuántos KB son **{mb} MB**?", "decimal", str(mb * 1024),
                            f"{mb} × 1024 = **{mb * 1024}** KB.", "1 MB = 1024 KB.", valor=mb * 1024))
    foto, pen = random.choice([2, 4, 8]), random.choice([8, 16, 32, 64])
    plantillas.append(_item(f"Una foto ocupa **{foto} MB**. ¿Cuántas caben en un pendrive de **{pen} GB**?",
                            "decimal", str(pen * 1024 // foto),
                            f"{pen} × 1024 ÷ {foto} = **{pen * 1024 // foto}** fotos.",
                            "Pasa primero los GB a MB.", valor=pen * 1024 // foto))
    fibra = random.choice([80, 160, 200, 300, 400, 600, 800, 1000])
    plantillas.append(_item(f"Tu fibra es de **{fibra} Mb** por segundo. ¿Cuántos **MB** descarga cada segundo?",
                            "decimal", f"{fibra / 8:g}", f"{fibra} ÷ 8 = **{fibra / 8:g}** MB/s.",
                            "Mb (bits) → MB (bytes): divide entre 8.", valor=fibra / 8))
    tb = random.choice([1, 2, 4])
    plantillas.append(_item(f"¿Cuántos GB son **{tb} TB** contando de 1024 en 1024?", "decimal", str(tb * 1024),
                            f"{tb} × 1024 = **{tb * 1024}** GB (el fabricante cuenta de 1000 en 1000).",
                            "1 TB = 1024 GB.", valor=tb * 1024))
    random.shuffle(plantillas)
    return (plantillas * 2)[:cantidad]


# ---------------------------------------------------------------------------
# ASCII
# ---------------------------------------------------------------------------
PALABRAS = ["SMR", "BIT", "CPU", "RAM", "USB", "SSD", "GPU", "PC", "ROM", "BIOS", "UEFI", "BYTE", "DISCO", "LINUX"]
PISTA_ASCII = "A = 41, B = 42, C = 43 … J = 4A … Z = 5A (en hexadecimal). A = 65 en decimal."
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gen_ascii(nivel=None, cantidad=10):
    items = []
    for i in range(cantidad):
        t = i % 5
        if t == 0:
            c = random.choice(ABC)
            items.append(_item(f"¿Cuál es el código ASCII de la letra **{c}** en hexadecimal?", "numero",
                               format(ord(c), "X"), f"{c} = {ord(c)} en decimal = **{format(ord(c), 'X')}** en hexadecimal.",
                               PISTA_ASCII, valor=ord(c), base=16, placeholder="p. ej. 41"))
        elif t == 1:
            c = random.choice(ABC)
            items.append(_item(f"¿Qué letra es el código **{format(ord(c), 'X')}**?", "texto", c,
                               f"{format(ord(c), 'X')}₁₆ = {ord(c)} → la letra **{c}**.", PISTA_ASCII, aceptadas=[c]))
        elif t == 2:
            w = random.choice(PALABRAS)
            cod = " ".join(format(ord(x), "X") for x in w)
            items.append(_item(f"Descifra este mensaje: **{cod}**", "texto", w,
                               " · ".join(f"{format(ord(x), 'X')} → {x}" for x in w), PISTA_ASCII, aceptadas=[w]))
        elif t == 3:
            w = random.choice(["PC", "RAM", "BIT", "SSD", "ROM"])
            cod = " ".join(format(ord(x), "08b") for x in w)
            items.append(_item(f"Descifra este mensaje en binario: **{cod}**", "texto", w,
                               " · ".join(f"{format(ord(x), '08b')} → {x}" for x in w), PISTA_ASCII, aceptadas=[w]))
        else:
            w = random.choice(["CPU", "RAM", "USB", "GPU", "PC"])
            cod = " ".join(format(ord(x), "X") for x in w)
            items.append(_item(f"Escribe **{w}** en hexadecimal (un código por letra).", "texto", cod,
                               " · ".join(f"{x} → {format(ord(x), 'X')}" for x in w), PISTA_ASCII,
                               aceptadas=[cod], placeholder="p. ej. 43 50 55"))
    random.shuffle(items)
    return items


# ---------------------------------------------------------------------------
# Bit de paridad (paridad par)
# ---------------------------------------------------------------------------
def gen_paridad(nivel=None, cantidad=10):
    items = []
    for i in range(cantidad):
        if i % 2 == 0:
            d = format(random.randint(1, 127), "07b")
            p = str(d.count("1") % 2)
            items.append(_item(f"Añade el bit de paridad (paridad par) al final de **{d}**.", "numero", d + p,
                               f"{d.count('1')} unos → {'par: se añade un 0' if p == '0' else 'impar: se añade un 1'} → **{d + p}**.",
                               "El total de unos debe quedar par.", valor=int(d + p, 2), base=2,
                               placeholder="Escribe los 8 bits"))
        else:
            d = format(random.randint(1, 255), "08b")
            hay = d.count("1") % 2 == 1
            op = ["No, se da por bueno", "Sí, hay un error"]
            items.append(_item(f"Con paridad par, llega **{d}**. ¿Hay error?", "texto", op[1] if hay else op[0],
                               f"Tiene {d.count('1')} unos ({'impar' if hay else 'par'}) → "
                               f"{'hay un error' if hay else 'se da por bueno'}.",
                               "Cuenta los unos: si son impares, hubo un error.",
                               aceptadas=[op[1] if hay else op[0]], opciones=op))
    return items


# ---------------------------------------------------------------------------
# Potencia de la fuente
# ---------------------------------------------------------------------------
def gen_fuente(nivel=None, cantidad=8):
    items = []
    pares = [(c, g) for c in (65, 95, 105, 125, 170) for g in (0, 150, 200, 250, 300, 350, 450)]
    for cpu, gpu in random.sample(pares, cantidad):
        base = cpu + gpu + 75
        total = base * 1.3
        items.append(_item(f"Un PC tiene un procesador de **{cpu} W** y una gráfica de **{gpu} W**. "
                           f"¿Qué potencia mínima (en W) necesita la fuente, contando 75 W para el resto y un 30 % de margen?",
                           "decimal", f"{total:g}", f"{cpu} + {gpu} + 75 = {base} W → × 1,3 (30 % de margen) = **{total:g} W**.",
                           "Procesador + gráfica + 75 W, y un 30 % de margen.", valor=total,
                           placeholder="Potencia en W"))
    return items


TEMAS_CALCULO = {
    "Mezcla de cambios de base": lambda n: gen_bases(n, "mezcla"),
    "Decimal → binario, octal o hexadecimal": lambda n: gen_bases(n, "dec"),
    "Binario, octal o hexadecimal → decimal": lambda n: gen_bases(n, "base"),
    "Atajo por binario (octal ⇄ hexadecimal ⇄ binario)": lambda n: gen_bases(n, "atajo"),
    "Suma y resta en binario": gen_sumas,
    "Unidades de medida": gen_unidades,
    "ASCII: mensajes secretos": gen_ascii,
    "Bit de paridad": gen_paridad,
    "Potencia de la fuente": gen_fuente,
}


# ---------------------------------------------------------------------------
# Clasificar: varios temas con desplegables
# ---------------------------------------------------------------------------
HW, SO, APP, FW, PER = "Hardware", "Software (sistema operativo)", "Software (aplicación)", "Firmware", "Persona"
CAMPOS_HSFP = {"tipo": {"nombre": "Tipo de elemento", "opciones": [HW, SO, APP, FW, PER]}}
CASOS_HSFP = [
    _c("💾 Un disco SSD", "Un disco SSD.", {"tipo": HW}, "Es una pieza física y tangible.", "¿Se puede tocar?"),
    _c("🔧 La UEFI", "La UEFI de la placa base.", {"tipo": FW}, "Software grabado en un chip de la placa; hace arrancar el equipo."),
    _c("📝 LibreOffice Writer", "LibreOffice Writer.", {"tipo": APP}, "Programa que usamos para una tarea concreta (ofimática)."),
    _c("🧑‍💻 El administrador", "El administrador de sistemas.", {"tipo": PER}, "Quienes usan, administran o desarrollan el sistema son personas."),
    _c("🐧 Ubuntu Linux", "Ubuntu Linux.", {"tipo": SO}, "Gestiona el hardware, la memoria, los archivos y los programas."),
    _c("📶 Router", "El programa interno de un router wifi.", {"tipo": FW}, "Software grabado dentro de un dispositivo."),
    _c("⌨️ El teclado", "El teclado.", {"tipo": HW}, "Hardware de entrada."),
    _c("🙋 Tú", "Tú, usando el ordenador.", {"tipo": PER}, "Eres el usuario: la parte «personas» del sistema."),
    _c("🪟 Windows 11", "Windows 11.", {"tipo": SO}, "Sistema operativo."),
    _c("🌐 Firefox", "El navegador Firefox.", {"tipo": APP}, "Aplicación para navegar por Internet."),
    _c("🖨️ Impresora", "El programa de la impresora que gestiona la cola de impresión.", {"tipo": FW}, "Firmware: software dentro del hardware."),
    _c("🧠 La RAM", "Un módulo de memoria RAM.", {"tipo": HW}, "Pieza física."),
    _c("👩‍💻 Programadora", "Una programadora que desarrolla el sistema.", {"tipo": PER}, "Personas: usuarios, técnicos y programadores."),
    _c("🎮 Mando", "El programa interno del mando de una videoconsola.", {"tipo": FW}, "Firmware."),
    _c("📱 Android", "Android.", {"tipo": SO}, "Sistema operativo de los móviles."),
    _c("🍞 Microondas", "El programa de control de un microondas.", {"tipo": FW}, "Firmware de un electrodoméstico."),
]

UF = ["Entrada", "Salida", "Entrada y salida", "Memoria principal (RAM)", "Memoria externa (SSD)", "ALU", "Unidad de control"]
CAMPOS_UF = {"unidad": {"nombre": "Unidad funcional", "opciones": UF}}
CASOS_UF = [
    _c("📷 Webcam", "Una webcam.", {"unidad": UF[0]}, "Recibe datos: es de entrada."),
    _c("🔊 Altavoces", "Unos altavoces.", {"unidad": UF[1]}, "Devuelven resultados: salida."),
    _c("📱 Pantalla táctil", "Una pantalla táctil.", {"unidad": UF[2]}, "Muestra (salida) y recibe pulsaciones (entrada)."),
    _c("🔌 Pendrive", "Un pendrive USB.", {"unidad": UF[4]}, "Guarda datos de forma permanente: memoria externa."),
    _c("➕ Calcular 7 + 5", "Calcular 7 + 5 dentro de la CPU.", {"unidad": UF[5]}, "La ALU hace operaciones aritméticas y lógicas."),
    _c("🧭 Siguiente instrucción", "Decidir cuál es la siguiente instrucción.", {"unidad": UF[6]}, "La unidad de control coordina al resto."),
    _c("🌐 Navegador abierto", "Guardar el navegador mientras lo usas.", {"unidad": UF[3]}, "La RAM guarda los programas en ejecución y sus datos."),
    _c("🖱️ Ratón", "Un ratón.", {"unidad": UF[0]}, "Entrada."),
    _c("🖨️ Impresora", "Una impresora (solo imprime).", {"unidad": UF[1]}, "Salida."),
    _c("🌍 Tarjeta de red", "Una tarjeta de red.", {"unidad": UF[2]}, "Envía y recibe datos: entrada y salida."),
    _c("🎤 Micrófono", "Un micrófono.", {"unidad": UF[0]}, "Entrada."),
    _c("💽 Disco SSD", "Un disco SSD donde se guardan tus archivos.", {"unidad": UF[4]}, "Memoria externa."),
]

LIC = ["Libre (GPL)", "Propietaria de pago", "OEM", "Por volumen", "Freeware", "Shareware o de prueba"]
CAMPOS_LIC = {"lic": {"nombre": "Tipo de licencia", "opciones": LIC},
              "libre": {"nombre": "¿Libre o propietario?", "opciones": ["Software libre", "Software propietario"]}}
L, P = "Software libre", "Software propietario"
CASOS_LIC = [
    _c("🐧 Ubuntu", "Ubuntu.", {"lic": LIC[0], "libre": L}, "Linux es libre (GPL)."),
    _c("💻 Windows del portátil", "El Windows 11 que venía en tu portátil.", {"lic": LIC[2], "libre": P}, "Viene con el equipo nuevo y solo vale para ese equipo: OEM."),
    _c("🗜️ WinRAR", "WinRAR.", {"lic": LIC[5], "libre": P}, "Se prueba un tiempo y después se paga: shareware."),
    _c("🎬 VLC", "VLC.", {"lic": LIC[0], "libre": L}, "Libre (GPL)."),
    _c("🌐 Chrome", "Google Chrome.", {"lic": LIC[4], "libre": P}, "Gratis, pero con el código cerrado: freeware."),
    _c("📊 Microsoft 365", "Microsoft 365.", {"lic": LIC[1], "libre": P}, "De pago, por suscripción."),
    _c("📝 LibreOffice", "LibreOffice.", {"lic": LIC[0], "libre": L}, "Libre (GPL)."),
    _c("📄 Acrobat Reader", "Adobe Acrobat Reader.", {"lic": LIC[4], "libre": P}, "Gratis, con el código cerrado: freeware."),
    _c("🏫 Windows de las aulas", "El Windows de los ordenadores de las aulas.", {"lic": LIC[3], "libre": P}, "Una clave para muchos equipos de un centro: por volumen."),
    _c("🦊 Firefox", "Firefox.", {"lic": LIC[0], "libre": L}, "Libre."),
    _c("🎨 Photoshop", "Photoshop.", {"lic": LIC[1], "libre": P}, "De pago y código cerrado."),
]

PIEZAS = ["Placa base", "Procesador (CPU)", "Memoria RAM", "Almacenamiento", "Tarjeta gráfica (GPU)",
          "Fuente de alimentación", "Chipset", "Refrigeración"]
CAMPOS_PIE = {"pieza": {"nombre": "Pieza", "opciones": PIEZAS}}
CASOS_PIE = [
    _c("🏙️ El plano de la ciudad", "Une todas las piezas; sus pistas son los buses.", {"pieza": PIEZAS[0]}, "Placa base."),
    _c("🧮 Unidad de control y ALU", "Contiene la unidad de control, la ALU y los registros.", {"pieza": PIEZAS[1]}, "Es el procesador."),
    _c("📋 Lo que se está usando", "Guarda lo que se está usando; se borra al apagar.", {"pieza": PIEZAS[2]}, "RAM: es volátil."),
    _c("🗄️ Conserva los datos", "HDD, SSD o NVMe: conserva los datos sin corriente.", {"pieza": PIEZAS[3]}, "Almacenamiento."),
    _c("🔌 Del enchufe a la PC", "Convierte los 230 V del enchufe en 12 V, 5 V y 3,3 V.", {"pieza": PIEZAS[5]}, "Fuente de alimentación."),
    _c("🖼️ La imagen del monitor", "Genera la imagen que se envía al monitor.", {"pieza": PIEZAS[4]}, "GPU."),
    _c("🚦 Semáforos y rotondas", "Chip de la placa que gestiona USB, SATA, red y audio.", {"pieza": PIEZAS[6]}, "Chipset (antes puente sur)."),
    _c("❄️ Sacar el calor", "Disipador, ventilador y pasta térmica.", {"pieza": PIEZAS[7]}, "Refrigeración."),
    _c("🧱 Miles de núcleos", "Miles de núcleos sencillos que hacen la misma operación sobre muchos datos.", {"pieza": PIEZAS[4]}, "GPU."),
    _c("🧊 Pila CR2032", "Lleva la pila CR2032 y el chip de la UEFI.", {"pieza": PIEZAS[0]}, "Placa base."),
    _c("⚡ Caché L1, L2 y L3", "Lleva dentro caché L1, L2 y L3 y núcleos e hilos.", {"pieza": PIEZAS[1]}, "Procesador."),
    _c("💨 Dual Channel", "Va en ranuras DIMM; 2 módulos en A2 y B2.", {"pieza": PIEZAS[2]}, "Memoria RAM."),
]

USOS = ["La placa base", "El procesador", "La tarjeta gráfica", "Discos duros y SSD SATA",
        "SSD NVMe", "Red por cable", "Red, sonido o Wi-Fi (tarjetas pequeñas)", "Borrar la configuración de la UEFI"]
CAMPOS_CON = {"uso": {"nombre": "¿Para qué sirve?", "opciones": USOS}}
CASOS_CON = [
    _c("🔋 ATX 24 pines", "Conector ATX de 24 pines.", {"uso": USOS[0]}, "Alimenta la placa base."),
    _c("🧠 EPS 8 pines", "Conector EPS de 8 pines (4+4).", {"uso": USOS[1]}, "Alimenta el procesador. No es igual que el PCIe de 8 pines."),
    _c("🎮 PCIe 6+2", "Conector PCIe de 6+2 pines.", {"uso": USOS[2]}, "Alimenta la gráfica (150 W cada uno)."),
    _c("⚡ 12V-2x6", "Conector 12V-2x6 de 16 pines.", {"uso": USOS[2]}, "Para gráficas actuales (hasta 600 W)."),
    _c("💽 SATA de corriente", "Conector SATA de corriente.", {"uso": USOS[3]}, "Alimenta discos duros y SSD SATA."),
    _c("🛣️ Ranura x16", "Ranura PCIe x16.", {"uso": USOS[2]}, "Es la ranura de la tarjeta gráfica."),
    _c("🛣️ Ranura x4 / M.2", "Ranura M.2 (PCIe x4).", {"uso": USOS[4]}, "SSD NVMe."),
    _c("🌐 RJ-45", "Conector RJ-45.", {"uso": USOS[5]}, "Ethernet, 1 o 2,5 Gb/s."),
    _c("🛣️ Ranura x1", "Ranura PCIe x1.", {"uso": USOS[6]}, "Red, sonido y Wi-Fi."),
    _c("🔘 Clear CMOS", "Botón Clear CMOS del panel trasero.", {"uso": USOS[7]}, "Borra la configuración de la UEFI."),
]

FASES = ["1 · Encendido y firmware", "2 · POST", "3 · Dispositivo de arranque", "4 · Gestor de arranque", "5-6 · Carga del sistema"]
REVIS = ["Enchufe, interruptor de la fuente y cable del botón", "RAM mal encajada, gráfica o LED de diagnóstico",
         "Orden de arranque y disco conectado con sistema", "Reparar el gestor desde un USB de instalación",
         "Arrancar en modo seguro y revisar el controlador", "Cambiar la pila CR2032"]
CAMPOS_ARR = {"fase": {"nombre": "¿En qué fase se ha parado?", "opciones": FASES},
              "revisar": {"nombre": "¿Qué revisas?", "opciones": REVIS}}
CASOS_ARR = [
    _c("🌑 No hace nada", "No hace nada: ni luces ni ventiladores.", {"fase": FASES[0], "revisar": REVIS[0]}, "Fase 1: falta energía (enchufe, fuente, cable F_PANEL)."),
    _c("🔊 Pitidos", "Los ventiladores giran, no hay imagen y suenan pitidos.", {"fase": FASES[1], "revisar": REVIS[1]}, "Fase 2 (POST): suele ser la RAM o la gráfica."),
    _c("🚫 No bootable device", "Aparece «No bootable device».", {"fase": FASES[2], "revisar": REVIS[2]}, "Fase 3: no encuentra un disco arrancable."),
    _c("🆘 grub rescue", "Aparece «grub rescue>».", {"fase": FASES[3], "revisar": REVIS[3]}, "Fase 4: el gestor de arranque está dañado."),
    _c("💙 Pantalla azul", "Pantalla azul o «kernel panic» al cargar.", {"fase": FASES[4], "revisar": REVIS[4]}, "Fases 5-6: controlador o actualización reciente."),
    _c("🕰️ Hora desajustada", "La hora se desajusta al desenchufar el equipo.", {"fase": FASES[0], "revisar": REVIS[5]}, "Firmware: pila CR2032 agotada."),
    _c("💡 LED DRAM", "Se queda encendido el LED de diagnóstico «DRAM».", {"fase": FASES[1], "revisar": REVIS[1]}, "POST: indica qué pieza falla (aquí, la memoria)."),
    _c("💽 Reboot and select", "«Reboot and select proper boot device».", {"fase": FASES[2], "revisar": REVIS[2]}, "Fase 3: orden de arranque, disco o USB olvidado."),
]

TEMAS_CLASIF = {
    "Hardware, software, firmware o persona": ("u1_hsfp", CASOS_HSFP, CAMPOS_HSFP, "Clasifica cada elemento de un sistema informático."),
    "Unidad funcional": ("u1_uf", CASOS_UF, CAMPOS_UF, "¿Qué unidad funcional es?"),
    "¿Qué licencia tiene?": ("u1_lic", CASOS_LIC, CAMPOS_LIC, "Tipo de licencia y si es libre o propietario."),
    "Pieza del ordenador": ("u1_pie", CASOS_PIE, CAMPOS_PIE, "Adivina la pieza por lo que hace."),
    "Conectores y ranuras": ("u1_con", CASOS_CON, CAMPOS_CON, "¿Para qué sirve cada conector?"),
    "Diagnostica el arranque": ("u1_arr", CASOS_ARR, CAMPOS_ARR, "Fase del arranque donde falla y qué revisar."),
}


# ---------------------------------------------------------------------------
# Ordena la secuencia (el orden de la lista ES el correcto)
# ---------------------------------------------------------------------------
ORDENAR = [
    {"titulo": "🚀 El arranque, paso a paso",
     "enunciado": "Ordena las 7 fases desde que pulsas el botón hasta que puedes usar el equipo.",
     "pasos": ["Encendido y firmware (UEFI)", "POST (autocomprobación)", "Búsqueda del dispositivo de arranque",
               "Gestor de arranque (GRUB o Windows Boot Manager)", "Carga del kernel en la RAM",
               "Inicio del sistema (drivers, memoria y servicios)", "Inicio de sesión"],
     "explicacion": "Cada etapa prepara la siguiente: es el bootstrap."},
    {"titulo": "🔁 El ciclo de la CPU",
     "enunciado": "Ordena los 4 pasos que repite la CPU millones de veces por segundo.",
     "pasos": ["Buscar la instrucción (unidad de control)", "Decodificar la operación", "Ejecutar el cálculo (ALU)",
               "Guardar el resultado en memoria"],
     "explicacion": "Al terminar el paso 4, la CPU busca la siguiente instrucción."},
    {"titulo": "🔥 El camino del calor",
     "enunciado": "Ordena desde donde se genera el calor hasta donde sale al aire.",
     "pasos": ["Silicio (die)", "IHS (tapa metálica del procesador)", "Pasta térmica", "Disipador", "Ventilador"],
     "explicacion": "La pasta térmica rellena los microhuecos entre el IHS y el disipador."},
    {"titulo": "🥞 La pila completa",
     "enunciado": "Ordena de abajo arriba los niveles de un sistema informático.",
     "pasos": ["Hardware", "Firmware", "Sistema operativo", "Aplicaciones", "Personas"],
     "explicacion": "Hardware → Firmware → Sistema operativo → Aplicaciones → Personas."},
    {"titulo": "📜 Cinco generaciones",
     "enunciado": "Ordena las generaciones de ordenadores según su tecnología.",
     "pasos": ["Válvulas de vacío (ENIAC)", "Transistores", "Circuitos integrados", "Microprocesador (ordenador personal)",
               "Redes, nube e IA"],
     "explicacion": "1ª 1940–1956 · 2ª 1956–1964 · 3ª 1964–1971 · 4ª 1971–hoy · 5ª hoy."},
    {"titulo": "🛣️ Evolución de las ranuras",
     "enunciado": "Ordena las ranuras y buses por año de aparición.",
     "pasos": ["ISA (1981)", "PCI (1992)", "AGP (1997)", "PCIe (2003)", "M.2 (2013)"],
     "explicacion": "ISA 1981 → PCI 1992 → AGP 1997 → PCIe 2003 → M.2 2013."},
    {"titulo": "💾 Velocidad del almacenamiento",
     "enunciado": "Ordena de menor a mayor velocidad de lectura aproximada.",
     "pasos": ["Disco duro HDD (≈ 200 MB/s)", "SSD SATA (≈ 550 MB/s)", "SSD NVMe PCIe 4.0 (≈ 7.000 MB/s)",
               "SSD NVMe PCIe 5.0 (≈ 14.000 MB/s)"],
     "explicacion": "El SATA limita a unos 550 MB/s; el NVMe usa carriles PCIe."},
    {"titulo": "🏅 Certificación 80 PLUS",
     "enunciado": "Ordena de menor a mayor eficiencia.",
     "pasos": ["Estándar (80 %)", "Bronze (85 %)", "Silver (88 %)", "Gold (90 %)", "Platinum (92 %)", "Titanium (94 %)"],
     "explicacion": "Cuanto más alta, menos energía se pierde como calor."},
    {"titulo": "📏 Unidades de medida",
     "enunciado": "Ordena de menor a mayor.",
     "pasos": ["bit", "byte (8 bits)", "KB (1024 bytes)", "MB (1024 KB)", "GB (1024 MB)", "TB (1024 GB)"],
     "explicacion": "A partir del byte, cada escalón es 1024 veces el anterior."},
    {"titulo": "📐 Formatos de placa base",
     "enunciado": "Ordena de mayor a menor tamaño.",
     "pasos": ["E-ATX (305 × 330 mm)", "ATX (305 × 244 mm)", "Micro-ATX (244 × 244 mm)", "Mini-ITX (170 × 170 mm)"],
     "explicacion": "Cuanto más pequeña, menos ranuras PCIe: 7, 7, 4 y 1."},
    {"titulo": "🐧 Arranque de Linux",
     "enunciado": "Ordena las etapas del arranque de Linux.",
     "pasos": ["GRUB", "Kernel (vmlinuz)", "systemd (proceso 1)", "Servicios", "Inicio de sesión"],
     "explicacion": "systemd es el primer proceso: de él nacen todos los demás."},
]


# ---------------------------------------------------------------------------
# Verdadero o falso
# ---------------------------------------------------------------------------
VERDADERO_FALSO = [
    ("Un sistema informático tiene hardware, software y personas.", True, "Los tres componentes no funcionan el uno sin el otro."),
    ("El firmware es software grabado dentro de un componente de hardware.", True, "Por ejemplo, la BIOS/UEFI o el programa de un router."),
    ("El firmware nunca se puede actualizar.", False, "Se puede, pero con cuidado: un fallo puede dejar el dispositivo inservible."),
    ("La 2ª generación de ordenadores usaba válvulas de vacío.", False, "Eran los transistores; las válvulas son de la 1ª generación."),
    ("En el sistema octal existe el dígito 8.", False, "Octal usa del 0 al 7."),
    ("En hexadecimal, la F vale 15.", True, "A=10, B=11, C=12, D=13, E=14, F=15."),
    ("11111111 en binario es 255.", True, "Es el número más grande que cabe en 1 byte."),
    ("Para pasar de decimal a binario se leen los restos de arriba abajo.", False, "Se leen de abajo arriba."),
    ("Un número par en binario acaba siempre en 0.", True, "Par → el resto de la última división es 0."),
    ("Una cifra octal equivale a 4 bits.", False, "Una cifra octal son 3 bits; la hexadecimal son 4."),
    ("83 en decimal es 123 en octal.", True, "83 ÷ 8 = 10 r 3 · 10 ÷ 8 = 1 r 2 · 1 → 123."),
    ("254 en decimal es FE en hexadecimal.", True, "254 ÷ 16 = 15 (F) y sobran 14 (E)."),
    ("En binario, 1 + 1 = 10: se escribe 0 y me llevo 1.", True, "Es una de las cuatro reglas de la suma."),
    ("1011 + 0110 = 10001 en binario.", True, "11 + 6 = 17."),
    ("Un byte son 8 bits.", True, "Un bit es un 0 o un 1."),
    ("1 GB son 1000 MB para Windows.", False, "Windows cuenta de 1024 en 1024; el fabricante, de 1000 en 1000."),
    ("MB con B mayúscula son bytes y Mb con b minúscula, bits.", True, "Mb se usa para velocidades; MB, para tamaños."),
    ("El ASCII estándar usa 7 bits y 128 caracteres.", True, "No tiene ñ ni tildes."),
    ("Unicode (UTF-8) usa de 1 a 4 bytes por carácter.", True, "Una sola tabla para todos los idiomas y los emojis."),
    ("El bit de paridad permite corregir un error.", False, "Solo lo detecta; no sabe qué bit ha fallado."),
    ("Si cambian dos bits a la vez, la paridad lo detecta siempre.", False, "No se entera."),
    ("PNG, FLAC y ZIP son formatos sin pérdida.", True, "JPG, MP3 y MP4 son con pérdida."),
    ("La arquitectura Von Neumann usa una sola memoria para instrucciones y datos.", True, "Y un bus compartido."),
    ("La arquitectura Harvard tiene memorias separadas, cada una con su bus.", True, "Permite acceder a ambas a la vez."),
    ("El cuello de botella de Von Neumann se debe al bus compartido.", True, "Todo pasa por el mismo bus y la memoria puede frenar a la CPU."),
    ("Un PC actual usa sobre todo la arquitectura Harvard pura.", False, "Usa sobre todo Von Neumann, con ideas de Harvard."),
    ("La unidad de control hace los cálculos aritméticos.", False, "Los hace la ALU; la unidad de control coordina."),
    ("Un zócalo LGA tiene los pines en la placa base.", True, "Es el tipo actual en Intel y en AMD AM5."),
    ("Un procesador BGA se puede cambiar fácilmente.", False, "Va soldado: portátiles, miniPC, consolas y Raspberry Pi."),
    ("Un Ryzen 9000 va en un zócalo AM4.", False, "Los Ryzen 7000 y 9000 usan AM5."),
    ("El TDP indica el calor que hay que sacar.", True, "Decide la refrigeración."),
    ("La pasta térmica se pone en abundancia, cuanta más mejor.", False, "Una capa fina, del tamaño de un guisante."),
    ("Un módulo DDR4 encaja en una placa DDR5.", False, "Tienen muescas distintas."),
    ("En Dual Channel, 2 × 8 GB rinde más que 1 × 16 GB.", True, "Con 2 módulos se colocan en A2 y B2."),
    ("La RAM conserva los datos al apagar.", False, "Es volátil."),
    ("El puente norte se ha integrado dentro del procesador.", True, "En la placa queda un solo chip: el chipset."),
    ("Una tarjeta PCIe x16 funciona en una ranura x1.", False, "Una tarjeta pequeña funciona en una ranura grande, pero no al revés."),
    ("Un SSD M.2 siempre es NVMe.", False, "Hay SSD M.2 que son SATA por dentro."),
    ("El monitor se conecta a la tarjeta gráfica dedicada, no al HDMI de la placa.", True, "Si lo conectas a la placa, lo normal es no ver nada."),
    ("Todos los conectores USB-C tienen la misma velocidad.", False, "La forma no dice la velocidad."),
    ("El conector EPS de 8 pines y el PCIe de 8 pines son iguales.", False, "Nunca fuerces un conector."),
    ("Una fuente 80 PLUS Titanium tiene una eficiencia del 94 %.", True, "Estándar 80 · Bronze 85 · Silver 88 · Gold 90 · Platinum 92 · Titanium 94."),
    ("Para elegir la fuente se suma procesador + gráfica + 75 W y se añade un 30 % de margen.", True, "125 + 300 + 75 = 500 → fuente de 650 W."),
    ("Al encender, la CPU ejecuta primero el sistema operativo.", False, "Ejecuta primero el firmware (UEFI)."),
    ("El POST comprueba CPU, memoria y dispositivos.", True, "Si falla, hay pitidos, LED o un código en un display."),
    ("La BIOS clásica usa discos GPT y Secure Boot.", False, "Eso es UEFI; la BIOS usa MBR (máx. 2 TB) y no tiene seguridad."),
    ("TPM 2.0 es obligatorio para Windows 11.", True, "Guarda claves de cifrado."),
    ("El MBR ocupa 512 bytes y termina en 55 AA.", True, "446 bytes de código + 64 de particiones + 2 de firma."),
    ("GRUB es el gestor de arranque estándar de Linux.", True, "Permite elegir sistema o versión del kernel."),
    ("systemd es el primer proceso en Linux.", True, "El proceso 1, del que nacen todos los demás."),
    ("«No bootable device» indica un problema en la fase del POST.", False, "Es la fase 3: dispositivo de arranque."),
    ("Si el reloj se atrasa al desenchufar el equipo, hay que cambiar la pila CR2032.", True, "Mantiene la hora y la configuración."),
    ("El software libre es siempre gratis.", False, "Libre no significa gratis."),
    ("El software libre respeta 4 libertades: usar, estudiar, copiar y repartir, mejorar y publicar.", True, "Numeradas del 0 al 3."),
    ("Chrome es freeware: gratis, pero con el código cerrado.", True, "Igual que Acrobat Reader."),
    ("Una licencia OEM sirve para instalar el programa en cualquier equipo.", False, "Solo vale para el equipo con el que vino."),
]


# ---------------------------------------------------------------------------
# Quiz de teoría
# ---------------------------------------------------------------------------
BLOQUES = ["Sistema informático e historia", "Sistemas de numeración", "Más sobre la información",
           "Arquitectura del ordenador", "Hardware por dentro", "El arranque", "Software y licencias"]
B0, B1, B2, B3, B4, B5, B6 = BLOQUES
QUIZ = [
    _q(B0, "¿Cuáles son los tres componentes de un sistema informático?", "Hardware, software y personas",
       ["Hardware, firmware y red", "Procesador, memoria y disco", "Sistema operativo, aplicaciones y drivers"],
       "Un sistema informático almacena y procesa información; sus tres componentes no funcionan el uno sin el otro."),
    _q(B0, "¿Qué es el firmware?", "Software grabado dentro de un componente de hardware",
       ["Un programa que instala el usuario", "La parte física de la placa", "Un tipo de memoria RAM"],
       "Permite que el dispositivo arranque, funcione y se comunique con programas más complejos."),
    _q(B0, "¿Cuál es el ejemplo más conocido de firmware?", "La BIOS o su sucesora, la UEFI",
       ["Microsoft Word", "El teclado", "Un pendrive"], "Está en la placa base del ordenador."),
    _q(B0, "Un fallo durante la actualización del firmware puede…", "dejar el dispositivo inservible",
       ["borrar la RAM", "acelerar el equipo", "no tener ningún efecto"], "Por eso se actualiza con cuidado."),
    _q(B0, "¿Qué tecnología define la 1ª generación de ordenadores (1940–1956)?", "Válvulas de vacío",
       ["Transistores", "Circuitos integrados", "Microprocesador"], "El ENIAC ocupaba una sala entera."),
    _q(B0, "¿Qué generación se caracteriza por los transistores?", "La 2ª (1956–1964)", ["La 1ª", "La 3ª", "La 4ª"],
       "Eran más pequeños y fiables."),
    _q(B0, "¿Cuándo nace el ordenador personal?", "En la 4ª generación, con el microprocesador",
       ["En la 1ª, con las válvulas", "En la 2ª, con los transistores", "En la 5ª, con la IA"], "1971–hoy."),
    _q(B0, "Los primeros sistemas operativos modernos aparecen con…", "los circuitos integrados (3ª generación)",
       ["las válvulas de vacío", "los transistores", "la nube"], "1964–1971."),
    _q(B0, "Un técnico o un programador dentro de un sistema informático son…", "personas",
       ["hardware", "firmware", "software"], "Personas: usuarios, técnicos y programadores."),
    _q(B1, "¿Cuántos símbolos distintos usa el sistema octal?", "8 (del 0 al 7)", ["7", "9 (del 0 al 8)", "10"],
       "En base 8 no existe el dígito 8."),
    _q(B1, "¿Cuántos símbolos usa el hexadecimal?", "16 (0-9 y A-F)", ["15", "10", "8"], "Se usan letras para el 10-15."),
    _q(B1, "¿Dónde se ven los permisos de archivos en Linux?", "En octal", ["En binario puro", "En hexadecimal", "En decimal"],
       "Por ejemplo, 755."),
    _q(B1, "¿Dónde verás el hexadecimal?", "Colores web, direcciones MAC y memoria",
       ["Permisos de Linux", "La vida cotidiana", "Solo en el disco duro"], "Octal: permisos de Linux."),
    _q(B1, "¿Cuál es el número más grande que cabe en 8 bits?", "255 (11111111)", ["256", "128", "127"],
       "Por eso los colores RGB van de 0 a 255 en cada canal."),
    _q(B1, "¿Cómo se pasa de decimal a binario con divisiones?", "Dividiendo entre 2 y leyendo los restos de abajo arriba",
       ["Dividiendo entre 2 y leyendo los restos de arriba abajo", "Multiplicando por 2", "Dividiendo entre 10"],
       "Con el 13: correcto 1101; al revés sale 1011 (el 11)."),
    _q(B1, "¿Qué valor tiene la letra F en hexadecimal?", "15", ["16", "14", "6"], "A es la 1ª letra → 10; F la 6ª → 15."),
    _q(B1, "¿Cómo se pasa de octal a decimal?", "Multiplicando cada cifra por su potencia de 8 y sumando",
       ["Dividiendo entre 8", "Dividiendo entre 10", "Agrupando en 4 bits"], "Pesos: 1, 8, 64, 512…"),
    _q(B1, "¿Cuántos bits corresponden a una cifra octal?", "3", ["2", "4", "8"], "Hexadecimal: 4 bits."),
    _q(B1, "¿Cuántos bits corresponden a una cifra hexadecimal?", "4", ["3", "2", "8"], "Octal: 3 bits."),
    _q(B1, "¿Cuánto es 347₈ en decimal?", "231", ["227", "247", "347"], "3×64 + 4×8 + 7 = 192 + 32 + 7."),
    _q(B1, "¿Cuánto es 2F₁₆ en decimal?", "47", ["37", "57", "215"], "2×16 + 15 = 47."),
    _q(B1, "¿Cómo se escribe 83₁₀ en octal?", "123₈", ["321₈", "103₈", "83₈"], "Leer los restos de arriba abajo daría 321: mal."),
    _q(B1, "¿Cuánto es 254₁₀ en hexadecimal?", "FE", ["EF", "FF", "E4"], "254 ÷ 16 = 15 (F) y sobran 14 (E)."),
    _q(B1, "¿Cuánto es 200₁₀ en hexadecimal?", "C8", ["8C", "C0", "B8"], "200 ÷ 16 = 12 (C) y sobran 8."),
    _q(B1, "¿Cuánto es 100₁₀ en octal?", "144₈", ["441₈", "124₈", "100₈"], "100÷8 = 12 r4 · 12÷8 = 1 r4 · 1÷8 = 0 r1."),
    _q(B1, "Para pasar de binario a hexadecimal, agrupas los bits…", "de 4 en 4 desde la derecha",
       ["de 3 en 3", "de 2 en 2", "de 8 en 8"], "1101 0110 → D6."),
    _q(B1, "¿Cuánto es 3C₁₆ en octal (pasando por binario)?", "74₈", ["64₈", "47₈", "30₈"], "0011 1100 → 111 100 → 7 4."),
    _q(B2, "En binario, 1 + 1 es…", "0 y me llevo 1", ["2", "1", "11 sin llevada"], "Con llevada: 1 + 1 + 1 = 1 y me llevo 1."),
    _q(B2, "¿Cuánto es 1011 + 0110 en binario?", "10001", ["10000", "1111", "10101"], "11 + 6 = 17."),
    _q(B2, "En una resta binaria, 0 − 1 se resuelve…", "pidiendo 1 prestado a la columna de la izquierda",
       ["dando 0", "dando −1", "sumando 1"], "Como en decimal."),
    _q(B2, "A partir del byte, cada escalón (KB, MB, GB…) es… veces el anterior", "1024", ["1000", "8", "100"],
       "1 KB = 1024 bytes → 1 MB = 1024 KB → 1 GB = 1024 MB → 1 TB = 1024 GB."),
    _q(B2, "¿Por qué un disco de 1 TB muestra unos 931 GB en Windows?",
       "El fabricante cuenta de 1000 en 1000 y Windows de 1024 en 1024",
       ["Se pierde espacio al formatear siempre", "Windows ocupa 69 GB", "Es un error del disco"], "Son dos formas de contar."),
    _q(B2, "¿Qué indica «MB» con B mayúscula?", "Bytes (tamaño)", ["Bits (velocidad)", "Megabaudios", "Mil bytes"],
       "Con b minúscula (Mb) son bits, y se usa para velocidades."),
    _q(B2, "Una fibra de 300 Mb/s descarga como máximo…", "37,5 MB por segundo", ["300 MB/s", "2.400 MB/s", "3,75 MB/s"], "300 ÷ 8."),
    _q(B2, "¿Cuántos bits usa el ASCII estándar?", "7 bits (128 caracteres)", ["8 bits (256)", "16 bits", "32 bits"],
       "El ASCII extendido usa 8 bits (256)."),
    _q(B2, "¿Qué estándar actual sirve para todos los idiomas y emojis?", "Unicode (UTF-8)", ["ASCII", "ASCII extendido", "BCD"],
       "De 1 a 4 bytes por carácter."),
    _q(B2, "La letra A en ASCII es…", "65 en decimal y 41 en hexadecimal", ["97 en decimal y 61 en hexadecimal", "41 en decimal", "1 en decimal"],
       "En binario: 0100 0001."),
    _q(B2, "El bit de paridad par se calcula para que…", "el número total de unos sea par",
       ["el total de ceros sea par", "el número sea múltiplo de 8", "haya más unos que ceros"], "Si al llegar es impar, hubo un error."),
    _q(B2, "¿Qué NO puede hacer el bit de paridad?", "Corregir el error: no sabe qué bit ha fallado",
       ["Detectar un cambio de un solo bit", "Contar los unos", "Añadirse a 7 bits de datos"], "Y si cambian dos bits, no se entera."),
    _q(B2, "¿Dónde se usa la paridad?", "RAM de servidores, discos en RAID y comunicaciones",
       ["Solo en pantallas", "En el teclado", "En impresoras"], "Detecta errores."),
    _q(B2, "¿Qué formato es sin pérdida?", "PNG", ["JPG", "MP3", "MP4"], "También FLAC y ZIP."),
    _q(B2, "¿Qué formato de imagen es vectorial (un dibujo, no una rejilla de píxeles)?", ".svg", [".jpg", ".png", ".mp3"],
       "Las imágenes normales son rejillas de píxeles."),
    _q(B2, "La extensión de un archivo indica…", "con qué programa abrirlo", ["cuánto pesa", "qué ordenador lo creó", "su contraseña"],
       "El formato dice cómo interpretar los bits."),
    _q(B3, "La arquitectura Von Neumann usa…", "una única memoria para instrucciones y datos",
       ["dos memorias separadas", "solo registros", "ninguna memoria"], "Y un bus compartido (direcciones, datos y control)."),
    _q(B3, "El cuello de botella de Von Neumann se debe a…", "un bus compartido por el que pasa todo",
       ["la falta de ALU", "el disco duro", "el ventilador"], "La memoria puede frenar a la CPU."),
    _q(B3, "¿Qué arquitectura separa la memoria de instrucciones y la de datos?", "Harvard", ["Von Neumann", "Turing", "Dual Channel"],
       "Cada una tiene su propio bus."),
    _q(B3, "La arquitectura Harvard se usa hoy en…", "microcontroladores (Arduino) y procesadores de señal (DSP)",
       ["PC y portátiles", "servidores web", "pantallas"], "Es más rápida, pero más compleja y cara."),
    _q(B3, "¿Cuál es el orden del ciclo de la CPU?", "Buscar, decodificar, ejecutar, guardar",
       ["Ejecutar, buscar, guardar, decodificar", "Guardar, buscar, ejecutar, decodificar", "Decodificar, guardar, buscar, ejecutar"],
       "Y vuelta a empezar."),
    _q(B3, "¿Quién hace los cálculos en el ciclo?", "La ALU", ["La unidad de control", "La RAM", "El chipset"], "Usa los registros."),
    _q(B3, "¿Qué unidad coordina al resto de componentes?", "La unidad de control", ["La ALU", "Los registros", "La memoria externa"],
       "También busca las instrucciones."),
    _q(B3, "La memoria HBM…", "apila chips de RAM junto al procesador con conexiones muy anchas",
       ["es un disco duro", "es la caché L1", "va dentro de la fuente"], "Los datos recorren menos distancia."),
    _q(B3, "¿Por qué la HBM encarece la RAM, según la noticia?", "Consume mucho más silicio y deja menos memoria para PC y móviles",
       ["Es gratis de fabricar", "Solo la usan los móviles", "Porque es más lenta"], "El cuello de botella de Von Neumann a escala gigante."),
    _q(B3, "Las puertas lógicas trabajan con dos estados…", "0 (tensión baja) y 1 (tensión alta)",
       ["frío y calor", "luz y sonido", "positivo y negativo"], "Por eso empezamos por el binario."),
    _q(B3, "¿Qué unidad funcional guarda los programas en ejecución y sus datos?", "La memoria principal (RAM)",
       ["La ALU", "La memoria externa (SSD)", "La unidad de control"], "La memoria externa guarda de forma permanente."),
    _q(B4, "¿Qué es la placa base?", "Un circuito impreso (PCB) que interconecta todos los componentes",
       ["Un tipo de memoria", "La carcasa del PC", "El programa que arranca el PC"], "Con varias capas de pistas de cobre."),
    _q(B4, "¿Cuál es el formato de placa más pequeño de la tabla?", "Mini-ITX (170 × 170 mm)", ["ATX", "Micro-ATX", "E-ATX"],
       "Solo tiene 1 ranura PCIe."),
    _q(B4, "¿Qué formato de placa es típico de sobremesa?", "ATX (305 × 244 mm)", ["E-ATX", "Micro-ATX", "Mini-ITX"],
       "E-ATX: workstation · Micro-ATX: oficina."),
    _q(B4, "Un zócalo LGA tiene los pines en…", "la placa base", ["el procesador", "la RAM", "la fuente"],
       "En PGA (como AM4), los pines están en el procesador."),
    _q(B4, "Un procesador soldado a la placa (portátiles, Raspberry Pi) es…", "BGA", ["LGA", "PGA", "ZIF"], "No se puede cambiar."),
    _q(B4, "Un zócalo LGA1700 admite…", "Core de 12ª, 13ª y 14ª generación",
       ["Ryzen 7000 y 9000", "Ryzen 1000 a 5000", "Core Ultra 200S"], "LGA1851: Core Ultra 200S."),
    _q(B4, "Un Ryzen 9000 va en el zócalo…", "AM5", ["AM4", "LGA1700", "LGA1851"], "AM5 es LGA; AM4 era PGA."),
    _q(B4, "La «regla de oro» del zócalo es…", "La placa fija el zócalo y el zócalo fija qué procesadores puedes montar",
       ["Cualquier CPU va en cualquier placa", "El zócalo lo decide la fuente", "El zócalo lo decide la RAM"],
       "El chipset y la UEFI también tienen que admitirlo."),
    _q(B4, "¿Qué indica la frecuencia en GHz?", "Los ciclos por segundo (5 GHz = 5.000 millones)", ["Los núcleos", "La caché", "Los vatios"],
       "No es lo mismo que el número de núcleos."),
    _q(B4, "¿Qué indica el TDP?", "El calor (en W) que hay que sacar; decide la refrigeración",
       ["La velocidad de la RAM", "El número de hilos", "El voltaje de la fuente"], "Ej.: 65 W."),
    _q(B4, "La caché L1, L2 y L3 es…", "memoria pequeña y rapidísima dentro del chip", ["un tipo de disco", "la memoria de la gráfica", "el chipset"],
       "La L3 se comparte entre núcleos."),
    _q(B4, "Un Ryzen 7 9700X tiene…", "8 núcleos y 16 hilos", ["16 núcleos y 8 hilos", "8 núcleos y 8 hilos", "4 núcleos y 8 hilos"],
       "Hasta 5,5 GHz, 32 MB de caché L3 y 65 W."),
    _q(B4, "¿Cuánta pasta térmica se pone?", "Una capa fina, del tamaño de un guisante", ["Cuanta más mejor", "Ninguna", "Un bote entero"],
       "Nunca montar el disipador sin ella."),
    _q(B4, "Si el procesador se calienta demasiado y baja su velocidad, eso es…", "thermal throttling", ["overclocking", "dual channel", "POST"],
       "En último caso, el equipo se apaga."),
    _q(B4, "La refrigeración líquida (AIO) se usa en…", "procesadores de mucho consumo",
       ["todos los PC de oficina", "solo en la fuente", "solo en la RAM"], "Lleva bomba, tubos y radiador."),
    _q(B4, "La memoria RAM es…", "volátil: se borra al apagar", ["permanente", "un tipo de disco", "firmware"], "El almacenamiento conserva los datos."),
    _q(B4, "¿Se puede poner un módulo DDR4 en una placa DDR5?", "No, tienen muescas distintas", ["Sí, siempre", "Sí, con un adaptador", "Solo si es de 8 GB"],
       "No son intercambiables."),
    _q(B4, "¿Qué voltaje usa la DDR5?", "1,1 V", ["1,2 V", "1,5 V", "3,3 V"], "La DDR4 usa 1,2 V."),
    _q(B4, "Para Dual Channel con 2 módulos se colocan en…", "A2 y B2 (un módulo por canal)", ["A1 y A2", "B1 y B2", "cualquiera"],
       "2 × 8 GB rinde más que 1 × 16 GB."),
    _q(B4, "¿Qué son XMP y EXPO?", "Perfiles que se activan en la UEFI para que la RAM vaya a su velocidad",
       ["Tipos de zócalo", "Conectores de la fuente", "Marcas de disco"], "Si no, la RAM va más lenta."),
    _q(B4, "¿Qué pasó con el puente norte del chipset?", "Se integró dentro del procesador",
       ["Desapareció la RAM", "Pasó al disco", "Se fusionó con la fuente"], "En la placa queda un solo chip: el chipset (PCH)."),
    _q(B4, "¿Qué ranura PCIe usa la tarjeta gráfica?", "x16", ["x1", "x4", "x8"], "x1: red, sonido, Wi-Fi · x4: NVMe · x8: redes rápidas."),
    _q(B4, "Cada versión nueva de PCIe…", "duplica la velocidad de la anterior", ["la triplica", "la reduce a la mitad", "la mantiene"],
       "Son compatibles: va a la velocidad de la más lenta."),
    _q(B4, "¿Cuánto lee aproximadamente un SSD NVMe PCIe 4.0?", "7.000 MB/s", ["550 MB/s", "200 MB/s", "14.000 MB/s"], "SATA: unos 550 MB/s."),
    _q(B4, "¿Cómo se conecta un SSD M.2 NVMe?", "Se atornilla en la placa y usa carriles PCIe",
       ["Con cable SATA", "Por USB", "Al conector ATX"], "Es el estándar para el disco del sistema."),
    _q(B4, "Diferencia entre CPU y GPU:", "La GPU tiene miles de núcleos sencillos; la CPU, pocos muy potentes",
       ["La CPU tiene miles de núcleos sencillos", "No hay diferencia", "La GPU no tiene memoria"], "La GPU hace la misma operación sobre muchos datos."),
    _q(B4, "¿Qué memoria lleva una tarjeta gráfica dedicada?", "VRAM (GDDR6 o GDDR7)", ["DDR3", "SATA", "Caché L1 compartida"], "Propia de la tarjeta."),
    _q(B4, "Con una gráfica dedicada, ¿dónde se conecta el monitor?", "A la tarjeta gráfica", ["Al HDMI de la placa", "A la fuente", "Al chipset"],
       "Si lo conectas a la placa, lo normal es no ver nada."),
    _q(B4, "Un conector USB-A azul ofrece…", "5 Gb/s", ["USB 2.0", "10 Gb/s", "1 Gb/s"], "Negro: USB 2.0 · rojo o turquesa: 10 Gb/s."),
    _q(B4, "¿Para qué sirve el conector RJ-45?", "Red por cable (Ethernet)", ["Vídeo", "Audio", "Teclado antiguo"], "1 o 2,5 Gb/s."),
    _q(B4, "¿Qué conectores ya no verías en una placa actual?", "PS/2, VGA, DVI y eSATA", ["HDMI, USB-C y RJ-45", "DisplayPort y HDMI", "USB-A y USB-C"],
       "Casi han desaparecido."),
    _q(B4, "Un ventilador de 4 pines incluye…", "PWM (control de velocidad)", ["Más potencia", "Un sensor de humo", "Refrigeración líquida"], "Los de 3 pines no."),
    _q(B4, "La fuente de alimentación convierte los 230 V del enchufe en…", "12 V, 5 V y 3,3 V", ["1 V, 2 V y 3 V", "110 V", "24 V"],
       "Y protege frente a sobretensiones."),
    _q(B4, "El conector ATX de 24 pines alimenta…", "la placa base", ["el procesador", "la gráfica", "los discos"], "EPS 8 pines: el procesador."),
    _q(B4, "Cada conector PCIe 6+2 pines puede dar…", "150 W a la gráfica", ["75 W", "600 W", "12 W"], "El 12V-2x6 llega hasta 600 W."),
    _q(B4, "¿Qué certificación 80 PLUS es la más eficiente?", "Titanium (94 %)", ["Estándar (80 %)", "Bronze (85 %)", "Gold (90 %)"],
       "Estándar, Bronze, Silver, Gold, Platinum, Titanium."),
    _q(B4, "Procesador 125 W + gráfica 300 W: ¿qué fuente necesitas?", "650 W", ["500 W", "575 W", "750 W"], "125 + 300 + 75 = 500 W, +30 % de margen."),
    _q(B4, "¿Qué hace la pila CR2032 de la placa?", "Mantiene la hora y la configuración de la UEFI", ["Alimenta la gráfica", "Alimenta los discos", "Arranca el ventilador"],
       "Si el reloj se atrasa, hay que cambiarla."),
    _q(B5, "¿Cuál es el problema del arranque?", "Al encender, la RAM está vacía y para leer el disco hace falta un programa",
       ["El disco está lleno", "La fuente no da voltaje", "La CPU no existe"], "¿Quién carga el sistema operativo?"),
    _q(B5, "El bootstrap consiste en…", "arrancar por etapas: un programa pequeño carga otro más grande",
       ["instalar Windows", "formatear el disco", "actualizar la UEFI"], "Cada etapa prepara la siguiente."),
    _q(B5, "¿Qué ejecuta primero la CPU al encender?", "El firmware (UEFI/BIOS)", ["El sistema operativo", "El gestor de arranque", "El kernel"],
       "El PC apunta a una dirección fija donde está la UEFI."),
    _q(B5, "¿Dónde está grabado el firmware?", "En un chip flash de la placa", ["En el disco duro", "En la RAM", "En la fuente"],
       "Por eso se puede actualizar."),
    _q(B5, "La señal «Power Good» indica que…", "los voltajes de la fuente son correctos", ["el disco arranca", "hay Internet", "la RAM es DDR5"],
       "La fuente la envía a la placa."),
    _q(B5, "El POST comprueba…", "CPU y registros, RAM, gráfica y dispositivos", ["solo el disco", "la conexión a Internet", "los programas instalados"],
       "Si algo falla: pitidos o LED de diagnóstico."),
    _q(B5, "Una ventaja de UEFI sobre BIOS es…", "discos enormes con GPT, Secure Boot y arranque más rápido",
       ["usa 16 bits", "solo funciona con teclado", "usa MBR"], "BIOS: MBR con máximo de 2 TB."),
    _q(B5, "Secure Boot…", "solo arranca software firmado", ["acelera la RAM", "borra el disco", "es un tipo de USB"],
       "Bloquea los virus que se cargan antes que el sistema."),
    _q(B5, "TPM 2.0 es obligatorio para…", "Windows 11", ["Ubuntu", "Android", "MS-DOS"], "Guarda claves de cifrado."),
    _q(B5, "Para entrar en la BIOS/UEFI se suele pulsar…", "Supr, F2 o F10", ["Ctrl + Alt + Supr", "Esc + Tab", "Alt + F4"], "Menú de arranque: F12, F11 o F8."),
    _q(B5, "¿Qué dispositivo suele ir primero en el orden de arranque?", "SSD o disco interno", ["Memoria USB", "Red (PXE)", "DVD"],
       "Después USB, red y DVD."),
    _q(B5, "¿Cuántos bytes ocupa el MBR?", "512 bytes", ["446 bytes", "64 bytes", "2 TB"], "446 de código + 64 de particiones + 2 de firma (55 AA)."),
    _q(B5, "¿Qué firma indica que un disco MBR es arrancable?", "55 AA", ["AA 55 AA", "00 00", "FF FF"], "En hexadecimal."),
    _q(B5, "En UEFI/GPT, el gestor de arranque está…", "en la partición del sistema EFI (ESP), en FAT32",
       ["en la RAM", "en la fuente", "en el chipset"], "Archivos .efi como bootmgfw.efi o grubx64.efi."),
    _q(B5, "¿Qué es GRUB?", "El gestor de arranque estándar de Linux", ["Un antivirus", "Un tipo de RAM", "El kernel de Windows"],
       "Muestra un menú para elegir sistema o versión del kernel."),
    _q(B5, "Con Windows y Ubuntu en el mismo disco, ¿quién deja elegir al arrancar?", "El gestor de arranque (GRUB)",
       ["El POST", "La fuente", "El chipset"], "Es el arranque dual."),
    _q(B5, "El gestor de arranque…", "localiza el kernel, lo carga en la RAM y le cede el control",
       ["comprueba la RAM", "enciende la fuente", "instala drivers"], "Es la fase 4."),
    _q(B5, "El primer proceso de Linux es…", "systemd (proceso 1)", ["smss.exe", "winload.efi", "grub"], "De él nacen todos los demás."),
    _q(B5, "El kernel de Windows es…", "ntoskrnl.exe", ["vmlinuz", "systemd", "bootmgfw.efi"], "El de Linux es vmlinuz."),
    _q(B5, "«grub rescue>» indica un fallo en…", "el gestor de arranque (fase 4)", ["el POST", "la fuente", "la RAM"], "Se repara desde un USB de instalación."),
    _q(B5, "«No bootable device» indica un fallo en…", "la fase 3: dispositivo de arranque", ["el POST", "el kernel", "la pila"],
       "Revisa orden de arranque, disco conectado o USB olvidado."),
    _q(B5, "Pantalla azul o «kernel panic» al cargar: ¿qué se hace?", "Arrancar en modo seguro y revisar controladores o actualizaciones",
       ["Cambiar la fuente", "Cambiar la pila", "Reformatear siempre"], "Son las fases 5-6."),
    _q(B5, "Ante un fallo de arranque, el método es…", "empezar por lo más sencillo y barato (cables, enchufe, piezas sueltas)",
       ["cambiar la placa base", "reinstalar todo", "comprar una fuente nueva"], "Averigua en qué fase se ha parado."),
    _q(B6, "¿Qué hace el sistema operativo?", "Gestiona hardware, memoria, archivos y programas, y hace de intermediario con el usuario",
       ["Solo muestra la pantalla", "Solo conecta a Internet", "Solo guarda archivos"], "Windows 11, Ubuntu, macOS, Android, iOS."),
    _q(B6, "¿Cuál es un software de aplicación?", "LibreOffice", ["Ubuntu", "Windows 11", "Android"], "Ofimática, navegadores, correo, videojuegos, IA."),
    _q(B6, "La pila completa de un sistema informático, de abajo arriba, es…", "Hardware, firmware, sistema operativo, aplicaciones y personas",
       ["Personas, aplicaciones, SO, firmware y hardware", "Hardware, aplicaciones, SO, firmware y personas", "Firmware, hardware, SO, personas y aplicaciones"],
       "El firmware une hardware y software."),
    _q(B6, "En el software propietario…", "el fabricante conserva todos los derechos y el código es cerrado",
       ["se puede modificar libremente", "siempre es gratis", "se puede repartir sin límites"], "No compras el programa: compras permiso para usarlo."),
    _q(B6, "¿Cuántas libertades define el software libre?", "4 (numeradas del 0 al 3)", ["3", "5", "2"], "Usar, estudiar, copiar y repartir, mejorar y publicar."),
    _q(B6, "La libertad 1 del software libre es…", "estudiar cómo funciona", ["usarlo para lo que quieras", "copiarlo", "mejorarlo"],
       "La 0 es usarlo; la 2, copiarlo; la 3, mejorarlo."),
    _q(B6, "«Libre» significa…", "que respeta las 4 libertades; no tiene por qué ser gratis", ["siempre gratis", "sin copyright", "sin soporte"],
       "Hay programas gratis que no son libres."),
    _q(B6, "Una licencia OEM…", "viene con el equipo nuevo y solo vale para ese equipo", ["vale para una empresa entera", "es gratis", "es libre"],
       "Ej.: el Windows de un portátil."),
    _q(B6, "Una licencia por volumen…", "es una clave para muchos equipos de una empresa o centro", ["solo vale para un equipo", "es gratis", "es de prueba"],
       "Ej.: el Windows de las aulas."),
    _q(B6, "El freeware es…", "gratis, pero con el código cerrado", ["libre y gratis", "de pago", "de prueba"], "Ej.: Acrobat Reader o Chrome."),
    _q(B6, "El shareware…", "se prueba un tiempo o con funciones limitadas y luego se paga", ["es libre", "es de código abierto", "viene con el equipo"],
       "Ej.: WinRAR."),
    _q(B6, "La licencia GPL…", "permite usar, estudiar, copiar y mejorar; las versiones modificadas siguen siendo libres",
       ["prohíbe copiar", "es de pago", "es de prueba"], "Ej.: Linux y VLC."),
]

CHULETA = """
### 🧱 Sistema informático
**Hardware + Software + Personas**, y el **firmware** (software dentro del hardware, p. ej. UEFI) une los dos primeros.
Pila: Hardware → Firmware → Sistema operativo → Aplicaciones → Personas.
Generaciones: 1ª válvulas (1940–56) · 2ª transistores (1956–64) · 3ª circuitos integrados (1964–71) · 4ª microprocesador (1971–hoy) · 5ª redes, nube e IA.

### 🔢 Sistemas de numeración
| Base | Símbolos | Dónde |
|---|---|---|
| Decimal (10) | 0-9 | Vida cotidiana |
| Binario (2) | 0, 1 | Dentro del ordenador |
| Octal (8) | 0-7 | Permisos de Linux |
| Hexadecimal (16) | 0-9, A-F | Colores web, MAC, memoria |

- **Decimal → otra base:** divide entre la base y lee los restos **de abajo arriba**.
- **Otra base → decimal:** multiplica cada cifra por su potencia (1, 8, 64… / 1, 16, 256…) y suma.
- **Atajo:** 1 cifra octal = **3 bits** · 1 cifra hexadecimal = **4 bits**.
- A=10, B=11, C=12, D=13, E=14, F=15. **255 = 11111111 = 377₈ = FF₁₆**.

### ➕ Operar y medir
- Suma: 0+0=0 · 0+1=1 · 1+1=0 y llevo 1 · 1+1+1=1 y llevo 1. Resta: 0−1 = 1 y pido 1 prestado.
- 1 byte = 8 bits; KB, MB, GB, TB: **×1024**. MB (bytes) ≠ Mb (bits).
- ASCII: 7 bits (128) · extendido: 8 bits (256) · Unicode (UTF-8): 1-4 bytes. A = 65 = 41₁₆.
- **Paridad par:** añade un bit para que el total de unos sea par. Detecta, no corrige.

### 🏛️ Arquitectura
- **Von Neumann (1945):** una memoria, un bus compartido → cuello de botella. **Harvard:** dos memorias, un bus cada una.
- **Ciclo:** buscar → decodificar → ejecutar → guardar.
- Unidades: CPU (control, ALU, registros) · memoria principal (RAM) · E/S · memoria externa.

### 🔩 Hardware
- **Placas:** E-ATX 305×330 · ATX 305×244 · Micro-ATX 244×244 · Mini-ITX 170×170.
- **Zócalos:** PGA (pines en la CPU, AM4) · LGA (pines en la placa, Intel y AM5) · BGA (soldado).
- **RAM:** DDR4 (1,2 V) · DDR5 (1,1 V); no intercambiables. Dual Channel: A2 y B2.
- **PCIe:** x1, x4, x8, x16; cada versión duplica. **Almacenamiento:** HDD ≈ 200 · SSD SATA ≈ 550 · NVMe 4.0 ≈ 7.000 · NVMe 5.0 ≈ 14.000 MB/s.
- **Fuente:** 80 PLUS Estándar 80 · Bronze 85 · Silver 88 · Gold 90 · Platinum 92 · Titanium 94 %. Potencia = (CPU + GPU + 75 W) × 1,3.
- **Conectores:** ATX 24 pines (placa) · EPS 8 pines (CPU) · PCIe 6+2 (gráfica, 150 W) · 12V-2x6 (hasta 600 W) · SATA (discos).

### 🚀 Arranque (7 fases)
1 Encendido y firmware → 2 POST → 3 Dispositivo de arranque → 4 Gestor de arranque → 5 Carga del kernel → 6 Inicio del sistema → 7 Inicio de sesión.
BIOS (MBR, ≤ 2 TB, 16 bits) vs UEFI (GPT, Secure Boot, TPM). MBR = 512 bytes, firma **55 AA**.

### 📜 Software y licencias
Sistema operativo (gestiona hardware, memoria, archivos y programas) + aplicaciones.
Propietaria de pago · OEM (solo ese equipo) · Por volumen · Freeware (gratis, cerrado) · Shareware (prueba) · Libre GPL (4 libertades: usar, estudiar, copiar, mejorar). **Libre ≠ gratis.**
"""
