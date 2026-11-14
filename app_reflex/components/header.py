import reflex as rx


class Header:
    @staticmethod
    def Encabezado(titulo: str) -> rx.Component:
        return rx.heading(
            titulo,
            size="7",
            margin_bottom="16px",
            text_align="center",
        )