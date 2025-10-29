import reflex as rx
from app.states.onboarding_state import OnboardingState

def return_link() -> rx.Component:
    return rx.hstack(
        rx.icon("circle-arrow-left", size=20),
        rx.text("Lista de onboardings"),
        spaging="2",
        align="center",
        margin = "1em"
    )

class TaskSelectState(rx.State):
    task_id: int | None = None

    @rx.event
    def set_task(self, id):
        self.task_id = id
        print(id)
        print(self.task_id)

def _render_task(tarefa: rx.Var[dict], etapa_idx: int, tarefa_idx: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=tarefa["concluido"],
                on_change=lambda: OnboardingState.toggle_task_completion(
                    etapa_idx, tarefa_idx
                ),
                class_name="form-checkbox h-5 w-5 text-teal-600 rounded focus:ring-teal-500 cursor-pointer",
            ),
            rx.el.span(
                tarefa["nome"],
                class_name=rx.cond(
                    tarefa["concluido"],
                    "ml-3 text-gray-500 line-through",
                    "ml-3 text-gray-800",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(
                tarefa["responsavel"], class_name="text-sm font-medium text-gray-600"
            ),
            rx.el.span(tarefa["prazo"], class_name="text-sm text-gray-500"),
            rx.icon("trash-2", size=20),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg",
        on_click = lambda: TaskSelectState.set_task(tarefa["id"])
    )


def _add_task_form(etapa_idx: int) -> rx.Component:
    return rx.el.div(
        rx.input(
            placeholder="Nome da Tarefa",
            on_change=lambda value: OnboardingState.set_new_task_detail(
                etapa_idx, "nome", value
            ),
            class_name="flex-grow",
            size="3"
        ),
        rx.button(
            "Adicionar Tarefa",
            size="3",
            on_click=lambda: OnboardingState.add_task(etapa_idx),
        ),
        class_name="flex items-center gap-2 mt-4 p-3 bg-gray-50 rounded-lg",
    )


def _render_etapa(etapa: rx.Var[dict], index: int) -> rx.Component:
    return rx.el.div(
        rx.heading(
            etapa["nome"],
            class_name="text-lg font-semibold text-gray-800",
            bg = rx.color("blue", 4),
            size="3",
            padding="1em"
        ),
        rx.box(
            rx.foreach(
                etapa["tarefas"],
                lambda tarefa, tarefa_idx: _render_task(tarefa, index, tarefa_idx),
            ),
            class_name="space-y-2 p-1",
        ),
        _add_task_form(index),
        class_name="border border-gray-200 rounded-xl shadow-sm",
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
                rx.el.div(OnboardingState.processo["nome"], class_name="text-gray-600"),
                class_name="p-3 rounded-lg shadow-sm",
                bg=rx.color("gray", 4)
            ),
            rx.el.div(
                rx.el.div(
                    "Início: 22/10/2025", class_name="font-semibold"
                ),
                rx.el.div("Término previsto: 22/10/2025", class_name="text-gray-600"),
                class_name="p-3 rounded-lg shadow-sm",
                bg=rx.color("gray", 4)
            ),
            class_name="flex justify-between p-4 gap-4",
        ),
        class_name="rounded-xl shadow-md mb-6 border border-gray-200",
    )


def onboarding_progress() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Progresso do onboarding:", class_name="font-semibold text-gray-700"
            ),
            rx.el.p(
                f"{OnboardingState.completed_tasks} / {OnboardingState.total_tasks} tarefas",
                class_name="font-medium text-gray-600",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name="bg-teal-500 h-2 rounded-full",
                style={"width": OnboardingState.progress_percentage.to_string() + "%"},
            ),
            class_name="w-full bg-gray-200 rounded-full h-2",
        ),
        class_name="p-4 rounded-xl shadow-md mb-6 border border-gray-200",
    )


def participants_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Participantes", class_name="text-xl font-bold text-gray-800"),
            rx.button(
                "Adicionar",
                size="3"
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.foreach(
                OnboardingState.participants,
                lambda p: rx.el.div(
                    rx.el.span(p["nome"], class_name="font-semibold text-gray-800"),
                    rx.el.span(p["email"], class_name="text-gray-600"),
                    rx.el.span(p["cargo"], class_name="text-gray-500"),
                    rx.cond(
                        p["tag"],
                        rx.el.span(
                            p["tag"],
                            class_name="bg-sky-100 text-sky-700 text-xs font-semibold px-2.5 py-1 rounded-full",
                        ),
                        None,
                    ),
                    class_name="flex items-center gap-4 p-2",
                ),
            ),
            class_name="space-y-1",
        ),
        class_name="p-6 rounded-xl shadow-md mb-8 border border-gray-200",
    )


def onboarding_steps() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Etapas do onboarding",
            class_name="text-xl font-bold text-center mb-6",
        ),
        rx.el.div(
            rx.foreach(OnboardingState.processo["etapas"], _render_etapa),
            class_name="space-y-6",
        ),
        rx.el.div(
            rx.input(
                placeholder="Nome da nova etapa",
                on_change=OnboardingState.set_new_etapa_name,
                class_name="flex-grow",
                size="3",
                default_value=OnboardingState.new_etapa_name,
            ),
            rx.button(
                "Adicionar Etapa",
                size="3",
                on_click=OnboardingState.add_etapa,                            
            ),
            class_name="mt-8 flex gap-4 p-4 bg-white rounded-xl shadow-sm border border-gray-200",
        ),
        class_name="w-full",
    )