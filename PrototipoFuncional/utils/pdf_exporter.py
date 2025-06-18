"""
Utilidad para exportar resultados a PDF
Genera reportes completos con tablas y gráficos
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
import matplotlib.pyplot as plt
import io
import base64

class PDFExporter:
    """Exportador de resultados a PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )
        
    def export_results(self, filename, original_text, huffman_results, shannon_results):
        """
        Exporta los resultados completos a PDF
        
        Args:
            filename (str): Nombre del archivo PDF
            original_text (str): Texto original
            huffman_results (dict): Resultados de Huffman
            shannon_results (dict): Resultados de Shannon-Fano
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        title = Paragraph("Reporte de Compresión de Datos", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Información del texto original
        story.extend(self.create_text_info_section(original_text))
        
        # Resultados de Huffman
        story.extend(self.create_algorithm_section("Huffman", huffman_results))
        
        # Resultados de Shannon-Fano
        story.extend(self.create_algorithm_section("Shannon-Fano", shannon_results))
        
        # Comparación
        story.extend(self.create_comparison_section(huffman_results, shannon_results))
        
        # Construir PDF
        doc.build(story)
        
    def create_text_info_section(self, text):
        """Crea la sección de información del texto"""
        elements = []
        
        # Título de sección
        section_title = Paragraph("Información del Texto Original", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # Información básica
        info_data = [
            ['Longitud del texto:', str(len(text))],
            ['Caracteres únicos:', str(len(set(text)))],
            ['Texto (primeros 200 caracteres):', text[:200] + ('...' if len(text) > 200 else '')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        return elements
        
    def create_algorithm_section(self, algorithm_name, results):
        """Crea una sección para un algoritmo específico"""
        elements = []
        
        # Título de sección
        section_title = Paragraph(f"Resultados - {algorithm_name}", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # Estadísticas generales
        stats = results['statistics']
        stats_data = [
            ['Métrica', 'Valor'],
            ['Longitud promedio', f"{stats['avg_length']:.4f} bits/símbolo"],
            ['Entropía total', f"{stats['total_entropy']:.4f} bits"],
            ['Eficiencia', f"{stats['efficiency']:.4f}"],
            ['Tasa de compresión', f"{stats['compression_ratio']:.2f}%"],
            ['Bits originales', str(stats['original_bits'])],
            ['Bits comprimidos', str(stats['compressed_bits'])]
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 15))
        
        # Tabla de códigos
        code_title = Paragraph(f"Tabla de Códigos - {algorithm_name}", self.styles['Heading3'])
        elements.append(code_title)
        elements.append(Spacer(1, 10))
        
        # Preparar datos de la tabla
        table_data = [['Símbolo', 'Frecuencia', 'Código', 'Información', 'Entropía', 'Bits', 'Probabilidad']]
        
        for symbol, data in results['table'].items():
            symbol_display = symbol if symbol != ' ' else 'ESPACIO'
            row = [
                symbol_display,
                str(data['frequency']),
                data['code'],
                f"{data['information']:.4f}",
                f"{data['entropy']:.4f}",
                str(data['bits']),
                f"{data['probability']:.4f}"
            ]
            table_data.append(row)
            
        code_table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 1*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.8*inch])
        code_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(code_table)
        elements.append(Spacer(1, 20))
        
        return elements
        
    def create_comparison_section(self, huffman_results, shannon_results):
        """Crea la sección de comparación"""
        elements = []
        
        # Título de sección
        section_title = Paragraph("Comparación de Algoritmos", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # Tabla comparativa
        h_stats = huffman_results['statistics']
        s_stats = shannon_results['statistics']
        
        comparison_data = [
            ['Métrica', 'Huffman', 'Shannon-Fano', 'Diferencia'],
            ['Longitud promedio', 
             f"{h_stats['avg_length']:.4f}", 
             f"{s_stats['avg_length']:.4f}",
             f"{abs(h_stats['avg_length'] - s_stats['avg_length']):.4f}"],
            ['Tasa de compresión (%)', 
             f"{h_stats['compression_ratio']:.2f}", 
             f"{s_stats['compression_ratio']:.2f}",
             f"{abs(h_stats['compression_ratio'] - s_stats['compression_ratio']):.2f}"],
            ['Eficiencia', 
             f"{h_stats['efficiency']:.4f}", 
             f"{s_stats['efficiency']:.4f}",
             f"{abs(h_stats['efficiency'] - s_stats['efficiency']):.4f}"],
            ['Bits comprimidos', 
             str(h_stats['compressed_bits']), 
             str(s_stats['compressed_bits']),
             str(abs(h_stats['compressed_bits'] - s_stats['compressed_bits']))]
        ]
        
        comparison_table = Table(comparison_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(comparison_table)
        elements.append(Spacer(1, 15))
        
        # Conclusiones
        conclusion_title = Paragraph("Conclusiones", self.styles['Heading3'])
        elements.append(conclusion_title)
        
        better_compression = "Huffman" if h_stats['compression_ratio'] > s_stats['compression_ratio'] else "Shannon-Fano"
        better_efficiency = "Huffman" if h_stats['efficiency'] > s_stats['efficiency'] else "Shannon-Fano"
        
        conclusions = f"""
        • Mejor compresión: {better_compression}
        • Mejor eficiencia: {better_efficiency}
        • Ambos algoritmos son efectivos para la compresión de datos
        • La diferencia en rendimiento depende de la distribución de frecuencias del texto
        """
        
        conclusion_text = Paragraph(conclusions, self.styles['Normal'])
        elements.append(conclusion_text)
        
        return elements