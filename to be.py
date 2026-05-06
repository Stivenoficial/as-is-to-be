import webbrowser
import os

def get_common_styles():
    return """
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .canvas {
                background-color: white;
                background-image: 
                    linear-gradient(#f0f0f0 1px, transparent 1px),
                    linear-gradient(90deg, #f0f0f0 1px, transparent 1px);
                background-size: 20px 20px;
                border: 3px solid #1a1a1a;
                display: flex;
                position: relative;
                min-width: 1850px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-top: 20px;
            }

            .main-label {
                writing-mode: vertical-rl;
                transform: rotate(180deg);
                background: #27ae60; 
                color: white;
                padding: 15px;
                font-weight: 700;
                text-align: center;
                border-right: 3px solid #1a1a1a;
                font-size: 1.1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                letter-spacing: 2px;
                z-index: 10;
            }

            .grid-container {
                display: grid;
                /* Col 1: Headers | Col 2: Start | Cols 3-9: Pasos | Col 10: End */
                grid-template-columns: 160px 100px repeat(7, 200px) 120px;
                grid-template-rows: 160px 160px 160px;
                position: relative;
                flex-grow: 1;
            }

            .lane-line {
                grid-column: 1 / -1;
                border-bottom: 3px solid #1a1a1a;
                z-index: 1;
            }
            .lane-line:nth-child(1) { grid-row: 1; }
            .lane-line:nth-child(2) { grid-row: 2; }
            .lane-line:nth-child(3) { grid-row: 3; border-bottom: none; }

            .header {
                grid-column: 1;
                background: white;
                border-right: 3px solid #1a1a1a;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-weight: 700;
                font-size: 0.85rem;
                padding: 10px;
                z-index: 5;
            }
            .header-1 { grid-row: 1; }
            .header-2 { grid-row: 2; }
            .header-3 { grid-row: 3; }
            
            .header span {
                font-weight: 400;
                font-size: 0.7rem;
                margin-top: 5px;
                color: #555;
            }

            .cell {
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                z-index: 10;
            }

            .node {
                width: 140px;
                min-height: 70px;
                background: white;
                border: 1px solid #1a1a1a;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-size: 0.75rem;
                padding: 10px;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.05);
                position: relative;
            }

            .node-title {
                font-weight: 700;
                margin-bottom: 4px;
            }

            .node-desc {
                font-size: 0.65rem;
                color: #444;
            }

            .node-manual {
                background-color: #fffaf0;
                border-color: #f39c12;
            }
            .node-manual::after {
                content: "👤 MANUAL";
                position: absolute;
                top: -10px;
                right: -10px;
                background: #f39c12;
                color: white;
                font-size: 0.55rem;
                padding: 3px 6px;
                border-radius: 4px;
                font-weight: 700;
                z-index: 20;
            }

            .node-automation {
                background-color: #e8f4fd;
                border: 2px solid #2980b9;
                color: #2c3e50;
            }
            .node-automation::after {
                content: "⚙️ SISTEMA";
                position: absolute;
                top: -10px;
                right: -10px;
                background: #2980b9;
                color: white;
                font-size: 0.55rem;
                padding: 3px 6px;
                border-radius: 4px;
                font-weight: 700;
                z-index: 20;
            }

            .node-exception {
                background-color: #ffeaea;
                border: 2px solid #e74c3c;
                color: #c0392b;
            }
            .node-exception::after {
                content: "⚠️ ALERTA";
                position: absolute;
                top: -10px;
                right: -10px;
                background: #e74c3c;
                color: white;
                font-size: 0.55rem;
                padding: 3px 6px;
                border-radius: 4px;
                font-weight: 700;
                z-index: 20;
            }

            .node-start {
                width: 50px;
                height: 50px;
                background-color: #27ae60;
                border-radius: 50%;
                border: 2px solid #1a1a1a;
                color: white;
                font-weight: 700;
                font-size: 0.7rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .node-end {
                width: 50px;
                height: 50px;
                background-color: #1a1a1a;
                border-radius: 8px;
                border: 2px solid #1a1a1a;
                color: white;
                font-weight: 700;
                font-size: 0.7rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .diamond-container {
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }

            .diamond {
                width: 65px;
                height: 65px;
                background-color: #f1c40f;
                border: 1px solid #1a1a1a;
                transform: rotate(45deg);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.05);
            }

            .diamond span {
                transform: rotate(-45deg);
                font-weight: 700;
                font-size: 0.65rem;
                text-align: center;
                display: block;
                line-height: 1.1;
                width: 70px;
            }

            .svg-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 15;
                pointer-events: none;
            }
            
            path {
                fill: none;
                stroke: #1a1a1a;
                stroke-width: 1.5px;
                marker-end: url(#arrowhead);
            }

            .path-yes {
                stroke: #27ae60;
                stroke-width: 2px;
                marker-end: url(#arrowhead-yes);
            }

            .path-no {
                stroke: #e74c3c;
                stroke-width: 2px;
                marker-end: url(#arrowhead-no);
                stroke-dasharray: 5, 5;
            }

            .label-path {
                font-size: 12px;
                font-weight: 700;
                text-shadow: 
                    2px 2px 0px #ffffff, 
                    -2px -2px 0px #ffffff, 
                    2px -2px 0px #ffffff, 
                    -2px 2px 0px #ffffff;
            }
            .label-yes { fill: #27ae60; }
            .label-no { fill: #c0392b; }

            .btn-download {
                padding: 12px 24px;
                font-size: 16px;
                cursor: pointer;
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-family: 'Inter', sans-serif;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s, background 0.2s;
                margin-bottom: 20px;
            }

            .btn-download:hover {
                background: #2ecc71;
                transform: translateY(-2px);
            }
        </style>
    """

def get_html_header(title):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        {get_common_styles()}
    </head>
    <body>
    """

def get_html_footer(filename):
    return f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            function descargarImagen() {{
                const btn = document.querySelector('.btn-download');
                btn.innerText = 'Generando...';
                btn.style.opacity = '0.5';

                html2canvas(document.getElementById('diagrama'), {{ 
                    scale: 3, 
                    backgroundColor: "#ffffff"
                }}).then(canvas => {{
                    const link = document.createElement('a');
                    link.download = '{filename.replace(".html", ".png")}';
                    link.href = canvas.toDataURL('image/png', 1.0);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }}).finally(() => {{
                    btn.innerText = 'Descargar Diagrama TO-BE';
                    btn.style.opacity = '1';
                }});
            }}
        </script>
    </body>
    </html>
    """

def get_pagos_tobe_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar Diagrama TO-BE</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">PROCESO OPTIMIZADO (TO-BE)</div>
            
            <div class="grid-container">
                <!-- 3 Carriles (Lanes) -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Cabeceras de Actor -->
                <div class="header header-1">Operador Administrativo<br><span>(Validador / Supervisor)</span></div>
                <div class="header header-2">Sistema vTiger<br><span>(BPMS / Core)</span></div>
                <div class="header header-3">Servicio Integración<br><span>(Middleware API / Cron)</span></div>

                <!-- ======== NODOS ======== -->
                
                <!-- Col 2: Start (Operador) -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Ingresar Ref (Operador - User Task) -->
                <div class="cell" style="grid-column: 3; grid-row: 1;">
                    <div class="node node-manual">
                        <div class="node-title">1. Ingresar Datos</div>
                        <div class="node-desc">Cargar Ref. y Monto (User Task)</div>
                    </div>
                </div>

                <!-- Col 4: Validar Fondos API (Middleware - Service Task) -->
                <div class="cell" style="grid-column: 4; grid-row: 3;">
                    <div class="node node-automation">
                        <div class="node-title">2. Validar Fondos</div>
                        <div class="node-desc">Cruce vs API bancaria y BDD</div>
                    </div>
                </div>

                <!-- Col 5: GW1 (vTiger - Exclusive Gateway) -->
                <div class="cell" style="grid-column: 5; grid-row: 2;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>3. ¿Ref.<br>Válida?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 6 Row 1: Excepción (Operador - Revisión Manual) - RUTA NO -->
                <div class="cell" style="grid-column: 6; grid-row: 1;">
                    <div class="node node-exception">
                        <div class="node-title">Pendiente Revisión</div>
                        <div class="node-desc">Alerta Operador: Discrepancia</div>
                    </div>
                </div>

                <!-- Col 6 Row 2: Crear Payment (vTiger - Service Task) - RUTA SI -->
                <div class="cell" style="grid-column: 6; grid-row: 2;">
                    <div class="node node-automation">
                        <div class="node-title">4. Crear Payment</div>
                        <div class="node-desc">Crear registro y vincular a factura</div>
                    </div>
                </div>

                <!-- Col 7: Script Actualización (vTiger - Script Task) -->
                <div class="cell" style="grid-column: 7; grid-row: 2;">
                    <div class="node node-automation">
                        <div class="node-title">5. Ejecutar Script</div>
                        <div class="node-desc">Actualización de datos (Sustituye Macro)</div>
                    </div>
                </div>

                <!-- Col 8: Generar PDF y Correo (vTiger - Service Task) -->
                <div class="cell" style="grid-column: 8; grid-row: 2;">
                    <div class="node node-automation">
                        <div class="node-title">6. Enviar Factura</div>
                        <div class="node-desc">Generar PDF con firma y enviar por correo</div>
                    </div>
                </div>

                <!-- Col 9: Cambiar Estatus (vTiger - Service Task) -->
                <div class="cell" style="grid-column: 9; grid-row: 2;">
                    <div class="node node-automation">
                        <div class="node-title">7. Marcar Procesado</div>
                        <div class="node-desc">Cierra ciclo sin intervención humana</div>
                    </div>
                </div>

                <!-- Col 10: Fin -->
                <div class="cell" style="grid-column: 10; grid-row: 2;">
                    <div class="node-end">FIN</div>
                </div>

                <!-- ======== CONECTORES (FLECHAS SVG) ======== -->
                <div class="svg-overlay">
                    <svg width="100%" height="100%">
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#1a1a1a" />
                            </marker>
                            <marker id="arrowhead-yes" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#27ae60" />
                            </marker>
                            <marker id="arrowhead-no" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#e74c3c" />
                            </marker>
                        </defs>

                        <!-- Start a Node 1 (Operador) -->
                        <path d="M 235 80 L 285 80" />

                        <!-- Node 1 a Node 2 (Baja a Integración) -->
                        <path d="M 430 80 C 460 80, 460 400, 485 400" />

                        <!-- Node 2 a Gateway (Sube a vTiger) -->
                        <path d="M 630 400 C 680 400, 680 240, 720 240" />

                        <!-- Gateway a Excepción (Camino NO) -->
                        <path class="path-no" d="M 760 207 L 760 80 L 885 80" />
                        <text x="770" y="140" class="label-path label-no">NO (Invalida)</text>

                        <!-- Gateway a Node 4 (Camino SÍ) -->
                        <path class="path-yes" d="M 795 240 L 885 240" />
                        <text x="820" y="230" class="label-path label-yes">SÍ (Exitosa)</text>

                        <!-- Node 4 a Node 5 -->
                        <path d="M 1030 240 L 1085 240" />

                        <!-- Node 5 a Node 6 -->
                        <path d="M 1230 240 L 1285 240" />

                        <!-- Node 6 a Node 7 -->
                        <path d="M 1430 240 L 1485 240" />

                        <!-- Node 7 a FIN -->
                        <path d="M 1630 240 L 1690 240" />
                    </svg>
                </div>
            </div>
        </div>
    """

def main():
    # Unimos Header, Contenido y Footer
    html_completo = get_html_header("Proceso TO-BE Optimizado") + get_pagos_tobe_content() + get_html_footer("pagos_tobe.html")
    
    # Creamos y guardamos el archivo HTML
    ruta_archivo = os.path.abspath("pagos_tobe.html")
    with open(ruta_archivo, "w", encoding="utf-8") as file:
        file.write(html_completo)
    
    print(f"Diagrama TO-BE generado correctamente en:\n{ruta_archivo}")
    
    # Abrimos automáticamente en el navegador web
    webbrowser.open("file://" + ruta_archivo)

if __name__ == "__main__":
    main()

# =========================================================
#   ASEGURATE DE COPIAR HASTA ESTA LÍNEA, NO TE QUEDES
#   A LA MITAD DEL CÓDIGO O DARÁ ERROR DE COMILLAS.
# =========================================================