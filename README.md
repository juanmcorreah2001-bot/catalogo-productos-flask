# Catálogo Dinámico de Productos — Flask + Quicksort + Búsqueda Binaria (LPII)

Aplicación web desacoplada construida con **Flask (Python)** en el backend y **HTML5 + CSS3 + JavaScript (Fetch API)** en el frontend. Implementa ordenamiento con **Quicksort**, **Búsqueda Binaria** con precondición de ordenamiento y un **Benchmark** comparativo frente a **Ordenamiento Burbuja** con 1.000 elementos.

## Estructura del repositorio

```text
catalogo-productos-flask/
├── app.py
├── productos.json
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── templates/
    └── index.html
```

## Requisitos previos

- Python 3.9 o superior
- `pip` instalado

## Instalación y ejecución local

1. **Clonar el repositorio:**
   ```bash
  git clone https://github.com/juanmcorreah2001-bot/catalogo-productos-flask.git
cd catalogo-productos-flask
   ```

2. **Crear y activar un entorno virtual:**
   - En Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - En macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

5. Abrir en el navegador: `http://127.0.0.1:5000`

## Endpoints de la API REST

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Renderiza la interfaz web interactiva (`templates/index.html`). |
| `GET` | `/api/productos?sort_by=precio&order=asc` | Retorna el catálogo ordenado con **Quicksort**. Campos válidos: `id`, `nombre`, `categoria`, `precio`, `stock`. Órdenes: `asc`, `desc`. |
| `GET` | `/api/productos/buscar?id=101` | Aplica la precondición de ordenamiento ascendente por `id` con Quicksort y ejecuta **Búsqueda Binaria** (`O(log n)`). |
| `GET` | `/api/benchmark?n=1000` | Mide el tiempo en milisegundos de **Quicksort** frente a **Burbuja** sobre `n` elementos generados aleatoriamente y verifica que ambos resultados sean idénticos. |

## Criterios cubiertos

1. **Quicksort modular en Flask:** Ordenamiento sobre `productos.json` sin mutar el archivo original, con validación de parámetros.
2. **Búsqueda Binaria:** Endpoint `/api/productos/buscar?id=X` que garantiza la precondición de ordenamiento antes de buscar y reporta el número de comparaciones.
3. **Frontend responsivo con `fetch()`:** Actualiza tabla, búsqueda y benchmark dinámicamente sin recargar la página.
4. **Benchmark (1.000 elementos):** Medición precisa con `time.perf_counter()` en milisegundos comparando `O(n log n)` vs. `O(n²)`.

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
