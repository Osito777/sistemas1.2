# 🖥️ Sistemas Quest

Juego interactivo hecho con **Streamlit** para estudiar **Sistemas Informáticos**.
Tiene dos unidades, que se cambian desde el menú lateral:

| Unidad | Temas |
|---|---|
| **UDI 1 · Arquitectura y componentes** (SISTEMAS 6) | Sistema informático (hardware, software, firmware, personas), generaciones, sistemas de numeración y conversiones, suma y resta binaria, unidades de medida, ASCII, paridad, formatos, arquitectura Von Neumann y Harvard, hardware por dentro (placa, zócalos, procesador, RAM, PCIe, almacenamiento, GPU, conectores, fuente), arranque (POST, BIOS/UEFI), software y licencias. |
| **Tema 2 · Sistemas operativos** (PARTE2) | Qué es un SO, historia, tipos (5 criterios), estructura (monolítico, THE, MINIX, cliente-servidor), funciones, procesos e hilos, memoria, entrada/salida, archivos, seguridad, virtualización, instalación, particiones (MBR/GPT), gestores de arranque (Windows Boot Manager y GRUB). |

## 🎮 Modos de juego (en cada unidad)

| Modo | Qué hace |
|---|---|
| 🧩 Clasifica | Casos con desplegables por tema (6 temas en la UDI 1 y 15 en el Tema 2). |
| 🧮 Entrenador de cálculos | Ejercicios **generados al azar**: cambios de base, sumas y restas binarias, unidades, ASCII, paridad, potencia de la fuente (UDI 1); nombres de discos en Linux, fragmentación y MBR/GPT (Tema 2). |
| 🔢 Ordena la secuencia | Arranque, ciclo de la CPU, estados de un proceso, capas THE, instalación de Windows y Ubuntu, reparar el arranque… |
| ❓ Verdadero o falso | Afirmaciones con explicación. |
| 🧠 Quiz de teoría | Preguntas por bloques. |
| ⚡ Reto mixto | 15 preguntas al azar con nota final. |
| 🧪 Laboratorio | Herramientas sin puntos: conversor de bases, fuente de alimentación, paridad, tabla ASCII, nombres de discos en Linux, fragmentación, plan de VM, ¿MBR o GPT? |
| 📖 Chuleta | Resumen de teoría de la unidad. |

Incluye puntos, racha 🔥, niveles (de *Usuario* a *Root*) y precisión.

## 📁 Estructura

```
├── app.py             # Interfaz y lógica del juego
├── preguntas.py       # Contenido y generadores de la UDI 1
├── preguntas_t2.py    # Contenido y generadores del Tema 2
├── requirements.txt   # Dependencias
└── README.md
```

## ▶️ Ejecutar en local

```bash
git clone https://github.com/TU_USUARIO/sistemas-quest.git
cd sistemas-quest
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Publicarlo gratis (Streamlit Community Cloud)

1. Sube este proyecto a un repositorio **nuevo** de GitHub (los 5 archivos en la raíz).
2. Entra en <https://share.streamlit.io> con tu cuenta de GitHub.
3. Pulsa **Create app**, elige el repositorio, rama `main` y archivo principal `app.py`.
4. Pulsa **Deploy** y comparte el enlace.

## ➕ Añadir contenido

Edita `preguntas.py` (UDI 1) o `preguntas_t2.py` (Tema 2):

- **Verdadero/falso**: añade una tupla `("afirmación", True/False, "explicación")`.
- **Quiz**: copia una llamada a `_q(...)` (la respuesta correcta va primero; el juego baraja las opciones).
- **Clasifica**: añade un caso con `_c(...)` a la lista del tema.
- **Ordena**: añade un diccionario a `ORDENAR` con los pasos en el orden correcto.

## 👥 Autores

Manuel Ramos Perca · Joel Flores Lopez
