import reflex as rx
from typing import List
from app.models.processo import Processo, Template
from datetime import datetime
from sqlmodel import select
from app.utils.integrador import Integracao

class OnboardingsState(rx.State):
    processos: List['Processo'] = []
    loading_processos: bool = True

    show_create_dialog: bool = False
    nome: str = ""
    cliente: str = ""
    template: str = ""
    data_inicio: str = ""
    comentario: str = ""
    onboardings: list = []
    
    templates = [
        "Template 1",
        "Template 2",
        "Template 3"
    ]

    def lista_processos(self):
        with rx.session() as session:
            dados = session.exec(
                select(Processo)
            ).all()
            print(dados)
            self.processos = dados
            self.loading_processos = False

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
    def toggle_create_dialog(self, open: bool):
        self.show_create_dialog = open

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

            try:
                self.lista_processos()
                yield rx.toast("Onboarding criado", duration=4000)
            except Exception as e:
                print("Erro ao recarregar detalhes após criar tarefa:", e)

    @rx.event
    def deletar_onboarding(self):
        try:
            with rx.session() as session:
                o = session.get(Processo, id)
                if not o:
                    print("excluir_tarefa: tarefa não encontrada no DB:", id)
                else:
                    session.delete(o)
                    session.commit()
                    yield rx.toast("Tarefa excluída com sucesso", duration=4000)

                    try:
                        self.lista_processos()
                    except Exception as e:
                        print("Erro ao recarregar detalhes após excluir processo:", e)
        except Exception as e:
            print("excluir_tarefa: erro ao deletar no DB:", e)



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

    