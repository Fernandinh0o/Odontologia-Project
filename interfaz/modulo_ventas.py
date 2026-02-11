import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_ventas import (
    obtener_productos_disponibles,
    obtener_ventas,
    registrar_venta,
)

FONDO_VENTANA = "#F5EAF1"
FONDO_PANEL = "#FDF7FA"
FONDO_TARJETA = "#E8F6FA"
FONDO_TARJETA_SECUNDARIA = "#F7E9F2"
ACENTO_PRIMARIO = "#8C78D9"
ACENTO_SECUNDARIO = "#5EC9D8"
ACENTO_ACCION = "#FF9FB4"
TEXTO_PRINCIPAL = "#493B61"
TEXTO_SECUNDARIO = "#766B8A"
BLANCO = "#FFFFFF"


def _configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Ventas.Treeview",
        background=BLANCO,
        foreground=TEXTO_PRINCIPAL,
        fieldbackground=BLANCO,
        borderwidth=0,
        rowheight=30,
        font=("Arial", 10),
    )
    style.configure(
        "Ventas.Treeview.Heading",
        background=ACENTO_PRIMARIO,
        foreground=BLANCO,
        font=("Arial", 10, "bold"),
        relief="flat",
    )
    style.map(
        "Ventas.Treeview",
        background=[("selected", "#D9F4F8")],
        foreground=[("selected", TEXTO_PRINCIPAL)],
    )

    style.configure(
        "Ventas.TCombobox",
        fieldbackground=BLANCO,
        background=BLANCO,
        foreground=TEXTO_PRINCIPAL,
        arrowsize=14,
        bordercolor="#E0D7E8",
        relief="flat",
        padding=5,
    )


def _crear_tarjeta(parent, x, y, w, h, color):
    tarjeta = tk.Frame(parent, bg=color, highlightthickness=0)
    tarjeta.place(x=x, y=y, width=w, height=h)
    return tarjeta


def _titulo(parent, text, x, y):
    tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=TEXTO_PRINCIPAL,
        font=("Arial", 11, "bold"),
    ).place(x=x, y=y)


def _boton(parent, text, command, x, y, w=160, h=38, color=ACENTO_PRIMARIO):
    tk.Button(
        parent,
        text=text,
        bg=color,
        fg=BLANCO,
        activebackground="#7A66C9",
        activeforeground=BLANCO,
        bd=0,
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=command,
    ).place(x=x, y=y, width=w, height=h)


def _input(parent, x, y, width=260):
    entrada = tk.Entry(
        parent,
        font=("Arial", 11),
        bd=0,
        relief="flat",
        fg=TEXTO_PRINCIPAL,
        bg=BLANCO,
        insertbackground=TEXTO_PRINCIPAL,
    )
    entrada.place(x=x, y=y, width=width, height=34)
    return entrada


def mostrar_modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Módulo de Ventas")
    ventana.geometry("1040x620")
    ventana.configure(bg=FONDO_VENTANA)
    ventana.resizable(False, False)

    _configurar_estilos()

    panel = tk.Frame(ventana, bg=FONDO_PANEL)
    panel.place(x=20, y=20, width=1000, height=580)

    tk.Label(
        panel,
        text="Facturación de Ventas",
        bg=FONDO_PANEL,
        fg=TEXTO_PRINCIPAL,
        font=("Arial", 22, "bold"),
    ).place(x=28, y=20)

    tk.Label(
        panel,
        text="Interfaz de facturación rápida con estética suave",
        bg=FONDO_PANEL,
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 10),
    ).place(x=30, y=55)

    frame_form = _crear_tarjeta(panel, x=28, y=92, w=430, h=218, color=FONDO_TARJETA_SECUNDARIA)
    _titulo(frame_form, "Datos de la venta", 16, 14)

    tk.Label(
        frame_form,
        text="Cliente",
        bg=FONDO_TARJETA_SECUNDARIA,
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 10, "bold"),
    ).place(x=18, y=56)
    tk.Label(
        frame_form,
        text="Producto",
        bg=FONDO_TARJETA_SECUNDARIA,
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 10, "bold"),
    ).place(x=18, y=104)
    tk.Label(
        frame_form,
        text="Cantidad",
        bg=FONDO_TARJETA_SECUNDARIA,
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 10, "bold"),
    ).place(x=18, y=152)

    entry_cliente = _input(frame_form, x=110, y=50, width=300)

    combo_producto = ttk.Combobox(frame_form, state="readonly", style="Ventas.TCombobox")
    combo_producto.place(x=110, y=98, width=300, height=34)

    entry_cantidad = _input(frame_form, x=110, y=146, width=300)

    frame_historial = _crear_tarjeta(panel, x=474, y=92, w=496, h=218, color=FONDO_TARJETA)
    _titulo(frame_historial, "Ventas registradas", 16, 14)

    columnas_historial = ("id_venta", "fecha", "cliente", "total")
    tabla_historial = ttk.Treeview(
        frame_historial,
        columns=columnas_historial,
        show="headings",
        style="Ventas.Treeview",
        height=6,
    )
    tabla_historial.heading("id_venta", text="Factura")
    tabla_historial.heading("fecha", text="Fecha")
    tabla_historial.heading("cliente", text="Cliente")
    tabla_historial.heading("total", text="Total")
    tabla_historial.column("id_venta", width=75, anchor="center")
    tabla_historial.column("fecha", width=160, anchor="center")
    tabla_historial.column("cliente", width=170, anchor="w")
    tabla_historial.column("total", width=85, anchor="e")
    tabla_historial.place(x=16, y=48, width=464, height=154)

    frame_detalle = _crear_tarjeta(panel, x=28, y=328, w=942, h=194, color="#ECFAFD")
    _titulo(frame_detalle, "Detalle de la factura", 16, 12)

    columnas_detalle = ("id", "nombre", "cantidad", "precio", "subtotal")
    tabla_detalle = ttk.Treeview(
        frame_detalle,
        columns=columnas_detalle,
        show="headings",
        style="Ventas.Treeview",
        height=5,
    )
    tabla_detalle.heading("id", text="ID")
    tabla_detalle.heading("nombre", text="Producto")
    tabla_detalle.heading("cantidad", text="Cantidad")
    tabla_detalle.heading("precio", text="P. Unitario")
    tabla_detalle.heading("subtotal", text="Subtotal")

    tabla_detalle.column("id", width=60, anchor="center")
    tabla_detalle.column("nombre", width=350, anchor="w")
    tabla_detalle.column("cantidad", width=120, anchor="center")
    tabla_detalle.column("precio", width=150, anchor="e")
    tabla_detalle.column("subtotal", width=150, anchor="e")
    tabla_detalle.place(x=16, y=46, width=904, height=132)

    total_var = tk.StringVar(value="₡0.00")
    tk.Label(
        panel,
        text="Total actual:",
        bg=FONDO_PANEL,
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 10, "bold"),
    ).place(x=736, y=534)
    tk.Label(
        panel,
        textvariable=total_var,
        bg=FONDO_PANEL,
        fg=ACENTO_PRIMARIO,
        font=("Arial", 14, "bold"),
    ).place(x=824, y=530)

    productos_mapa = {}
    lineas = []

    def actualizar_total():
        total = sum(linea["subtotal"] for linea in lineas)
        total_var.set(f"₡{total:.2f}")

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

        actualizar_total()

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

    _boton(panel, "Agregar producto", agregar_producto, x=30, y=532, w=170, color=ACENTO_SECUNDARIO)
    _boton(panel, "Facturar venta", facturar_venta, x=214, y=532, w=170, color=ACENTO_PRIMARIO)
    _boton(
        panel,
        "Refrescar",
        lambda: (cargar_productos(), cargar_historial()),
        x=398,
        y=532,
        w=150,
        color="#7DB7E5",
    )
    _boton(panel, "Cerrar", ventana.destroy, x=562, y=532, w=150, color=ACENTO_ACCION)

    tk.Button(
        panel,
        text="✕",
        bg=ACENTO_PRIMARIO,
        fg=BLANCO,
        activebackground="#7A66C9",
        activeforeground=BLANCO,
        bd=0,
        font=("Arial", 11, "bold"),
        cursor="hand2",
        command=ventana.destroy,
    ).place(x=950, y=16, width=32, height=28)

    cargar_productos()
    cargar_historial()

