"""
Utilidad para visualización de datos
Genera gráficos usando matplotlib para mostrar resultados de compresión
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

class DataVisualizer:
    """Generador de visualizaciones para datos de compresión"""
    
    def __init__(self):
        plt.style.use('default')
        
    def create_comparison_charts(self, huffman_results, shannon_results):
        """
        Crea gráficos de comparación entre Huffman y Shannon-Fano
        
        Args:
            huffman_results (dict): Resultados de Huffman
            shannon_results (dict): Resultados de Shannon-Fano
            
        Returns:
            Figure: Figura de matplotlib con los gráficos
        """
        fig = Figure(figsize=(15, 10))
        
        # Gráfico 1: Comparación de frecuencias
        ax1 = fig.add_subplot(2, 3, 1)
        self.plot_frequencies(ax1, huffman_results['frequencies'])
        ax1.set_title('Frecuencias de Símbolos')
        
        # Gráfico 2: Longitudes de código Huffman
        ax2 = fig.add_subplot(2, 3, 2)
        self.plot_code_lengths(ax2, huffman_results['codes'], 'Huffman')
        ax2.set_title('Longitudes de Código - Huffman')
        
        # Gráfico 3: Longitudes de código Shannon-Fano
        ax3 = fig.add_subplot(2, 3, 3)
        self.plot_code_lengths(ax3, shannon_results['codes'], 'Shannon-Fano')
        ax3.set_title('Longitudes de Código - Shannon-Fano')
        
        # Gráfico 4: Comparación de estadísticas
        ax4 = fig.add_subplot(2, 3, 4)
        self.plot_statistics_comparison(ax4, huffman_results['statistics'], shannon_results['statistics'])
        ax4.set_title('Comparación de Estadísticas')
        
        # Gráfico 5: Eficiencia vs Entropía
        ax5 = fig.add_subplot(2, 3, 5)
        self.plot_efficiency_entropy(ax5, huffman_results['statistics'], shannon_results['statistics'])
        ax5.set_title('Eficiencia vs Entropía')
        
        # Gráfico 6: Tasa de compresión
        ax6 = fig.add_subplot(2, 3, 6)
        self.plot_compression_ratio(ax6, huffman_results['statistics'], shannon_results['statistics'])
        ax6.set_title('Tasa de Compresión')
        
        fig.tight_layout()
        return fig
        
    def plot_frequencies(self, ax, frequencies):
        """Gráfico de barras de frecuencias"""
        chars = list(frequencies.keys())
        freqs = list(frequencies.values())
        
        # Reemplazar espacios para mejor visualización
        display_chars = [char if char != ' ' else 'ESP' for char in chars]
        
        bars = ax.bar(display_chars, freqs, color='skyblue', edgecolor='navy')
        ax.set_xlabel('Símbolos')
        ax.set_ylabel('Frecuencia')
        ax.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, freq in zip(bars, freqs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{freq}', ha='center', va='bottom')
                   
    def plot_code_lengths(self, ax, codes, algorithm_name):
        """Gráfico de longitudes de código"""
        chars = list(codes.keys())
        lengths = [len(code) for code in codes.values()]
        
        display_chars = [char if char != ' ' else 'ESP' for char in chars]
        
        bars = ax.bar(display_chars, lengths, color='lightcoral', edgecolor='darkred')
        ax.set_xlabel('Símbolos')
        ax.set_ylabel('Longitud del Código (bits)')
        ax.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, length in zip(bars, lengths):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{length}', ha='center', va='bottom')
                   
    def plot_statistics_comparison(self, ax, huffman_stats, shannon_stats):
        """Gráfico de comparación de estadísticas"""
        metrics = ['Longitud\nPromedio', 'Entropía\nTotal', 'Eficiencia']
        huffman_values = [
            huffman_stats['avg_length'],
            huffman_stats['total_entropy'],
            huffman_stats['efficiency']
        ]
        shannon_values = [
            shannon_stats['avg_length'],
            shannon_stats['total_entropy'],
            shannon_stats['efficiency']
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, huffman_values, width, label='Huffman', color='lightblue')
        bars2 = ax.bar(x + width/2, shannon_values, width, label='Shannon-Fano', color='lightgreen')
        
        ax.set_xlabel('Métricas')
        ax.set_ylabel('Valores')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        
        # Agregar valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}', ha='center', va='bottom', fontsize=8)
                       
    def plot_efficiency_entropy(self, ax, huffman_stats, shannon_stats):
        """Gráfico de eficiencia vs entropía"""
        algorithms = ['Huffman', 'Shannon-Fano']
        efficiencies = [huffman_stats['efficiency'], shannon_stats['efficiency']]
        entropies = [huffman_stats['total_entropy'], shannon_stats['total_entropy']]
        
        ax.scatter(entropies, efficiencies, s=100, c=['blue', 'green'], alpha=0.7)
        
        for i, alg in enumerate(algorithms):
            ax.annotate(alg, (entropies[i], efficiencies[i]), 
                       xytext=(5, 5), textcoords='offset points')
                       
        ax.set_xlabel('Entropía Total')
        ax.set_ylabel('Eficiencia')
        ax.grid(True, alpha=0.3)
        
    def plot_compression_ratio(self, ax, huffman_stats, shannon_stats):
        """Gráfico de tasa de compresión"""
        algorithms = ['Huffman', 'Shannon-Fano']
        ratios = [huffman_stats['compression_ratio'], shannon_stats['compression_ratio']]
        
        bars = ax.bar(algorithms, ratios, color=['gold', 'orange'], edgecolor='darkorange')
        ax.set_ylabel('Tasa de Compresión (%)')
        
        # Agregar valores en las barras
        for bar, ratio in zip(bars, ratios):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{ratio:.2f}%', ha='center', va='bottom')