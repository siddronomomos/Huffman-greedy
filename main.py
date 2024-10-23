import heapq
from collections import Counter

class NodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izquierda = None
        self.derecha = None

    def __lt__(self, other):
        return self.freq < other.freq

def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(char, freq) for char, freq in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izquierda = heapq.heappop(heap)
        derecha = heapq.heappop(heap)
        fusionado = NodoHuffman(None, izquierda.freq + derecha.freq)
        fusionado.izquierda = izquierda
        fusionado.derecha = derecha
        heapq.heappush(heap, fusionado)

    return heap[0]

def generar_codigos(nodo, prefijo="", libro_codigos={}):
    if nodo is not None:
        if nodo.char is not None:
            libro_codigos[nodo.char] = prefijo
        generar_codigos(nodo.izquierda, prefijo + "0", libro_codigos)
        generar_codigos(nodo.derecha, prefijo + "1", libro_codigos)
    return libro_codigos

def codificacion_huffman(texto):
    frecuencias = Counter(texto)
    arbol_huffman = construir_arbol_huffman(frecuencias)
    return generar_codigos(arbol_huffman)

def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return archivo.read()

if __name__ == "__main__":
    ruta_archivo = '/Users/siddronomomos/Desktop/Huffman greedy/input.txt'
    texto = leer_archivo(ruta_archivo)
    codigos = codificacion_huffman(texto)
    for char, codigo in codigos.items():
        print(f"Carácter: {char} Código: {codigo}")