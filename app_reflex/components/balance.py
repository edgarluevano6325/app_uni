import reflex as rx
from app_reflex.state.state import State as st


class Balance:
    @staticmethod
    def reestablecer_saldo() -> rx.Component:
        return rx.button(
            "Reiniciar datos",
            on_click=st.reiniciar_datos,
            color_scheme="red",
            variant="soft",
        )

    @staticmethod
    def ingresar_dinero() -> rx.Component:
        return rx.vstack(
            rx.hstack(
                rx.text("Saldo disponible:", size="5", weight="bold"),
                rx.text("$", st.capital, size="5", weight="bold", color_scheme="green"),
                justify="between",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    width="200px",
                    on_change=st.set_value,
                    value=st.value,
                    placeholder="Monto a agregar...",
                    type="number",
                ),
                rx.button("Agregar dinero", on_click=st.agregar_dinero),
                justify="between",
                align="center",
                width="100%",
            ),
            spacing="3",
            width="100%",
        )