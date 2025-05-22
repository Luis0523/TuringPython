import pdfplumber
from fpdf import FPDF

# Definimos las cadenas a detectar y sus traducciones
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

        # Intentar encontrar la secuencia empezando en cada índice posible del texto
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
                    # Secuencia rota, salir del bucle
                    break
                
                # Si ya completó la secuencia, salir del bucle
                if progreso == len(secuencia):
                    break

            # Guardar mejor progreso y traducción para esta cadena
            if progreso > mejor_progreso:
                mejor_progreso = progreso
                mejor_traduccion = mensaje_traducido

            # Si se completa al 100%, no tiene sentido seguir buscando
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



def generar_reporte_mensajes(resultados):
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

    nombre_archivo = "reporte_mensajes_ocultos.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo

# --- Código principal ---
if __name__ == "__main__":
    archivo_pdf = "documento.pdf"  # Cambia esto por el nombre de tu archivo PDF
    texto = extraer_texto_pdf(archivo_pdf)
    resultados = buscar_cadenas_en_texto(texto, cadenas)
    ruta_reporte = generar_reporte_mensajes(resultados)
    print(f"Reporte generado: {ruta_reporte}")
