import reflex as rx
from datetime import datetime
from typing import List, Optional
import sqlmodel

class Cliente(rx.Model, table=True):
    nome: str

class Tarefa(rx.Model, table=True):
    nome: str | None = None
    responsavel: str | None = None
    data_criacao: datetime | None = None
    data_ult_modif: datetime | None = None
    data_conclusao: datetime | None = None
    prazo: datetime | None = None

class Etapa(rx.Model, table=True):
    nome: str | None = None

class Template(rx.Model, table=True):
    nome: str
    descricao: str
    data_criacao: datetime | None = None

class Processo(rx.Model, table=True):
    nome: str
    descricao: str
    cliente: str | None = None
    template: str | None = None
    status: str = "Ativo"
    progresso: int = 0
    data_criacao: datetime | None = None
    data_inicio: datetime | None = None