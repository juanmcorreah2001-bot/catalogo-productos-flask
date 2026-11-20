from pathlib import Path
import json
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "productos.json"
CLAVES_VALIDAS = {"id", "nombre", "categoria", "precio", "stock"}


def cargar_productos():
    """Carga el catálogo de productos desde el archivo productos.json."""
    with DATA_FILE.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def _valor_comparable(item, clave):
    """Normaliza cadenas a minúsculas para un ordenamiento alfabético consistente."""
    valor = item[clave]
    return valor.lower() if isinstance(valor, str) else valor


def quicksort(items, clave, reverse=False):
    """
    Algoritmo Quicksort modular sobre listas de diccionarios.
    Complejidad promedio: O(n log n).
    """
    if len(items) <= 1:
        return list(items)

    pivote = _valor_comparable(items[len(items) // 2], clave)

    if reverse:
        izq = [x for x in items if _valor_comparable(x, clave) > pivote]
        centro = [x for x in items if _valor_comparable(x, clave) == pivote]
        der = [x for x in items if _valor_comparable(x, clave) < pivote]
    else:
        izq = [x for x in items if _valor_comparable(x, clave) < pivote]
        centro = [x for x in items if _valor_comparable(x, clave) == pivote]
        der = [x for x in items if _valor_comparable(x, clave) > pivote]

    return quicksort(izq, clave, reverse) + centro + quicksort(der, clave, reverse)


def bubble_sort(items, clave, reverse=False):
    """
    Algoritmo de ordenamiento Burbuja (Bubble Sort) para comparación en benchmark.
    Complejidad promedio y peor caso: O(n^2).
    """
    arr = list(items)
    n = len(arr)

    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            a = _valor_comparable(arr[j], clave)
            b = _valor_comparable(arr[j + 1], clave)
            if (a < b) if reverse else (a > b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:
            break

    return arr


def busqueda_binaria(items_ordenados, id_objetivo):
    """
    Búsqueda binaria iterativa por 'id'.
    Precondición: la lista 'items_ordenados' debe estar ordenada ascendentemente por 'id'.
    Complejidad: O(log n).
    Retorna una tupla (producto_o_None, numero_de_comparaciones).
    """
    izquierda = 0
    derecha = len(items_ordenados) - 1
    comparaciones = 0

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        comparaciones += 1
        id_actual = items_ordenados[medio]["id"]

        if id_actual == id_objetivo:
            return items_ordenados[medio], comparaciones
        elif id_actual < id_objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None, comparaciones


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/productos")
def get_productos():
    productos = cargar_productos()
    sort_by = request.args.get("sort_by", "precio")
    order = request.args.get("order", "asc")

    if sort_by not in CLAVES_VALIDAS:
        return jsonify({
            "error": f"Campo de ordenamiento inválido: '{sort_by}'.",
            "campos_validos": sorted(CLAVES_VALIDAS),
        }), 400

    reverse = order.lower() == "desc"
    ordenados = quicksort(productos, sort_by, reverse=reverse)
    return jsonify(ordenados)


@app.route("/api/productos/buscar")
def buscar_producto():
    id_param = request.args.get("id")
    if id_param is None or id_param.strip() == "":
        return jsonify({
            "encontrado": False,
            "error": "Debes proporcionar el parámetro 'id'. Ejemplo: /api/productos/buscar?id=101",
        }), 400

    try:
        id_objetivo = int(id_param)
    except ValueError:
        return jsonify({
            "encontrado": False,
            "error": f"El parámetro 'id' debe ser un número entero. Recibido: '{id_param}'.",
        }), 400

    productos = cargar_productos()
    # Precondición obligatoria para búsqueda binaria: ordenar por 'id' ascendente
    productos_ordenados = quicksort(productos, "id", reverse=False)
    resultado, comparaciones = busqueda_binaria(productos_ordenados, id_objetivo)

    if resultado is None:
        return jsonify({
            "encontrado": False,
            "mensaje": f"No se encontró ningún producto con ID {id_objetivo}.",
            "comparaciones": comparaciones,
            "precondicion_ordenamiento": "Ordenado ascendentemente por 'id' con Quicksort",
        }), 404

    return jsonify({
        "encontrado": True,
        "producto": resultado,
        "comparaciones": comparaciones,
        "precondicion_ordenamiento": "Ordenado ascendentemente por 'id' con Quicksort",
    })


@app.route("/api/benchmark")
def benchmark():
    """
    Compara el tiempo de ejecución en milisegundos entre Quicksort y Burbuja
    usando N elementos generados aleatoriamente (por defecto N = 1000).
    """
    n_param = request.args.get("n", "1000")
    try:
        n = int(n_param)
    except ValueError:
        return jsonify({"error": "El parámetro 'n' debe ser un número entero."}), 400

    if n < 10 or n > 5000:
        return jsonify({"error": "El parámetro 'n' debe estar entre 10 y 5000."}), 400

    datos = [
        {"id": i + 1, "nombre": f"Producto {i + 1}", "precio": round(random.uniform(5.0, 2000.0), 2)}
        for i in range(n)
    ]

    inicio_qs = time.perf_counter()
    res_qs = quicksort(datos, "precio", reverse=False)
    tiempo_qs_ms = (time.perf_counter() - inicio_qs) * 1000

    inicio_bs = time.perf_counter()
    res_bs = bubble_sort(datos, "precio", reverse=False)
    tiempo_bs_ms = (time.perf_counter() - inicio_bs) * 1000

    precios_qs = [p["precio"] for p in res_qs]
    precios_bs = [p["precio"] for p in res_bs]
    aceleracion = round(tiempo_bs_ms / tiempo_qs_ms, 2) if tiempo_qs_ms > 0 else 0

    return jsonify({
        "elementos": n,
        "quicksort_ms": round(tiempo_qs_ms, 3),
        "burbuja_ms": round(tiempo_bs_ms, 3),
        "aceleracion_x": aceleracion,
        "resultados_identicos": precios_qs == precios_bs,
    })


if __name__ == "__main__":
    app.run(debug=True)
