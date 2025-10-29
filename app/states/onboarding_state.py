import reflex as rx
from typing import TypedDict
from app.models.processo import Tarefa

class TarefaDict(TypedDict):
    id: int | None = None
    nome: str
    concluido: bool = False
    responsavel: str | None = None
    prazo: str | None = None


class EtapaDict(TypedDict):
    nome: str
    tarefas: list[TarefaDict]


class ProcessoDict(TypedDict):
    nome: str
    etapas: list[EtapaDict]


class OnboardingState(rx.State):
    processo: ProcessoDict = {
        "nome": "Plano de Onboarding Superlógica + Cliente A",
        "etapas": [
            {
                "nome": "Etapa 1: Kick-off",
                "tarefas": [
                    {
                        "nome": "Reunião de alinhamento inicial",
                        "concluido": True,
                        "responsavel": "Fulano",
                        "prazo": "20/10/2025",
                    },
                    {
                        "nome": "Definir escopo do projeto",
                        "concluido": False,
                        "responsavel": "Ciclano",
                        "prazo": "21/10/2025",
                    },
                ],
            },
            {
                "nome": "Etapa 2: Configuração",
                "tarefas": [
                    {
                        "nome": "Configurar ambiente de produção",
                        "concluido": False,
                        "responsavel": "Beltrano",
                        "prazo": "25/10/2025",
                    },
                    {
                        "nome": "Treinamento da equipe do cliente",
                        "concluido": False,
                        "responsavel": "Fulano",
                        "prazo": "28/10/2025",
                    },
                ],
            },
        ],
    }
    participants: list[dict[str, str]] = [
        {
            "nome": "Fulano",
            "email": "fulano@cliente.com",
            "cargo": "Gerente",
            "tag": "Pessoa chave",
        },
        {
            "nome": "Ciclano",
            "email": "ciclano@cliente.com",
            "cargo": "Analista",
            "tag": "",
        },
        {
            "nome": "Beltrano",
            "email": "beltrano@cliente.com",
            "cargo": "Desenvolvedor",
            "tag": "",
        },
    ]
    new_etapa_name: str = ""
    new_task_details: dict[int, dict[str, str]] = {}

    @rx.var
    def total_tasks(self) -> int:
        return sum((len(etapa["tarefas"]) for etapa in self.processo["etapas"]))

    @rx.var
    def completed_tasks(self) -> int:
        return sum(
            (
                1
                for etapa in self.processo["etapas"]
                for tarefa in etapa["tarefas"]
                if tarefa["concluido"]
            )
        )

    @rx.var
    def progress_percentage(self) -> float:
        return (
            self.completed_tasks / self.total_tasks * 100 if self.total_tasks > 0 else 0
        )

    @rx.event
    def toggle_task_completion(self, etapa_idx: int, tarefa_idx: int):
        self.processo["etapas"][etapa_idx]["tarefas"][tarefa_idx][
            "concluido"
        ] = not self.processo["etapas"][etapa_idx]["tarefas"][tarefa_idx]["concluido"]

    @rx.event
    def add_etapa(self):
        if self.new_etapa_name:
            self.processo["etapas"].append({"nome": self.new_etapa_name, "tarefas": []})
            self.new_etapa_name = ""

    @rx.event
    def set_new_task_detail(self, etapa_idx: int, field: str, value: str):
        if etapa_idx not in self.new_task_details:
            self.new_task_details[etapa_idx] = {}
        self.new_task_details[etapa_idx][field] = value

    @rx.event
    def add_task(self, etapa_idx: int):
        details = self.new_task_details.get(etapa_idx, {})
        if details.get("nome"):
            new_task: TarefaDict = {
                "nome": details["nome"],
                "concluido": False,
                "responsavel": None,
                "prazo": None,
            }
            self.processo["etapas"][etapa_idx]["tarefas"].append(new_task)
            self.new_task_details[etapa_idx] = {}