import reflex as rx
from app_reflex.state.state import State as st


class ProductsCards:
    @staticmethod
    def _tarjeta_item(item) -> rx.Component:
        nombre = item[0]
        datos = item[1]
        return rx.card(
            rx.hstack(
                rx.vstack(
                    rx.text(nombre, size="4", weight="bold"),
                    rx.text(
                        "Costo: $",
                        datos["costo"],
                        " | Cantidad: ",
                        datos["cantidad"],
                        size="2",
                        color_scheme="gray",
                    ),
                    rx.text("Subtotal: $", datos["subtotal"], size="2", weight="medium"),
                    spacing="1",
                    align="start",
                ),
                rx.button(
                    "Editar",
                    on_click=lambda: st.abrir_modal_edicion(nombre),
                    variant="soft",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            width="100%",
        )

    @staticmethod
    def lista_productos() -> rx.Component:
        return rx.vstack(
            rx.text("Productos registrados", size="5", weight="bold"),
            rx.foreach(st.productos, ProductsCards._tarjeta_item),
            rx.divider(),
            # Resumen estadístico generado con Pandas
            rx.vstack(
                rx.text("Análisis del inventario", size="3", weight="bold", color_scheme="gray"),
                rx.hstack(
                    rx.text("Total de artículos:", size="2"),
                    rx.text(st.total_unidades, size="2", weight="bold"),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Promedio por producto:", size="2"),
                    rx.text("$", st.promedio_gasto, size="2", weight="bold"),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Mayor gasto:", size="2"),
                    rx.text(st.producto_mayor_gasto, size="2", weight="bold", color_scheme="amber"),
                    justify="between",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Total a pagar:", size="4", weight="bold"),
                rx.text("$", st.total, size="4", weight="bold", color_scheme="blue"),
                justify="between",
                width="100%",
            ),
            spacing="3",
            width="400px",
        )