import os
import json
from tkinter import messagebox
import customtkinter as ctk

from frames.ver_gastos import VerGastosFrame
from frames.registrar import RegistrarFrame
from frames.modificar import ModificarFrame
from frames.eliminar import EliminarFrame
from frames.ver_estadistica import EstadisticasFrame
from frames.exportar import ExportarFrame
from constantes import CATEGORIAS_DISPONIBLES

class GestorGastosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Gastos")
        width, height = 900, 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(800, 500)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.datos = self.cargar_datos()

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.menu_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.menu_frame, text="").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(self.menu_frame, text="Guardar y Salir", command=self.salir, cursor="hand2").grid(row=0, column=1, sticky="e", padx=5)

        self.content_container = ctk.CTkFrame(self.main_frame)
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.content_container.grid_columnconfigure(0, weight=4)
        self.content_container.grid_columnconfigure(1, weight=0, minsize=480)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.tree_frame = VerGastosFrame(self.content_container, self)
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.opciones_scroll = ctk.CTkScrollableFrame(self.content_container, width=480)
        self.opciones_scroll.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.opciones_scroll.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F, titulo in [
            (RegistrarFrame, "Registrar gasto"),
            (ModificarFrame, "Modificar gasto"),
            (EliminarFrame, "Eliminar gasto"),
            (EstadisticasFrame, "Estadísticas"),
            (ExportarFrame, "Exportar datos"),
        ]:
            card = ctk.CTkFrame(self.opciones_scroll, corner_radius=12, border_width=2, border_color="#444")
            card.grid_columnconfigure(0, weight=1)
            card.pack(fill="x", padx=10, pady=10, anchor="n")
            ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
            frame = F(card, self)
            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
            if hasattr(frame, "actualizar"):
                frame.actualizar()

    def cargar_datos(self):
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

    def guardar_datos(self):
        with open("gastos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.datos, archivo, indent=4, ensure_ascii=False)

    def salir(self):
        self.guardar_datos()
        self.root.destroy()

    def actualizar_todo(self):
        if hasattr(self, "tree_frame"):
            self.tree_frame.actualizar()
        if EstadisticasFrame in self.frames:
            self.frames[EstadisticasFrame].actualizar()