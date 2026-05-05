import webbrowser
import os

def get_html_content():
    """Generates the TO-BE Swimlane diagram exactly matching the AS-IS format."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>TO-BE Diagrama de Procesos</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 40px;
                display: flex;
                justify-content: center;
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
            }

            /* Left Main Label */
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

            /* Lane Backgrounds & Borders */
            .lane-line {
                grid-column: 1 / -1;
                border-bottom: 3px solid #1a1a1a;
                z-index: 1;
            }
            .lane-line:nth-child(1) { grid-row: 1; }
            .lane-line:nth-child(2) { grid-row: 2; }
            .lane-line:nth-child(3) { grid-row: 3; border-bottom: none; }

            /* Headers */
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

            /* Cells for Nodes */
            .cell {
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                z-index: 10;
            }

            /* Nodes Style */
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

            .node-exception {
                background-color: #ffeaea;
                border-color: #d32f2f;
                color: #d32f2f;
            }
            .node-exception .node-desc {
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

            /* Decision Diamond */
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

            /* SVG Arrows */
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

        </style>
    </head>
    <body>
        <div style="text-align: center; margin-bottom: 20px; width: 100%; position: absolute; top: 10px; left: 0; z-index: 1000;">
            <button onclick="descargarImagen()" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background: #2c3e50; color: white; border: none; border-radius: 5px; font-family: 'Inter', sans-serif; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">Descargar como Imagen</button>
        </div>
        <div class="canvas" id="diagrama" style="margin-top: 40px;">
            <div class="main-label">GESTIÓN DE INSCRIPCIÓN (TO-BE)</div>
            
            <div class="grid-container">
                <!-- Lane Lines -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Headers -->
                <div class="header header-1">Operador de Ventas<br><span>(Supervisor/Excepciones)</span></div>
                <div class="header header-2">vTiger CRM / BPMS<br><span>(Automatizador)</span></div>
                <div class="header header-3">Notificación<br><span>(Email/Cron)</span></div>

                <!-- Elements -->
                <!-- Col 2: Start -->
                <div class="cell" style="grid-column: 2; grid-row: 2;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: Detectar Pago -->
                <div class="cell" style="grid-column: 3; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">1. Detectar Pago</div>
                        <div class="node-desc">Extraer correo API</div>
                    </div>
                </div>

                <!-- Col 4: Buscar Contacto -->
                <div class="cell" style="grid-column: 4; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">2. Buscar Contacto</div>
                        <div class="node-desc">Cruce automático</div>
                    </div>
                </div>

                <!-- Col 5: Validar Soporte -->
                <div class="cell" style="grid-column: 5; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">3. Validar Soporte</div>
                        <div class="node-desc">Verificar monto adjunto</div>
                    </div>
                </div>

                <!-- Col 6: Gateway -->
                <div class="cell" style="grid-column: 6; grid-row: 2;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Monto<br>Válido?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 7: Crear Factura / Excepción -->
                <div class="cell" style="grid-column: 7; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">4. Crear Factura</div>
                        <div class="node-desc">Generación automática</div>
                    </div>
                </div>
                
                <div class="cell" style="grid-column: 7; grid-row: 1;">
                    <div class="node node-exception">
                        <div class="node-title">EXCEPCIÓN:</div>
                        <div class="node-desc">Revisión Manual de<br>Inconsistencia</div>
                    </div>
                </div>

                <!-- Col 8: Crear Oportunidad -->
                <div class="cell" style="grid-column: 8; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">5. Crear Oportunidad</div>
                        <div class="node-desc">Cerrada-Ganada</div>
                    </div>
                </div>

                <!-- Col 9: Enviar Comprobante -->
                <div class="cell" style="grid-column: 9; grid-row: 3;">
                    <div class="node">
                        <div class="node-title">6. Notificar</div>
                        <div class="node-desc">Enviar comprobante</div>
                    </div>
                </div>

                <!-- Col 10: End -->
                <div class="cell" style="grid-column: 10; grid-row: 3;">
                    <div class="node-end">FIN</div>
                </div>

                <!-- SVG Overlays for arrows -->
                <!-- 
                    Row Centers: R1=80, R2=240, R3=400
                    Col Centers (approx): 
                    C1=70 (140 width)
                    C2=180 (140+40) -> Left=140, Right=220. Center=180.
                    C3=310 (220+90) -> Right=400
                    C4=490 (400+90) -> Right=580
                    C5=670 (580+90) -> Right=760
                    C6=850 (760+90) -> Right=940
                    C7=1030 (940+90) -> Right=1120
                    C8=1210 (1120+90) -> Right=1300
                    C9=1390 (1300+90) -> Right=1480
                    C10=1530 (1480+50)
                -->
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

                    <!-- Start to Node 1 -->
                    <path d="M 205 240 L 230 240" />
                    
                    <!-- Node 1 to Node 2 -->
                    <path d="M 390 240 L 410 240" />

                    <!-- Node 2 to Node 3 (Up to R1) -->
                    <path d="M 570 240 L 590 240 L 590 80 L 610 80" />

                    <!-- Node 3 to Gateway (Down to R2) -->
                    <path d="M 750 80 L 770 80 L 770 240 L 800 240" />

                    <!-- Gateway to Node 4 (SÍ) -->
                    <path class="path-yes" d="M 900 240 L 950 240" />
                    <text x="915" y="230" class="label-path label-yes">SÍ</text>

                    <!-- Gateway to Exception (NO) -->
                    <path class="path-no" d="M 850 190 L 850 80 L 950 80" />
                    <text x="860" y="130" class="label-path label-no">NO</text>

                    <!-- Node 4 to Node 5 -->
                    <path d="M 1110 240 L 1130 240" />

                    <!-- Node 5 to Node 6 (Down to R3) -->
                    <path d="M 1290 240 L 1310 240 L 1310 400 L 1330 400" />

                    <!-- Node 6 to End -->
                    <path d="M 1470 400 L 1500 400" />
                </svg>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            function descargarImagen() {
                const element = document.getElementById('diagrama');
                html2canvas(element, { scale: 2 }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = 'Diagrama_Inscripcion_TO-BE.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                });
            }
        </script>
    </body>
    </html>
    """

def generar_diagrama_final():
    """Generates the HTML file and opens it in the browser."""
    html = get_html_content()
    filename = "diagrama_tobe_formato_original.html"
    abs_path = os.path.abspath(filename)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"Diagrama TO-BE generado con el formato solicitado: {filename}")
    webbrowser.open(f"file://{abs_path}")

if __name__ == "__main__":
    generar_diagrama_final()
