import tkinter as tk
from tkinter import ttk
from datetime import date
import customtkinter as ctk

class VerGastosFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self._configurar_treeview_style()
        self._last_appearance_mode = ctk.get_appearance_mode()
        self.after(300, self._verificar_tema)

        self.tree = ttk.Treeview(self, 
            columns=("ID", "Descripción", "Categoría", "Monto", "Fecha"), 
            show='headings',
            style="Treeview")
        for col, w in [("ID",50),("Descripción",400),("Categoría",150),("Monto",100),("Fecha",150)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.lbl_total = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_total.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

    def _verificar_tema(self):
        modo_actual = ctk.get_appearance_mode()
        if modo_actual != self._last_appearance_mode:
            self._configurar_treeview_style()
            self._last_appearance_mode = modo_actual
        self.after(300, self._verificar_tema)

    def _configurar_treeview_style(self):
        if ctk.get_appearance_mode() == "Dark":
            bg_color = "#2a2d2e"
            fg_color = "white"
            selected_color = "#22559b"
            header_bg = "#23272a"  
            header_fg = "white"
        else:
            bg_color = "#f7f7f7"
            fg_color = "black"
            selected_color = "#0078d7"
            header_bg = "#e0e0e0"
            header_fg = "black"
        self.style.theme_use('default')
        self.style.configure("Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=bg_color,
            rowheight=25)
        self.style.map('Treeview',
            background=[('selected', selected_color)],
            foreground=[('selected', 'white')])
        self.style.configure("Treeview.Heading",
            background=header_bg,
            foreground=header_fg,
            font=('Segoe UI', 11, 'bold'),
            relief="flat")
        self.style.map("Treeview.Heading",
            background=[('active', header_bg)],
            foreground=[('active', header_fg)])

    def actualizar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0.0
        for g in self.controller.datos:
            id_val = g.get('id', 0)
            desc = g.get('descripcion','')
            cat = g.get('categoria','')
            try:
                monto = float(g.get('monto',0))
            except:
                monto = 0.0
            fecha = g.get('fecha','')
            total += monto
            self.tree.insert('', 'end', values=(id_val, desc, cat, f"{monto:.2f}", fecha))
        self.lbl_total.configure(text=f"TOTAL: {total:.2f}    Fecha: {date.today().strftime('%d/%m/%Y')}")