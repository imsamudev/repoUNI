import tkinter as tk
import customtkinter as ctk
from collections import defaultdict

class EstadisticasFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.text_stats = ctk.CTkTextbox(self.inner_frame, height=300, width=400)
        self.text_stats.pack(pady=5)

    def calcular_estadisticas(self):
        datos = self.controller.datos
        montos = []
        for g in datos:
            try:
                montos.append(float(g.get("monto", 0)))
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
        return {
            "total": total,
            "promedio": promedio,
            "mayor": mayor,
            "menor": menor,
            "por_categoria": porc_cat,
            "categoria_mayor": cat_may
        }

    def actualizar(self):
        self.text_stats.delete("0.0", tk.END)
        stats = self.calcular_estadisticas()
        info = f"Total gastado: {stats['total']:.2f}\n"
        info += f"Promedio: {stats['promedio']:.2f}\n"
        info += f"Gasto máximo: {stats['mayor']:.2f}\n"
        info += f"Gasto mínimo: {stats['menor']:.2f}\n\n"
        info += "--- Por categoría ---\n"
        for cat, pct in stats['por_categoria'].items():
            info += f"{cat}: {pct:.2f}%\n"
        if stats.get('categoria_mayor'):
            info += f"\nCategoría con mayor gasto: {stats['categoria_mayor']}"
        self.text_stats.insert("0.0", info)