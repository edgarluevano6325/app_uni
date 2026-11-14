import reflex as rx
from .state import State


class ProductState(rx.State):
    """Estado independiente para el catálogo y edición de productos."""
    productos: dict[str, dict] = {}
    total: float = 0.0

    # Variables para agregar producto
    nombre_producto: str = ""
    costo_producto: str = ""
    cantidad_producto: str = ""

    # Variables para editar producto
    producto_editando: str = ""
    nuevo_costo: str = "0"
    nueva_cantidad: str = "0"

    @rx.var
    def cantidad_de_productos(self) -> int:
        return len(self.productos)

    def calcular_costo(self):
        self.total = 0.0
        for nombre in self.productos:
            self.total += self.productos[nombre]["costo"] * self.productos[nombre]["cantidad"]

    # Setters de creación
    def set_nombre_producto(self, value: str):
        self.nombre_producto = value

    def set_costo_producto(self, value: str):
        self.costo_producto = value

    def set_cantidad_producto(self, value: str):
        self.cantidad_producto = value

    # Setters de edición
    def set_nueva_cantidad(self, valor: str):
        self.nueva_cantidad = valor

    def set_nuevo_costo(self, valor: str):
        self.nuevo_costo = valor

    async def agregar_producto(self):
        main_state = await self.get_state(State)
        self.calcular_costo()
        try:
            costo = float(self.costo_producto)
            cantidad = int(self.cantidad_producto)
            nuevo_total = self.total + (costo * cantidad)

            if main_state.capital == 0:
                return rx.window_alert("debes agregar primero el saldo")
            elif main_state.capital >= nuevo_total:
                self.productos[self.nombre_producto] = {
                    "costo": costo,
                    "cantidad": cantidad,
                }
                self.calcular_costo()
                self.nombre_producto = ""
                self.costo_producto = ""
                self.cantidad_producto = ""
            else:
                return rx.window_alert("el saldo no es suficiente")
        except ValueError:
            return

    def eliminar_producto(self, value: str):
        self.productos.pop(value, None)
        self.calcular_costo()

    def abrir_edicion(self, nombre: str):
        producto = self.productos.get(nombre)
        if producto:
            self.producto_editando = nombre
            self.nuevo_costo = str(producto["costo"])
            self.nueva_cantidad = str(producto["cantidad"])

    def guardar_edicion(self):
        if self.producto_editando in self.productos:
            self.productos[self.producto_editando] = {
                "costo": float(self.nuevo_costo),
                "cantidad": int(self.nueva_cantidad),
            }
            self.calcular_costo()