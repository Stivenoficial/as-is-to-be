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
                /* Ampliado para 12 columnas (2180px) */
                min-width: 2180px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-top: 20px;
            }

            .main-label {
                writing-mode: vertical-rl;
                transform: rotate(180deg);
                /* Azul Corporativo para AS-IS */
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
                /* Col 1: 160px | Col 2: 100px | Cols 3 a 11: 200px | Col 12: 120px */
                grid-template-columns: 160px 100px repeat(9, 200px) 120px;
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
                min-height: 80px;
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
                font-size: 0.55rem;
                padding: 3px 6px;
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
                background-color: #2c3e50;
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
                stroke: #2ecc71;
                marker-end: url(#arrowhead-yes);
            }

            .path-no {
                stroke: #e74c3c;
                marker-end: url(#arrowhead-no);
            }

            .label-path {
                font-size: 11px;
                font-weight: 700;
                text-shadow: 
                    2px 2px 0px #ffffff, 
                    -2px -2px 0px #ffffff, 
                    2px -2px 0px #ffffff, 
                    -2px 2px 0px #ffffff,
                    0px 2px 0px #ffffff,
                    0px -2px 0px #ffffff,
                    2px 0px 0px #ffffff,
                    -2px 0px 0px #ffffff;
            }
            .label-yes { fill: #27ae60; }
            .label-no { fill: #c0392b; }

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
                    btn.innerText = 'Descargar Diagrama AS-IS';
                    btn.style.opacity = '1';
                }});
            }}
        </script>
    </body>
    </html>
    """

def get_pagos_asis_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar Diagrama AS-IS</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">PAGOS AS-IS</div>
            
            <div class="grid-container">
                <!-- 3 Carriles (Lanes) -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Cabeceras de Actor -->
                <div class="header header-1">Operador Administrativo<br><span>(Ejecutor Manual)</span></div>
                <div class="header header-2">vTiger CRM<br><span>(Sistema Base)</span></div>
                <div class="header header-3">Plataforma Bancaria<br><span>(Validación Externa)</span></div>

                <!-- ======== NODOS ======== -->
                
                <!-- Col 2: Start (Operador) -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Abrir Factura (vTiger) -->
                <div class="cell" style="grid-column: 3; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">1. Acceder Factura</div>
                        <div class="node-desc">Abrir detalles de la factura generada</div>
                    </div>
                </div>

                <!-- Col 4: Payments (vTiger) -->
                <div class="cell" style="grid-column: 4; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">2. Módulo Payments</div>
                        <div class="node-desc">Ingresar al sub-módulo de pagos</div>
                    </div>
                </div>

                <!-- Col 5: Banco (Plataforma Bancaria) -->
                <div class="cell" style="grid-column: 5; grid-row: 3;">
                    <div class="node">
                        <div class="node-title">3. Consultar Banco</div>
                        <div class="node-desc">Revisar Mercantil, Zelle o PayPal</div>
                    </div>
                </div>

                <!-- Col 6: GW1 (Operador) -->
                <div class="cell" style="grid-column: 6; grid-row: 1;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Ingreso<br>Validado?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 6 Row 2: Excepción -->
                <div class="cell" style="grid-column: 6; grid-row: 2;">
                    <div class="node node-exception">
                        <div class="node-title">EXCEPCIÓN</div>
                        <div class="node-desc">Fondo no disponible o ref. errónea (Pausa)</div>
                    </div>
                </div>

                <!-- Col 7: Registrar Datos (Operador) [PAIN] -->
                <div class="cell" style="grid-column: 7; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">4. Registrar Datos</div>
                        <div class="node-desc">Transcripción manual de Monto y Ref (Propenso a errores)</div>
                    </div>
                </div>

                <!-- Col 8: Record Payment (vTiger) -->
                <div class="cell" style="grid-column: 8; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">5. Record Payment</div>
                        <div class="node-desc">Ejecutar botón de guardado en el CRM</div>
                    </div>
                </div>

                <!-- Col 9: Macro (Operador) [PAIN] -->
                <div class="cell" style="grid-column: 9; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">6. Ejecutar Macro</div>
                        <div class="node-desc">Clic manual para "Actualizar Datos" (Falta automatización)</div>
                    </div>
                </div>

                <!-- Col 10: Email (Operador) [PAIN] -->
                <div class="cell" style="grid-column: 10; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">7. Enviar PDF</div>
                        <div class="node-desc">Quitar firma y adjuntar correo repetitivamente</div>
                    </div>
                </div>

                <!-- Col 11: Procesado (Operador) [PAIN] -->
                <div class="cell" style="grid-column: 11; grid-row: 1;">
                    <div class="node node-pain">
                        <div class="node-title">8. Estatus Final</div>
                        <div class="node-desc">Cambio manual a "Procesado" (Cierre redundante)</div>
                    </div>
                </div>

                <!-- Col 12: Fin (Operador) -->
                <div class="cell" style="grid-column: 12; grid-row: 1;">
                    <div class="node-end">FIN</div>
                </div>

                <!-- ======== RUTAS Y FLECHAS ======== -->
                <svg class="svg-overlay" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#1a1a1a" />
                        </marker>
                        <marker id="arrowhead-yes" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#27ae60" />
                        </marker>
                        <marker id="arrowhead-no" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                            <polygon points="0 0, 6 2, 0 4" fill="#c0392b" />
                        </marker>
                    </defs>

                    <!-- Inicio a Nodo 1 (Baja a Carril 2) -->
                    <path d="M 235 80 L 260 80 L 260 240 L 285 240" />
                    
                    <!-- Nodo 1 a Nodo 2 (Carril 2) -->
                    <path d="M 430 240 L 485 240" />
                    
                    <!-- Nodo 2 a Banco (Baja a Carril 3) -->
                    <path d="M 630 240 L 660 240 L 660 400 L 685 400" />
                    
                    <!-- Banco a GW1 (Sube a Carril 1) -->
                    <path d="M 830 400 L 860 400 L 860 80 L 914 80" />

                    <!-- GW1 a Nodo 4 (SÍ -> Derecho en Carril 1) -->
                    <path class="path-yes" d="M 1006 80 L 1085 80" />
                    <text x="1030" y="72" class="label-path label-yes">SÍ</text>

                    <!-- GW1 a Excepción (NO -> Baja a Carril 2) -->
                    <path class="path-no" d="M 960 126 L 960 195" />
                    <text x="970" y="165" class="label-path label-no">NO</text>

                    <!-- Nodo 4 (Datos) a Nodo 5 (Baja a Carril 2) -->
                    <path d="M 1230 80 L 1260 80 L 1260 240 L 1285 240" />

                    <!-- Nodo 5 a Nodo 6 (Sube a Carril 1) -->
                    <path d="M 1430 240 L 1460 240 L 1460 80 L 1485 80" />

                    <!-- Nodo 6 a Nodo 7 (Carril 1) -->
                    <path d="M 1630 80 L 1685 80" />

                    <!-- Nodo 7 a Nodo 8 (Carril 1) -->
                    <path d="M 1830 80 L 1885 80" />

                    <!-- Nodo 8 a FIN (Carril 1) -->
                    <path d="M 2030 80 L 2090 80" />
                </svg>
            </div>
        </div>
    """

def generar_diagrama_pagos_asis():
    html = get_html_header("AS-IS Registro de Pagos") + get_pagos_asis_content() + get_html_footer("diagrama_pagos_asis_oficial.html")
    
    filename = "diagrama_pagos_asis_oficial.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Diagrama AS-IS de Pagos generado exitosamente en: {filename}")
    webbrowser.open(f"file://{os.path.abspath(filename)}")

if __name__ == "__main__":
    generar_diagrama_pagos_asis()