import reflex as rx
from app.models.processo import Template
from app.states.processo import TemplatesState

from app.components.componentes_gerais import heading_pagina, card_headings, card_description

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
            rx.vstack(
                rx.vstack(
                    rx.text("Nome do template (identificador)", class_name="text-sm font-medium"),
                    rx.input(
                        name="name",
                        placeholder="ex: Onboarding Cliente A",
                        width='100%',
                        size='3',
                        on_change=TemplatesState.set_nome
                    ),
                    spacing='1',
                    width='100%'
                ),
                rx.vstack(
                    rx.text("Comentário", class_name="text-sm font-medium"),
                    rx.text_area(
                        name="notes",
                        placeholder="Comentários opcionais sobre este onboarding...",
                        width='100%',
                        size='3',
                        on_change=TemplatesState.set_comentario
                    ),
                    spacing='1',
                    width='100%'
                ),
                rx.hstack(
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
                        size="3",
                        on_click=TemplatesState.criar_template,
                    ),
                    spacing='1',
                    width='100%',
                    justify='between'
                ),
            ),
            style={"max_width": "500px"},
        ),
        open=TemplatesState.show_create_dialog,
        on_open_change=TemplatesState.toggle_create_dialog,
    )

def card_template(template: Template) -> rx.Component:
    titulo = template["nome"]
    descricao = template["descricao"]
    num_etapas = 1
    num_tarefas = 1
    data_criacao = template['data_criacao']

    return rx.card(
        rx.vstack(
            rx.hstack(
                card_headings(titulo),
                rx.hstack(
                    rx.icon("trash-2", size = 15, color=rx.color("gray", 10), on_click=lambda: TemplatesState.deletar_template(template['id']))
                ),
                justify="between",
                width="100%"
            ),
            card_description(descricao),
            rx.hstack(
                rx.icon("footprints", size=15, color=rx.color("accent")),
                rx.text(f"{num_etapas} etapas", size='2'),
                align='center',
                width='100%'
            ),
            rx.hstack(
                rx.icon("circle-check-big", size=15, color=rx.color("accent")),
                rx.text(f"{num_tarefas} tarefas", size='2'),
                align='center',
                width='100%'
            ),
            rx.divider(),
            rx.text(f"Data de criação: {data_criacao}", color_scheme='gray', size='2'),
            width="100%"
        ),
        width="100%",
        on_click=lambda: rx.redirect(f"/templates/{template['id']}"),
        class_name="shadow-md hover:shadow-xl hover:scale-[1.02] transition-all duration-300 cursor-pointer"
    )

def templates_cards_box():
    return rx.grid(
        rx.foreach(TemplatesState.templates, card_template),
        columns="4",
        width = "100%",
        padding = "1em",
        margin_top='10px',
        spacing='4'
    )

def templates_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                heading_pagina("Templates", "Crie e gerencie templates (modelos) para seus processos"),
                create_template_dialog(),
                class_name="flex justify-between items-center",
            ),
            rx.cond(
                TemplatesState.templates.length() == 0,
                rx.text("Nenhum template encontrado"),
                templates_cards_box()
            ),
            class_name="p-4 sm:p-6 md:p-8",
        ),
        class_name="flex-1 overflow-y-auto",
    )