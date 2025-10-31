import reflex as rx
from typing import List
from app.pages.base_page import base_blank_page
from app.models.processo import Etapa, Processo
from sqlmodel import select

class OnboardingDetailsState(rx.State):
    processo: Processo = None
    etapas: List['Etapa'] = []

    @rx.var(cache=True)
    def onboarding_id(self) -> str:
        print(self.router.page.params)
        return self.router.page.params.get("id", "")
    
    def captura_detalhes_onboarding(self): # GET onboarding
        with rx.session() as session:
            dados = session.exec(
                Processo.select().where(
                    Processo.id == self.onboarding_id
                )
            ).first()
            print(dados)
            self.processo = dados

def return_link() -> rx.Component:
    return rx.hstack(
        rx.icon("circle-arrow-left", size=20),
        rx.text("Lista de onboardings"),
        spaging="2",
        align="center",
        margin = "1em"
    )

def onboarding_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.heading(
                "Boas-vindas Cliente Cliente A",
                size="7",
            ),
            class_name="w-full p-4 rounded-t-xl text-center shadow-md",
            bg=rx.color("blue")
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Plano de Onboarding", class_name="font-semibold"
                ),
                rx.el.div(OnboardingDetailsState.processo["nome"], class_name="text-gray-600"),
                class_name="p-3 rounded-lg shadow-sm",
                bg=rx.color("gray", 4)
            ),
            rx.el.div(
                rx.el.div(
                    OnboardingDetailsState.processo["data_inicio"], class_name="font-semibold"
                ),
                rx.el.div("Término previsto: 22/10/2025", class_name="text-gray-600"),
                class_name="p-3 rounded-lg shadow-sm",
                bg=rx.color("gray", 4)
            ),
            class_name="flex justify-between p-4 gap-4",
        ),
        class_name="rounded-xl shadow-md mb-6 border border-gray-200",
    )

def detalhes_onboarding():
    return base_blank_page(
        onboarding_header()
    )