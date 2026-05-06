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
                min-width: 1400px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-top: 20px;
            }

            .main-label {
                writing-mode: vertical-rl;
                transform: rotate(180deg);
                background: #2c3e50;
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
                grid-template-columns: 140px 80px repeat(7, 180px) 100px;
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

            .node-pain {
                background-color: #fff4e5;
                border-color: #ff9800;
                color: #e65100;
                border-style: dashed;
            }
            .node-pain::after {
                content: "⚠️ PUNTO DE DOLOR";
                position: absolute;
                top: -10px;
                right: -10px;
                background: #ff9800;
                color: white;
                font-size: 0.6rem;
                padding: 2px 6px;
                border-radius: 4px;
                font-weight: 700;
                z-index: 20;
            }

            .node-exception {
                background-color: #ffeaea;
                border-color: #d32f2f;
                color: #d32f2f;
            }

            .node-start {
                width: 50px;
                height: 50px;
                background-color: #e91e63;
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
                z-index: 5;
                pointer-events: none;
            }
            
            path {
                fill: none;
                stroke: #1a1a1a;
                stroke-width: 1.5px;
                marker-end: url(#arrowhead);
            }

            .path-yes {
                stroke: #2ecc71;
                marker-end: url(#arrowhead-yes);
            }

            .path-no {
                stroke: #e74c3c;
                stroke-dasharray: 4;
                marker-end: url(#arrowhead-no);
            }

            .label-path {
                font-size: 11px;
                font-weight: 700;
            }
            .label-yes { fill: #2ecc71; }
            .label-no { fill: #e74c3c; }

            .btn-download {
                padding: 12px 24px;
                font-size: 16px;
                cursor: pointer;
                background: #2c3e50;
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
                background: #34495e;
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
                const element = document.getElementById('diagrama');
                if (!element) {{
                    console.error('No se encontró el elemento #diagrama');
                    alert('Error: No se encontró el diagrama para exportar.');
                    return;
                }}

                console.log('Iniciando captura de imagen...');
                const btn = document.querySelector('.btn-download');
                btn.innerText = 'Generando...';
                btn.style.opacity = '0.5';

                html2canvas(element, {{ 
                    scale: 3, 
                    useCORS: true, 
                    allowTaint: true,
                    backgroundColor: "#ffffff",
                    logging: true
                }}).then(canvas => {{
                    try {{
                        const link = document.createElement('a');
                        link.download = '{filename.replace(".html", ".png")}';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        console.log('Descarga iniciada exitosamente.');
                    }} catch (err) {{
                        console.error('Error al generar el enlace de descarga:', err);
                        alert('Hubo un error al procesar la descarga. Revisa la consola del navegador.');
                    }}
                }}).catch(err => {{
                    console.error('Error en html2canvas:', err);
                    alert('Error técnico al generar la imagen. Verifica si tienes conexión a internet para cargar la librería.');
                }}).finally(() => {{
                    btn.innerText = 'Descargar como Imagen';
                    btn.style.opacity = '1';
                }});
            }}
        </script>
    </body>
    </html>
    """

def get_arancel_asis_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar como Imagen</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">ARANCEL AS-IS</div>
            
            <div class="grid-container">
                <!-- Lane Lines -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Headers -->
                <div class="header header-1">Operador Administrativo<br><span>(Manual)</span></div>
                <div class="header header-2">Sistema CRM (vTiger)<br><span>(Soporte de Datos)</span></div>
                <div class="header header-3">Salida / Notificación<br><span>(Manual/Email)</span></div>

                <!-- Elements -->
                <!-- Col 2: Start -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Filtrar -->
                <div class="cell" style="grid-column: 3; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">1. Filtrar Registros</div>
                        <div class="node-desc">Payment Record: "No Procesado" y "Arancel"</div>
                    </div>
                </div>

                <!-- Col 4: Validar -->
                <div class="cell" style="grid-column: 4; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">2. Validar Soporte</div>
                        <div class="node-desc">Extraer ID Estudiante manualmente</div>
                    </div>
                </div>

                <!-- Col 5: Abrir Perfil -->
                <div class="cell" style="grid-column: 5; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">3. Abrir Perfil</div>
                        <div class="node-desc">Generar factura desde Contacto</div>
                    </div>
                </div>

                <!-- Col 6: Oportunidad -->
                <div class="cell" style="grid-column: 6; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">4. Crear Oportunidad</div>
                        <div class="node-desc">Cerrada-Ganada (Creación manual)</div>
                    </div>
                </div>

                <!-- Col 7: Borrar Cláusulas -->
                <div class="cell" style="grid-column: 7; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">5. Intervención Manual</div>
                        <div class="node-desc">Borrar cláusula "Diplomados" en Condiciones</div>
                    </div>
                </div>

                <!-- Col 8: Guardar -->
                <div class="cell" style="grid-column: 8; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">6. Indexar y Guardar</div>
                        <div class="node-desc">Item "ARANCEL DE EGRESO" y montos</div>
                    </div>
                </div>

                <!-- Col 9: Fin -->
                <div class="cell" style="grid-column: 9; grid-row: 2;">
                    <div class="node-end">FIN</div>
                </div>

                <svg class="svg-overlay" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#1a1a1a" />
                        </marker>
                    </defs>

                    <!-- Path Logic -->
                    <path d="M 205 80 L 230 80" /> <!-- Start to 1 -->
                    <path d="M 390 80 L 410 80" /> <!-- 1 to 2 -->
                    <path d="M 570 80 L 590 80 L 590 240 L 610 240" /> <!-- 2 to 3 -->
                    <path d="M 750 240 L 770 240 L 770 80 L 800 80" /> <!-- 3 to 4 -->
                    <path d="M 940 80 L 980 80" /> <!-- 4 to 5 -->
                    <path d="M 1120 80 L 1140 80 L 1140 240 L 1160 240" /> <!-- 5 to 6 -->
                    <path d="M 1300 240 L 1330 240" /> <!-- 6 to End -->
                </svg>
            </div>
        </div>
    """

def get_arancel_tobe_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar como Imagen</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">ARANCEL TO-BE</div>
            
            <div class="grid-container">
                <!-- Lane Lines -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Headers -->
                <div class="header header-1">Operador Administrativo<br><span>(Supervisor / Validador)</span></div>
                <div class="header header-2">Workflow Engine (vTiger)<br><span>(Automatizador)</span></div>
                <div class="header header-3">Sistema de Notificaciones<br><span>(Comunicador)</span></div>

                <!-- Elements -->
                <!-- Col 2: Start -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Validar Soporte -->
                <div class="cell" style="grid-column: 3; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">1. Validar Soporte</div>
                        <div class="node-desc">Marcar como "Verificado" (User Task)</div>
                    </div>
                </div>

                <!-- Col 4: Workflow Oportunidad -->
                <div class="cell" style="grid-column: 4; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">2. Crear Oportunidad</div>
                        <div class="node-desc">Fase Cerrada-Ganada (Service Task)</div>
                    </div>
                </div>

                <!-- Col 5: Generar Factura -->
                <div class="cell" style="grid-column: 5; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">3. Generar Factura</div>
                        <div class="node-desc">Vinculada automáticamente (Service Task)</div>
                    </div>
                </div>

                <!-- Col 6: Script Limpieza -->
                <div class="cell" style="grid-column: 6; grid-row: 2;">
                    <div class="node" style="border: 2px solid #2c3e50; background: #f8f9fa;">
                        <div class="node-title">4. Script de Limpieza</div>
                        <div class="node-desc">Reemplazo de Cláusulas (Script Task)</div>
                    </div>
                </div>

                <!-- Col 7: Gateway Integridad -->
                <div class="cell" style="grid-column: 7; grid-row: 2;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Datos<br>Íntegros?</span>
                        </div>
                    </div>
                </div>
                
                <div class="cell" style="grid-column: 7; grid-row: 1;">
                    <div class="node node-exception">
                        <div class="node-title">EXCEPCIÓN:</div>
                        <div class="node-desc">Revisión por Error en Montos</div>
                    </div>
                </div>

                <!-- Col 8: Enviar PDF -->
                <div class="cell" style="grid-column: 8; grid-row: 3;">
                    <div class="node">
                        <div class="node-title">5. Enviar PDF</div>
                        <div class="node-desc">Notificación automática (Service Task)</div>
                    </div>
                </div>

                <!-- Col 9: End -->
                <div class="cell" style="grid-column: 9; grid-row: 3;">
                    <div class="node-end">FIN</div>
                </div>

                <svg class="svg-overlay" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#1a1a1a" />
                        </marker>
                        <marker id="arrowhead-yes" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#2ecc71" />
                        </marker>
                        <marker id="arrowhead-no" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#e74c3c" />
                        </marker>
                    </defs>

                    <!-- Path Logic -->
                    <path d="M 205 80 L 230 80" /> <!-- Start to 1 -->
                    <path d="M 390 80 L 410 80 L 410 240 L 430 240" /> <!-- 1 to 2 -->
                    <path d="M 570 240 L 590 240" /> <!-- 2 to 3 -->
                    <path d="M 750 240 L 770 240" /> <!-- 3 to 4 -->
                    <path d="M 930 240 L 980 240" /> <!-- 4 to Gateway -->
                    
                    <path class="path-yes" d="M 1030 290 L 1030 400 L 1110 400" /> <!-- Yes to 5 -->
                    <text x="1040" y="340" class="label-path label-yes">SÍ</text>

                    <path class="path-no" d="M 1030 190 L 1030 80 L 1110 80" /> <!-- No to Exc -->
                    <text x="1040" y="140" class="label-path label-no">NO</text>

                    <path d="M 1250 400 L 1330 400" /> <!-- 5 to End -->
                </svg>
            </div>
        </div>
    """

def get_promociones_asis_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar como Imagen</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">PROMO AS-IS</div>
            
            <div class="grid-container">
                <!-- Lane Lines -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Headers -->
                <div class="header header-1">Operador Administrativo<br><span>(Manual)</span></div>
                <div class="header header-2">vTiger CRM<br><span>(Soporte de Datos)</span></div>
                <div class="header header-3">Salida / Control<br><span>(Manual)</span></div>

                <!-- Elements -->
                <!-- Col 2: Start -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Filtrar -->
                <div class="cell" style="grid-column: 3; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">1. Filtrar Concepto</div>
                        <div class="node-desc">Localizar "Promo 2x100" en Payment Record</div>
                    </div>
                </div>

                <!-- Col 4: Verificar -->
                <div class="cell" style="grid-column: 4; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">2. Verificar Datos</div>
                        <div class="node-desc">Cruce de Estudiante 1 y 2 en Fichas</div>
                    </div>
                </div>

                <!-- Col 5: Gateway 1 -->
                <div class="cell" style="grid-column: 5; grid-row: 1;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Datos<br>Correctos?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 6: Crear Factura -->
                <div class="cell" style="grid-column: 6; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">3. Crear Factura</div>
                        <div class="node-desc">Nomenclatura manual de asunto y oportunidad</div>
                    </div>
                </div>

                <!-- Col 7: Agregar Items -->
                <div class="cell" style="grid-column: 7; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">4. Agregar Productos</div>
                        <div class="node-desc">Diplomado 1 y 2 en Detalles Elemento</div>
                    </div>
                </div>

                <!-- Col 8: Aplicar Descuento -->
                <div class="cell" style="grid-column: 8; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">5. Aplicar Descuento</div>
                        <div class="node-desc">Carga manual de 90% a cada ítem</div>
                    </div>
                </div>

                <!-- Col 9: Gateway 2 -->
                <div class="cell" style="grid-column: 9; grid-row: 1;">
                    <div class="diamond-container">
                        <div class="diamond" style="border-color: #ff9800; background: #fff4e5;">
                            <span style="color: #e65100;">¿Total exacto<br>$100.00?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 10: Fin -->
                <div class="cell" style="grid-column: 10; grid-row: 2;">
                    <div class="node-end">FIN</div>
                </div>

                <svg class="svg-overlay" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#1a1a1a" />
                        </marker>
                    </defs>

                    <!-- Path Logic -->
                    <path d="M 205 80 L 230 80" /> <!-- Start to 1 -->
                    <path d="M 390 80 L 410 80" /> <!-- 1 to 2 -->
                    <path d="M 570 80 L 590 80" /> <!-- 2 to G1 -->
                    
                    <path d="M 760 80 L 800 80" /> <!-- G1 to 3 -->
                    <path d="M 940 80 L 960 80 L 960 240 L 980 240" /> <!-- 3 to 4 -->
                    <path d="M 1120 240 L 1140 240 L 1140 80 L 1160 80" /> <!-- 4 to 5 -->
                    <path d="M 1300 80 L 1340 80" /> <!-- 5 to G2 -->
                    <path d="M 1485 80 L 1510 80 L 1510 240 L 1520 240" /> <!-- G2 to 6 -->
                </svg>
            </div>
        </div>
    """

def generar_diagramas_promociones():
    # AS-IS
    html_asis = get_html_header("AS-IS Promociones") + get_promociones_asis_content() + get_html_footer("diagrama_promociones_asis_profesional.html")
    with open("diagrama_promociones_asis_profesional.html", "w", encoding="utf-8") as f:
        f.write(html_asis)
    
    print("Diagrama AS-IS de Promociones generado.")
    webbrowser.open(f"file://{os.path.abspath('diagrama_promociones_asis_profesional.html')}")

def generar_diagramas_arancel():
    # AS-IS
    html_asis = get_html_header("AS-IS Arancel") + get_arancel_asis_content() + get_html_footer("diagrama_arancel_asis_profesional.html")
    with open("diagrama_arancel_asis_profesional.html", "w", encoding="utf-8") as f:
        f.write(html_asis)
    
    # TO-BE
    html_tobe = get_html_header("TO-BE Arancel") + get_arancel_tobe_content() + get_html_footer("diagrama_arancel_tobe_profesional.html")
    with open("diagrama_arancel_tobe_profesional.html", "w", encoding="utf-8") as f:
        f.write(html_tobe)
        
    print("Diagramas de Arancel (AS-IS y TO-BE) generados.")
    webbrowser.open(f"file://{os.path.abspath('diagrama_arancel_tobe_profesional.html')}")

if __name__ == "__main__":
    # Generamos el TO-BE de Arancel por petición del usuario
    generar_diagramas_arancel()
