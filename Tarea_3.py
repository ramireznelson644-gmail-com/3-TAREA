import csv
import os
from graphviz import Digraph

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(valor, self.raiz)
        self.generar_reporte()

    def _insertar_recursivo(self, valor, nodo_actual):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.izquierdo)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.derecho)

    def buscar(self, valor):
        return self._buscar_recursivo(valor, self.raiz)

    def _buscar_recursivo(self, valor, nodo_actual):
        if nodo_actual is None or nodo_actual.valor == valor:
            return nodo_actual
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(valor, nodo_actual.izquierdo)
        return self._buscar_recursivo(valor, nodo_actual.derecho)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
        self.generar_reporte()

    def _eliminar_recursivo(self, raiz, valor):
        if raiz is None:
            return raiz
        if valor < raiz.valor:
            raiz.izquierdo = self._eliminar_recursivo(raiz.izquierdo, valor)
        elif valor > raiz.valor:
            raiz.derecho = self._eliminar_recursivo(raiz.derecho, valor)
        else:
            if raiz.izquierdo is None:
                return raiz.derecho
            elif raiz.derecho is None:
                return raiz.izquierdo
            temp = self._min_valor_nodo(raiz.derecho)
            raiz.valor = temp.valor
            raiz.derecho = self._eliminar_recursivo(raiz.derecho, temp.valor)
        return raiz

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def generar_reporte(self):
        dot = Digraph(comment='Árbol Binario de Búsqueda')
        if self.raiz:
            self._agregar_nodos_dot(self.raiz, dot)
        dot.render('arbol_abb', format='png', cleanup=True)
        print("\n[Sistema] Imagen 'arbol_abb.png' actualizada.")

    def _agregar_nodos_dot(self, nodo, dot):
        if nodo:
            dot.node(str(nodo.valor), str(nodo.valor))
            if nodo.izquierdo:
                dot.edge(str(nodo.valor), str(nodo.izquierdo.valor))
                self._agregar_nodos_dot(nodo.izquierdo, dot)
            if nodo.derecho:
                dot.edge(str(nodo.valor), str(nodo.derecho.valor))
                self._agregar_nodos_dot(nodo.derecho, dot)

def cargar_desde_archivo(arbol, ruta):
    try:
        with open(ruta, 'r') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                for dato in fila:
                    arbol.insertar(int(dato.strip()))
        print(f"Datos cargados exitosamente desde {ruta}")
    except FileNotFoundError:
        print("Error: Archivo no encontrado.")
    except ValueError:
        print("Error: El archivo contiene datos no numéricos.")

def menu():
    mi_arbol = ABB()
    while True:
        print("\n--- MENÚ INTERACTIVO ABB ---")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde archivo (.csv / .txt)")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            num = int(input("Ingrese el número a insertar: "))
            mi_arbol.insertar(num)
        elif opcion == '2':
            num = int(input("Ingrese el número a buscar: "))
            resultado = mi_arbol.buscar(num)
            print("Número encontrado" if resultado else "Número no encontrado")
        elif opcion == '3':
            num = int(input("Ingrese el número a eliminar: "))
            mi_arbol.eliminar(num)
        elif opcion == '4':
            ruta = input("Ingrese la ruta del archivo (ej: datos.csv): ")
            cargar_desde_archivo(mi_arbol, ruta)
        elif opcion == '5':
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()