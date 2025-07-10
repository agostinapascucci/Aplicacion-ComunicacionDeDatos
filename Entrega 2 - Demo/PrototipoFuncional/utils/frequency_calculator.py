"""
Utilidad para calcular frecuencias de símbolos
Proporciona métodos para analizar la distribución de caracteres en el texto
"""

from collections import Counter

class FrequencyCalculator:
    """Calculadora de frecuencias de símbolos"""
    
    @staticmethod
    def calculate_frequencies(text):
        """
        Calcula la frecuencia de cada símbolo en el texto
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            dict: Diccionario con símbolo como clave y frecuencia como valor
        """
        if not text:
            return {}
            
        return dict(Counter(text))
        
    @staticmethod
    def calculate_probabilities(frequencies, total_chars):
        """
        Calcula las probabilidades de cada símbolo
        
        Args:
            frequencies (dict): Frecuencias de símbolos
            total_chars (int): Total de caracteres
            
        Returns:
            dict: Diccionario con símbolo como clave y probabilidad como valor
        """
        if total_chars == 0:
            return {}
            
        probabilities = {}
        for char, freq in frequencies.items():
            probabilities[char] = freq / total_chars
            
        return probabilities
        
    @staticmethod
    def get_sorted_frequencies(frequencies, reverse=True):
        """
        Obtiene las frecuencias ordenadas
        
        Args:
            frequencies (dict): Frecuencias de símbolos
            reverse (bool): Si True, ordena de mayor a menor
            
        Returns:
            list: Lista de tuplas (símbolo, frecuencia) ordenadas
        """
        return sorted(frequencies.items(), key=lambda x: x[1], reverse=reverse)