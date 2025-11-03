import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar

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

def base_auth_page(child: rx.Component) -> rx.Component:
    return rx.el.div(
        child,
        class_name="flex flex-col items-center justify-center h-screen bg-gray-100",
    )

def base_blank_page(child: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        child,
        class_name="flex flex-col items-center bg-gray-100",
    )