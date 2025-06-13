import json
import os
from datetime import datetime, date
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

CATEGORIAS_DISPONIBLES = [
    "Comida",
    "Transporte",
    "Ocio",
    "Salud",
    "Hogar",
    "Otros"
]


def cargar_datos():
    if not os.path.exists("gastos.json"):
        return []
    with open("gastos.json", "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
    if isinstance(data, dict):
        try:
            return list(data.values())
        except Exception:
            return []
    return data


def guardar_datos(datos):
    with open("gastos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


from datetime import date

def ver_gastos(datos):
    if not datos:
        print("No hay gastos registrados.")
        return
    print(f"{'ID':<4} {'Descripción':<25} {'Categoría':<12} {'Monto':<10} {'Fecha':<12}")
    total = 0.0
    for idx, g in enumerate(datos, start=1):
        id_val = g.get("id", idx)
        desc = g.get("descripcion", "")[:25]
        cat = g.get("categoria", "")
        try:
            monto = float(g.get("monto", 0))
        except:
            monto = 0.0
        fecha = g.get("fecha", "")
        total += monto
        print(f"{id_val:<4} {desc:<25} {cat:<12} {monto:<10.2f} {fecha:<12}")
    print("-" * 70)
    fecha_hoy = date.today().strftime('%d/%m/%Y')
    print(f"{'':<4} {'TOTAL':<25} {'':<12} {total:<10.2f} {fecha_hoy:<12}")



def elegir_categoria():
    print("Categorías disponibles:")
    for i, c in enumerate(CATEGORIAS_DISPONIBLES, start=1):
        print(f"{i}. {c}")
    op = input("Elegí categoría (número): ").strip()
    try:
        idx = int(op) - 1
        if 0 <= idx < len(CATEGORIAS_DISPONIBLES):
            return CATEGORIAS_DISPONIBLES[idx]
    except:
        pass
    print("Categoría no válida, se asigna 'Otros'.")
    return "Otros"


def registrar_gasto(datos):
    descripcion = input("Descripción: ").strip()
    while True:
        try:
            monto = float(input("Monto (número): ").strip())
            break
        except:
            print("Monto inválido. Ingresá un número.")
    fecha = input("Fecha (DD-MM-YYYY): ").strip()
    categoria = elegir_categoria()
    nuevo_id = max([g.get("id", 0) for g in datos], default=0) + 1
    datos.append({
        "id": nuevo_id,
        "descripcion": descripcion,
        "categoria": categoria,
        "monto": monto,
        "fecha": fecha
    })
    print("Gasto registrado.")


def modificar_gasto(datos):
    if not datos:
        print("No hay gastos para modificar.")
        return
    try:
        id_buscar = int(input("ID del gasto a modificar: ").strip())
    except:
        print("ID inválido.")
        return
    for g in datos:
        if g.get("id") == id_buscar:
            nueva_desc = input(f"Nueva descripción (actual: {g.get('descripcion')}): ").strip()
            if nueva_desc:
                g["descripcion"] = nueva_desc
            nueva_cat = input(f"Nueva categoría (actual: {g.get('categoria')}), Enter para mantener: ").strip()
            if nueva_cat:
                g["categoria"] = nueva_cat
            while True:
                nm = input(f"Nuevo monto (actual: {g.get('monto')}): ").strip()
                if not nm:
                    break
                try:
                    g["monto"] = float(nm)
                    break
                except:
                    print("Monto inválido. Ingresá un número.")
            nf = input(f"Nueva fecha (actual: {g.get('fecha')}): ").strip()
            if nf:
                g["fecha"] = nf
            print("Gasto modificado.")
            return
    print("No se encontró un gasto con ese ID.")


def eliminar_gasto(datos):
    if not datos:
        print("No hay gastos para eliminar.")
        return
    try:
        id_buscar = int(input("ID del gasto a eliminar: ").strip())
    except:
        print("ID inválido.")
        return
    for i, g in enumerate(datos):
        if g.get("id") == id_buscar:
            if input(f"Querés eliminar '{g.get('descripcion')}'? (s/n): ").lower() == 's':
                datos.pop(i)
                print("Gasto eliminado.")
            else:
                print("Operación cancelada.")
            return
    print("No se encontró un gasto con ese ID.")


def calcular_estadisticas(datos):
    montos = []
    for g in datos:
        try:
            montos.append(float(g.get("monto", 0)))
        except:
            pass
    total = sum(montos)
    promedio = total / len(montos) if montos else 0.0
    mayor = max(montos) if montos else 0.0
    menor = min(montos) if montos else 0.0
    suma_cat = defaultdict(float)
    for g in datos:
        suma_cat[g.get("categoria", "Otros")] += float(g.get("monto", 0))
    porc_cat = {cat: (m/total*100 if total else 0.0) for cat, m in suma_cat.items()}
    cat_may = max(suma_cat, key=suma_cat.get) if suma_cat else None
    return {"total": total, "promedio": promedio, "mayor": mayor, "menor": menor, "por_categoria": porc_cat, "categoria_mayor": cat_may}


def ver_estadisticas(datos):
    stats = calcular_estadisticas(datos)
    print(f"Total gastado: {stats['total']:.2f}")
    print(f"Promedio:       {stats['promedio']:.2f}")
    print(f"Gasto máximo:   {stats['mayor']:.2f}")
    print(f"Gasto mínimo:   {stats['menor']:.2f}\n")
    print("--- Por categoría ---")
    print(f"{'Categoría':<12} {'% Gasto':>8}")
    for cat, pct in stats['por_categoria'].items():
        print(f"{cat:<12} {pct:8.2f}%")
    if stats.get('categoria_mayor'):
        print(f"\nCategoría con mayor gasto: {stats['categoria_mayor']}")


def exportar_a_txt(datos):
    ahora = datetime.now()
    fecha_display = ahora.strftime("%d/%m/%Y")
    fecha_file    = ahora.strftime("%d-%m-%Y_%H-%M-%S")
    nombre_archivo = f"gastos_exportados_{fecha_file}.txt"

    stats = calcular_estadisticas(datos)
    contenido = {
        "titulo": "Listado de gastos",
        "estadisticas": {
            "total": round(stats["total"], 2),
            "promedio": round(stats["promedio"], 2),
            "mayor": round(stats["mayor"], 2),
            "menor": round(stats["menor"], 2),
            "por_categoria": {cat: round(pct, 2) for cat, pct in stats["por_categoria"].items()},
            "categoria_con_mayor_gasto": stats.get('categoria_mayor'),
            "fecha_exportacion": fecha_display
        },
        "datos": datos
    }
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(json.dumps(contenido, indent=4, ensure_ascii=False))
    print(f"Gastos exportados a {nombre_archivo}")


def exportar_a_pdf(datos):
    ahora = datetime.now()
    fecha_display = ahora.strftime("%d/%m/%Y")
    fecha_file = ahora.strftime("%d-%m-%Y_%H-%M-%S")
    nombre_archivo = f"gastos_exportados_{fecha_file}.pdf"

    stats = calcular_estadisticas(datos)
    total = stats["total"]

    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Listado de gastos")

    c.setFont("Helvetica-Bold", 12)
    y = height - 80
    c.drawString(50, y, "ID")
    c.drawString(100, y, "Descripción")
    c.drawString(300, y, "Monto")
    c.drawString(400, y, "Fecha")
    y -= 20

    c.setFont("Helvetica", 10)
    for idx, g in enumerate(datos, start=1):
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, str(g.get('id', idx)))
        c.drawString(100, y, g.get('descripcion','')[:30])
        c.drawString(300, y, f"{float(g.get('monto',0)):.2f}")
        c.drawString(400, y, g.get('fecha',''))
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: {total:.2f} - Fecha de exportación: {fecha_display}")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Estadísticas Detalladas")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Promedio: {stats['promedio']:.2f}")
    y -= 20
    c.drawString(50, y, f"Gasto máximo: {stats['mayor']:.2f}")
    y -= 20
    c.drawString(50, y, f"Gasto mínimo: {stats['menor']:.2f}")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Distribución por categoría")
    y -= 20
    c.setFont("Helvetica", 12)
    for cat, pct in stats['por_categoria'].items():
        c.drawString(50, y, f"{cat}: {pct:.2f}%")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Categoría con mayor gasto: {stats.get('categoria_mayor')}")

    c.save()
    print(f"Gastos exportados a {nombre_archivo}")


def menu():
    datos = cargar_datos()
    while True:
        print("\n--- Menú de Gastos ---")
        print("1. Ver lista de todos los gastos")
        print("2. Registrar un nuevo gasto")
        print("3. Modificar un gasto existente")
        print("4. Eliminar un gasto")
        print("5. Ver estadísticas")
        print("6. Eliminar todos los gastos")
        print("7. Exportar (TXT o PDF)")
        print("8. Salir y guardar")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1": ver_gastos(datos)
        elif opcion == "2": registrar_gasto(datos)
        elif opcion == "3": modificar_gasto(datos)
        elif opcion == "4": eliminar_gasto(datos)
        elif opcion == "5": ver_estadisticas(datos)
        elif opcion == "6": eliminar_todos(datos)
        elif opcion == "7":
            print("1. Exportar a TXT")
            print("2. Exportar a PDF")
            fmt = input("Elegí formato: ").strip()
            if fmt == "1": exportar_a_txt(datos)
            elif fmt == "2": exportar_a_pdf(datos)
            else: print("Formato no válido.")
        elif opcion == "8":
            guardar_datos(datos)
            print("Datos guardados. Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
