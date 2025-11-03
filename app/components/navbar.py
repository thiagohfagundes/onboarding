import reflex as rx
from app.states.auth_state import StateUsuario, AuthState

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

def notificacoes_icon(numero: int) -> rx.Component:
    return rx.box(
        rx.box(
            rx.icon("bell", size=24, class_name="text-gray-700"),
            rx.cond(
                numero > 0,
                rx.box(
                    str(numero),
                    class_name=(
                        "absolute -top-1.5 -right-1.5 bg-red-500 text-white text-xs "
                        "font-semibold rounded-full w-5 h-5 flex items-center justify-center shadow-sm"
                    ),
                ),
            ),
            class_name="relative inline-block",
        ),
        class_name="cursor-pointer hover:text-blue-600 transition-colors duration-150"
    )

def notificacao(mensagem: str) -> rx.Component:
    return rx.box(
        rx.text(mensagem, size="3"),
        padding="0.5em",
        hover_bg=rx.color("gray", 2),
        width="200px",
        cursor="pointer",
        class_name="hover:bg-gray-100"
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.heading("Professional Services Superlógica", size="5", weight="bold"),
                    rx.text("Página do cliente", size="4", color_scheme="gray"),
                    align="center",
                    justify="center",
                    spacing="5"
                ),
                rx.hstack(
                    rx.menu.root(
                        rx.menu.trigger(notificacoes_icon(3)),
                        rx.menu.content(
                            notificacao("Notificação 1"),
                            notificacao("Notificação 2"),
                            notificacao("Notificação 3"),
                            side="left"
                        ),
                    ),
                    usuario_info(StateUsuario.usuario_nome, StateUsuario.usuario_empresa, StateUsuario.usuario_iniciais),
                    align="center",
                    spacing="5"
                ),  
                padding_x="1em",
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg", width="2em", height="auto", border_radius="25%"
                    ),
                    rx.heading("Onboarding", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(rx.icon("user"), size="2", radius="full")
                    ),
                    rx.menu.content(
                        rx.menu.item("Settings"),
                        rx.menu.item("Earnings"),
                        rx.menu.separator(),
                        rx.menu.item("Log out"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
        class_name="shadow-md",
    )