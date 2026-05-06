import webbrowser
import os

def get_html_content():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Diagramas: Procesamiento de Cuotas</title>
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
                /* 10 Columnas */
                grid-template-columns: 160px 100px repeat(7, 200px) 120px;
                /* 3 Carriles de 180px cada uno */
                grid-template-rows: 180px 180px 180px;
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
                border-radius: 6px;
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

            .node-title { font-weight: 700; margin-bottom: 4px; }
            .node-desc { font-size: 0.65rem; color: #444; }

            .node-manual { background-color: #fffaf0; border-color: #f39c12; }
            .node-manual::after {
                content: "👤 MANUAL"; position: absolute; top: -10px; right: -10px;
                background: #f39c12; color: white; font-size: 0.55rem; padding: 3px 6px;
                border-radius: 4px; font-weight: 700; z-index: 20;
            }

            .node-automation { background-color: #e8f4fd; border: 2px solid #2980b9; color: #2c3e50; }
            .node-automation::after {
                content: "⚙️ SISTEMA"; position: absolute; top: -10px; right: -10px;
                background: #2980b9; color: white; font-size: 0.55rem; padding: 3px 6px;
                border-radius: 4px; font-weight: 700; z-index: 20;
            }

            .node-external { background-color: #f8f9fa; border: 2px dashed #7f8c8d; }
            .node-external::after {
                content: "🌐 EXTERNO"; position: absolute; top: -10px; right: -10px;
                background: #7f8c8d; color: white; font-size: 0.55rem; padding: 3px 6px;
                border-radius: 4px; font-weight: 700; z-index: 20;
            }

            .node-exception { background-color: #ffeaea; border: 2px solid #e74c3c; color: #c0392b; }

            .node-start { width: 50px; height: 50px; background-color: #27ae60; border-radius: 50%; border: 2px solid #1a1a1a; color: white; font-weight: 700; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; }
            .node-end { width: 50px; height: 50px; background-color: #1a1a1a; border-radius: 8px; border: 2px solid #1a1a1a; color: white; font-weight: 700; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; }

            .diamond-container { display: flex; align-items: center; justify-content: center; position: relative; }
            .diamond {
                width: 65px; height: 65px; background-color: #f1c40f; border: 1px solid #1a1a1a;
                transform: rotate(45deg); display: flex; align-items: center; justify-content: center;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.05);
            }
            .diamond span {
                transform: rotate(-45deg); font-weight: 700; font-size: 0.65rem;
                text-align: center; display: block; line-height: 1.1; width: 70px;
            }

            .svg-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 15; pointer-events: none; }
            
            path { fill: none; stroke: #34495e; stroke-width: 2.5px; stroke-linejoin: round; marker-end: url(#arrowhead); }
            .path-yes { stroke: #27ae60; marker-end: url(#arrowhead-yes); }
            .path-no { stroke: #e74c3c; marker-end: url(#arrowhead-no); stroke-dasharray: 6,4; }
            .path-loop { stroke: #2980b9; marker-end: url(#arrowhead-loop); stroke-dasharray: 4,4; }

            .label-path { font-size: 11px; font-weight: 700; text-shadow: 2px 2px 0px #fff, -2px -2px 0px #fff, 2px -2px 0px #fff, -2px 2px 0px #fff; }
            .label-yes { fill: #27ae60; }
            .label-no { fill: #c0392b; }
            .label-loop { fill: #2980b9; }

            .btn-download {
                padding: 12px 24px; font-size: 16px; cursor: pointer; color: white; border: none;
                border-radius: 8px; font-family: 'Inter', sans-serif; font-weight: bold;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s, background 0.2s;
            }
            .btn-asis { background: #e67e22; } .btn-asis:hover { background: #d35400; transform: translateY(-2px); }
            .btn-tobe { background: #27ae60; } .btn-tobe:hover { background: #2ecc71; transform: translateY(-2px); }
            hr { width: 80%; border: 1px solid #ccc; margin: 20px 0; }
        </style>
    </head>
    <body>

        <h1>Registro y Conciliación de Pagos (Cuotas)</h1>

        <!-- ==================== SECCIÓN AS-IS ==================== -->
        <div class="diagram-section">
            <button id="btnAsis" class="btn-download btn-asis" onclick="descargarImagen('diagrama-asis', 'Cuotas_AS-IS.png', 'btnAsis', 'AS-IS')">
                Descargar Diagrama AS-IS
            </button>
            
            <div class="canvas" id="diagrama-asis">
                <div class="main-label label-asis">ESTADO ACTUAL (AS-IS)</div>
                
                <div class="grid-container">
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>

                    <!-- Headers -->
                    <div class="header header-1">Operador CRM<br><span>(Ejecutor / Validador)</span></div>
                    <div class="header header-2">vTiger CRM<br><span>(Repositorio Base)</span></div>
                    <div class="header header-3">Entorno Externo<br><span>(Portal Web BCV)</span></div>

                    <!-- NODOS AS-IS -->
                    <!-- R1: Operador -->
                    <div class="cell" style="grid-column: 2; grid-row: 1;"><div class="node-start">INICIO</div></div>
                    
                    <div class="cell" style="grid-column: 3; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">1. Filtrar y Extraer</div>
                            <div class="node-desc">Abrir PDF y extraer Fecha, Monto y Ref</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 5; grid-row: 1;">
                        <div class="node node-manual">
                            <div class="node-title">3. Calcular</div>
                            <div class="node-desc">Uso de calculadora externa (Divisas/Bs)</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 7; grid-row: 1;">
                        <div class="diamond-container">
                            <div class="diamond"><span>¿Múltiples<br>Cuotas?</span></div>
                        </div>
                    </div>

                    <!-- R2: CRM -->
                    <div class="cell" style="grid-column: 6; grid-row: 2;">
                        <div class="node node-manual">
                            <div class="node-title">4. Record Payment</div>
                            <div class="node-desc">Formulario manual de vinculación de pago</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 8; grid-row: 2;">
                        <div class="node node-manual">
                            <div class="node-title">5. Procesar</div>
                            <div class="node-desc">Actualizar estatus y guardar cambios finales</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 9; grid-row: 2;"><div class="node-end">FIN</div></div>

                    <!-- R3: Externo -->
                    <div class="cell" style="grid-column: 4; grid-row: 3;">
                        <div class="node node-external">
                            <div class="node-title">2. Tasa BCV</div>
                            <div class="node-desc">Búsqueda manual de tasa histórica en portal</div>
                        </div>
                    </div>

                    <!-- FLECHAS AS-IS (ORTOGONALES) -->
                    <div class="svg-overlay">
                        <svg width="100%" height="100%">
                            <defs>
                                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#34495e" /></marker>
                                <marker id="arrowhead-yes" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#27ae60" /></marker>
                                <marker id="arrowhead-no" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#e74c3c" /></marker>
                                <marker id="arrowhead-loop" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#2980b9" /></marker>
                            </defs>
                            
                            <!-- Start to N1 -->
                            <path d="M 235 90 L 285 90" /> 
                            
                            <!-- N1 (R1) a BCV (R3) -->
                            <path d="M 430 90 L 460 90 L 460 450 L 485 450" /> 
                            
                            <!-- BCV (R3) a Calcular (R1) -->
                            <path d="M 630 450 L 660 450 L 660 90 L 685 90" /> 
                            
                            <!-- Calcular (R1) a Record Payment (R2) -->
                            <path d="M 830 90 L 860 90 L 860 270 L 885 270" /> 
                            
                            <!-- Record Payment (R2) a GW (R1) -->
                            <path d="M 1030 270 L 1075 270 L 1075 90 L 1120 90" /> 
                            
                            <!-- GW NO a Procesar (R2) -->
                            <path class="path-no" d="M 1195 90 L 1240 90 L 1240 270 L 1285 270" />
                            <text x="1245" y="180" class="label-path label-no">NO (Una cuota)</text>

                            <!-- GW YES (Bucle Manual a Record Payment) -->
                            <path class="path-loop" d="M 1160 55 L 1160 30 L 960 30 L 960 230" />
                            <text x="1010" y="20" class="label-path label-loop">SÍ (Repetir carga manual)</text>

                            <!-- Procesar a FIN -->
                            <path d="M 1430 270 L 1530 270" /> 
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <hr>

        <!-- ==================== SECCIÓN TO-BE ==================== -->
        <div class="diagram-section">
            <button id="btnTobe" class="btn-download btn-tobe" onclick="descargarImagen('diagrama-tobe', 'Cuotas_TO-BE.png', 'btnTobe', 'TO-BE')">
                Descargar Diagrama TO-BE
            </button>
            
            <div class="canvas" id="diagrama-tobe">
                <div class="main-label label-tobe">PROCESO OPTIMIZADO (TO-BE)</div>
                
                <div class="grid-container">
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>
                    <div class="lane-line"></div>

                    <!-- Headers -->
                    <div class="header header-1">Sistema vTiger<br><span>(Ejecutor Central)</span></div>
                    <div class="header header-2">Operador CRM<br><span>(Supervisor)</span></div>
                    <div class="header header-3">API BCV<br><span>(Servicio Externo)</span></div>

                    <!-- NODOS TO-BE -->
                    <!-- R1: Sistema -->
                    <div class="cell" style="grid-column: 2; grid-row: 1;"><div class="node-start">INICIO</div></div>
                    
                    <div class="cell" style="grid-column: 3; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">1. OCR Metadatos</div>
                            <div class="node-desc">Extracción automática de PDF/Imagen</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 5; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">3. Calcular/Validar</div>
                            <div class="node-desc">Cruza monto vs. deuda del alumno</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 6; grid-row: 1;">
                        <div class="diamond-container">
                            <div class="diamond"><span>¿Datos<br>Coinciden?</span></div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 7; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">4. Auto-Payment</div>
                            <div class="node-desc">Crea registro. Bucle automático si hay saldo a favor</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 8; grid-row: 1;">
                        <div class="node node-automation">
                            <div class="node-title">5. Facturar</div>
                            <div class="node-desc">Generar documento, procesar y notificar</div>
                        </div>
                    </div>

                    <div class="cell" style="grid-column: 9; grid-row: 1;"><div class="node-end">FIN</div></div>

                    <!-- R2: Operador (Excepción) -->
                    <div class="cell" style="grid-column: 7; grid-row: 2;">
                        <div class="node node-exception">
                            <div class="node-title">Revisión Manual</div>
                            <div class="node-desc">Alerta por discrepancia (Intervención humana)</div>
                        </div>
                    </div>
                    <div class="cell" style="grid-column: 8; grid-row: 2;"><div class="node-end">FIN</div></div>

                    <!-- R3: API Externa -->
                    <div class="cell" style="grid-column: 4; grid-row: 3;">
                        <div class="node node-external">
                            <div class="node-title">2. API BCV</div>
                            <div class="node-desc">Consulta de tasa histórica programática</div>
                        </div>
                    </div>

                    <!-- FLECHAS TO-BE (ORTOGONALES) -->
                    <div class="svg-overlay">
                        <svg width="100%" height="100%">
                            <!-- Start a N1 -->
                            <path d="M 235 90 L 285 90" />
                            
                            <!-- N1 (R1) a API BCV (R3) -->
                            <path d="M 430 90 L 460 90 L 460 450 L 485 450" />
                            
                            <!-- API BCV (R3) a Validar (R1) -->
                            <path d="M 630 450 L 660 450 L 660 90 L 685 90" />
                            
                            <!-- Validar a GW -->
                            <path d="M 830 90 L 920 90" />
                            
                            <!-- GW YES a Auto-Payment -->
                            <path class="path-yes" d="M 995 90 L 1085 90" />
                            <text x="1010" y="80" class="label-path label-yes">SÍ (Éxito)</text>
                            
                            <!-- Bucle Automático en Auto-Payment -->
                            <path class="path-loop" d="M 1190 55 L 1190 20 L 1130 20 L 1130 50" />
                            <text x="1135" y="12" class="label-path label-loop">Bucle Saldo</text>

                            <!-- GW NO a Revisión Manual -->
                            <path class="path-no" d="M 960 125 L 960 270 L 1085 270" />
                            <text x="970" y="200" class="label-path label-no">NO (Error)</text>

                            <!-- Auto-Payment a Facturar -->
                            <path d="M 1230 90 L 1285 90" />
                            
                            <!-- Facturar a FIN 1 -->
                            <path d="M 1430 90 L 1530 90" />
                            
                            <!-- Revisión Manual a FIN 2 -->
                            <path d="M 1230 270 L 1330 270" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

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
    html_completo = get_html_content()
    ruta_archivo = os.path.abspath("cuotas_diagramas.html")
    
    with open(ruta_archivo, "w", encoding="utf-8") as file:
        file.write(html_completo)
    
    print(f"Archivo generado correctamente en:\n{ruta_archivo}")
    webbrowser.open("file://" + ruta_archivo)

if __name__ == "__main__":
    main()