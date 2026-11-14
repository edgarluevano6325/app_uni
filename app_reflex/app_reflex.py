import reflex as rx

from app_reflex.state.state import State as st
from app_reflex.components.balance import Balance as bl
from app_reflex.components.products import Products as pr
from app_reflex.components.header import Header as hr
from app_reflex.components.products_cards import ProductsCards as card


def modal_editar_producto() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(f"Editar: {st.producto_original}"),
            rx.dialog.description(
                "Modifica los datos del producto y guarda los cambios.",
                size="2",
                margin_bottom="12px",
            ),
            rx.vstack(
                rx.text("Nombre del producto", size="2", weight="bold"),
                rx.input(
                    value=st.nuevo_nombre,
                    on_change=st.set_nuevo_nombre,
                    width="100%",
                ),
                rx.text("Costo", size="2", weight="bold"),
                rx.input(
                    value=st.nuevo_precio,
                    on_change=st.set_nuevo_precio,
                    type="number",
                    width="100%",
                ),
                rx.text("Cantidad", size="2", weight="bold"),
                rx.input(
                    value=st.nueva_cantidad,
                    on_change=st.set_nueva_cantidad,
                    type="number",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray"),
                ),
                rx.button("Guardar cambios", on_click=st.guardar_edicion),
                justify="end",
                spacing="3",
                margin_top="16px",
            ),
        ),
        open=st.modal,
        on_open_change=st.set_modal,
    )


def index() -> rx.Component:
    return rx.box(
        # Header
        rx.hstack(
            bl.reestablecer_saldo(),
            justify="end",
            padding="10px",
        ),
        # Body
        rx.center(
            rx.vstack(
                rx.vstack(
                    hr.Encabezado("Bienvenido a la app de balance"),
                    rx.vstack(
                        rx.card(bl.ingresar_dinero(), width="100%"),
                        rx.card(
                            pr.ingresar_producto(),
                            align="center",
                            justify="center",
                            width="100%",
                        ),
                        align="center",
                        width="100%",
                    ),
                    align="center",
                ),
                rx.vstack(
                    rx.box(height="40px"),
                    rx.cond(
                        st.cantidad_de_productos == 0,
                        rx.box(),
                        rx.card(card.lista_productos()),
                    ),
                    align="center",
                ),
                align="center",
            )
        ),
        # Modal único de edición
        modal_editar_producto(),
    )


app = rx.App()
app.add_page(index, on_load=st.cargar_desde_excel)