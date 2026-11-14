import os
import pandas as pd
import reflex as rx

ARCHIVO_EXCEL = "productos.xlsx"


class State(rx.State):
    """Estado principal de la aplicación."""

    # --- Variables de Capital y Totales ---
    value: str = ""
    capital: float = 0.0
    total: float = 0.0

    # --- Variables de Análisis (calculadas con Pandas) ---
    total_unidades: int = 0
    promedio_gasto: float = 0.0
    producto_mayor_gasto: str = "-"

    # --- Variables de Productos ---
    nombre_producto: str = ""
    costo_producto: str = ""
    cantidad_producto: str = ""
    productos: dict[str, dict[str, float]] = {}

    # --- Variables del Modal de Edición ---
    modal: bool = False
    producto_original: str = ""
    nuevo_nombre: str = ""
    nuevo_precio: str = ""
    nueva_cantidad: str = ""

    @rx.var
    def cantidad_de_productos(self) -> int:
        return len(self.productos)

    # --- Setters explícitos ---
    def set_value(self, value: str):
        self.value = value

    def set_nombre_producto(self, value: str):
        self.nombre_producto = value

    def set_costo_producto(self, value: str):
        self.costo_producto = value

    def set_cantidad_producto(self, value: str):
        self.cantidad_producto = value

    def set_modal(self, value: bool):
        self.modal = value

    def set_nuevo_nombre(self, value: str):
        self.nuevo_nombre = value

    def set_nuevo_precio(self, value: str):
        self.nuevo_precio = value

    def set_nueva_cantidad(self, value: str):
        self.nueva_cantidad = value

    #
    # 1. MANIPULACIÓN, LIMPIEZA Y ANÁLISIS (PANDAS)
    #
    def _obtener_dataframe(self) -> pd.DataFrame:
        """Convierte el diccionario en un DataFrame limpio, calculado y ordenado."""
        if not self.productos:
            return pd.DataFrame(columns=["Producto", "Costo", "Cantidad", "Subtotal"])

        filas = [
            {
                "Producto": nombre,
                "Costo": datos["costo"],
                "Cantidad": int(datos["cantidad"]),
            }
            for nombre, datos in self.productos.items()
        ]
        df = pd.DataFrame(filas)

        # Manipulación vectorizada: calcular columna Subtotal y ordenar de mayor a menor
        df["Subtotal"] = df["Costo"] * df["Cantidad"]
        df = df.sort_values(by="Subtotal", ascending=False).reset_index(drop=True)
        return df

    def analizar_datos(self):
        """Extrae métricas estadísticas del DataFrame para mostrarlas en la UI."""
        df = self._obtener_dataframe()

        if df.empty:
            self.total = 0.0
            self.total_unidades = 0
            self.promedio_gasto = 0.0
            self.producto_mayor_gasto = "-"
            return

        self.total = round(float(df["Subtotal"].sum()), 2)
        self.total_unidades = int(df["Cantidad"].sum())
        self.promedio_gasto = round(float(df["Subtotal"].mean()), 2)
        indice_max = df["Subtotal"].idxmax()
        self.producto_mayor_gasto = str(df.loc[indice_max, "Producto"])

    def guardar_en_excel(self):
        df = self._obtener_dataframe()
        df.to_excel(ARCHIVO_EXCEL, sheet_name="Productos", index=False)

    def cargar_desde_excel(self):
        if not os.path.exists(ARCHIVO_EXCEL):
            return

        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Productos")

        # Limpieza de datos con Pandas
        df = df.dropna(subset=["Producto", "Costo", "Cantidad"]).copy()
        df["Producto"] = df["Producto"].astype(str).str.strip()
        df = df[df["Producto"] != ""]
        df["Costo"] = pd.to_numeric(df["Costo"], errors="coerce")
        df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")
        df = df.dropna(subset=["Costo", "Cantidad"])
        df = df[(df["Costo"] > 0) & (df["Cantidad"] > 0)]
        df = df.drop_duplicates(subset=["Producto"], keep="last")

        # Manipulación: recalcular subtotales y ordenar
        df["Subtotal"] = df["Costo"] * df["Cantidad"]
        df = df.sort_values(by="Subtotal", ascending=False)

        self.productos = {
            str(fila["Producto"]): {
                "costo": float(fila["Costo"]),
                "cantidad": int(fila["Cantidad"]),
                "subtotal": float(fila["Subtotal"]),
            }
            for _, fila in df.iterrows()
        }

        self.analizar_datos()
        if self.capital < self.total:
            self.capital = self.total

    # ==========================================
    # 2. GESTIÓN DE CAPITAL
    # ==========================================
    def agregar_dinero(self):
        try:
            monto = float(self.value)
            if monto <= 0:
                return rx.window_alert("Ingresa una cantidad mayor a cero")
            self.capital += monto
            self.value = ""
        except ValueError:
            return rx.window_alert("Error: ingresa solo números")

    def reiniciar_datos(self):
        self.capital = 0.0
        self.productos = {}
        self.analizar_datos()
        self.guardar_en_excel()

    # ==========================================
    # 3. ALTA DE PRODUCTOS
    # ==========================================
    def agregar_producto(self):
        self.analizar_datos()
        if not self.nombre_producto.strip():
            return rx.window_alert("Ingresa el nombre del producto")

        try:
            costo = float(self.costo_producto)
            cantidad = int(self.cantidad_producto)
            if costo <= 0 or cantidad <= 0:
                return rx.window_alert("Costo y cantidad deben ser mayores a cero")

            nuevo_total = self.total + (costo * cantidad)

            if self.capital == 0:
                return rx.window_alert("Debes agregar primero el saldo")
            elif self.capital >= nuevo_total:
                self.productos[self.nombre_producto.strip()] = {
                    "costo": costo,
                    "cantidad": cantidad,
                    "subtotal": costo * cantidad,
                }
                self.analizar_datos()
                self.guardar_en_excel()
                self.nombre_producto = ""
                self.costo_producto = ""
                self.cantidad_producto = ""
            else:
                return rx.window_alert("El saldo no es suficiente")
        except ValueError:
            return rx.window_alert("Verifica que costo y cantidad sean números válidos")

    # ==========================================
    # 4. MODAL DE EDICIÓN
    # ==========================================
    def abrir_modal_edicion(self, nombre: str):
        if nombre in self.productos:
            datos = self.productos[nombre]
            self.producto_original = nombre
            self.nuevo_nombre = nombre
            self.nuevo_precio = str(datos["costo"])
            self.nueva_cantidad = str(int(datos["cantidad"]))
            self.modal = True

    def guardar_edicion(self):
        if not self.nuevo_nombre.strip():
            return rx.window_alert("El nombre del producto no puede quedar vacío")

        try:
            precio = float(self.nuevo_precio)
            cantidad = int(self.nueva_cantidad)
            if precio <= 0 or cantidad <= 0:
                return rx.window_alert("Precio y cantidad deben ser mayores a cero")

            datos_anteriores = self.productos[self.producto_original]
            subtotal_anterior = datos_anteriores["costo"] * datos_anteriores["cantidad"]
            nuevo_total = (self.total - subtotal_anterior) + (precio * cantidad)

            if nuevo_total > self.capital:
                return rx.window_alert("El saldo no es suficiente para esta modificación")

            nombre_final = self.nuevo_nombre.strip()
            if nombre_final != self.producto_original:
                del self.productos[self.producto_original]

            self.productos[nombre_final] = {
                "costo": precio,
                "cantidad": cantidad,
                "subtotal": precio * cantidad,
            }
            self.analizar_datos()
            self.guardar_en_excel()
            self.modal = False
        except ValueError:
            return rx.window_alert("Verifica que precio y cantidad sean números válidos")