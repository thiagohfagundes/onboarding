import reflex as rx
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship

class Cliente(rx.Model, table=True):
    nome: str

class Template(rx.Model, table=True):
    nome: str
    descricao: str
    data_criacao: datetime | None = None

class Processo(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    cliente: Optional[str] = None
    template: Optional[str] = None
    status: str = "Ativo"
    progresso: int = 0
    data_criacao: Optional[datetime] = None
    data_inicio: Optional[datetime] = None
    etapas: Optional[List["Etapa"]] = Relationship(back_populates="processo")


class Etapa(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: Optional[str] = None
    processo_id: Optional[int] = Field(default=None, foreign_key="processo.id")
    processo: Optional[Processo] = Relationship(back_populates="etapas")
    tarefas: Optional[List["Tarefa"]] = Relationship(back_populates="etapa")


class Tarefa(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: Optional[str] = None
    responsavel: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_ult_modif: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None
    prazo: Optional[datetime] = None

    etapa_id: Optional[int] = Field(default=None, foreign_key="etapa.id")
    etapa: Optional[Etapa] = Relationship(back_populates="tarefas")