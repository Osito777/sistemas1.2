"""
preguntas_t2.py
Contenido y generadores del Tema 2 · Sistemas operativos (PARTE2).
Mismas estructuras que preguntas.py (UDI 1).
"""
import random

from preguntas import _c, _item, _q, comprobar  # noqa: F401  (comprobar se reexporta)

NIVELES_CALC = ["Normal"]


def _k(campo, nombre, opciones):
    return {campo: {"nombre": nombre, "opciones": opciones}}


def _c1(campo, titulo, enunciado, valor, just, pista=""):
    return _c(titulo, enunciado, {campo: valor}, just, pista)


# ---------------------------------------------------------------------------
# 1 · Tipo de sistema operativo (5 criterios)
# ---------------------------------------------------------------------------
LOTES, INTER, RT = "Por lotes", "Interactivo (tiempo compartido)", "Tiempo real"
MONO_U, MULTI_U = "Monousuario", "Multiusuario"
MONO_P, MULTI_P = "Monoprogramación", "Multiprogramación"
MONO_CPU, SIM, ASIM = "Monoproceso", "Multiproceso simétrico", "Multiproceso asimétrico"
CENTRAL, RED, DISTRIB = "Centralizado", "En red", "Distribuido"
CAMPOS_TIPO = {
    "tiempo": {"nombre": "1. Tiempo de respuesta", "opciones": [LOTES, INTER, RT]},
    "usuarios": {"nombre": "2. Número de usuarios", "opciones": [MONO_U, MULTI_U]},
    "procesos": {"nombre": "3. Número de procesos", "opciones": [MONO_P, MULTI_P]},
    "procesadores": {"nombre": "4. Número de procesadores", "opciones": [MONO_CPU, SIM, ASIM]},
    "red": {"nombre": "5. Trabajo en red", "opciones": [CENTRAL, RED, DISTRIB]},
}


def _tipo(titulo, enunciado, r, just, pista=""):
    return _c(titulo, enunciado, dict(zip(CAMPOS_TIPO, r)), just, pista)


CASOS_TIPO = [
    _tipo("🚗 Frenos ABS", "El sistema de frenos ABS de un coche: un microcontrolador, sin pantalla ni usuario.",
          [RT, MONO_U, MONO_P, MONO_CPU, CENTRAL], "Debe responder en un tiempo máximo garantizado: un retraso es peligroso.",
          "¿Qué pasa si tarda?"),
    _tipo("💻 Portátil con Windows 11", "Tu portátil con Windows 11 y varios programas abiertos; procesador de 8 núcleos iguales; wifi.",
          [INTER, MONO_U, MULTI_P, SIM, RED], "Varios programas se turnan la CPU y los núcleos iguales se reparten el trabajo.",
          "Los 8 núcleos son iguales."),
    _tipo("🖧 Servidor del instituto", "Un servidor del instituto al que se conectan 30 alumnos a la vez.",
          [INTER, MULTI_U, MULTI_P, SIM, RED], "Varias personas trabajan a la vez en el mismo equipo.", "¿Cuántas personas?"),
    _tipo("🌍 Red social", "Los servidores de una red social repartidos por el mundo, que el usuario ve como uno solo.",
          [INTER, MULTI_U, MULTI_P, SIM, DISTRIB], "Muchos equipos que parecen uno solo: distribuido.", "«Que parecen uno solo»."),
    _tipo("🏦 Nóminas de noche", "El ordenador de un banco que procesa todos los recibos por la noche.",
          [LOTES, MONO_U, MULTI_P, SIM, CENTRAL], "Muchos trabajos seguidos sin que el usuario intervenga.", "Nadie espera delante."),
    _tipo("📟 MS-DOS", "Un PC con MS-DOS: una persona, un programa cada vez, un procesador, sin red.",
          [INTER, MONO_U, MONO_P, MONO_CPU, CENTRAL], "Solo un programa en memoria; el siguiente espera a que acabe.", "Un programa cada vez."),
    _tipo("🏥 Monitor de hospital", "Un monitor de hospital que debe dar la alarma en menos de 1 segundo y envía datos por la red.",
          [RT, MONO_U, MULTI_P, MONO_CPU, RED], "Tiempo máximo garantizado; está conectado a la red del hospital.", "Plazo garantizado."),
    _tipo("🧠 Procesador jefe", "Un equipo con varios procesadores donde uno «jefe» reparte las tareas a los demás.",
          [INTER, MONO_U, MULTI_P, ASIM, CENTRAL], "Un procesador jefe reparte las tareas: asimétrico.", "¿Quién reparte el trabajo?"),
]

# ---------------------------------------------------------------------------
# 2 · Estructura
# ---------------------------------------------------------------------------
ESTR = ["Monolítico", "En capas (THE)", "En capas (MINIX)", "Máquina virtual", "Cliente-servidor"]
CASOS_ESTR = [
    _c1("estructura", "📦 Un único programa", "Todo es un único programa grande: rápido, pero si una parte falla puede caer todo.", ESTR[0],
        "Es la estructura monolítica. Ejemplo: MS-DOS."),
    _c1("estructura", "🍽️ Restaurante de 6 niveles", "Tiene los niveles 0 a 5 (procesador, memoria, E/S, comunicación, programas y operador).", ESTR[1],
        "Es el sistema THE: cada capa solo usa los servicios de la capa de abajo."),
    _c1("estructura", "🏫 Secretaría del instituto", "Tiene 4 capas: procesos de usuario, servidores, tareas de E/S y gestión de procesos.", ESTR[2],
        "Es MINIX, creado por un profesor para enseñar; dio la idea para crear Linux."),
    _c1("estructura", "🖥️ VirtualBox", "Simula varios ordenadores dentro de uno, cada uno con su propio sistema operativo.", ESTR[3],
        "Máquina virtual."),
    _c1("estructura", "📬 Servidores por mensajes", "Núcleo mínimo; los «servidores» dan servicios a los procesos «clientes» por mensajes. Si un servidor falla, el resto sigue.",
        ESTR[4], "Cliente-servidor."),
    _c1("estructura", "🧱 MS-DOS", "El MS-DOS.", ESTR[0], "Ejemplo clásico de sistema monolítico."),
    _c1("estructura", "🔎 Buscar el fallo", "Si algo falla, sabes en qué capa buscar (nivel 3: entrada/salida).", ESTR[1],
        "La estructura en capas permite localizar el fallo por capa."),
]

# ---------------------------------------------------------------------------
# 3 · Función del sistema operativo
# ---------------------------------------------------------------------------
FUNC = ["Procesos", "Memoria", "Entrada/Salida", "Archivos", "Seguridad"]
CASOS_FUNC = [
    _c1("funcion", "🎵 Spotify y Chrome", "Tienes abiertos Spotify y Chrome a la vez y los dos funcionan.", FUNC[0], "Decide quién usa la CPU y cuándo."),
    _c1("funcion", "🖱️ Mover el ratón", "Mueves el ratón y la flecha se mueve en la pantalla.", FUNC[2], "Controla los periféricos."),
    _c1("funcion", "📁 Crear una carpeta", "Creas una carpeta «Trabajos» y metes dentro un documento.", FUNC[3], "Organiza el disco."),
    _c1("funcion", "🔐 Contraseña", "Al encender el ordenador te pide la contraseña.", FUNC[4], "Protege el sistema y los datos."),
    _c1("funcion", "🐢 40 pestañas", "Con 40 pestañas abiertas el ordenador va lento porque la RAM está llena.", FUNC[1], "Reparte la RAM entre los programas."),
    _c1("funcion", "🖨️ Imprimir", "Imprimes un trabajo en la impresora de clase.", FUNC[2], "Periférico: entrada/salida."),
    _c1("funcion", "🧊 Programa colgado", "Un programa se cuelga y lo cierras con el Administrador de tareas.", FUNC[0], "Gestión de procesos."),
    _c1("funcion", "🗑️ Papelera", "Borras un archivo y aparece en la Papelera.", FUNC[3], "Gestión de archivos."),
    _c1("funcion", "👨‍👩‍👦 Cuenta propia", "Tu hermano no puede ver tus fotos porque tiene su propia cuenta.", FUNC[4], "Seguridad lógica: usuarios y permisos."),
    _c1("funcion", "🔌 Pendrive", "Conectas un pendrive y suena el aviso de «dispositivo conectado».", FUNC[2], "Entrada/salida (Plug and Play + driver)."),
    _c1("funcion", "🎮 Cerrar un juego", "Al cerrar un juego, la memoria que usaba queda libre para otros programas.", FUNC[1], "Gestión de la memoria."),
    _c1("funcion", "🛡️ Defender", "Windows Defender bloquea un programa con virus.", FUNC[4], "Seguridad lógica: antivirus."),
]

# ---------------------------------------------------------------------------
# 4 · Programa, proceso o hilo / estados
# ---------------------------------------------------------------------------
PPH = ["Programa", "Proceso", "Hilo"]
CASOS_PPH = [
    _c1("concepto", "📄 notepad.exe", "notepad.exe guardado en el disco, sin abrir.", PPH[0], "Fichero «dormido»: no usa CPU ni RAM."),
    _c1("concepto", "📝 Bloc de notas ×2", "Abres el Bloc de notas dos veces: cada ventana es…", PPH[1], "Un programa abierto 2 veces = 2 procesos, cada uno con su PID."),
    _c1("concepto", "🔤 Corrector de Word", "El corrector que subraya las faltas mientras escribes en Word.", PPH[2], "Un hilo del proceso de Word: comparte su memoria."),
    _c1("concepto", "🎧 Spotify y Word", "Spotify y Word abiertos a la vez son…", PPH[1], "Programas distintos: cada uno con su propia memoria."),
    _c1("concepto", "💾 Autoguardado", "La tarea de Word que guarda el documento cada pocos minutos.", PPH[2], "Otro hilo del mismo proceso."),
    _c1("concepto", "📕 La receta", "La receta del libro (antes de cocinar).", PPH[0], "Programa = receta; proceso = cocinarla ahora."),
    _c1("concepto", "👩‍🍳 Cocineros", "Los cocineros que trabajan a la vez y comparten la nevera.", PPH[2], "Hilos: comparten la memoria del proceso."),
    _c1("concepto", "🔢 Tiene un PID", "Tiene un número, el PID, y está cargado en la RAM.", PPH[1], "Un proceso es un programa en ejecución."),
]
EST = ["Nuevo", "Listo", "En ejecución", "Bloqueado", "Terminado"]
CASOS_EST = [
    _c1("estado", "🎶 Spotify espera", "Spotify espera a que llegue la canción por Internet.", EST[3], "Espera una E/S (la red). Al llegar los datos pasa a listo."),
    _c1("estado", "⌨️ Espera una tecla", "Un programa espera a que pulses una tecla.", EST[3], "Pide E/S: espera tecla, disco…"),
    _c1("estado", "⏳ Esperando la CPU", "Un proceso preparado que espera a que le toque la CPU.", EST[1], "Listo: espera en la cola."),
    _c1("estado", "⚙️ Usando la CPU", "El proceso que tiene ahora mismo el núcleo de la CPU.", EST[2], "Solo uno por núcleo."),
    _c1("estado", "🆕 Acaba de crearse", "El proceso acaba de crearse.", EST[0], "Nuevo."),
    _c1("estado", "🏁 Ha acabado", "El proceso ha finalizado su trabajo.", EST[4], "Terminado."),
    _c1("estado", "✅ Termina la E/S", "Un proceso bloqueado recibe por fin los datos que esperaba.", EST[1], "Termina la E/S → pasa a listo."),
    _c1("estado", "⏱️ Se acaba su turno", "A un proceso en ejecución se le acaba su turno de CPU (sin haber terminado).", EST[1], "Se acaba su turno → vuelve a listo."),
]

# ---------------------------------------------------------------------------
# 5 · Memoria
# ---------------------------------------------------------------------------
MEM = ["Protección", "Compartición", "Paginación", "Segmentación", "Reubicación", "Intercambio (swap)",
       "Memoria virtual", "Fragmentación interna", "Fragmentación externa"]
CASOS_MEM = [
    _c1("concepto", "🔒 Ningún proceso entra", "Ningún proceso puede entrar en la memoria de otro.", MEM[0], "Protección."),
    _c1("concepto", "👯 Mismo programa ×2", "Varios procesos usan la misma zona (p. ej., el mismo programa abierto 2 veces).", MEM[1], "Compartición."),
    _c1("concepto", "🧩 Trozos iguales", "Se divide la memoria en trozos iguales llamados páginas.", MEM[2], "Paginación."),
    _c1("concepto", "✂️ Trozos según el programa", "Se divide la memoria en trozos según el programa (segmentos).", MEM[3], "Segmentación."),
    _c1("concepto", "🕳️ Cualquier hueco", "Un proceso puede colocarse en cualquier hueco libre.", MEM[4], "Reubicación."),
    _c1("concepto", "💿 Al disco", "Pasar al disco lo que no se usa para hacer sitio.", MEM[5], "Intercambio (swap)."),
    _c1("concepto", "📀 pagefile.sys", "Usar parte del disco como si fuera RAM (pagefile.sys en Windows, swap en Linux).", MEM[6], "Memoria virtual: permite abrir más programas de los que caben, pero el disco es mucho más lento."),
    _c1("concepto", "📦 Sobra dentro del trozo", "Sobra espacio dentro del trozo asignado al proceso.", MEM[7], "Fragmentación interna."),
    _c1("concepto", "🧱 Huecos sueltos", "Hay huecos libres, pero sueltos y pequeños: P4 (1,5) no cabe aunque sumen 2,1.", MEM[8], "Fragmentación externa."),
]

# ---------------------------------------------------------------------------
# 6 · E/S, archivos y seguridad
# ---------------------------------------------------------------------------
TEC = ["Interrupción", "DMA", "Caching", "Buffering", "Spooling", "Plug and Play + driver"]
CASOS_TEC = [
    _c1("tecnica", "⌨️ Pulsas una tecla", "Pulsas una tecla: el teclado avisa a la CPU, que para un instante, la lee y se la pasa al programa.", TEC[0], "Interrupción."),
    _c1("tecnica", "🎬 Película al USB", "Copias una película al USB: los datos pasan de la RAM al USB sin ocupar la CPU, que solo recibe un aviso al final.", TEC[1], "DMA."),
    _c1("tecnica", "▶️ YouTube", "Ves un vídeo en YouTube: descarga unos segundos por adelantado para que no se corte.", TEC[3], "Buffering."),
    _c1("tecnica", "🖨️ 3 documentos", "Imprimes 3 documentos seguidos: se ponen en cola y la impresora los saca uno a uno.", TEC[4], "Spooling."),
    _c1("tecnica", "🌐 Web ya visitada", "Vuelves a una web que ya visitaste y carga antes porque se usan las imágenes guardadas.", TEC[2], "Caching."),
    _c1("tecnica", "🖱️ Ratón nuevo", "Conectas un ratón nuevo: se detecta, se busca su controlador y queda listo.", TEC[5], "Plug and Play + driver."),
    _c1("tecnica", "🎧 Spotify descargando", "Escuchas música en Spotify mientras se descarga.", TEC[3], "Buffering: memoria intermedia que compensa velocidades."),
    _c1("tecnica", "📬 Cola de impresión", "La cola de impresión donde los documentos esperan su turno.", TEC[4], "Spooling."),
]
SIST = ["FAT16", "FAT32", "NTFS", "EXT4", "CDFS · UDF", "HFS · HFS+ (hoy APFS)"]
CASOS_SIST = [
    _c1("sistema", "🔌 USB y tarjetas", "Memorias USB y tarjetas; ficheros de 4 GB como máximo.", SIST[1], "FAT32."),
    _c1("sistema", "🪟 Windows actual", "Windows actual: permisos, cifrado y journaling.", SIST[2], "NTFS."),
    _c1("sistema", "🐧 Linux", "Sistema de archivos de Linux con journaling (EXT3 y EXT4).", SIST[3], "ext4."),
    _c1("sistema", "💿 DVD y Blu-ray", "Discos ópticos: DVD y Blu-ray.", SIST[4], "CDFS · UDF."),
    _c1("sistema", "🍎 Mac antiguos", "Mac antiguos; hoy se usa APFS.", SIST[5], "HFS · HFS+."),
    _c1("sistema", "📟 MS-DOS", "MS-DOS y Windows antiguos, con particiones pequeñas.", SIST[0], "FAT16."),
]
SEG = ["Seguridad lógica", "Seguridad física"]
CASOS_SEG = [
    _c1("seg", "🔑 Usuario y contraseña", "Usuario y contraseña.", SEG[0], "Lógica."),
    _c1("seg", "📹 Cámaras", "Cámaras de vigilancia.", SEG[1], "Física."),
    _c1("seg", "🛡️ Antivirus y cortafuegos", "Antivirus y cortafuegos.", SEG[0], "Lógica."),
    _c1("seg", "🔋 SAI", "SAI: mantiene el equipo encendido si se va la luz.", SEG[1], "Física."),
    _c1("seg", "📑 Permisos", "Permisos sobre los ficheros.", SEG[0], "Lógica."),
    _c1("seg", "🚪 Sala con llave", "Salas con llave.", SEG[1], "Física."),
    _c1("seg", "💾 Cifrado y copias", "Cifrado y copias de seguridad.", SEG[0], "Lógica."),
    _c1("seg", "🧯 Antiincendios", "Sistemas antiincendios.", SEG[1], "Física."),
]

# ---------------------------------------------------------------------------
# 7 · Virtualización e instalación
# ---------------------------------------------------------------------------
VIRT = ["Hipervisor tipo 1 (nativo)", "Hipervisor tipo 2 (alojado)", "Virtualización completa", "Paravirtualización",
        "Contenedores", "Emulación"]
CASOS_VIRT = [
    _c1("tec", "🧱 VMware ESXi", "VMware ESXi, Proxmox VE, Hyper-V o KVM, instalados directamente sobre el hardware.", VIRT[0], "Tipo 1: más rendimiento, para servidores y centros de datos."),
    _c1("tec", "📦 VirtualBox", "VirtualBox, VMware Workstation o Parallels: un programa sobre Windows, Linux o macOS.", VIRT[1], "Tipo 2: más cómodo para aprender y probar."),
    _c1("tec", "🙈 Invitado sin saberlo", "El invitado no sabe que es virtual; funciona con ayuda de VT-x / AMD-V.", VIRT[2], "Virtualización completa."),
    _c1("tec", "🤝 Guest Additions", "El invitado colabora con el hipervisor mediante drivers (Guest Additions, VirtIO).", VIRT[3], "Paravirtualización."),
    _c1("tec", "🐳 Docker", "Aíslan aplicaciones que comparten el núcleo del anfitrión; muy ligeros.", VIRT[4], "Contenedores (p. ej., Docker)."),
    _c1("tec", "🎮 QEMU", "Simula otro procesador; es lento (QEMU, emuladores de consolas).", VIRT[5], "Emulación."),
    _c1("tec", "🏢 Centro de datos", "Un hipervisor para un servidor de centro de datos, sin sistema operativo debajo.", VIRT[0], "Tipo 1 (bare-metal)."),
    _c1("tec", "🎓 Aprender en clase", "Un hipervisor para aprender y probar sistemas en el ordenador del aula con Windows.", VIRT[1], "Tipo 2 (hosted)."),
]
INST = ["Limpia", "Actualización", "Multiarranque", "Desatendida", "Por red (PXE)", "Clonación"]
CASOS_INST = [
    _c1("instalacion", "🧼 Desde cero", "Se formatea y se instala desde cero; la más recomendable.", INST[0], "Limpia."),
    _c1("instalacion", "⬆️ Encima", "Se instala encima de la anterior, conservando datos y programas; puede arrastrar errores.", INST[1], "Actualización."),
    _c1("instalacion", "🔀 Varios SO", "Varios sistemas en un equipo; el gestor de arranque deja elegir.", INST[2], "Multiarranque."),
    _c1("instalacion", "📜 autounattend.xml", "Las respuestas van en un fichero: autounattend.xml o autoinstall.", INST[3], "Desatendida."),
    _c1("instalacion", "🌐 Desde la red", "El equipo arranca desde la red y descarga la instalación de un servidor.", INST[4], "Por red (PXE)."),
    _c1("instalacion", "🐑 Equipo modelo", "Se copia la imagen de un equipo modelo (Clonezilla; sysprep en Windows).", INST[5], "Clonación."),
]

# ---------------------------------------------------------------------------
# 8 · Particiones
# ---------------------------------------------------------------------------
FUNCP = ["EFI", "MSR", "Sistema (C: o /)", "Datos (D: o /home)", "swap", "/boot", "Recuperación (WinRE)", "Restauración (OEM)"]
CASOS_FUNCP = [
    _c1("funcion", "🚀 Gestores de arranque", "FAT32, 100–500 MB: guarda los gestores de arranque (.efi).", FUNCP[0], "Partición EFI."),
    _c1("funcion", "🧰 16 MB reservados", "16 MB sin formato: espacio reservado para que Windows gestione el disco.", FUNCP[1], "MSR."),
    _c1("funcion", "🪟 Sistema", "NTFS o ext4, 25–64 GB o más: el sistema operativo y los programas.", FUNCP[2], "Sistema."),
    _c1("funcion", "📚 Documentos", "El resto del disco: documentos, para reinstalar sin perderlos.", FUNCP[3], "Datos."),
    _c1("funcion", "🔁 Memoria virtual", "Linux: tamaño como la RAM; memoria virtual y hibernación.", FUNCP[4], "swap."),
    _c1("funcion", "🐧 Kernel y GRUB", "ext4, 1 GB: el kernel y los ficheros de GRUB.", FUNCP[5], "/boot."),
    _c1("funcion", "🛟 WinRE", "NTFS, 0,5–1 GB: reparar Windows si no arranca.", FUNCP[6], "Recuperación."),
    _c1("funcion", "🏭 De fábrica", "NTFS oculta, 10–20 GB: dejar el equipo como salió de fábrica.", FUNCP[7], "Restauración (OEM)."),
]
PEL = ["Primaria", "Extendida", "Lógica"]
CASOS_PEL = [
    _c1("tipo", "1️⃣ Máximo 4", "Máximo 4 por disco; puede arrancar un sistema operativo.", PEL[0], "Primaria."),
    _c1("tipo", "📦 La caja", "Solo una por disco; es una caja para meter lógicas; no se formatea ni guarda datos.", PEL[1], "Extendida."),
    _c1("tipo", "5️⃣ sda5", "Va dentro de la extendida; en Linux se numera desde el 5 (sda5, sda6…).", PEL[2], "Lógica."),
    _c1("tipo", "🅰️ La activa", "En BIOS, una de ellas es la «activa» (la que arranca).", PEL[0], "Primaria."),
    _c1("tipo", "🔢 Muchas", "Puede haber muchas dentro de la extendida.", PEL[2], "Lógicas."),
    _c1("tipo", "1K en lsblk", "En lsblk aparece con 1K porque solo es la caja (Id 5).", PEL[1], "Extendida."),
]
TAB = ["MBR", "GPT"]
CASOS_TAB = [
    _c1("tabla", "📏 Máximo 2 TB", "Tamaño máximo de disco: 2 TB.", TAB[0], "MBR."),
    _c1("tabla", "♾️ 9,4 ZB", "Tamaño prácticamente ilimitado (9,4 ZB).", TAB[1], "GPT."),
    _c1("tabla", "🧬 BIOS Legacy", "Funciona con BIOS (Legacy).", TAB[0], "MBR."),
    _c1("tabla", "🆕 UEFI", "Funciona con UEFI y arranca desde la partición EFI.", TAB[1], "GPT."),
    _c1("tabla", "🔢 128", "Hasta 128 particiones en Windows, todas primarias.", TAB[1], "GPT."),
    _c1("tabla", "4️⃣ 3+1", "4 primarias, o 3 primarias + 1 extendida con lógicas.", TAB[0], "MBR."),
    _c1("tabla", "💥 Si se daña", "Si la tabla se daña, se pierde: el disco no arranca.", TAB[0], "MBR. GPT guarda una copia al final del disco."),
    _c1("tabla", "🪟 Windows 11", "Requisito para instalar Windows 11.", TAB[1], "GPT con UEFI."),
]

# ---------------------------------------------------------------------------
# 9 · Gestores de arranque
# ---------------------------------------------------------------------------
HERR = ["bcdedit", "msconfig", "EasyBCD", "/etc/default/grub", "sudo update-grub", "Grub Customizer", "bootrec", "bcdboot", "Boot-Repair"]
CASOS_HERR = [
    _c1("herr", "⌨️ /timeout 45", "bcdedit /timeout 45 cambia el tiempo de espera. Esta orden es de…", HERR[0], "Es el comando de texto para ver y editar el BCD."),
    _c1("herr", "🪟 Pestaña Arranque", "Herramienta con ventanas de Windows donde marcas el sistema predeterminado y el arranque a prueba de errores.", HERR[1], "msconfig › Arranque."),
    _c1("herr", "🖼️ bcdedit con ventanas", "Gestor de arranque de Windows en modo gráfico, equivalente a bcdedit.", HERR[2], "EasyBCD."),
    _c1("herr", "📝 GRUB_TIMEOUT", "Fichero donde se cambia GRUB_TIMEOUT y GRUB_DEFAULT.", HERR[3], "/etc/default/grub."),
    _c1("herr", "🔁 Aplicar cambios", "Orden obligatoria para que los cambios de GRUB se apliquen.", HERR[4], "Sin sudo update-grub no cambia nada."),
    _c1("herr", "🖱️ Ordenar con flechas", "Herramienta gráfica de GRUB: ordenar con flechas y renombrar con doble clic.", HERR[5], "Grub Customizer."),
    _c1("herr", "🛠️ MBR dañado", "Herramienta de WinRE para BIOS/MBR: /fixmbr, /fixboot y /rebuildbcd.", HERR[6], "bootrec."),
    _c1("herr", "🛠️ UEFI dañado", "Comando que reconstruye el arranque de Windows en UEFI: bcdboot C:\\Windows /s S: /f UEFI.", HERR[7], "bcdboot."),
    _c1("herr", "🚑 grub rescue>", "Herramienta que se ejecuta desde un USB de Ubuntu cuando sale «grub rescue>».", HERR[8], "Boot-Repair."),
]

TEMAS_CLASIF = {
    "¿Qué tipo de SO es? (5 criterios)": ("t2_tipo", CASOS_TIPO, CAMPOS_TIPO, "Elige un tipo para cada uno de los 5 criterios."),
    "Estructura de un SO": ("t2_estr", CASOS_ESTR, _k("estructura", "Estructura", ESTR), "Monolítico, capas THE, MINIX, máquina virtual o cliente-servidor."),
    "¿Qué función del SO es?": ("t2_func", CASOS_FUNC, _k("funcion", "Función del SO", FUNC), "Las 5 funciones del sistema operativo."),
    "Programa, proceso o hilo": ("t2_pph", CASOS_PPH, _k("concepto", "Concepto", PPH), "Actividad 2: procesos e hilos."),
    "Estado de un proceso": ("t2_est", CASOS_EST, _k("estado", "Estado", EST), "Nuevo, listo, en ejecución, bloqueado o terminado."),
    "Gestión de la memoria": ("t2_mem", CASOS_MEM, _k("concepto", "Concepto de memoria", MEM), "Protección, paginación, swap, fragmentación…"),
    "Técnica de entrada/salida": ("t2_tec", CASOS_TEC, _k("tecnica", "Técnica", TEC), "Interrupción, DMA, caching, buffering o spooling."),
    "Sistema de archivos": ("t2_sist", CASOS_SIST, _k("sistema", "Sistema de archivos", SIST), "FAT, NTFS, ext4…"),
    "Seguridad lógica o física": ("t2_seg", CASOS_SEG, _k("seg", "Tipo de seguridad", SEG), "Contraseñas, cámaras, SAI…"),
    "Virtualización": ("t2_virt", CASOS_VIRT, _k("tec", "Tecnología", VIRT), "Hipervisores y otras tecnologías."),
    "Tipo de instalación": ("t2_inst", CASOS_INST, _k("instalacion", "Tipo de instalación", INST), "Limpia, actualización, multiarranque…"),
    "Función de una partición": ("t2_funcp", CASOS_FUNCP, _k("funcion", "Función", FUNCP), "EFI, MSR, sistema, swap…"),
    "Primaria, extendida o lógica": ("t2_pel", CASOS_PEL, _k("tipo", "Tipo de partición", PEL), "Particiones en discos MBR."),
    "MBR o GPT": ("t2_tab", CASOS_TAB, _k("tabla", "Tabla de particiones", TAB), "Dos tablas de particiones."),
    "Herramienta de arranque": ("t2_herr", CASOS_HERR, _k("herr", "Herramienta", HERR), "bcdedit, GRUB, reparación…"),
}


# ---------------------------------------------------------------------------
# Generadores
# ---------------------------------------------------------------------------
def gen_dev_linux(nivel=None, cantidad=10):
    letras = "abcd"
    ord_ = {1: "primer", 2: "segundo", 3: "tercer", 4: "cuarto"}
    items = []
    for i in range(cantidad):
        t = i % 4
        d, p = random.randint(1, 4), random.randint(1, 4)
        if t == 0:
            r = f"/dev/sd{letras[d - 1]}"
            items.append(_item(f"Linux: ¿cómo se llama el **{ord_[d]} disco SATA o USB**?", "texto", r,
                               f"a = 1.º, b = 2.º, c = 3.º, d = 4.º → **{r}**.", "Cada disco es un fichero en /dev: sda, sdb, sdc…",
                               aceptadas=[r], placeholder="p. ej. /dev/sdb"))
        elif t == 1:
            r = f"/dev/sd{letras[d - 1]}{p}"
            items.append(_item(f"Linux: la **partición {p}** del **{ord_[d]} disco** SATA. ¿Cómo se llama?", "texto", r,
                               f"Disco {letras[d - 1]} + número de partición → **{r}**.", "Partición = número detrás del disco.",
                               aceptadas=[r], placeholder="p. ej. /dev/sdb2"))
        elif t == 2:
            n = random.randint(1, 3)
            r = f"/dev/sd{letras[d - 1]}{4 + n}"
            items.append(_item(f"Linux, disco MBR: la **partición lógica nº {n}** del **{ord_[d]} disco**. ¿Cómo se llama?", "texto", r,
                               f"Las lógicas siempre empiezan en 5: {4 + n} → **{r}**.", "Las lógicas se numeran desde el 5.",
                               aceptadas=[r], placeholder="p. ej. /dev/sdb5"))
        else:
            r = f"/dev/nvme{d - 1}n1p{p}"
            items.append(_item(f"Linux: la **partición {p}** del **{ord_[d]} disco NVMe**. ¿Cómo se llama?", "texto", r,
                               f"Los NVMe cuentan desde 0: {d - 1} → **{r}**.", "nvme0n1 es el primero; sus particiones, nvme0n1p1…",
                               aceptadas=[r], placeholder="p. ej. /dev/nvme1n1p2"))
    random.shuffle(items)
    return items


def gen_frag(nivel=None, cantidad=8):
    items = []
    for _ in range(cantidad):
        huecos = [random.choice([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]) for _ in range(3)]
        proceso = random.choice([0.5, 0.9, 1.2, 1.5, 1.8, 2.0])
        total = round(sum(huecos), 1)
        mayor = max(huecos)
        txt = ", ".join(str(h).replace(".", ",") for h in huecos)
        op = ["Sí, cabe en un hueco", "No: fragmentación externa", "No: no hay memoria libre en total"]
        if proceso <= mayor:
            c, expl = op[0], f"Hay un hueco de {str(mayor).replace('.', ',')} GB, suficiente para {str(proceso).replace('.', ',')} GB."
        elif proceso <= total:
            c = op[1]
            expl = (f"Los huecos suman {str(total).replace('.', ',')} GB, pero el mayor es {str(mayor).replace('.', ',')} GB: "
                    f"hay memoria libre, pero suelta y en trozos pequeños → fragmentación externa.")
        else:
            c, expl = op[2], f"Los huecos suman solo {str(total).replace('.', ',')} GB, menos de los {str(proceso).replace('.', ',')} GB que necesita."
        items.append(_item(f"Hay tres huecos libres de **{txt} GB** separados entre procesos. "
                           f"Llega un proceso que necesita **{str(proceso).replace('.', ',')} GB**. ¿Qué pasa?",
                           "texto", c, expl, "Un proceso necesita un hueco seguido, no la suma de varios.",
                           aceptadas=[c], opciones=op))
    return items


def gen_mbrgpt(nivel=None, cantidad=8):
    casos = [
        ("un equipo nuevo con UEFI", "GPT", "Equipo nuevo con UEFI → GPT."),
        ("un equipo antiguo que solo tiene BIOS", "MBR", "Equipo antiguo que solo tiene BIOS → MBR."),
        ("un disco de 4 TB", "GPT", "MBR solo llega a 2 TB: más de 2 TB → GPT."),
        ("un equipo donde instalarás Windows 11", "GPT", "Windows 11 necesita UEFI, es decir, GPT."),
        ("un disco de 500 GB en un PC con BIOS (Legacy)", "MBR", "BIOS Legacy arranca con MBR."),
        ("un servidor nuevo con UEFI y un disco de 8 TB", "GPT", "UEFI y más de 2 TB → GPT."),
        ("un portátil con UEFI y 1 TB, para arranque dual", "GPT", "UEFI → GPT; Windows y Ubuntu comparten la EFI."),
        ("un viejo PC con BIOS y un disco de 160 GB", "MBR", "Solo BIOS → MBR."),
    ]
    random.shuffle(casos)
    return [_item(f"¿Qué tabla de particiones usarías en **{d}**?", "texto", r, e,
                  "Equipo con UEFI → GPT · solo BIOS → MBR · más de 2 TB → GPT.",
                  aceptadas=[r], opciones=["MBR", "GPT"]) for d, r, e in casos[:cantidad]]


TEMAS_CALCULO = {
    "Nombres de discos y particiones en Linux": gen_dev_linux,
    "Fragmentación: ¿cabe el proceso?": gen_frag,
    "¿MBR o GPT?": gen_mbrgpt,
}

# ---------------------------------------------------------------------------
# Ordena la secuencia
# ---------------------------------------------------------------------------
ORDENAR = [
    {"titulo": "🔄 La vida de un proceso", "enunciado": "Ordena los estados de un proceso que pide una E/S antes de terminar.",
     "pasos": ["Nuevo", "Listo (espera su turno)", "En ejecución", "Bloqueado (pide E/S)", "Listo otra vez (termina la E/S)",
               "En ejecución otra vez", "Terminado"],
     "explicacion": "Solo hay un proceso «en ejecución» por núcleo; el resto espera en «listo»."},
    {"titulo": "📶 Jerarquía de almacenamiento", "enunciado": "Ordena de la memoria más rápida y pequeña a la más lenta, grande y barata.",
     "pasos": ["Registros", "Caché", "Memoria principal (RAM)", "Caché de disco", "Memoria auxiliar (disco, SSD, USB, DVD)"],
     "explicacion": "Como: en la mano, encima de la mesa, mochila, taquilla y biblioteca."},
    {"titulo": "🍽️ Capas del sistema THE", "enunciado": "Ordena de arriba (usuario) abajo (hardware).",
     "pasos": ["Nivel 5 · Operador", "Nivel 4 · Programas de usuario", "Nivel 3 · Gestión de entrada/salida",
               "Nivel 2 · Comunicación operador-procesos", "Nivel 1 · Gestión de la memoria",
               "Nivel 0 · Asignación del procesador y multiprogramación", "Hardware"],
     "explicacion": "Cada capa solo usa los servicios de la capa de abajo."},
    {"titulo": "🏫 Capas de MINIX", "enunciado": "Ordena de arriba abajo las 4 capas de MINIX.",
     "pasos": ["Nivel 4 · Procesos de usuario", "Nivel 3 · Procesos servidores", "Nivel 2 · Tareas de entrada/salida",
               "Nivel 1 · Gestión de procesos", "Hardware"],
     "explicacion": "Alumno → ventanillas → conserje → jefe → edificio."},
    {"titulo": "📜 Generaciones de SO", "enunciado": "Ordena por generación.",
     "pasos": ["1.ª · Válvulas de vacío (casi sin SO)", "2.ª · Transistores (CTSS)", "3.ª · Circuitos integrados (OS/360, UNIX)",
               "4.ª · Microprocesadores (BSD UNIX, VMS)", "5.ª · PC y redes (MS-DOS, Windows)"],
     "explicacion": "Válvulas → transistores → circuitos integrados → microprocesadores → PC y redes."},
    {"titulo": "🔔 Una interrupción", "enunciado": "Ordena lo que ocurre cuando pulsas una tecla.",
     "pasos": ["El periférico «levanta la mano»", "La CPU para un momento lo que hace", "Ejecuta la rutina de atención a la interrupción",
               "Vuelve a lo que estaba haciendo"],
     "explicacion": "Así la CPU no tiene que estar pendiente del teclado."},
    {"titulo": "💽 Particionar un disco nuevo", "enunciado": "Ordena los 4 pasos.",
     "pasos": ["Disco nuevo, sin tabla ni particiones", "Elegir la tabla de particiones (MBR o GPT)", "Crear las particiones", "Formatear (sistema de archivos)"],
     "explicacion": "Cada partición recibe su sistema de archivos (NTFS, ext4, FAT32…)."},
    {"titulo": "🪟 Instalar Windows 11", "enunciado": "Ordena los 7 pasos.",
     "pasos": ["Arrancar desde el USB o la ISO", "Idioma, hora y teclado", "Clave (o «No tengo clave»)", "Edición (igual que la licencia)",
               "Disco: dónde instalar (particiones)", "Copia de archivos y reinicios", "OOBE: región, equipo, cuenta y privacidad"],
     "explicacion": "Con Mayús + F10 se abre un CMD durante la instalación."},
    {"titulo": "🐧 Instalar Ubuntu 26.04 LTS", "enunciado": "Ordena los 7 pasos.",
     "pasos": ["Arrancar (GRUB: Try or Install Ubuntu)", "Idioma, accesibilidad y teclado", "Red", "Aplicaciones (predeterminadas o ampliadas)",
               "Tipo de instalación (borrar disco, junto a Windows o manual)", "Cuenta (usuario, equipo y contraseña)", "Instalar, reiniciar y quitar el USB"],
     "explicacion": "Ubuntu funciona desde el USB (sesión en vivo) sin instalar."},
    {"titulo": "📦 Crear una máquina virtual", "enunciado": "Ordena los 7 pasos de la práctica de VirtualBox.",
     "pasos": ["Descargar la ISO oficial", "Nueva VM (nombre, tipo e ISO)", "RAM y CPU", "Disco VDI dinámico", "EFI + TPM (obligatorio en Windows 11)",
               "Red (NAT o puente)", "Instantánea antes y después de instalar"],
     "explicacion": "Al terminar, instala las Guest Additions."},
    {"titulo": "🚀 Tras el gestor de arranque", "enunciado": "Ordena las 4 etapas.",
     "pasos": ["Gestor de arranque", "Carga del kernel", "Inicio del SO (drivers, memoria virtual, primer proceso)", "Interfaz (consola o escritorio gráfico)"],
     "explicacion": "El primer proceso en Linux es systemd (PID 1)."},
    {"titulo": "🪟 Arranque de Ubuntu con UEFI", "enunciado": "Ordena el arranque de Ubuntu con UEFI.",
     "pasos": ["shimx64.efi", "grubx64.efi", "Lee grub.cfg → menú", "vmlinuz + initrd", "systemd (PID 1)"],
     "explicacion": "Windows: bootmgfw.efi → BCD → winload.efi → núcleo de Windows."},
    {"titulo": "🔀 Orden de instalación (multiarranque)", "enunciado": "¿En qué orden se instalan los sistemas para que arranquen bien?",
     "pasos": ["Windows primero", "macOS después", "Linux al final"],
     "explicacion": "Windows sobrescribe el gestor de arranque y no ve Linux; GRUB detecta todos los sistemas."},
    {"titulo": "⚙️ Configurar GRUB", "enunciado": "Ordena los 3 pasos.",
     "pasos": ["Copia de seguridad (sudo cp /etc/default/grub /etc/default/grub.bak)", "Editar con sudo nano /etc/default/grub", "Aplicar con sudo update-grub"],
     "explicacion": "Sin sudo update-grub no cambia nada."},
    {"titulo": "🛠️ Reparar el arranque de Windows (UEFI)", "enunciado": "Ordena los pasos.",
     "pasos": ["Arrancar desde el USB de instalación", "Solucionar problemas", "Reparación de inicio (automática)", "Símbolo del sistema",
               "diskpart: list vol, select vol y assign letter=S", "bcdboot C:\\Windows /s S: /f UEFI"],
     "explicacion": "Prueba primero la reparación automática."},
]

# ---------------------------------------------------------------------------
# Verdadero o falso
# ---------------------------------------------------------------------------
VERDADERO_FALSO = [
    ("El sistema operativo es lo primero que se carga y lo último que se cierra.", True, "Sin él, ningún otro programa puede funcionar."),
    ("El navegador y el procesador de textos son software de base.", False, "Son aplicaciones; el software de base es el SO, los drivers y el firmware."),
    ("Un SO por lotes dialoga con el usuario.", False, "Eso es un SO interactivo; en los lotes el usuario no interviene."),
    ("En el tiempo compartido, la CPU se reparte en turnos muy cortos.", True, "Es típico de los SO interactivos."),
    ("Un SO de tiempo real responde en un tiempo máximo garantizado.", True, "Un retraso puede ser peligroso: airbag, torre de control."),
    ("MS-DOS es multiprogramación.", False, "Es monoprogramación: un solo programa en memoria."),
    ("En el multiproceso asimétrico, un procesador «jefe» reparte las tareas.", True, "En el simétrico, todos son iguales."),
    ("En un sistema en red, cada equipo tiene su propio SO.", True, "Y comparten recursos. En el distribuido parecen uno solo."),
    ("Un SO monolítico es un único programa grande y rápido.", True, "Si una parte falla, puede caer todo."),
    ("El sistema THE tiene 4 capas.", False, "Tiene los niveles 0 a 5 sobre el hardware; MINIX es el de 4 capas."),
    ("MINIX dio la idea para crear Linux.", True, "Lo creó un profesor para enseñar."),
    ("Un programa abierto dos veces son dos procesos.", True, "Cada uno con su propio PID."),
    ("Un programa guardado en el disco usa CPU y RAM.", False, "Está «dormido»: no usa CPU ni RAM."),
    ("Los hilos de un proceso comparten su memoria.", True, "Por eso crearlos es más rápido que crear procesos."),
    ("Si falla un hilo de Word, también se cierra Spotify.", False, "Los procesos no comparten memoria."),
    ("En cada núcleo puede haber varios procesos «en ejecución» a la vez.", False, "Solo uno; el resto espera en «listo»."),
    ("Un proceso que espera datos de la red está bloqueado.", True, "Cuando llegan, pasa a listo."),
    ("La memoria virtual usa parte del disco como si fuera RAM.", True, "Pero el disco es mucho más lento."),
    ("La paginación divide la memoria en trozos de tamaño distinto según el programa.", False, "Eso es la segmentación; las páginas son iguales."),
    ("La fragmentación externa son huecos libres sueltos y pequeños.", True, "Un proceso no cabe aunque la suma sea suficiente."),
    ("Un driver es un traductor entre el SO y un dispositivo concreto.", True, "Sin el driver, Windows no sabe cómo hablar con la impresora."),
    ("Con DMA, la CPU copia cada dato de la RAM al dispositivo.", False, "El dispositivo copia directamente a la RAM; la CPU solo da la orden."),
    ("El spooling es una cola de trabajos para un dispositivo lento.", True, "Ejemplo: la cola de impresión."),
    ("FAT32 permite ficheros de más de 4 GB.", False, "Máximo 4 GB por fichero."),
    ("NTFS tiene permisos, cifrado y journaling.", True, "Es el de Windows actual."),
    ("El journaling apunta en un «diario» los cambios antes de hacerlos.", True, "Si se va la luz, se recupera sin perder datos."),
    ("Un SAI es seguridad lógica.", False, "Es seguridad física: mantiene el equipo encendido."),
    ("Una máquina virtual está formada por ficheros que se pueden copiar.", True, "También se pueden hacer instantáneas."),
    ("VirtualBox es un hipervisor de tipo 1.", False, "Es de tipo 2 (alojado)."),
    ("Un hipervisor tipo 1 se instala directamente sobre el hardware.", True, "ESXi, Proxmox, Hyper-V y KVM."),
    ("Los contenedores como Docker comparten el núcleo del anfitrión.", True, "Por eso son ligeros."),
    ("Windows 11 en una VM necesita EFI y TPM 2.0.", True, "Obligatorio."),
    ("NAT deja ver la máquina virtual desde la red del aula.", False, "NAT sale a Internet pero no se ve desde la red; el puente sí."),
    ("La instalación limpia es la más recomendable.", True, "Se formatea y se instala desde cero."),
    ("La actualización conserva datos y programas, pero puede arrastrar errores.", True, "Se instala encima de la anterior."),
    ("Una ISO es un archivo con el disco de instalación completo.", True, "Como un DVD guardado en un solo archivo."),
    ("En MBR puede haber hasta 8 particiones primarias.", False, "Máximo 4 (o 3 primarias + 1 extendida)."),
    ("La partición extendida se formatea y guarda datos.", False, "Es solo una caja para las lógicas."),
    ("En GPT no hay extendidas ni lógicas.", True, "Todas son primarias (hasta 128 en Windows)."),
    ("MBR admite discos de más de 2 TB.", False, "Su máximo es 2 TB."),
    ("En GPT, si se daña la tabla, se recupera con la copia del final.", True, "En MBR se pierde."),
    ("Windows 11 se puede instalar en un disco MBR con BIOS.", False, "Necesita UEFI (GPT)."),
    ("Ubuntu solo necesita 2 particiones: EFI y raíz.", True, "Windows crea 4: EFI, MSR, C: y recuperación."),
    ("En Linux, la primera partición lógica de un disco MBR es sda5.", True, "Las lógicas empiezan siempre en 5."),
    ("Los discos NVMe de Linux empiezan en nvme1n1.", False, "Cuentan desde 0: nvme0n1."),
    ("El comando clean de diskpart borra la tabla de particiones entera.", True, "Practica solo en la máquina virtual."),
    ("Para multiarranque conviene instalar Linux primero y Windows al final.", False, "Windows primero y Linux al final."),
    ("Windows Boot Manager lee el almacén BCD.", True, "GRUB lee grub.cfg."),
    ("Antes de tocar el BCD hay que hacer una copia con bcdedit /export.", True, "Sin copia, no se toca."),
    ("Los cambios en /etc/default/grub se aplican solos.", False, "Hay que ejecutar sudo update-grub."),
    ("update-grub regenera grub.cfg y se pierden los cambios hechos a mano.", True, "Por eso se usa /etc/default/grub."),
    ("bootrec /rebuildbcd es para arranque BIOS/MBR de Windows.", True, "Junto con /fixmbr y /fixboot."),
    ("Con «grub rescue>» se usa Boot-Repair desde un USB de Ubuntu.", True, "Y después sudo grub-install y update-grub."),
]

# ---------------------------------------------------------------------------
# Quiz de teoría
# ---------------------------------------------------------------------------
BLOQUES = ["Qué es un SO e historia", "Tipos de SO", "Estructura", "Funciones, procesos e hilos", "Memoria",
           "Entrada/salida, archivos y seguridad", "Virtualización", "Instalación y particiones", "Gestores de arranque"]
Q0, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 = BLOQUES
QUIZ = [
    _q(Q0, "¿Qué es un sistema operativo?", "Un conjunto de programas que hace de intermediario entre el usuario y el hardware",
       ["Un programa de ofimática", "Una pieza de la placa base", "Un tipo de memoria"], "Hace que usar el ordenador sea fácil."),
    _q(Q0, "El SO es «software de base» porque…", "hace que el ordenador funcione y controla el hardware",
       ["sirve para tareas concretas del usuario", "se instala después del navegador", "solo existe en móviles"], "Ej.: SO, drivers y firmware."),
    _q(Q0, "El SO es lo primero que se carga y…", "lo último que se cierra", ["lo primero que se cierra", "lo que menos se usa", "lo que se borra al apagar"],
       "Sin él, ningún otro programa puede funcionar."),
    _q(Q0, "Analogía: el SO es la carretera y las aplicaciones son…", "los coches", ["los semáforos", "los peajes", "los mapas"], "Funcionan «encima» del SO."),
    _q(Q0, "¿Qué SO llevan la mayoría de los móviles?", "Android", ["macOS", "ChromeOS", "MS-DOS"], "iOS: iPhone y iPad."),
    _q(Q0, "ChromeOS se ve sobre todo en…", "Chromebooks de muchos colegios", ["servidores", "iPhone", "consolas antiguas"], "Linux: servidores, Internet y PC."),
    _q(Q0, "¿Cuál es software de base?", "Los controladores (drivers)", ["WhatsApp", "Un juego", "Un procesador de textos"], "También el SO y el firmware."),
    _q(Q0, "¿Qué generación tiene tarjetas perforadas y cintas, casi sin SO?", "La 1.ª (válvulas de vacío)", ["La 2.ª", "La 3.ª", "La 5.ª"], "Ej.: EXEC I."),
    _q(Q0, "CTSS (tiempo compartido) pertenece a la generación…", "2.ª (transistores)", ["1.ª", "4.ª", "5.ª"], "También EXEC II y EXEC 8."),
    _q(Q0, "OS/360 y UNIX son de la…", "3.ª (circuitos integrados)", ["1.ª", "2.ª", "5.ª"], "También CP/CMS y MULTICS."),
    _q(Q0, "MS-DOS y Windows son de la…", "5.ª (PC y redes)", ["1.ª", "2.ª", "3.ª"], "Con XENIX, NetWare, Solaris y Mac OS."),
    _q(Q1, "Un SO por lotes…", "agrupa muchos trabajos y los ejecuta seguidos sin que el usuario intervenga",
       ["dialoga con el usuario", "garantiza un tiempo máximo", "reparte la CPU en turnos"], "Ej.: un banco calcula las nóminas por la noche."),
    _q(Q1, "El tiempo compartido es típico de los SO…", "interactivos", ["por lotes", "de tiempo real", "monolíticos"], "La CPU se reparte en turnos muy cortos."),
    _q(Q1, "Los SO de tiempo real…", "responden en un tiempo máximo garantizado", ["son siempre los más rápidos", "no usan CPU", "solo existen en móviles"],
       "Un retraso puede ser peligroso."),
    _q(Q1, "¿Cuál es un ejemplo de tiempo real?", "Un airbag", ["Un editor de texto", "Las nóminas nocturnas", "Tu móvil"], "También torre de control, cajero y monitor de hospital."),
    _q(Q1, "Multiusuario significa que…", "varias personas trabajan a la vez en el mismo equipo", ["solo una persona lo usa a la vez", "tiene varios monitores", "tiene varios discos"],
       "Ej.: un servidor Linux."),
    _q(Q1, "Monoprogramación significa…", "un solo programa en memoria; el siguiente espera a que acabe", ["varios programas se turnan la CPU", "varios procesadores", "varios usuarios"], "Ej.: MS-DOS."),
    _q(Q1, "Multiprogramación significa…", "varios programas en memoria que se turnan la CPU", ["un solo programa", "un solo usuario", "un solo procesador"], "Ej.: Windows y Linux."),
    _q(Q1, "Multiproceso simétrico:", "varios procesadores iguales que se reparten el trabajo", ["un procesador jefe reparte las tareas", "un solo procesador", "varios equipos"],
       "Asimétrico: hay un procesador «jefe»."),
    _q(Q1, "En un sistema distribuido…", "muchos equipos parecen uno solo", ["un ordenador central hace todo", "cada equipo trabaja aislado", "no hay red"],
       "Centralizado: un ordenador central hace todo."),
    _q(Q2, "Un SO monolítico…", "es un único programa grande: rápido, pero si una parte falla puede caer todo",
       ["tiene muchas capas", "es siempre virtual", "solo existe en servidores"], "Ej.: MS-DOS."),
    _q(Q2, "En un SO por capas, cada capa solo usa…", "los servicios de la capa de abajo", ["los de la capa de arriba", "todos los de las demás", "ninguno"], "Si algo falla, sabes en qué capa buscar."),
    _q(Q2, "¿Cuántos niveles (sin contar el hardware) tiene THE?", "6 (del 0 al 5)", ["4", "5", "7"], "Del procesador al operador."),
    _q(Q2, "El nivel 0 de THE se encarga de…", "asignar el procesador y la multiprogramación", ["la memoria", "la E/S", "el operador"], "El jefe de cocina que reparte los fogones."),
    _q(Q2, "El nivel 1 de THE gestiona…", "la memoria principal y secundaria", ["el procesador", "los programas de usuario", "las órdenes del operador"], "La despensa y la nevera."),
    _q(Q2, "El nivel 3 de THE es…", "la gestión de entrada/salida", ["la memoria", "el operador", "el procesador"], "Los camareros."),
    _q(Q2, "MINIX tiene…", "4 capas", ["3 capas", "5 capas", "6 capas"], "Como la secretaría del instituto."),
    _q(Q2, "En MINIX, los procesos servidores…", "atienden las peticiones (uno la memoria y otro los archivos)", ["son los programas del usuario", "mueven el ratón", "son el hardware"],
       "Las ventanillas de secretaría."),
    _q(Q2, "MINIX lo creó un profesor para enseñar y dio la idea para crear…", "Linux", ["Windows", "MS-DOS", "macOS"], "Ej. de estructura en capas."),
    _q(Q2, "En cliente-servidor, si un servidor falla…", "el resto sigue", ["cae todo", "se apaga el hardware", "se borra el disco"], "Núcleo mínimo."),
    _q(Q2, "Una máquina virtual…", "simula varios ordenadores dentro de uno, cada uno con su SO", ["es un disco duro", "es un tipo de RAM", "es un virus"], "Ej.: VirtualBox."),
    _q(Q3, "Las 5 funciones del SO son…", "procesos, memoria, entrada/salida, archivos y seguridad", ["procesos, red, vídeo, sonido y archivos", "memoria, disco, CPU, red y pantalla", "solo procesos y memoria"], "Pro-Me-E/S-Ar-Se."),
    _q(Q3, "¿Qué es un programa?", "Un fichero guardado en el disco, «dormido»", ["Un programa en ejecución", "Un hilo", "Una ficha PCB"], "No usa CPU ni RAM."),
    _q(Q3, "Un proceso es…", "un programa en ejecución, cargado en la RAM, con un PID", ["un fichero en el disco", "un hilo", "un driver"], "Programa = receta; proceso = cocinarla."),
    _q(Q3, "Abres el Bloc de notas dos veces. ¿Cuántos procesos hay?", "2, cada uno con su PID", ["1", "0", "4"], "Y 1 solo programa (notepad.exe)."),
    _q(Q3, "La ficha del proceso (PCB) guarda…", "PID, estado, prioridad, memoria que usa y ficheros abiertos", ["solo el nombre", "las contraseñas", "la caché L3"], "Es su carnet."),
    _q(Q3, "Un hilo es…", "una tarea de un proceso, la unidad más pequeña que el SO reparte en la CPU", ["otro nombre del programa", "un proceso con su propia memoria", "un driver"], "Un proceso tiene al menos uno."),
    _q(Q3, "Los hilos de un mismo proceso…", "comparten su memoria", ["tienen cada uno su memoria", "no pueden trabajar a la vez", "son procesos distintos"], "Los cocineros comparten la nevera."),
    _q(Q3, "Crear un hilo, comparado con un proceso, es…", "más rápido", ["más lento", "igual", "imposible"], "Los hilos comparten la memoria."),
    _q(Q3, "Word y su corrector ortográfico son…", "dos hilos del mismo proceso", ["dos procesos", "dos programas", "dos drivers"], "Trabajan sobre el mismo documento."),
    _q(Q3, "Spotify y Word abiertos a la vez son…", "dos procesos", ["dos hilos", "un solo proceso", "un solo programa"], "Cada uno con su memoria."),
    _q(Q3, "¿Qué estados tiene un proceso?", "Nuevo, listo, en ejecución, bloqueado y terminado", ["Abierto, cerrado y colgado", "Nuevo, activo y borrado", "Listo y terminado solamente"], "Diagrama de estados."),
    _q(Q3, "Un proceso que espera una tecla o el disco está…", "bloqueado", ["listo", "en ejecución", "terminado"], "Pide E/S."),
    _q(Q3, "¿Cuántos procesos pueden estar «en ejecución» por núcleo?", "Solo uno a la vez", ["Todos", "Dos", "Ninguno"], "El resto espera en «listo»."),
    _q(Q3, "Cuando termina su E/S, un proceso bloqueado pasa a…", "listo", ["en ejecución", "nuevo", "terminado"], "Espera a que le toque la CPU."),
    _q(Q3, "Windows llama «subprocesos» a los…", "hilos", ["procesos hijos", "drivers", "servicios"], "Se ven en el Administrador de tareas › Rendimiento."),
    _q(Q4, "¿Qué memoria es la más rápida y pequeña de la jerarquía?", "Los registros", ["La caché de disco", "La RAM", "El SSD"], "Registros, caché, RAM, caché de disco y memoria auxiliar."),
    _q(Q4, "La memoria auxiliar (disco, SSD, USB, DVD) es…", "la más lenta, grande y barata", ["la más rápida", "la más cara", "la más pequeña"], "Como la biblioteca."),
    _q(Q4, "La protección de memoria garantiza que…", "ningún proceso entra en la memoria de otro", ["todos comparten la RAM", "no se usa el disco", "solo hay un proceso"], "Una de las funciones."),
    _q(Q4, "La compartición permite que…", "varios procesos usen la misma zona (el mismo programa abierto 2 veces)", ["nadie entre en otra zona", "se use el disco", "se borre la caché"], "Ahorra memoria."),
    _q(Q4, "La paginación divide la memoria en…", "trozos iguales (páginas)", ["trozos según el programa", "un solo trozo", "trozos de 1 GB"], "La segmentación usa segmentos."),
    _q(Q4, "La reubicación permite…", "colocar un proceso en cualquier hueco libre", ["mover el disco", "cambiar de SO", "borrar la RAM"], "No tiene que ir siempre en el mismo sitio."),
    _q(Q4, "El intercambio (swap) consiste en…", "pasar al disco lo que no se usa para hacer sitio", ["comprar más RAM", "cambiar de CPU", "copiar a USB"], "Memoria virtual."),
    _q(Q4, "La memoria virtual en Windows es…", "pagefile.sys", ["swap", "grub.cfg", "bootmgr"], "En Linux es swap."),
    _q(Q4, "El inconveniente de la memoria virtual es que…", "el disco es mucho más lento que la RAM", ["gasta RAM", "no se puede usar", "solo funciona en Linux"], "Pero permite abrir más programas."),
    _q(Q4, "Fragmentación interna:", "sobra espacio dentro del trozo asignado", ["hay huecos sueltos entre procesos", "el disco está lleno", "falta caché"], "La externa: huecos sueltos."),
    _q(Q4, "Hay tres huecos libres que suman 2,1 pero ninguno llega a 1,5. Un proceso de 1,5…", "no cabe: fragmentación externa", ["cabe sumando los huecos", "cabe en el disco", "se parte en dos"], "Necesita un hueco seguido."),
    _q(Q5, "Un controlador (driver) es…", "un pequeño programa que traduce entre el SO y un dispositivo concreto", ["una pieza de hardware", "un tipo de RAM", "un antivirus"], "Sin el driver de la impresora, Windows no sabe hablar con ella."),
    _q(Q5, "La pantalla táctil, el disco y la tarjeta de red son dispositivos de…", "entrada y salida", ["solo entrada", "solo salida", "ninguna"], "Hacen las dos cosas."),
    _q(Q5, "En una interrupción, la CPU…", "para un momento lo que hace, ejecuta la rutina de atención y vuelve", ["se apaga", "borra la RAM", "reinicia el SO"], "El periférico «levanta la mano»."),
    _q(Q5, "Con DMA…", "el dispositivo copia datos directamente a la RAM sin ocupar la CPU", ["la CPU copia cada dato", "no se usa la RAM", "solo se usa el USB"], "La CPU recibe un aviso al final."),
    _q(Q5, "El caching consiste en…", "guardar cerca lo que se usa mucho", ["hacer una cola", "usar memoria intermedia", "usar el disco como RAM"], "Ej.: el navegador guarda imágenes de webs."),
    _q(Q5, "El buffering es…", "una memoria intermedia que compensa velocidades distintas", ["una cola de impresión", "un driver", "una copia de seguridad"], "Ej.: YouTube carga unos segundos por adelantado."),
    _q(Q5, "El spooling es…", "una cola de trabajos para un dispositivo lento", ["una caché", "un buffer de vídeo", "un driver"], "Ej.: la cola de impresión."),
    _q(Q5, "Conectas un ratón nuevo y se detecta y se busca su controlador: es…", "Plug and Play + driver", ["DMA", "Spooling", "Swap"], "Queda listo para usar."),
    _q(Q5, "La extensión de un archivo (.docx, .jpg, .exe) indica…", "el tipo de archivo", ["su tamaño", "su dueño", "su contraseña"], "Atributos: tamaño, fecha, oculto, solo lectura."),
    _q(Q5, "FAT32 se usa en…", "memorias USB y tarjetas; ficheros de 4 GB como máximo", ["Windows actual", "Linux", "DVD"], "NTFS: Windows actual."),
    _q(Q5, "ext4 es el sistema de archivos de…", "Linux", ["Windows", "Mac antiguos", "DVD"], "EXT3 y EXT4 con journaling."),
    _q(Q5, "El journaling…", "apunta en un «diario» los cambios antes de hacerlos", ["borra archivos viejos", "comprime el disco", "cifra los datos"], "Si se va la luz, se recupera sin perder datos."),
    _q(Q5, "Usuario y contraseña, permisos, antivirus y cifrado son seguridad…", "lógica", ["física", "eléctrica", "de red solamente"], "Física: cámaras, salas con llave, antiincendios, SAI."),
    _q(Q6, "Un hipervisor es…", "el programa que reparte un ordenador real entre varias máquinas virtuales", ["un virus", "un tipo de RAM", "un disco"], "El administrador de la finca."),
    _q(Q6, "Antes de crear máquinas virtuales hay que activar en la UEFI…", "Intel VT-x o AMD-V (SVM)", ["Secure Boot", "XMP", "PXE"], "En el Administrador de tareas: «Virtualización: Habilitado»."),
    _q(Q6, "Una ventaja de las VM es…", "las instantáneas: volver atrás en segundos", ["que no usan RAM", "que no necesitan disco", "que son más rápidas que el equipo real"], "También aislamiento y probar sin tocar el equipo real."),
    _q(Q6, "Un hipervisor tipo 1 (nativo)…", "se instala directamente sobre el hardware (ESXi, Proxmox, Hyper-V, KVM)", ["es un programa sobre Windows", "es VirtualBox", "es Docker"], "Más rendimiento."),
    _q(Q6, "Un hipervisor tipo 2 (alojado)…", "es un programa sobre Windows, Linux o macOS (VirtualBox, VMware Workstation, Parallels)", ["se instala sobre el hardware", "es Proxmox", "es KVM"], "Más cómodo para aprender y probar."),
    _q(Q6, "Los contenedores (Docker)…", "aíslan aplicaciones que comparten el núcleo del anfitrión", ["simulan otro procesador", "son máquinas completas", "necesitan TPM"], "Ligeros."),
    _q(Q6, "La emulación…", "simula otro procesador y es lenta (QEMU)", ["comparte el núcleo", "es la más rápida", "es tipo 1"], "Ej.: emuladores de consolas."),
    _q(Q6, "La paravirtualización…", "hace que el invitado colabore con el hipervisor mediante drivers (Guest Additions, VirtIO)", ["oculta que es virtual", "simula otro procesador", "aísla aplicaciones"], "La completa: el invitado no sabe que es virtual."),
    _q(Q6, "En VirtualBox, «NAT»…", "sale a Internet pero no se ve desde la red", ["es un equipo más del aula", "no tiene Internet", "es el modo de Docker"], "Puente: un equipo más del aula."),
    _q(Q6, "Para Windows 11 en una VM hace falta…", "EFI y TPM 2.0", ["BIOS y MBR", "solo 1 GB de RAM", "un USB físico"], "Recomendado: 4 GB de RAM y 2 CPU."),
    _q(Q6, "Las Guest Additions sirven para…", "pantalla ajustable, portapapeles y carpetas compartidas", ["crear la ISO", "activar VT-x", "formatear el disco"], "Se instalan al terminar."),
    _q(Q7, "Una instalación limpia…", "formatea y instala desde cero; es la más recomendable", ["conserva datos y programas", "usa un fichero de respuestas", "clona un equipo"], "La actualización conserva datos."),
    _q(Q7, "Una instalación desatendida usa…", "un fichero de respuestas: autounattend.xml o autoinstall", ["un USB con Ventoy", "una VM", "una partición swap"], "Por red: PXE."),
    _q(Q7, "La clonación usa…", "la imagen de un equipo modelo (Clonezilla; sysprep en Windows)", ["una ISO de Microsoft", "un DVD", "PXE solamente"], "Imagen de un equipo modelo."),
    _q(Q7, "Una ISO es…", "un archivo con el disco de instalación completo", ["un tipo de partición", "un driver", "un hipervisor"], "En una VM no hace falta USB."),
    _q(Q7, "Ventoy sirve para…", "tener varias ISO en un mismo USB y elegir cuál arrancar", ["particionar discos", "crear VM", "instalar drivers"], "Rufus y Etcher copian una ISO."),
    _q(Q7, "La ISO se descarga siempre de…", "la web oficial (microsoft.com / ubuntu.com)", ["cualquier foro", "un USB ajeno", "una app de mensajes"], "Evita malware."),
    _q(Q7, "Una partición es…", "un trozo del disco que el SO usa como si fuera un disco distinto", ["un tipo de RAM", "un driver", "un hipervisor"], "Para separar sistema y datos, varios SO y zonas especiales."),
    _q(Q7, "El orden al preparar un disco nuevo es…", "tabla (MBR/GPT) → particiones → formatear", ["formatear → tabla → particiones", "particiones → formatear → tabla", "solo formatear"], "Cada partición recibe su sistema de archivos."),
    _q(Q7, "En MBR, el máximo de particiones primarias es…", "4 (o 3 primarias + 1 extendida)", ["2", "8", "128"], "GPT: hasta 128 en Windows."),
    _q(Q7, "La partición extendida…", "es una caja para meter lógicas; no se formatea", ["es la que arranca", "guarda el kernel", "solo existe en GPT"], "Solo una por disco."),
    _q(Q7, "En Linux, las particiones lógicas se numeran desde…", "5", ["1", "3", "0"], "sda5, sda6…"),
    _q(Q7, "El tamaño máximo de un disco MBR es…", "2 TB", ["512 GB", "4 TB", "9,4 ZB"], "GPT: prácticamente ilimitado (9,4 ZB)."),
    _q(Q7, "GPT arranca desde…", "la partición EFI (no hay activa)", ["la partición activa", "la extendida", "la swap"], "MBR: la partición marcada como activa."),
    _q(Q7, "Si la tabla de particiones MBR se daña…", "se pierde y el disco no arranca", ["se recupera con la copia del final", "no pasa nada", "se regenera sola"], "GPT guarda copia al final."),
    _q(Q7, "Windows 11 necesita…", "UEFI con GPT", ["BIOS con MBR", "solo MBR", "ninguna"], "Para decidir: equipo nuevo con UEFI → GPT."),
    _q(Q7, "La partición EFI es…", "FAT32 de 100–500 MB con los gestores de arranque (.efi)", ["NTFS de 16 MB", "ext4 de 1 GB", "swap"], "MSR: 16 MB reservados de Windows."),
    _q(Q7, "Windows crea 4 particiones; Ubuntu solo necesita…", "2: EFI y raíz (/)", ["1", "3", "5"], "La swap ahora es un archivo dentro de /."),
    _q(Q7, "La partición swap sirve para…", "la memoria virtual (y la hibernación)", ["guardar el kernel", "arrancar Windows", "guardar documentos"], "Tamaño como la RAM."),
    _q(Q7, "La partición /boot guarda…", "el kernel y los ficheros de GRUB", ["los documentos", "la hibernación", "WinRE"], "ext4, 1 GB."),
    _q(Q7, "En Linux, la segunda partición del segundo disco es…", "/dev/sdb2", ["/dev/sda2", "/dev/sdb5", "/dev/sdc1"], "a = 1.º, b = 2.º, c = 3.º."),
    _q(Q7, "La segunda partición del segundo NVMe es…", "/dev/nvme1n1p2", ["/dev/nvme2n1p2", "/dev/nvme1n1p1", "/dev/sdb2"], "Los NVMe cuentan desde 0."),
    _q(Q7, "En Windows los discos se numeran desde…", "0 (Disco 0, Disco 1…)", ["1", "A", "5"], "Las particiones llevan letra: C:, D:…"),
    _q(Q7, "¿Con qué comando ves el árbol de discos en Linux?", "lsblk", ["diskpart", "bcdedit", "update-grub"], "fdisk -l da los detalles de la tabla."),
    _q(Q7, "En fdisk -l, «Tipo de etiqueta de disco: dos» significa…", "MBR", ["GPT", "NTFS", "ext4"], "Si pone gpt, es GPT."),
    _q(Q7, "En fdisk, los Id 83, 82, 7 y b son…", "Linux, Linux swap, NTFS y FAT32", ["MBR, GPT, EFI y MSR", "ext2, ext3, ext4 y XFS", "Todas ocultas"], "Id 5 = extendida."),
    _q(Q7, "El comando clean de diskpart…", "borra la tabla de particiones entera", ["limpia la caché", "formatea una partición", "borra la papelera"], "Practica solo en la máquina virtual."),
    _q(Q7, "En la instalación de Windows 11, Mayús + F10…", "abre un CMD", ["reinicia", "formatea", "activa el TPM"], "Útil para saltarse requisitos en VM."),
    _q(Q7, "Ubuntu con «sesión en vivo»…", "funciona desde el USB sin instalar; útil para reparar", ["borra el disco", "instala Windows", "solo funciona en VM"], "Try or Install Ubuntu."),
    _q(Q7, "Si vas a instalar varios sistemas, el orden recomendado es…", "Windows primero, Linux al final", ["Linux primero", "da igual", "macOS al final siempre"], "Windows sobrescribe el gestor de arranque."),
    _q(Q8, "Windows Boot Manager lee…", "el almacén BCD", ["grub.cfg", "/etc/fstab", "initrd"], "GRUB lee grub.cfg."),
    _q(Q8, "El arranque de Ubuntu con UEFI es…", "shimx64.efi → grubx64.efi → vmlinuz + initrd → systemd", ["bootmgfw.efi → winload.efi", "bootmgr → ntldr", "grub.cfg → bcdedit"], "Windows: bootmgfw.efi → BCD → winload.efi."),
    _q(Q8, "Las herramientas de Windows para configurar el arranque son…", "bcdedit, msconfig y EasyBCD", ["update-grub y nano", "Grub Customizer", "lsblk y fdisk"], "Todas cambian el mismo almacén: el BCD."),
    _q(Q8, "Las herramientas de GRUB son…", "/etc/default/grub, update-grub y Grub Customizer", ["bcdedit y msconfig", "diskpart", "EasyBCD"], "Configuración en Ubuntu."),
    _q(Q8, "¿Por qué instalar Windows antes que Linux?", "Windows sobrescribe el gestor de arranque y no ve Linux; GRUB detecta todos los sistemas", ["Linux ocupa más", "Windows no cabe después", "GRUB solo funciona primero"], "El orden de instalación importa."),
    _q(Q8, "Windows no aparece en GRUB: ¿qué haces?", "GRUB_DISABLE_OS_PROBER=false y sudo update-grub", ["bcdedit /timeout", "reinstalar Linux", "borrar la EFI"], "Para que GRUB detecte otros sistemas."),
    _q(Q8, "Antes de tocar el BCD…", "haz una copia con bcdedit /export C:\\copiabcdedit", ["reinicia", "borra la EFI", "usa diskpart clean"], "Para restaurar: bcdedit /import."),
    _q(Q8, "bcdedit /timeout 45…", "pone 45 segundos de espera en el menú", ["borra 45 entradas", "pone 45 sistemas", "reinicia en 45 s"], "El predeterminado son 30 s."),
    _q(Q8, "En bcdedit, {current} es…", "el sistema con el que has arrancado", ["el que arranca por defecto", "el administrador de arranque", "Windows XP"], "{default}: el que arranca por defecto."),
    _q(Q8, "EasyBCD es…", "bcdedit con ventanas", ["un gestor de Linux", "un antivirus", "un hipervisor"], "Lo que hagas en uno se ve en el otro."),
    _q(Q8, "En /etc/default/grub, GRUB_TIMEOUT es…", "los segundos de espera", ["la entrada por defecto", "el tema", "la contraseña"], "GRUB_DEFAULT=0: la primera entrada."),
    _q(Q8, "Sin «sudo update-grub»…", "los cambios en /etc/default/grub no se aplican", ["se aplican solos", "se reinicia el equipo", "se borra GRUB"], "Es obligatorio."),
    _q(Q8, "Si editas grub.cfg a mano y luego ejecutas update-grub…", "los cambios se pierden", ["se guardan para siempre", "se duplican", "se aplican a Windows"], "update-grub regenera grub.cfg."),
    _q(Q8, "Grub Customizer permite…", "ordenar, renombrar entradas y cambiar el tiempo de espera de forma gráfica", ["particionar", "reinstalar Windows", "activar VT-x"], "Guardar = aplicar y actualizar GRUB."),
    _q(Q8, "Si no ves el menú de GRUB…", "mantén Mayús (BIOS) o pulsa Esc (UEFI) al arrancar", ["pulsa Supr", "reinstala", "usa bcdedit"], "Al arrancar."),
    _q(Q8, "En el modo recuperación de GRUB, «fsck» sirve para…", "comprobar los sistemas de archivos", ["reparar paquetes", "activar la red", "liberar espacio"], "dpkg: paquetes; clean: espacio."),
    _q(Q8, "Para reparar el arranque de Windows con UEFI/GPT usas…", "diskpart (asignar letra a la EFI) y bcdboot C:\\Windows /s S: /f UEFI", ["bootrec /fixmbr", "grub-install", "update-grub"], "Prueba antes la reparación automática."),
    _q(Q8, "Para reparar Windows con BIOS/MBR usas…", "bootrec /fixmbr, /fixboot y /rebuildbcd", ["bcdboot /f UEFI", "grub-install", "bcdedit /timeout"], "En WinRE, Windows puede no estar en C: (comprueba con list vol)."),
    _q(Q8, "Con «grub rescue>» o si no arranca ningún sistema en Linux…", "Boot-Repair desde un USB de Ubuntu", ["bootrec /fixmbr", "msconfig", "EasyBCD"], "Después: sudo grub-install /dev/sda y sudo update-grub."),
]

# ---------------------------------------------------------------------------
# Chuleta
# ---------------------------------------------------------------------------
CHULETA = """
### 🧱 Qué es un SO
Programas que hacen de **intermediario** entre usuario y hardware. Es **software de base** (SO, drivers, firmware); las aplicaciones funcionan encima.
Generaciones: 1.ª válvulas · 2.ª transistores (CTSS) · 3.ª circuitos integrados (OS/360, UNIX) · 4.ª microprocesadores (BSD UNIX, VMS) · 5.ª PC y redes (MS-DOS, Windows).

### 🧭 Tipos (5 criterios)
| Criterio | Tipos |
|---|---|
| Tiempo de respuesta | Por lotes · Interactivo (tiempo compartido) · Tiempo real |
| Usuarios | Monousuario · Multiusuario |
| Procesos | Monoprogramación · Multiprogramación |
| Procesadores | Monoproceso · Multiproceso simétrico / asimétrico |
| Red | Centralizado · En red · Distribuido |

### 🏗️ Estructura
Monolítico (MS-DOS) · Capas **THE** (niveles 0-5: procesador, memoria, E/S, comunicación, programas, operador) · **MINIX** (4 capas) · Máquina virtual · Cliente-servidor.

### ⚙️ Las 5 funciones
Procesos · Memoria · Entrada/Salida · Archivos · Seguridad (**Pro-Me-E/S-Ar-Se**).

### 🔄 Procesos e hilos
- Programa (en disco) ≠ **proceso** (en RAM, con PID, PCB) ≠ **hilo** (tarea del proceso; comparte su memoria).
- Estados: nuevo → listo → en ejecución ⇄ bloqueado → terminado.

### 🧠 Memoria
Jerarquía: registros → caché → RAM → caché de disco → memoria auxiliar. Protección · compartición · particionamiento (**paginación** = trozos iguales, **segmentación** = según el programa) · reubicación · **swap**. Memoria virtual: pagefile.sys (Windows) / swap (Linux). Fragmentación **interna** (sobra dentro) y **externa** (huecos sueltos).

### 🔌 Entrada/salida, archivos y seguridad
Driver = traductor. **Interrupción** · **DMA** · **Caching** · **Buffering** · **Spooling** · Plug and Play.
FAT16 · FAT32 (4 GB máx.) · NTFS (Windows) · ext4 (Linux, journaling) · CDFS/UDF · HFS+/APFS.
Seguridad lógica (contraseñas, permisos, antivirus, cifrado, copias) y física (cámaras, llaves, antiincendios, SAI).

### 📦 Virtualización
Hipervisor **tipo 1** (ESXi, Proxmox, Hyper-V, KVM) frente a **tipo 2** (VirtualBox, VMware Workstation, Parallels). Completa · paravirtualización (Guest Additions, VirtIO) · contenedores (Docker) · emulación (QEMU). Activa **VT-x / AMD-V**. Windows 11 en VM: EFI + TPM 2.0.

### 💽 Particiones
| | MBR | GPT |
|---|---|---|
| Máximo | 2 TB | 9,4 ZB |
| Particiones | 4 primarias (o 3 + extendida) | hasta 128 |
| Firmware | BIOS | UEFI |
| Arranca | partición activa | partición EFI |
| Si se daña | se pierde | copia al final |

EFI (FAT32, 100-500 MB) · MSR (16 MB) · Sistema C: o / · Datos D: o /home · swap · /boot · Recuperación WinRE.
Linux: /dev/sda, sdb… · sda1 · lógicas desde **sda5** · NVMe: nvme0n1p1 (desde 0).

### 🚀 Gestores de arranque
- **Windows Boot Manager**: bootmgfw.efi → BCD → winload.efi. Herramientas: `bcdedit`, `msconfig`, EasyBCD. Copia primero: `bcdedit /export`.
- **GRUB**: shimx64.efi → grubx64.efi → grub.cfg → vmlinuz + initrd → systemd (PID 1). Edita `/etc/default/grub` y aplica con `sudo update-grub`.
- Multiarranque: **Windows primero, Linux al final**.
- Reparar Windows UEFI: `bcdboot C:\\Windows /s S: /f UEFI` · BIOS: `bootrec /fixmbr /fixboot /rebuildbcd` · GRUB: Boot-Repair.
"""
