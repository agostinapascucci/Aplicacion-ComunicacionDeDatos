# 📃 Codificacion de datos - Grupo 03 - S31
## ⚙️ Funcionalidades
* Carga de texto (por entrada directa o archivo .txt)
*  Cálculo de frecuencia de símbolos
* Construcción de tabla de códigos (Huffman y Shannon-Fano)
*	Codificación y decodificación del mensaje
*	Comparación de resultados: tasa de compresión, eficiencia, longitud promedio de código
*	Visualización de tabla de símbolos y sus códigos
*   En la descarga del resultado muestra la comparación entre ambos códigos

## 💻 Tecnologías utilizadas
 *   Python
 *   Tkinter
 *   Matplotlib
 *   ReportLab

## Como ejecutar la aplicación
1. Clonar el respositorio localmente
2. Abrir la terminal en la carpeta _Prototipo Funcional_
3. Instalar las dependencias requeridas ( esto solo se requiere la primera vez ):
    `pip install matplotlib pandas reportlab`
4. Ejecutar el archivo _main.py_

## Estructura de archivos
    Aplicacion-ComunicacionDeDatos
     |_PrototipoFuncional
     |   |_algorithms
     |   |  |_ __init__.py
     |   |  |_ hufmman-py
     |   |  |_ shannon_fano.py
     |   |_ui
     |   |  |_ __init__.py
     |   |  |_ main_window.py
     |   |_utils
     |   |  |_ __init__.py
     |   |  |_ frequency_calculator.py
     |   |  |_ pdf_exporter.py
     |   |  |_ visualizer.py
     |   |_ main.py -------------- *ejecutar*
     |_PruebaTexto.txt ------------ *archivo de texto que se puede utilizar para la prueba*
     |_README.md
## Ejecutable de la Aplicacion:
[Ejecutable](Entrega 3/PrototipoFuncional-E3/dist/main)


