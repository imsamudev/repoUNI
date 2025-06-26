import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from constantes import CATEGORIAS_DISPONIBLES


class RegistrarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        form_frame = ctk.CTkFrame(self.inner_frame)
        form_frame.pack(padx=10, pady=5)
        ctk.CTkLabel(form_frame, text="Descripción:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_desc = ctk.CTkEntry(form_frame, width=250)
        self.entry_desc.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(form_frame, text="Monto:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_monto = ctk.CTkEntry(form_frame, width=250)
        self.entry_monto.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(form_frame, text="Fecha (DD-MM-YYYY):").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_fecha = ctk.CTkEntry(form_frame, width=250)
        self.entry_fecha.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(form_frame, text="Categoría:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.categoria_var = ctk.StringVar(value=CATEGORIAS_DISPONIBLES[0])
        self.categoria_menu = ctk.CTkOptionMenu(form_frame, values=CATEGORIAS_DISPONIBLES, variable=self.categoria_var, width=250)
        self.categoria_menu.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkButton(self.inner_frame, text="Guardar", command=self.guardar_gasto).pack(pady=10)
    def guardar_gasto(self):
        descripcion = self.entry_desc.get().strip()
        try:
            monto = float(self.entry_monto.get().strip())
        except:
            messagebox.showerror("Error", "Monto inválido. Ingresá un número.")
            return
        fecha = self.entry_fecha.get().strip()
        categoria = self.categoria_var.get()
        nuevo_id = max([g.get("id",0) for g in self.controller.datos], default=0) + 1
        self.controller.datos.append({
            "id": nuevo_id,
            "descripcion": descripcion,
            "categoria": categoria,
            "monto": monto,
            "fecha": fecha
        })
        messagebox.showinfo("Éxito", "Gasto registrado.")
        self.limpiar_campos()
        self.controller.actualizar_todo()

    def limpiar_campos(self):
        self.entry_desc.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.categoria_var.set(CATEGORIAS_DISPONIBLES[0])

    def actualizar(self):
        self.limpiar_campos()