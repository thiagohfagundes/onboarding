import reflex as rx
from app.models.processo import Processo
from datetime import datetime

class OnboardingPageState(rx.State):
    show_create_dialog: bool = False
    templates = [
        "Template 1",
        "Template 2",
        "Template 3"
    ]
    filtered_onboardings = [
        {"name": "Onboarding 1", "client": "Cliente ABC", "template": "template 1", "status": "Active", "progress": 50, "start_date": "20/10/2025"},
        {"name": "Onboarding 1", "client": "Cliente ABC", "template": "template 1", "status": "Active", "progress": 50, "start_date": "20/10/2025"},
        {"name": "Onboarding 1", "client": "Cliente ABC", "template": "template 1", "status": "Active", "progress": 50, "start_date": "20/10/2025"}
    ]

    @rx.event
    def toggle_create_dialog(self, open: bool):
        self.show_create_dialog = open

    @rx.event
    def create_onboarding(self, form_data: dict):
        cliente = form_data.get("client")
        nome = form_data.get("name")
        data_inicio = form_data.get("start_date")
        notas = form_data.get("notes")

        #criar o cliente

        #criar o onboarding
        with rx.session() as session:
            session.add(
                Processo(
                    nome=nome,
                    descricao=notas,
                    cliente=cliente,
                    data_criacao=datetime.now(),
                    data_inicio=datetime.now() # CORRIGIR
                )
            )
            session.commit()
        
        print(f"Onboarding criado, dados: {cliente}")
