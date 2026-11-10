import reflex as rx
from ..state.state import State as st


class Products:

    def ingresar_producto():
        return rx.vstack(
            rx.text("producto: ", size="6"),
            rx.hstack(
                rx.text("nombre del producto: ", size="4"),
                rx.input(
                    placeholder="nombre del producto...",
                    on_change=st.set_nombre_producto,
                    value=st.nombre_producto,
                ),
            ),
            rx.hstack(
                rx.text("costo del producto: ", size="4"),
                rx.input(
                    placeholder="costo del producto...",
                    on_change=st.set_costo_producto,
                    value=st.costo_producto,
                ),
            ),
            rx.hstack(
                rx.text("cantidad del producto: ", size="4"),
                rx.input(
                    placeholder="cantidad del producto...",
                    on_change=st.set_cantidad_producto,
                    value=st.cantidad_producto
                ),
            ),
            rx.button("agregar producto", on_click=st.agregar_producto),
            justify="between",
            align="center",
            width="100%",
        )
