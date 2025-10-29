import reflex as rx
from sqlmodel import select
from app.models.processo import Processo
from typing import List

from app.components.onboardings_list import create_onboarding_dialog, status_badge, progress_bar

class OnboardingListState(rx.State):
    processos: List['Processo'] = []

    def lista_processos(self):
        with rx.session() as session:
            dados = session.exec(
                select(Processo)
            ).all()
            print(dados)
            self.processos = dados


def onboardings_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Onboardings", class_name="text-3xl font-bold"),
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
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                "Processo", scope="col", class_name="p-4 text-left w-2/6"
                            ),
                            rx.table.column_header_cell(
                                "Cliente", scope="col", class_name="p-4 text-left w-1/6"
                            ),
                            rx.table.column_header_cell(
                                "Template",
                                scope="col",
                                class_name="p-4 text-left w-1/6",
                            ),
                            rx.table.column_header_cell(
                                "Status", 
                                scope="col", 
                                class_name="p-4 text-left"
                            ),
                            rx.table.column_header_cell(
                                "Progresso",
                                scope="col",
                                class_name="p-4 text-left w-1/6",
                            ),
                            rx.table.column_header_cell(
                                "Data de início", 
                                scope="col", 
                                class_name="p-4 text-left"
                            ),
                            class_name="text-sm font-semibold tracking-wider",
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            OnboardingListState.processos,
                            lambda onboarding: rx.table.row(
                                rx.table.cell(
                                    onboarding["nome"],
                                    class_name="p-4 font-medium",
                                ),
                                rx.table.cell(
                                    onboarding["cliente"], class_name="p-4"
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        onboarding["template"] != None,
                                        onboarding["template"],
                                        "Nenhum template"
                                    ),
                                    class_name="p-4",
                                ),
                                rx.table.cell(
                                    status_badge(onboarding["status"]), class_name="p-4"
                                ),
                                rx.table.cell(
                                    progress_bar(onboarding["progresso"]),
                                    class_name="p-4 align-middle",
                                ),
                                rx.table.cell(
                                    onboarding["data_inicio"],
                                    class_name="p-4",
                                ),
                                on_click=lambda: rx.redirect(
                                    f"/onboardings/{onboarding['id']}"
                                ),
                                class_name="hover:bg-gray-50 cursor-pointer transition-colors",
                            ),
                        )
                    ),
                    class_name="w-full text-sm",
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
                class_name="mt-6 rounded-2xl border border-gray-100 shadow-sm overflow-hidden",
            ),
            class_name="p-4 sm:p-6 md:p-8",
        ),
        class_name="flex-1 overflow-y-auto",
    )
