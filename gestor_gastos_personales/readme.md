# Aplicación de Control de Gastos por Consola

Este sistema en **Python** permite:

- Registrar, modificar y eliminar gastos.
- Visualizar estadísticas detalladas.
- Exportar gastos a archivos **TXT** y **PDF**.

---

## Requisitos Previos

1. **Python 3.8+** instalado en tu sistema. Descargar en https://www.python.org/downloads/
2. **pip** (viene con Python). Verificá con:
   ```bash
   python --version /   py --version
   pip --version
   ```

> Si algún comando no existe, agregá Python al `PATH` o reinstalá marcando _Add Python to PATH_.

---

## Instalación de Dependencias

La aplicación usa la librería externa `reportlab` para generar PDFs.

```bash
pip install reportlab
```

Si da error de permisos:

```bash
pip install --user reportlab
```

---

## Entorno Virtual (Recomendado)

Para aislar dependencias (similar a `node_modules`):

1. Crear:
   ```bash
   python -m venv venv
   ```
2. Activar:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Instalar dependencia:
   ```bash
   pip install reportlab
   ```
4. Ejecutar app:
   ```bash
   python nombre_del_archivo.py
   ```
5. Salir:
   ```bash
   deactivate
   ```

---

## Ejecución de la Aplicación

Desde la carpeta del script:

```bash
python nombre_del_archivo.py
```

El menú interactivo permite:

- Ver lista de gastos
- Registrar nuevo gasto
- Modificar gasto existente
- Eliminar gasto
- Ver estadísticas
- Exportar (TXT o PDF)
- Eliminar todos los gastos
- Salir y guardar

---

## Archivos Generados

- `gastos.json` → Datos persistidos de gastos.
- `gastos_exportados_<fecha>.txt` → Exportación en texto.
- `gastos_exportados_<fecha>.pdf` → Exportación en PDF.

---

## Alternative: requirements.txt

Crear `requirements.txt` con:

```
reportlab
```

Luego:

```bash
pip install -r requirements.txt
```

---

## Guía para usuarios de Node.js/npm

| npm            | pip                |
| -------------- | ------------------ |
| `node_modules` | `venv`             |
| `package.json` | `requirements.txt` |

Pasos rápidos:

1. Instalar Python.
2. `python -m venv venv`
3. Activar entorno.
4. `pip install reportlab`
5. `python nombre_del_archivo.py`
6. `deactivate`

---

## Notas y Solución de Problemas

- **Codificación**: usar terminal en UTF-8.
- **Formato de fecha**: `DD-MM-YYYY`.
- **Error pip**: agregá Python al PATH o usá `--user`.
- **Dependencias**: usá entorno virtual para evitar conflictos SI SOS USUARIO NPM.

---
