import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import json
import os

# Definición de las clases

class Supermercado:
    def __init__(self, nombre: str, direccion: str, telefono: str):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.stock = {}
        self.cargar_stock()

    def cargar_stock(self):
        if os.path.exists('stock.json'):
            with open('stock.json', 'r') as file:
                self.stock = json.load(file)
                # Convertir los productos a sus clases correspondientes
                for nombre, info in self.stock.items():
                    if info['tipo'] == 'alimento':
                        self.stock[nombre] = {
                            'producto': Alimento(nombre, info['precio'], info['fecha_vencimiento']),
                            'cantidad': info['cantidad']
                        }
                    elif info['tipo'] == 'bebida':
                        self.stock[nombre] = {
                            'producto': Bebida(nombre, info['precio'], info['tipo_bebida']),
                            'cantidad': info['cantidad']
                        }

    def guardar_stock(self):
        with open('stock.json', 'w') as file:
            json.dump({
                nombre: {
                    'precio': info['producto'].precio,
                    'cantidad': info['cantidad'],
                    'tipo': 'alimento' if isinstance(info['producto'], Alimento) else 'bebida',
                    'fecha_vencimiento': getattr(info['producto'], 'fecha_vencimiento', None),
                    'tipo_bebida': getattr(info['producto'], 'tipo', None)
                }
                for nombre, info in self.stock.items()
            }, file)

    def agregar_producto_stock(self, producto, cantidad):
        if producto.nombre in self.stock:
            self.stock[producto.nombre]['cantidad'] += cantidad
        else:
            self.stock[producto.nombre] = {'producto': producto, 'cantidad': cantidad}
        self.guardar_stock()  # Guardar después de agregar

    def listar_productos_stock(self):
        return {nombre: {'cantidad': info['cantidad']} for nombre, info in self.stock.items()}

    def actualizar_stock(self, nombre_producto, cantidad):
        if nombre_producto in self.stock:
            self.stock[nombre_producto]['cantidad'] -= cantidad
            if self.stock[nombre_producto]['cantidad'] <= 0:
                del self.stock[nombre_producto]  # Eliminar producto si la cantidad es cero
            self.guardar_stock()  # Guardar después de actualizar
        else:
            messagebox.showwarning("Error", f"El producto {nombre_producto} no está en el stock.")

class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

class Alimento(Producto):
    def __init__(self, nombre: str, precio: float, fecha_vencimiento: str):
        super().__init__(nombre, precio)
        self.fecha_vencimiento = fecha_vencimiento

class Bebida(Producto):
    def __init__(self, nombre: str, precio: float, tipo: str):
        super().__init__(nombre, precio)
        self.tipo = tipo

class Carrito:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto: Producto, cantidad: int):
        if producto.nombre in self.productos:
            self.productos[producto.nombre]['cantidad'] += cantidad
        else:
            self.productos[producto.nombre] = {'producto': producto, 'cantidad': cantidad}

    def total_parcial(self):
        return sum(info['producto'].precio * info['cantidad'] for info in self.productos.values())

    def vaciar(self):
        self.productos.clear()

    def contenido(self):
        return {nombre: {'cantidad': info['cantidad']} for nombre, info in self.productos.items()}

class Cliente:
    def __init__(self, nombre: str, telefono: str):
        self.nombre = nombre
        self.telefono = telefono
        self.carrito = Carrito()

class Caja:
    @staticmethod
    def procesar_compra(cliente: Cliente, supermercado: Supermercado):
        total = cliente.carrito.total_parcial()
        if total > 0:
            for nombre, info in cliente.carrito.contenido().items():
                supermercado.actualizar_stock(nombre, info['cantidad'])  # Actualizar stock
            cliente.carrito.vaciar()  # Vaciar el carrito después de la compra
            return total
        else:
            return 0
        
    

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermercado")

        self.supermercado = Supermercado("Supermercado Ejemplo", "Calle Falsa 123", "123456789")
        self.cliente = Cliente("Cliente Ejemplo", "987654321")

        self.label = tk.Label(root, text="Bienvenido al Supermercado")
        self.label.pack()

        self.btn_abrir = tk.Button(root, text="Abrir Supermercado", command=self.abrir_supermercado, width=20, height=2)
        self.btn_abrir.pack(pady=5)

        self.btn_agregar_producto_stock = tk.Button(root, text="Agregar Producto al Stock", command=self.abrir_ventana_agregar_stock, width=20, height=2)
        self.btn_agregar_producto_stock.pack(pady=5)

        self.btn_agregar_producto_carrito = tk.Button(root, text="Agregar Producto al Carrito", command=self.abrir_ventana_agregar_carrito, width=20, height=2)
        self.btn_agregar_producto_carrito.pack(pady=5)

        self.btn_ver_total = tk.Button(root, text="Ver Total Carrito", command=self.ver_total, width=20, height=2)
        self.btn_ver_total.pack(pady=5)

        self.btn_ver_contenido_carrito = tk.Button(root, text="Ver Contenido Carrito", command=self.ver_contenido_carrito, width=20, height=2)
        self.btn_ver_contenido_carrito.pack(pady=5)

        self.btn_ver_stock_actualizado = tk.Button(root, text="Ver Stock Actualizado", command=self.ver_stock_actualizado, width=20, height=2)
        self.btn_ver_stock_actualizado.pack(pady=5)

        self.btn_realizar_compra = tk.Button(root, text="Realizar Compra", command=self.realizar_compra, width=20, height=2)
        self.btn_realizar_compra.pack(pady=5)

        self.btn_vaciar_carrito = tk.Button(root, text="Vaciar Carrito", command=self.vaciar_carrito, width=20, height=2)
        self.btn_vaciar_carrito.pack(pady=5)

    def abrir_supermercado(self):
        mensaje = f"{self.supermercado.nombre} está abierto."
        messagebox.showinfo("Estado", mensaje)

    def abrir_ventana_agregar_stock(self):
        self.ventana_stock = Toplevel(self.root)
        self.ventana_stock.title("Agregar Producto al Stock")

        tk.Label(self.ventana_stock, text="Nombre del Producto:").pack()
        self.entry_nombre_stock = tk.Entry(self.ventana_stock)
        self.entry_nombre_stock.pack()

        tk.Label(self.ventana_stock, text="Precio del Producto:").pack()
        self.entry_precio_stock = tk.Entry(self.ventana_stock)
        self.entry_precio_stock.pack()

        tk.Label(self.ventana_stock, text="Cantidad:").pack()
        self.entry_cantidad_stock = tk.Entry(self.ventana_stock)
        self.entry_cantidad_stock.pack()

        tk.Label(self.ventana_stock, text="Tipo de Producto (alimento/bebida):").pack()
        self.entry_tipo_stock = tk.Entry(self.ventana_stock)
        self.entry_tipo_stock.pack()

        tk.Button(self.ventana_stock, text="Agregar", command=self.agregar_producto_stock).pack()

    def agregar_producto_stock(self):
        nombre_producto = self.entry_nombre_stock.get()
        precio_producto = float(self.entry_precio_stock.get())
        cantidad_producto = int(self.entry_cantidad_stock.get())
        tipo_producto = self.entry_tipo_stock.get()

        if nombre_producto and precio_producto is not None and cantidad_producto is not None and tipo_producto:
            if tipo_producto.lower() == 'alimento':
                fecha_vencimiento = simpledialog.askstring("Fecha de Vencimiento", "Ingrese la fecha de vencimiento:")
                producto = Alimento(nombre_producto, precio_producto, fecha_vencimiento)
            elif tipo_producto.lower() == 'bebida':
                tipo_bebida = simpledialog.askstring("Tipo de Bebida", "Ingrese el tipo de bebida:")
                producto = Bebida(nombre_producto, precio_producto, tipo_bebida)
            else:
                messagebox.showwarning("Error", "Tipo de producto no válido.")
                return
            
            self.supermercado.agregar_producto_stock(producto, cantidad_producto)
            messagebox.showinfo("Producto Agregado", f"Producto {producto.nombre} agregado al stock con {cantidad_producto} unidades.")
            self.ventana_stock.destroy()

    def abrir_ventana_agregar_carrito(self):
        self.ventana_carrito = Toplevel(self.root)
        self.ventana_carrito.title("Agregar Producto al Carrito")

        tk.Label(self.ventana_carrito, text="Nombre del Producto:").pack()
        self.entry_nombre_carrito = tk.Entry(self.ventana_carrito)
        self.entry_nombre_carrito.pack()

        tk.Label(self.ventana_carrito, text="Cantidad:").pack()
        self.entry_cantidad_carrito = tk.Entry(self.ventana_carrito)
        self.entry_cantidad_carrito.pack()

        tk.Button(self.ventana_carrito, text="Agregar", command=self.agregar_producto_carrito).pack()

    def agregar_producto_carrito(self):
        nombre_producto = self.entry_nombre_carrito.get()
        cantidad_producto = int(self.entry_cantidad_carrito.get())
        
        if nombre_producto in self.supermercado.stock:
            if self.supermercado.stock[nombre_producto]['cantidad'] >= cantidad_producto:
                self.cliente.carrito.agregar_producto(self.supermercado.stock[nombre_producto]['producto'], cantidad_producto)
                self.supermercado.actualizar_stock(nombre_producto, cantidad_producto)  # Actualizar stock
                messagebox.showinfo("Producto Agregado", f"Producto {nombre_producto} agregado al carrito.")
                self.ventana_carrito.destroy()
            else:
                messagebox.showwarning("Cantidad Insuficiente", f"No hay suficientes unidades de {nombre_producto} en stock.")
        else:
            messagebox.showwarning("Producto No Encontrado", f"El producto {nombre_producto} no está en el stock.")

    def ver_total(self):
        total = self.cliente.carrito.total_parcial()
        messagebox.showinfo("Total Carrito", f"El total del carrito es: {total}")

    def ver_contenido_carrito(self):
        contenido = self.cliente.carrito.contenido()
        if contenido:
            contenido_info = "\n".join([f"{nombre}: {info['cantidad']} unidades" for nombre, info in contenido.items()])
            messagebox.showinfo("Contenido del Carrito", contenido_info)
        else:
            messagebox.showwarning("Carrito Vacío", "El carrito está vacío.")

    def ver_stock_actualizado(self):
        stock_actual = self.supermercado.listar_productos_stock()
        if stock_actual:
            stock_info = "\n".join([f"{nombre}: {info['cantidad']} unidades" for nombre, info in stock_actual.items()])
            messagebox.showinfo("Stock Actualizado", stock_info)
        else:
            messagebox.showwarning("Stock Vacío", "No hay productos en stock.")

    def realizar_compra(self):
        total = Caja.procesar_compra(self.cliente, self.supermercado)
        if total > 0:
            messagebox.showinfo("Compra Realizada", f"Compra realizada por un total de: {total}")
        else:
            messagebox.showwarning("Compra", "El carrito está vacío.")

    def vaciar_carrito(self):
        self.cliente.carrito.vaciar()
        messagebox.showinfo("Carrito Vacío", "El carrito ha sido vaciado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()