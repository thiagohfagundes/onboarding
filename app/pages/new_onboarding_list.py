import reflex as rx
from sqlmodel import select
from app.models.processo import Processo
from typing import List

from app.components.componentes_gerais import heading_pagina
from app.components.onboardings_list import create_onboarding_dialog, status_badge, progress_bar, nome_template_processo
from app.utils.integrador import Integracao


class OnboardingListState(rx.State):
    processos: List['Processo'] = []
    loading_processos: bool = True
    

    def lista_processos(self):
        with rx.session() as session:
            dados = session.exec(
                select(Processo)
            ).all()
            self.processos = dados
            self.loading_processos = False
            

def onboardings_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Processo"),
                rx.table.column_header_cell("Cliente"),
                rx.table.column_header_cell("Responsável"),
                rx.table.column_header_cell("Status"),
                rx.table.column_header_cell("Progresso"),
                rx.table.column_header_cell(
                    "Data de início", 
                    max_width="100px"),
                rx.table.column_header_cell(rx.icon("settings", size=20, color="gray"), max_width="20px")
            )
        ),
        rx.table.body(
            rx.foreach(
                OnboardingListState.processos,
                lambda onboarding: rx.table.row(
                    rx.table.cell(nome_template_processo(onboarding['nome'], onboarding['template'])),
                    rx.table.cell(
                        rx.cond(
                            onboarding["cliente"] != "", 
                            onboarding["cliente"],
                            rx.text("Cliente não definido", color_scheme="gray")
                        )
                        
                    ),
                    rx.table.cell(
                        "Fulano"
                    ),
                    rx.table.cell(status_badge(onboarding["status"])),
                    rx.table.cell(progress_bar(onboarding["progresso"])),
                    rx.table.cell(onboarding["data_inicio"], max_width="100px"),
                    rx.table.cell(
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text("...")
                            ),
                            rx.menu.content(
                                rx.menu.item("Excluir"),
                                rx.menu.item("Duplicar")
                            )
                        ),
                        max_width="20px"
                    ),
                    on_click=lambda: rx.redirect(f"/onboardings/{onboarding['id']}"),
                    class_name="cursor-pointer",
                    align="center"
                )
            )
        ),
        # Propriedades da tabela
        width="100%"
    )


def onboardings_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                heading_pagina("Onboardings", "Gerencie todos os seus processos de onboarding de clientes."),
                create_onboarding_dialog(),
                class_name="flex justify-between items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.input(
                        placeholder="Pesquise por nome ou cliente...",
                        width="100%",
                        size='3'
                    ),
                    class_name="relative",
                ),
                rx.select(
                    ["Todos", "Ativos", "Completos", "Atrasados"],
                    size='3'
                ),
                class_name="flex flex-col md:flex-row gap-4 mt-6",
            ),
            rx.el.div(
                onboardings_table(),
                rx.cond(
                    OnboardingListState.loading_processos,
                    rx.el.div(
                        rx.spinner(),
                        class_name= "flex justify-center items-center h-64 rounded-2xl border border-gray-100 shadow-sm mt-6",
                    ),
                    rx.cond(
                        OnboardingListState.processos.length() == 0,
                        rx.el.div(
                            rx.el.p(
                                "Nenhum onboarding encontrado.",
                                class_name="text-center py-10",
                            ),
                            class_name= "rounded-2xl border border-gray-100 shadow-sm mt-6",
                        ),
                        None,
                    ),
                ), 
                class_name="mt-6 rounded-2xl border border-gray-100 shadow-sm overflow-hidden",
            ),
            class_name="p-4 sm:p-6 md:p-8",
        ),
        class_name="flex-1 overflow-y-auto",
    )
