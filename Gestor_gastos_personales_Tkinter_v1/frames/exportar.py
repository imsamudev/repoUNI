import os
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
import subprocess
import sys

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Docs")

class ExportarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        if not os.path.exists(DOCS_DIR):
            os.makedirs(DOCS_DIR)

        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkButton(self.inner_frame, text="Exportar a TXT", command=lambda: self.exportar("txt")).pack(pady=5)
        ctk.CTkButton(self.inner_frame, text="Exportar a PDF", command=lambda: self.exportar("pdf")).pack(pady=5)
        ctk.CTkLabel(
            self.inner_frame,
            text="Doble click para visualizar",
            font=ctk.CTkFont(size=14, slant="italic")
        ).pack(pady=(5, 0))

        tabla_frame = ctk.CTkFrame(self.inner_frame)
        tabla_frame.pack(fill="x", padx=5, pady=5, expand=False)

        columns = ("nombre", "tipo")
        self.tree = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("tipo", text="Tipo")

        self.tree.column("nombre", width=320, anchor="center")
        self.tree.column("tipo", width=120, anchor="center")

        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.actualizar()

        botones_frame = ctk.CTkFrame(self.inner_frame)
        botones_frame.pack(fill="x", padx=5, pady=(0, 5))

        ctk.CTkButton(
            botones_frame, text="Eliminar seleccionado", command=self.eliminar_seleccionado
        ).pack(side="left", padx=5, pady=5, expand=True, fill="x")

        ctk.CTkButton(
            botones_frame, text="Eliminar todos", command=self.eliminar_todos
        ).pack(side="left", padx=5, pady=5, expand=True, fill="x")

    def exportar(self, formato):
        if formato == "txt":
            self.exportar_a_txt()
        else:
            self.exportar_a_pdf()
        self.actualizar()

    def exportar_a_txt(self):
        ahora = datetime.now()
        fecha_display = ahora.strftime("%d/%m/%Y")
        fecha_file = ahora.strftime("%d-%m-%Y_%H-%M-%S")
        nombre_archivo = f"gastos_exportados_{fecha_file}.txt"
        ruta = os.path.join(DOCS_DIR, nombre_archivo)
        stats = self.controller.frames[list(self.controller.frames.keys())[3]].calcular_estadisticas()
        contenido = {
            "titulo": "Listado de gastos",
            "estadisticas": {
                "total": round(stats["total"], 2),
                "promedio": round(stats["promedio"], 2),
                "mayor": round(stats["mayor"], 2),
                "menor": round(stats["menor"], 2),
                "por_categoria": {cat:round(pct,2) for cat,pct in stats["por_categoria"].items()},
                "categoria_con_mayor_gasto": stats.get('categoria_mayor'),
                "fecha_exportacion": fecha_display
            },
            "datos": self.controller.datos
        }
        with open(ruta, "w", encoding="utf-8") as archivo:
            import json
            archivo.write(json.dumps(contenido, indent=4, ensure_ascii=False))
        messagebox.showinfo("Exportación", f"Gastos exportados a {ruta}")

    def exportar_a_pdf(self):
        ahora = datetime.now()
        fecha_display = ahora.strftime("%d/%m/%Y")
        fecha_file = ahora.strftime("%d-%m-%Y_%H-%M-%S")
        nombre_archivo = f"gastos_exportados_{fecha_file}.pdf"
        ruta = os.path.join(DOCS_DIR, nombre_archivo)
        stats = self.controller.frames[list(self.controller.frames.keys())[3]].calcular_estadisticas()
        total = stats["total"]
        c = canvas.Canvas(ruta, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, "Listado de gastos")
        c.setFont("Helvetica-Bold", 12)
        y = height-80
        for col, x in [("ID",50),("Descripción",100),("Monto",300),("Fecha",400)]:
            c.drawString(x, y, col)
        y -= 20
        c.setFont("Helvetica", 10)
        for idx, g in enumerate(self.controller.datos, 1):
            if y < 100:
                c.showPage()
                y = height-50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, str(g.get('id', idx)))
            c.drawString(100, y, g.get('descripcion', '')[:30])
            c.drawString(300, y, f"{float(g.get('monto', 0)):.2f}")
            c.drawString(400, y, g.get('fecha', ''))
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
        messagebox.showinfo("Exportación", f"Gastos exportados a {ruta}")

    def actualizar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        archivos = sorted(os.listdir(DOCS_DIR), reverse=True)
        for archivo in archivos:
            ruta = os.path.join(DOCS_DIR, archivo)
            if not os.path.isfile(ruta):
                continue
            tipo = archivo.split('.')[-1].upper()
            self.tree.insert("", "end", values=(archivo, tipo))

    def on_tree_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        nombre = self.tree.item(item, "values")[0]
        ruta = os.path.join(DOCS_DIR, nombre)
        self.visualizar_archivo(ruta)

    def visualizar_archivo(self, ruta):
        try:
            if sys.platform.startswith('win'):
                os.startfile(ruta)
            elif sys.platform.startswith('darwin'):
                subprocess.call(('open', ruta))
            else:
                subprocess.call(('xdg-open', ruta))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def eliminar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Eliminar", "Seleccione un archivo para eliminar.")
            return
        nombre = self.tree.item(item[0], "values")[0]
        ruta = os.path.join(DOCS_DIR, nombre)
        if messagebox.askyesno("Eliminar", f"¿Seguro que desea eliminar '{nombre}'?"):
            try:
                os.remove(ruta)
                self.actualizar()
                messagebox.showinfo("Eliminar", f"Archivo '{nombre}' eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el archivo: {e}")

    def eliminar_todos(self):
        archivos = [f for f in os.listdir(DOCS_DIR) if os.path.isfile(os.path.join(DOCS_DIR, f))]
        if not archivos:
            messagebox.showinfo("Eliminar todos", "No hay archivos para eliminar.")
            return
        if messagebox.askyesno("Eliminar todos", "¿Seguro que desea eliminar TODOS los archivos?"):
            errores = []
            for archivo in archivos:
                try:
                    os.remove(os.path.join(DOCS_DIR, archivo))
                except Exception as e:
                    errores.append(archivo)
            self.actualizar()
            if errores:
                messagebox.showerror("Error", f"No se pudieron eliminar: {', '.join(errores)}")
            else:
                messagebox.showinfo("Eliminar todos", "Todos los archivos han sido eliminados.")