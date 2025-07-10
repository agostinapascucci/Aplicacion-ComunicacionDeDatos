"""
Capa de Funcionalidad - Algoritmo de Shannon-Fano
Implementa la codificación y decodificación usando el algoritmo de Shannon-Fano
"""

from collections import Counter
from utils.frequency_calculator import FrequencyCalculator
from utils.statistics import StatisticsCalculator

class ShannonFanoCoding:
    """Implementación del algoritmo de Shannon-Fano"""
    
    def __init__(self):
        self.codes = {}
        
    def shannon_fano_recursive(self, symbols, codes, code=""):
        """Implementación recursiva del algoritmo Shannon-Fano"""
        if len(symbols) == 1:
            # Caso base: un solo símbolo
            char, freq = symbols[0]
            codes[char] = code if code else "0"
            return
            
        if len(symbols) == 0:
            return
            
        # Calcular la suma total de frecuencias
        total_freq = sum(freq for char, freq in symbols)
        
        # Encontrar el punto de división óptimo
        best_split = self.find_best_split(symbols, total_freq)
        
        # Dividir en dos grupos
        left_group = symbols[:best_split]
        right_group = symbols[best_split:]
        
        # Asignar códigos recursivamente
        self.shannon_fano_recursive(left_group, codes, code + "0")
        self.shannon_fano_recursive(right_group, codes, code + "1")
        
    def find_best_split(self, symbols, total_freq):
        """Encuentra el mejor punto de división"""
        best_split = 1
        best_diff = float('inf')
        
        for i in range(1, len(symbols)):
            left_freq = sum(freq for char, freq in symbols[:i])
            right_freq = total_freq - left_freq
            diff = abs(left_freq - right_freq)
            
            if diff < best_diff:
                best_diff = diff
                best_split = i
                
        return best_split
        
    def encode(self, text):
        """Codifica el texto usando Shannon-Fano"""
        if not text:
            return None
            
        # Calcular frecuencias
        freq_calc = FrequencyCalculator()
        frequencies = freq_calc.calculate_frequencies(text)
        
        # Ordenar símbolos por frecuencia (descendente)
        sorted_symbols = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        # Generar códigos usando Shannon-Fano
        self.codes = {}
        self.shannon_fano_recursive(sorted_symbols, self.codes)
        
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
        
    def decode(self, encoded_text, codes):
        """Decodifica el texto usando los códigos Shannon-Fano"""
        if not encoded_text:
            return ""
            
        # Crear diccionario inverso
        reverse_codes = {code: char for char, code in codes.items()}
        
        decoded_text = ""
        current_code = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_codes:
                decoded_text += reverse_codes[current_code]
                current_code = ""
                
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