import reflex as rx
from app.states.auth_state import StateUsuario
from app.components.onboarding_details import *

def container_onboarding_details() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            return_link(),
            onboarding_header(),
            onboarding_progress(),
            participants_section(),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Tarefas e etapas", value="tab1"), rx.tabs.trigger("Linha do tempo (em breve)", value="tab2", disabled=True)
                ),
                rx.tabs.content(
                    onboarding_steps(),
                    value="tab1",
                    margin_top="20px"
                ),
                default_value="tab1",
            ),
            class_name="max-w-4xl mx-auto p-4 md:p-8",
        ),
        class_name="bg-gray-50 min-h-screen",
    )