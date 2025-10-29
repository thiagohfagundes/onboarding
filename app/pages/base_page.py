import reflex as rx
from app.components.sidebar import sidebar

def base_page(child: rx.Component) -> rx.Component:
    return rx.fragment(
        rx.hstack(
            sidebar(),
            rx.box(
                child,
                width='100%',
                height='100%',
            )
        ),
        height="100vh",
    )