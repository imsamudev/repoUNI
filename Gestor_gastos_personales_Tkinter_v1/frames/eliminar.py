import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

class EliminarFrame(ctk.CTkFrame):
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
        ctk.CTkButton(buscar_frame, text="Eliminar", command=self.eliminar_gasto).pack(side='left')
        ctk.CTkButton(self.inner_frame, text="Eliminar Todos los Gastos", command=self.eliminar_todos, fg_color="red", hover_color="darkred").pack(pady=10)

    def eliminar_gasto(self):
        try:
            id_buscar = int(self.entry_id.get())
        except:
            messagebox.showerror("Error", "ID inválido")
            return
        for i, g in enumerate(self.controller.datos):
            if g.get("id") == id_buscar:
                if messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar el gasto '{g.get('descripcion')}'?"):
                    self.controller.datos.pop(i)
                    messagebox.showinfo("Éxito", "Gasto eliminado")
                    self.entry_id.delete(0, tk.END)
                    if hasattr(self.controller, 'tree_frame'):
                        self.controller.tree_frame.actualizar()
                return
        messagebox.showerror("Error", "No se encontró un gasto con ese ID")

    def eliminar_todos(self):
        if messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar TODOS los gastos?"):
            self.controller.datos.clear()
            messagebox.showinfo("Éxito", "Todos los gastos han sido eliminados")
            if hasattr(self.controller, 'tree_frame'):
                self.controller.tree_frame.actualizar()
    def actualizar(self):
        self.entry_id.delete(0, tk.END)