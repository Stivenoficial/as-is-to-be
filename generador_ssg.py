import os
import sys
import subprocess
import webbrowser
import uuid

# --- AUTO-INSTALADOR ---
try:
    import mammoth
except ImportError:
    print("📦 Instalando mammoth...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mammoth", "--break-system-packages"])
    import mammoth

# --- CONFIGURACIÓN DE CARPETAS ---
CARPETA_WORDS = r"C:\Users\DOL\.gemini\antigravity\scratch\MapeoProcesos"
CARPETA_WEB = r"C:\Users\DOL\.gemini\antigravity\scratch\MapeoProcesos\docs" 
CARPETA_IMAGENES = os.path.join(CARPETA_WEB, "images") # <--- NUEVA CARPETA PARA IMÁGENES

def asegurar_carpetas():
    if not os.path.exists(CARPETA_WORDS): os.makedirs(CARPETA_WORDS)
    if not os.path.exists(CARPETA_WEB): os.makedirs(CARPETA_WEB)
    if not os.path.exists(CARPETA_IMAGENES): os.makedirs(CARPETA_IMAGENES)
        
    ruta_nojekyll = os.path.join(CARPETA_WEB, ".nojekyll")
    if not os.path.exists(ruta_nojekyll):
        with open(ruta_nojekyll, "w") as f: pass

# --- MANEJADOR DE IMÁGENES (Extrae y guarda como archivo real) ---
def manejar_imagen(image):
    ext = image.content_type.split("/")[-1]
    if ext == "jpeg": ext = "jpg"
    
    # Genera un nombre único para la imagen
    nombre_imagen = f"img_{uuid.uuid4().hex[:8]}.{ext}"
    ruta_imagen = os.path.join(CARPETA_IMAGENES, nombre_imagen)
    
    # Guarda la imagen en la carpeta docs/images/
    with open(ruta_imagen, "wb") as f:
        with image.open() as image_bytes:
            f.write(image_bytes.read())
            
    # Le dice al HTML dónde encontrarla
    return {"src": f"images/{nombre_imagen}"}

def obtener_estilos_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; background-color: #f8f9fa; color: #333; }
        .sidebar { width: 280px; background-color: #2c3e50; color: white; padding: 20px 0; overflow-y: auto; flex-shrink: 0; }
        .sidebar h2 { text-align: center; font-size: 1.2rem; margin-bottom: 20px; }
        .sidebar ul { list-style: none; padding: 0; margin: 0; }
        .sidebar li a { display: block; color: #bdc3c7; text-decoration: none; padding: 12px 25px; font-size: 0.95rem; transition: 0.3s; }
        .sidebar li a:hover { background-color: #34495e; color: white; border-left: 4px solid #27ae60; }
        .content { flex-grow: 1; padding: 50px; overflow-y: auto; background-color: white; }
        .document-container { max-width: 900px; margin: 0 auto; line-height: 1.6; }
        h1, h2, h3 { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f4f7f6; }
        
        /* --- ESTILOS MEJORADOS PARA IMÁGENES --- */
        img {
            max-width: 100%; /* Nunca se saldrá de la pantalla */
            height: auto;
            border-radius: 6px;
            margin: 20px 0;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15); /* Sombreado elegante */
            display: block;
        }
    </style>
    """

def generar_html_base(titulo, enlaces_sidebar, contenido_html):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        {obtener_estilos_css()}
    </head>
    <body>
        <div class="sidebar">
            <h2>📚 MIS MANUALES</h2>
            <ul><li><a href="index.html">🏠 Inicio</a></li>{enlaces_sidebar}</ul>
        </div>
        <div class="content"><div class="document-container">{contenido_html}</div></div>
    </body>
    </html>
    """

def main():
    asegurar_carpetas()
    archivos_docx =[f for f in os.listdir(CARPETA_WORDS) if f.endswith('.docx')]
    
    if not archivos_docx:
        print("⚠️ No hay archivos .docx.")
        return

    enlaces_sidebar = ""
    for archivo in archivos_docx:
        nombre_sin_ext = archivo.replace('.docx', '')
        url_archivo = f"{nombre_sin_ext.replace(' ', '%20')}.html"
        enlaces_sidebar += f'<li><a href="{url_archivo}">📄 {nombre_sin_ext}</a></li>\n'

    for archivo in archivos_docx:
        ruta_docx = os.path.join(CARPETA_WORDS, archivo)
        nombre_sin_ext = archivo.replace('.docx', '')
        ruta_html = os.path.join(CARPETA_WEB, f"{nombre_sin_ext}.html")

        print(f"Procesando documento: {archivo} ...")
        
        # Aquí le decimos a mammoth que use nuestra función para guardar las imágenes
        with open(ruta_docx, "rb") as docx_file:
            resultado = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.img_element(manejar_imagen))
            contenido_convertido = resultado.value
        
        html_final = generar_html_base(nombre_sin_ext, enlaces_sidebar, f"<h1>{nombre_sin_ext}</h1>" + contenido_convertido)
        
        with open(ruta_html, "w", encoding="utf-8") as html_file:
            html_file.write(html_final)

    html_inicio = generar_html_base("Inicio", enlaces_sidebar, "<h1>Bienvenido</h1><p>Selecciona un manual del menú de la izquierda.</p>")
    ruta_index = os.path.join(CARPETA_WEB, "index.html")
    with open(ruta_index, "w", encoding="utf-8") as html_file:
        html_file.write(html_inicio)

    print(f"\n🚀 ¡Sitio listo! Todo guardado en '{CARPETA_WEB}'.")
    webbrowser.open("file://" + os.path.abspath(ruta_index))

if __name__ == "__main__":
    main()