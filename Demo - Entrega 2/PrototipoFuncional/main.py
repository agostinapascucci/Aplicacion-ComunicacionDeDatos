"""
Aplicación de Compresión de Datos - Huffman y Shannon-Fano
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from ui.main_window import MainWindow

def main():
    """
    Función principal que inicializa la aplicación
    """
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()