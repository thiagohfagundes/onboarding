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

            self.processo = dados
            self.etapas = dados.etapas

def card_detalhes_onboarding(titulo: str, descricao: str, data_inicio: str, data_fim: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(titulo, size="5", weight="bold"),
                width="100%"
            ),
            rx.text(descricao, size='2', color_scheme='gray'),
            rx.divider(),
            rx.hstack(
                rx.icon("calendar", size=15, color=rx.color("accent")),
                rx.text(f"Início: {data_inicio}", size='2'),
                align='center',
                width='100%'
            ),
            rx.hstack(
                rx.icon("calendar-check", size=15, color=rx.color("accent")),
                rx.text(f"Término: {data_fim}", size='2'),
                align='center',
                width='100%'
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def card_etapas_onboarding(lista_etapas: list =[]) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Etapas do Onboarding", size="5", weight="bold"),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def card_progresso_onboarding() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Progresso do Onboarding", size="5", weight="bold"),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                rx.progress(value=70, size="3", width="100%"),
                rx.hstack(
                    rx.text("70 % concluído", size='2'),
                    rx.text("7 de 10 tarefas concluídas", size='2'),
                    justify="between",
                    width="100%"
                ),
                align="center",
                width="100%"
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def participantes_item(nome: str, email: str, iniciais: str, empresa: str, cargo: str, papel: str) -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.avatar(fallback=iniciais),
            rx.vstack(
                rx.text(nome, size='3', weight='bold'),
                rx.text(email, size='2', color_scheme='gray'),
                spacing='1'
            ),
            spacing='3',
            align='center',
        ),
        rx.badge(
            papel,
            color_scheme='cyan',
            size='3'
        ),
        rx.icon("pencil", size=20, color=rx.color("gray", 7)),
        width='100%',
        align='center',
        justify='between',
        spacing='5',
        padding_x='1em',
    )

def card_participantes_onboarding() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Participantes", size="5", weight="bold"),
                rx.button("Adicionar", size="3"),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                participantes_item("Thiago Silva", "thiago.silva@example.com", "TS", "Gerente", "Empresa X", "Ponto focal"),
                width="100%",
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def caixa_proxima_tarefa() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Próxima Tarefa", size="5", weight="bold"),
                width="100%"
            ),
            rx.vstack(
                rx.text("Configurar conta do cliente", size='3', weight='medium'),
                rx.text("Data de vencimento: 25/11/2025", size='2', color_scheme='gray'),
                rx.text("Responsável: Ana Pereira", size='2', color_scheme='gray'),
                spacing='2',
                width="100%"
            ),
            width="100%"
        ),
        width="100%",
        bg=rx.color("blue", 3),
        class_name="shadow-md"
    )

def header_onboarding_details() -> rx.Component:
    return rx.box(
        rx.text("Detalhes do Onboarding", size="6", weight="bold", align="center"),
        align="center",
        justify="center",
        width="100%",
        padding="1em",
        margin_top="1em",
        border_radius="10px",
        
        bg=rx.color("blue"),
    )

def bloco_esquedo() -> rx.Component:
    return rx.scroll_area(
        rx.vstack(
            card_detalhes_onboarding(
                "Onboarding de Cliente X",
                "Este é o onboarding do Cliente X, que inclui todas as etapas necessárias para garantir uma integração bem-sucedida.",
                "22/10/2025",
                "22/12/2025"
            ),
            card_progresso_onboarding(),
            card_participantes_onboarding(),
            spacing="4",
            width="100%"
        ),
        width="100%",
    )

def bloco_direito(child: rx.Component = None, *args, **kwargs) -> rx.Component:
    return rx.scroll_area(
        rx.vstack(
            caixa_proxima_tarefa(),
            card_etapas_onboarding(OnboardingDetailsState.etapas),
            spacing="4",
            width="100%"
        ),
        width="100%"
    )

def onboarding_screen() -> rx.Component:
    return rx.vstack(
        header_onboarding_details(),
        rx.grid(
            bloco_esquedo(),
            bloco_direito(),
            width="100%",
            columns="1fr 2fr",
            spacing="4",
        ),
        margin_x='1em',
    )


def detalhes_onboarding():
    return onboarding_screen()