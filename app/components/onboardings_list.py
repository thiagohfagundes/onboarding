import reflex as rx
from app.states.onboardings_list import OnboardingPageState

def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.badge(
        status,
        class_scheme=rx.match(
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
            "px-2 py-1 text-xs font-medium text-gray-800 bg-gray-100 rounded-full",
        ),
    )

def progress_bar(progresso: rx.Var[int]) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(f"{progresso} %", width='100%'),
            rx.progress(
                value=progresso,
                color_scheme=rx.cond(
                    progresso == 100,
                    'grass',
                    'cyan'
                ),
            ),
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
            rx.el.form(
                rx.el.div(
                    rx.el.label("Nome do onboarding (identificador)", class_name="text-sm font-medium"),
                    rx.input(
                        name="name",
                        placeholder="ex: Onboarding Cliente A",
                        width='100%',
                        size='3'
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Nome do cliente", class_name="text-sm font-medium"),
                    rx.input(
                        name="client",
                        placeholder="ex: Imobiliária ABC",
                        width='100%',
                        size='3'
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Template", class_name="text-sm font-medium"),
                    rx.el.select(
                        rx.el.option("Começar do zero (sem template)"),
                        rx.foreach(
                            OnboardingPageState.templates,
                            lambda template: rx.el.option(template, value=template),
                        ),
                        name="template",
                        class_name="mt-1 w-full p-2 border rounded-md",
                        placeholder="Select a template...",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Data de início", class_name="text-sm font-medium"),
                    rx.input(
                        name="start_date",
                        type="date",
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
                on_submit=OnboardingPageState.create_onboarding,
                reset_on_submit=True,
            ),
            style={"max_width": "500px"},
        ),
        open=OnboardingPageState.show_create_dialog,
        on_open_change=OnboardingPageState.toggle_create_dialog,
    )