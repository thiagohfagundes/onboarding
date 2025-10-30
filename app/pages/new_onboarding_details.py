import reflex as rx
from typing import List
from app.pages.base_page import base_page
from app.models.processo import Etapa, Processo
from sqlmodel import select

class OnboardingDetailsState(rx.State):
    processo: Processo = None
    etapas: List['Etapa'] = []

    @rx.var(cache=True)
    def onboarding_id(self) -> str:
        print(self.router.page.params)
        return self.router.page.params.get("id", "")
    
    @rx.event
    def captura_detalhes_onboarding(self): # GET onboarding
        with rx.session() as session:
            dados = session.exec(
                Processo.select().where(
                    Processo.id == self.onboarding_id
                )
            ).first()
            print(dados)
            self.processo = dados
    

def detalhes_onboarding():
    child = rx.vstack(
        rx.text(f"Detalhes do onboarding {OnboardingDetailsState.onboarding_id}"),
        rx.button("clique aqui", on_click=OnboardingDetailsState.captura_detalhes_onboarding)
    )
    return base_page(
        child
    )