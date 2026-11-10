"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from app_reflex.state.state import State as st
from app_reflex.components.balance import Balance as bl
from app_reflex.components.products import Products as pr


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        # header
        rx.hstack(
            bl.reestablecer_saldo(),
            justify="end",
            padding="10px",
        ),
        # main
        rx.center(
            rx.vstack(
                bl.Encabezado("Bienvenido a la app de balance"),
                rx.card(bl.ingresar_dinero(), width="100%"),
                rx.card(
                    pr.ingresar_producto(),
                    align="center",
                    justify="center",
                    width="100%",
                ),
                rx.text(f"capital: {st.capital}", size="6"),
                rx.text(st.productos, size="6"),
                rx.text("total a pagar: ",),
                rx.text(st.total),
                align="center",
            )

        ),
    )


app = rx.App()
app.add_page(index)
