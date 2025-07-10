"""
Capa de Funcionalidad - Algoritmo de Huffman
Implementa la codificación y decodificación usando el algoritmo de Huffman
"""

import heapq
from collections import defaultdict, Counter
from utils.frequency_calculator import FrequencyCalculator
from utils.statistics import StatisticsCalculator

class Node:
    """Nodo del árbol de Huffman"""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    """Implementación del algoritmo de Huffman"""
    
    def __init__(self):
        self.root = None
        self.codes = {}
        
    def build_tree(self, frequencies):
        """Construye el árbol de Huffman"""
        heap = []
        
        # Crear nodos hoja para cada carácter
        for char, freq in frequencies.items():
            node = Node(char, freq)
            heapq.heappush(heap, node)
            
        # Construir el árbol
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)
            
        self.root = heap[0] if heap else None
        
    def generate_codes(self, node=None, code=""):
        """Genera los códigos de Huffman"""
        if node is None:
            node = self.root
            
        if node is None:
            return
            
        # Si es una hoja, guardar el código
        if node.char is not None:
            self.codes[node.char] = code if code else "0"  # Caso especial para un solo carácter
            return
            
        # Recorrer recursivamente
        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")
        
    def encode(self, text):
        """Codifica el texto usando Huffman"""
        if not text:
            return None
            
        # Calcular frecuencias
        freq_calc = FrequencyCalculator()
        frequencies = freq_calc.calculate_frequencies(text)
        
        # Construir árbol y generar códigos
        self.build_tree(frequencies)
        self.codes = {}
        self.generate_codes()
        
        # Codificar texto
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
            
        # Calcular estadísticas
        stats_calc = StatisticsCalculator()
        statistics = stats_calc.calculate_statistics(text, frequencies, self.codes)
        
        # Crear tabla detallada
        table = self.create_detailed_table(text, frequencies, self.codes)
        
        return {
            'original_text': text,
            'encoded_text': encoded_text,
            'codes': self.codes,
            'frequencies': frequencies,
            'statistics': statistics,
            'table': table
        }
        
    def decode(self, encoded_text):
        """Decodifica el texto usando el árbol de Huffman"""
        if not encoded_text or not self.root:
            return ""
            
        decoded_text = ""
        current_node = self.root
        
        for bit in encoded_text:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right
                
            # Si llegamos a una hoja
            if current_node.char is not None:
                decoded_text += current_node.char
                current_node = self.root
                
        return decoded_text
        
    def create_detailed_table(self, text, frequencies, codes):
        """Crea una tabla detallada con todas las estadísticas"""
        table = {}
        total_chars = len(text)
        
        for char, freq in frequencies.items():
            probability = freq / total_chars
           
            if probability > 0:
                import math
                information = math.log2(1 / probability)
            else:
                information = 0
                
            entropy = probability * information
            code = codes[char]
            bits = len(code)
            avg_length = probability * bits
            
            table[char] = {
                'frequency': freq,
                'probability': probability,
                'code': code,
                'information': information,
                'entropy': entropy,
                'bits': bits,
                'avg_length': avg_length
            }
            
        return table