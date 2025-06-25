import tkinter as tk
import customtkinter as ctk
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EstadisticasFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.cards_frame = ctk.CTkFrame(self.inner_frame)
        self.cards_frame.pack(fill="x", pady=5)
        self.card_total = ctk.CTkLabel(self.cards_frame, text="", font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color="#2e86c1", corner_radius=8, text_color="white", width=220, height=50)
        self.card_total.pack(fill="x", pady=5)
        self.card_prom = ctk.CTkLabel(self.cards_frame, text="", font=ctk.CTkFont(size=16, weight="bold"),
                                      fg_color="#27ae60", corner_radius=8, text_color="white", width=220, height=50)
        self.card_prom.pack(fill="x", pady=5)
        self.card_max = ctk.CTkLabel(self.cards_frame, text="", font=ctk.CTkFont(size=16, weight="bold"),
                                     fg_color="#e67e22", corner_radius=8, text_color="white", width=220, height=50)
        self.card_max.pack(fill="x", pady=5)
        self.card_min = ctk.CTkLabel(self.cards_frame, text="", font=ctk.CTkFont(size=16, weight="bold"),
                                     fg_color="#8e44ad", corner_radius=8, text_color="white", width=220, height=50)
        self.card_min.pack(fill="x", pady=5)

        self.grafico_frame = ctk.CTkFrame(self.inner_frame)
        self.grafico_frame.pack(pady=(10, 0), fill="x")
        self.canvas = None

        self.leyenda_frame = ctk.CTkFrame(self.inner_frame)
        self.leyenda_frame.pack(pady=(10, 0), fill="x")

        self.extra_stats = ctk.CTkLabel(self.inner_frame, text="", font=ctk.CTkFont(size=14))
        self.extra_stats.pack(pady=(15, 0), fill="x")

    def calcular_estadisticas(self):
        datos = self.controller.datos
        montos = []
        fechas = defaultdict(float)
        for g in datos:
            try:
                monto = float(g.get("monto", 0))
                montos.append(monto)
                fechas[g.get("fecha", "")] += monto
            except:
                pass
        total = sum(montos)
        promedio = total/len(montos) if montos else 0.0
        mayor = max(montos) if montos else 0.0
        menor = min(montos) if montos else 0.0
        suma_cat = defaultdict(float)
        for g in datos:
            suma_cat[g.get("categoria", "Otros")] += float(g.get("monto", 0))
        porc_cat = {cat:(m/total*100 if total else 0.0) for cat,m in suma_cat.items()}
        cat_may = max(suma_cat, key=suma_cat.get) if suma_cat else None
        dia_may = max(fechas, key=fechas.get) if fechas else None
        return {
            "total": total,
            "promedio": promedio,
            "mayor": mayor,
            "menor": menor,
            "por_categoria": porc_cat,
            "categoria_mayor": cat_may,
            "suma_cat": suma_cat,
            "dia_mayor": dia_may,
            "monto_dia_mayor": fechas[dia_may] if dia_may else 0.0
        }

    def mostrar_grafico_categoria(self, suma_cat):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        categorias = list(suma_cat.keys())
        montos = list(suma_cat.values())
        if not categorias or sum(montos) == 0:
            return
        fig, ax = plt.subplots(figsize=(4, 3))
        wedges, texts, autotexts = ax.pie(montos, labels=None, autopct='%1.1f%%', startangle=90)
        ax.set_title("Distribución por categoría")
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        plt.close(fig)

        for widget in self.leyenda_frame.winfo_children():
            widget.destroy()
        for i, cat in enumerate(categorias):
            color = wedges[i].get_facecolor()
            color_hex = '#%02x%02x%02x' % tuple(int(c*255) for c in color[:3])
            leyenda = ctk.CTkLabel(self.leyenda_frame, text=f"{cat}: ${montos[i]:.2f}", anchor="w",
                                   fg_color=color_hex, text_color="white", corner_radius=6, width=180)
            leyenda.pack(fill="x", padx=2, pady=2)

    def actualizar(self):
        stats = self.calcular_estadisticas()
        self.card_total.configure(text=f"Total\n${stats['total']:.2f}")
        self.card_prom.configure(text=f"Promedio\n${stats['promedio']:.2f}")
        self.card_max.configure(text=f"Máximo\n${stats['mayor']:.2f}")
        self.card_min.configure(text=f"Mínimo\n${stats['menor']:.2f}")

        self.mostrar_grafico_categoria(stats["suma_cat"])

        texto_extra = ""
        if stats.get('categoria_mayor'):
            texto_extra += f"Categoría con mayor gasto: {stats['categoria_mayor']}\n"
        if stats.get('dia_mayor'):
            texto_extra += f"Día con mayor gasto: {stats['dia_mayor']} (${stats['monto_dia_mayor']:.2f})"
        self.extra_stats.configure(text=texto_extra)