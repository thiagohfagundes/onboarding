import reflex as rx

# EXCLUSIVO DO STATE
from app.models.processo import Template
from typing import List
from sqlmodel import select
from datetime import datetime

class TemplateListViewState(rx.State):
    templates: List['Template'] = []
    show_create_dialog: bool = False

    def lista_templates(self):
        with rx.session() as session:
            dados = session.exec(
                select(Template)
            ).all()
            print(dados)
            self.templates = dados

    @rx.event
    def deletar_template(self, id):
        print(f"deletar {id}")

    @rx.event
    def toggle_create_dialog(self, open: bool):
        self.show_create_dialog = open

    @rx.event
    def ir_para(self, id: int):
        url = f"/templates/{id}"
        print(url)
        rx.redirect("/")

    @rx.event
    def criar_template(self, form_data: dict):    
        nome = form_data.get("name")
        notas = form_data.get("notes")

        with rx.session() as session:
            session.add(
                Template(
                    nome=nome,
                    descricao=notas,
                    data_criacao=datetime.now(),
                )
            )
            session.commit()
        
        print(f"Onboarding criado, dados: {nome}")

def create_template_dialog():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("circle_plus", class_name="mr-2"),
                "Criar Template",
                size="3"
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Criar Novo Template", class_name="text-lg font-bold"),
            rx.dialog.description(
                "Preencha os detalhes para o novo template de processo de onboarding.",
                class_name="text-sm text-gray-500 mb-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Nome do template", class_name="text-sm font-medium"),
                    rx.input(
                        name="name",
                        placeholder="ex: Onboarding Grandes Contas",
                        width='100%',
                        size='3'
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Comentário", class_name="text-sm font-medium"),
                    rx.text_area(
                        name="notes",
                        placeholder="Comentários opcionais sobre este onboarding...",
                        width='100%',
                        size='3'
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            class_name="bg-gray-200 text-gray-800",
                            size="3"
                        )
                    ),
                    rx.button(
                        "Criar Onboarding",
                        type="submit",
                        size="3"
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                on_submit=TemplateListViewState.criar_template,
                reset_on_submit=True,
            ),
            style={"max_width": "500px"},
        ),
        open=TemplateListViewState.show_create_dialog,
        on_open_change=TemplateListViewState.toggle_create_dialog,
    )

def card_template(template: Template) -> rx.Component:
    titulo = template["nome"]
    descricao = template["descricao"]
    num_etapas = 1
    num_tarefas = 1

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(titulo),
                rx.hstack(
                    rx.icon("trash-2", on_click=lambda: TemplateListViewState.deletar_template(template['id']))
                ),
                justify="between",
                width="100%"
            ),
            rx.text(descricao),
            rx.divider(),
            rx.text(f"{num_etapas} etapas"),
            rx.text(f"{num_tarefas} tarefas"),
            width="100%"
        ),
        width="100%",
        on_click=lambda: rx.redirect(f"/templates/{template['id']}")
    )

def templates_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.heading("Templates", size="3"),
                create_template_dialog(),
                class_name="flex justify-between items-center",
            ),
            rx.cond(
                TemplateListViewState.templates.length() == 0,
                rx.text("Nenhum template encontrado"),
                rx.grid(
                    rx.foreach(TemplateListViewState.templates, card_template),
                    columns="4"
                )
            ),
            class_name="p-4 sm:p-6 md:p-8",
        ),
        class_name="flex-1 overflow-y-auto",
    )