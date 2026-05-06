import webbrowser
import os

def get_html_content():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Diagramas de Proceso: Trámites Administrativos</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 50px;
            }

            h1 {
                color: #2c3e50;
                margin-bottom: 0;
                text-align: center;
            }

            .diagram-section {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
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
                min-width: 1800px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-top: 15px;
            }

            .main-label {
                writing-mode: vertical-rl;
                transform: rotate(180deg);
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
            .label-asis { background: #e67e22; }
            .label-tobe { background: #27ae60; }

            .grid-container {
                display: grid;
                /* Col 1: Header | Col 2: Start | Cols 3 a 9: Nodos | Col 10: End */
                grid-template-columns: 160px 100px repeat(7, 200px) 120px;
                /* 2 Carriles de 180px cada uno */
                grid-template-rows: 180px 180px;
                position: relative;
                flex-grow: 1;
            }

            .lane-line {
                grid-column: 1 / -1;
                border-bottom: 3px solid #1a1a1a;
                z-index: 1;
            }
            .lane-line:nth-child(1) { grid-row: 1; }
            .lane-line:nth-child(2) { grid-row: 2; border-bottom: none; }

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
                stroke-width: 2px;
                marker-end: url(#arrowhead);
            }

            .path-yes { stroke: #27ae60; marker-end: url(#arrowhead-yes); }
            .path-no { stroke: #e74c3c; marker-end: url(#arrowhead-no); stroke-dasharray: 5,5; }

            .label-path {
                font-size: 12px;
                font-weight: 700;
                text-shadow: 2px 2px 0px #fff, -2px -2px 0px #fff, 2px -2px 0px #fff, -2px 2px 0px #fff;
            }
            .label-yes { fill: #27ae60; }
            .label-no { fill: #c0392b; }

            .btn-download {
                padding: 12px 24px;
                font-size: 16px;
                cursor: pointer;
                color: white;
                border: none;
                border-radius: 8px;
                font-family: 'Inter', sans-serif;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s, background 0.2s;
            }

            .btn-asis { background: #e67e22; }
            .btn-asis:hover { background: #d35400; transform: translateY(-2px); }
            
            .btn-tobe { background: #27ae60; }
            .btn-tobe:hover { background: #2ecc71; transform: translateY(-2px); }

            hr { width: 80%; border: 1px solid #ccc; margin: 20px 0; }
        </style>
    </head>
    <body>

        <h1>Gestión y Facturación de Trámites Administrativos</h1>

        <!-- ==================== SECCIÓN AS-IS ==================== -->
        <div class="diagram-section">
            <button id="btnAsis" class="btn-download btn-asis" onclick="descargarImagen('diagrama-asis', 'Trámites_AS-IS.png', 'btnAsis', 'AS-IS')">
                Descargar Diagrama AS-IS
            </button>
            
            <div class="canvas" id="diagrama-asis">
                <div class="main-label label-asis">ESTADO ACTUAL (AS-IS)</div>
                
                <div class="grid-container">
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>

                    <!-- Headers -->
                    <div class="header header-1">Operador Administrativo<br><span>(Ejecutor Manual)</span></div>
                    <div class="header header-2">vTiger CRM<br><span>(Repositorio/Sistema)</span></div>

                    <!-- NODOS AS-IS -->
                    <div class="cell" style="grid-column: 2; grid-row: 1;"><div class="node-start">INICIO</div></div>
                    
                    <div class="cell" style="grid-column: 3; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">1. Acceder y Filtrar</div>
                            <div class="node-desc">Abrir módulo y seleccionar categoría manualmente</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 4; grid-row: 1;">
                        <div class="diamond-container">
                            <div class="diamond"><span>2. ¿Trámite<br>Admin.?</span></div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 5; grid-row: 2;">
                        <div class="node node-exception">
                            <div class="node-title">Fin del Flujo</div>
                            <div class="node-desc">Deriva a proceso de cuotas regulares</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 5; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">3. Abrir Registro</div>
                            <div class="node-desc">Buscar expediente del estudiante</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 6; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">4. Validar Soporte</div>
                            <div class="node-desc">Verificar comprobante / depósito</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 7; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">5. Tasa BCV</div>
                            <div class="node-desc">Consultar portal BCV y calcular externo</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 8; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">6. Facturar</div>
                            <div class="node-desc">Registrar factura y cambiar a "Procesado"</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 9; grid-row: 1;"><div class="node-end">FIN</div></div>

                    <!-- FLECHAS AS-IS -->
                    <div class="svg-overlay">
                        <svg width="100%" height="100%">
                            <defs>
                                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#1a1a1a" /></marker>
                                <marker id="arrowhead-yes" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#27ae60" /></marker>
                                <marker id="arrowhead-no" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#e74c3c" /></marker>
                            </defs>
                            <!-- Start a N1 -->
                            <path d="M 235 90 L 285 90" />
                            <!-- N1 a GW -->
                            <path d="M 430 90 L 525 90" />
                            <!-- GW NO a Excepcion -->
                            <path class="path-no" d="M 560 125 L 560 270 L 685 270" />
                            <text x="570" y="180" class="label-path label-no">NO (Es Cuota)</text>
                            <!-- GW YES a N3 -->
                            <path class="path-yes" d="M 595 90 L 685 90" />
                            <text x="615" y="80" class="label-path label-yes">SÍ</text>
                            <!-- N3 a N4 -->
                            <path d="M 830 90 L 885 90" />
                            <!-- N4 a N5 -->
                            <path d="M 1030 90 L 1085 90" />
                            <!-- N5 a N6 -->
                            <path d="M 1230 90 L 1285 90" />
                            <!-- N6 a Fin -->
                            <path d="M 1430 90 L 1490 90" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <hr>

        <!-- ==================== SECCIÓN TO-BE ==================== -->
        <div class="diagram-section">
            <button id="btnTobe" class="btn-download btn-tobe" onclick="descargarImagen('diagrama-tobe', 'Trámites_TO-BE.png', 'btnTobe', 'TO-BE')">
                Descargar Diagrama TO-BE
            </button>
            
            <div class="canvas" id="diagrama-tobe">
                <div class="main-label label-tobe">PROCESO OPTIMIZADO (TO-BE)</div>
                
                <div class="grid-container">
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>

                    <!-- Headers -->
                    <div class="header header-1">vTiger CRM (Sistema)<br><span>(Ejecutor/Automatizador)</span></div>
                    <div class="header header-2">Operador Administrativo<br><span>(Validador)</span></div>

                    <!-- NODOS TO-BE -->
                    <div class="cell" style="grid-column: 2; grid-row: 1;"><div class="node-start">INICIO</div></div>
                    
                    <div class="cell" style="grid-column: 3; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">1. Auto-Filtrar</div>
                            <div class="node-desc">Detectar pago y filtrar por metadatos (Service Task)</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 4; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">2. API BCV</div>
                            <div class="node-desc">Consultar tasa oficial en tiempo real</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 5; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">3. Notificar</div>
                            <div class="node-desc">Avisar a operador sobre trámite pendiente</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 6; grid-row: 2;">
                        <div class="node node-manual">
                            <div class="node-title">4. Validar Soporte</div>
                            <div class="node-desc">Verificar integridad del comprobante (User Task)</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 7; grid-row: 2;">
                        <div class="diamond-container">
                            <div class="diamond"><span>5. ¿Soporte<br>Válido?</span></div>
                        </div>
                    </div>

                    <!-- RUTA SÍ -->
                    <div class="cell" style="grid-column: 8; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">6. Facturar y Enviar</div>
                            <div class="node-desc">Cerrar ciclo, estatus Procesado y notificar cliente</div>
                        </div>
                    </div>

                    <!-- RUTA NO -->
                    <div class="cell" style="grid-column: 8; grid-row: 2;">
                        <div class="node node-exception">
                            <div class="node-title">Rechazar / Alerta</div>
                            <div class="node-desc">Soporte ilegible. Solicitar corrección al estudiante</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 9; grid-row: 1;"><div class="node-end">FIN</div></div>
                    <div class="cell" style="grid-column: 9; grid-row: 2;"><div class="node-end">FIN</div></div>

                    <!-- FLECHAS TO-BE -->
                    <div class="svg-overlay">
                        <svg width="100%" height="100%">
                            <!-- Start a N1 -->
                            <path d="M 235 90 L 285 90" />
                            <!-- N1 a N2 -->
                            <path d="M 430 90 L 485 90" />
                            <!-- N2 a N3 -->
                            <path d="M 630 90 L 685 90" />
                            <!-- N3 baja a N4 -->
                            <path d="M 830 90 C 860 90, 860 270, 885 270" />
                            <!-- N4 a GW -->
                            <path d="M 1030 270 L 1125 270" />
                            
                            <!-- GW NO (sigue recto) -->
                            <path class="path-no" d="M 1195 270 L 1285 270" />
                            <text x="1215" y="260" class="label-path label-no">NO</text>
                            
                            <!-- GW YES (sube) -->
                            <path class="path-yes" d="M 1160 235 C 1160 90, 1220 90, 1285 90" />
                            <text x="1170" y="150" class="label-path label-yes">SÍ</text>
                            
                            <!-- N6 a FIN 1 -->
                            <path d="M 1430 90 L 1490 90" />
                            <!-- Excepcion a FIN 2 -->
                            <path d="M 1430 270 L 1490 270" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- SCRIPT PARA DESCARGAR IMÁGENES -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            function descargarImagen(idDiagrama, nombreArchivo, idBoton, tipo) {
                const btn = document.getElementById(idBoton);
                const textoOriginal = btn.innerText;
                
                btn.innerText = 'Generando...';
                btn.style.opacity = '0.5';

                html2canvas(document.getElementById(idDiagrama), { 
                    scale: 3, 
                    backgroundColor: "#ffffff"
                }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = nombreArchivo;
                    link.href = canvas.toDataURL('image/png', 1.0);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }).finally(() => {
                    btn.innerText = textoOriginal;
                    btn.style.opacity = '1';
                });
            }
        </script>
    </body>
    </html>
    """

def main():
    # Creamos el HTML que contiene ambos diagramas
    html_completo = get_html_content()
    ruta_archivo = os.path.abspath("tramites_diagramas.html")
    
    with open(ruta_archivo, "w", encoding="utf-8") as file:
        file.write(html_completo)
    
    print(f"Archivo generado correctamente en:\n{ruta_archivo}")
    
    # Abre en el navegador
    webbrowser.open("file://" + ruta_archivo)

if __name__ == "__main__":
    main()