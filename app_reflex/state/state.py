"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config


class State(rx.State):
    """The app state."""
    value: str = ""
    capital: float = 0.0
    nombre_producto: str = ""
    costo_producto: str = ""
    cantidad_producto: str = ""
    productos: dict [str, dict] = {}
    total: float = 0

    def reiniciar_datos(self):
        self.capital = 0.0
        self.productos = {}

    def filtro_dinero(self, value: str):
            self.value = value


    def agregar_dinero(self):
        try:
            self.capital += float(self.value)
            self.value = ("")
        except ValueError as e:
            return rx.window_alert(f"error, ingresa solo numeros") 
    
    
    def calcular_costo(self):
        self.total = 0
        for nombre in self.productos:
            self.total += self.productos[nombre]["costo"] * self.productos[nombre]["cantidad"]
        
    def set_nombre_producto(self, value: str):
        self.nombre_producto = value

    def set_costo_producto(self, value: str):
        self.costo_producto = value

    def set_cantidad_producto(self, value: str):
        self.cantidad_producto = value

    def agregar_producto(self):
        self.calcular_costo()
        try:
            costo = float(self.costo_producto)
            cantidad = int(self.cantidad_producto)
            nuevo_total = self.total + (costo * cantidad)
            if self.capital == 0:
                return rx.window_alert("debes agregar primero el saldo")
            elif self.capital >= nuevo_total:
                self.productos[self.nombre_producto] = {
                "costo": float(self.costo_producto),
                "cantidad": int(self.cantidad_producto),
                }
                self.calcular_costo()
                self.nombre_producto = ""
                self.costo_producto = ""
                self.cantidad_producto = ""
            else:
                return rx.window_alert("el saldo no es suficiente")
        except:
            return
    