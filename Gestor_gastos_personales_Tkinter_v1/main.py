import customtkinter as ctk
from gestor_gastos_app import GestorGastosApp

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = GestorGastosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()