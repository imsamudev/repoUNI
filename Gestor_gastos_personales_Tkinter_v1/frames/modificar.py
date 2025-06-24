import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from constantes import CATEGORIAS_DISPONIBLES

class ModificarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        buscar_frame = ctk.CTkFrame(self.inner_frame)
        buscar_frame.pack(pady=5)
        ctk.CTkLabel(buscar_frame, text="ID del gasto:").pack(side='left')
        self.entry_id = ctk.CTkEntry(buscar_frame, width=100)
        self.entry_id.pack(side='left', padx=5)
        ctk.CTkButton(buscar_frame, text="Buscar", command=self.buscar_gasto).pack(side='left')
        self.form_frame = ctk.CTkFrame(self.inner_frame)
        self.form_frame.pack(pady=10)
        ctk.CTkLabel(self.form_frame, text="Descripción:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_desc = ctk.CTkEntry(self.form_frame, width=300)
        self.entry_desc.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(self.form_frame, text="Monto:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_monto = ctk.CTkEntry(self.form_frame, width=300)
        self.entry_monto.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(self.form_frame, text="Fecha:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_fecha = ctk.CTkEntry(self.form_frame, width=300)
        self.entry_fecha.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        ctk.CTkLabel(self.form_frame, text="Categoría:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.categoria_var = ctk.StringVar(value=CATEGORIAS_DISPONIBLES[0])
        self.categoria_menu = ctk.CTkOptionMenu(self.form_frame, values=CATEGORIAS_DISPONIBLES, variable=self.categoria_var)
        self.categoria_menu.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.btn_guardar = ctk.CTkButton(self.form_frame, text="Guardar Cambios", command=self.guardar_modificacion)
        self.btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)
        self.gasto_actual = None
        self.form_frame.pack_forget()

    def buscar_gasto(self):
        try:
            id_buscar = int(self.entry_id.get())
        except:
            messagebox.showerror("Error", "ID inválido")
            return
        for g in self.controller.datos:
            if g.get("id") == id_buscar:
                self.gasto_actual = g
                self.mostrar_datos_gasto()
                self.form_frame.pack(pady=20)
                return
        messagebox.showerror("Error", "No se encontró un gasto con ese ID")
        self.form_frame.pack_forget()

    def mostrar_datos_gasto(self):
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, self.gasto_actual.get("descripcion", ""))
        self.entry_monto.delete(0, tk.END)
        self.entry_monto.insert(0, str(self.gasto_actual.get("monto", "")))
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, self.gasto_actual.get("fecha", ""))
        self.categoria_var.set(self.gasto_actual.get("categoria", CATEGORIAS_DISPONIBLES[0]))

    def guardar_modificacion(self):
        if not self.gasto_actual:
            return
        try:
            monto = float(self.entry_monto.get().strip())
        except:
            messagebox.showerror("Error", "Monto inválido")
            return
        self.gasto_actual.update({
            "descripcion": self.entry_desc.get().strip(),
            "monto": monto,
            "fecha": self.entry_fecha.get().strip(),
            "categoria": self.categoria_var.get()
        })
        messagebox.showinfo("Éxito", "Gasto modificado correctamente")
        self.entry_id.delete(0, tk.END)
        self.form_frame.pack_forget()
        if hasattr(self.controller, 'tree_frame'):
            self.controller.tree_frame.actualizar()

    def actualizar(self):
        self.entry_id.delete(0, tk.END)
        self.form_frame.pack_forget()
        if hasattr(self.controller, 'tree_frame'):
            self.controller.tree_frame.actualizar()