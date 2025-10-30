import reflex as rx
from reflex.style import set_color_mode, color_mode
from app.states.auth_state import StateUsuario, AuthState

def dark_mode_toggle() -> rx.Component:
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="monitor", size=20),
            value="system",
        ),
        rx.segmented_control.item(
            rx.icon(tag="sun", size=20),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=20),
            value="dark",
        ),
        on_change=set_color_mode,
        variant="classic",
        radius="large",
        value=color_mode,
    )

def usuario_info(nome:str, email:str, iniciais: str) -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.hstack(
                rx.avatar(fallback=iniciais),
                rx.vstack(
                    rx.text(nome, size="2"),
                    rx.text(email, size="1"),
                    spacing="0",
                    justify="center"
                ),
                align="center",
            ),
        ),
        rx.menu.content(
            rx.menu.item("Perfil", shortcut="⌘ E"),
            rx.menu.item("Configurações", shortcut="⌘ D"),
            rx.menu.separator(),
            rx.menu.item("Logout", shortcut="⌘ N", on_click=AuthState.sign_out),
        ),
    )

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.text(text, size="2"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("gray", 4),
                    "color": rx.color("gray", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        color= rx.color("black", 11),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Onboardings", "layout-dashboard", "/onboardings"),
        sidebar_item("Templates", "layout-dashboard", "/templates"),
        spacing="1",
        width="100%",
    )

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            sidebar_items(),
            rx.vstack(
                usuario_info(StateUsuario.usuario_nome, StateUsuario.usuario_empresa, StateUsuario.usuario_iniciais),
                dark_mode_toggle(),
            ),
            justify="between",  
            align="center",           
            height="100%",
        ),
        height="100vh",
        width="14em",
        padding="1em",
        bg=rx.color("gray", 2)
    )

