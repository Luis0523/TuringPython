import pdfplumber
from fpdf import FPDF
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
# Definición de cadenas y funciones originales (igual que antes)
cadenas = [
    {
        "secuencia": ["La", "implementación", "de", "este", "prodificultadecto", "involucra", "el","uso"],
        "traduccion": {
            "La": "Los",
            "implementación": "estudiantes", 
            "de": "de",
            "este": "quinto",
            "prodificultadecto": "semestre",
            "involucra": "perdieron",
            "el": "el",
            "uso":"curso"
        }
    },
    {
        "secuencia": ["La", "programación", "de", "este", "proceso", "requiere", "una", "estructura", "sólida"],
        "traduccion": {
            "La": "Los",
            "programación": "alumnos",
            "de": "del",
            "este": "curso",
            "proceso": "final",
            "requiere": "revisar",
            "una": "su",
            "estructura": "entrega",
            "sólida": "completa"
        }
    }
]

def extraer_texto_pdf(archivo_pdf):
    with pdfplumber.open(archivo_pdf) as pdf:
        texto_completo = ""
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + " "
    return texto_completo.strip()

def buscar_cadenas_en_texto(texto, cadenas):
    palabras_texto = texto.split()
    resultados = []

    for cadena in cadenas:
        secuencia = cadena["secuencia"]
        traduccion = cadena["traduccion"]
        mejor_progreso = 0
        mejor_traduccion = []

        for i in range(len(palabras_texto)):
            progreso = 0
            mensaje_traducido = []

            for j in range(i, len(palabras_texto)):
                if progreso < len(secuencia) and palabras_texto[j].lower() == secuencia[progreso].lower():
                    palabra_clave = secuencia[progreso]
                    palabra_traducida = traduccion.get(palabra_clave, palabra_clave)
                    mensaje_traducido.append(palabra_traducida)
                    progreso += 1
                elif progreso > 0 and progreso < len(secuencia) and palabras_texto[j].lower() != secuencia[progreso].lower():
                    break

                if progreso == len(secuencia):
                    break

            if progreso > mejor_progreso:
                mejor_progreso = progreso
                mejor_traduccion = mensaje_traducido

            if mejor_progreso == len(secuencia):
                break

        porcentaje = (mejor_progreso / len(secuencia)) * 100
        resultado = {
            "cadena_original": " ".join(secuencia),
            "mensaje_traducido": " ".join(mejor_traduccion) if mejor_progreso > 0 else "",
            "completitud": porcentaje,
            "completo": mejor_progreso == len(secuencia)
        }
        resultados.append(resultado)

    return resultados

def generar_reporte_mensajes(resultados, ruta_guardado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Reporte de Mensajes Ocultos Detectados", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)

    for idx, res in enumerate(resultados, start=1):
        pdf.cell(0, 10, f"Mensaje {idx}:", ln=True)
        pdf.multi_cell(0, 10, f"Cadena original: {res['cadena_original']}")
        if res["completo"]:
            pdf.multi_cell(0, 10, f"Mensaje traducido completo: {res['mensaje_traducido']}")
        else:
            if res['mensaje_traducido']:
                pdf.multi_cell(0, 10, f"Mensaje traducido parcial: {res['mensaje_traducido']}")
            else:
                pdf.multi_cell(0, 10, "No se detectó mensaje.")
        pdf.cell(0, 10, f"Completitud: {res['completitud']:.2f}%", ln=True)
        pdf.ln(5)

    pdf.output(ruta_guardado)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis de Mensajes Ocultos en PDF")
        self.geometry("600x280")
        self.resizable(False, False)

        # Etiqueta y entrada para archivo PDF origen
        self.label_origen = tk.Label(self, text="Archivo PDF de origen:")
        self.label_origen.pack(anchor="w", padx=10, pady=(10,0))

        frame_origen = tk.Frame(self)
        frame_origen.pack(fill="x", padx=10)
        self.entry_origen = tk.Entry(frame_origen)
        self.entry_origen.pack(side="left", fill="x", expand=True)
        self.btn_origen = tk.Button(frame_origen, text="Seleccionar...", command=self.seleccionar_origen)
        self.btn_origen.pack(side="right", padx=(5,0))

        # Etiqueta y entrada para ruta guardado
        self.label_destino = tk.Label(self, text="Guardar reporte en:")
        self.label_destino.pack(anchor="w", padx=10, pady=(15,0))

        frame_destino = tk.Frame(self)
        frame_destino.pack(fill="x", padx=10)
        self.entry_destino = tk.Entry(frame_destino)
        self.entry_destino.pack(side="left", fill="x", expand=True)
        self.btn_destino = tk.Button(frame_destino, text="Seleccionar...", command=self.seleccionar_destino)
        self.btn_destino.pack(side="right", padx=(5,0))

        # Barra de progreso + label de porcentaje
        frame_progress = tk.Frame(self)
        frame_progress.pack(fill="x", padx=10, pady=15)
        self.progress = ttk.Progressbar(frame_progress, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True)
        self.label_progress = tk.Label(frame_progress, text="0%")
        self.label_progress.pack(side="right", padx=(10,0))

        # Botones Iniciar y Cerrar
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)
        self.btn_iniciar = tk.Button(frame_botones, text="Iniciar análisis", command=self.iniciar_analisis, width=15)
        self.btn_iniciar.pack(side="left", padx=10)
        self.btn_cerrar = tk.Button(frame_botones, text="Cerrar", command=self.destroy, width=15)
        self.btn_cerrar.pack(side="right", padx=10)

        # Variables para control de proceso simulado
        self.pasos = [0, 30, 60, 90, 100]
        self.etapa_actual = 0

    def seleccionar_origen(self):
        archivo = filedialog.askopenfilename(
            title="Selecciona el archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if archivo:
            self.entry_origen.delete(0, tk.END)
            self.entry_origen.insert(0, archivo)

    def seleccionar_destino(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar reporte como",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if archivo:
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, archivo)

    def iniciar_analisis(self):
        origen = self.entry_origen.get()
        destino = self.entry_destino.get()

        if not origen:
            messagebox.showwarning("Aviso", "Selecciona un archivo PDF de origen.")
            return
        if not destino:
            messagebox.showwarning("Aviso", "Selecciona la ruta para guardar el reporte.")
            return

        # Desactivar botones mientras corre
        self.btn_iniciar.config(state="disabled")
        self.btn_origen.config(state="disabled")
        self.btn_destino.config(state="disabled")

        self.etapa_actual = 0
        self.progress["value"] = 0
        self.label_progress.config(text="0%")

        # Empezar la simulación del proceso
        self.proceso_simulado(origen, destino)

    def proceso_simulado(self, origen, destino):
        etapas = len(self.pasos)

        try:
            # Simular trabajo con delays en cada etapa
            if self.etapa_actual == 0:
                # Extraer texto PDF (puede ser rápido)
                extraer_texto_pdf(origen)  # No guardamos resultado aquí para simplicidad
            elif self.etapa_actual == 1:
                # Buscar cadenas
                # para simular un poco más lento, hacemos delay
                pass
            elif self.etapa_actual == 2:
                # Generar reporte
                pass

            # Actualizar barra y label
            valor = self.pasos[self.etapa_actual]
            self.progress["value"] = valor
            self.label_progress.config(text=f"{valor}%")

            self.etapa_actual += 1

            if self.etapa_actual < etapas:
                # Esperar 600 ms antes de la siguiente etapa para que se note el progreso
                self.after(600, lambda: self.proceso_simulado(origen, destino))
            else:
                # Última etapa: hacemos realmente todo el proceso completo, para asegurar que funciona bien
                texto = extraer_texto_pdf(origen)
                resultados = buscar_cadenas_en_texto(texto, cadenas)
                generar_reporte_mensajes(resultados, destino)
                self.progress["value"] = 100
                self.label_progress.config(text="100%")
                messagebox.showinfo("Éxito", f"Reporte generado correctamente:\n{destino}")
                # Reactivar botones
                self.btn_iniciar.config(state="normal")
                self.btn_origen.config(state="normal")
                self.btn_destino.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
            self.progress["value"] = 0
            self.label_progress.config(text="0%")
            self.btn_iniciar.config(state="normal")
            self.btn_origen.config(state="normal")
            self.btn_destino.config(state="normal")
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
