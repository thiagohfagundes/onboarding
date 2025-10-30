import reflex as rx

class Equipe(rx.Model, table=True):
    nome: str | None = None

class Usuario(rx.Model, table=True):
    id: str
    nome: str | None = None
    cargo: str | None = None
    # empresa

class Empresa(rx.Model, table=True):
    nome: str | None = None
    dominio_email: str | None = None