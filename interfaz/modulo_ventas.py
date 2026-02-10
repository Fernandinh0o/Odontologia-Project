import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_ventas import (
    obtener_productos_disponibles,
    obtener_ventas,
    registrar_venta,
)

ROSA_SUAVE = "#E8D4E0"
TEXTO_CLARO = "#FFFFFF"
MORADO = "#4B2A6A"
TEXTO_GRIS = "#5B5B5B"


def _boton(panel, text, command, x, y, w=160, h=35):
    tk.Button(
        panel,
        text=text,
        bg=MORADO,
        fg=TEXTO_CLARO,
        bd=0,
        font=("Arial", 10, "bold"),
        command=command,
    ).place(x=x, y=y, width=w, height=h)


def mostrar_modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Módulo de Ventas")
    ventana.geometry("980x560")
    ventana.configure(bg=ROSA_SUAVE)
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Facturación de Ventas",
        bg=ROSA_SUAVE,
        fg=MORADO,
        font=("Arial", 16, "bold"),
    ).place(x=30, y=20)

    frame_form = tk.Frame(ventana, bg=ROSA_SUAVE)
    frame_form.place(x=30, y=70, width=420, height=220)

    tk.Label(frame_form, text="Cliente", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    tk.Label(frame_form, text="Producto", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
    tk.Label(frame_form, text="Cantidad", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=8)

    entry_cliente = tk.Entry(frame_form, font=("Arial", 11))
    entry_cliente.grid(row=0, column=1, padx=10)

    combo_producto = ttk.Combobox(frame_form, state="readonly", width=30)
    combo_producto.grid(row=1, column=1, padx=10)

    entry_cantidad = tk.Entry(frame_form, font=("Arial", 11))
    entry_cantidad.grid(row=2, column=1, padx=10)

    frame_detalle = tk.Frame(ventana, bg=ROSA_SUAVE)
    frame_detalle.place(x=30, y=300, width=920, height=180)

    columnas_detalle = ("id", "nombre", "cantidad", "precio", "subtotal")
    tabla_detalle = ttk.Treeview(frame_detalle, columns=columnas_detalle, show="headings", height=7)
    tabla_detalle.heading("id", text="ID")
    tabla_detalle.heading("nombre", text="Producto")
    tabla_detalle.heading("cantidad", text="Cantidad")
    tabla_detalle.heading("precio", text="P. Unitario")
    tabla_detalle.heading("subtotal", text="Subtotal")

    tabla_detalle.column("id", width=60, anchor="center")
    tabla_detalle.column("nombre", width=260, anchor="w")
    tabla_detalle.column("cantidad", width=100, anchor="center")
    tabla_detalle.column("precio", width=130, anchor="center")
    tabla_detalle.column("subtotal", width=130, anchor="center")
    tabla_detalle.pack(side="left", fill="both", expand=True)

    scroll_detalle = ttk.Scrollbar(frame_detalle, orient="vertical", command=tabla_detalle.yview)
    tabla_detalle.configure(yscrollcommand=scroll_detalle.set)
    scroll_detalle.pack(side="right", fill="y")

    frame_historial = tk.Frame(ventana, bg=ROSA_SUAVE)
    frame_historial.place(x=470, y=70, width=480, height=220)

    tk.Label(frame_historial, text="Ventas registradas", bg=ROSA_SUAVE, fg=MORADO,
             font=("Arial", 11, "bold")).pack(anchor="w")

    columnas_historial = ("id_venta", "fecha", "cliente", "total")
    tabla_historial = ttk.Treeview(frame_historial, columns=columnas_historial, show="headings", height=8)
    tabla_historial.heading("id_venta", text="Factura")
    tabla_historial.heading("fecha", text="Fecha")
    tabla_historial.heading("cliente", text="Cliente")
    tabla_historial.heading("total", text="Total")
    tabla_historial.column("id_venta", width=70, anchor="center")
    tabla_historial.column("fecha", width=150, anchor="center")
    tabla_historial.column("cliente", width=150, anchor="w")
    tabla_historial.column("total", width=90, anchor="center")
    tabla_historial.pack(fill="both", expand=True)

    productos_mapa = {}
    lineas = []

    def cargar_productos():
        nonlocal productos_mapa
        productos_mapa = {}
        opciones = []
        try:
            for prod in obtener_productos_disponibles():
                productos_mapa[prod[0]] = {
                    "id_producto": prod[0],
                    "nombre": prod[1],
                    "stock": prod[2],
                    "precio_unitario": float(prod[3]),
                }
                opciones.append(f"{prod[0]} - {prod[1]} (Stock: {prod[2]})")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        combo_producto["values"] = opciones
        if opciones:
            combo_producto.current(0)

    def cargar_historial():
        for item in tabla_historial.get_children():
            tabla_historial.delete(item)

        try:
            ventas = obtener_ventas()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        for venta in ventas:
            tabla_historial.insert(
                "",
                "end",
                values=(
                    venta[0],
                    venta[1],
                    venta[2],
                    f"₡{float(venta[6]):.2f}",
                ),
            )

    def refrescar_detalle():
        for item in tabla_detalle.get_children():
            tabla_detalle.delete(item)

        for linea in lineas:
            tabla_detalle.insert(
                "",
                "end",
                values=(
                    linea["id_producto"],
                    linea["nombre"],
                    linea["cantidad"],
                    f"₡{linea['precio_unitario']:.2f}",
                    f"₡{linea['subtotal']:.2f}",
                ),
            )

    def agregar_producto():
        seleccion = combo_producto.get().strip()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return

        try:
            id_producto = int(seleccion.split("-")[0].strip())
            cantidad = int(entry_cantidad.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        if id_producto not in productos_mapa:
            messagebox.showerror("Error", "Producto no disponible")
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a cero")
            return

        producto = productos_mapa[id_producto]
        if cantidad > producto["stock"]:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
            return

        subtotal = round(producto["precio_unitario"] * cantidad, 2)
        lineas.append(
            {
                "id_producto": producto["id_producto"],
                "nombre": producto["nombre"],
                "cantidad": cantidad,
                "precio_unitario": producto["precio_unitario"],
                "subtotal": subtotal,
            }
        )
        refrescar_detalle()
        entry_cantidad.delete(0, tk.END)

    def facturar_venta():
        cliente = entry_cliente.get().strip()
        if not cliente:
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return

        if not lineas:
            messagebox.showerror("Error", "Debe agregar productos al detalle")
            return

        try:
            id_venta, ruta_factura = registrar_venta(
                cliente=cliente,
                usuario="Secretaria",
                lineas=lineas,
            )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo(
            "Venta registrada",
            f"Factura #{id_venta} generada correctamente.\nArchivo: {ruta_factura}",
        )

        entry_cliente.delete(0, tk.END)
        lineas.clear()
        refrescar_detalle()
        cargar_productos()
        cargar_historial()

    _boton(ventana, "Agregar Producto", agregar_producto, x=30, y=500, w=180)
    _boton(ventana, "Facturar Venta", facturar_venta, x=230, y=500, w=180)
    _boton(ventana, "Refrescar", lambda: (cargar_productos(), cargar_historial()), x=430, y=500, w=150)
    _boton(ventana, "Cerrar", ventana.destroy, x=600, y=500, w=150)

    tk.Button(
        ventana,
        text="X",
        bg=MORADO,
        fg=TEXTO_CLARO,
        bd=0,
        font=("Arial", 10, "bold"),
        command=ventana.destroy,
    ).place(x=930, y=15, width=35, height=28)

    cargar_productos()
    cargar_historial()
