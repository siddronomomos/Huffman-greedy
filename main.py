import heapq
from collections import Counter
from tkinter import Tk, filedialog, Text, Button, Label, Frame, END
from tkinter import ttk
import threading

class Nodo:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.freq < otro.freq

def construir_arbol_huffman(frecuencias):
    heap = [Nodo(char, freq) for char, freq in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izquierda = heapq.heappop(heap)
        derecha = heapq.heappop(heap)
        fusionado = Nodo(None, izquierda.freq + derecha.freq)
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

def codificar_texto(texto, libro_codigos):
    return ''.join(libro_codigos[char] for char in texto)

def decodificar_texto(texto_codificado, raiz):
    texto_decodificado = []
    nodo = raiz
    for bit in texto_codificado:
        nodo = nodo.izquierda if bit == '0' else nodo.derecha
        if nodo.char is not None:
            texto_decodificado.append(nodo.char)
            nodo = raiz
    return ''.join(texto_decodificado)

def calcular_ratio_compresion(texto_original, texto_codificado):
    tamano_original = len(texto_original) * 8  # en bits
    tamano_codificado = len(texto_codificado)  # en bits
    return tamano_original, tamano_codificado

def calcular_similitud(texto1, texto2):
    coincidencias = sum(1 for a, b in zip(texto1, texto2) if a == b)
    return (coincidencias / len(texto1)) * 100

def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        threading.Thread(target=procesar_archivo, args=(ruta_archivo,)).start()

def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        texto = archivo.read()
    frecuencias = Counter(texto)
    raiz = construir_arbol_huffman(frecuencias)
    libro_codigos = generar_codigos(raiz)
    texto_codificado = codificar_texto(texto, libro_codigos)
    texto_decodificado = decodificar_texto(texto_codificado, raiz)
    tamano_original, tamano_codificado = calcular_ratio_compresion(texto, texto_codificado)
    similitud = calcular_similitud(texto, texto_decodificado)

    text_original.delete(1.0, END)
    text_original.insert(END, texto)

    text_codificado.delete(1.0, END)
    text_codificado.insert(END, texto_codificado)

    text_decodificado.delete(1.0, END)
    text_decodificado.insert(END, texto_decodificado)

    text_comparacion.delete(1.0, END)
    text_comparacion.insert(END, f"Tamaño Original: {tamano_original} bits\n")
    text_comparacion.insert(END, f"Tamaño Codificado: {tamano_codificado} bits\n")
    text_comparacion.insert(END, f"Ratio de Compresión: {tamano_codificado/tamano_original:.2f}\n")
    text_comparacion.insert(END, f"Similitud entre Original y Decodificado: {similitud:.2f}%\n")

app = Tk()
app.title("Compresión Huffman")

frame = Frame(app, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label_titulo = Label(frame, text="Compresión Huffman", font=("Helvetica", 16))
label_titulo.pack(pady=10)

boton_abrir = Button(frame, text="Abrir Archivo", command=abrir_archivo)
boton_abrir.pack(pady=5)

notebook = ttk.Notebook(frame)
notebook.pack(pady=10)

tab_original = Frame(notebook)
tab_codificado = Frame(notebook)
tab_decodificado = Frame(notebook)
tab_comparacion = Frame(notebook)

notebook.add(tab_original, text="Texto Original")
notebook.add(tab_codificado, text="Texto Codificado")
notebook.add(tab_decodificado, text="Texto Decodificado")
notebook.add(tab_comparacion, text="Comparación")

text_original = Text(tab_original, wrap='word', height=30, width=80)
text_original.pack(pady=10)

text_codificado = Text(tab_codificado, wrap='word', height=30, width=80)
text_codificado.pack(pady=10)

text_decodificado = Text(tab_decodificado, wrap='word', height=30, width=80)
text_decodificado.pack(pady=10)

text_comparacion = Text(tab_comparacion, wrap='word', height=30, width=80)
text_comparacion.pack(pady=10)

app.mainloop()