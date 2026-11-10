import reflex as rx
from rxconfig import config
from app_reflex.state.state import State as st


class Balance(rx.Component):
    def Encabezado(saludo):
        return rx.heading(saludo, size="8"),
        
    def reestablecer_saldo():
        return rx.button("reiniciar datos", on_click=st.reiniciar_datos),

    def ingresar_dinero():
        return rx.hstack(
            rx.text("saldo: ", size="6"),

            rx.input(
                width="200px",
                height="30px",
                on_change=st.filtro_dinero,
                value=st.value,
                placeholder="saldo...",
            ),
            rx.button("agregar dinero", on_click=st.agregar_dinero, ),
            justify = "between",
        ),

    
    def calcular_costos() -> float :
        return 2.0