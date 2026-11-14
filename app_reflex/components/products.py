import reflex as rx
from app_reflex.state.state import State as st


class Products:
    @staticmethod
    def ingresar_producto() -> rx.Component:
        return rx.vstack(
            rx.text("Agregar producto", size="5", weight="bold"),
            rx.input(
                placeholder="Nombre del producto...",
                value=st.nombre_producto,
                on_change=st.set_nombre_producto,
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Costo...",
                    value=st.costo_producto,
                    on_change=st.set_costo_producto,
                    type="number",
                    width="50%",
                ),
                rx.input(
                    placeholder="Cantidad...",
                    value=st.cantidad_producto,
                    on_change=st.set_cantidad_producto,
                    type="number",
                    width="50%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Agregar producto",
                on_click=st.agregar_producto,
                width="100%",
            ),
            spacing="3",
            width="100%",
        )