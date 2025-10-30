import reflex as rx
from typing import List
from app.models.processo import Processo, Template
from datetime import datetime
from sqlmodel import select

class OnboardingsState(rx.State):
    show_create_dialog: bool = False
    nome: str = ""
    cliente: str = ""
    template: str = ""
    data_inicio: str = ""
    comentario: str = ""
    
    templates = [
        "Template 1",
        "Template 2",
        "Template 3"
    ]

    @rx.event
    def set_nome(self, nome: str):
        self.nome = nome

    @rx.event
    def set_cliente(self, cliente: str):
        self.cliente = cliente

    @rx.event
    def set_datainicio(self, data_inicio: str):
        self.data_inicio = data_inicio

    @rx.event
    def set_template(self, template: str):
        self.template = template

    @rx.event
    def set_comentario(self, comentario: str):
        self.comentario = comentario

    @rx.event
    def create_onboarding(self):

        #criar o onboarding
        with rx.session() as session:
            session.add(
                Processo(
                    nome=self.nome,
                    descricao=self.comentario,
                    cliente=self.cliente,
                    data_criacao=datetime.now(),
                    data_inicio=datetime.now() # CORRIGIR
                )
            )
            session.commit()
            self.show_create_dialog = False
            yield rx.toast("Onboarding criado, atualize a tela.", duration=4000)
        rx.redirect("/")

    @rx.event
    def toggle_create_dialog(self, open: bool):
        self.show_create_dialog = open


class TemplatesState(rx.State):
    show_create_dialog: bool = False

    templates: List['Template'] = []
    nome: str = None
    comentario: str = None

    def set_nome(self, nome: str):
        self.nome = nome

    def set_comentario(self, comentario: str):
        self.comentario = comentario

    def lista_templates(self):
        with rx.session() as session:
            dados = session.exec(
                select(Template)
            ).all()
            print(dados)
            self.templates = dados

    @rx.event
    def criar_template(self):    
        nome = self.nome
        comentario = self.comentario

        with rx.session() as session:
            session.add(
                Template(
                    nome=nome,
                    descricao=comentario,
                    data_criacao=datetime.now(),
                )
            )
            session.commit()
        self.show_create_dialog = False
        yield rx.toast("Template criado, atualize a tela.", duration=4000)
    
    @rx.event
    def deletar_template(self, id):
        print(f"deletar {id}") # TERMINAR

    @rx.event
    def toggle_create_dialog(self, open: bool):
        self.show_create_dialog = open

    @rx.event
    def ir_para(self, id: int):
        url = f"/templates/{id}"
        print(url)
        rx.redirect("/")

    