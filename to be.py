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
                /* Restaurado al azul marino corporativo */
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
                /* Col 1: Headers (160px) | Col 2: Start (100px) | Cols 3 a 9: Nodos (200px) | Col 10: End (120px) */
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

            .node-automation {
                background-color: #e8f4fd;
                border: 2px solid #2980b9;
                color: #2c3e50;
            }
            .node-automation::after {
                content: "⚙️ SCRIPT / BOT";
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
                /* Borde blanco grueso al texto para que nunca se mezcle con las líneas de fondo */
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
                    btn.innerText = 'Descargar como Imagen TO-BE';
                    btn.style.opacity = '1';
                }});
            }}
        </script>
    </body>
    </html>
    """

def get_promociones_tobe_content():
    return """
        <button class="btn-download" onclick="descargarImagen()">Descargar como Imagen TO-BE</button>
        <div class="canvas" id="diagrama">
            <div class="main-label">PROMO TO-BE</div>
            
            <div class="grid-container">
                <!-- 3 Carriles (Lanes) -->
                <div class="lane-line"></div>
                <div class="lane-line"></div>
                <div class="lane-line"></div>

                <!-- Cabeceras de Actor -->
                <div class="header header-1">Operador Administrativo<br><span>(Supervisor)</span></div>
                <div class="header header-2">vTiger CRM<br><span>(Motor / Automatizador)</span></div>
                <div class="header header-3">Notificaciones<br><span>(Soporte)</span></div>

                <!-- ======== NODOS ======== -->
                
                <!-- Col 2: Start (Operador) -->
                <div class="cell" style="grid-column: 2; grid-row: 1;">
                    <div class="node-start">INICIO</div>
                </div>

                <!-- Col 3: User Task (Operador) -->
                <div class="cell" style="grid-column: 3; grid-row: 1;">
                    <div class="node">
                        <div class="node-title">1. Activar Bandera</div>
                        <div class="node-desc">Identificar pago "Promo 2x100" y disparar flujo</div>
                    </div>
                </div>

                <!-- Col 4: Validar Datos (vTiger) -->
                <div class="cell" style="grid-column: 4; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">2. Validar Datos</div>
                        <div class="node-desc">Existencia de Fichas para Estudiante 1 y 2</div>
                    </div>
                </div>

                <!-- Col 5: GW1 (vTiger) -->
                <div class="cell" style="grid-column: 5; grid-row: 2;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Datos<br>Completos?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 5 Row 1: Excepcion Corrección (Operador) -->
                <div class="cell" style="grid-column: 5; grid-row: 1;">
                    <div class="node node-exception">
                        <div class="node-title">EXCEPCIÓN:</div>
                        <div class="node-desc">Tarea asignada: "Corregir datos de estudiantes"</div>
                    </div>
                </div>

                <!-- Col 6: Generar Factura (vTiger) -->
                <div class="cell" style="grid-column: 6; grid-row: 2;">
                    <div class="node">
                        <div class="node-title">3. Generar Factura</div>
                        <div class="node-desc">Vincular programas automáticamente (Service)</div>
                    </div>
                </div>

                <!-- Col 7: Script Descuento Automático (vTiger) -->
                <div class="cell" style="grid-column: 7; grid-row: 2;">
                    <div class="node node-automation">
                        <div class="node-title">4. Ajuste Contable</div>
                        <div class="node-desc">Script: Forzar Descuento hasta clavar $100.00</div>
                    </div>
                </div>

                <!-- Col 8: GW2 Balance Seguro (vTiger) -->
                <div class="cell" style="grid-column: 8; grid-row: 2;">
                    <div class="diamond-container">
                        <div class="diamond">
                            <span>¿Total<br>Exacto $100?</span>
                        </div>
                    </div>
                </div>

                <!-- Col 8 Row 3: Excepcion Alerta (Notificaciones) -->
                <div class="cell" style="grid-column: 8; grid-row: 3;">
                    <div class="node node-exception" style="background-color: #fff3e0; border-color: #e67e22; color: #d35400;">
                        <div class="node-title">ALERTA SISTEMA</div>
                        <div class="node-desc">Bloqueo guardado y Notifica Admin de CRM</div>
                    </div>
                </div>

                <!-- Col 9: Guardar y Enviar (Notificaciones) -->
                <div class="cell" style="grid-column: 9; grid-row: 3;">
                    <div class="node">
                        <div class="node-title">5. Guardar y Enviar</div>
                        <div class="node-desc">Cerrar registro y enviar copia digital PDF</div>
                    </div>
                </div>

                <!-- Col 10: Fin (Notificaciones) -->
                <div class="cell" style="grid-column: 10; grid-row: 3;">
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

                    <!-- Inicio a Nodo 1 (Carril 1) -->
                    <path d="M 235 80 L 285 80" />
                    
                    <!-- Nodo 1 a Nodo 2 (Baja a Carril 2) -->
                    <path d="M 430 80 L 460 80 L 460 240 L 485 240" />
                    
                    <!-- Nodo 2 a GW1 (Carril 2) -->
                    <path d="M 630 240 L 709 240" />
                    
                    <!-- GW1 a Nodo 3 (SÍ) -->
                    <path class="path-yes" d="M 806 240 L 885 240" />
                    <text x="830" y="232" class="label-path label-yes">SÍ</text>

                    <!-- GW1 a Excepción 1 (NO -> Sube a Carril 1) -->
                    <path class="path-no" d="M 760 194 L 760 120" />
                    <text x="770" y="165" class="label-path label-no">NO</text>

                    <!-- Nodo 3 a Nodo 4 (Carril 2) -->
                    <path d="M 1030 240 L 1085 240" />

                    <!-- Nodo 4 (Script) a GW2 (Carril 2) -->
                    <path d="M 1230 240 L 1309 240" />

                    <!-- GW2 a Guardar/Enviar (SÍ) -->
                    <!-- Avanza horizontalmente al centro de la columna 9 y luego baja hacia la caja -->
                    <path class="path-yes" d="M 1406 240 L 1560 240 L 1560 360" />
                    <text x="1450" y="232" class="label-path label-yes">SÍ (Balance Seguro)</text>

                    <!-- GW2 a Excepción Alerta (NO) -->
                    <!-- Baja en línea recta hacia la alerta -->
                    <path class="path-no" d="M 1360 286 L 1360 360" />
                    <text x="1375" y="335" class="label-path label-no">NO (Error Base)</text>

                    <!-- Guardar a Fin (Carril 3) -->
                    <path d="M 1630 400 L 1690 400" />
                </svg>
            </div>
        </div>
    """

def generar_diagrama_promociones_tobe():
    html_tobe = get_html_header("TO-BE Promociones Automatizado") + get_promociones_tobe_content() + get_html_footer("diagrama_promociones_tobe_oficial.html")
    
    filename = "diagrama_promociones_tobe_oficial.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_tobe)
    
    print(f"Diagrama TO-BE generado exitosamente. Barra lateral restaurada al azul corporativo: {filename}")
    webbrowser.open(f"file://{os.path.abspath(filename)}")

if __name__ == "__main__":
    generar_diagrama_promociones_tobe()