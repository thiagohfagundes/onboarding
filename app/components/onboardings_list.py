import reflex as rx
from app.states.processo import OnboardingsState

def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.badge(
        status,
        color_scheme=rx.match(
            status,
            (
                "Ativo",
                "indigo",
            ),
            (
                "Completo",
                "cyan",
            ),
            (
                "Atrasado",
                "crimson",
            ),
            "indigo",
        ),
        size='3'
    )

def progress_bar(progresso: rx.Var[int]) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.progress(
                value=progresso,
                color_scheme=rx.cond(
                    progresso == 100,
                    'grass',
                    'cyan'
                ),
                size="3"
            ),
            rx.text(f"{progresso} %", width='100%'),
            align="center"
        ),
        align="center"
    )

def nome_template_processo(nome_processo: str, nome_template: str | None) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(nome_processo),
            rx.cond(nome_template != None,
                rx.text(nome_template, color_scheme="gray"),
                rx.text("Nenhum template", color_scheme="gray")
            ),
            spacing='1'
        )
    )

def create_onboarding_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("circle_plus", class_name="mr-2"),
                "Criar Onboarding",
                size="3"
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Criar Novo Onboarding", class_name="text-lg font-bold"),
            rx.dialog.description(
                "Preencha os detalhes para o novo processo de onboarding.",
                class_name="text-sm text-gray-500 mb-4",
            ),
            rx.vstack(
                rx.vstack(
                    rx.text("Nome do onboarding (identificador)", class_name="text-sm font-medium"),
                    rx.input(
                        name="name",
                        placeholder="ex: Onboarding Cliente A",
                        width='100%',
                        size='3',
                        on_change=OnboardingsState.set_nome
                    ),
                    spacing='1',
                    width='100%'
                ),
                rx.vstack(
                    rx.text("Nome do cliente", class_name="text-sm font-medium"),
                    rx.input(
                        name="client",
                        placeholder="ex: Imobiliária ABC",
                        width='100%',
                        size='3',
                        on_change=OnboardingsState.set_cliente
                    ),
                    spacing='1',
                    width='100%'
                ),
                rx.vstack(
                    rx.text("Template", class_name="text-sm font-medium"),
                    rx.el.select(
                        rx.el.option("Começar do zero (sem template)"),
                        rx.foreach(
                            OnboardingsState.templates,
                            lambda template: rx.el.option(template, value=template),
                        ),
                        name="template",
                        class_name="mt-1 w-full p-2 border rounded-md",
                        placeholder="Selecione um template...",
                        on_change=OnboardingsState.set_template
                    ),
                    spacing='1',
                    width='100%'
                ),
                rx.vstack(
                    rx.text("Data de início", class_name="text-sm font-medium"),
                    rx.input(
                        name="start_date",
                        type="date",
                        width='100%',
                        size='3',
                        on_change=OnboardingsState.set_datainicio
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
                        on_change=OnboardingsState.set_comentario
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
                        on_click=OnboardingsState.create_onboarding,
                    ),
                    spacing='1',
                    width='100%',
                    justify='between'
                ),
            ),
            style={"max_width": "500px"},
        ),
        open=OnboardingsState.show_create_dialog,
        on_open_change=OnboardingsState.toggle_create_dialog,
    )