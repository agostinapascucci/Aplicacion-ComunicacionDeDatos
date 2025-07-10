"""
Utilidad para cálculos estadísticos
Calcula métricas de compresión, entropía y eficiencia
"""

import math

class StatisticsCalculator:
    """Calculadora de estadísticas de compresión"""
    
    @staticmethod
    def calculate_entropy(probabilities):
        """
        Calcula la entropía del mensaje
        
        Args:
            probabilities (dict): Probabilidades de cada símbolo
            
        Returns:
            float: Entropía en bits
        """
        entropy = 0
        for prob in probabilities.values():
            if prob > 0:
                entropy += prob * math.log2(1 / prob)
        return entropy
        
    @staticmethod
    def calculate_average_length(probabilities, codes):
        """
        Calcula la longitud promedio del código
        
        Args:
            probabilities (dict): Probabilidades de cada símbolo
            codes (dict): Códigos de cada símbolo
            
        Returns:
            float: Longitud promedio en bits
        """
        avg_length = 0
        for char, prob in probabilities.items():
            if char in codes:
                avg_length += prob * len(codes[char])
        return avg_length
        
    @staticmethod
    def calculate_compression_ratio(original_bits, compressed_bits):
        """
        Calcula la tasa de compresión
        
        Args:
            original_bits (int): Bits del texto original
            compressed_bits (int): Bits del texto comprimido
            
        Returns:
            float: Tasa de compresión como porcentaje
        """
        if original_bits == 0:
            return 0
        return ((original_bits - compressed_bits) / original_bits) * 100
        
    @staticmethod
    def calculate_efficiency(entropy, avg_length):
        """
        Calcula la eficiencia del código
        
        Args:
            entropy (float): Entropía del mensaje
            avg_length (float): Longitud promedio del código
            
        Returns:
            float: Eficiencia (0-1)
        """
        if avg_length == 0:
            return 0
        return entropy / avg_length
        
    def calculate_statistics(self, text, frequencies, codes):
        """
        Calcula todas las estadísticas de compresión
        
        Args:
            text (str): Texto original
            frequencies (dict): Frecuencias de símbolos
            codes (dict): Códigos de símbolos
            
        Returns:
            dict: Diccionario con todas las estadísticas
        """
        total_chars = len(text)
        
        # Calcular probabilidades
        probabilities = {}
        for char, freq in frequencies.items():
            probabilities[char] = freq / total_chars
            
        # Calcular métricas
        entropy = self.calculate_entropy(probabilities)
        avg_length = self.calculate_average_length(probabilities, codes)
        
        # Calcular bits
        original_bits = total_chars * 8  # Asumiendo ASCII
        compressed_bits = sum(len(codes[char]) * freq for char, freq in frequencies.items())
        
        compression_ratio = self.calculate_compression_ratio(original_bits, compressed_bits)
        efficiency = self.calculate_efficiency(entropy, avg_length)
        
        return {
            'total_entropy': entropy,
            'avg_length': avg_length,
            'original_bits': original_bits,
            'compressed_bits': compressed_bits,
            'compression_ratio': compression_ratio,
            'efficiency': efficiency,
            'total_chars': total_chars
        }