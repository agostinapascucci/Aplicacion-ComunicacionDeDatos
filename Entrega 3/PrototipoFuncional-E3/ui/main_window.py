"""
Capa de Presentación - Interfaz gráfica principal
Maneja toda la interacción con el usuario y la visualización de resultados
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkFont
import ttkthemes as ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from algorithms.huffman import HuffmanCoding
from algorithms.shannon_fano import ShannonFanoCoding
from utils.frequency_calculator import FrequencyCalculator
from utils.statistics import StatisticsCalculator
from utils.visualizer import DataVisualizer
from utils.pdf_exporter import PDFExporter

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresión de Datos - Huffman vs Shannon-Fano")
        self.root.geometry("1200x800")
        # Crear fuente grande y en negrita
        bold_font = tkFont.Font(family="Helvetica", size=11, weight="bold")
        # Estilo general
        style = ttk.Style()
        style.theme_use(themename="clam")
        style.map(
            "TButton",
            background=[('active', "#050A3F"), ('pressed', '#009ACD')],
            foreground=[('disabled', 'gray'), ('pressed', 'white'), ('active', 'white')])
        style.configure("TLabel", padding=6)
        
        
        # Variables de instancia
        self.text_data = ""
        self.huffman_results = None
        self.shannon_results = None
        
        # Inicializar componentes
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Sección de entrada de datos
        self.create_input_section(main_frame)
        
        # Sección de controles
        self.create_controls_section(main_frame)
        
        # Sección de resultados
        self.create_results_section(main_frame)
        
    def create_input_section(self, parent):
        """Crea la sección de entrada de datos"""
        input_frame = ttk.LabelFrame(parent, text="Cargar texto", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Área de texto
        self.text_area = scrolledtext.ScrolledText(input_frame, height=6, width=80)
        self.text_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Botones
        ttk.Button(input_frame, text="Cargar Archivo", 
                  command=self.load_file,
                  style="TButton").grid(row=1, column=0, padx=(0, 5))
        ttk.Button(input_frame, text="Limpiar", 
                  command=self.clear_text,
                  style="TButton").grid(row=1, column=1, padx=5)
        ttk.Button(input_frame, text="Texto de Ejemplo", 
                  command=self.load_sample_text,
                  style="TButton").grid(row=1, column=2, padx=(5, 0))
        
    def create_controls_section(self, parent):
        """Crea la sección de controles"""
        controls_frame = ttk.LabelFrame(parent, text="Controles", padding="5")
        controls_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="Comparar Algoritmos",
            command=lambda: [
                self.process_huffman(),
                self.process_shannon_fano(),
                self.compare_algorithms()
            ],
            style="TButton"
        ).grid(row=0, column=2, padx=5)
        ttk.Button(controls_frame, text="Exportar PDF", 
                  command=self.export_pdf,
                  style="TButton").grid(row=0, column=3, padx=(5, 0))
        
    def create_results_section(self, parent):
        """Crea la sección de resultados"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Pestaña de tablas
        self.create_tables_tab()
        
        # Pestaña de gráficos
        self.create_charts_tab()
        
        # Pestaña de comparación
        self.create_comparison_tab()
        
    def create_tables_tab(self):
        """Crea la pestaña de tablas"""
        tables_frame = ttk.Frame(self.notebook)
        self.notebook.add(tables_frame, text="Resultados")
        
        # Frame para Huffman
        huffman_frame = ttk.LabelFrame(tables_frame, text="Huffman", padding="5")
        huffman_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Treeview para Huffman
        self.huffman_tree = ttk.Treeview(huffman_frame, columns=('freq', 'code', 'info', 'entropy', 'bits', 'prob', 'avg_len'), show='tree headings')
        self.setup_treeview(self.huffman_tree)
        self.huffman_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para Huffman
        huffman_scroll = ttk.Scrollbar(huffman_frame, orient=tk.VERTICAL, command=self.huffman_tree.yview)
        huffman_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.huffman_tree.configure(yscrollcommand=huffman_scroll.set)
        
        # Frame para Shannon-Fano
        shannon_frame = ttk.LabelFrame(tables_frame, text="Shannon-Fano", padding="5")
        shannon_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Treeview para Shannon-Fano
        self.shannon_tree = ttk.Treeview(shannon_frame, columns=('freq', 'code', 'info', 'entropy', 'bits', 'prob', 'avg_len'), show='tree headings')
        self.setup_treeview(self.shannon_tree)
        self.shannon_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para Shannon-Fano
        shannon_scroll = ttk.Scrollbar(shannon_frame, orient=tk.VERTICAL, command=self.shannon_tree.yview)
        shannon_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.shannon_tree.configure(yscrollcommand=shannon_scroll.set)
        
        # Configurar grid weights
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.columnconfigure(1, weight=1)
        tables_frame.rowconfigure(0, weight=1)
        huffman_frame.columnconfigure(0, weight=1)
        huffman_frame.rowconfigure(0, weight=1)
        shannon_frame.columnconfigure(0, weight=1)
        shannon_frame.rowconfigure(0, weight=1)
        
    def setup_treeview(self, tree):
        """Configura las columnas del Treeview"""
        tree.heading('#0', text='Símbolo')
        tree.heading('freq', text='Frecuencia')
        tree.heading('code', text='Código')
        tree.heading('info', text='Información')
        tree.heading('entropy', text='Entropía')
        tree.heading('bits', text='Bits')
        tree.heading('prob', text='Probabilidad')
        tree.heading('avg_len', text='Long. Promedio')
        
        tree.column('#0', width=80)
        tree.column('freq', width=80)
        tree.column('code', width=100)
        tree.column('info', width=100)
        tree.column('entropy', width=100)
        tree.column('bits', width=80)
        tree.column('prob', width=100)
        tree.column('avg_len', width=100)
        
    def create_charts_tab(self):
        """Crea la pestaña de gráficos"""
        self.charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_frame, text="Gráficos")
        
    def create_comparison_tab(self):
        """Crea la pestaña de comparación"""
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="Comparación")
        
        # Área de texto para mostrar comparación
        self.comparison_text = scrolledtext.ScrolledText(comparison_frame, height=20, width=80)
        self.comparison_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        comparison_frame.columnconfigure(0, weight=1)
        comparison_frame.rowconfigure(0, weight=1)
        
    def load_file(self):
        """Carga un archivo de texto"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
                
    def clear_text(self):
        """Limpia el área de texto"""
        self.text_area.delete(1.0, tk.END)
        
    def load_sample_text(self):
        """Carga un texto de ejemplo"""
        sample_text = """DDABEBADACABAAECDCBAEACABCBAADDEAACAEAB"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, sample_text)
        
    def get_text_data(self):
        """Obtiene el texto del área de entrada"""
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            return None
        return text
        
    def process_huffman(self):
        """Procesa el texto con el algoritmo Huffman"""
        text = self.get_text_data()
        if not text:
            messagebox.showwarning("Advertencia", "Por favor ingrese o cargue un texto.")
            return
            
        try:
            huffman = HuffmanCoding()
            self.huffman_results = huffman.encode(text)
            self.update_table(self.huffman_tree, self.huffman_results)
            messagebox.showinfo("Éxito", "Procesamiento con Huffman completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en Huffman: {str(e)}")
            
    def process_shannon_fano(self):
        """Procesa el texto con el algoritmo Shannon-Fano"""
        text = self.get_text_data()
        if not text:
            return
            
        try:
            shannon = ShannonFanoCoding()
            self.shannon_results = shannon.encode(text)
            self.update_table(self.shannon_tree, self.shannon_results)
            messagebox.showinfo("Éxito", "Procesamiento con Shannon-Fano completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en Shannon-Fano: {str(e)}")
            
    def update_table(self, tree, results):
        """Actualiza la tabla con los resultados"""
        # Limpiar tabla
        for item in tree.get_children():
            tree.delete(item)
            
        # Agregar datos
        for symbol, data in results['table'].items():
            symbol_display = symbol if symbol != ' ' else 'ESPACIO'
            tree.insert('', 'end', text=symbol_display, values=(
                data['frequency'],
                data['code'],
                f"{data['information']:.4f}",
                f"{data['entropy']:.4f}",
                data['bits'],
                f"{data['probability']:.4f}",
                f"{data['avg_length']:.4f}"
            ))
            
    def compare_algorithms(self):
        """Compara los resultados de ambos algoritmos"""
            
        # Generar comparación
        comparison = self.generate_comparison()
        
        # Mostrar en la pestaña de comparación
        self.comparison_text.delete(1.0, tk.END)
        self.comparison_text.insert(1.0, comparison)
        
        # Generar gráficos
        self.generate_charts()
        
        # Cambiar a la pestaña de comparación
        self.notebook.select(2)
        
    def generate_comparison(self):
        """Genera el texto de comparación"""
        h_stats = self.huffman_results['statistics']
        s_stats = self.shannon_results['statistics']
        
        comparison = f"""
COMPARACIÓN DE ALGORITMOS DE COMPRESIÓN
=====================================

HUFFMAN:
--------
• Longitud promedio: {h_stats['avg_length']:.4f} bits/símbolo
• Tasa de compresión: {h_stats['compression_ratio']:.2f}%
• Eficiencia: {h_stats['efficiency']:.4f}
• Entropía total: {h_stats['total_entropy']:.4f}
• Texto original: {h_stats['original_bits']} bits
• Texto comprimido: {h_stats['compressed_bits']} bits

SHANNON-FANO:
-------------
• Longitud promedio: {s_stats['avg_length']:.4f} bits/símbolo
• Tasa de compresión: {s_stats['compression_ratio']:.2f}%
• Eficiencia: {s_stats['efficiency']:.4f}
• Entropía total: {s_stats['total_entropy']:.4f}
• Texto original: {s_stats['original_bits']} bits
• Texto comprimido: {s_stats['compressed_bits']} bits

COMPARACIÓN:
-----------
• Mejor compresión: {"Huffman" if h_stats['compression_ratio'] > s_stats['compression_ratio'] else "Shannon-Fano"}
• Diferencia en compresión: {abs(h_stats['compression_ratio'] - s_stats['compression_ratio']):.2f}%
• Mejor eficiencia: {"Huffman" if h_stats['efficiency'] > s_stats['efficiency'] else "Shannon-Fano"}
• Diferencia en eficiencia: {abs(h_stats['efficiency'] - s_stats['efficiency']):.4f}
"""
        return comparison
        
    def generate_charts(self):
        """Genera los gráficos de comparación"""
        # Limpiar frame de gráficos
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
            
        visualizer = DataVisualizer()
        fig = visualizer.create_comparison_charts(self.huffman_results, self.shannon_results)
        
        # Integrar matplotlib con tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def export_pdf(self):
        """Exporta los resultados a PDF"""
        if not self.huffman_results or not self.shannon_results:
            messagebox.showwarning("Advertencia", "Debe procesar el texto con ambos algoritmos primero.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Guardar PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if file_path:
            try:
                exporter = PDFExporter()
                exporter.export_results(
                    file_path, 
                    self.get_text_data(),
                    self.huffman_results, 
                    self.shannon_results
                )
                messagebox.showinfo("Éxito", f"PDF exportado exitosamente: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")