import os
import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_prod = os.path.join(base_dir, "datos", "productos.json")
    ruta_usrs = os.path.join(base_dir, "datos", "usuarios.json")
    ruta_vnts = os.path.join(base_dir, "datos", "ventas.json")

    servicio = RestauranteServicio(
        ruta_productos=ruta_prod, 
        ruta_usuarios=ruta_usrs,
        ruta_ventas=ruta_vnts
    )

    root = tk.Tk()

    def abrir_login():
        LoginView(root, servicio=servicio, on_login_success=abrir_main_view)

    def abrir_main_view(usuario_autenticado):
        MainView(root, servicio=servicio, usuario_actual=usuario_autenticado, on_logout=abrir_login)

    abrir_login()
    root.mainloop()

if __name__ == "__main__":
    main()